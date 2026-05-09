# Pamplin AI Agent Recipes

A static, public-facing recipe book of teaching-focused AI agent designs for Pamplin College of Business faculty at Virginia Tech. Twenty-three recipes across seven families, each fully specified for Microsoft Copilot, ChatGPT, Claude, and Google Gemini, plus four platform tutorials and a NotebookLM appendix.

**Build:**

```bash
pip install -r requirements.txt
python3 build.py
```

The build reads `recipes/`, `tutorials/`, `site_content.json`, and `config.json`, renders Jinja2 templates from `templates/`, and writes the static site to `docs/`. The build is idempotent and runs in well under five seconds. Single dependency: Jinja2.

GitHub Pages serves the live site from this `docs/` folder on `main` (Pages does not support arbitrary folder names — only `/(root)` or `/docs`). The build output is committed; no CI is needed.

**Live site:** <https://contextmaps.github.io/teaching-agents/>

**Architectural source of truth:** [`SPEC.md`](./SPEC.md). For per-iteration work units, see `HANDOFF_*.md`. Operational notes for Pamplin IT live in `JIM_INTEGRATION_NOTES.md`; analytics-form setup in `FORM_SETUP_GUIDE.md`.
