import re
import uuid

from app.core.models import Chunk, Document


def chunk_document(document: Document, chunk_size: int, overlap: int) -> list[Chunk]:
    if overlap >= chunk_size:
        raise ValueError("Chunk overlap must be smaller than chunk size.")

    normalized = re.sub(r"\n{3,}", "\n\n", document.text).strip()
    if not normalized:
        raise ValueError("Document is empty after extraction.")

    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        if end < len(normalized):
            paragraph_break = normalized.rfind("\n\n", start, end)
            sentence_break = normalized.rfind(". ", start, end)
            best_break = max(paragraph_break, sentence_break)
            if best_break > start + chunk_size // 2:
                end = best_break + 1

        text = normalized[start:end].strip()
        if text:
            digest = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{document.source}:{index}:{text[:80]}"))
            chunks.append(
                Chunk(
                    id=digest,
                    text=text,
                    index=index,
                    source_type=document.source_type,
                    source=document.source,
                    title=document.title,
                    metadata=document.metadata,
                )
            )
            index += 1

        if end == len(normalized):
            break
        start = max(0, end - overlap)

    return chunks
