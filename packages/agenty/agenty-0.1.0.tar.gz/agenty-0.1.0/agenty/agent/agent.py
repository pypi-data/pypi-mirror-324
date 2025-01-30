from typing import Optional, Type, Any, Dict, Union, cast
from typing_extensions import Generic

import instructor
import instructor.templating
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from agenty.components import AgentMemory, AgentUsage, ModelUsage
from agenty.io import AgentInput, AgentOutput
from .config import AgentConfig
from .types import AgentInputT, AgentOutputT, AgentOutputOverrideT


class Agent(Generic[AgentInputT, AgentOutputT]):
    """A base class for implementing AI agents with type-safe input and output handling.

    Provides core functionality for creating AI agents that can process structured inputs,
    maintain conversation history, and generate typed responses using language models.
    Supports template-based prompting and configurable response schemas.

    Type Parameters:
        AgentInputT: The type of input the agent accepts
        AgentOutputT: The type of output the agent produces

    Attributes:
        raw_client: The underlying OpenAI client instance
        client: The instructor-wrapped OpenAI client for structured outputs
        model: The name/identifier of the language model to use
        memory: The conversation history manager
        max_tokens: Maximum number of tokens in model responses
        temperature: Sampling temperature for response generation (0.0-2.0)
        input_schema: The expected schema for agent inputs
        output_schema: The schema for parsing model responses
        usage: Tracks token usage across model calls
        system_prompt: The system-level instruction prompt
        _context: Internal context dictionary for templating
    """

    def __init__(self, config: AgentConfig) -> None:
        """Initialize an agent with the specified configuration.

        Args:
            config: Configuration object containing all agent parameters including
                   model settings, memory management, and response schemas.
        """
        self.raw_client = config.client
        self.client = instructor.from_openai(self.raw_client)

        self.model = config.model
        self.memory = config.memory or AgentMemory()
        self.max_tokens = config.max_tokens
        self.temperature = config.temperature
        self.input_schema = (
            config.input_schema if config.input_schema is not None else AgentInput
        )
        self.output_schema = (
            config.output_schema if config.output_schema is not None else AgentOutput
        )
        self.usage = config.usage if config.usage is not None else AgentUsage()
        self.system_prompt = config.system_prompt if config.system_prompt else ""
        self._context: Dict[str, Any] = {}

    async def get_response(
        self,
        input: Optional[AgentInputT] = None,
        *,
        output_schema: Optional[
            Union[AgentOutputT, Type[AgentOutputOverrideT], str]
        ] = None,
        max_retries: int = 2,
        context: Optional[Dict[str, Any]] = None,
    ) -> Union[AgentOutputT, AgentOutputOverrideT]:
        """Generate a structured response using the language model.

        Processes the input (if provided) and conversation history to generate
        a response according to the specified output schema. Supports both
        free-form text and structured outputs.

        Args:
            input: Optional input to process and add to conversation history
            output_schema: Optional schema to override the default output type
            max_retries: Number of retry attempts for failed API calls
            context: Additional context variables for template rendering

        Returns:
            A response matching either the default output type or the override schema.
            For string schemas, returns the raw model completion.

        Note:
            When using string output_schema, the response bypasses instructor's
            structured parsing and returns the raw completion text.
        """
        if context is None:
            context = {}

        if input is not None:
            self.memory.add("user", input)

        messages = self.memory.history
        if self.system_prompt:
            system_msg: ChatCompletionMessageParam = {
                "role": "system",
                "content": self.system_prompt,
            }
            messages = [system_msg] + self.memory.history

        ctx = self._context.copy()
        ctx.update(context)

        if output_schema is None:
            output_schema = cast(AgentOutputT, self.output_schema)

        if output_schema is str:
            template_output = instructor.templating.handle_templating(
                {"messages": messages},
                ctx,
            )
            handled_messages: list[ChatCompletionMessageParam] = template_output[
                "messages"
            ]
            raw: ChatCompletion = await self.raw_client.chat.completions.create(
                messages=handled_messages,
                model=self.model,
                temperature=self.temperature,
                stream=False,
            )
            self.usage[self.model] += ModelUsage.from_openai(raw.usage)
            content = raw.choices[0].message.content or ""
            if content:
                self.memory.add("assistant", content)
            return cast(AgentOutputT, content)
        else:
            resp, raw = await self.client.chat.completions.create_with_completion(  # type: ignore
                response_model=output_schema,  # type: ignore
                model=self.model,
                messages=messages,
                max_retries=max_retries,
                temperature=self.temperature,
                context=ctx,
            )
            self.usage[self.model] += ModelUsage.from_openai(raw.usage)
            resp: AgentOutputT = cast(AgentOutputT, resp)  # type: ignore
            self.memory.add("assistant", resp)
            return resp

    def end_turn(self) -> None:
        """Mark the end of the current conversation turn.

        Updates the internal memory state to indicate a completed
        interaction cycle.
        """
        self.memory.end_turn()


__all__ = [
    "AgentInputT",
    "AgentOutputT",
    "AgentOutputOverrideT",
]
