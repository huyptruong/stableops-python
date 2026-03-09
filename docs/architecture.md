# Project Architecture

StableOps uses a simple layered architecture: UI → services → integrations → storage.

---

## High-level architecture

```
UI (app.py)
    ↓
Services (business logic)
    ↓
Integrations (LLM, storage)
    ↓
SQLite (single database)
```

---

## Folder responsibilities

### app.py

Streamlit entry point. Calls `bootstrap_app()` from `src/startup` once at the top, then renders the UI, builds input from user input, calls one service per workflow, and displays results. Stays thin; no business logic or direct external calls.

---

### src/startup.py

Single bootstrap: `bootstrap_app()` runs `load_dotenv()`, `ensure_data_dir()`, `configure_logging()`, `init_db()`. Call once at app entry before any UI.

---

### src/services/

Core workflow logic. Each module implements one workflow (e.g. Create Social Post).

**Current:** `create_social_post.py` — `run_create_social_post(inp, use_llm)` builds prompts, calls the LLM integration (or uses a template fallback), saves the result via the artifact integration, and returns a structured output.

Services call integrations (LLM, storage); they do not call external APIs directly.

---

### src/integrations/

External systems:

- **llm.py** — `llm_complete_chat(system_prompt, user_prompt, max_tokens)`. Uses OpenAI (Chat API) or Anthropic, or returns a stub when no API key is set. API key is resolved in `src/config.py` (Streamlit secrets first, then env `OPENAI_API_KEY`).
- **storage.py** — SQLite: `init_db()` (creates `artifacts` table), `save_artifact(kind, content, meta)`, `load_artifacts(kind?, limit)`. Single database file (`data/app.db` by default).
- **artifacts.py** — Re-exports `save_artifact` and `load_artifacts` from storage so callers can import from a single place.

---

### src/prompts/

Prompt templates used by workflows. Services import and format them (e.g. `SOCIAL_POST_SYSTEM`, `SOCIAL_POST_USER` in `social_post.py`). Keeps prompt text separate from service code for easier editing and versioning.

**Current:** `social_post.py` — system and user prompt strings for the Create Social Post workflow.

---

### src/config.py

Configuration and env: paths (`DATA_DIR`, `SQLITE_PATH`), model names, API key resolution. `get_openai_api_key()` returns the OpenAI key (Streamlit secrets first, then `OPENAI_API_KEY` env). `.env` is loaded at startup in `bootstrap_app()` (see `src/startup.py`), not at config import.

---

### src/schemas.py

Pydantic models for workflow inputs and outputs (e.g. `CreatePostInput`, `CreatePostOutput`, `SocialPlatform`). Used by the app and services.

---

### src/db/

Optional. Right now all database logic lives in **src/integrations/storage.py** (single `artifacts` table). Use `src/db/` when you add migrations or want schema in a dedicated place.

---

### src/utils/

Helpers that don’t belong to a specific workflow (none used by the current workflows).

---

### tests/

Pytest tests. Current: smoke test plus tests for `run_create_social_post` (fallback and LLM paths, with mocks for LLM and `save_artifact`).

---

## Design principles

1. Prefer readability over clever code.
2. Keep UI separate from business logic.
3. Isolate external integrations.
4. Keep prompts in `src/prompts/`, separate from service code.
5. One database for app data (artifacts); config centralised in `src/config.py`.

---

## Purpose

StableOps is an AI-powered app for therapeutic riding programs. This architecture keeps the codebase easy to understand and extend as new workflows are added.
