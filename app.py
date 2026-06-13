import logging
import shutil
import sys
from pathlib import Path

#only comments adding
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def _clear_app_bytecode() -> None:
    sys.dont_write_bytecode = True
    for cache_dir in Path(__file__).resolve().parent.joinpath("app").rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


if __name__ == "__main__":
    logger.info("Preparing BuildSmall app")
    _clear_app_bytecode()
    logger.info("Loading Gradio UI")
    from app.ui.gradio_app import serve

    logger.info("Launching BuildSmall app")
    serve()
    logger.info("BuildSmall app stopped")
