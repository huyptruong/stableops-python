You are helping me build a Python AI application starting from the stableops-python app.

Follow these rules:

1. Keep the existing project structure unless there is a strong reason to change it.
2. Keep UI code separate from business logic.
3. Put core feature logic into `src/services/`.
4. Put external API/database integrations into `src/integrations/`.
5. Put prompt text into `src/prompts/`.
6. Prefer readable code over clever code.
7. Add the minimum code needed for the first working version.
8. Explain what files you changed and why.
9. Also explain your changes in a simple analogy for a beginner.

When generating code, return:
- what you changed
- why you changed it
- anything fragile or worth improving later
