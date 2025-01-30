# -------------------------------------------------------------------------------- #
# Message Types
# -------------------------------------------------------------------------------- #

"""
This module defines a simplified Message Pydantic model (with optional text/image)
and utility methods to create messages from Python-format strings or Jinja2 templates,
with optional strict placeholder validation.

It also provides methods to convert each Message (and a list of Messages)
into a format suitable for certain OpenAI endpoints.
"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
import os
import string
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    TypeAlias
)

# Pydantic imports
from pydantic import BaseModel, Field

# Jinja2 imports
from jinja2 import Environment, FileSystemLoader, meta

# Custom exceptions (adjust import paths to your app structure)
from astral_ai.exceptions import (
    Jinja2EnvironmentError,
    MissingTemplateVariablesError,
    StringTemplateError
)

# -------------------------------------------------------------------------------- #
# Base Types
# -------------------------------------------------------------------------------- #

# Image Detail
ImageDetail: TypeAlias = Literal["high", "low", "auto"]

# Message Role
MessageRole: TypeAlias = Literal["system", "user", "developer"]

# -------------------------------------------------------------------------------- #
# Helper Functions
# -------------------------------------------------------------------------------- #


def find_string_placeholders(text: str) -> Set[str]:
    """
    Given a Python-format-compatible string, return a set of placeholder field names.

    Example:
        text = "Hello, {name}! Today is {day}."
        placeholders = find_string_placeholders(text)
        # placeholders -> {"name", "day"}
    """
    formatter = string.Formatter()
    placeholders = set()
    for literal_text, field_name, format_spec, conversion in formatter.parse(text):
        if field_name is not None:
            placeholders.add(field_name)
    return placeholders


def partial_format(template: str, **kwargs: Any) -> str:
    """
    A 'partial' Python string formatter that:
    - Substitutes placeholders found in kwargs.
    - Leaves placeholders as-is if not in kwargs (avoids KeyError).

    Note: This handles only top-level placeholders like "{name}".
          Nested placeholders (e.g., "{user.name}") require custom logic.
    """
    formatter = string.Formatter()
    result = []

    for literal_text, field_name, format_spec, conversion in formatter.parse(template):
        # Always add the literal text portion
        result.append(literal_text or "")

        # If there's no placeholder, just continue
        if field_name is None:
            continue

        if field_name in kwargs:
            # Perform normal formatting
            value = kwargs[field_name]
            # Handle format spec
            if format_spec:
                value = formatter.format_field(value, format_spec)
            # Handle conversions (!r, !s, etc.)
            if conversion == 'r':
                value = repr(value)
            elif conversion == 's':
                value = str(value)
            result.append(str(value))
        else:
            # Missing placeholder in non-strict mode: keep it as {field_name}
            placeholder = f"{{{field_name}"
            if format_spec:
                placeholder += f":{format_spec}"
            if conversion:
                placeholder += f"!{conversion}"
            placeholder += "}"
            result.append(placeholder)

    return "".join(result)

# -------------------------------------------------------------------------------- #
# Message Model
# -------------------------------------------------------------------------------- #


class Message(BaseModel):
    """
    Represents a single message with optional text and image parameters.
    Includes class methods to generate instances from Python-format strings or Jinja2 templates.

    The to_openai_format() method outputs a dict like:
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://some-image-url.jpg",
                },
            },
        ],
    }
    """
    role: MessageRole = Field(
        default="user",
        description="The role of the message sender."
    )
    text: Optional[str] = Field(
        default=None,
        description="Plain text content for the message."
    )
    image_url: Optional[str] = Field(
        default=None,
        description="The URL of an image to display with the message."
    )
    image_detail: ImageDetail = Field(
        default="auto",
        description="The detail level of the image (high, low, or auto)."
    )

    @classmethod
    def from_string_with_optional_kwargs(
        cls,
        string_template: str,
        role: MessageRole = "user",
        strict: bool = False,
        template_args: Optional[Dict[str, Any]] = None,
        image_url: Optional[str] = None,
        image_detail: ImageDetail = "auto"
    ) -> "Message":
        """
        Create a Message by formatting a Python-format string with optional kwargs.

        :param string_template: The template string (e.g. "Hello, {name}!").
        :param role: The role of the message sender (defaults to "user").
        :param strict: If True, raises MissingTemplateVariablesError if placeholders are missing.
        :param template_args: Optional dict of key-value pairs for placeholders.
        :param image_url: Optional image URL for the message.
        :param image_detail: The image detail level (defaults to "auto").
        """
        template_args = template_args or {}
        placeholders = find_string_placeholders(string_template)
        missing_vars = placeholders - set(template_args.keys())

        if strict and missing_vars:
            raise MissingTemplateVariablesError(f"Missing required placeholder variables for string template: {missing_vars}")

        if strict:
            # Strict mode uses standard .format()
            try:
                rendered = string_template.format(**template_args)
            except KeyError as e:
                raise StringTemplateError(f"Missing placeholder in 'message': {str(e)}") from e
        else:
            # Non-strict: partial_format to preserve missing placeholders
            rendered = partial_format(string_template, **template_args)

        return cls(
            role=role,
            text=rendered,
            image_url=image_url,
            image_detail=image_detail
        )

    @classmethod
    def from_jinja2_template(
        cls,
        template_name: str,
        environment: Optional[Environment] = None,
        environment_path: str = "src/templates",
        role: MessageRole = "user",
        strict: bool = False,
        template_args: Optional[Dict[str, Any]] = None,
        image_url: Optional[str] = None,
        image_detail: ImageDetail = "auto"
    ) -> "Message":
        """
        Create a Message by rendering a Jinja2 template with optional kwargs.

        :param template_name: Jinja2 template file name (e.g. "example.jinja").
        :param environment: Optional Jinja2 Environment. If None, a new one is created.
        :param environment_path: Path where the template is located.
        :param role: The role of the message sender (defaults to "user").
        :param strict: If True, raises MissingTemplateVariablesError if placeholders are missing.
        :param template_args: Optional dict of key-value pairs for rendering the template.
        :param image_url: Optional image URL for the message.
        :param image_detail: The image detail level (defaults to "auto").
        """
        template_args = template_args or {}

        # Create or use existing environment
        if environment is None:
            if not os.path.isdir(environment_path):
                raise Jinja2EnvironmentError(
                    f"Provided environment path '{environment_path}' "
                    "does not exist or is not a directory."
                )
            environment = Environment(loader=FileSystemLoader(environment_path))

        # Load the template
        try:
            template = environment.get_template(template_name)
        except Exception as e:
            raise Jinja2EnvironmentError(
                f"Error retrieving Jinja2 template '{template_name}' "
                f"from '{environment_path}': {e}"
            ) from e

        # Determine which variables the template expects
        try:
            template_source = environment.loader.get_source(environment, template_name)[0]
            parsed_content = environment.parse(template_source)
            jinja_vars = meta.find_undeclared_variables(parsed_content)
        except Exception as e:
            raise Jinja2EnvironmentError(f"Error parsing template '{template_name}': {e}") from e

        # Check for missing template variables
        missing_vars = jinja_vars - set(template_args.keys())
        if strict and missing_vars:
            raise MissingTemplateVariablesError(
                f"Missing required variables for Jinja2 template '{template_name}': {missing_vars}"
            )

        # Render the template
        try:
            rendered_message = template.render(**template_args)
        except Exception as e:
            raise Jinja2EnvironmentError(
                f"Error rendering template '{template_name}': {e}"
            ) from e

        return cls(
            role=role,
            text=rendered_message,
            image_url=image_url,
            image_detail=image_detail
        )

    def to_openai_format(self) -> Dict[str, Any]:
        """
        Return the message in a structure like:
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "..."},
                {"type": "image_url", "image_url": {"url": "..."}},
            ]
        }
        Only includes text block if self.text is provided.
        Only includes image block if self.image_url is provided.
        """
        content_blocks = []

        if self.text:
            content_blocks.append({"type": "text", "text": self.text})

        if self.image_url:
            content_blocks.append({
                "type": "image_url",
                "image_url": {"url": self.image_url, "detail": self.image_detail}
            })

        return {
            "role": self.role,
            "content": content_blocks,
        }

# -------------------------------------------------------------------------------- #
# Message List
# -------------------------------------------------------------------------------- #


class MessageList(BaseModel):
    """
    Represents a collection of Message objects.
    """

    messages: List[Message] = Field(
        default_factory=list,
        description="A list of Message objects."
    )

    def to_openai_format(self) -> List[Dict[str, Any]]:
        """
        Return all messages in the OpenAI-friendly format.
        """
        return [msg.to_openai_format() for msg in self.messages]

    def __len__(self) -> int:
        """
        Return the number of messages in the list.
        """
        return len(self.messages)
