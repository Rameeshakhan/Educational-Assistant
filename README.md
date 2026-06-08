# 📚 Education Assistant — CrewAI Project

A beginner-friendly agentic AI application built with **CrewAI**, **Streamlit**, and **Langfuse**.

---

## What it does

You enter a topic (e.g. "Photosynthesis") and choose a difficulty level.  
Three AI agents then work together to:

1. **Research** the topic using Wikipedia
2. **Explain** it at your chosen level (beginner / intermediate / advanced)
3. **Quiz** you with multiple-choice questions

---

## Project Structure

```
education_assistant/
├── app.py                    ← Streamlit UI (run this)
├── crew.py                   ← Assembles and runs the CrewAI crew
├── agents.py                 ← Defines the 3 agents
├── tasks.py                  ← Defines the 3 tasks
├── tools/
│   └── custom_tool.py        ← 3 tools (Wikipedia, Difficulty Adjuster, Quiz Generator)
├── fallback/
│   └── fallback_handler.py   ← Retry + validation logic
├── monitoring/
│   └── langfuse_config.py    ← Langfuse observability setup
├── outputs/                  ← Saved session results (auto-created)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup Instructions

### Step 1 — Clone / download the project

```bash
cd education_assistant
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up your API keys

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```
OPENAI_API_KEY=sk-...          # Required — get from https://platform.openai.com
LANGFUSE_PUBLIC_KEY=pk-...     # Optional — get free at https://langfuse.com
LANGFUSE_SECRET_KEY=sk-...     # Optional
```

### Step 5 — Run the app

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Agents

| Agent | Role | Tool Used |
|-------|------|-----------|
| Research Agent | Finds facts about the topic | Wikipedia Summary Tool |
| Explainer Agent | Rewrites content at the right level | Difficulty Adjuster Tool (custom) |
| Quiz Agent | Creates a multiple-choice quiz | Quiz Generator Tool (custom) |

---

## Tools

| Tool | Type | Purpose |
|------|------|---------|
| `WikipediaSummaryTool` | External API | Fetches topic summary from Wikipedia |
| `DifficultyAdjusterTool` | **Custom** | Adjusts explanation level (beginner/intermediate/advanced) |
| `QuizGeneratorTool` | **Custom** | Builds a structured quiz prompt for the LLM |

---

## Fallback Mechanism

- `with_fallback()` retries any failing function up to 2 times before returning a safe message
- `validate_llm_output()` checks that LLM responses are not empty or too short
- If the entire crew fails, a user-friendly error is shown instead of a crash
- **Test it**: disconnect your internet — the Wikipedia tool will time out and the fallback message will appear

---

## Langfuse Observability

Langfuse automatically tracks:
- Every LLM call (prompt + response + tokens)
- Every tool invocation
- Agent execution steps
- Errors and latencies

View traces at: https://cloud.langfuse.com

---

## MCP Discussion

If MCP (Model Context Protocol) were used:

- **Wikipedia** could be an MCP server, exposing a `get_summary(topic)` tool that any agent can call
- **Quiz APIs** (e.g. Open Trivia DB) could be an MCP server
- **Textbook/document stores** could be MCP servers with RAG capabilities
- This would make tool discovery automatic and tool integration standardised — no hardcoded URLs
- Agents would connect to an MCP registry and find the right tool by capability, not by name

---

## Example Output

**Topic**: Photosynthesis | **Level**: Beginner | **Questions**: 3

> **Research**: Photosynthesis is the process by which plants use sunlight, water, and CO₂ to produce glucose...
>
> **Explanation**: Think of a plant like a tiny kitchen. The sun is the stove, water and air are the ingredients...
>
> **Quiz**:
> 1. What do plants use to make food? A) Moonlight B) Sunlight ✓ C) Wind D) Rain
