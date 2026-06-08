"""
agents.py
Defines the three agents in the Education Assistant crew.
"""

from crewai import Agent
from tools.custom_tool import WikipediaSummaryTool, DifficultyAdjusterTool, QuizGeneratorTool


def create_agents(difficulty: str = "beginner"):
    """Create and return the three education agents."""

    wiki_tool       = WikipediaSummaryTool()
    adjuster_tool   = DifficultyAdjusterTool()
    quiz_tool       = QuizGeneratorTool()

    # ── Agent 1: Research Agent ──────────────────────────────────────────
    research_agent = Agent(
        role="Educational Research Agent",
        goal="Gather accurate and factual information about the requested topic.",
        backstory=(
            "You are a knowledgeable research assistant specialised in finding clear, "
            "reliable educational content. You always verify facts and present information "
            "in a structured way."
        ),
        tools=[wiki_tool],
        verbose=True,
        allow_delegation=False,
    )

    # ── Agent 2: Explainer Agent ─────────────────────────────────────────
    explainer_agent = Agent(
        role="Educational Explainer Agent",
        goal=(
            f"Take the researched information and explain it clearly "
            f"at a {difficulty} level so students can understand it easily."
        ),
        backstory=(
            "You are a patient and creative teacher who specialises in breaking down "
            "complex topics into digestible lessons. You adapt your language to the "
            "student's level and always include relatable examples."
        ),
        tools=[adjuster_tool],
        verbose=True,
        allow_delegation=False,
    )

    # ── Agent 3: Quiz Agent ──────────────────────────────────────────────
    quiz_agent = Agent(
        role="Quiz Creator Agent",
        goal="Create a short multiple-choice quiz to test the student's understanding of the topic.",
        backstory=(
            "You are an experienced educator who writes clear, fair, and educational quizzes. "
            "Your questions reinforce key concepts and are always matched to the student's level."
        ),
        tools=[quiz_tool],
        verbose=True,
        allow_delegation=False,
    )

    return research_agent, explainer_agent, quiz_agent
