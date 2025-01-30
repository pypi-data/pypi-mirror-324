# -------------------------------------------------------------------------------- #
# OpenAI Framework Examples
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
# Built-in imports
from typing import Dict, Any

# OpenAI imports
from astral_ai.typing.messages import Message, MessageList
from astral_ai.typing.models import ModelName
from astral_ai.agents.openai import OpenAIAgent
from astral_ai.logger import AIModuleLogger

# -------------------------------------------------------------------------------- #
# Logger Configuration
# -------------------------------------------------------------------------------- #
ai_logger = AIModuleLogger()

# -------------------------------------------------------------------------------- #
# Example Message Creation and GPT-4 Usage
# -------------------------------------------------------------------------------- #

def run_examples():
    ai_logger.info("Starting OpenAI Framework demo...")

    # Initialize system context
    ai_logger.debug("Creating system message with Louvre expertise context")
    system_message = Message(
        role="system",
        text="You are an expert on the history of the Paris and the Louvre Museum."
    )

    # Basic message example
    ai_logger.debug("Creating basic user message")
    basic_user_message = Message(
        role="user",
        text="What is the capital of France?"
    )

    # Template message example
    ai_logger.debug("Creating message from string template")
    template_vars = {"city": "Paris"}
    template_message = Message.from_string_with_optional_kwargs(
        string_template="Tell me about {{ city }} and its history.",
        role="user",
        template_args=template_vars
    )

    # Image message example
    ai_logger.debug("Creating message with image content")
    image_message = Message(
        role="user",
        text="What's in this image?",
        image_url="https://cdn.mos.cms.futurecdn.net/z3rNHS9Y6PV6vbhH8w83Yn-1000-80.jpg",
        image_detail="high"  # Can be 'low' or 'high' or 'auto'
    )

    # Jinja template example with strict validation
    ai_logger.debug("Creating message from Jinja template with strict validation")
    strict_template_vars: Dict[str, Any] = {
        "location": "Louvre Museum",
        "time_period": "18th century"
    }
    strict_message = Message.from_jinja2_template(
        template_name="demo.jinja",
        role="user",
        template_args=strict_template_vars,
        strict=True
    )

    # Initialize OpenAI agent
    ai_logger.info("Initializing GPT-4o agent")
    agent = OpenAIAgent(
        model_name="gpt-4o",  # Using Vision model to handle image
        user_email="example@domain.com"
    )

    # Create message lists for different scenarios
    ai_logger.debug("Preparing message lists for API calls")
    basic_message_list = MessageList(messages=[system_message, basic_user_message])
    template_message_list = MessageList(messages=[system_message, template_message])
    image_message_list = MessageList(messages=[system_message, image_message])
    strict_message_list = MessageList(messages=[system_message, strict_message])

    # Execute API calls and log results
    ai_logger.info("Making API calls for each message type...")

    # Basic message call
    ai_logger.debug("Processing basic message query")
    response, cost, usage = agent.call(basic_message_list)
    ai_logger.info(f"Basic query completed - Cost: ${cost.total_cost:.4f}, Tokens: {usage.total_tokens}")

    # Template message call
    ai_logger.debug("Processing template message query")
    response, cost, usage = agent.call(template_message_list)
    ai_logger.info(f"Template query completed - Cost: ${cost.total_cost:.4f}, Tokens: {usage.total_tokens}")

    # Image message call
    ai_logger.debug("Processing image message query")
    response, cost, usage = agent.call(image_message_list)
    ai_logger.info(f"Image query completed - Cost: ${cost.total_cost:.4f}, Tokens: {usage.total_tokens}")

    # Strict template message call
    ai_logger.debug("Processing strict template message query")
    response, cost, usage = agent.call(strict_message_list)
    ai_logger.info(f"Strict template query completed - Cost: ${cost.total_cost:.4f}, Tokens: {usage.total_tokens}")

    # Print final results
    print("\n=== Final Results ===")
    print(f"Response: {response}")
    print(f"Cost: ${cost.total_cost:.4f}")
    print(f"Total tokens used: {usage.total_tokens}")

    ai_logger.info("OpenAI Framework demo completed successfully")


if __name__ == "__main__":
    run_examples()
