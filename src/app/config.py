import os


class Config:
    """Configuration class to manage environment variables."""
    LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://localhost:1234")
    LLM_NAME = os.getenv("LLM_NAME", "gemma-4-26b-a4b-it-mlx")
    LLM_APIKEY = os.getenv("LLM_APIKEY", "**FakeKEy**")
