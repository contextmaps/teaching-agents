# CC Prompt — HANDOFF_05: Family 3 Recipe Authoring

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. Four content-authoring rounds have already landed: HANDOFF_02 (Family 2, 4 recipes + schema and template extensions for customization notes), HANDOFF_03 (Family 1, 6 recipes), HANDOFF_04 (Family 4, 3 recipes). 13 of 23 recipes ship with real content. SPEC v0.1.2 is current.

This handoff (HANDOFF_05) is the fourth content-authoring round. It adds real content for the three Family 3 recipes (discussion and case-method). Mechanically identical to HANDOFF_04; no schema, template, or build-pipeline changes.

## Mandatory reading order

Before changing any files, read in this order:

1. **`HANDOFF_05.md`** — full document. Your work order, including all deliverables (D1 through D3), the verbatim recipe content for three recipes, and the done criteria.
2. **`SPEC.md`** (currently v0.1.2) — for architectural context if needed, especially §7 (Recipe Page Anatomy) and §9 (Build Pipeline and JSON schema).
3. **The three target recipe files** (`recipes/011-discussion-question-generator.json`, `recipes/012-socratic-case-method-facilitator.json`, `recipes/013-case-discussion-debrief-synthesizer.json`) to confirm their current placeholder state.
4. **`HANDOFF_04.md`** as a reference if anything in HANDOFF_05's pattern is unclear — HANDOFF_04 used the same mechanical pattern that HANDOFF_05 follows directly.

If anything in HANDOFF_05 conflicts with `SPEC.md` v0.1.2, surface it in your final report. None is expected.

## Your task

Apply the changes specified in HANDOFF_05:

- For each of the three Family 3 recipes (numbers 3.1 through 3.3, files 011 through 013):
  - Replace `framing_paragraph` with the real text from HANDOFF_05.
  - Replace `fields.instructions` with the real text from HANDOFF_05 (verbatim, including all guillemet markers).
  - Add `customization_notes` field with the markdown content from HANDOFF_05.
  - Set `content_status: "final"`.
- Run `python build.py` and verify clean output.
- Verify the three Family 3 pages render correctly (real content, no DRAFT banner, customization notes section visible).
- Verify the 13 already-final recipe pages (Families 1, 2, 4) still render correctly (no regression).
- Verify the 7 still-placeholder recipes still show DRAFT banners.
- Commit and push as a single commit with the message specified in HANDOFF_05 D3.

The done criteria in HANDOFF_05 are exhaustive — work through them as a checklist.

## Operational guidance

**Same as HANDOFF_04.** This handoff is mechanically identical to HANDOFF_04 — same kinds of fields, same conventions, same constraints. Three recipes, same scope. The `tools/_apply_handoff_04_content.py` pattern works directly here — write `tools/_apply_handoff_05_content.py` with the same structure and adjusted recipe IDs and content blocks.

**On the recipe content.** All Instructions text, framing paragraphs, and customization notes come from HANDOFF_05 verbatim. Do not edit, "improve," or "clean up" the prose. If something looks like a typo, flag it in the final report rather than silently changing it.

**On the guillemet markers `«...»`.** Same as previous handoffs — they are part of the Instructions content, not a templating syntax. Render verbatim. Faculty see them on the page; the agent reads them as punctuation.

**On JSON encoding.** Use `json.dumps()` rather than hand-escaping. The customization notes content includes markdown formatting (bullets, sub-bullets at two-space indent, bold, inline code with backticks), guillemet characters, and apostrophes within prose.

**On character counts.** All three Instructions fields in HANDOFF_05 are within budget (range: 6,065 to 6,696 characters; buffers between 800 and 1,400 characters). Recipes 3.2 and 3.3 are tighter than recent recipes — their behavioral specification is nuanced (student persona for 3.2, synthesis-not-summary for 3.3) which adds words. All within the 7,500-character ceiling. If any recipe exceeds 7,500 characters in the JSON file (raw decoded text), surface it in the final report.

**On rebuild verification.** The rebuild touches all 23 recipe pages. After running `python build.py`:

- Spot-check at least one Family 3 page (e.g., `dist/recipes/socratic-case-method-facilitator.html`) for: real Instructions visible, no DRAFT banner, customization notes section rendered with proper markdown.
- Spot-check at least one Family 1, 2, or 4 page (e.g., `dist/recipes/concept-tutor-no-answers.html`) to confirm no regression.
- Spot-check at least one still-placeholder page (e.g., `dist/recipes/rubric-builder.html` from Family 5) to confirm placeholder Instructions and DRAFT banner still show.

## Constraints — non-negotiable

- **No new dependencies.** Markdown library and Jinja2 only.
- **No content authoring by you.** Verbatim from HANDOFF_05.
- **No changes to other recipes.** Only Family 3's three recipes get touched.
- **No schema, template, or build pipeline changes.**
- **Single commit.**

## Working approach

1. **Read HANDOFF_05 fully.**
2. **Confirm the three target recipe files exist and are currently in placeholder state.**
3. **Decide on the apply mechanism.** Write `tools/_apply_handoff_05_content.py` following the `_apply_handoff_04_content.py` pattern.
4. **Apply the content** to the three recipe JSON files. Use `json.dumps()` for safety.
5. **Rebuild** with `python build.py`.
6. **Spot-check three pages** (one Family 3 final, one Family 1/2/4 final no-regression, one still-placeholder).
7. **Run the done-criteria checklist** from HANDOFF_05.
8. **Commit and push** as a single commit per D3.

## Final report format

When done, write a report covering:

1. **What got changed.** Brief summary: which recipes, which fields.
2. **Decisions made.** Apply mechanism, JSON formatting choices, anything else.
3. **Done-criteria status.** Walk through HANDOFF_05's done criteria as a checklist with status per item.
4. **Sample output.** Paste the rendered HTML excerpt of one of the new Family 3 customization notes sections so Onur can confirm rendering. Confirm one no-regression page still renders.
5. **Conflicts encountered.** Any places where SPEC.md v0.1.2 and HANDOFF_05 disagreed (none expected).
6. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on.
7. **Verification.** Confirm `python build.py` runs clean and idempotent, and the spot-checks show expected output.

Be honest in the report.

## Begin

Read HANDOFF_05.md. Then SPEC.md if needed. Then proceed.
