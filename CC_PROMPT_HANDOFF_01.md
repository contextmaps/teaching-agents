# CC Prompt — HANDOFF_01: Platform Skeleton

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. This is the foundational build that establishes the architecture; real recipe content authoring comes in later handoffs.

## Setup

This repo is fresh. The only files that exist are:

- `SPEC.md` — architectural source of truth
- `HANDOFF_01.md` — your work order
- `CONTEXT_TRANSFER.md` — initial briefing from the predecessor project (reference; the SPEC supersedes anything here that conflicts)
- `AGENT_DEFINITION.md` — context on a different agent built for the predecessor workshop project (informational; not relevant to this build)

## Mandatory reading order

Before writing any code, read in this order:

1. **`SPEC.md`** — full document. This is the architectural source of truth.
2. **`HANDOFF_01.md`** — full document. This is your work order, including all deliverables (D1.1 through D6.2) and done criteria.
3. **`CONTEXT_TRANSFER.md`** — skim only for the design-system inheritance context (the workshop platform's `plib-*` conventions, copy-button patterns, accessibility primitives). Most of CONTEXT_TRANSFER is now superseded by SPEC.md; read it for design-DNA context, not for current state.

If anything in HANDOFF_01 conflicts with SPEC.md, **SPEC.md wins**. Surface the conflict in your final report; do not silently resolve.

## Your task

Produce the complete platform skeleton specified in HANDOFF_01:

- The build pipeline (`build.py`, `requirements.txt`, `.gitignore`)
- Configuration (`config.json` with placeholder form values, `site_content.json`)
- All 23 recipe JSON files in `recipes/` (placeholder Instructions, real metadata from SPEC §6)
- All 5 tutorial JSON files in `tutorials/` (placeholder content, marked as such)
- All 6 Jinja2 templates in `templates/`
- Single CSS stylesheet at `assets/css/styles.css` (or embedded in `base.html` — your call per HANDOFF_01)
- Single JS file at `assets/js/site.js` for clipboard + analytics
- 5 placeholder PNG files for tutorial anchor screenshots
- `dist/` populated by running `python3 build.py`
- Three documentation files: `README.md`, `JIM_INTEGRATION_NOTES.md`, `FORM_SETUP_GUIDE.md`

The done criteria in HANDOFF_01 are exhaustive — work through them as a checklist.

## Operational guidance

**On reading the workshop platform's design system.** CONTEXT_TRANSFER references the workshop platform's `index.html` as the source of `plib-*` CSS conventions. That file isn't in this repo. Work from the design tokens and patterns described in SPEC §5 and the inline CSS examples in HANDOFF_01 D2.1. If you need a `plib-*` pattern that isn't documented, write a clean implementation matching the SPEC's overall aesthetic (system fonts, 8px radius, generous whitespace, focus-visible outlines, accessible color contrast on the maroon primary). Don't fabricate references to specific workshop-platform code.

**On the 23 recipe JSON files.** Per HANDOFF_01's "Notes for CC" section, you may write a one-off generator script that produces the 23 JSON skeletons from the SPEC §6 catalog table. Run it once, verify the output, then either delete the generator or leave it in a `tools/` directory clearly marked as scaffold-only. Don't ship it as part of the build pipeline. The recipe metadata (title, number, family_id, tier, level, description, recommended_platforms block) is real and final — extract it verbatim from SPEC §6. The framing_paragraph and Instructions field are placeholder.

**On placeholder content.** The DRAFT banner on recipe pages and the "Tutorial content under review" banner on tutorial pages are intentional honesty signals. Do not try to soften, hide, or condition them away. They disappear in v0.2 once real content lands, via a single CSS class flip. Make sure the class flip is genuinely a single change — don't scatter conditional logic across templates.

**On placeholder PNG files for tutorial screenshots.** A simple gray rectangle (800×500) with the platform name centered is fine. You can generate these with PIL/Pillow as part of a one-off setup script, or write a single SVG-to-PNG converter. Either works. The point is just to have valid image files at the paths the templates reference, so pages render without broken images.

**On the build script.** `build.py` should be readable. Use Jinja2's `FileSystemLoader`, render each template with appropriate context, write outputs to `dist/`. Schema validation can be a simple dict-comparison against required keys, with clear error messages naming the file and missing field. Don't reach for `pydantic` or other validation frameworks — single dependency is Jinja2 only.

**On clipboard handling in `assets/js/site.js`.** Use `navigator.clipboard.writeText()` with a fallback to a hidden textarea + `document.execCommand('copy')` for older browsers. The success-state pattern (button text changes for 2 seconds, then reverts) is described in HANDOFF_01 D2.2. Implement an `aria-live="polite"` announcement region so screen readers announce "Copied" on successful copy, matching the accessibility approach SPEC §5 inherits from the workshop platform.

**On analytics.** All POSTs to the Google Form use `mode: 'no-cors'` and silently swallow errors. Console.log on failure is fine; don't surface analytics failures to the user. With the placeholder form URL, every analytics call will fail — that's expected during the skeleton phase, and the site must keep working through those failures.

**On the always-expanded family sections.** No collapsible behavior in v1. The catalog renders all 23 recipe cards under their 7 family headers, all visible, no JavaScript required for browse. This is per the design decision documented in HANDOFF_01.

**On responsive layout.** Three breakpoints per SPEC §5: ≥1024px (3-col grid), 720–1023px (2-col), <720px (1-col). Use CSS Grid with `repeat(auto-fit, minmax(...))` or explicit media queries — your call.

## Constraints — non-negotiable

- **Single dependency:** Jinja2. No CSS preprocessor. No JS framework. No bundler. No TypeScript.
- **No localStorage.** sessionStorage for the per-tab session ID is fine.
- **No external CDN links** for fonts, CSS, or JS.
- **No client-side routing.** Every page is a real `.html` file in `dist/`.
- **JS is enhancement, not requirement.** All navigation works without JS; clipboard + analytics are progressive.
- **Light theme only.**
- **Do not author real recipe Instructions text.** Placeholder only, clearly marked.
- **Do not author real tutorial step content beyond plausible placeholder prose.** Placeholder only, clearly marked.

## Working approach

1. **Read all three documents in order.** Take notes on questions or ambiguities; surface them at the end if they're not blocking, or before starting if they're blocking.
2. **Set up the directory structure first.** Create empty directories per the layout in HANDOFF_01 D1.1.
3. **Build the design system before content.** Write `assets/css/styles.css` and verify it makes a meaningful page render before generating 23 recipe pages with broken styling.
4. **Templates next, then content.** Write `base.html`, `catalog.html`, `recipe.html`, `tutorial.html`, `notebooklm.html`, `about.html` in that order.
5. **Then `build.py`.** Wire it up against an empty content set first; verify the build runs and produces an empty `dist/`.
6. **Then content.** Generate the 23 recipe JSON files, the 5 tutorial JSON files, `site_content.json`, `config.json`. Run `build.py` after each major content addition to verify nothing breaks.
7. **Then JavaScript.** Add `site.js` with clipboard + analytics; verify in a browser by opening `dist/index.html` directly via `file://` and clicking through.
8. **Then documentation.** Write `README.md`, `JIM_INTEGRATION_NOTES.md`, `FORM_SETUP_GUIDE.md`.
9. **Run the done-criteria checklist** in HANDOFF_01 as a final sweep.

## Final report format

When you're done, write a report covering:

1. **What got built.** A short summary of the deliverables produced.
2. **What was skipped or deferred, and why.** Anything from HANDOFF_01 you didn't deliver, with a clear reason.
3. **Decisions you made.** Any "CC's choice" decisions from HANDOFF_01 (e.g., embedded vs. external CSS, generator script approach), and what you picked.
4. **Conflicts encountered.** Any places where SPEC.md and HANDOFF_01 disagreed, and how you resolved them per "SPEC wins" guidance.
5. **Known issues.** Anything you're aware of that doesn't quite work yet, or that future handoffs should address.
6. **Verification.** Confirm `python3 build.py` runs clean, `dist/` is populated, and a manual browser walkthrough of catalog → recipe page → tutorial → about works end-to-end.

Be honest in the report. If something in HANDOFF_01 was unclear, say so; if you took a shortcut, surface it; if a deliverable looks finished but you have low confidence, flag it. The next handoff depends on knowing the real state of the build, not an optimistic version.

## Begin

Read SPEC.md, then HANDOFF_01.md, then CONTEXT_TRANSFER.md (skim). Ask questions if anything is blocking; otherwise proceed.
