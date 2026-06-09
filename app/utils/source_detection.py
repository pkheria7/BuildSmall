import re
from pathlib import Path
from urllib.parse import urlparse

from app.core.models import SourceType


ARXIV_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/)?(?P<id>\d{4}\.\d{4,5})(?:v\d+)?", re.I)
MEDIUM_HOST_PARTS = ("medium.com", "freedium")


def detect_source(url: str | None, pdf_path: str | None) -> SourceType:
    if pdf_path:
        suffix = Path(pdf_path).suffix.lower()
        if suffix == ".pdf":
            return SourceType.PDF
        raise ValueError("Uploaded file must be a PDF.")

    if not url or not url.strip():
        raise ValueError("Provide a Medium article link, arXiv link/ID, or upload a PDF.")

    clean_url = url.strip()
    parsed = urlparse(clean_url)
    host = parsed.netloc.lower()

    if "arxiv.org" in host or ARXIV_RE.search(clean_url):
        return SourceType.ARXIV
    if parsed.scheme in {"http", "https"}:
        return SourceType.MEDIUM
    raise ValueError("Could not detect source type. Use a Medium URL, arXiv URL/ID, or PDF.")


def extract_arxiv_id(value: str) -> str:
    match = ARXIV_RE.search(value.strip())
    if not match:
        raise ValueError("Could not find a valid arXiv ID.")
    return match.group("id")
