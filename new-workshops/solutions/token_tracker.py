"""
Token Usage Tracking Utility

Provides utilities for tracking token usage across different LLM integrations:
- Agent Framework (azure-ai-projects): Uses built-in UsageDetails
- neo4j-graphrag (OpenAILLM): Wraps the LLM to capture usage from responses
"""

from dataclasses import dataclass, field
from typing import Any, Optional, List, Union

from neo4j_graphrag.llm.openai_llm import OpenAILLM
from neo4j_graphrag.llm.types import LLMResponse
from neo4j_graphrag.message_history import MessageHistory
from neo4j_graphrag.types import LLMMessage


@dataclass
class TokenUsage:
    """Tracks token usage across multiple LLM calls."""

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    call_count: int = 0
    calls: list[dict[str, Any]] = field(default_factory=list)

    def add(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
        total_tokens: int = 0,
        label: str = "",
    ) -> None:
        """Add token counts from a single call."""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens += total_tokens or (input_tokens + output_tokens)
        self.call_count += 1
        self.calls.append({
            "label": label,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens or (input_tokens + output_tokens),
        })

    def add_from_agent_response(self, response: Any, label: str = "") -> None:
        """Add tokens from an AgentRunResponse (agent_framework)."""
        if hasattr(response, "usage_details") and response.usage_details:
            usage = response.usage_details
            self.add(
                input_tokens=usage.input_token_count or 0,
                output_tokens=usage.output_token_count or 0,
                total_tokens=usage.total_token_count or 0,
                label=label,
            )

    def add_from_openai_response(self, response: Any, label: str = "") -> None:
        """Add tokens from an OpenAI API response."""
        if hasattr(response, "usage") and response.usage:
            usage = response.usage
            self.add(
                input_tokens=getattr(usage, "prompt_tokens", 0),
                output_tokens=getattr(usage, "completion_tokens", 0),
                total_tokens=getattr(usage, "total_tokens", 0),
                label=label,
            )

    def summary(self) -> str:
        """Return a formatted summary of token usage."""
        lines = [
            "",
            "=" * 50,
            "TOKEN USAGE SUMMARY",
            "=" * 50,
            f"Total Calls: {self.call_count}",
            f"Input Tokens: {self.input_tokens:,}",
            f"Output Tokens: {self.output_tokens:,}",
            f"Total Tokens: {self.total_tokens:,}",
        ]
        if self.calls:
            lines.append("-" * 50)
            lines.append("Breakdown by call:")
            for i, call in enumerate(self.calls, 1):
                label = f" ({call['label']})" if call["label"] else ""
                lines.append(
                    f"  {i}{label}: in={call['input_tokens']:,}, "
                    f"out={call['output_tokens']:,}, total={call['total_tokens']:,}"
                )
        lines.append("=" * 50)
        return "\n".join(lines)

    def print_summary(self) -> None:
        """Print the token usage summary."""
        print(self.summary())


# Global tracker instance for convenience
_global_tracker: TokenUsage | None = None


def get_tracker() -> TokenUsage:
    """Get or create the global token tracker."""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = TokenUsage()
    return _global_tracker


def reset_tracker() -> TokenUsage:
    """Reset and return a fresh global tracker."""
    global _global_tracker
    _global_tracker = TokenUsage()
    return _global_tracker


class TrackedLLM(OpenAILLM):
    """
    Wrapper around OpenAILLM that tracks token usage.

    Use this instead of OpenAILLM when you want to track tokens
    in neo4j-graphrag pipelines (GraphRAG, retrievers, etc.).
    """

    def __init__(
        self,
        tracker: TokenUsage,
        model_name: str,
        model_params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        super().__init__(model_name, model_params, **kwargs)
        self.tracker = tracker

    def invoke(
        self,
        input: str,
        message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        """Invoke the LLM and track token usage."""
        try:
            if isinstance(message_history, MessageHistory):
                message_history = message_history.messages
            response = self.client.chat.completions.create(
                messages=self.get_messages(input, message_history, system_instruction),
                model=self.model_name,
                **self.model_params,
            )

            # Track token usage
            if response.usage:
                self.tracker.add(
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    label=input[:30] if input else "",
                )

            content = response.choices[0].message.content or ""
            return LLMResponse(content=content)
        except self.openai.OpenAIError as e:
            from neo4j_graphrag.exceptions import LLMGenerationError
            raise LLMGenerationError(e)
