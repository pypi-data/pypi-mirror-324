
# -------------------------------------------------------------------------------- #
# Exceptions
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in
from typing import List

# Project
from astral_ai.typing.models import ModelName
from astral_ai.constants.usage import DEVELOPER_MESSAGE_SUPPORTED_MODELS, SYSTEM_MESSAGE_SUPPORTED_MODELS, REASONING_EFFORT_SUPPORTED_MODELS, RESPONSE_MODEL_SUPPORTED_MODELS, IMAGE_INGESTION_SUPPORTED_MODELS

# -------------------------------------------------------------------------------- #
# Helper Functions
# -------------------------------------------------------------------------------- #


def get_model_message_not_supported_error(model_name: ModelName, supported_models: List[ModelName]) -> str:
    """
    Get's the message not supported for model error.
    """
    return f"Message not supported for model {model_name}. This is only supported for {', '.join([model_name for model_name in supported_models])}."


# -------------------------------------------------------------------------------- #
# Client Exceptions
# -------------------------------------------------------------------------------- #


class AsyncClientError(Exception):
    """
    Exception raised for errors in the async client.
    """

    def __init__(self, message: str = "Async method called on sync client."):
        self.message = message
        super().__init__(self.message)


class SyncClientError(Exception):
    """
    Exception raised for errors in the sync client.
    """

    def __init__(self, message: str = "Sync method called on async client."):
        self.message = message
        super().__init__(self.message)

# -------------------------------------------------------------------------------- #
# Model Message Not Supported Exceptions
# -------------------------------------------------------------------------------- #


class ResponseModelNotSupportedError(Exception):
    """Exception raised for errors in response model support."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, RESPONSE_MODEL_SUPPORTED_MODELS)
        super().__init__(self.message)


class ReasoningEffortNotSupportedError(Exception):
    """Exception raised for errors in reasoning effort support."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, REASONING_EFFORT_SUPPORTED_MODELS)
        super().__init__(self.message)


class DeveloperMessageOrTemplateNotSupportedError(Exception):
    """Exception raised for errors in developer message support."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, DEVELOPER_MESSAGE_SUPPORTED_MODELS)
        super().__init__(self.message)


class SystemMessageOrTemplateNotSupportedError(Exception):
    """Exception raised for errors in system message support."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, SYSTEM_MESSAGE_SUPPORTED_MODELS)
        super().__init__(self.message)


class ImageIngestionNotSupportedError(Exception):
    """Exception raised for errors in image ingestion support."""

    def __init__(self, model_name: ModelName):
        self.message = get_model_message_not_supported_error(model_name, IMAGE_INGESTION_SUPPORTED_MODELS)
        super().__init__(self.message)


# -------------------------------------------------------------------------------- #
# LLM Response Exceptions
# -------------------------------------------------------------------------------- #


class LLMResponseError(Exception):
    """
    Exception raised for errors in the LLM response.
    """

    def __init__(self, message: str = "An error occurred in the LLM response."):
        self.message = message
        super().__init__(self.message)


# -------------------------------------------------------------------------------- #
# Messages Exceptions
# -------------------------------------------------------------------------------- #

# Jinja2 Exceptions

class Jinja2EnvironmentError(Exception):
    """Exception raised for errors in the Jinja2 environment."""

    def __init__(self, message: str = "An error occurred in the Jinja2 environment."):
        self.message = message
        super().__init__(self.message)

# -------------------------------------------------------------------------------- #
# String Template Exceptions
# -------------------------------------------------------------------------------- #


class StringTemplateError(Exception):
    """Raised when there is an issue rendering a string with placeholders."""

    def __init__(self, message: str = "An error occurred when rendering a string with placeholders."):
        self.message = message
        super().__init__(self.message)


class MissingTemplateVariablesError(Exception):
    """
    Raised when required variables are not provided to a template or string formatter
    when strict validation is enabled.
    """

    def __init__(self, message: str = "Required variables are not provided to a template or string formatter when strict validation is enabled."):
        self.message = message
        super().__init__(self.message)
