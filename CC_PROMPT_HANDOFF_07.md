# CC Prompt — HANDOFF_07: Family 6 + Family 7 Recipe Authoring (Final Content Handoff)

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. Six content-authoring rounds have already landed: HANDOFF_02 (Family 2, 4 recipes + schema/template extensions), HANDOFF_03 (Family 1, 6 recipes), HANDOFF_04 (Family 4, 3 recipes), HANDOFF_05 (Family 3, 3 recipes), HANDOFF_06 (Family 5, 3 recipes). 19 of 23 recipes ship with real content. SPEC v0.1.2 is current.

This handoff (HANDOFF_07) is the **final content-authoring round**. It adds real content for the four remaining placeholder recipes — three from Family 6 (Examples, cases, content) and one from Family 7 (AI-policy). Mechanically identical to previous content handoffs; no schema, template, or build-pipeline changes.

After this handoff lands, **all 23 of 23 recipes ship with real content**. Zero placeholders remain. The DRAFT banner does not appear anywhere in the site.

## Mandatory reading order

Before changing any files, read in this order:

1. **`HANDOFF_07.md`** — full document. Your work order, including all deliverables (D1 through D3), the verbatim recipe content for four recipes, and the done criteria.
2. **`SPEC.md`** (currently v0.1.2) — for architectural context if needed.
3. **The four target recipe files** (`recipes/020-discipline-specific-example-generator.json`, `recipes/021-current-events-case-freshener.json`, `recipes/022-concept-explainer-multiple-framings.json`, `recipes/023-course-ai-policy-drafter.json`) to confirm their current placeholder state.
4. **`HANDOFF_06.md`** as a reference if anything in HANDOFF_07's pattern is unclear — HANDOFF_06 used the same mechanical pattern.

If anything in HANDOFF_07 conflicts with `SPEC.md` v0.1.2, surface it in your final report. None is expected.

## Your task

Apply the changes specified in HANDOFF_07:

- For each of the four recipes (numbers 6.1, 6.2, 6.3, 7.1, files 020 through 023):
  - Replace `framing_paragraph` with the real text from HANDOFF_07.
  - Replace `fields.instructions` with the real text from HANDOFF_07 (verbatim, including all guillemet markers).
  - Add `customization_notes` field with the markdown content from HANDOFF_07.
  - Set `content_status: "final"`.
- Run `python build.py` and verify clean output.
- Verify the four newly-final recipe pages render correctly (real content, no DRAFT banner, customization notes section visible).
- Verify the 19 already-final recipe pages still render correctly (no regression).
- **Verify zero files retain the draft-banner after rebuild.** This is the cumulative completion check — every recipe in the catalog now ships with real content.
- Commit and push as a single commit with the message specified in HANDOFF_07 D3.

The done criteria in HANDOFF_07 are exhaustive — work through them as a checklist.

## Operational guidance

**Same as HANDOFF_06.** This handoff is mechanically identical to HANDOFF_06. Four recipes (one more than HANDOFF_06's three). Write `tools/_apply_handoff_07_content.py` following the `_apply_handoff_06_content.py` pattern.

**On the recipe content.** All Instructions text, framing paragraphs, and customization notes come from HANDOFF_07 verbatim. Do not edit, "improve," or "clean up" the prose. If something looks like a typo, flag it in the final report rather than silently changing it.

**On the guillemet markers `«...»`.** Same as previous handoffs. Render verbatim. Recipe 7.1 has 32 guillemet pairs (the most of any recipe in the catalog — pronouns appear repeatedly throughout the AI-policy drafter's instructions); preserve them all.

**On JSON encoding.** Use `json.dumps()` with `ensure_ascii=False` to preserve guillemets as UTF-8.

**On character counts.** All four Instructions fields in HANDOFF_07 are within budget (range: 5,042 to 6,518 characters). Recipe 6.3 (the Level 3 cross-disciplinary recipe) has the tightest headroom at 982 characters but is well under 7,500. No truncation needed. If any recipe exceeds 7,500 characters in the JSON file, surface it in the final report.

**On the cumulative completion check.** After HANDOFF_07 lands, **zero files** should retain the draft-banner. The previous handoffs established the pattern of reporting how many files retain the banner; HANDOFF_07's report should explicitly confirm zero. If the count is non-zero, something has gone wrong — investigate before declaring done.

**On rebuild verification.** The rebuild touches all 23 recipe pages. Spot-check at least one of the four newly-final pages (e.g., `dist/recipes/concept-explainer-multiple-framings.html`), and one already-final page from earlier handoffs (e.g., `dist/recipes/concept-tutor-no-answers.html`) to confirm no regression.

## Constraints — non-negotiable

- **No new dependencies.** Markdown library and Jinja2 only.
- **No content authoring by you.** Verbatim from HANDOFF_07.
- **No changes to other recipes.** Only the four target recipes get touched.
- **No schema, template, or build pipeline changes.**
- **Single commit.**

## Working approach

1. **Read HANDOFF_07 fully.**
2. **Confirm the four target recipe files exist and are currently in placeholder state.**
3. **Decide on the apply mechanism.** Write `tools/_apply_handoff_07_content.py` following the `_apply_handoff_06_content.py` pattern.
4. **Apply the content** to the four recipe JSON files. Use `json.dumps()` for safety.
5. **Rebuild** with `python build.py`.
6. **Spot-check pages** (one newly-final, one already-final no-regression).
7. **Verify the cumulative completion check** — exactly zero files retain the draft-banner.
8. **Run the done-criteria checklist** from HANDOFF_07.
9. **Commit and push** as a single commit per D3.

## Final report format

When done, write a report covering:

1. **What got changed.** Brief summary: which recipes, which fields.
2. **Decisions made.** Apply mechanism, JSON formatting choices, anything else.
3. **Done-criteria status.** Walk through HANDOFF_07's done criteria as a checklist with status per item.
4. **Sample output.** Paste the rendered HTML excerpt of one of the new customization notes sections so Onur can confirm rendering. Confirm one no-regression page still renders.
5. **Cumulative completion check.** Explicitly confirm zero files retain the draft-banner. If non-zero, name the files and investigate.
6. **Conflicts encountered.** Any places where SPEC.md v0.1.2 and HANDOFF_07 disagreed (none expected).
7. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on.
8. **Verification.** Confirm `python build.py` runs clean and idempotent, the spot-checks show expected output, and zero files retain the draft-banner.

Be honest in the report.

This is the final content handoff. After it lands, the recipe catalog is structurally and substantively complete from a content perspective.

## Begin

Read HANDOFF_07.md. Then SPEC.md if needed. Then proceed.
