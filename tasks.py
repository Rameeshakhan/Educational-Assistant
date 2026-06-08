"""
tasks.py
Defines the three tasks that flow through the crew sequentially.
"""

from crewai import Task


def create_tasks(research_agent, explainer_agent, quiz_agent, topic: str, difficulty: str, num_questions: int):
    """Create and return the three sequential tasks."""

    # ── Task 1: Research the topic ───────────────────────────────────────
    research_task = Task(
        description=(
            f"Use the Wikipedia Summary tool to find factual information about: '{topic}'. "
            f"Return a concise summary with the most important facts, definitions, and concepts."
        ),
        expected_output=(
            "A factual 2-4 paragraph summary of the topic with key concepts clearly identified."
        ),
        agent=research_agent,
    )

    # ── Task 2: Explain the topic at the right difficulty level ──────────
    explain_task = Task(
        description=(
            f"Take the research summary from the previous task and use the Difficulty Adjuster tool "
            f"to rewrite it for a '{difficulty}' level student about the topic '{topic}'. "
            f"Make sure the explanation is clear, engaging, and educational. "
            f"Include a real-life example if possible."
        ),
        expected_output=(
            f"A well-structured educational explanation of '{topic}' written for a {difficulty} student. "
            f"Should include: a simple definition, key points, and one example."
        ),
        agent=explainer_agent,
        context=[research_task],  # receives output from research_task
    )

    # ── Task 3: Generate a quiz ──────────────────────────────────────────
    quiz_task = Task(
        description=(
            f"Use the Quiz Generator tool to create {num_questions} multiple-choice questions "
            f"about '{topic}' for a '{difficulty}' level student. "
            f"Base the questions on the explanation from the previous task. "
            f"Format: each question numbered, four options (A/B/C/D), and the correct answer at the end."
        ),
        expected_output=(
            f"{num_questions} clear multiple-choice questions about '{topic}' with answer key."
        ),
        agent=quiz_agent,
        context=[explain_task],  # receives output from explain_task
    )

    return research_task, explain_task, quiz_task
