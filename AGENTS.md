# Agent guidelines

Use this file to keep AI-assisted changes aligned with the project.

## Structure

- **app.py** — UI entrypoint. Keep it thin; delegate to `src/services/`.
- **src/services/** — Core business logic. Call `src/integrations/`, not external APIs directly.
- **src/integrations/** — External systems (LLM, DB, etc.).
- **src/prompts/** — AI prompt templates for the app.
- **src/db/** — Database schema/migrations (optional; SQLite currently lives in integrations).
- **src/utils/** — Shared helpers.
- **src/config.py** — Configuration and env vars only.

## Conventions

- Prefer readable code over clever code.
- Add tests for important logic. Run: `pytest` from project root.
- Use the existing logging pattern: `logging.getLogger(__name__)` in each module.
- See `docs/architecture.md` and `docs/new_project_workflow.md` for full details.
