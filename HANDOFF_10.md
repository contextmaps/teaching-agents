# HANDOFF_10 — Home Page Framing + About Page Copy

**Project:** Pamplin AI Agent Recipes (`teaching-agents`)
**Spec reference:** `SPEC.md` v0.1.4 (no SPEC update required; this handoff is content within the existing structure)
**Cut:** Operational — replace placeholder framing copy on the catalog home page and About page with final text.

---

## Why

The site is otherwise content-complete and live, but two pieces of placeholder copy remain visible to faculty:

1. **Home page framing paragraph** currently references the May 7 AI Teaching Workshop and includes a time estimate range that isn't useful in this position. Faculty who didn't attend the workshop are accidentally framed as outsiders; the time range mixes Light and Heavy recipes into a single span that doesn't help any specific reader.

2. **About page** currently shows a placeholder stub that references the workshop, names a contributor list and calibration process that don't fit the project's actual scope, and ends with "Final About copy is pending."

Both are replaced with final text in this handoff. The new copy is reader-facing rather than process-facing — it tells faculty what the site is and how to use it, not how it was made.

---

## Inputs

**Repo path:** `contextmaps/teaching-agents`.

**Files to modify:**

```
site_content.json    (likely; this is the canonical home for both pieces of copy)
config.json          (verify — site title was found here in HANDOFF_08 post-work; framing paragraph and About copy may also live here)
```

CC should grep both files for the current text strings before applying changes — the keys may live in either file, and the goal is to update the canonical source, not duplicate the text. If the framing paragraph and About copy are in different files than I've assumed, CC should update wherever they actually live and report the locations in the final report.

---

## Deliverables

### D1 — Update the catalog home framing paragraph

**Current text** (or close to it):

```
23 agent designs for Pamplin faculty, derived from what came up at the May 7 AI Teaching Workshop. Pick a recipe, copy the fields into your platform of choice, build the agent in 15-90 minutes.
```

**Replace with:**

```
A working collection of AI teaching agent recipes for Pamplin faculty. Each recipe is a starting point for an agent you can build in any major platform — Microsoft Copilot, ChatGPT, Claude, or Gemini. Browse by family, pick a recipe that fits, copy the fields into your platform, and you're running.
```

This text replaces the workshop-history framing with a what-this-is, what-to-do-with-it framing, and notes platform compatibility directly.

### D2 — Update the About page copy

**Current placeholder text** (or close to it):

```
The site is a follow-up to the May 7, 2026 Pamplin AI Teaching Workshop, which surfaced unprompted faculty interest in building their own agents. The 23 recipes in v1 are derived from the actual selections and free-text submissions of 98 workshop participants. Final About copy will name contributors, link the workshop platform, and describe the calibration process behind each recipe.
```

**Replace with:**

```
This is a working collection of AI teaching agent recipes for faculty at Virginia Tech's Pamplin College of Business. Each recipe is a starting point: copy the fields into your preferred AI platform, build the agent, customize the parts that need to fit your course.

Please contact Onur Seref ([seref@vt.edu](mailto:seref@vt.edu)) for questions, concerns, or suggestions.
```

Two paragraphs. The second paragraph contains a mailto link that should render as a clickable email link in the final HTML.

The page title ("About this site") stays as-is — it's likely set in the template or the About page's own metadata field, not in the body copy.

If the About copy is stored as a single string in the JSON, separate the two paragraphs with `\n\n` (the build's existing markdown rendering, or the multi-paragraph splitting pattern from HANDOFF_09_PATCH, should produce visible paragraph breaks). If the About copy is stored as an array of paragraph strings or a markdown blob, format appropriately for whichever shape the schema uses.

### D3 — Verify the email link renders correctly

The `[seref@vt.edu](mailto:seref@vt.edu)` syntax above is markdown. If the About page content is rendered as markdown (via the same `markdown` library used for recipe customization notes), this produces a clickable email link. If the About page content is rendered as plain text in the template, the markdown won't render and you'll need to use HTML directly:

```html
<a href="mailto:seref@vt.edu">seref@vt.edu</a>
```

CC should inspect the existing About page template and content rendering to determine which form is appropriate, then use that form in the JSON. In the final report, note which form was used and why.

### D4 — Rebuild and verify

After making the changes:

- `python build.py` runs clean and idempotent.
- The catalog home page (`docs/index.html`) shows the new framing paragraph at the top, with no reference to the workshop or time estimates.
- The About page (`docs/about.html`) shows the new two-paragraph copy, with the email link rendering as a clickable mailto link.
- The page title on the About page is still "About this site" (or whatever it currently is — the title isn't changing).
- All 23 recipe pages still render correctly (no regression).
- All 5 tutorial pages still render correctly (no regression).

### D5 — Commit and push

A single commit:

```
HANDOFF_10: Final framing copy for home page and About page

- Replaces home page framing paragraph (was workshop-history-framed
  with time estimate) with reader-facing what-it-is, what-to-do
  framing including platform compatibility
- Replaces About page placeholder stub with two-paragraph copy
  ending in a mailto link to Onur Seref
- No structural changes; copy lives in the existing content JSON
```

---

## Constraints

- **No content changes outside these two pieces of copy.** Recipes untouched, tutorials untouched, page titles untouched, navigation untouched.
- **No schema changes.**
- **No new dependencies.**
- **Single commit.**

---

## Done criteria

**Content:**
- [ ] Catalog home framing paragraph replaced with the new text matching this handoff verbatim.
- [ ] About page copy replaced with the two-paragraph version matching this handoff verbatim.
- [ ] Email link renders as a clickable `mailto:` link in the rendered About page.

**Build:**
- [ ] `python build.py` runs clean and idempotent.
- [ ] No errors or warnings.
- [ ] No schema validation errors.

**Visual verification:**
- [ ] Catalog home page shows new framing paragraph; no workshop reference, no time estimate.
- [ ] About page shows two paragraphs separated by visible whitespace; email link is clickable.
- [ ] All 23 recipe pages still render correctly (no regression).
- [ ] All 5 tutorial pages still render correctly (no regression).

**Hygiene:**
- [ ] Single commit with the message specified in D5.
- [ ] CC's final report includes: confirmation of done criteria, which file the framing and About copy were stored in, which form was used for the email link (markdown vs. HTML), any decisions made.

---

## Notes for CC

- **Grep before applying.** The framing paragraph and About copy may live in `site_content.json`, `config.json`, or somewhere else entirely. Find them by string-matching a unique fragment of the current placeholder text (e.g., "May 7 AI Teaching Workshop" for the framing paragraph, "Final About copy is pending" for the About page). Update wherever they actually live.
- **The page title for About stays as-is.** The body copy changes; the title doesn't.
- **The framing paragraph location** is likely a `tagline` or `framing` or `hero_description` field on the site or catalog object. The wording of the JSON key may not match my guess.
- **On the email link rendering.** If the About content already renders as markdown (likely, since recipe customization notes use markdown and the same library is available), use the markdown form. If not, use the HTML form. Either is fine; the goal is a clickable link in the rendered HTML.
- **No content authoring by you.** All text comes verbatim from this handoff.
- **Spot-check the home and About pages in the rendered HTML** to confirm the changes landed and the email link works.
