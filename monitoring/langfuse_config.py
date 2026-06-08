"""
monitoring/langfuse_config.py
Sets up Langfuse for observability — tracks every LLM call, tool use, and error.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def setup_langfuse():
    """
    Configure Langfuse tracing via environment variables.
    CrewAI picks these up automatically when langfuse is installed.
    Returns True if keys are present, False otherwise.
    """
    public_key  = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key  = os.getenv("LANGFUSE_SECRET_KEY", "")
    host        = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not public_key or not secret_key:
        print("[Langfuse] WARNING: LANGFUSE keys not set — monitoring disabled.")
        return False

    # These env vars are read automatically by the langfuse SDK
    os.environ["LANGFUSE_PUBLIC_KEY"] = public_key
    os.environ["LANGFUSE_SECRET_KEY"] = secret_key
    os.environ["LANGFUSE_HOST"]       = host

    print(f"[Langfuse] Monitoring enabled → {host}")
    return True
