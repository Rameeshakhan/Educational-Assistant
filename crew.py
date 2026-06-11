"""
crew.py
Assembles agents + tasks into a CrewAI Crew and runs it.
"""

import os
from crewai import Crew, Process
from agents import create_agents
from tasks  import create_tasks
from fallback.fallback_handler import validate_llm_output


def run_education_crew(topic: str, difficulty: str = "beginner", num_questions: int = 3) -> dict:
    """
    Main entry point. Builds the crew, runs it, and returns results.

    Returns a dict with keys:
        - research   : raw research summary
        - explanation: adjusted explanation
        - quiz       : generated quiz
        - error      : error message if something went wrong (else None)
    """

    # 1. Set LLM model via environment (CrewAI uses OPENAI_API_KEY automatically)
    os.environ.setdefault("OPENAI_MODEL_NAME", "gpt-4o-mini")

    # 2. Build agents and tasks
    research_agent, explainer_agent, quiz_agent = create_agents(difficulty=difficulty)
    research_task, explain_task, quiz_task = create_tasks(
        research_agent, explainer_agent, quiz_agent,
        topic=topic, difficulty=difficulty, num_questions=num_questions
    )

    # 3. Assemble the crew (sequential: task 1 → task 2 → task 3)
    crew = Crew(
        agents=[research_agent, explainer_agent, quiz_agent],
        tasks=[research_task, explain_task, quiz_task],
        process=Process.sequential,
        verbose=True,
        # tracing=True removed — Langfuse v4 instruments via OpenTelemetry automatically
    )

    # 4. Run with fallback protection
    try:
        result = crew.kickoff()

        research_output    = validate_llm_output(str(research_task.output))
        explanation_output = validate_llm_output(str(explain_task.output))
        quiz_output        = validate_llm_output(str(quiz_task.output))

        return {
            "research":    research_output,
            "explanation": explanation_output,
            "quiz":        quiz_output,
            "error":       None,
        }

    except Exception as e:
        print(f"[Fallback] Crew execution failed: {e}")
        fallback_text = (
            "I couldn't complete the learning session because the AI service is unavailable. "
            "Please check your OpenAI API key and try again."
        )
        return {
            "research":    fallback_text,
            "explanation": fallback_text,
            "quiz":        fallback_text,
            "error": (
                f"The education assistant encountered an error: {str(e)}\n\n"
                "Please check your API keys in the .env file and try again."
            ),
        }