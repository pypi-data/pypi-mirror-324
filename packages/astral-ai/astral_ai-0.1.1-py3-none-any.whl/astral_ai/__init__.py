# -------------------------------------------------------------------------------- #
# Astral AI Package Initialization
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Version Information
# -------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------- #
# Package Exports
# -------------------------------------------------------------------------------- #

# Agents
from .agents import OpenAIAgent

# Messages
from .typing import ChatResponse, StructuredOutputResponse, AIUsage, AICost

# Re-export messages module
from .typing import messages

# Exceptions
from .exceptions import (AsyncClientError, SyncClientError, ResponseModelNotSupportedError,
                         ReasoningEffortNotSupportedError, DeveloperMessageOrTemplateNotSupportedError,
                         SystemMessageOrTemplateNotSupportedError, ImageIngestionNotSupportedError,
                         LLMResponseError, Jinja2EnvironmentError, StringTemplateError,
                         MissingTemplateVariablesError)

# Define what should be available when using `from astral_ai import *`
__all__ = [

    # Agents
    "OpenAIAgent",

    # Typing
    "ChatResponse",
    "StructuredOutputResponse",
    "AIUsage",
    "AICost",

    # Messages
    "messages",

    # Exceptions
    "AsyncClientError",
    "SyncClientError",
    "ResponseModelNotSupportedError",
    "ReasoningEffortNotSupportedError",
    "DeveloperMessageOrTemplateNotSupportedError",
    "SystemMessageOrTemplateNotSupportedError",
    "ImageIngestionNotSupportedError",
    "LLMResponseError",
    "Jinja2EnvironmentError",
    "StringTemplateError",
    "MissingTemplateVariablesError",
]
