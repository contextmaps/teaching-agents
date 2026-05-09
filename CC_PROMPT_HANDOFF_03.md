# CC Prompt — HANDOFF_03: Family 1 Recipe Authoring

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. The platform skeleton was built in HANDOFF_01 (with HANDOFF_01_PATCH for path bugs). The first content-authoring round (HANDOFF_02) added real Instructions, framing paragraphs, and customization notes for the four Family 2 recipes, plus a small schema/template extension to support per-recipe customization notes and a controllable DRAFT banner. SPEC v0.1.2 captures the current state.

This handoff (HANDOFF_03) is the second content-authoring round. It adds real content for the six Family 1 recipes (in-class activity engines). Mechanically nearly identical to HANDOFF_02; no schema, template, or build-pipeline changes.

## Mandatory reading order

Before changing any files, read in this order:

1. **`HANDOFF_03.md`** — full document. This is your work order, including all deliverables (D1 through D3), the verbatim recipe content for six recipes, and the done criteria.
2. **`SPEC.md`** (currently v0.1.2) — for architectural context, especially §7 (Recipe Page Anatomy, including the new authoring conventions) and §9 (Build Pipeline and JSON schema).
3. **The six target recipe files** (`recipes/001-stakeholder-roleplay-partner.json` through `recipes/006-think-pair-share-question-engine.json`) to confirm their current placeholder state.
4. **`HANDOFF_02.md`** as a reference if anything in HANDOFF_03's pattern is unclear — HANDOFF_02 established the same structure and HANDOFF_03 follows it directly.

If anything in HANDOFF_03 conflicts with `SPEC.md` v0.1.2, surface it in your final report. None is expected — the SPEC was updated specifically to match HANDOFF_02's additions, and HANDOFF_03 uses the same patterns.

## Your task

Apply the changes specified in HANDOFF_03:

- For each of the six Family 1 recipes (007 → 001 by file number; recipe numbers 1.1 through 1.6):
  - Replace `framing_paragraph` with the real text from HANDOFF_03.
  - Replace `fields.instructions` with the real text from HANDOFF_03 (verbatim, including all guillemet markers).
  - Add `customization_notes` field with the markdown content from HANDOFF_03.
  - Set `content_status: "final"`.
- Run `python build.py` and verify clean output.
- Verify the six Family 1 pages render correctly (real content, no DRAFT banner, customization notes section visible).
- Verify the four Family 2 pages still render correctly (no regression).
- Verify the 13 still-placeholder recipes still show DRAFT banners.
- Commit and push as a single commit with the message specified in HANDOFF_03 D3.

The done criteria in HANDOFF_03 are exhaustive — work through them as a checklist.

## Operational guidance

**Same as HANDOFF_02, with one note.** This handoff is mechanically identical to HANDOFF_02 — same kinds of fields, same conventions, same constraints. The only difference is which six recipes you're updating instead of which four. If you wrote a one-shot apply script for HANDOFF_02 (e.g., `tools/_apply_handoff_02_content.py`), the same structure works for HANDOFF_03 — write `tools/_apply_handoff_03_content.py` with the same pattern and adjust the recipe IDs and content blocks.

**On the recipe content.** All Instructions text, framing paragraphs, and customization notes come from HANDOFF_03 verbatim. Do not edit, "improve," or "clean up" the prose. If something looks like a typo, flag it in your final report rather than silently changing it. The content was authored deliberately.

**On the guillemet markers `«...»`.** Same as HANDOFF_02 — they are part of the Instructions content, not a templating syntax. Render them verbatim. Faculty see them on the page; the agent reads them as punctuation.

**On JSON encoding.** The customization notes content includes markdown formatting (bullets, sub-bullets at two-space indent, bold, inline code with backticks), guillemet characters, and apostrophes within prose. Use `json.dumps()` rather than hand-escaping. Verify the resulting JSON parses correctly before declaring done.

**On the 7,500-character upper bound.** Each Instructions field in HANDOFF_03 is already drafted within budget (range: 5,244 to 5,785 characters; all have 1,700+ characters of headroom). You should not need to truncate or edit. If you find any Instructions field exceeds 7,500 characters when you put it into the JSON, surface it in your final report — that would indicate either a copy-paste error or an unexpected JSON encoding issue.

**On rebuild verification.** The rebuild touches all 23 recipe pages (idempotent). After running `python build.py`:
- Spot-check at least one Family 1 page (e.g., `dist/recipes/stakeholder-roleplay-partner.html`) for: real Instructions visible, no DRAFT banner, customization notes section rendered with proper markdown.
- Spot-check at least one Family 2 page (e.g., `dist/recipes/concept-tutor-no-answers.html`) to confirm no regression — the existing real content should still render correctly.
- Spot-check at least one still-placeholder page (e.g., `dist/recipes/syllabus-modernizer.html` from Family 4) to confirm placeholder Instructions and DRAFT banner still show.

## Constraints — non-negotiable

- **No new dependencies.** Markdown library and Jinja2 are the only build dependencies; both already installed. Don't add anything else.
- **No content authoring by you.** All content comes verbatim from HANDOFF_03.
- **No changes to other recipes.** Only the six Family 1 recipes get touched. Don't modify Family 2's content (already real) or the 13 still-placeholder recipes.
- **No schema, template, or build pipeline changes.** Everything was set up in HANDOFF_02. This handoff is purely content.
- **Single commit.** Don't split into multiple commits — six recipe updates are a coherent batch.

## Working approach

1. **Read HANDOFF_03 fully.** Note the six verbatim content blocks.
2. **Confirm the six target recipe files exist and are currently in placeholder state.**
3. **Decide on the apply mechanism.** A one-shot Python script following the HANDOFF_02 pattern is cleanest; manual edits work but are more error-prone with six recipes.
4. **Apply the content** to the six recipe JSON files. Use `json.dumps()` for safety.
5. **Rebuild** with `python build.py`.
6. **Spot-check three pages** as above (one Family 1 final, one Family 2 final, one Family 4+ draft).
7. **Run the done-criteria checklist** from HANDOFF_03.
8. **Commit and push** as a single commit per D3.

## Final report format

When done, write a report covering:

1. **What got changed.** Brief summary: which recipes, which fields.
2. **Decisions made.** Especially: whether you wrote an apply script or edited manually, and any decisions about JSON formatting.
3. **Done-criteria status.** Walk through HANDOFF_03's done criteria as a checklist with status per item.
4. **Sample output.** Paste the rendered HTML excerpt of one of the new Family 1 customization notes sections so Onur can confirm markdown rendering still works correctly. Also confirm one Family 2 page still renders (no regression).
5. **Conflicts encountered.** Any places where SPEC.md v0.1.2 and HANDOFF_03 disagreed (none expected).
6. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on, anything future handoffs should be aware of.
7. **Verification.** Confirm `python build.py` runs clean, idempotent, and the spot-checks above show the expected output.

Be honest in the report. If something in HANDOFF_03 was unclear, say so; if you took a shortcut, surface it.

## Begin

Read HANDOFF_03.md. Then SPEC.md if you need architectural context. Then proceed.
