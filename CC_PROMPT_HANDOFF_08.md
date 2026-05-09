# CC Prompt — HANDOFF_08: Rename Build Output Folder

You are picking up a static-site project for Pamplin College of Business at Virginia Tech. The recipe catalog is now content-complete (all 23 recipes have real content, zero placeholders, last commit 3b8c567 on origin/main). SPEC v0.1.2 is current.

This handoff (HANDOFF_08) is a small operational change: rename the build output folder from `dist/` to `docs/` so GitHub Pages can deploy from it natively (Pages only supports `/(root)` or `/docs` as deployment folders, not arbitrary names like `/dist`).

This is the smallest handoff in the project. No content changes, no behavioral changes — just a folder rename and references to that folder.

## Mandatory reading order

1. **`HANDOFF_08.md`** — full document. Your work order, deliverables (D1 through D5; D6 is for Onur), and done criteria.
2. **`build.py`** — to find where the output folder is defined.
3. **`.gitignore`, `README.md`** — to find any references to `dist/`.

## Your task

Apply the changes specified in HANDOFF_08:

- Update `build.py` to write to `docs/` instead of `dist/`.
- Update `.gitignore`, `README.md`, and any other repo files that reference `dist/` to use `docs/` instead.
- Remove the existing `dist/` folder.
- Run `python build.py` to populate `docs/`.
- Verify the rendered site in `docs/` is correct.
- Commit and push as a single commit per D5.

D6 (changing the GitHub Pages settings) is for Onur to do after the commit lands. Don't try to do it from CC.

## Operational guidance

**The grep check is mandatory.** Before declaring done, run a recursive grep for `dist` across the repo. Some hits will be legitimate (e.g., the word "distinct" in recipe content); others may be references to the old folder path that need updating. Report what you found in your final report — both what you updated and what you confirmed was unrelated.

**Centralize the output path if it isn't already.** If `build.py` has the string `"dist"` hardcoded in multiple places, refactor it into a single constant (e.g., `OUTPUT_DIR = "docs"`) and reference it everywhere. If it's already centralized, no refactor needed — just change the value.

**Do not preserve `dist/` as a backup.** Delete it. Git history preserves prior state.

**Do not touch recipe JSONs, templates, or any content files.** This handoff is purely about the build output folder location. Recipe content is final and locked.

**The rebuild should produce HTML identical to what was in `dist/`.** Modulo only the folder path. If you spot rendered-output differences (e.g., a page rendering differently, an asset path resolving wrong), surface them in your report — that would indicate something unintended changed.

## Constraints — non-negotiable

- **No content changes.** Recipe JSONs untouched. Templates untouched. Schema untouched.
- **No new dependencies.**
- **No behavioral changes.** The site renders identically.
- **Single commit.** Don't split.

## Working approach

1. **Read HANDOFF_08 fully.**
2. **Grep the repo for `dist`** to enumerate all places it appears.
3. **Update `build.py`** to use `docs` instead of `dist` for the output folder.
4. **Update `.gitignore`, `README.md`, and any other files** that reference `dist/`.
5. **Delete the existing `dist/` folder.**
6. **Run `python build.py`** to populate `docs/`.
7. **Verify** the rebuild produced the correct output (23 recipe pages, 5 tutorial pages, catalog, about, assets — all in `docs/`).
8. **Run the done-criteria checklist** from HANDOFF_08.
9. **Commit and push** per D5.

## Final report format

When done, write a report covering:

1. **What got changed.** Files modified, files deleted, files created.
2. **Decisions made.** Especially: how `build.py` defines the output folder (was it already centralized? did you refactor?).
3. **Grep results.** What `dist` references did you find? Which did you update? Which did you confirm were unrelated (legitimate prose hits)?
4. **Done-criteria status.** Walk through HANDOFF_08's done criteria as a checklist.
5. **Sample listing of `docs/`.** A short tree or `ls` output confirming the rebuild produced the expected structure.
6. **Conflicts encountered.** Any places where SPEC.md v0.1.2 and HANDOFF_08 disagreed (none expected; SPEC will be updated to v0.1.3 after this handoff).
7. **Known issues.** Anything that doesn't quite work, anything you took a shortcut on.
8. **Verification.** Confirm `python build.py` runs clean and idempotent, and the rendered output in `docs/` looks correct.

Be honest in the report.

## A note on D6

After your commit lands on origin/main, Onur will manually change the GitHub Pages settings to deploy from `/docs` instead of `/(root)`. That's not part of your work — your work ends with the push. The README and the SPEC update will document the GitHub Pages configuration so future readers know what's required.

## Begin

Read HANDOFF_08.md. Grep for `dist`. Then proceed.
