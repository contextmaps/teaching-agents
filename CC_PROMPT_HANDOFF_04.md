# CC Prompt — HANDOFF_04: Family 4 Recipe Authoring

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. Three content-authoring rounds have already landed: HANDOFF_02 added real content for Family 2 (4 recipes) plus the schema and template extensions for customization notes; HANDOFF_03 added real content for Family 1 (6 recipes). 10 of 23 recipes now ship with real content. SPEC v0.1.2 is current.

This handoff (HANDOFF_04) is the third content-authoring round. It adds real content for the three Family 4 recipes (course architecture and conversion). Mechanically identical to HANDOFF_03; no schema, template, or build-pipeline changes. The note worth attention: HANDOFF_04 includes the catalog's third Heavy-tier recipe (4.1 Course Format Converter), and its Instructions text is closer to the 7,500-character upper bound than previous recipes.

## Mandatory reading order

Before changing any files, read in this order:

1. **`HANDOFF_04.md`** — full document. Your work order, including all deliverables (D1 through D3), the verbatim recipe content for three recipes, and the done criteria.
2. **`SPEC.md`** (currently v0.1.2) — for architectural context, especially §7 (Recipe Page Anatomy) and §9 (Build Pipeline and JSON schema).
3. **The three target recipe files** (`recipes/014-course-format-converter.json`, `recipes/015-syllabus-modernizer.json`, `recipes/016-module-architect.json`) to confirm their current placeholder state.
4. **`HANDOFF_03.md`** as a reference if anything in HANDOFF_04's pattern is unclear — HANDOFF_03 established the mechanical pattern that HANDOFF_04 follows directly.

If anything in HANDOFF_04 conflicts with `SPEC.md` v0.1.2, surface it in your final report. None is expected.

## Your task

Apply the changes specified in HANDOFF_04:

- For each of the three Family 4 recipes (numbers 4.1 through 4.3, files 014 through 016):
  - Replace `framing_paragraph` with the real text from HANDOFF_04.
  - Replace `fields.instructions` with the real text from HANDOFF_04 (verbatim, including all guillemet markers).
  - Add `customization_notes` field with the markdown content from HANDOFF_04.
  - Set `content_status: "final"`.
- Run `python build.py` and verify clean output.
- Verify the three Family 4 pages render correctly (real content, no DRAFT banner, customization notes section visible).
- Verify the 10 already-final recipe pages (Families 1, 2) still render correctly (no regression).
- Verify the 10 still-placeholder recipes still show DRAFT banners.
- Commit and push as a single commit with the message specified in HANDOFF_04 D3.

The done criteria in HANDOFF_04 are exhaustive — work through them as a checklist.

## Operational guidance

**Same as HANDOFF_03, with one note specific to recipe 4.1.** Recipe 4.1 (Course Format Converter) is the catalog's only remaining Heavy-tier recipe, and its Instructions text is ~6,580 characters — closer to the 7,500-character ceiling than previous recipes. All three recipes in this handoff are within budget; CC should not need to truncate. If after JSON encoding any recipe's Instructions exceeds 7,500 characters in the JSON file, surface it in the final report. The character budget includes the JSON-escaped form (which can grow slightly compared to raw text due to escape sequences).

**On the recipe content.** All Instructions text, framing paragraphs, and customization notes come from HANDOFF_04 verbatim. Do not edit, "improve," or "clean up" the prose. If something looks like a typo, flag it in the final report rather than silently changing it.

**On the guillemet markers `«...»`.** Same as previous handoffs — they are part of the Instructions content, not a templating syntax. Render verbatim.

**On JSON encoding.** Use `json.dumps()` rather than hand-escaping. The customization notes content includes markdown (bullets, sub-bullets at two-space indent, bold, inline code with backticks), guillemet characters, and apostrophes within prose.

**On rebuild verification.** The rebuild touches all 23 recipe pages. After running `python build.py`:

- Spot-check at least one Family 4 page (e.g., `dist/recipes/course-format-converter.html`) for: real Instructions visible, no DRAFT banner, customization notes section rendered with proper markdown.
- Spot-check at least one Family 1 or Family 2 page (e.g., `dist/recipes/concept-tutor-no-answers.html`) to confirm no regression.
- Spot-check at least one still-placeholder page (e.g., `dist/recipes/discussion-question-generator.html` from Family 3) to confirm placeholder Instructions and DRAFT banner still show.

## Constraints — non-negotiable

- **No new dependencies.** Markdown library and Jinja2 only.
- **No content authoring by you.** Verbatim from HANDOFF_04.
- **No changes to other recipes.** Only Family 4's three recipes get touched.
- **No schema, template, or build pipeline changes.**
- **Single commit.**

## Working approach

1. **Read HANDOFF_04 fully.**
2. **Confirm the three target recipe files exist and are currently in placeholder state.**
3. **Decide on the apply mechanism.** If you wrote `tools/_apply_handoff_03_content.py`, write `tools/_apply_handoff_04_content.py` with the same structure.
4. **Apply the content** to the three recipe JSON files. Use `json.dumps()` for safety.
5. **Rebuild** with `python build.py`.
6. **Spot-check three pages** (one Family 4 final, one Family 1 or 2 final no-regression, one still-placeholder).
7. **Run the done-criteria checklist** from HANDOFF_04.
8. **Commit and push** as a single commit per D3.

## Final report format

When done, write a report covering:

1. **What got changed.** Brief summary: which recipes, which fields.
2. **Decisions made.** Apply mechanism, JSON formatting choices, anything else.
3. **Done-criteria status.** Walk through HANDOFF_04's done criteria as a checklist with status per item.
4. **Sample output.** Paste the rendered HTML excerpt of one of the new Family 4 customization notes sections so Onur can confirm rendering. Confirm one no-regression page still renders.
5. **Conflicts encountered.** Any places where SPEC.md v0.1.2 and HANDOFF_04 disagreed (none expected).
6. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on.
7. **Verification.** Confirm `python build.py` runs clean and idempotent, and the spot-checks show expected output.

Be honest in the report.

## Begin

Read HANDOFF_04.md. Then SPEC.md if needed. Then proceed.
