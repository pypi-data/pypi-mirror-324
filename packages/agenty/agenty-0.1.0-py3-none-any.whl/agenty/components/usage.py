from collections.abc import MutableMapping
from copy import copy
from dataclasses import dataclass
from typing import Optional

from openai.types import CompletionUsage

__all__ = "ModelUsage", "AgentUsage"


@dataclass
class ModelUsage:
    """Usage information for LLM."""

    requests: int = 0
    request_tokens: Optional[int] = None
    response_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    def __add__(self, other: "ModelUsage") -> "ModelUsage":
        """Add two Usages together."""
        self_copy = copy(self)

        for attr in "requests", "request_tokens", "response_tokens", "total_tokens":
            self_val = getattr(self_copy, attr)
            other_val = getattr(other, attr)
            if self_val is not None or other_val is not None:
                setattr(self_copy, attr, (self_val or 0) + (other_val or 0))
        return self_copy

    @staticmethod
    def from_openai(usage: Optional[CompletionUsage]) -> "ModelUsage":
        """Create a Usage object from OpenAI API response."""
        if usage is None:
            return ModelUsage()
        return ModelUsage(
            requests=1,
            request_tokens=usage.prompt_tokens,
            response_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )


class AgentUsage(MutableMapping[str, ModelUsage]):
    def __init__(self):
        self._usage: dict[str, ModelUsage] = {}

    def __getitem__(self, key: str) -> ModelUsage:
        try:
            return self._usage[key]
        except KeyError:
            self._usage[key] = ModelUsage()
            return self._usage[key]

    def __setitem__(self, key: str, value: ModelUsage) -> None:
        self._usage[key] = value

    def __delitem__(self, key: str) -> None:
        del self._usage[key]

    def __iter__(self):
        return iter(self._usage)

    def __len__(self) -> int:
        return len(self._usage)

    @property
    def requests(self) -> int:
        """Get the total number of requests."""
        return sum(usage.requests for usage in self._usage.values())

    @property
    def request_tokens(self) -> int:
        """Get the total number of request tokens."""
        return sum(usage.request_tokens or 0 for usage in self._usage.values())

    @property
    def response_tokens(self) -> int:
        """Get the total number of response tokens."""
        return sum(usage.response_tokens or 0 for usage in self._usage.values())

    @property
    def total_tokens(self) -> int:
        """Get the total number of response tokens."""
        return sum(usage.total_tokens or 0 for usage in self._usage.values())
