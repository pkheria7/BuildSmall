from pathlib import Path

from pypdf import PdfReader

from app.core.models import Document, SourceType


def extract_pdf(path: str | Path, title: str | None = None, metadata: dict | None = None) -> Document:
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"\n\n[Page {page_number}]\n{text.strip()}")

    combined_text = "\n".join(pages).strip()
    if not combined_text:
        raise ValueError("No selectable text was found in this PDF.")

    return Document(
        source_type=SourceType.PDF,
        title=title or pdf_path.stem,
        text=combined_text,
        source=str(pdf_path),
        metadata={"pages": len(reader.pages), **(metadata or {})},
    )
