from functools import cached_property, lru_cache

from app.core.config import settings
from app.utils.zerogpu import is_enabled as zerogpu_is_enabled


class LocalEmbeddingClient:
    def __init__(self, model: str | None = None, device: str | None = None):
        self.model_name = model or settings.NEMOTRON_EMBED_MODEL
        self.device = device or _resolve_device()

    @cached_property
    def model(self):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required for local embeddings. "
                "Install dependencies with `pip install -r requirements.txt`."
            ) from exc

        return SentenceTransformer(
            self.model_name,
            device=self.device,
            token=settings.HF_TOKEN or None,
            trust_remote_code=True,
        )

    @cached_property
    def native_model(self):
        try:
            from transformers import AutoModel
        except ImportError as exc:
            raise ImportError(
                "transformers is required for native local embeddings. "
                "Install dependencies with `pip install -r requirements.txt`."
            ) from exc

        model = AutoModel.from_pretrained(
            self.model_name,
            token=settings.HF_TOKEN or None,
            trust_remote_code=True,
            dtype="auto" if self.device != "cpu" else None,
        )
        if self.device:
            model = model.to(self.device)
        return model.eval()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        try:
            embeddings = self.model.encode(
                texts,
                batch_size=8,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            return embeddings.tolist()
        except ValueError as exc:
            if "Modality 'text' is not supported" not in str(exc):
                raise

        embeddings = self._embed_with_native_query_encoder(texts)
        return embeddings.tolist()

    def _embed_with_native_query_encoder(self, texts: list[str]):
        try:
            import torch
            import torch.nn.functional as F
        except ImportError as exc:
            raise ImportError(
                "torch is required for the native Nemotron embedding path. "
                "Install dependencies with `pip install -r requirements.txt`."
            ) from exc

        if not hasattr(self.native_model, "forward_queries"):
            raise ValueError(
                f"{self.model_name} does not support SentenceTransformer text encoding "
                "or a native forward_queries API."
            )

        with torch.no_grad():
            output = self.native_model.forward_queries(texts, batch_size=4)

        if isinstance(output, (list, tuple)):
            output = output[0]

        if not torch.is_tensor(output):
            output = torch.as_tensor(output)

        if output.ndim == 3:
            output = output.float().mean(dim=1)
        elif output.ndim != 2:
            raise ValueError(f"Unexpected embedding shape from {self.model_name}: {tuple(output.shape)}")

        return F.normalize(output.float(), p=2, dim=1).cpu()


@lru_cache(maxsize=1)
def get_embedding_client() -> LocalEmbeddingClient:
    return LocalEmbeddingClient()


def _resolve_device() -> str:
    if zerogpu_is_enabled() and settings.EMBEDDING_DEVICE == "cpu":
        return "cuda"
    return settings.EMBEDDING_DEVICE
