"""Interface to LLM providers."""

from typing import Literal, get_args

from langchain.chat_models.base import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# TODO : Complete the list of the models.
google_models_literal = Literal["gemini-2.0-flash"]  # to be completed
anthropic_models_literal = Literal["claude-3-5-sonnet-latest"]  # to be completed
openai_models_literal = Literal["gpt-4o-mini"]  # to be completed
ollama_models_literal = Literal["llama3.2:latest"]  # to be completed
all_models_literal = Literal[
    "gemini-2.0-flash", "claude-3-5-sonnet-latest", "gpt-4o-mini", "llama3.2:latest"
]


def get_llm(model_name: all_models_literal) -> BaseChatModel:
    """Returns the appropriate ChatModel based on the model name."""

    if model_name in get_args(google_models_literal):
        return ChatGoogleGenerativeAI(model=model_name)
    elif model_name in get_args(anthropic_models_literal):
        return ChatAnthropic(model_name=model_name)
    elif model_name in get_args(openai_models_literal):
        return ChatOpenAI(model=model_name)
    elif model_name in get_args(ollama_models_literal):
        return ChatOllama(model=model_name)
    else:
        raise ValueError(f"Model {model_name} not supported.")
