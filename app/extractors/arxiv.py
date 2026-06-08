import tempfile
from pathlib import Path

import arxiv
import requests

from app.core.models import Document, SourceType
from app.extractors.pdf import extract_pdf
from app.utils.source_detection import extract_arxiv_id


def extract_arxiv(value: str) -> Document:
    paper_id = extract_arxiv_id(value)
    client = arxiv.Client()
    search = arxiv.Search(id_list=[paper_id])
    paper = next(client.results(search), None)
    if paper is None:
        raise ValueError(f"No arXiv paper found for {paper_id}.")

    with tempfile.TemporaryDirectory(prefix="knowledgehub_arxiv_") as tmpdir:
        pdf_url = paper.pdf_url or f"https://arxiv.org/pdf/{paper_id}.pdf"
        pdf_path = Path(tmpdir) / f"{paper_id}.pdf"
        response = requests.get(pdf_url, timeout=60)
        response.raise_for_status()
        pdf_path.write_bytes(response.content)

        document = extract_pdf(
            pdf_path,
            title=paper.title,
            metadata={
                "arxiv_id": paper_id,
                "authors": [str(author) for author in paper.authors],
                "published": paper.published.isoformat() if paper.published else None,
                "summary": paper.summary,
                "pdf_url": pdf_url,
                "entry_id": paper.entry_id,
            },
        )

    return Document(
        source_type=SourceType.ARXIV,
        title=document.title,
        text=document.text,
        source=paper.entry_id,
        metadata=document.metadata,
    )
