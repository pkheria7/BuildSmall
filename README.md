---
title: BuildSmall KnowledgeHub
emoji: 📚
colorFrom: cyan
colorTo: lime
sdk: gradio
sdk_version: 6.17.3
app_file: app.py
pinned: false
license: mit
short_description: Ingest PDFs, arXiv papers, and YouTube transcripts into Qdrant with NVIDIA-powered RAG.
---

# BuildSmall KnowledgeHub

BuildSmall KnowledgeHub is a modular Gradio app for loading knowledge from:

- YouTube links with public transcripts/captions
- arXiv links or IDs
- PDF documents

It extracts text, chunks it, embeds chunks locally with the configured NVIDIA Nemotron embedding model, uploads vectors into Qdrant, and generates grounded answers with NVIDIA's OpenAI-compatible chat API.

## NVIDIA Usage

This project explicitly uses NVIDIA in two places:

- Local retrieval embedding model: `nvidia/llama-nemotron-colembed-vl-3b-v2`
- NVIDIA API chat model: `nvidia/nvidia-nemotron-nano-9b-v2`

The chat client calls:

```text
https://integrate.api.nvidia.com/v1
```

You must provide `NVIDIA_API_KEY` as a Hugging Face Space secret or in your local `.env`.

## Hugging Face Spaces Deployment

Create a new Hugging Face Space with:

- SDK: `Gradio`
- App file: `app.py`
- Hardware: `ZeroGPU` if available, otherwise CPU/GPU according to your quota
- Python dependencies: installed from `requirements.txt`

Push this repository to the Space repo:

```bash
git remote add space https://huggingface.co/spaces/<your-username>/<your-space-name>
git push space main
```

For ZeroGPU Spaces, add these Space variables:

```bash
ENABLE_ZEROGPU=true
EMBEDDING_DEVICE=cuda
ZEROGPU_DURATION_SECONDS=180
```

For local Apple Silicon development, keep:

```bash
EMBEDDING_DEVICE=cpu
```

The Gradio ingest, search, and answer callbacks are decorated with `spaces.GPU` when running on Hugging Face Spaces. Locally, the decorator becomes a no-op.

## Hugging Face Secrets

Add these in your Space settings under **Settings → Variables and secrets**.

Required secrets:

```bash
NVIDIA_API_KEY=<your-nvidia-api-key>
QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-qdrant-api-key>
```

Optional variables:

```bash
QDRANT_COLLECTION_NAME=knowledge_base
NVIDIA_API_URL=https://integrate.api.nvidia.com/v1
NVIDIA_CHAT_MODEL=nvidia/nvidia-nemotron-nano-9b-v2
NEMOTRON_EMBED_MODEL=nvidia/llama-nemotron-colembed-vl-3b-v2
NEMOTRON_PARSE_MODEL=Qwen/Qwen2-VL-2B-Instruct
HF_TOKEN=<token-if-needed-for-gated-model-downloads>
```

Use a hosted Qdrant instance for Hugging Face Spaces. `localhost:6333` only works for local development.

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
