# -------------------------------------------------------------------------------- #
# LLM Module
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Python imports
import time
from typing import Tuple, Union, Optional, List, Type
# OpenAI imports
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ParsedChatCompletion, ChatCompletion

# Pydantic imports
from pydantic import BaseModel, Field

# AI imports
from src.astral_ai.typing.models import ModelName, ReasoningEffort
from src.astral_ai.typing.usage import AIUsage, AICost
from src.astral_ai.typing.messages import MessageList, Message
from src.astral_ai.typing.response import StructuredOutputResponse, ChatResponse
from src.astral_ai.constants.usage import REASONING_EFFORT_SUPPORTED_MODELS
from src.astral_ai.exceptions import LLMResponseError, AsyncClientError, SyncClientError, ReasoningEffortNotSupportedError
from src.astral_ai.utils.usage_utils import compute_usage_and_cost

# OpenAI imports
from src.astral_ai.clients.openai_client import OpenAILLMClient

# Logger
from src.astral_ai.logger import AIModuleLogger

ai_logger = AIModuleLogger()


class OpenAIAgent:
    """
    Public interface for calling the language model (both sync and async).
    It delegates the actual low-level calls to OpenAILLMClient and
    delegates cost/usage calculation to compute_usage_and_cost.
    """

    def __init__(self,
                 model_name: ModelName,
                 user_email: Optional[str] = None,
                 reasoning_effort: Optional[ReasoningEffort] = None,
                 use_async: bool = False):
        """
        Initialize the LLM class.

        Args:
            model_name (ModelName): The model to use.
            reasoning_effort (ReasoningEffort): The reasoning effort to use.
            user_email (str): The user email to use.
            use_async (bool): Whether to use the async client.
        """
        ai_logger.info(f"Initializing OpenAIAgent with model={model_name}, reasoning_effort={reasoning_effort}, user={user_email}, async={use_async}")
        self.api_client = OpenAILLMClient(
            model_name=model_name,
            reasoning_effort=reasoning_effort,
            user_email=user_email,
            use_async=use_async
        )

    def call(self, messages: Union[MessageList, List[Message]]) -> Tuple[str, AICost, AIUsage]:
        """
        Synchronously call the LLM. Returns the response, cost, and usage.

        Args:
            messages (Union[MessageList, List[Message]]): The messages to send to the LLM.
        """
        ai_logger.debug(f"Making synchronous LLM call with {len(messages)} messages")
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

        # Log the completion of the LLM call
        ai_logger.info(f"Completed LLM call - Tokens used: {usage.total_tokens}, Cost: ${cost.total_cost:.4f}. Took {usage.latency:.2f} seconds.")
        ai_logger.debug(f"Response details - Input tokens: {usage.prompt_tokens}, Output tokens: {usage.completion_tokens}")

        return chat_response, cost, usage

    async def call_async(self, messages: MessageList) -> Tuple[ChatResponse, AICost, AIUsage]:
        """
        Asynchronously call the LLM. Returns the response, cost, and usage.

        Args:
            messages (MessageList): The messages to send to the LLM.
        """
        ai_logger.debug(f"Making async LLM call with {len(messages)} messages")
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

        # Log the completion of the async LLM call
        ai_logger.info(f"Completed async LLM call - Tokens used: {usage.total_tokens}, Cost: ${cost.total_cost:.4f}. Took {usage.latency:.2f} seconds.")
        ai_logger.debug(f"Async response details - Input tokens: {usage.prompt_tokens}, Output tokens: {usage.completion_tokens}")

        # Return the response, cost, and usage
        return chat_response, cost, usage

    def call_structured(self,
                        messages: Union[MessageList, List[Message]],
                        structured_model: Type[StructuredOutputResponse]
                        ) -> Tuple[StructuredOutputResponse, AICost, AIUsage]:
        """
        Synchronously call the LLM with structured output. Returns the response, cost, and usage.

        Args:
            messages (MessageList): The messages to send to the LLM.
            structured_model (BaseModel): The structured output object to use.
        """
        ai_logger.debug(f"Making structured LLM call with {len(messages)} messages")
        # Start timer
        start_time = time.monotonic()

        # Call the model
        response = self.api_client.call_structured(messages, structured_model)

        # Compute usage and cost
        usage, cost = compute_usage_and_cost(
            response, self.api_client.model_name, start_time
        )

        try:
            # Dynamically parse the structured output
            parsed_output = structured_model.model_validate(response.choices[0].message.parsed)
        except Exception as e:
            ai_logger.error(f"Failed to parse structured output: {str(e)}")
            raise

        # Log the completion of the structured LLM call
        ai_logger.info(f"Completed structured LLM call - Tokens used: {usage.total_tokens}, Cost: ${cost.total_cost:.4f}. Took {usage.latency:.2f} seconds.")
        ai_logger.debug(f"Structured response details - Input tokens: {usage.prompt_tokens}, Output tokens: {usage.completion_tokens}")

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
        ai_logger.debug(f"Making async structured LLM call with {len(messages)} messages")
        # Start timer
        start_time = time.monotonic()

        # Call the model
        response = await self.api_client.call_structured_async(messages, structured_model)

        # Compute usage and cost
        usage, cost = compute_usage_and_cost(
            response, self.api_client.model_name, start_time
        )

        try:
            # Dynamically parse the structured output
            parsed_output = structured_model.model_validate(response.choices[0].message.parsed)
        except Exception as e:
            ai_logger.error(f"Failed to parse async structured output: {str(e)}")
            raise

        # Log the completion of the async structured LLM call
        ai_logger.info(f"Completed async structured LLM call - Tokens used: {usage.total_tokens}, Cost: ${cost.total_cost:.4f}. Took {usage.latency:.2f} seconds.")
        ai_logger.debug(f"Async structured response details - Input tokens: {usage.prompt_tokens}, Output tokens: {usage.completion_tokens}")

        # Return the response, cost, and usage
        return parsed_output, cost, usage
