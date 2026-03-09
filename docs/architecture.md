# Project Architecture

This repository follows a simple layered architecture designed for small AI applications.

The goal is to keep the code easy to understand, easy to extend, and friendly for AI-assisted development.

---

## High-level architecture

UI
↓
Services (business logic)
↓
Integrations (external systems)
↓
Storage / Database

---

## Folder Responsibilities

### app.py

Application entry point.

Examples:
- Streamlit UI
- FastAPI server
- CLI tool

This file should stay thin and delegate real work to services.

---

### src/services/

Contains **core business logic** of the application.

Each service usually represents a feature or workflow.

Examples:

- generate_newsletter
- generate_social_post
- summarize_document

Services should not directly call external APIs.  
Instead they call integrations.

---

### src/integrations/

Handles communication with **external systems**.

Examples:

- OpenAI
- Anthropic
- databases
- email providers
- payment systems

Examples in this project:

- llm.py → communication with LLM providers
- storage.py → SQLite persistence (schema and writes). For larger projects, you can move schema/migrations to **src/db/**.

---

### src/prompts/

Optional. Stores prompt templates used by AI workflows.

Keeping prompts separate makes them easier to edit, test, and version. This template does not yet load prompts from here; add files when you introduce system prompts or reusable templates.

---

### src/db/

Optional. Database logic when you want to separate it from integrations.

This may include:

- SQLite setup
- database models
- migrations

Right now, SQLite is implemented in **src/integrations/storage.py**. Use **src/db/** when you add migrations or want a dedicated place for schema.

---

### src/utils/

Small helper functions that do not belong to a specific domain.

Examples:

- formatting helpers
- parsing helpers
- logging utilities

---

### tests/

Automated tests for the project.

Even small projects should include basic tests to prevent regressions.

---

## Design principles

1. Prefer readability over clever code
2. Keep UI separate from business logic
3. Isolate external integrations
4. Keep prompts separate from Python code
5. Make the project easy for future maintainers to understand

---

## Purpose of this template

This starter template is designed for building **AI-powered Python applications quickly while maintaining clean architecture**.
