import uuid
from typing import Optional, Literal, Union
from pydantic import BaseModel

from openai.types.chat import ChatCompletionMessageParam


from agenty.io import AgentIO

Role = Literal["user", "assistant", "tool", "system", "developer", "function"]


class AgentMessage(BaseModel):
    """A message in the chat history.

    This class represents a single message exchanged between the agent and other participants
    in the conversation. Each message has a role, content, and optional metadata.

    Attributes:
        role: The role of the message sender (user, assistant, etc.)
        content: The message content wrapped in an AgentIO object
        turn_id: Optional UUID identifying the conversation turn this message belongs to
        name: Optional name of the message sender
    """

    role: Role
    content: Union[AgentIO, str]
    turn_id: Optional[str] = None
    name: Optional[str] = None

    def to_openai(self) -> ChatCompletionMessageParam:
        """Convert the message to OpenAI API format.

        Returns:
            A dictionary containing the message data formatted for the OpenAI API.
        """
        content = self.content
        if not isinstance(content, str):
            content = content.model_dump_json()
        return {
            "role": self.role,  # type: ignore
            "content": content,
            "name": str(self.name),
        }


class AgentMemory:
    """Manages conversation history for an AI agent.

    This class handles storing, retrieving, and managing the chat history between
    an AI agent and other participants. It supports conversation turns and can
    limit the history length.

    Attributes:
        max_messages: Maximum number of messages to keep in history (-1 for unlimited)
        current_turn_id: UUID of the current conversation turn, if any
    """

    def __init__(self, max_messages: int = -1) -> None:
        """Initialize the agent memory.

        Args:
            max_messages: Maximum number of messages to keep in history.
                        Use -1 for unlimited history.
        """
        self._history: list[AgentMessage] = []
        self.max_messages = max_messages
        self.current_turn_id: Optional[str] = None

    def initialize_turn(self) -> None:
        """Start a new conversation turn.

        Generates a new UUID for the current turn, allowing messages to be
        grouped together.
        """
        self.current_turn_id = str(uuid.uuid4())

    def add(
        self,
        role: Role,
        content: Union[AgentIO, str],
        name: Optional[str] = None,
    ) -> None:
        """Add a message to the chat history.

        Creates a new message with the given parameters and adds it to the history.
        Initializes a new turn if none is active.

        Args:
            role: The role of the message sender
            content: The message content
            name: Optional name of the message sender
        """
        if self.current_turn_id is None:
            self.initialize_turn()

        message = AgentMessage(
            role=role,
            content=content,
            turn_id=self.current_turn_id,
            name=name,
        )
        self._history.append(message)
        self._cull_history()

    def _cull_history(self) -> None:
        """Remove oldest messages if history exceeds maximum length."""
        if self.max_messages >= 0:
            while len(self.history) > self.max_messages:
                self.history.pop(0)

    def end_turn(self) -> None:
        """End the current conversation turn."""
        self.current_turn_id = None

    @property
    def history(self) -> list[ChatCompletionMessageParam]:
        """Get the chat history in OpenAI format.

        Returns:
            List of messages formatted for the OpenAI API.
        """
        return [msg.to_openai() for msg in self._history]

    def __len__(self) -> int:
        """Get the number of messages in history.

        Returns:
            The count of messages in the history.
        """
        return len(self._history)
