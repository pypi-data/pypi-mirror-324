from typing import Optional, Type, Union

from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from agenty.components import AgentMemory, AgentUsage
from agenty.io import AgentIO


class AgentConfig(BaseModel):
    """Configuration class for Agent initialization.

    This class uses Pydantic for validation and holds all necessary parameters
    to initialize an Agent instance.
    """

    model_config = {"arbitrary_types_allowed": True}

    client: AsyncOpenAI = Field(
        ..., description="Client for interacting with the language model."
    )
    model: str = Field(..., description="The model to use for generating responses.")
    memory: Optional[AgentMemory] = Field(
        default=None, description="Memory component for storing chat history."
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="Maximum number of token allowed in the response generation.",
    )
    temperature: Optional[float] = Field(
        default=0.0,
        description="Temperature for response generation, typically ranging from 0 to 1.",
    )
    input_schema: Optional[Union[Type[str], Type[AgentIO]]] = Field(
        default=str,
        description="The input schema that this agent accepts.",
    )
    output_schema: Optional[Union[Type[str], Type[AgentIO]]] = Field(
        default=str,
        description="The output schema to use for generating responses.",
    )
    system_prompt: Optional[str] = Field(
        default="", description="The system prompt for this agent. Supports templating."
    )
    usage: Optional[AgentUsage] = Field(
        default=None, description="Usage component for tracking agent statistics."
    )
