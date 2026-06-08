# KnowledgeHub Ingestor

KnowledgeHub Ingestor is a modular Gradio app for loading knowledge from:

- YouTube links with public transcripts/captions
- arXiv links or IDs
- PDF documents

It extracts text, chunks it, embeds chunks locally with your embedding model, and uploads vectors into Qdrant for retrieval. The answer generation step uses NVIDIA's OpenAI-compatible chat API.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add `NVIDIA_API_KEY` to `.env` for chat completions. Start Qdrant locally or point `QDRANT_URL` to your hosted instance.

The default model split is:

- Local parsing model: `Qwen/Qwen2-VL-2B-Instruct`
- Local embedding model: `nvidia/llama-nemotron-colembed-vl-3b-v2`
- NVIDIA API chat model: `nvidia/nvidia-nemotron-nano-9b-v2`

## Run

```bash
python app.py
```

Open the local Gradio URL printed in the terminal, usually `http://127.0.0.1:7860`.

The app binds to `0.0.0.0:7860`, which is suitable for Hugging Face Spaces and container deployments.

For Hugging Face ZeroGPU Spaces, set:

```bash
ENABLE_ZEROGPU=true
EMBEDDING_DEVICE=cuda
```

The Gradio ingest/search/answer callbacks are decorated with `spaces.GPU` when running on Spaces. Locally, the decorator becomes a no-op.

## Project Structure

```text
app/
  core/        settings and shared models
  extractors/  PDF, arXiv, and YouTube extraction
  services/    chunking, embeddings, Qdrant, retrieval, ingestion orchestration
  ui/          Gradio Blocks UI
  utils/       source detection helpers
```

YouTube extraction requires captions/transcripts to be available for the video. arXiv ingestion downloads the paper PDF and parses it with `pypdf`.
