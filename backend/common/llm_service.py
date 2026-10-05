import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from helpers.constants import (
    QWEN_MODEL,
    QWEN_SKIP_REASONING,
    LLM_DEFAULT_TEMP,
    MAX_OUTPUT_TOKEN
)

load_dotenv()


if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is missing. Add it to backend/.env file")


def get_groq(model = QWEN_MODEL, 
             max_tokens = MAX_OUTPUT_TOKEN,
             reasoning_effort = QWEN_SKIP_REASONING,
             temperature = LLM_DEFAULT_TEMP):
    return ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_effort=reasoning_effort
    )