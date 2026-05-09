#!/usr/bin/env python3
"""
build.py — Pamplin AI Agent Recipes static site builder.

Reads:
  - config.json
  - site_content.json
  - recipes/*.json   (one per recipe)
  - tutorials/*.json (one per platform plus notebooklm)
  - templates/*.html (Jinja2)
  - assets/**        (copied verbatim into dist/)

Writes:
  - dist/index.html
  - dist/recipes/<slug>.html   (one per recipe)
  - dist/tutorials/<platform>.html (one per primary platform)
  - dist/tutorials/notebooklm.html
  - dist/about.html
  - dist/assets/**             (mirrors source assets)

Single dependency: jinja2.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import markdown as md
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

REPO_ROOT = Path(__file__).resolve().parent
RECIPES_DIR = REPO_ROOT / "recipes"
TUTORIALS_DIR = REPO_ROOT / "tutorials"
TEMPLATES_DIR = REPO_ROOT / "templates"
ASSETS_DIR = REPO_ROOT / "assets"
DIST_DIR = REPO_ROOT / "dist"
CONFIG_PATH = REPO_ROOT / "config.json"
SITE_CONTENT_PATH = REPO_ROOT / "site_content.json"

PLATFORM_LABELS = {
    "copilot": "Copilot",
    "chatgpt": "ChatGPT",
    "claude": "Claude",
    "gemini": "Gemini",
}

# ---------- Validation ----------

REQUIRED_RECIPE_KEYS = {
    "id", "number", "title", "family_id", "tier", "level",
    "description", "framing_paragraph", "fields", "related_recipes",
}
OPTIONAL_RECIPE_KEYS = {"content_status", "customization_notes"}
REQUIRED_RECIPE_FIELD_KEYS = {
    "instructions", "knowledge_base", "tools", "recommended_platforms",
}
REQUIRED_RECOMMENDED_KEYS = {
    "best_on", "comparative_phrase", "tradeoff_subline",
}
ALLOWED_TIERS = {"light", "medium", "heavy"}
ALLOWED_CONTENT_STATUS = {"draft", "final"}

REQUIRED_TUTORIAL_KEYS = {
    "platform_id", "platform_label", "intro_paragraph",
    "anchor_screenshot", "anchor_screenshot_alt",
    "steps", "field_mapping", "footer_note", "last_updated",
}


class BuildError(Exception):
    pass


def validate_recipe(recipe: dict, source: Path) -> None:
    name = source.name

    missing = REQUIRED_RECIPE_KEYS - recipe.keys()
    if missing:
        raise BuildError(f"{name}: missing required field(s): {sorted(missing)}")

    if recipe["tier"] not in ALLOWED_TIERS:
        raise BuildError(
            f"{name}: tier must be one of {sorted(ALLOWED_TIERS)}, got {recipe['tier']!r}"
        )
    if not isinstance(recipe["level"], int):
        raise BuildError(f"{name}: level must be an integer, got {type(recipe['level']).__name__}")

    fields = recipe.get("fields") or {}
    missing_fields = REQUIRED_RECIPE_FIELD_KEYS - fields.keys()
    if missing_fields:
        raise BuildError(f"{name}: fields.* missing key(s): {sorted(missing_fields)}")

    rec_plat = fields.get("recommended_platforms") or {}
    missing_rp = REQUIRED_RECOMMENDED_KEYS - rec_plat.keys()
    if missing_rp:
        raise BuildError(
            f"{name}: fields.recommended_platforms missing key(s): {sorted(missing_rp)}"
        )
    if not isinstance(rec_plat["best_on"], list) or not rec_plat["best_on"]:
        raise BuildError(f"{name}: fields.recommended_platforms.best_on must be a non-empty list")

    if not isinstance(recipe["related_recipes"], list):
        raise BuildError(f"{name}: related_recipes must be a list")

    if "content_status" in recipe:
        if recipe["content_status"] not in ALLOWED_CONTENT_STATUS:
            raise BuildError(
                f"{name}: content_status must be one of {sorted(ALLOWED_CONTENT_STATUS)}, "
                f"got {recipe['content_status']!r}"
            )
    if "customization_notes" in recipe:
        if not isinstance(recipe["customization_notes"], str):
            raise BuildError(
                f"{name}: customization_notes must be a string, "
                f"got {type(recipe['customization_notes']).__name__}"
            )


def validate_tutorial(tutorial: dict, source: Path) -> None:
    name = source.name
    missing = REQUIRED_TUTORIAL_KEYS - tutorial.keys()
    if missing:
        raise BuildError(f"{name}: missing required field(s): {sorted(missing)}")
    if not isinstance(tutorial["steps"], list) or not tutorial["steps"]:
        raise BuildError(f"{name}: steps must be a non-empty list")
    for i, step in enumerate(tutorial["steps"]):
        for k in ("number", "title", "body"):
            if k not in step:
                raise BuildError(f"{name}: steps[{i}] missing key {k!r}")
    if not isinstance(tutorial["field_mapping"], list):
        raise BuildError(f"{name}: field_mapping must be a list")


# ---------- Loading ----------

def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise BuildError(f"{path.name}: invalid JSON ({e.msg} at line {e.lineno})") from e


def load_recipes() -> list[dict]:
    files = sorted(RECIPES_DIR.glob("*.json"))
    if not files:
        raise BuildError(f"No recipe JSON files found in {RECIPES_DIR}")
    out: list[dict] = []
    for path in files:
        recipe = load_json(path)
        validate_recipe(recipe, path)
        # file_slug is the on-disk filename without prefix and .json — used for URLs.
        # File names are NN-slug.json; URL slug is the 'id' field.
        recipe["file_slug"] = recipe["id"]
        recipe["__source__"] = path.name
        # Default content_status to "draft" so templates can branch unconditionally.
        recipe.setdefault("content_status", "draft")
        # Pre-render customization notes markdown to HTML; only surface it when
        # the recipe is final and notes are present.
        if recipe["content_status"] == "final" and recipe.get("customization_notes"):
            recipe["customization_notes_html"] = md.markdown(
                recipe["customization_notes"], tab_length=2
            )
        else:
            recipe["customization_notes_html"] = None
        out.append(recipe)
    # Warn on unknown top-level keys (forward-compatible).
    known = (REQUIRED_RECIPE_KEYS | OPTIONAL_RECIPE_KEYS
             | {"file_slug", "__source__", "customization_notes_html"})
    for r in out:
        unknown = r.keys() - known
        if unknown:
            print(f"  warn: {r['__source__']}: unknown top-level field(s) {sorted(unknown)}",
                  file=sys.stderr)
    return out


def load_tutorials() -> dict[str, dict]:
    out: dict[str, dict] = {}
    files = sorted(TUTORIALS_DIR.glob("*.json"))
    if not files:
        raise BuildError(f"No tutorial JSON files found in {TUTORIALS_DIR}")
    for path in files:
        tut = load_json(path)
        validate_tutorial(tut, path)
        out[tut["platform_id"]] = tut
    return out


# ---------- Helpers ----------

def best_on_label(best_on_list: list[str]) -> str:
    """Render ['claude'] → 'Claude'; ['claude','chatgpt'] → 'Claude and ChatGPT'."""
    labels = [PLATFORM_LABELS.get(p, p.capitalize()) for p in best_on_list]
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} and {labels[1]}"
    return ", ".join(labels[:-1]) + ", and " + labels[-1]


def copy_assets() -> None:
    dest = DIST_DIR / "assets"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ASSETS_DIR, dest)


def ensure_dist() -> None:
    if DIST_DIR.exists():
        # Fully clear dist for idempotent output.
        for child in DIST_DIR.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        DIST_DIR.mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "recipes").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "tutorials").mkdir(parents=True, exist_ok=True)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(content)


# ---------- Render ----------

def main() -> int:
    started = time.time()
    print("teaching-agents build")

    config = load_json(CONFIG_PATH)
    site_content = load_json(SITE_CONTENT_PATH)
    recipes = load_recipes()
    tutorials = load_tutorials()

    families = sorted(config["families"], key=lambda f: f["order"])
    family_label_by_id = {f["id"]: f["label"] for f in families}

    # Group recipes by family, preserving recipe number order within family.
    recipes_by_family: dict[str, list[dict]] = {f["id"]: [] for f in families}
    for r in recipes:
        if r["family_id"] not in recipes_by_family:
            raise BuildError(
                f"{r['__source__']}: family_id {r['family_id']!r} not declared in config.families"
            )
        recipes_by_family[r["family_id"]].append(r)

    def number_key(r: dict) -> tuple[int, int]:
        m = re.match(r"^(\d+)\.(\d+)$", r["number"])
        if not m:
            raise BuildError(f"{r['__source__']}: number {r['number']!r} not in N.M form")
        return (int(m.group(1)), int(m.group(2)))

    for fam_id in recipes_by_family:
        recipes_by_family[fam_id].sort(key=number_key)

    recipes_by_id = {r["id"]: r for r in recipes}

    ensure_dist()

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        undefined=StrictUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    )
    env.globals["best_on_label"] = best_on_label

    # Common context keys.
    base_context = {
        "site": config["site"],
        "form": config["form"],
        "families": families,
        "platforms": config["platforms"],
        "site_content": site_content,
    }

    # ---- catalog (index.html) ----
    catalog_tmpl = env.get_template("catalog.html")
    catalog_ctx = dict(base_context)
    catalog_ctx.update({
        "page": {"type": "catalog", "recipe_id": None},
        "root_prefix": "",   # already at site root
        "recipes_by_family": recipes_by_family,
    })
    write(DIST_DIR / "index.html", catalog_tmpl.render(**catalog_ctx))
    print("  wrote dist/index.html")

    # ---- recipe pages ----
    recipe_tmpl = env.get_template("recipe.html")
    rendered_recipes = 0
    for r in recipes:
        related = []
        for sib_id in r.get("related_recipes", []):
            sib = recipes_by_id.get(sib_id)
            if sib is not None:
                related.append(sib)
        ctx = dict(base_context)
        ctx.update({
            "page": {"type": "recipe", "recipe_id": r["id"]},
            "root_prefix": "../",   # one level up from dist/recipes/
            "recipe": r,
            "family_label": family_label_by_id[r["family_id"]],
            "related": related,
        })
        out_path = DIST_DIR / "recipes" / f"{r['id']}.html"
        write(out_path, recipe_tmpl.render(**ctx))
        rendered_recipes += 1
    print(f"  wrote {rendered_recipes} recipe page(s) under dist/recipes/")

    # ---- tutorial pages ----
    tutorial_tmpl = env.get_template("tutorial.html")
    notebooklm_tmpl = env.get_template("notebooklm.html")
    rendered_tutorials = 0
    for platform_id, tut in tutorials.items():
        ctx = dict(base_context)
        ctx.update({
            "page": {
                "type": "notebooklm" if platform_id == "notebooklm" else "tutorial",
                "recipe_id": None,
            },
            "root_prefix": "../",   # one level up from dist/tutorials/
            "tutorial": tut,
        })
        out_path = DIST_DIR / "tutorials" / f"{platform_id}.html"
        if platform_id == "notebooklm":
            write(out_path, notebooklm_tmpl.render(**ctx))
        else:
            write(out_path, tutorial_tmpl.render(**ctx))
        rendered_tutorials += 1
    print(f"  wrote {rendered_tutorials} tutorial page(s) under dist/tutorials/")

    # ---- about page ----
    about_tmpl = env.get_template("about.html")
    about_ctx = dict(base_context)
    about_ctx.update({
        "page": {"type": "about", "recipe_id": None},
        "root_prefix": "",   # already at site root
    })
    write(DIST_DIR / "about.html", about_tmpl.render(**about_ctx))
    print("  wrote dist/about.html")

    # ---- copy assets ----
    copy_assets()
    print("  copied assets/ -> dist/assets/")

    elapsed = time.time() - started
    print(f"build complete in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as e:
        print(f"BUILD ERROR: {e}", file=sys.stderr)
        sys.exit(1)
