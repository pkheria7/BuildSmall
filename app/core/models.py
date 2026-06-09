from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class SourceType(str, Enum):
    PDF = "pdf"
    ARXIV = "arxiv"
    MEDIUM = "medium"


@dataclass(frozen=True)
class Document:
    source_type: SourceType
    title: str
    text: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    index: int
    source_type: SourceType
    source: str
    title: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IngestionResult:
    document: Document
    chunks: list[Chunk]
    collection_name: str
    export_path: Path


@dataclass(frozen=True)
class SearchResult:
    score: float
    text: str
    title: str
    source: str
    source_type: str
    metadata: dict[str, Any]
