"""
fallback/fallback_handler.py
Handles failures gracefully so the app never crashes on the student.
"""

import time


def with_fallback(func, fallback_value: str, retries: int = 2, delay: float = 1.0):
    """
    Calls `func()`. If it raises an exception, retries up to `retries` times.
    If all retries fail, returns `fallback_value` instead of crashing.

    Usage:
        result = with_fallback(
            lambda: my_tool.run(input),
            fallback_value="Sorry, the tool is unavailable right now."
        )
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as e:
            last_error = e
            print(f"[Fallback] Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)

    print(f"[Fallback] All {retries} attempts failed. Using fallback value.")
    return fallback_value


def validate_llm_output(output: str, min_length: int = 20) -> str:
    """
    Checks that the LLM returned something meaningful.
    If the output is too short or empty, returns a safe fallback message.
    """
    if not output or len(output.strip()) < min_length:
        return (
            "I was unable to generate a proper response for this topic. "
            "Please try rephrasing your question or choosing a different subject."
        )
    return output.strip()
