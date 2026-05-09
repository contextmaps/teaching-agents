# HANDOFF_08 — Rename Build Output Folder

**Project:** Pamplin AI Agent Recipes (`teaching-agents`)
**Spec reference:** `SPEC.md` v0.1.2 (this handoff introduces a small structural change reflected in SPEC v0.1.3 after the handoff lands)
**Cut:** Operational — rename the build output folder from `dist/` to `docs/` to enable native GitHub Pages deployment.

---

## Why

GitHub Pages' folder selector for "deploy from a branch" only offers two options: `/(root)` or `/docs`. It does not support arbitrary folder names like `/dist`. To deploy the site without adding CI workflow infrastructure, we rename the build output folder to the supported name.

The change is purely a folder rename plus references to that name. No content changes, no behavior changes, no recipe changes.

After this handoff, GitHub Pages can deploy from `main` branch, `/docs` folder, and the site goes live at `https://contextmaps.github.io/teaching-agents/`.

---

## Inputs

**Repo path:** `contextmaps/teaching-agents`.

**Files to modify:**

```
build.py                          # change OUTPUT_DIR from "dist" to "docs"
.gitignore                        # if it mentions dist/, update to docs/ (likely doesn't)
README.md                         # update any references to dist/
JIM_INTEGRATION_NOTES.md          # update any references to dist/ (if present)
FORM_SETUP_GUIDE.md               # update any references to dist/ (if present)
```

**Files to delete:**

```
dist/                             # remove the entire folder
```

**Files to create (via rebuild):**

```
docs/                             # new build output folder, populated by python build.py
```

CC should grep the entire repo for the string `dist` before making changes, to catch any references in other files. Likely candidates: any helper scripts in `tools/`, any other markdown docs.

---

## Deliverables

### D1 — Update build pipeline

In `build.py`, find the constant or variable that defines the output directory (likely something like `OUTPUT_DIR = "dist"` or `dist_path = Path("dist")`). Change it to `docs`. There should be exactly one place this value is set; if there are multiple references to the string `"dist"` in the file, update all of them.

If the build pipeline writes to a path that's hardcoded inline rather than centralized, refactor it into a single constant. (This is a small code-quality improvement; if it's already centralized, no refactor needed.)

### D2 — Update repo metadata files

- `.gitignore`: if it lists `dist/` as ignored, change to `docs/`. (We're committing the build output, so `docs/` should NOT be ignored either; check current state.)
- `README.md`: update any prose mentions of `dist/` to `docs/`. Update the build instructions section if it tells the reader the output goes to `dist/`.
- Any other docs that mention `dist/`: update to `docs/`.

### D3 — Remove the existing dist/ folder

Delete the `dist/` folder entirely. Don't leave a stub. The folder was a build artifact; it should not coexist with `docs/`.

### D4 — Rebuild

Run `python build.py`. The build now writes to `docs/`. Verify:
- `docs/` exists and contains the rendered site.
- All 23 recipe pages, 5 tutorial pages, the catalog, and the about page render correctly into `docs/`.
- No errors during the build.
- Idempotent rebuild still works.

### D5 — Commit and push

A single commit:

```
HANDOFF_08: Rename build output folder dist/ to docs/

- Renames build output folder from dist/ to docs/ to enable native
  GitHub Pages deployment (Pages does not support arbitrary folder
  names; only /(root) and /docs)
- Updates build.py, .gitignore, README.md, and other repo files
  that reference dist/
- Removes the existing dist/ folder
- Rebuilds into docs/
- No content, behavior, or recipe changes
```

### D6 — Manual step (Onur, after CC's commit)

After the commit lands on origin/main:

1. Visit `https://github.com/contextmaps/teaching-agents/settings/pages`.
2. Under "Build and deployment", change the folder selector from `/(root)` to `/docs`.
3. Click Save.
4. Wait 1-3 minutes for the GitHub Pages workflow to deploy.
5. Visit `https://contextmaps.github.io/teaching-agents/` to confirm the site loads.

This step is NOT part of CC's work; it's an Onur action after the commit lands.

---

## Constraints

- **No content changes.** Recipe JSONs are not touched. Templates are not touched. Schema is not touched. The dependency list does not change.
- **No behavioral changes.** The site renders identically — it just lives at a different folder path in the repo.
- **No new dependencies.**
- **Single commit.** Don't split into "rename in build.py" + "rebuild" + "delete dist" — these are a coherent atomic change.
- **The rebuild produces output identical in content to what was in dist/.** Only the folder name changes; the HTML inside should be byte-identical (modulo any timestamps in the build).

---

## Done criteria

**Code:**
- [ ] `build.py` writes to `docs/` instead of `dist/`. The change is centralized (one place, not scattered).
- [ ] `.gitignore`, `README.md`, and any other prose mentions of `dist/` updated to `docs/`.

**Filesystem:**
- [ ] `dist/` no longer exists in the repo.
- [ ] `docs/` exists and contains the rendered site (23 recipe pages, 5 tutorial pages, catalog, about, assets).
- [ ] The `docs/` contents match what `dist/` contained before the rename (modulo only the path).

**Build:**
- [ ] `python build.py` runs clean and idempotent.
- [ ] No errors. Build time still under 5 seconds.

**Hygiene:**
- [ ] Single commit with the message specified in D5.
- [ ] CC's final report includes: confirmation of all done criteria, sample listing of `docs/` contents to verify the rename worked, any places where `dist/` was referenced that CC found via grep, any decisions made.

---

## Notes for CC

- **This is a smaller handoff than any previous one.** It's mostly a rename. The biggest risk is missing a reference to `dist/` somewhere — grep the whole repo before declaring done.
- **The grep check is mandatory.** Run `grep -r "dist" .` (or equivalent) and verify every hit is either (a) genuinely unrelated to the build folder (e.g., a recipe Instructions field that uses the word "distinct"), or (b) updated to `docs/`. Report what you found.
- **No apply script needed for this handoff.** It's a code change, not a content authoring task. Just edit `build.py` directly.
- **Do not preserve `dist/` as a backup.** Delete it cleanly. Git history preserves the prior state if we ever need it.
- **The rebuild should produce identical HTML to what was in `dist/`.** If you spot any differences in the rendered output beyond the folder path, surface them — that would indicate something unintended changed.
- **Onur is responsible for the GitHub Pages settings change** after the commit lands. CC's work ends with the push.
