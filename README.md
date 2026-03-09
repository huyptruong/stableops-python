# StableOps

AI-powered tools for therapeutic riding programs. Python + Streamlit app built on a simple layered architecture.

---

## What’s included

- **Create Social Post** — Generate social post content for Instagram and/or Facebook (AI or template fallback). Results are saved in the app database.
- **Create Newsletter** — Generate newsletter subject and body (AI). Results are saved as artifacts.
- **Draft Grant Proposal** — Draft grant narrative sections with suggested headings (AI). Results are saved as artifacts.

---

## Local setup

**Dependencies:** `pyproject.toml` is the source of truth. For run-only installs (e.g. Streamlit Community Cloud), `requirements.txt` lists the same runtime dependencies. When you add or change dependencies in `pyproject.toml`, update `requirements.txt` to match (e.g. copy the `[project.dependencies]` list).

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

For local development including tests: `pip install -e '.[dev]'` (installs runtime + pytest).

Add your API key(s) to `.env`, then:

```bash
streamlit run app.py
```

Run tests:

```bash
pytest
```

(Requires dev dependencies: `pip install -e '.[dev]'` or `pip install pytest`.)

---

## Environment variables

See `.env.example` for a template.

- **OPENAI_API_KEY** — Used for AI generation (optional; template fallback if unset). On Streamlit Community Cloud, set it in app Secrets; locally, set it in `.env`. Config resolves it via `get_openai_api_key()` (secrets first, then env).
- **ANTHROPIC_API_KEY** — Used if OpenAI is not set (optional).
- **OPENAI_MODEL**, **ANTHROPIC_MODEL** — Model names (defaults in `.env.example`).
- **MAX_TOKENS_SOCIAL_POST** — Max tokens for social post (default: 512).
- **MAX_TOKENS_NEWSLETTER** — Max tokens for newsletter (default: 1024).
- **MAX_TOKENS_GRANT** — Max tokens for grant draft (default: 2048).
- **DATA_DIR**, **SQLITE_PATH** — Override data directory and database path (defaults: `./data`, `./data/app.db`).

---

## Project structure

```
app.py                → Streamlit UI (thin; delegates to services)
src/config.py         → Configuration, env vars, API key resolution (secrets + env)
src/services/         → Workflow logic (e.g. create_social_post)
src/integrations/     → LLM (OpenAI/Anthropic), storage (SQLite artifacts)
src/prompts/          → AI prompt templates (e.g. social_post)
src/schemas.py        → Pydantic input/output models
tests/                → Pytest tests
docs/                 → Architecture and development notes
```

See **AGENTS.md** and `docs/architecture.md` for conventions and AI-assisted development.

---

## Version control

**Tracked (source):** Application code (`app.py`, `src/`, `tests/`), config and docs (`pyproject.toml`, `requirements.txt`, `docs/`, `AGENTS.md`, `.env.example`, `.gitignore`). The `data/` directory exists in the repo with a `.gitkeep` placeholder only.

**Not tracked (runtime/generated):** Everything under `data/` except `.gitkeep` (e.g. `data/app.db`), `.env` (secrets), `.venv/`, `__pycache__/`, `.pytest_cache/`, and `*.pyc`. These are created locally or at deploy time and should not be committed.


---

## Purpose

StableOps helps therapeutic riding programs with AI-assisted content (social posts, and more workflows over time) while keeping the codebase readable and easy to extend.
