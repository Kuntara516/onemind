"""
Context Compression interface.

Defines the contract between Context Compression
service and concrete compression implementations.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from abc import ABC, abstractmethod

from .models import CompressionRequest, CompressionResult


class ContextCompressionInterface(ABC):
    """
    Abstract contract for context compression.

    Implementations are responsible for reducing
    context size while preserving important information.

    Future compression capabilities:

    - token-aware compression
    - semantic deduplication
    - LLM summarization
    - adaptive compression strategy
    - context window optimization
    """

    @abstractmethod
    async def compress(
        self,
        request: CompressionRequest,
    ) -> CompressionResult:
        """
        Execute context compression.

        Args:
            request:
                Compression request containing
                context candidates and constraints.

        Returns:
            CompressionResult containing optimized context.
        """

        raise NotImplementedError
