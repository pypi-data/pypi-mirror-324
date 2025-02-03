from contextlib import closing
from dataclasses import dataclass, asdict
from typing import Any, Generator, Optional, TypeAlias

from llmtricks.clients import get_groq_client

# Type alias for clarity
ThoughtStream: TypeAlias = Generator[tuple[str, Optional[Any]], None, None]


@dataclass(frozen=True)  # Make immutable since it's just config
class ThinkingParams:
    temperature: float = 0.6
    max_completion_tokens: int = 8096
    top_p: float = 0.95


def think(prompt: str, **kwargs) -> ThoughtStream:
    """Generate thought chunks from an LLM prompt.

    Args:
        prompt: The input prompt to generate thoughts from
        **kwargs: Additional parameters to pass to the model

    Yields:
        Tuples of (thought_chunk, stream), where thought_chunk is a string and
        stream is the underlying response stream (or None for final chunk)
    """
    # Merge default params with overrides, excluding incompatible streaming params
    params = {
        k: v
        for k, v in {**asdict(ThinkingParams()), **kwargs}.items()
        if k not in {"stream", "stop"}
    }

    client = get_groq_client()
    with closing(
        client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            stop=None,
            **params,
        )
    ) as stream:
        chunks: list[str] = []
        in_thinking = False

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if "<think>" in content:
                in_thinking = True
                continue
            if "</think>" in content:
                break

            chunks.append(content)
            if in_thinking and content.endswith("\n\n"):
                yield "".join(chunks), stream
                chunks.clear()

        if chunks:  # Yield any remaining content
            yield "".join(chunks), None
