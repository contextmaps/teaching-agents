# CC Prompt — HANDOFF_09_PATCH

You are picking up the static-site project for Pamplin College of Business at Virginia Tech. HANDOFF_09 (commit ef296b9) revised the tutorial pages — replaced screenshots with terminology + ask-the-platform fallbacks, dropped the "under review" banner, kept the recipe-field-to-platform-field mapping table. In HANDOFF_09's final report, CC surfaced one known issue: multi-paragraph step bodies in the tutorial JSONs preserve `\n\n` as data, but the templates render each step body inside a single `<p>` tag, so the paragraph breaks aren't visible in the browser.

This patch fixes that — a two-line Jinja change in two template files, no JSON content changes, no schema changes.

## Mandatory reading order

1. **`HANDOFF_09_PATCH.md`** — full document. Your work order, the template change, done criteria.
2. **`templates/tutorial.html`** — to find the step body rendering line.
3. **`templates/notebooklm.html`** — same change in the NotebookLM template.

## Your task

Apply the patch:

- Update `templates/tutorial.html` to split each step body on `\n\n` and emit one `<p class="tutorial-step__body">` per paragraph.
- Apply the same change to `templates/notebooklm.html`.
- Run `python build.py`.
- Verify multi-paragraph steps render with visible paragraph breaks (Copilot Step 1, ChatGPT Step 2, Claude Step 3 are good test cases — each has a two-paragraph body).
- Confirm no regression on recipe pages.
- Commit and push as a single commit per D4.

## Operational guidance

**The change is mechanical.** Find the existing `<p class="tutorial-step__body">{{ step.body }}</p>` (or equivalent) and replace with:

```jinja
{% for paragraph in step.body.split('\n\n') %}
<p class="tutorial-step__body">{{ paragraph }}</p>
{% endfor %}
```

If the existing rendering uses a slightly different form (e.g., a filter chain like `{{ step.body | safe }}`), apply the split logic appropriately — the key is that the split happens on `\n\n` and each result becomes its own `<p>`. Preserve any existing filters or escaping behavior.

**Confirm via rendered HTML.** After rebuild, check `docs/tutorials/copilot.html` (or wherever tutorials render): the rendered HTML for Step 1 should contain *two* `<p class="tutorial-step__body">` elements — one for "Sign in to Copilot at copilot.microsoft.com..." and one for "If you land in Microsoft 365 Copilot search...". Not one `<p>` containing both with a collapsed line break.

## Constraints — non-negotiable

- **No content changes.** Tutorial JSONs untouched.
- **No schema changes.**
- **No new dependencies.**
- **No styling changes.** The `tutorial-step__body` class stays.
- **Single commit.**

## Working approach

1. **Read HANDOFF_09_PATCH fully.**
2. **Open `templates/tutorial.html`** and locate the step body rendering.
3. **Apply the split.**
4. **Open `templates/notebooklm.html`** and apply the same change.
5. **Rebuild** with `python build.py`.
6. **Spot-check a multi-paragraph step** (e.g., Copilot Step 1) in the rendered HTML to confirm two distinct `<p>` elements.
7. **Confirm a single-paragraph step** still renders as a single `<p>`.
8. **Commit and push** per D4.

## Final report format

1. **What got changed.** The two template files, the exact Jinja change.
2. **Decisions made.** Especially: if the existing template rendering used a slightly different form than expected, how you adapted the split logic.
3. **Done-criteria status.** Walk through the criteria as a checklist.
4. **Sample output.** Paste the rendered HTML for one multi-paragraph step (Copilot Step 1 ideal) showing the two `<p>` elements. Paste a single-paragraph step to confirm it renders unchanged.
5. **No-regression confirmation.** Confirm one recipe page still renders correctly.
6. **Conflicts encountered.** None expected.
7. **Known issues.** Anything you'd flag.
8. **Verification.** Confirm `python build.py` runs clean.

Be honest in the report.

## Begin

Read HANDOFF_09_PATCH.md. Open `templates/tutorial.html`. Then proceed.
