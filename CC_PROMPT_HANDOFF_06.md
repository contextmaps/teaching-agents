# CC Prompt — HANDOFF_06: Family 5 Recipe Authoring

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. Five content-authoring rounds have already landed: HANDOFF_02 (Family 2, 4 recipes + schema/template extensions), HANDOFF_03 (Family 1, 6 recipes), HANDOFF_04 (Family 4, 3 recipes), HANDOFF_05 (Family 3, 3 recipes). 16 of 23 recipes ship with real content. SPEC v0.1.2 is current.

This handoff (HANDOFF_06) is the fifth content-authoring round. It adds real content for the three Family 5 recipes (assessment and feedback). Mechanically identical to HANDOFF_05; no schema, template, or build-pipeline changes.

## Mandatory reading order

Before changing any files, read in this order:

1. **`HANDOFF_06.md`** — full document. Your work order, including all deliverables (D1 through D3), the verbatim recipe content for three recipes, and the done criteria.
2. **`SPEC.md`** (currently v0.1.2) — for architectural context if needed.
3. **The three target recipe files** (`recipes/017-rubric-builder.json`, `recipes/018-formative-check-generator.json`, `recipes/019-feedback-tone-matcher.json`) to confirm their current placeholder state.
4. **`HANDOFF_05.md`** as a reference if anything in HANDOFF_06's pattern is unclear — HANDOFF_05 used the same mechanical pattern.

If anything in HANDOFF_06 conflicts with `SPEC.md` v0.1.2, surface it in your final report. None is expected.

## Your task

Apply the changes specified in HANDOFF_06:

- For each of the three Family 5 recipes (numbers 5.1 through 5.3, files 017 through 019):
  - Replace `framing_paragraph` with the real text from HANDOFF_06.
  - Replace `fields.instructions` with the real text from HANDOFF_06 (verbatim, including all guillemet markers).
  - Add `customization_notes` field with the markdown content from HANDOFF_06.
  - Set `content_status: "final"`.
- Run `python build.py` and verify clean output.
- Verify the three Family 5 pages render correctly (real content, no DRAFT banner, customization notes section visible).
- Verify the 16 already-final recipe pages (Families 1, 2, 3, 4) still render correctly (no regression).
- Verify the 4 still-placeholder recipes (Families 6, 7) still show DRAFT banners — this is the "exactly 4 files retain draft-banner" check from HANDOFF_06's done criteria.
- Commit and push as a single commit with the message specified in HANDOFF_06 D3.

The done criteria in HANDOFF_06 are exhaustive — work through them as a checklist.

## Operational guidance

**Same as HANDOFF_05.** This handoff is mechanically identical to HANDOFF_05. Three recipes, same scope. Write `tools/_apply_handoff_06_content.py` following the `_apply_handoff_05_content.py` pattern.

**On the recipe content.** All Instructions text, framing paragraphs, and customization notes come from HANDOFF_06 verbatim. Do not edit, "improve," or "clean up" the prose. If something looks like a typo, flag it in the final report rather than silently changing it.

**On the guillemet markers `«...»`.** Same as previous handoffs. Render verbatim.

**On JSON encoding.** Use `json.dumps()` with `ensure_ascii=False` to preserve guillemets as UTF-8.

**On character counts.** All three Instructions fields in HANDOFF_06 are well within budget (range: 5,280 to 5,390 characters; over 2,100 characters of headroom each). Family 5 recipes are shorter than recent recipes because their behaviors are simpler (interview-then-generate, one-shot generation, voice-matching refinement). No truncation needed. If any recipe exceeds 7,500 characters in the JSON file, surface it in the final report.

**On the cumulative check.** HANDOFF_05's report introduced the "exactly 7 files retain the draft-banner" check as a positive verification. After HANDOFF_06 lands, exactly 4 files should retain the draft-banner (the four Family 6 + Family 7 placeholders). Include this check in your final report.

**On rebuild verification.** The rebuild touches all 23 recipe pages. Spot-check at least one Family 5 page (e.g., `dist/recipes/feedback-tone-matcher.html`), one already-final page (e.g., `dist/recipes/concept-tutor-no-answers.html`), and one still-placeholder page (e.g., `dist/recipes/discipline-specific-example-generator.html` from Family 6).

## Constraints — non-negotiable

- **No new dependencies.** Markdown library and Jinja2 only.
- **No content authoring by you.** Verbatim from HANDOFF_06.
- **No changes to other recipes.** Only Family 5's three recipes get touched.
- **No schema, template, or build pipeline changes.**
- **Single commit.**

## Working approach

1. **Read HANDOFF_06 fully.**
2. **Confirm the three target recipe files exist and are currently in placeholder state.**
3. **Decide on the apply mechanism.** Write `tools/_apply_handoff_06_content.py` following the `_apply_handoff_05_content.py` pattern.
4. **Apply the content** to the three recipe JSON files. Use `json.dumps()` for safety.
5. **Rebuild** with `python build.py`.
6. **Spot-check three pages** (one Family 5 final, one already-final no-regression, one still-placeholder).
7. **Verify the cumulative count** — exactly 4 files retain the draft-banner.
8. **Run the done-criteria checklist** from HANDOFF_06.
9. **Commit and push** as a single commit per D3.

## Final report format

When done, write a report covering:

1. **What got changed.** Brief summary: which recipes, which fields.
2. **Decisions made.** Apply mechanism, JSON formatting choices, anything else.
3. **Done-criteria status.** Walk through HANDOFF_06's done criteria as a checklist with status per item.
4. **Sample output.** Paste the rendered HTML excerpt of one of the new Family 5 customization notes sections so Onur can confirm rendering. Confirm one no-regression page still renders.
5. **Conflicts encountered.** Any places where SPEC.md v0.1.2 and HANDOFF_06 disagreed (none expected).
6. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on.
7. **Verification.** Confirm `python build.py` runs clean and idempotent, the spot-checks show expected output, and exactly 4 files retain the draft-banner.

Be honest in the report.

## Begin

Read HANDOFF_06.md. Then SPEC.md if needed. Then proceed.
