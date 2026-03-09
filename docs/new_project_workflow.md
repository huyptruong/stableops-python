# New Project Workflow

This document describes how to start a new project using this template.

---

## 1. Copy the template

```bash
cd ~/git_repos
cp -r python-ai-starter-template my-new-project
cd my-new-project
```

---

## 2. Open the project in Cursor

```bash
cursor .
```

---

## 3. Use the master build prompt

Open:

```
docs/prompts/master_build_prompt.md
```

Paste the prompt into Cursor and describe the project you want to build.

Example:

- what the app does
- who the user is
- what the main workflow is

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

Use the review prompt located at:

```
docs/prompts/review_prompt.md
```

Ask Cursor to review the architecture and suggest improvements.

---

## 6. Improve structure before adding many features

Focus on:

- readability
- service boundaries
- prompt structure
- tests
- storage
