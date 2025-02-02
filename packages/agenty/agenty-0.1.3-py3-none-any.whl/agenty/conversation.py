from typing import (
    cast,
    Any,
    Dict,
    List,
    Callable,
    Union,
    Optional,
    Generic,
    Type,
    AsyncIterator,
)
import logging

import pydantic_ai as pai
from pydantic_ai.agent import EndStrategy
from pydantic_ai.models import KnownModelName, Model, ModelSettings

from agenty.agent import Agent
from agenty.components.memory import AgentMemory, ChatMessage
from agenty.components.usage import AgentUsage, AgentUsageLimits
from agenty.template import apply_template
from agenty.types import AgentInputT, AgentOutputT, AgentIO


class AgentTeam(Generic[AgentInputT, AgentOutputT]):
    def __init__(
        self,
        agents: List[Agent],
    ) -> None:
        pass

    async def run(
        self,
        input_data: AgentInputT,
    ) -> AgentOutputT:
        pass
