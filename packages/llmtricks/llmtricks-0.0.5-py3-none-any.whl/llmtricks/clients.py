"""Client factory functions for various LLM providers."""

import os
from functools import lru_cache
from typing import Final

from anthropic import Anthropic
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

# Load environment variables once at module import
load_dotenv()

# Constants for environment variable names
OPENAI_KEY: Final = "OPENAI_API_KEY"
GROQ_KEY: Final = "GROQ_API_KEY"
ANTHROPIC_KEY: Final = "ANTHROPIC_API_KEY"


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    """Get a cached OpenAI client instance."""
    return OpenAI(api_key=os.getenv(OPENAI_KEY))


@lru_cache(maxsize=1)
def get_groq_client() -> Groq:
    """Get a cached Groq client instance."""
    return Groq(api_key=os.getenv(GROQ_KEY))


@lru_cache(maxsize=1)
def get_anthropic_client() -> Anthropic:
    """Get a cached Anthropic client instance."""
    return Anthropic(api_key=os.getenv(ANTHROPIC_KEY))
