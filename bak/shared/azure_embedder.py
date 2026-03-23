"""
Azure AI Foundry shims for neo4j-agent-memory.

The neo4j-agent-memory package defaults to OpenAI's embedding and LLM APIs,
requiring OPENAI_API_KEY. This module provides embedder and LLM extractor
implementations that use Azure AI Foundry's OpenAI-compatible inference
endpoint with Azure CLI authentication — the same LLM used in Labs 5/6.

Usage:
    from azure_embedder import get_memory_embedder, get_memory_extractor

    # Embedder for MemoryClient (required)
    embedder = get_memory_embedder()
    async with MemoryClient(settings, embedder=embedder) as client:
        ...

    # LLM extractor for MemoryClient (optional, use instead of spacy)
    extractor = get_memory_extractor()
    async with MemoryClient(settings, embedder=embedder, extractor=extractor) as client:
        ...
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from openai import AsyncOpenAI

from neo4j_agent_memory.core.exceptions import EmbeddingError
from neo4j_agent_memory.embeddings.base import BaseEmbedder
from neo4j_agent_memory.extraction.llm_extractor import LLMEntityExtractor

from config import _get_azure_token, get_agent_config

if TYPE_CHECKING:
    from neo4j_agent_memory.extraction.base import EntityExtractor

logger = logging.getLogger(__name__)


class AzureFoundryEmbedder(BaseEmbedder):
    """Embedder using Azure AI Foundry's OpenAI-compatible inference endpoint."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        dimensions: int = 1536,
        batch_size: int = 100,
    ):
        self._base_url = base_url
        self._api_key = api_key
        self._model = model
        self._dimensions = dimensions
        self._batch_size = batch_size
        self._client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed(self, text: str) -> list[float]:
        try:
            response = await self._client.embeddings.create(
                input=text,
                model=self._model,
            )
            return response.data[0].embedding
        except Exception as e:
            raise EmbeddingError(f"Azure embedding failed: {e}") from e

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        try:
            all_embeddings: list[list[float]] = []
            for i in range(0, len(texts), self._batch_size):
                batch = texts[i : i + self._batch_size]
                response = await self._client.embeddings.create(
                    input=batch,
                    model=self._model,
                )
                all_embeddings.extend([item.embedding for item in response.data])
            return all_embeddings
        except Exception as e:
            raise EmbeddingError(f"Azure batch embedding failed: {e}") from e


class AzureFoundryLLMExtractor(LLMEntityExtractor):
    """LLM entity extractor that routes through Azure AI Foundry.

    Subclasses LLMEntityExtractor and overrides _ensure_client() to create
    an AsyncOpenAI client pointed at the Azure inference endpoint.
    All extraction/parsing logic is inherited unchanged.
    """

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str = "gpt-4o",
        entity_types: list[str] | None = None,
        temperature: float = 0.0,
        extract_relations: bool = True,
        extract_preferences: bool = True,
    ):
        super().__init__(
            model=model,
            api_key=api_key,
            entity_types=entity_types,
            temperature=temperature,
            extract_relations=extract_relations,
            extract_preferences=extract_preferences,
        )
        self._base_url = base_url

    def _ensure_client(self):
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._client


def get_memory_embedder() -> AzureFoundryEmbedder | None:
    """Factory that returns a configured AzureFoundryEmbedder, or None for OpenAI.

    When None is returned, MemoryClient will use its default OpenAI embedder.
    """
    config = get_agent_config()
    if config.use_openai:
        return None
    token = _get_azure_token()
    return AzureFoundryEmbedder(
        base_url=config.inference_endpoint,
        api_key=token,
        model=config.embedding_name,
    )


def get_memory_extractor() -> EntityExtractor:
    """Factory that returns an LLM entity extractor configured from environment.

    Use instead of spacy extraction for richer entity/relation/preference
    extraction powered by the same Azure LLM used in Labs 5/6.

    Pass to MemoryClient as: MemoryClient(settings, embedder=..., extractor=extractor)
    """
    config = get_agent_config()

    if config.use_openai:
        return LLMEntityExtractor(
            model=config.model_name,
            api_key=config.openai_api_key,
        )

    token = _get_azure_token()
    return AzureFoundryLLMExtractor(
        model=config.model_name,
        base_url=config.inference_endpoint,
        api_key=token,
    )
