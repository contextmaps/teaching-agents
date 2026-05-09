# CC Prompt — HANDOFF_02: Family 2 Recipe Authoring

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. The platform skeleton was built in HANDOFF_01 and patched (HANDOFF_01_PATCH) to fix asset and navigation paths. This handoff adds the first real recipe content for four of the 23 recipes — the Family 2 student-facing always-on agents — plus a small schema and template extension to support per-recipe customization notes and a controllable DRAFT banner.

## Mandatory reading order

Before changing any files, read in this order:

1. **`HANDOFF_02.md`** — full document. This is your work order, including all deliverables (D1 through D5), the verbatim recipe content, and the done criteria.
2. **`SPEC.md`** (currently v0.1.1) — for architectural context. Specifically: §6 (catalog structure), §7 (recipe page anatomy), §9 (build pipeline and JSON schema), and §11 (analytics events).
3. **`recipes/007-course-faq-answerer.json`**, `recipes/008-concept-tutor-no-answers.json`, `recipes/009-adaptive-concept-practice-partner.json`, `recipes/010-reusable-course-assistant.json` — the current placeholder content. You'll be replacing key fields in each.
4. **`templates/recipe.html`** — the template you'll be extending.
5. **`build.py`** — the schema validator you'll be extending.

If anything in HANDOFF_02 conflicts with `SPEC.md`, surface the conflict in your final report. SPEC v0.1.1 does not yet reflect the schema additions in this handoff (`content_status` and `customization_notes`); that's deliberate and gets resolved in SPEC v0.1.2 after this handoff lands. So discovering "HANDOFF_02 introduces fields not in SPEC" is expected and not a real conflict.

## Your task

Apply the changes specified in HANDOFF_02:

- Replace `framing_paragraph`, `fields.instructions` content for the four Family 2 recipes; add `customization_notes` and `content_status: "final"` fields.
- Extend the JSON schema and `build.py` validation to support the two new optional fields.
- Update `templates/recipe.html` to (a) suppress the DRAFT banner when `content_status == "final"` and (b) render a "Customization notes" section below the Instructions card, parsing the field as markdown.
- Pick a markdown rendering approach (Python library or Jinja2 filter — your call; document the choice).
- Rebuild `dist/`, verify the four Family 2 recipes show real content with no DRAFT banner and customization notes section, verify the other 19 still show the DRAFT banner and placeholder Instructions.
- Commit and push as a single commit with the message specified in HANDOFF_02 D5.

The done criteria in HANDOFF_02 are exhaustive — work through them as a checklist.

## Operational guidance

**On the recipe content.** All Instructions text, framing paragraphs, and customization notes come from HANDOFF_02 verbatim. Do not edit, "improve," or "clean up" the prose. If something looks like a typo to you, flag it in your final report rather than silently changing it. The content was written deliberately; opinionated phrasing is intentional.

**On the guillemet markers `«...»`.** These are part of the Instructions content, not a templating syntax. They render to faculty as visible characters on the page; the agent reads them as punctuation. Preserve them verbatim in the JSON. Do not strip, escape, or replace them.

**On JSON encoding.** The customization notes content includes markdown formatting (bullets, bold, inline code with backticks), guillemets (UTF-8 multi-byte characters), and apostrophes inside prose. Use `json.dumps()` or your language's equivalent rather than hand-escaping. Verify the resulting JSON parses correctly before declaring done.

**On the markdown library choice.** Either `markdown` or `mistune` is fine. `markdown` is more standard in the Python ecosystem; `mistune` is faster. Either should be added to `requirements.txt` with a pinned version. If you'd rather implement a small subset of markdown rendering directly in templates without a library (e.g., handling only bullets, bold, and code spans), that's also acceptable — just document the choice in your final report. Note that the customization notes content uses bullet lists, bold (`**...**`), and inline code (`` `...` ``); whatever approach you pick must handle those three correctly.

**On the customization notes section's visual treatment.** HANDOFF_02 specifies that the section should be visually distinct from the Instructions card — lighter background, smaller heading, no copy button. Use the existing design system tokens (`--c-meta-bg`, `--c-muted`, etc.) rather than introducing new ones. The section is documentation, not content to paste, so it should read as a different kind of element on the page.

**On the DRAFT banner conditional.** The current implementation likely has the banner hardcoded into `templates/recipe.html` or the `content-final` body class. Replace this with a per-recipe check: `{% if content_status != "final" %}` (or your preferred Jinja2 conditional pattern). Recipes without an explicit `content_status` should default to "draft" behavior — the banner shows.

**On schema validation.** Both new fields are optional. Missing fields should not cause errors. Present-but-invalid `content_status` values (anything other than `"draft"` or `"final"`) should cause a clear build error naming the file and the bad value. `customization_notes` is freeform markdown; no validation beyond "must be a string if present."

**On the other 19 recipes.** They should NOT have their content changed. They will continue to show placeholder Instructions and the DRAFT banner. If your implementation requires the new fields to be explicitly present on every recipe (rather than treating absence as default), add `"content_status": "draft"` to all 19 — but do not add `customization_notes` to any of them, since they don't have real content yet.

**On the build.** After the changes, `python build.py` should still complete in a few seconds. If markdown rendering significantly slows the build, that's worth noting in your report. The build must remain idempotent.

## Constraints — non-negotiable

- **No new dependencies beyond a markdown library.** If you add `markdown` or `mistune`, that's the only addition allowed. No new templating engine, no new framework, no test runner.
- **No content authoring by you.** All Instructions, framing paragraphs, and customization notes come verbatim from HANDOFF_02.
- **No changes to the other 19 recipes' content.** Only the four Family 2 recipes get real content in this handoff.
- **Single commit.** Don't split into multiple commits — schema, template, and content are a coherent batch.
- **JS is unchanged.** This handoff doesn't touch `assets/js/site.js`. The clipboard and analytics behavior from HANDOFF_01 remains as-is.

## Working approach

1. **Read HANDOFF_02 fully.** Note the verbatim content blocks. Note the schema and template changes. Note the done criteria.
2. **Check the current state of the four target recipe files.** Confirm they currently have placeholder content. Confirm the existing schema fields you're not touching.
3. **Pick the markdown approach.** Library or hand-rolled Jinja2 filter. Document the choice for the final report.
4. **Update the schema validator in `build.py` first.** Add the two new optional fields. Verify the build still passes with the existing recipes (which don't have the new fields).
5. **Update `templates/recipe.html` next.** Add the conditional DRAFT banner. Add the customization notes section. Verify the build still produces correct output for the existing placeholder-content recipes (they shouldn't visibly change yet, since none have `content_status == "final"`).
6. **Then update the four recipe JSON files.** Replace `framing_paragraph` and `fields.instructions`; add `customization_notes` and `content_status: "final"`. Use `json.dumps()` for safety.
7. **Rebuild and inspect output.** Spot-check `dist/recipes/<slug>.html` for one of the four Family 2 recipes to confirm: real Instructions, no DRAFT banner, customization notes section with rendered markdown.
8. **Spot-check a non-Family-2 recipe** (e.g., `dist/recipes/stakeholder-roleplay-partner.html`) to confirm it still shows placeholder Instructions and the DRAFT banner.
9. **Run the done-criteria checklist** from HANDOFF_02 as a final sweep.
10. **Commit and push.** Single commit, message per D5.

## Final report format

When done, write a report covering:

1. **What got changed.** Brief summary: which files, what nature of change.
2. **Decisions made.** Especially: which markdown library or rendering approach you picked, and why.
3. **Done-criteria status.** Walk through HANDOFF_02's done criteria as a checklist with status per item.
4. **Sample output.** Paste the rendered HTML excerpt of one of the new "Customization notes" sections so Onur can confirm markdown is rendering correctly. Also paste the `<link>` and `<script>` lines from one of the four updated recipe pages to confirm the path-fix from HANDOFF_01_PATCH still holds.
5. **Conflicts encountered.** Any places where SPEC.md and HANDOFF_02 disagreed (the schema fields not being in SPEC v0.1.1 is expected; flag anything else).
6. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on, anything future handoffs should be aware of.
7. **Verification.** Confirm `python build.py` runs clean, dist is updated, and the spot-checks above show the expected output.

Be honest in the report. If something in HANDOFF_02 was unclear, say so; if you took a shortcut, surface it.

## Begin

Read HANDOFF_02.md. Then SPEC.md if you need architectural context. Then proceed.
