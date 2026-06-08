from pathlib import Path

from app.core.config import settings
from app.core.models import Document, IngestionResult, SourceType
from app.extractors.arxiv import extract_arxiv
from app.extractors.pdf import extract_pdf
from app.extractors.youtube import extract_youtube
from app.services.chat import NvidiaChatClient
from app.services.chunking import chunk_document
from app.services.embeddings import get_embedding_client
from app.services.vector_store import QdrantVectorStore
from app.utils.source_detection import detect_source


EXPORT_DIR = Path("data/exports")


def extract_document(
    url: str | None = None,
    pdf_path: str | None = None,
    manual_transcript: str | None = None,
) -> Document:
    source_type = detect_source(url, pdf_path)
    if source_type == SourceType.PDF:
        return extract_pdf(str(pdf_path))
    if source_type == SourceType.ARXIV:
        return extract_arxiv(str(url))
    if source_type == SourceType.YOUTUBE:
        if manual_transcript and manual_transcript.strip():
            return Document(
                source_type=SourceType.YOUTUBE,
                title="YouTube Transcript",
                text=manual_transcript.strip(),
                source=str(url),
                metadata={"transcript_source": "manual"},
            )
        return extract_youtube(str(url))
    raise ValueError(f"Unsupported source type: {source_type}")


def save_markdown(document: Document, chunks_count: int) -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(char if char.isalnum() or char in "-_" else "_" for char in document.title)[:80]
    path = EXPORT_DIR / f"{safe_title or document.source_type.value}.md"
    metadata_lines = "\n".join(f"- {key}: {value}" for key, value in document.metadata.items())
    path.write_text(
        "\n".join(
            [
                f"# {document.title}",
                "",
                f"- Source type: {document.source_type.value}",
                f"- Source: {document.source}",
                f"- Chunks uploaded: {chunks_count}",
                metadata_lines,
                "",
                "## Extracted Text",
                "",
                document.text,
            ]
        ),
        encoding="utf-8",
    )
    return path


def ingest_source(
    url: str | None,
    pdf_path: str | None,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    collection_name: str | None = None,
    manual_transcript: str | None = None,
) -> IngestionResult:
    document = extract_document(url=url, pdf_path=pdf_path, manual_transcript=manual_transcript)
    chunks = chunk_document(
        document,
        chunk_size=chunk_size or settings.CHUNK_SIZE,
        overlap=chunk_overlap or settings.CHUNK_OVERLAP,
    )
    embeddings = get_embedding_client().embed_texts([chunk.text for chunk in chunks])
    store = QdrantVectorStore(collection_name=collection_name)
    store.upsert_chunks(chunks, embeddings)
    export_path = save_markdown(document, len(chunks))
    return IngestionResult(
        document=document,
        chunks=chunks,
        collection_name=store.collection_name,
        export_path=export_path,
    )


def search_knowledge_base(query: str, limit: int = 5, collection_name: str | None = None):
    query_text = query.strip()
    if not query_text:
        raise ValueError("Enter a query to search.")
    embedding = get_embedding_client().embed_texts([query_text])[0]
    return QdrantVectorStore(collection_name=collection_name).search(embedding, limit=limit)


def answer_from_knowledge_base(query: str, limit: int = 5, collection_name: str | None = None):
    results = search_knowledge_base(query, limit=limit, collection_name=collection_name)
    return NvidiaChatClient().answer_with_context(query, results)
