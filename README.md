# Python AI Starter Template

A reusable Python starter template for building AI-powered applications.

This template provides a clean architecture and basic components so new projects can start quickly while remaining easy to understand and extend.

---

# What this template includes

- Streamlit app shell
- OpenAI integration
- SQLite storage
- environment-based configuration
- simple service layer
- architecture documentation
- prompt templates for Cursor
- basic test setup

---

# Project structure

```
app.py                → application entry point (UI)

src/config.py         → configuration and environment variables
src/services/         → core business logic
src/integrations/     → external systems (LLM, database, etc.)
src/prompts/          → AI prompt templates
src/db/               → database-related code
src/utils/            → helper utilities

tests/                → automated tests
docs/                 → architecture and development documentation
```

---

# Local setup

Create a virtual environment and install dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the environment template:

```bash
cp .env.example .env
```

Add your OpenAI key inside `.env`.

Then run the app:

```bash
streamlit run app.py
```

Run tests (from project root):

```bash
pytest
```

---

# Environment variables

See `.env.example` for a template. Required and optional variables:

Required:

```
OPENAI_API_KEY
```

Optional:

```
OPENAI_MODEL
DATA_DIR      # Override data directory (default: ./data)
SQLITE_PATH   # Override SQLite file path (default: DATA_DIR/app.db)
```

---

# Development principles

This template follows a few simple rules:

- prefer readable code over clever code
- keep UI separate from business logic
- isolate external integrations
- keep prompts separate from Python code
- add tests for important logic

---

# AI-assisted development

For Cursor or other AI tools: see `docs/new_project_workflow.md` and the prompts in `docs/prompts/`. The project also includes `AGENTS.md` and `.cursor/rules/` to keep generated code aligned with this architecture.

---

# Purpose of this template

The goal of this project is to provide a clean starting point for building AI-powered Python applications quickly while keeping the architecture understandable and maintainable.
