"""`smartbrowser.llms` module.

Interface to LLM providers.
"""

from typing import Literal, get_args

from langchain.chat_models.base import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI


google_models_literal = Literal["gemini-2.0-flash", "gemini-2.0-flash-lite"]
anthropic_models_literal = Literal[
    "claude-3-7-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-5-sonnet-latest"
]
openai_models_literal = Literal["gpt-4o-mini", "gpt-4o", "o3-mini", "o1-mini"]
ollama_models_literal = Literal["llama3.2:latest"]
all_models_literal = Literal[
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "claude-3-7-sonnet-latest",
    "claude-3-5-haiku-latest",
    "claude-3-5-sonnet-latest",
    "gpt-4o-mini",
    "gpt-4o",
    "o3-mini",
    "o1-mini",
    "llama3.2:latest",
]


def get_llm(model_name: all_models_literal, api_key: str) -> BaseChatModel:
    """Returns the appropriate ChatModel based on the model name."""

    if model_name in get_args(google_models_literal):
        return ChatGoogleGenerativeAI(model=model_name, api_key=api_key)
    elif model_name in get_args(anthropic_models_literal):
        return ChatAnthropic(model_name=model_name, api_key=api_key)
    elif model_name in get_args(openai_models_literal):
        return ChatOpenAI(model=model_name, api_key=api_key)
    elif model_name in get_args(ollama_models_literal):
        return ChatOllama(model=model_name)
    else:
        raise ValueError(f"Model {model_name} not supported.")
