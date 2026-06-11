"""
monitoring/langfuse_config.py
Langfuse v4 — pure OpenTelemetry auto-instrumentation, no manual init needed.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def setup_langfuse():
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
    host = os.getenv("LANGFUSE_HOST") or os.getenv("LANGFUSE_BASE_URL") or "https://cloud.langfuse.com"

    if not public_key or not secret_key:
        print("[Langfuse] WARNING: Keys not set — monitoring disabled.")
        return False

    os.environ["LANGFUSE_PUBLIC_KEY"] = public_key
    os.environ["LANGFUSE_SECRET_KEY"] = secret_key
    os.environ["LANGFUSE_HOST"]       = host

    try:
        from langfuse.openai import openai  # patches OpenAI client automatically
        from langfuse import get_client

        # Verify auth so you know immediately if keys are wrong
        get_client().auth_check()

        print(f"[Langfuse] ✓ OpenAI instrumented and authenticated -> {host}")
        return True
    except Exception as e:
        print(f"[Langfuse] ERROR: Could not initialize — {e}")
        return False


def flush_langfuse():
    try:
        from langfuse import get_client
        get_client().flush()
    except Exception:
        pass