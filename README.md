# StableOps

AI-powered tools for therapeutic riding programs. Python + Streamlit app built on a simple layered architecture.

---

## What’s included

- **Create Social Post** — Generate social post content for Instagram and/or Facebook (AI or template fallback). Results are saved in the app database.

---

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Add your API key(s) to `.env`, then:

```bash
streamlit run app.py
```

Run tests:

```bash
pytest
```

---

## Environment variables

See `.env.example` for a template.

- **OPENAI_API_KEY** — Used first for AI generation (optional; template fallback if unset).
- **ANTHROPIC_API_KEY** — Used if OpenAI is not set (optional).
- **OPENAI_MODEL**, **ANTHROPIC_MODEL** — Model names (defaults in `.env.example`).
- **MAX_TOKENS_SOCIAL_POST** — Max tokens for social post (default: 512).
- **DATA_DIR**, **SQLITE_PATH** — Override data directory and database path (defaults: `./data`, `./data/app.db`).

---

## Project structure

```
app.py                → Streamlit UI (thin; delegates to services)
src/config.py         → Configuration and env vars
src/services/         → Workflow logic (e.g. create_social_post)
src/integrations/     → LLM, storage (SQLite)
src/prompts/          → AI prompt templates
src/schemas.py        → Pydantic input/output models
tests/                → Pytest tests
docs/                 → Architecture and development notes
```

See **AGENTS.md** and `docs/architecture.md` for conventions and AI-assisted development.

---

## Purpose

StableOps helps therapeutic riding programs with AI-assisted content (social posts, and more workflows over time) while keeping the codebase readable and easy to extend.
