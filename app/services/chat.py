from dataclasses import dataclass

from openai import OpenAI

from app.core.config import settings
from app.core.models import SearchResult


@dataclass(frozen=True)
class ChatAnswer:
    answer: str
    reasoning: str | None
    context: list[SearchResult]


class NvidiaChatClient:
    def __init__(self):
        if not settings.NVIDIA_API_KEY:
            raise ValueError("NVIDIA_API_KEY is required for NVIDIA chat completions.")

        self.client = OpenAI(
            base_url=settings.NVIDIA_API_URL,
            api_key=settings.NVIDIA_API_KEY,
        )

    def answer_with_context(self, question: str, context: list[SearchResult]) -> ChatAnswer:
        context_text = "\n\n".join(
            [
                (
                    f"[{index}] title={item.title}\n"
                    f"source={item.source}\n"
                    f"score={item.score:.4f}\n"
                    f"text={item.text}"
                )
                for index, item in enumerate(context, start=1)
            ]
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "You are KnowledgeHub's retrieval assistant. Answer only from the "
                    "provided context. If the context is insufficient, say what is missing. "
                    "Cite sources using bracket numbers like [1], [2]."
                ),
            },
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nRetrieved context:\n{context_text}",
            },
        ]
        completion = self.client.chat.completions.create(
            model=settings.NVIDIA_CHAT_MODEL,
            messages=messages,
            temperature=settings.CHAT_TEMPERATURE,
            top_p=settings.CHAT_TOP_P,
            max_tokens=settings.CHAT_MAX_TOKENS,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False,
            extra_body={
                "min_thinking_tokens": settings.MIN_THINKING_TOKENS,
                "max_thinking_tokens": settings.MAX_THINKING_TOKENS,
            },
        )
        message = completion.choices[0].message
        reasoning = getattr(message, "reasoning_content", None)
        return ChatAnswer(answer=message.content or "", reasoning=reasoning, context=context)
