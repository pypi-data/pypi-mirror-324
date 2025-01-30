"""Remote model implementation that supports full message protocol."""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
import json
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import urlparse

import httpx
from pydantic import Field, TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter,
    ModelResponse,
    ModelResponsePart,
    ModelResponseStreamEvent,
    TextPart,
)
from pydantic_ai.models import AgentModel, StreamedResponse
from pydantic_ai.result import Usage

from llmling_models.base import PydanticModel
from llmling_models.log import get_logger


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from pydantic_ai.settings import ModelSettings
    from pydantic_ai.tools import ToolDefinition
    from websockets import ClientConnection

logger = get_logger(__name__)


class RemoteProxyModel(PydanticModel):
    """Model that proxies requests to a remote model server.

    Example YAML configuration:
        ```yaml
        models:
          remote-gpt4:
            type: remote-proxy
            url: ws://model-server:8000/v1/completion  # or http://
            api_key: your-api-key
        ```
    """

    type: Literal["remote-proxy"] = Field(default="remote-proxy", init=False)
    """Discriminator field for model type."""

    url: str = "ws://localhost:8000/v1/completion/stream"
    """URL of the remote model server."""

    api_key: str | None = None
    """API key for authentication."""

    def name(self) -> str:
        """Get model name."""
        return f"remote-proxy({self.url})"

    @property
    def protocol(self) -> Literal["rest", "websocket"]:
        """Infer protocol from URL."""
        scheme = urlparse(self.url).scheme.lower()
        return "websocket" if scheme in ("ws", "wss") else "rest"

    async def agent_model(
        self,
        *,
        function_tools: list[ToolDefinition],
        allow_text_result: bool,
        result_tools: list[ToolDefinition],
    ) -> AgentModel:
        """Create agent model implementation."""
        if self.protocol == "websocket":
            return WebSocketProxyAgent(url=self.url, api_key=self.api_key)
        return RestProxyAgent(url=self.url, api_key=self.api_key)


class RestProxyAgent(AgentModel):
    """Agent implementation using REST API."""

    def __init__(self, url: str, api_key: str | None = None):
        """Initialize with configuration."""
        self.url = url
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.client = httpx.AsyncClient(
            base_url=url,
            headers=headers,
            timeout=30.0,
        )

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None = None,
    ) -> tuple[ModelResponse, Usage]:
        """Make request to remote model."""
        try:
            # Serialize complete message history
            payload = ModelMessagesTypeAdapter.dump_json(messages)

            logger.debug("Sending request to %s", self.url)
            logger.debug("Request payload: %s", payload)

            response = await self.client.post(
                "/v1/completion",
                content=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            # Deserialize response
            data = response.json()
            logger.debug("Received response: %s", data)

            model_response = ModelResponse(
                parts=[TextPart(data["content"])],
                timestamp=datetime.now(UTC),
            )
            usage = Usage(**data.get("usage", {}))
        except httpx.HTTPError as e:
            if hasattr(e, "response") and e.response is not None:  # pyright: ignore
                logger.exception("Error response: %s", e.response.text)  # pyright: ignore
            msg = f"HTTP error: {e}"
            raise RuntimeError(msg) from e
        else:
            return model_response, usage

    async def __aenter__(self):
        """Enter async context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context and cleanup resources."""
        await self.client.aclose()


@dataclass(kw_only=True)
class WebSocketStreamedResponse(StreamedResponse):
    """Stream implementation for WebSocket responses."""

    websocket: ClientConnection
    _timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    _model_name: str = "remote-proxy"

    def __post_init__(self):
        """Initialize the usage tracker."""
        self._usage = Usage()

    async def _get_event_iterator(self) -> AsyncIterator[ModelResponseStreamEvent]:
        """Stream responses as events."""
        import websockets

        try:
            while True:
                raw_data = await self.websocket.recv()
                data = json.loads(raw_data)
                logger.debug("Stream received: %s", data)

                if data.get("error"):
                    msg = f"Server error: {data['error']}"
                    raise RuntimeError(msg)

                if data.get("usage"):
                    self._usage = Usage(**data["usage"])

                if data.get("done", False):
                    break

                chunk = data.get("chunk")
                if chunk:  # Only emit non-empty chunks
                    yield self._parts_manager.handle_text_delta(
                        vendor_part_id="content",
                        content=chunk,
                    )

        except (websockets.ConnectionClosed, ValueError, KeyError) as e:
            msg = f"Stream error: {e}"
            raise RuntimeError(msg) from e

    def timestamp(self) -> datetime:
        """Get response timestamp."""
        return self._timestamp


class WebSocketProxyAgent(AgentModel):
    """Agent implementation using WebSocket connection."""

    response_part_adapter: TypeAdapter[Any] = TypeAdapter(ModelResponsePart)

    def __init__(self, url: str, api_key: str | None = None):
        """Initialize with configuration."""
        self.url = url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None = None,
    ) -> tuple[ModelResponse, Usage]:
        """Make request using WebSocket connection."""
        import websockets

        async with websockets.connect(
            self.url,
            additional_headers=self.headers,
        ) as websocket:
            try:
                # Serialize and send messages
                payload = ModelMessagesTypeAdapter.dump_json(messages)
                logger.debug("Sending WebSocket request: %s", payload)
                await websocket.send(payload)

                # Accumulate response chunks
                chunks: list[str] = []
                usage = Usage()

                while True:
                    raw_data = await websocket.recv()
                    data = json.loads(raw_data)
                    logger.debug("Received WebSocket data: %s", data)

                    if data.get("error"):
                        msg = f"Server error: {data['error']}"
                        raise RuntimeError(msg)

                    if data.get("usage"):
                        usage = Usage(**data["usage"])

                    chunk = data.get("chunk")
                    if chunk is not None:  # Include empty strings but not None
                        chunks.append(chunk)

                    if data.get("done", False):
                        break

                content = "".join(chunks)
                if not content:
                    msg = "Received empty response from server"
                    raise RuntimeError(msg)

                return ModelResponse(parts=[TextPart(content)]), usage

            except (websockets.ConnectionClosed, ValueError, KeyError) as e:
                msg = f"WebSocket error: {e}"
                raise RuntimeError(msg) from e

    @asynccontextmanager
    async def request_stream(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None = None,
    ) -> AsyncIterator[StreamedResponse]:
        """Stream responses using WebSocket connection."""
        import websockets

        websocket = await websockets.connect(
            self.url,
            additional_headers=self.headers,
        )

        try:
            # Send messages
            payload = ModelMessagesTypeAdapter.dump_json(messages)
            await websocket.send(payload)
            yield WebSocketStreamedResponse(websocket=websocket)

        except websockets.ConnectionClosed as e:
            msg = f"WebSocket error: {e}"
            raise RuntimeError(msg) from e
        finally:
            await websocket.close()


if __name__ == "__main__":
    import asyncio
    import logging

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Starting client test...")

    async def test():
        model = RemoteProxyModel(url="ws://localhost:8000/v1/completion/stream")
        agent: Agent[None, str] = Agent(model=model)

        # Test streaming
        logger.info("\nTesting streaming...")
        print("Streaming response:")
        chunk_count = 0

        async with agent.run_stream("Tell me a story about a brave knight") as response:
            # Use stream_text with delta=True instead of stream()
            async for chunk in response.stream_text(delta=True):
                chunk_count += 1
                print(chunk, end="", flush=True)

        print(f"\nStreaming complete! Received {chunk_count} chunks")

    asyncio.run(test())
