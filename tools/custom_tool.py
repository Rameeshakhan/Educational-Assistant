"""
tools/custom_tool.py
Three tools used by the education assistant agents.
"""

import requests
from crewai.tools import BaseTool
from pydantic import Field


# ─────────────────────────────────────────────
# Tool 1 (CUSTOM): Quiz Generator
# Used by: Quiz Agent
# What it does: Takes a topic + number of questions → returns a plain-text quiz
# ─────────────────────────────────────────────
class QuizGeneratorTool(BaseTool):
    name: str = "Quiz Generator"
    description: str = (
        "Generates a simple multiple-choice quiz for a given topic. "
        "Input format: 'topic | number_of_questions'  e.g. 'Photosynthesis | 3'"
    )

    def _run(self, input_text: str) -> str:
        # Parse input
        parts = input_text.split("|")
        topic = parts[0].strip() if len(parts) > 0 else "General Knowledge"
        try:
            num_q = int(parts[1].strip()) if len(parts) > 1 else 3
        except ValueError:
            num_q = 3

        # Build a structured prompt result (no extra API needed — we use the LLM backbone)
        return (
            f"Generate exactly {num_q} multiple-choice questions about '{topic}'. "
            f"For each question provide: the question text, four options (A/B/C/D), "
            f"and the correct answer. Format clearly and keep language simple."
        )


# ─────────────────────────────────────────────
# Tool 2: Wikipedia Summary Tool
# Used by: Research Agent
# What it does: Fetches a short summary of any topic from Wikipedia REST API
# ─────────────────────────────────────────────
class WikipediaSummaryTool(BaseTool):
    name: str = "Wikipedia Summary"
    description: str = (
        "Fetches a short educational summary about a topic from Wikipedia. "
        "Input: the topic name, e.g. 'Photosynthesis'"
    )

    def _run(self, topic: str) -> str:
        topic_clean = topic.strip().replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic_clean}"

        try:
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                return data.get("extract", "No summary found.")
            else:
                return f"Wikipedia returned status {response.status_code} for '{topic}'."
        except requests.exceptions.Timeout:
            return "Wikipedia request timed out. Using offline knowledge instead."
        except Exception as e:
            return f"Wikipedia lookup failed: {str(e)}"


# ─────────────────────────────────────────────
# Tool 3: Difficulty Adjuster Tool (CUSTOM)
# Used by: Explainer Agent
# What it does: Wraps content with instructions to simplify or deepen explanation
# ─────────────────────────────────────────────
class DifficultyAdjusterTool(BaseTool):
    name: str = "Difficulty Adjuster"
    description: str = (
        "Adjusts the explanation level of educational content. "
        "Input format: 'level | content'  where level is beginner / intermediate / advanced"
    )

    def _run(self, input_text: str) -> str:
        parts = input_text.split("|", 1)
        level   = parts[0].strip().lower() if len(parts) > 0 else "beginner"
        content = parts[1].strip()         if len(parts) > 1 else input_text

        level_instructions = {
            "beginner":     "Use very simple words. Avoid jargon. Add a real-life analogy.",
            "intermediate": "Use standard academic language. Include key terms with brief definitions.",
            "advanced":     "Use precise technical language. Include deeper mechanisms and edge cases.",
        }

        instruction = level_instructions.get(level, level_instructions["beginner"])
        return f"Rewrite the following content for a {level} student. {instruction}\n\nContent:\n{content}"
