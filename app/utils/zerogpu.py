import os
from collections.abc import Callable
from typing import TypeVar

from app.core.config import settings


F = TypeVar("F", bound=Callable)


def gpu(duration: int | None = None) -> Callable[[F], F]:
    if not _should_use_zerogpu():
        return _identity

    try:
        import spaces
    except ImportError:
        return _identity

    return spaces.GPU(duration=duration or settings.ZEROGPU_DURATION_SECONDS)


def _identity(func: F) -> F:
    return func


def _should_use_zerogpu() -> bool:
    if os.getenv("DISABLE_ZEROGPU", "").lower() in {"1", "true", "yes"}:
        return False
    if os.getenv("ENABLE_ZEROGPU", "").lower() in {"1", "true", "yes"}:
        return True
    return bool(os.getenv("SPACE_ID"))


def is_enabled() -> bool:
    return _should_use_zerogpu()
