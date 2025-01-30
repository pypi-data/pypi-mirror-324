# -------------------------------------------------------------------------------- #
# LLM Module
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Python imports
from abc import ABC, abstractmethod
from typing import Union, Optional
# OpenAI imports
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ParsedChatCompletion, ChatCompletion


# AI imports
from src.ai.typing.models import ModelName, ReasoningEffort
from src.ai.typing.messages import MessageList
from src.ai.typing.response import StructuredOutputResponse
from src.ai.constants.usage import REASONING_EFFORT_SUPPORTED_MODELS
from src.ai.exceptions import AsyncClientError, SyncClientError, ReasoningEffortNotSupportedError


# -------------------------------------------------------------------------------- #
# BaseLLMClient Class
# -------------------------------------------------------------------------------- #


class BaseLLMClient(ABC):
    """
    Abstract base class responsible for initializing and validating the OpenAI client (sync or async)
    and for making the actual calls (base or structured).
    """

    def __init__(self,
                 model_name: ModelName,
                 user_email: str,
                 reasoning_effort: Optional[ReasoningEffort] = None,
                 use_async: bool = False):
        """
        Initialize the BaseLLMClient.
        """
        self.model_name = model_name
        self.reasoning_effort = reasoning_effort
        self.user_email = user_email
        self.is_async = use_async

        # Validate reasoning effort
        self._validate_reasoning_effort(reasoning_effort)

        # Initialize the client
        self.client = self._init_client(use_async)

    @abstractmethod
    def _init_client(self, use_async: bool) -> Union[OpenAI, AsyncOpenAI]:
        """
        Initialize the client (sync or async).
        """
        pass

    def _validate_reasoning_effort(self, reasoning_effort: Union[ReasoningEffort, None]) -> None:
        """
        Validate that the model supports the requested reasoning effort.

        Args:
            reasoning_effort: The requested reasoning effort level


        Raises:
            ReasoningEffortNotSupportedError if the model doesn't support reasoning effort
        """

        if reasoning_effort and reasoning_effort not in REASONING_EFFORT_SUPPORTED_MODELS:
            raise ReasoningEffortNotSupportedError(self.model_name)

    def _validate_client(self, use_async: bool):
        """
        Validate that the call type (sync/async) matches the client.
        """
        if use_async and not self.is_async:
            raise AsyncClientError("Async call made on sync client.")
        elif not use_async and self.is_async:
            raise SyncClientError("Sync call made on async client.")

    @abstractmethod
    def call(self, messages: MessageList, user_email: str = None) -> ChatCompletion:
        """
        Synchronously call the LLM (base).
        """
        pass

    @abstractmethod
    def call_structured(self,
                        messages: MessageList,
                        structured_output_object: StructuredOutputResponse,
                        user_email: str = None) -> ParsedChatCompletion:
        """
        Synchronously call the LLM (structured).
        """
        pass

    @abstractmethod
    async def call_async(self, messages: MessageList, user_email: str = None) -> ChatCompletion:
        """
        Asynchronously call the LLM (base).
        """
        pass

    @abstractmethod
    async def call_structured_async(self,
                                    messages: MessageList,
                                    structured_output_object: StructuredOutputResponse,
                                    user_email: str = None) -> ParsedChatCompletion:
        """
        Asynchronously call the LLM (structured).
        """
        pass
