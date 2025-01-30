# -------------------------------------------------------------------------------- #
# LLM Module
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Python imports
import time
from typing import Tuple, Union, Optional
# OpenAI imports
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ParsedChatCompletion, ChatCompletion

# Pydantic imports
from pydantic import BaseModel, Field

# AI imports
from astral_ai.typing.models import ModelName, ReasoningEffort
from astral_ai.typing.usage import AIUsage, AICost
from astral_ai.typing.messages import MessageList
from astral_ai.typing.response import StructuredOutputResponse, ChatResponse
from astral_ai.constants.usage import REASONING_EFFORT_SUPPORTED_MODELS
from astral_ai.exceptions import LLMResponseError, AsyncClientError, SyncClientError, ReasoningEffortNotSupportedError
from astral_ai.utils.usage_utils import compute_usage_and_cost


# -----------------------------
# 1. LLMClient: handles client setup/validation & raw calls
# -----------------------------
class LLMClient:
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
        Initialize the LLMClient.
        """
        self.model_name = model_name
        self.reasoning_effort = reasoning_effort
        self.user_email = user_email
        self.is_async = use_async

        # Validate reasoning effort
        self._validate_reasoning_effort(reasoning_effort)

        # Initialize the client
        self.client = self._init_client(use_async)

    def _init_client(self, use_async: bool) -> Union[OpenAI, AsyncOpenAI]:
        """
        Initialize the client (sync or async).
        """
        if use_async:
            return AsyncOpenAI()
        else:
            return OpenAI()

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

    def call(self, messages: MessageList, user_email: str = None) -> ChatCompletion:
        """
        Synchronously call the LLM (base).
        """
        self._validate_client(use_async=False)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            reasoning_effort=self.reasoning_effort or None,
            store=True,
            user=user_email if user_email else self.user_email
        )

        if not response.choices:
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.content:
            raise LLMResponseError("No content in the LLM response.")

        return response

    def call_structured(self,
                        messages: MessageList,
                        structured_model: StructuredOutputResponse,
                        user_email: str = None) -> ParsedChatCompletion:
        """
        Synchronously call the LLM (structured).
        """
        self._validate_client(use_async=False)

        response = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=messages,
            response_format=structured_model,
            reasoning_effort=self.reasoning_effort or None,
            store=True,
            user=user_email if user_email else self.user_email
        )

        if not response.choices:
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.parsed:
            raise LLMResponseError("No parsed object in the LLM response.")

        return response

    async def call_async(self, messages: MessageList, user_email: str = None) -> ChatCompletion:
        """
        Asynchronously call the LLM (base).
        """
        self._validate_client(use_async=True)

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            reasoning_effort=self.reasoning_effort or None,
            store=True,
            user=user_email if user_email else self.user_email
        )

        if not response.choices:
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.content:
            raise LLMResponseError("No content in the LLM response.")

        return response

    async def call_structured_async(self,
                                    messages: MessageList,
                                    structured_model: StructuredOutputResponse,
                                    user_email: str = None) -> ParsedChatCompletion:
        """
        Asynchronously call the LLM (structured).
        """
        self._validate_client(use_async=True)

        response = await self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=messages,
            response_format=structured_model,
            reasoning_effort=self.reasoning_effort or None,
            store=True,
            user=user_email if user_email else self.user_email
        )

        if not response.choices:
            raise LLMResponseError("No response from the LLM.")
        if not response.choices[0].message.parsed:
            raise LLMResponseError("No parsed object in the LLM response.")

        return response





class LLM:
    """
    Public interface for calling the language model (both sync and async).
    It delegates the actual low-level calls to LLMClient and
    delegates cost/usage calculation to compute_usage_and_cost.
    """

    def __init__(self,
                 model_name: ModelName,
                 reasoning_effort: ReasoningEffort,
                 user_email: str,
                 use_async: bool = False):
        """
        Initialize the LLM class.

        Args:
            model_name (ModelName): The model to use.
            reasoning_effort (ReasoningEffort): The reasoning effort to use.
            user_email (str): The user email to use.
            use_async (bool): Whether to use the async client.
        """
        self.api_client = LLMClient(
            model_name=model_name,
            reasoning_effort=reasoning_effort,
            user_email=user_email,
            use_async=use_async
        )

    def call(self, messages: MessageList) -> Tuple[str, AICost, AIUsage]:
        """
        Synchronously call the LLM. Returns the response, cost, and usage.

        Args:
            messages (MessageList): The messages to send to the LLM.
        """
        # Start timer
        start_time = time.monotonic()

        # Call the model
        response = self.api_client.call(messages)

        # Compute usage and cost
        usage, cost = compute_usage_and_cost(
            response, self.api_client.model_name, start_time
        )

        # Get the chat response
        chat_response: ChatResponse = response.choices[0].message.content

        return chat_response, cost, usage

    async def call_async(self, messages: MessageList) -> Tuple[ChatResponse, AICost, AIUsage]:
        """
        Asynchronously call the LLM. Returns the response, cost, and usage.

        Args:
            messages (MessageList): The messages to send to the LLM.
        """
        # Start timer
        start_time = time.monotonic()

        # Call the model
        response = await self.api_client.call_async(messages)

        # Compute usage and cost
        usage, cost = compute_usage_and_cost(
            response, self.api_client.model_name, start_time
        )

        # Get the chat response
        chat_response: ChatResponse = response.choices[0].message.content

        # Return the response, cost, and usage
        return chat_response, cost, usage

    def call_structured(self,
                        messages: MessageList,
                        structured_model: StructuredOutputResponse
                        ) -> Tuple[BaseModel, AICost, AIUsage]:
        """
        Synchronously call the LLM with structured output. Returns the response, cost, and usage.

        Args:
            messages (MessageList): The messages to send to the LLM.
            structured_model (BaseModel): The structured output object to use.
        """
        # Start timer
        start_time = time.monotonic()

        # Call the model
        response = self.api_client.call_structured(messages, structured_model)

        # Compute usage and cost
        usage, cost = compute_usage_and_cost(
            response, self.api_client.model_name, start_time
        )

        # Dynamically parse the structured output
        parsed_output = structured_model.model_validate(response.choices[0].message.parsed)

        # Return the response, cost, and usage
        return parsed_output, cost, usage

    async def call_structured_async(
            self,
            messages: MessageList,
            structured_model: StructuredOutputResponse
    ) -> Tuple[StructuredOutputResponse, AICost, AIUsage]:
        """
        Asynchronously call the LLM with structured output. Returns the response, cost, and usage.

        Args:
            messages (MessageList): The messages to send to the LLM.
            structured_model (BaseModel): The structured output object to use.
        """

        # Start timer
        start_time = time.monotonic()

        # Call the model
        response = await self.api_client.call_structured_async(messages, structured_model)

        # Compute usage and cost
        usage, cost = compute_usage_and_cost(
            response, self.api_client.model_name, start_time
        )

        # Dynamically parse the structured output
        parsed_output = structured_model.model_validate(response.choices[0].message.parsed)

        # Return the response, cost, and usage
        return parsed_output, cost, usage
