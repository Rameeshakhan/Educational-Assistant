"""
app.py  –  Education Assistant (Streamlit UI)
Run with:  streamlit run app.py
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ── Make sure local modules are importable ────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Education Assistant",
    page_icon="📚",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Sora', sans-serif;
    }

    /* Header banner */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .hero h1 { font-size: 2rem; margin: 0; color: #e2e8f0; }
    .hero p  { color: #94a3b8; margin: 0.5rem 0 0; font-size: 1rem; }

    /* Section cards */
    .result-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0f3460;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .result-card h3 { margin-top: 0; color: #0f3460; font-family: 'Sora', sans-serif; }

    /* Agents info */
    .agent-box {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #f1f5f9 !important;
    }
    .agent-box b {
        color: #ffffff !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #0f3460, #1a237e);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📚 Education Assistant</h1>
    <p>Powered by CrewAI · 3 agents work together to teach and test you</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar: API key check + how it works ────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Setup")

    openai_key = os.getenv("OPENAI_API_KEY", "")
    if openai_key and openai_key != "your_openai_api_key_here":
        st.success("✅ OpenAI key loaded")
    else:
        st.error("❌ OpenAI key missing")
        st.info("Add your key to `.env` file:\n```\nOPENAI_API_KEY=sk-...\n```")

    langfuse_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    if langfuse_key and langfuse_key != "your_langfuse_public_key":
        st.success("✅ Langfuse monitoring on")
    else:
        st.warning("⚠️ Langfuse keys missing\n(monitoring disabled)")

    st.divider()
    st.markdown("### 🤖 How it works")
    st.markdown("""
<div class="agent-box">🔍 <b>Research Agent</b><br>Fetches facts from Wikipedia</div>
<div class="agent-box">📖 <b>Explainer Agent</b><br>Rewrites for your level</div>
<div class="agent-box">✏️ <b>Quiz Agent</b><br>Creates a quiz for you</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🛡️ Fallback")
    st.markdown("If any step fails, the app retries automatically and returns a safe message instead of crashing.")

    st.divider()
    st.markdown("### 📡 MCP Note")
    st.markdown("""
In a future version, tools like Wikipedia, Quiz APIs, and textbook databases could be exposed as **MCP servers**, letting agents discover and call them in a standardised way without hardcoded URLs.
""")


# ── Main form ─────────────────────────────────────────────────────────────────
st.markdown("### 🎯 What do you want to learn?")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    topic = st.text_input(
        "Topic",
        placeholder="e.g. Photosynthesis, World War 2, Newton's Laws...",
        label_visibility="collapsed",
    )

with col2:
    difficulty = st.selectbox(
        "Level",
        options=["beginner", "intermediate", "advanced"],
        label_visibility="collapsed",
    )

with col3:
    num_questions = st.number_input(
        "Questions",
        min_value=1, max_value=5, value=3,
        label_visibility="collapsed",
    )

st.caption("Topic  ·  Difficulty level  ·  Number of quiz questions")

run_button = st.button("🚀 Start Learning Session")


# ── Run the crew ──────────────────────────────────────────────────────────────
if run_button:
    if not topic.strip():
        st.warning("Please enter a topic before starting.")
    elif not openai_key or openai_key == "your_openai_api_key_here":
        st.error("Please add your OpenAI API key to the .env file first.")
    else:
        # Import here so missing packages don't crash the UI on startup
        from crew import run_education_crew

        with st.spinner("🤖 Agents are working... this may take 30–60 seconds"):
            results = run_education_crew(
                topic=topic.strip(),
                difficulty=difficulty,
                num_questions=num_questions,
            )

        # ── Show error if crew failed ──────────────────────────────────
        if results["error"]:
            st.error(results["error"])

        else:
            st.success("✅ Learning session complete!")
            st.markdown("---")

            # ── Research output ────────────────────────────────────────
            st.markdown('<div class="result-card"><h3>🔍 Research Summary</h3>', unsafe_allow_html=True)
            st.markdown(results["research"])
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Explanation output ─────────────────────────────────────
            st.markdown('<div class="result-card"><h3>📖 Explanation</h3>', unsafe_allow_html=True)
            st.markdown(results["explanation"])
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Quiz output ────────────────────────────────────────────
            st.markdown('<div class="result-card"><h3>✏️ Quiz</h3>', unsafe_allow_html=True)
            st.markdown(results["quiz"])
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Save output to file ────────────────────────────────────
            output_path = Path("outputs") / f"{topic.replace(' ', '_')}_session.md"
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(
                f"# Topic: {topic}  |  Level: {difficulty}\n\n"
                f"## Research\n{results['research']}\n\n"
                f"## Explanation\n{results['explanation']}\n\n"
                f"## Quiz\n{results['quiz']}\n"
            )
            st.caption(f"💾 Session saved to `{output_path}`")