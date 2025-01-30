from typing import Any, Dict, Optional, Type, overload, Generic

from .config import AgentConfig
from .types import AgentInputT, AgentOutputT, AgentOutputOverrideT

class Agent(Generic[AgentInputT, AgentOutputT]):
    def __init__(self, config: AgentConfig) -> None: ...
    @overload
    async def get_response(
        self,
        input: Optional[AgentInputT],
        *,
        output_schema: None = None,
        max_retries: int = 2,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentOutputT: ...
    @overload
    async def get_response(
        self,
        input: Optional[AgentInputT],
        *,
        output_schema: AgentOutputT,
        max_retries: int = 2,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentOutputT: ...
    @overload
    async def get_response(
        self,
        input: Optional[AgentInputT],
        *,
        output_schema: Type[AgentOutputOverrideT],
        max_retries: int = 2,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentOutputOverrideT: ...
