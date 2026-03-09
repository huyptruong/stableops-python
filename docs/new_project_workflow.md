# Development workflow

This document describes how to run, develop, and extend the StableOps app.

---

## 1. Get the repo

Clone or fork the repo:

```bash
cd ~/git_repos
git clone <repo-url> stableops-python
cd stableops-python
```

---

## 2. Open the project in Cursor

```bash
cursor .
```

---

## 3. Use the master build prompt (for new features)

When adding a new workflow or feature, open:

```
docs/prompts/master_build_prompt.md
```

Paste the prompt into Cursor and describe what you want to build (e.g. new workflow, who the user is, main steps).

---

## 4. Run the project locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

---

## 5. Ask Cursor for a review

Use the review prompt:

```
docs/prompts/review_prompt.md
```

Ask Cursor to review the architecture and suggest improvements.

---

## 6. Keep structure clear before adding many features

Focus on:

- readability
- service boundaries
- prompt structure
- tests
- storage
