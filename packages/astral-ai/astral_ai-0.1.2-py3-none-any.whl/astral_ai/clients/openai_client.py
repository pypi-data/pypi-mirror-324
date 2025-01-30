# -------------------------------------------------------------------------------- #
# LLM Module
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Python imports
from typing import Tuple, Union, Optional, List
# OpenAI imports
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ParsedChatCompletion, ChatCompletion


# AI imports
from src.astral_ai.typing.models import ModelName, ReasoningEffort
from src.astral_ai.typing.messages import MessageList, Message
from src.astral_ai.typing.response import StructuredOutputResponse, ChatResponse
from src.astral_ai.constants.usage import REASONING_EFFORT_SUPPORTED_MODELS, REASONING_EFFORT_DEFAULT
from src.astral_ai.exceptions import LLMResponseError, AsyncClientError, SyncClientError, ReasoningEffortNotSupportedError
from src.astral_ai.logger import AIModuleLogger

# -------------------------------------------------------------------------------- #
# BaseLLMClient Class
# -------------------------------------------------------------------------------- #

ai_logger = AIModuleLogger()


class OpenAILLMClient:
    """
    Responsible for initializing and validating the OpenAI client (sync or async)
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
        ai_logger.debug(
            f"Initializing OpenAILLMClient with model={model_name}, user={user_email}, reasoning_effort={reasoning_effort}, async={use_async}"
        )

        self.model_name = model_name
        self.reasoning_effort = reasoning_effort
        self.user_email = user_email
        self.is_async = use_async

        # Validate reasoning effort
        self._validate_reasoning_effort(reasoning_effort)

        # Initialize the client
        self.client = self._init_client(use_async)
        ai_logger.info(
            f"Successfully initialized {'async' if use_async else 'sync'} OpenAI client"
        )

    def _init_client(self, use_async: bool) -> Union[OpenAI, AsyncOpenAI]:
        """
        Initialize the client (sync or async).
        """
        ai_logger.debug(
            f"Initializing {'async' if use_async else 'sync'} OpenAI client")
        if use_async:
            return AsyncOpenAI()
        else:
            return OpenAI()

    def _validate_reasoning_effort(
            self, reasoning_effort: Union[ReasoningEffort, None]) -> None:
        """
        Validate that the model supports the requested reasoning effort.

        Args:
            reasoning_effort: The requested reasoning effort level

        Raises:
            ReasoningEffortNotSupportedError if the model doesn't support reasoning effort
            or if reasoning effort is provided for an unsupported model
        """
        ai_logger.debug(f"Validating reasoning effort: {reasoning_effort}")

        # Check if model supports reasoning effort
        model_supports_reasoning = self.model_name in REASONING_EFFORT_SUPPORTED_MODELS

        # If reasoning effort provided but model doesn't support it
        if reasoning_effort and not model_supports_reasoning:
            ai_logger.error(
                f"Model {self.model_name} does not support reasoning effort but {reasoning_effort} was provided"
            )
            raise ReasoningEffortNotSupportedError(self.model_name)

        # If model requires reasoning effort but none provided, use default
        if model_supports_reasoning and not reasoning_effort:
            self.reasoning_effort = REASONING_EFFORT_DEFAULT
            ai_logger.debug(
                f"Using default reasoning effort {REASONING_EFFORT_DEFAULT} for model {self.model_name}"
            )
        else:
            ai_logger.debug(
                f"Reasoning effort validation passed for model {self.model_name}"
            )

    def _validate_client(self, use_async: bool):
        """
        Validate that the call type (sync/async) matches the client.
        """
        ai_logger.debug(
            f"Validating client async={use_async} against instance async={self.is_async}"
        )
        if use_async and not self.is_async:
            ai_logger.error("Async call attempted on sync client")
            raise AsyncClientError("Async call made on sync client.")
        elif not use_async and self.is_async:
            ai_logger.error("Sync call attempted on async client")
            raise SyncClientError("Sync call made on async client.")
        

    def _format_messages(self, messages: Union[MessageList, List[Message]]) -> List[dict]:
        """
        Format the messages for the OpenAI API.
        """
        if isinstance(messages, MessageList):
            return messages.to_openai_format()
        elif isinstance(messages, List[Message]):
            return [message.to_openai_format() for message in messages]

    def call(self,
             messages: Union[MessageList, List[Message]],
             user_email: str = None) -> ChatCompletion:
        """
        Synchronously call the LLM (base).
        """
        ai_logger.debug(f"Making sync LLM call with {len(messages)} messages")
        self._validate_client(use_async=False)

        messages = self._format_messages(messages)

        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "store": True,
            "user": user_email if user_email else self.user_email
        }
        if self.reasoning_effort is not None:
            kwargs["reasoning_effort"] = self.reasoning_effort

        response = self.client.chat.completions.create(**kwargs)

        if not response.choices:
            ai_logger.error("LLM returned no choices in response")
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.content:
            ai_logger.error("LLM returned empty content in response")
            raise LLMResponseError("No content in the LLM response.")

        ai_logger.debug("Successfully completed sync LLM call")
        return response

    def call_structured(self,
                        messages: Union[MessageList, List[Message]],
                        structured_model: StructuredOutputResponse,
                        user_email: str = None) -> ParsedChatCompletion:
        """
        Synchronously call the LLM (structured).
        """
        ai_logger.debug(
            f"Making sync structured LLM call with {len(messages)} messages")
        self._validate_client(use_async=False)

        messages = self._format_messages(messages)


        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "response_format": structured_model,
            "store": True,
            "user": user_email if user_email else self.user_email
        }
        if self.reasoning_effort is not None:
            kwargs["reasoning_effort"] = self.reasoning_effort
        

        response = self.client.beta.chat.completions.parse(**kwargs)

        if not response.choices:
            ai_logger.error("LLM returned no choices in structured response")
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.parsed:
            ai_logger.error(
                "LLM returned no parsed object in structured response")
            raise LLMResponseError("No parsed object in the LLM response.")

        ai_logger.debug("Successfully completed sync structured LLM call")
        return response

    async def call_async(self,
                         messages: Union[MessageList, List[Message]],
                         user_email: str = None) -> ChatCompletion:
        """
        Asynchronously call the LLM (base).
        """
        ai_logger.debug(f"Making async LLM call with {len(messages)} messages")
        self._validate_client(use_async=True)

        messages = self._format_messages(messages)

        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "store": True,
            "user": user_email if user_email else self.user_email
        }
        if self.reasoning_effort is not None:
            kwargs["reasoning_effort"] = self.reasoning_effort

        response = await self.client.chat.completions.create(**kwargs)

        if not response.choices:
            ai_logger.error("LLM returned no choices in async response")
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.content:
            ai_logger.error("LLM returned empty content in async response")
            raise LLMResponseError("No content in the LLM response.")

        ai_logger.debug("Successfully completed async LLM call")
        return response

    async def call_structured_async(
            self,
            messages: Union[MessageList, List[Message]],
            structured_model: StructuredOutputResponse,
            user_email: str = None) -> ParsedChatCompletion:
        """
        Asynchronously call the LLM (structured).
        """
        ai_logger.debug(
            f"Making async structured LLM call with {len(messages)} messages")
        self._validate_client(use_async=True)

        messages = self._format_messages(messages)

        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "response_format": structured_model,
            "store": True,
            "user": user_email if user_email else self.user_email
        }
        if self.reasoning_effort is not None:
            kwargs["reasoning_effort"] = self.reasoning_effort

        response = await self.client.beta.chat.completions.parse(**kwargs)

        if not response.choices:
            ai_logger.error(
                "LLM returned no choices in async structured response")
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.parsed:
            ai_logger.error(
                "LLM returned no parsed object in async structured response")
            raise LLMResponseError("No parsed object in the LLM response.")

        ai_logger.debug("Successfully completed async structured LLM call")
        return response
