# HANDOFF_01_PATCH — Path Bugs Discovered in Smoke Test

**Project:** Pamplin AI Agent Recipes (`teaching-agents`)
**Parent handoff:** `HANDOFF_01.md`
**Cut:** Patch — three related path bugs surfaced during Onur's manual smoke test of the v0.1 skeleton.

---

## Goal of this patch

Fix three navigation and asset-path bugs that broke the rendered site during smoke testing. All three bugs share a single root cause: templates do not correctly account for the current page's location relative to the site root when emitting paths.

After this patch:
- The site renders with full styling on every page (including recipe pages and tutorial pages, which live one folder deeper than the home page).
- The site runs JavaScript correctly on every page (clipboard copy + analytics).
- Top-nav links work from every page.
- Breadcrumb links work from every page.
- The site works correctly when served from a URL prefix (specifically `https://contextmaps.github.io/teaching-agents/`), not just from the domain root.

---

## Bugs to fix

### Bug 1 — CSS reference points to wrong path

**Symptom:** All pages render unstyled (default browser fonts, blue underlined links, no layout). Onur worked around this manually by moving `dist/assets/css/styles.css` to `dist/css/styles.css`. The manual workaround should be reverted; the templates should be fixed instead.

**Root cause:** The `<link rel="stylesheet">` tag in `base.html` (or wherever the stylesheet is referenced) points to `css/styles.css`. The build script copies the actual stylesheet to `dist/assets/css/styles.css` — matching SPEC §5 and HANDOFF_01 D2.1. The HTML link path and the build's asset destination disagree.

**Fix:** Update the template's stylesheet reference so it resolves to `assets/css/styles.css` from any page. Because pages live at different depths (home page at `dist/index.html`, recipe pages at `dist/recipes/*.html`, tutorial pages at `dist/tutorials/*.html`), the path needs to be either:

- A **relative path computed from the page's depth** — e.g., `assets/css/styles.css` from the home page, `../assets/css/styles.css` from recipe and tutorial pages.
- A **root-relative path with a configurable site prefix** — e.g., `/teaching-agents/assets/css/styles.css` when deployed to GitHub Pages.

The first approach (depth-aware relative paths) is preferred because it works under any URL prefix without configuration changes.

### Bug 2 — JS reference points to wrong path

**Symptom:** Copy buttons on recipe pages do not work — clicking does nothing visually and nothing lands on the clipboard. Browser console shows `GET http://localhost:8000/dist/js/site.js net::ERR_ABORTED 404 (File not found)`.

**Root cause:** Identical to Bug 1. The `<script>` tag points to `js/site.js`, but the build copies the file to `dist/assets/js/site.js` per HANDOFF_01 D2.2.

**Fix:** Same approach as Bug 1 — update the template's script reference so it resolves to `assets/js/site.js` from any page using a depth-aware relative path.

### Bug 3 — Top-nav and breadcrumb links broken on non-home pages

**Symptom:** From the about page (and presumably from every page that's not the home page), the top-nav "Home" link shows `href=""` (empty string), which the browser interprets as a self-reference. Hovering "Home" shows `about.html`; clicking does nothing. The "Tutorials" link uses `href="#tutorials"`, which scrolls to a `#tutorials` anchor on the *current* page rather than navigating to the home page's tutorials section. The "About" link uses `href="about.html"`, which works from the home page only — from any other page (e.g., a recipe page in `dist/recipes/`), it would resolve to a non-existent path like `dist/recipes/about.html`.

The breadcrumb on the about page also has `href=""` for the "Home" link.

**Root cause:** Templates do not know how deep the current page is in the site tree, so they emit either empty hrefs (when relative-path computation fails) or bare filenames (which only resolve correctly from the home page).

**Fix:** Pass the current page's depth (or its path relative to the site root) into every template render call in `build.py`. Use that depth to compute correct relative paths to navigation targets. Apply this fix to:

- The top-nav links (`Home`, `Tutorials`, `About`) in `base.html` or wherever the nav is defined.
- The breadcrumb links in any template that renders breadcrumbs (`recipe.html`, `tutorial.html`, `notebooklm.html`, `about.html`).
- The "related recipes" cross-links on recipe pages (these may already work since they cross-link within the same `recipes/` folder, but verify).
- Any other internal links emitted by templates.

**The "Tutorials" link specifically:** the home page has a `#tutorials` anchor section (per SPEC §4 and HANDOFF_01 — the tutorial section sits below the catalog on the home page). The "Tutorials" nav link should resolve to `index.html#tutorials` from the home page and `../index.html#tutorials` from a recipe or tutorial page. The current `#tutorials`-only href is wrong from any page that isn't the home page.

---

## Suggested implementation approach

The cleanest way to fix all three bugs at once is to introduce a single template variable representing the path prefix to the site root from the current page's location.

For example, in `build.py`, when rendering a recipe page (which lives one folder deep at `dist/recipes/<slug>.html`):

```python
context = {
    # ... existing context ...
    "root_prefix": "../",   # one level up from dist/recipes/ to dist/
}
```

When rendering the home page:

```python
context = {
    # ... existing context ...
    "root_prefix": "",      # already at root
}
```

When rendering a tutorial page:

```python
context = {
    "root_prefix": "../",
}
```

Then in templates, every internal path uses the prefix:

```html
<link rel="stylesheet" href="{{ root_prefix }}assets/css/styles.css">
<script src="{{ root_prefix }}assets/js/site.js"></script>
<a href="{{ root_prefix }}index.html">Home</a>
<a href="{{ root_prefix }}index.html#tutorials">Tutorials</a>
<a href="{{ root_prefix }}about.html">About</a>
```

Recipe-to-recipe cross-links (the "related recipes" section) can use bare filenames since they're within the same folder:

```html
<a href="{{ related.slug }}.html">{{ related.title }}</a>
```

The exact mechanism is CC's choice — a Jinja2 macro, a custom filter, a context variable, or some other approach. The constraint is that the resulting HTML works correctly when:

1. Served from `http://localhost:8000/dist/` (Onur's local smoke test).
2. Served from `https://contextmaps.github.io/teaching-agents/` (production GitHub Pages).
3. Opened directly via `file://` (lower priority but should still work).

Depth-aware relative paths satisfy all three.

---

## Constraints

- **No new dependencies.** Jinja2 only.
- **No client-side path manipulation in JavaScript.** All path resolution happens at build time.
- **No `<base>` tag.** Has surprising interactions with anchor links and is generally fragile for static sites.
- **No hardcoded `/teaching-agents/` prefixes.** The site should work without knowing its eventual deployment URL.
- **Smoke-testable headlessly.** After the patch, CC should grep the rendered HTML in `dist/` and confirm no `href=""` or `src=""` remain in any output file. CC should also confirm that `dist/recipes/001-stakeholder-roleplay-partner.html` references the stylesheet at `../assets/css/styles.css`, not `assets/css/styles.css` or `css/styles.css`.

---

## Done criteria

After running the patch and rebuilding (`python build.py`):

**Asset paths:**
- [ ] No file in `dist/` references `css/styles.css` or `js/site.js` (the wrong paths).
- [ ] The home page (`dist/index.html`) references `assets/css/styles.css` and `assets/js/site.js`.
- [ ] Recipe pages (`dist/recipes/*.html`) reference `../assets/css/styles.css` and `../assets/js/site.js`.
- [ ] Tutorial pages (`dist/tutorials/*.html`) reference `../assets/css/styles.css` and `../assets/js/site.js`.
- [ ] `dist/about.html` references `assets/css/styles.css` and `assets/js/site.js` (assuming it lives at the root of dist; if it lives in a subfolder, adjust accordingly).

**Navigation paths:**
- [ ] No `href=""` (empty) or `src=""` (empty) appears in any rendered HTML in `dist/`.
- [ ] Top-nav "Home" link resolves to `index.html` from the home page and `../index.html` from recipe/tutorial pages.
- [ ] Top-nav "Tutorials" link resolves to `index.html#tutorials` from the home page and `../index.html#tutorials` from recipe/tutorial pages.
- [ ] Top-nav "About" link resolves to `about.html` from the home page and `../about.html` from recipe/tutorial pages.
- [ ] Breadcrumb "Home" links on recipe and tutorial pages resolve to `../index.html`.
- [ ] Related-recipe cross-links on recipe pages still work (likely just bare filenames within the same folder).

**Manual workaround cleanup:**
- [ ] If Onur's manual `dist/css/` directory still exists from the workaround, remove it (the build's idempotent dist-wipe should handle this automatically; just verify).
- [ ] No stray paths in templates pointing to the wrong locations.

**Self-verification:**
- [ ] CC runs `grep -r 'href=""' dist/` and confirms no matches.
- [ ] CC runs `grep -r 'src=""' dist/` and confirms no matches.
- [ ] CC runs `grep -r 'href="css/' dist/` and `grep -r 'src="js/' dist/` and confirms no matches (these would be the pre-patch paths).
- [ ] CC reports the exact `<link>` and `<script>` lines from one home page, one recipe page, and one tutorial page in the final patch report — so Onur can sanity-check before re-running the smoke test.

**Build pipeline:**
- [ ] `python build.py` still completes in under 5 seconds.
- [ ] Build is still idempotent.
- [ ] Schema validation still works.

---

## What's NOT in this patch

The smoke test surfaced these three bugs. Other potential issues that *might* exist but were not observed:

- Tutorial-page screenshot paths (placeholder PNGs may have similar path issues; CC should verify and fix if they do).
- Form submission URL is still a placeholder (per HANDOFF_01; not a bug).
- DRAFT and "under review" banners are intentional.
- Recipe Instructions are intentionally placeholder text.

If CC finds related path bugs in the same template family while implementing this patch (e.g., screenshot paths broken in the same way), CC should fix them and report them in the final report. CC should not, however, expand scope into recipe content or tutorial content.

---

## Final report format

CC's patch report should cover:

1. **What was changed.** A short list of the files modified and the nature of the change.
2. **Verification of done criteria.** Run through the checklist above and note status of each.
3. **Sample output.** The exact `<link>`, `<script>`, and top-nav `<a>` tags from one home page, one recipe page, and one tutorial page in the rendered output.
4. **Any related bugs found and fixed.** If CC discovers related path issues while implementing this patch, fix and report.
5. **Anything not fixed and why.** If a done-criterion can't be met (unlikely for a path patch), explain.

---

## Notes for CC

- This is a small, surgical patch. The architecture from HANDOFF_01 is sound; only the path-emission logic needs fixing.
- Onur's manual `dist/css/` workaround should be cleaned up automatically by the build's idempotent dist-wipe behavior, assuming the build clears `dist/` before each run (per HANDOFF_01). If `dist/css/` persists somehow, delete it manually.
- Resist scope creep. Real recipe content, tutorial content, and About page content are out of scope. They come in HANDOFF_02 and beyond.
- After the patch, smoke-test headlessly to the extent possible: grep the dist for known-bad patterns, render the templates with sample contexts, confirm output file paths match references in the HTML.
