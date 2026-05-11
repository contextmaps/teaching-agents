# HANDOFF_09_PATCH — Multi-Paragraph Tutorial Step Rendering

**Project:** Pamplin AI Agent Recipes (`teaching-agents`)
**Spec reference:** `SPEC.md` v0.1.3 (no SPEC change required for this patch; it's a rendering correction within the design established by HANDOFF_09)
**Cut:** Patch following HANDOFF_09 (commit ef296b9) — fix multi-paragraph step bodies in tutorial pages to render as real `<p>` elements rather than collapsing into one paragraph.

---

## Why

HANDOFF_09 introduced tutorial step content with intentional paragraph breaks — for instance, Copilot's Step 1 has a main instruction followed by a secondary note about landing in the wrong product. The step body in the JSON preserves these breaks as `\n\n`. CC correctly preserved the data, but the existing `tutorial.html` and `notebooklm.html` templates render each step body inside a single `<p>` tag, and HTML collapses whitespace inside `<p>` — so the secondary paragraphs render flush with the main instruction instead of as distinct beats.

CC surfaced this in HANDOFF_09's final report (Known Issues, item 7), explicitly choosing data fidelity over visual fidelity rather than making an unauthorized template change. The right fix is semantic: render real `<p>` elements for each paragraph by splitting on `\n\n` in the templates.

---

## Inputs

**Repo path:** `contextmaps/teaching-agents`.

**Files to modify:**

```
templates/tutorial.html
templates/notebooklm.html
```

No other files change. No JSON content changes. No build pipeline changes.

---

## Deliverables

### D1 — Update tutorial.html

Find the step body rendering — currently a single `<p>` element of the form:

```jinja
<p class="tutorial-step__body">{{ step.body }}</p>
```

Replace with a Jinja loop that splits the body on `\n\n` and emits one `<p>` per resulting paragraph:

```jinja
{% for paragraph in step.body.split('\n\n') %}
<p class="tutorial-step__body">{{ paragraph }}</p>
{% endfor %}
```

The class on each `<p>` stays the same, so existing styling continues to apply to each paragraph. Steps that contain only one paragraph (no `\n\n` in the body) render unchanged — the loop produces a single iteration.

### D2 — Update notebooklm.html

Same change in `notebooklm.html`. The NotebookLM tutorial template was separated from the four-platform `tutorial.html` early in the project (per HANDOFF_09's report); the same step-body rendering pattern applies, and the same fix.

### D3 — Rebuild and verify

After making the changes:

- `python build.py` runs clean and idempotent.
- Open at least one tutorial page in the browser and confirm that multi-paragraph steps now render with visible paragraph breaks. Good test cases:
  - **Copilot Step 1** has a two-paragraph body (main instruction + the "if you land in Microsoft 365 Copilot search" note). Both paragraphs should be visible as distinct paragraphs.
  - **ChatGPT Step 2** has a two-paragraph body. Same check.
  - **Claude Step 3** has a two-paragraph body. Same check.
- Confirm that single-paragraph steps still render correctly (no extra `<p>` wrappers, no visual change).
- All 23 recipe pages still render correctly (no regression — this patch doesn't touch recipes).

### D4 — Commit and push

A single commit:

```
HANDOFF_09_PATCH: Render multi-paragraph tutorial steps as real paragraphs

- Updates tutorial.html and notebooklm.html templates to split step
  bodies on \n\n and emit one <p> element per paragraph
- Fixes the rendering issue surfaced in HANDOFF_09's final report
  (Known Issues, item 7) where multi-paragraph step bodies collapsed
  into a single visual paragraph
- No JSON content changes; no build pipeline changes; no schema changes
```

---

## Constraints

- **No content changes.** Tutorial JSONs are not touched. Recipe JSONs are not touched.
- **No schema changes.**
- **No new dependencies.**
- **No styling changes.** The `tutorial-step__body` class on each `<p>` stays exactly as it is; CSS continues to handle the rest.
- **Single commit.**

---

## Done criteria

**Template:**
- [ ] `tutorial.html` step body rendering uses `{% for paragraph in step.body.split('\n\n') %}` to emit one `<p>` per paragraph.
- [ ] `notebooklm.html` step body rendering uses the same pattern.
- [ ] The class on each `<p>` is still `tutorial-step__body`.

**Build:**
- [ ] `python build.py` runs clean and idempotent.
- [ ] No errors or warnings.

**Visual verification:**
- [ ] Copilot Step 1 renders as two visible paragraphs.
- [ ] ChatGPT Step 2 renders as two visible paragraphs.
- [ ] Claude Step 3 renders as two visible paragraphs.
- [ ] Single-paragraph steps render unchanged.
- [ ] All 23 recipe pages still render correctly.

**Hygiene:**
- [ ] Single commit with the message specified in D4.
- [ ] CC's final report confirms: the template change, the multi-paragraph rendering in the rebuilt pages, and the no-regression check.

---

## Notes for CC

- **This is a 2-line template change in 2 files.** It's the smallest patch in the project. Don't overthink it.
- **If the step body rendering in either template uses a slightly different form** than the example above (e.g., `{{ step.body | safe }}` or a filter chain), apply the split logic appropriately — the key is that the split happens on `\n\n` and each result becomes its own `<p>`.
- **Confirm the patch via the rendered HTML.** After rebuild, the rendered tutorial page should show multiple `<p class="tutorial-step__body">` elements per multi-paragraph step (not one `<p>` with `\n\n` collapsed inside).
- **No new template logic beyond the split.** Don't add any conditional handling, filters, or escaping changes. Jinja's default escaping continues to apply to each paragraph the same way it applies to a single body.
