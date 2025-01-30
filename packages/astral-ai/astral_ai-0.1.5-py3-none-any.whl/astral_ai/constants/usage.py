# -------------------------------------------------------------------------------- #
# Usage Constants
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Set, Union, Dict

# Module imports 
from src.astral_ai.typing.models import ModelName, ModelNameUnion, ReasoningEffort
from src.astral_ai.typing.usage import TokenCost, TokenCount


# -------------------------------------------------------------------------------- #
# Model Support Constants
# -------------------------------------------------------------------------------- #

DEVELOPER_MESSAGE_SUPPORTED_MODELS: Set[ModelName] = {"o1-2024-12-17"}
SYSTEM_MESSAGE_SUPPORTED_MODELS: Set[ModelName] = {"gpt-4o-2024-11-20"}
REASONING_EFFORT_SUPPORTED_MODELS: Set[ModelName] = {"o1-2024-12-17"}
RESPONSE_MODEL_SUPPORTED_MODELS: Set[ModelName] = {"o1-2024-12-17", "gpt-4o-2024-11-20"}
IMAGE_INGESTION_SUPPORTED_MODELS: Set[ModelName] = {"gpt-4o-2024-11-20", "o1-2024-12-17"}


# -------------------------------------------------------------------------------- #
# Reasoning Effort Constants
# -------------------------------------------------------------------------------- #

REASONING_EFFORT_DEFAULT: ReasoningEffort = "medium"

# -------------------------------------------------------------------------------- #
# Model Cost Constants
# -------------------------------------------------------------------------------- #


# O1 Mini Model Costs
O1_MINI_MODEL_COST_PER_1M_INPUT: TokenCost = 3.00
O1_MINI_MODEL_CACHED_COST_PER_1M_INPUT: TokenCost = 1.50
O1_MINI_MODEL_COST_PER_1M_OUTPUT: TokenCost = 12.00

# O1 Model Costs
O1_MODEL_COST_PER_1M_INPUT: TokenCost = 15
O1_MODEL_CACHED_COST_PER_1M_INPUT: TokenCost = 7.5
O1_MODEL_COST_PER_1M_OUTPUT: TokenCost = 60

# GPT-4o Model Costs
GPT_4O_MODEL_COST_PER_1M_INPUT: TokenCost = 2.50
GPT_4O_MODEL_CACHED_COST_PER_1M_INPUT: TokenCost = 1.25
GPT_4O_MODEL_COST_PER_1M_OUTPUT: TokenCost = 10

# 1 Million Tokens
ONE_MILLION_TOKENS: TokenCount = 1000000

# Model Cost Mappings
MODEL_COSTS: Dict[ModelNameUnion, Dict[str, Union[TokenCost, TokenCount]]] = {
    # Full model names
    "o1-mini-2024-09-12": {
        "prompt_tokens": O1_MINI_MODEL_COST_PER_1M_INPUT,
        "cached_prompt_tokens": O1_MINI_MODEL_CACHED_COST_PER_1M_INPUT,
        "output_tokens": O1_MINI_MODEL_COST_PER_1M_OUTPUT
    },
    "o1-2024-12-17": {
        "prompt_tokens": O1_MODEL_COST_PER_1M_INPUT,
        "cached_prompt_tokens": O1_MODEL_CACHED_COST_PER_1M_INPUT,
        "output_tokens": O1_MODEL_COST_PER_1M_OUTPUT
    },
    "gpt-4o-2024-11-20": {
        "prompt_tokens": GPT_4O_MODEL_COST_PER_1M_INPUT,
        "cached_prompt_tokens": GPT_4O_MODEL_CACHED_COST_PER_1M_INPUT,
        "output_tokens": GPT_4O_MODEL_COST_PER_1M_OUTPUT
    },
    # Aliases
    "o1-mini": {
        "prompt_tokens": O1_MINI_MODEL_COST_PER_1M_INPUT,
        "cached_prompt_tokens": O1_MINI_MODEL_CACHED_COST_PER_1M_INPUT,
        "output_tokens": O1_MINI_MODEL_COST_PER_1M_OUTPUT
    },
    "o1": {
        "prompt_tokens": O1_MODEL_COST_PER_1M_INPUT,
        "cached_prompt_tokens": O1_MODEL_CACHED_COST_PER_1M_INPUT,
        "output_tokens": O1_MODEL_COST_PER_1M_OUTPUT
    },
    "gpt-4o": {
        "prompt_tokens": GPT_4O_MODEL_COST_PER_1M_INPUT,
        "cached_prompt_tokens": GPT_4O_MODEL_CACHED_COST_PER_1M_INPUT,
        "output_tokens": GPT_4O_MODEL_COST_PER_1M_OUTPUT
    }
}
