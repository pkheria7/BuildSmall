from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from app.core.config import settings
from app.core.models import Chunk, SearchResult


class QdrantVectorStore:
    def __init__(self, collection_name: str | None = None):
        self.collection_name = collection_name or settings.QDRANT_COLLECTION_NAME
        self.client = QdrantClient(
            url=settings.get_qdrant_url(),
            api_key=settings.QDRANT_API_KEY or None,
            timeout=60,
        )

    def ensure_collection(self, vector_size: int) -> None:
        collections = self.client.get_collections().collections
        exists = any(collection.name == self.collection_name for collection in collections)
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def upsert_chunks(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must have the same length.")
        if not chunks:
            return

        self.ensure_collection(vector_size=len(embeddings[0]))
        points = [
            PointStruct(
                id=chunk.id,
                vector=embedding,
                payload={
                    "text": chunk.text,
                    "chunk_index": chunk.index,
                    "source_type": chunk.source_type.value,
                    "source": chunk.source,
                    "title": chunk.title,
                    "metadata": chunk.metadata,
                },
            )
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_embedding: list[float], limit: int = 5) -> list[SearchResult]:
        if hasattr(self.client, "query_points"):
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=limit,
                with_payload=True,
            )
            hits = response.points
        else:
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True,
            )

        results: list[SearchResult] = []
        for hit in hits:
            payload = hit.payload or {}
            results.append(
                SearchResult(
                    score=float(hit.score),
                    text=str(payload.get("text", "")),
                    title=str(payload.get("title", "")),
                    source=str(payload.get("source", "")),
                    source_type=str(payload.get("source_type", "")),
                    metadata=dict(payload.get("metadata", {})),
                )
            )
        return results
