import logging
import traceback

import gradio as gr

from app.core.config import settings
from app.ui.theme import CSS, HEAD, JS
from app.utils.zerogpu import gpu

logger = logging.getLogger(__name__)

THEME = gr.themes.Base(
    primary_hue="teal",
    secondary_hue="yellow",
    neutral_hue="stone",
    radius_size="sm",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "monospace"],
)

# Fixed pipeline constants
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
RETRIEVE_K = 3


def _format_metadata(metadata: dict) -> str:
    if not metadata:
        return "No metadata found."
    rows = []
    for key, value in metadata.items():
        rows.append(f"**{key}**: {value}")
    return "\n\n".join(rows)


@gpu()
def _ingest(
    url: str,
    pdf_file: str | None,
    collection_name: str,
):
    logger.info(
        "Ingest requested url=%s pdf_file=%s chunk_size=%s chunk_overlap=%s collection=%s",
        url,
        pdf_file,
        CHUNK_SIZE,
        CHUNK_OVERLAP,
        collection_name,
    )
    try:
        from app.services.ingestion import ingest_source

        result = ingest_source(
            url=url,
            pdf_path=pdf_file,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            collection_name=collection_name,
        )
        document = result.document
        status = (
            f"### Ingestion complete\n\n"
            f"Uploaded **{len(result.chunks)} chunks** into Qdrant collection "
            f"`{result.collection_name}`.\n\n"
            f"Saved extracted text to `{result.export_path}`."
        )
        preview = document.text[:12000]
        if len(document.text) > len(preview):
            preview += "\n\n[Preview truncated in UI. Full text is saved in the export file.]"
        return (
            status,
            document.title,
            document.source_type.value,
            str(len(document.text)),
            str(len(result.chunks)),
            _format_metadata(document.metadata),
            preview,
            str(result.export_path),
        )
    except Exception as exc:
        return (
            f"### Ingestion failed\n\n`{type(exc).__name__}: {exc}`\n\n```text\n{traceback.format_exc(limit=2)}\n```",
            "",
            "",
            "0",
            "0",
            "",
            "",
            "",
        )


@gpu()
def _search(query: str, collection_name: str):
    logger.info("Search requested query=%s limit=%s collection=%s", query, RETRIEVE_K, collection_name)
    try:
        from app.services.ingestion import search_knowledge_base

        results = search_knowledge_base(query, limit=RETRIEVE_K, collection_name=collection_name)
    except Exception as exc:
        if "MPS backend out of memory" in str(exc):
            return (
                "### Search failed\n\n"
                "The local embedding model ran out of Apple GPU memory. "
                "Restart the app so the new CPU embedding setting takes effect. "
                "Keep `EMBEDDING_DEVICE=cpu` in `.env`."
            )
        return f"### Search failed\n\n`{type(exc).__name__}: {exc}`"

    if not results:
        return "No matches found."

    blocks = []
    for index, result in enumerate(results, start=1):
        excerpt = result.text[:1200]
        blocks.append(
            "\n".join(
                [
                    f"### {index}. {result.title}",
                    f"**Score:** {result.score:.4f}",
                    f"**Source:** {result.source_type} | {result.source}",
                    "",
                    excerpt,
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


@gpu()
def _answer(query: str, collection_name: str):
    logger.info("Answer requested query=%s limit=%s collection=%s", query, RETRIEVE_K, collection_name)
    try:
        from app.services.ingestion import answer_from_knowledge_base

        result = answer_from_knowledge_base(query, limit=RETRIEVE_K, collection_name=collection_name)
    except Exception as exc:
        if "MPS backend out of memory" in str(exc):
            return (
                "### Answer failed\n\n"
                "The local embedding model ran out of Apple GPU memory. "
                "Restart the app so the new CPU embedding setting takes effect. "
                "Keep `EMBEDDING_DEVICE=cpu` in `.env`.",
                "",
                "",
            )
        return f"### Answer failed\n\n`{type(exc).__name__}: {exc}`", "", ""

    context_blocks = []
    for index, item in enumerate(result.context, start=1):
        context_blocks.append(
            "\n".join(
                [
                    f"### [{index}] {item.title}",
                    f"**Score:** {item.score:.4f}",
                    f"**Source:** {item.source_type} | {item.source}",
                    "",
                    item.text[:1000],
                ]
            )
        )

    reasoning = result.reasoning or "No reasoning content was returned by the API."
    return result.answer, reasoning, "\n\n---\n\n".join(context_blocks)


def build_app() -> gr.Blocks:
    with gr.Blocks(
        title=f"{settings.PROJECT_NAME} Ingestor",
    ) as demo:
        with gr.Column(elem_id="kh-shell"):
            # Room Tag badge inside the chalkboard frame
            gr.HTML(
                f'<div class="kh-room-tag">ROOM: {settings.QDRANT_COLLECTION_NAME}</div>',
                elem_id="kh-room-container"
            )
            gr.Markdown(
                f"""
# KnowledgeMesh
*push papers · ask questions · study together*
""",
                elem_id="kh-title",
            )
            gr.HTML(
                f"""
<div class="kh-chip-row">
  <div class="kh-chip">Embeddings <code>{settings.NEMOTRON_EMBED_MODEL}</code></div>
  <div class="kh-chip">Parser <code>{settings.NEMOTRON_PARSE_MODEL}</code></div>
  <div class="kh-chip">Chat <code>{settings.NVIDIA_CHAT_MODEL}</code></div>
  <div class="kh-chip">Collection <code>{settings.QDRANT_COLLECTION_NAME}</code></div>
  <div class="kh-chip">Sources PDF · arXiv · Medium</div>
</div>
""",
            )

            with gr.Tabs():
                with gr.Tab("Ingest"):
                    with gr.Row(equal_height=True):
                        with gr.Column(scale=5, elem_classes=["kh-panel"]):
                            gr.Markdown(
                                "### Push source\n<div class='kh-subhead'>Upload a PDF or paste one link. The pipeline handles extraction, chunking, local embeddings, and Qdrant upload.</div>"
                            )
                            source_url = gr.Textbox(
                                label="Medium or arXiv input",
                                placeholder="Paste a Medium article URL, arXiv URL, or arXiv ID",
                                lines=2,
                            )
                            pdf_file = gr.File(
                                label="PDF document",
                                file_types=[".pdf"],
                                type="filepath",
                            )
                            collection_name_ingest = gr.Textbox(
                                label="Collection Name",
                                value=settings.QDRANT_COLLECTION_NAME,
                                placeholder="Enter Qdrant collection name",
                            )
                            ingest_btn = gr.Button("Write to board →", variant="primary")

                        with gr.Column(scale=4, elem_classes=["kh-panel"]):
                            gr.Markdown("### Pipeline Status")
                            status = gr.Markdown(elem_id="kh-status")
                            with gr.Row():
                                title = gr.Textbox(
                                    label="Title",
                                    interactive=False,
                                    elem_classes=["kh-stat"],
                                )
                                source_type = gr.Textbox(
                                    label="Type",
                                    interactive=False,
                                    elem_classes=["kh-stat"],
                                )
                            with gr.Row():
                                char_count = gr.Textbox(
                                    label="Characters",
                                    interactive=False,
                                    elem_classes=["kh-stat"],
                                )
                                chunk_count = gr.Textbox(
                                    label="Chunks",
                                    interactive=False,
                                    elem_classes=["kh-stat"],
                                )
                            export_path = gr.Textbox(label="Export file", interactive=False)

                    with gr.Row(equal_height=True):
                        metadata = gr.Markdown(label="Metadata", elem_classes=["kh-panel"])
                        text_preview = gr.Textbox(
                            label="Extracted text preview",
                            lines=18,
                            interactive=False,
                            elem_id="kh-text-preview",
                            elem_classes=["kh-panel"],
                        )

                    ingest_btn.click(
                        fn=_ingest,
                        inputs=[
                            source_url,
                            pdf_file,
                            collection_name_ingest,
                        ],
                        outputs=[
                            status,
                            title,
                            source_type,
                            char_count,
                            chunk_count,
                            metadata,
                            text_preview,
                            export_path,
                        ],
                    )

                with gr.Tab("Retrieve"):
                    with gr.Row(equal_height=True):
                        with gr.Column(scale=3, elem_classes=["kh-panel"]):
                            gr.Markdown(
                                "### Ask the room\n<div class='kh-subhead'>Run a similarity search against the Qdrant collection. Returns top 3 matches.</div>"
                            )
                            query = gr.Textbox(
                                label="Search query",
                                placeholder="Ask a question or enter keywords",
                                lines=4,
                            )
                            collection_name_retrieve = gr.Textbox(
                                label="Collection Name",
                                value=settings.QDRANT_COLLECTION_NAME,
                                placeholder="Enter Qdrant collection name",
                            )
                            with gr.Row():
                                search_btn = gr.Button("Search", variant="secondary")
                                answer_btn = gr.Button("Answer", variant="primary")
                            gr.HTML(
                                """
                                <div class="kh-retrieve-status">
                                  <div class="kh-online-status">
                                    <span class="kh-dot green"></span>
                                    <span class="kh-dot green"></span>
                                    <span class="kh-dot green"></span>
                                    <span class="kh-online-text">2/4 online</span>
                                  </div>
                                  <div class="kh-brackets">[ ]</div>
                                </div>
                                """
                            )
                        with gr.Column(scale=5, elem_classes=["kh-panel"]):
                            gr.Markdown("### Answer")
                            answer_output = gr.Markdown(elem_id="kh-answer")

                    with gr.Row(equal_height=True):
                        with gr.Column(elem_classes=["kh-panel"]):
                            gr.Markdown("### Matches")
                            search_results = gr.Markdown(elem_id="kh-search-results")
                        with gr.Column(elem_classes=["kh-panel"]):
                            gr.Markdown("### Reasoning")
                            reasoning_output = gr.Markdown(elem_id="kh-reasoning")

                    search_btn.click(
                        fn=_search,
                        inputs=[query, collection_name_retrieve],
                        outputs=search_results,
                    )
                    answer_btn.click(
                        fn=_answer,
                        inputs=[query, collection_name_retrieve],
                        outputs=[answer_output, reasoning_output, search_results],
                    )

            # Wooden chalk tray with white, yellow, and purple chalk pieces resting on it
            gr.HTML(
                """
                <div class="kh-bottom-tray">
                  <div class="kh-chalks">
                    <span class="kh-chalk white"></span>
                    <span class="kh-chalk yellow"></span>
                    <span class="kh-chalk purple"></span>
                  </div>
                  <div class="kh-watermark">NVIDIA · Qdrant · k=3</div>
                </div>
                """,
                elem_id="kh-bottom-container"
            )

    return demo


def serve() -> None:
    logger.info("Building Gradio app")
    demo = build_app()
    logger.info("Launching Gradio server on 0.0.0.0:7860")
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        theme=THEME,
        css=CSS,
        js=JS,
        head=HEAD,
    )
