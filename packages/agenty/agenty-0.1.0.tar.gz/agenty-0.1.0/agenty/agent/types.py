from typing import Union
from typing_extensions import TypeVar

from agenty.io import AgentIO

AgentInputT = TypeVar(
    "AgentInputT",
    bound=Union[str, AgentIO],
    default=str,
)

AgentOutputT = TypeVar(
    "AgentOutputT",
    bound=Union[str, AgentIO],
    default=str,
)

AgentOutputOverrideT = TypeVar("AgentOutputOverrideT", bound=AgentIO)
