# CC Prompt — HANDOFF_10: Home Page and About Page Copy

You are picking up the static-site project for Pamplin College of Business at Virginia Tech. The recipe catalog (23 recipes) and tutorial pages (5 tutorials) are content-complete; the site is live at `https://contextmaps.github.io/teaching-agents/`. SPEC v0.1.4 is current.

This handoff (HANDOFF_10) replaces two pieces of placeholder copy with final text: the catalog home page's framing paragraph (currently references the May 7 AI Teaching Workshop), and the About page (currently shows a placeholder stub). No structural changes — copy replacement only.

This is one of the smallest handoffs in the project.

## Mandatory reading order

1. **`HANDOFF_10.md`** — full document. Your work order, deliverables (D1 through D5), the verbatim new copy, and done criteria.
2. **`site_content.json` and `config.json`** — to locate the current framing paragraph and About copy. Grep for unique fragments ("May 7 AI Teaching Workshop" or "Final About copy is pending") to find the canonical source.

## Your task

Apply the changes specified in HANDOFF_10:

- Replace the catalog home page's framing paragraph with the new text from HANDOFF_10 D1.
- Replace the About page's copy with the two-paragraph version from HANDOFF_10 D2, including the mailto email link.
- Run `python build.py`.
- Verify the home page and About page render correctly with the new content.
- Verify the email link is clickable in the rendered HTML.
- Commit and push as a single commit per D5.

## Operational guidance

**Grep before editing.** I've assumed the framing paragraph and About copy live in `site_content.json`, but the actual canonical location may differ — site title was found in `config.json` previously. Run `grep -l "May 7 AI Teaching Workshop" .` and `grep -l "Final About copy is pending" .` (or use ripgrep) to find the actual files. Update the canonical source, not duplicates.

**On the email link.** The handoff provides two possible forms:
- Markdown: `[seref@vt.edu](mailto:seref@vt.edu)` — works if About content is rendered through the markdown library (likely, since recipe customization notes use it).
- HTML: `<a href="mailto:seref@vt.edu">seref@vt.edu</a>` — works if About content is rendered as raw HTML or plain text.

Inspect the existing About page template (`templates/about.html` or wherever About renders) and the build pipeline to determine which form is appropriate. Pick the form that produces a clickable link in the rendered HTML. Note which form was used in your final report.

**On the verbatim copy.** All new text comes from HANDOFF_10 verbatim. Don't edit, "improve," or rephrase. If something looks like a typo, flag it in the final report rather than fixing silently.

**On the no-regression check.** This handoff doesn't touch recipes or tutorials. The 23 recipe pages and 5 tutorial pages should render identically before and after. Confirm in the final report.

## Constraints — non-negotiable

- **No new dependencies.**
- **No content changes outside the framing paragraph and About copy.**
- **No schema changes.**
- **Single commit.**

## Working approach

1. **Read HANDOFF_10 fully.**
2. **Grep for the current text** to find which file holds the framing paragraph and About copy.
3. **Inspect the About page template/rendering** to determine markdown-vs-HTML for the email link.
4. **Apply the two text replacements.**
5. **Rebuild** with `python build.py`.
6. **Spot-check** the rendered home page and About page, confirming the new copy and the clickable email link.
7. **Confirm no-regression** on one recipe page and one tutorial page.
8. **Commit and push** per D5.

## Final report format

1. **What got changed.** Which files modified, what fields/keys updated.
2. **Decisions made.** Especially: which file held the framing paragraph and About copy, which form (markdown vs. HTML) was used for the email link, and why.
3. **Done-criteria status.** Walk through the criteria as a checklist.
4. **Sample output.** Paste the rendered HTML for the home page framing paragraph and the About page two-paragraph block (showing the email link as `<a href="mailto:...">`).
5. **No-regression confirmation.** Confirm one recipe page and one tutorial page still render correctly.
6. **Conflicts encountered.** None expected.
7. **Known issues.** Anything you'd flag.
8. **Verification.** Confirm `python build.py` runs clean.

Be honest in the report.

## Begin

Read HANDOFF_10.md. Grep for the current placeholder text. Then proceed.
