# CC Prompt — HANDOFF_09: Tutorial Page Revision

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. All 23 recipes are content-complete; the build output folder was renamed from `dist/` to `docs/` in HANDOFF_08 to enable GitHub Pages deployment, and the site is live at `https://contextmaps.github.io/teaching-agents/`. SPEC v0.1.3 is current.

This handoff (HANDOFF_09) is operational: convert tutorial pages from screenshot-anchored UI walkthroughs to orientation-focused text. The rationale is documented in the handoff: maintaining screenshots for four rapidly-changing platforms is unrealistic, and the project's own walkthrough confirmed the existing tutorial text already doesn't match current UIs. The new design uses platform terminology as the durable anchor, with an "ask the platform" fallback for UI navigation.

## Mandatory reading order

1. **`HANDOFF_09.md`** — full document. Your work order, deliverables (D1 through D6), tutorial content, and done criteria.
2. **`SPEC.md`** (currently v0.1.3) — §8 Tutorial Section describes the current tutorial design; HANDOFF_09 changes that. A SPEC update to v0.1.4 will follow after this handoff lands.
3. **One existing tutorial JSON** (e.g., `tutorials/copilot.json`) — to confirm the schema field names. HANDOFF_09's content maps onto whatever the existing fields are called.
4. **`templates/tutorial.html`** — to find the screenshot block and "under review" banner that need to be removed.
5. **The `assets/tutorials/` directory structure** — to confirm placeholder PNG paths before deletion.

If anything in HANDOFF_09 conflicts with `SPEC.md` v0.1.3, surface it in your final report. Some conflict is expected — HANDOFF_09 changes the tutorial design and SPEC will be updated to match after this handoff lands.

## Your task

Apply the changes specified in HANDOFF_09:

- Update each of the five tutorial JSONs with the new framing paragraph, three step contents, mapping table content, and institutional note from HANDOFF_09's "Tutorial content" section.
- Set `tutorial_status` (or equivalent) to indicate "final / verified" so no "under review" banner renders on any tutorial page.
- Update `templates/tutorial.html` to remove the screenshot block and the "under review" banner block.
- Delete the five placeholder PNGs from `assets/tutorials/<platform>/` and from `docs/assets/tutorials/<platform>/` if they exist there too.
- If any logic in `build.py` references the deleted screenshots, remove that logic.
- Run `python build.py` and verify clean output.
- Verify the five tutorial pages render without screenshots and without the "under review" banner.
- Verify the 23 recipe pages still render correctly (no regression).
- Commit and push as a single commit per D6.

The done criteria in HANDOFF_09 are exhaustive — work through them as a checklist.

## Operational guidance

**Confirm the tutorial JSON schema before applying content.** I've assumed field names like `framing_paragraph`, `steps`, `field_mapping`, and `institutional_note`, but the existing JSONs (created in HANDOFF_01) may use different names. Open one tutorial JSON before applying to confirm the actual structure, then map HANDOFF_09's content onto the existing field names. If field names don't match cleanly, surface the mapping in your final report rather than restructuring the schema.

**On the content.** All framing paragraphs, step content, mapping tables, and institutional notes come from HANDOFF_09 verbatim. Don't edit, "improve," or rephrase. The "ask the platform" fallback phrasing in Steps 1 and 3 is calibrated — don't soften or strengthen it. If something looks like a typo, flag it in the final report rather than fixing silently.

**On the template changes.** Two blocks need to go from `templates/tutorial.html`: the screenshot block (typically a `<figure>` containing the placeholder `<img>` tag) and the "tutorial content under review" banner block. The rest of the template (page header, breadcrumb, framing paragraph rendering, numbered steps rendering, mapping table rendering, institutional note rendering) stays as-is.

If the screenshot block is rendered conditionally (e.g., `{% if screenshot_path %}`), removing the conditional and its contents is cleaner than just removing the data. Don't leave dead conditionals.

**On the PNG deletions.** Confirm paths before deleting. The placeholder PNGs may live in `assets/tutorials/<platform>/entry-point.png` (source location), `docs/assets/tutorials/<platform>/entry-point.png` (built location), or both. For NotebookLM the file is named `notebook-overview.png` per SPEC. After deletion, remove the empty `assets/tutorials/<platform>/` directories — don't leave empty husks.

**On `build.py` logic.** If `build.py` has logic that copies tutorial screenshots from `assets/` to `docs/assets/` during the build, that logic needs to go. If it doesn't, no change to `build.py` needed. Check before assuming.

**On the cumulative no-regression check.** After HANDOFF_07, zero recipe HTML pages had `class="draft-banner"`. That count should remain zero after HANDOFF_09 — HANDOFF_09 doesn't touch recipes. Confirm in your final report.

**On rebuild verification.** After running `python build.py`, spot-check:

- One of the five tutorial pages (e.g., `docs/recipes/../tutorials/copilot.html` or wherever tutorials are output) for the new content, no screenshot, no banner.
- One recipe page (e.g., `docs/recipes/concept-tutor-no-answers.html`) to confirm no regression.

## Constraints — non-negotiable

- **No new dependencies.**
- **No content authoring by you.** Verbatim from HANDOFF_09.
- **No changes to recipes, recipe schema, or recipe templates.**
- **Single commit.**

## Working approach

1. **Read HANDOFF_09 fully.**
2. **Open one existing tutorial JSON** to confirm the schema field structure. Note which fields the content maps to.
3. **Open `templates/tutorial.html`** to locate the screenshot block and "under review" banner block.
4. **Apply the content** to all five tutorial JSONs. Use `json.dumps()` for safety.
5. **Update the template** to remove the screenshot block and banner block.
6. **Delete the placeholder PNGs** (in both `assets/` and `docs/assets/` if present) and remove the empty directories.
7. **Check `build.py`** for any logic referencing the deleted screenshots; remove if found.
8. **Rebuild** with `python build.py`.
9. **Spot-check pages** (one tutorial, one recipe).
10. **Run the done-criteria checklist** from HANDOFF_09.
11. **Commit and push** as a single commit per D6.

## Final report format

1. **What got changed.** Files modified, files deleted.
2. **Decisions made.** Especially: the field mapping between HANDOFF_09's content and the existing tutorial JSON schema. Whether `build.py` needed any changes.
3. **Done-criteria status.** Walk through HANDOFF_09's done criteria as a checklist.
4. **Sample output.** Paste a rendered HTML excerpt of one of the new tutorial pages so Onur can confirm: no screenshot, no banner, three numbered steps with embedded "ask the platform" fallbacks, mapping table present, institutional note where applicable.
5. **No-regression confirmation.** Confirm one recipe page still renders correctly. Confirm zero recipe pages have `class="draft-banner"`.
6. **Conflicts encountered.** Especially any places where SPEC v0.1.3 (which describes the old screenshot-anchored tutorial design in §8) and HANDOFF_09 disagreed. This is expected; SPEC will be updated to v0.1.4 after this handoff.
7. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on.
8. **Verification.** Confirm `python build.py` runs clean and idempotent.

Be honest in the report.

## Begin

Read HANDOFF_09.md. Then open one tutorial JSON to confirm schema. Then proceed.
