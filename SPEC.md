# Pamplin AI Agent Recipes — SPEC.md

**Version:** 0.1
**Status:** Draft for review
**Last updated:** 2026-05-08
**Project lead:** Onur Seref (Pamplin BIT)
**Predecessor project:** AI Workshop Triage Platform (SPEC.md v0.6.2)

---

## 1. Purpose

A curated, public-facing reference site for Pamplin College of Business faculty who want to build their own AI agents. The site is a recipe book: 23 teaching-focused agent designs across 7 families, each fully specified across the parameters needed to create the agent on any of four major consumer platforms. Plus a tutorial section showing faculty how to navigate to the agent-creation UI in each platform and how to share the resulting agent.

The metaphor is deliberate. Each recipe has *ingredients* (Title, Description, Instructions, Knowledge Base notes, Tools notes), produces a *dish* (a configured AI agent), and faculty assemble the dish themselves in their preferred platform.

**Audience.** Pamplin faculty across seven departments (ACIS, BIT, Finance, HTM, Management, Marketing, Real Estate). Mixed AI fluency. Some attended the May 7 AI Teaching Workshop; some did not. The site assumes faculty know what an AI assistant is and have basic comfort using one. It does not assume prior agent-building experience.

**Origin.** This project is a follow-up to the Pamplin AI Teaching Workshop (May 7, 2026), which surfaced unprompted faculty interest in building their own agents. The 23 recipes in v1 are derived from the actual selections and free-text submissions of 98 workshop participants, not from designer-imposed structure.

**Deployment context.** The site is hosted on GitHub Pages under `contextmaps` (final URL TBD; placeholder `https://contextmaps.github.io/agent-recipes/`). The site can be accessed directly or embedded as an iframe in a Pamplin-hosted wrapper page if Pamplin IT (Jim Dickhans) has bandwidth to set one up. Direct access is the default-supported mode; iframe wrapping is optional.

The site is not an AI tool. It is a static reference resource that helps faculty configure agents elsewhere.

---

## 2. Scope

### In scope (v1)

- Static, multi-page site: home (catalog), 23 recipe pages, 4 platform tutorial pages, NotebookLM appendix page, About page.
- 23 recipes across 7 families, derived from workshop demand data, with per-recipe Title / Description / Instructions / Knowledge Base / Tools / Recommended Platforms.
- Per-field copy buttons on each recipe page; field-level platform-support visibility.
- Four platform tutorials: Copilot (Chat), ChatGPT, Claude, Gemini. Plus a NotebookLM appendix page covering the lightweight grounded-chat pattern.
- Behavioral analytics via Google Forms (silent capture; same pattern as workshop platform).
- Static build pipeline: per-recipe JSON files → Python build script → static HTML pages.

### Out of scope (v1)

- Live AI agents on the site itself. The site does not call any model.
- User authentication, accounts, or personalization.
- Server-side analytics dashboard. Data is captured to Google Sheet and analyzed offline.
- Research-focused recipes. Deferred to a separate future project (potentially with its own workshop).
- Recipe editing UI for non-developers. Recipe content is config-driven (per-recipe JSON), but editing requires file access; no in-browser CMS.
- Search across recipes. Catalog is small enough (23) that browse-by-family is sufficient for v1.
- Comments, ratings, faculty-submitted recipes. v1 is curated and read-only.
- Cross-recipe linking ("recipes related to this one"). Considered for v2 if analytics show it's useful.

---

## 3. Architecture

```
[Recipe authoring layer]
   recipes/<slug>.json   (one file per recipe; content of record)
   tutorials/<platform>/index.json  (tutorial copy + screenshot manifests)
   site_content.json     (catalog metadata, family descriptions, About page text)

   |
   v
[Build step: Python]
   build.py reads JSON sources + page templates,
   writes static HTML to dist/ along with assets.
   
   |
   v
[Static site: dist/]
   index.html                  (catalog home — 23 recipes grouped by family)
   recipes/<slug>.html         (one page per recipe)
   tutorials/<platform>.html   (one page per platform: copilot, chatgpt, claude, gemini)
   tutorials/notebooklm.html   (appendix page)
   about.html                  (origin and Pamplin context)
   assets/                     (CSS, JS, screenshots, fonts)
   
   |
   v
[GitHub Pages serves dist/]
   Faculty browse, copy recipe fields per-platform,
   paste into agent-creation UI in the platform of their choice.
   
   |
   v
[Behavioral analytics]
   Per-field copy click → POST to Google Form (no-cors)
   Per-page view → POST to Google Form (no-cors)
   No backend; same pattern as workshop platform.
```

**Build step.** Python 3 script (`build.py`) in repo root. Reads JSON sources, renders against Jinja2 templates, writes HTML to `dist/`. Run locally before commit; `dist/` is committed to the repo and served by GitHub Pages from a configured branch (likely `main` or `gh-pages`). No CI/CD; no external build infrastructure. This matches the workshop platform's no-backend discipline.

**Why static-build over single-page-app.** Real per-recipe URLs are shareable, indexable, and load fast on slow connections. A 23-page static build adds about 30 lines of Python over a single-file SPA, and the result is more honest about what each page is.

**Why config-driven.** Recipe content (Instructions especially) is the load-bearing artifact of the project. Editing it without touching code is a hedge against the recipe needing revision after launch. Per Onur's guidance: design for set-and-forget, but keep the edit path cheap.

---

## 4. Faculty Experience

1. Faculty arrives at the site (direct URL or via iframe wrapper if Pamplin IT deploys one).
2. **Home page (catalog).** Sees a brief introduction (1–2 sentences), the 7 family groupings, and 23 recipe cards arranged within their families. Each card shows: title, one-line description, tier badge (Light / Medium / Heavy), and the platform recommendation badge ("Best on X · …"). Family ordering reflects demand from the workshop (Family 1 first, smaller families later). Faculty can scan the whole catalog in under two minutes.
3. **Tutorial section** is below the catalog on the home page (per design decision). A separator row introduces the tutorials: "New to building agents? Start here." Faculty scrolls past the catalog if they want to learn the agent-creation UI; otherwise they engage with recipes directly.
4. Faculty clicks a recipe card → recipe page loads at `/recipes/<slug>.html`.
5. **Recipe page.** Faculty sees the full recipe: Title, Description, Tier, Family, Recommended Platforms (with sub-line trade-off), then the six fields (Title, Description, Instructions, Knowledge Base, Tools, Recommended Platforms — see §5 for layout). Each field has a copy button. Clicking copy → field text is on clipboard, button shows success state, behavioral event fires.
6. Faculty opens their preferred platform's agent-creation UI (separately, in a new tab) and pastes each field into the corresponding form. The recipe page stays open as reference; the workflow is recipe-in-one-tab, platform-in-another, click-paste-click-paste.
7. **Tutorial pages** are accessible from a top nav link or from the home-page tutorial section. Each tutorial walks faculty through the agent-creation UI for one platform: where to start, what each field maps to, how to share the result.
8. Faculty completes their agent in the platform of their choice. The recipes site is done helping at that point.

There is no committed session, no review screen, no clipboard-confirmation Bridge. The recipes site is reference material, not a workflow. Faculty visit it the way they visit a cookbook — open the page they need, copy what they want, close the tab.

---

## 5. UI Baseline

Adopts the `plib-*` design system established in BUS 1001 and refined in the workshop platform, with one specific extension: **VT/Pamplin maroon as the dominant accent**. Per the design decision in early ideation, the recipes site is a destination (faculty revisit it, share URLs, screenshot it), not a workflow inside a wrapper. The body itself carries the brand.

### Color tokens (extending the workshop platform's `:root` block)

The workshop platform uses `--c-obj-accent: #1a5da0` (blue) as the dominant accent. The recipes site overrides this with VT maroon and demotes blue to a secondary role.

```css
:root {
  /* ... workshop platform's existing tokens preserved ... */
  
  /* Pamplin-recipes accent overrides */
  --c-vt-maroon: #861F41;
  --c-vt-maroon-hover: #6b1934;
  --c-vt-orange: #E5751F;       /* secondary accent, sparingly */
  --c-obj-accent: var(--c-vt-maroon);     /* now maroon, was blue */
  --c-primary: var(--c-vt-maroon);
  --c-primary-hover: var(--c-vt-maroon-hover);
  
  /* Tier badge colors */
  --c-tier-light-bg: #f0f7ee;
  --c-tier-light-fg: #14552f;
  --c-tier-medium-bg: #fdf6e3;
  --c-tier-medium-fg: #8a4a00;
  --c-tier-heavy-bg: #fbeae5;
  --c-tier-heavy-fg: #861F41;
}
```

The blue (`#1a5da0`) remains in use for hyperlinks and focus rings — this preserves accessibility contrast and avoids visual collision between primary CTAs and inline links.

### Layout

- **Home page (catalog).** Full-width header strip in maroon with "Pamplin AI Agent Recipes" title and tagline. Below: 7 family sections, each with a section header and a grid of recipe cards. Recipe cards are uniform in size; family sections stack vertically on narrow viewports. Tutorial section below the catalog with its own separator and slightly different visual treatment (lighter background) to signal "different content type."
- **Recipe page.** Single column, ~760px max width (matching the workshop platform's text-content cap). Header with breadcrumb (Home › Family › Recipe Title), then page title, then the field stack. Right rail not used in v1 — keeps the page mobile-friendly without responsive complexity.
- **Tutorial page.** Single column, similar width. Step-by-step layout: short paragraph, screenshot, short paragraph, screenshot. Numbered steps to anchor the sequence.

### Typography and spacing

Inherits from workshop platform: 17px body, 16px form controls, 8px radius, generous whitespace, focus-visible outlines on all interactive elements. No new typography decisions in v1.

### Responsive behavior

- ≥1024px: full layout as above
- 720–1023px: catalog grid collapses to 2 columns; recipe pages unchanged
- <720px: catalog grid collapses to 1 column; recipe pages unchanged; tutorial screenshots scale to fit

---

## 6. Recipe Catalog

The catalog has **23 recipes across 7 families.** Family ordering reflects demand from the May 7 workshop (98 submissions analyzed); within each family, recipes are ordered from most-broadly-applicable to most-specialized.

Tier definitions:
- **Light:** saved system prompt + at most one uploaded file. Faculty who have never built an agent can complete in 15–30 min.
- **Medium:** multi-turn agent with defined role and behavioral constraints. Mostly instruction-led with optional knowledge base. 30–60 min to build, longer to refine.
- **Heavy:** persistent knowledge base, intended for sustained use over a course or research project. May benefit from connectors where the platform supports them. 1–3 hours to build, with calibration over time.

Level definitions (kept light per workshop-data calibration):
- **Level 2** (default): domain-shaped, applies to a kind of teaching work without naming a single discipline.
- **Level 3** (sparingly used, 2 recipes total): explicitly designed around the contrast or intersection of disciplines as the recipe's core value.

### Family 1 — In-class activity engines (6 recipes)

The largest family. Workshop data showed `design_activity` was the most-requested category by a wide margin (25/98 submissions; 2× the next category). Within it, role-play (9) and small-group (8) dominated.

**1.1 The Stakeholder Roleplay Partner** · Medium · Level 2
*Plays a specific stakeholder — a CFO, customer, regulator, hotel guest, founder — for students to interview, negotiate with, or pitch to in class.*
**Best on Claude · decent on Copilot, Gemini, and ChatGPT.** Claude holds a single character voice across long roleplay without slipping into "helpful assistant" mode. The others run the recipe well for shorter exchanges; faculty running long in-class roleplays will notice the difference. A Copilot prototype is a reasonable starting point.

**1.2 The Live Case-Discussion Facilitator** · Medium · Level 2
*Runs a structured case discussion in class — opens with framing, calls on perspectives, surfaces tensions, debriefs at the end.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Multi-turn classroom orchestration works well across all four. Pick by access.

**1.3 The Structured Debate Moderator** · Medium · Level 2
*Runs a two-sided debate in class — assigns positions, prompts each side, plays devil's advocate, synthesizes the strongest arguments.*
**Best on Copilot · similar performance on Gemini and ChatGPT, slightly stronger on Claude for contested topics.** All four handle the format well; Claude is a touch more reliably balanced when the debate involves politically charged or values-laden positions.

**1.4 The Small-Group Exercise Generator** · Light · Level 2
*Produces a fresh small-group exercise — task, materials, time budget, debrief questions — tailored to the day's topic and class size.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Fast generative task; pick by access.

**1.5 The Hands-On Data Activity Builder** · Medium · Level 3 (analytics-using disciplines: ACIS × BIT × Finance × Marketing analytics)
*Generates a realistic, made-up dataset (CSV-shaped) plus an analysis task and discussion questions, for use in quantitative or analytics courses.*
**Best on ChatGPT · strong on Claude, decent on Copilot and Gemini.** ChatGPT's code interpreter validates the dataset shape and runs analyses inline, which makes the recipe more reliable. Claude can produce datasets and reason about them carefully without execution. Copilot and Gemini work for simpler datasets.

**1.6 The Think-Pair-Share Question Engine** · Light · Level 2
*Produces a sequence of think-pair-share prompts at varying cognitive levels for a 50-minute class session, paced to fit the lecture flow.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** The most platform-agnostic recipe in the catalog.

### Family 2 — Student-facing always-on agents (4 recipes)

The high-leverage tier. One build, hundreds of student-uses. Design constraints (hallucination guardrails, scope-creep prevention, "when not to answer" instructions) make the Instructions field for these recipes longer and more guardrail-heavy than faculty-facing recipes. Workshop data showed `student_ai_activity` at 12/98 plus a substantial portion of the 14 free-text "other" entries describing student-facing patterns.

**2.1 The Course FAQ Answerer** · Light · Level 2
*Grounded on a syllabus and course documents; answers student logistics questions and refers back to the human instructor when the answer isn't in the sources.*
**Best on ChatGPT (custom GPT) · similar performance on Gemini (custom Gem) and Claude (Projects), advanced on Copilot Studio for faculty with tenant access.** Custom GPTs and Gemini Gems both support file grounding and shareable links. Copilot Studio offers stronger institutional integration but requires Pamplin tenant access (most faculty would coordinate with Jim Dickhans). NotebookLM is a lightweight alternative.

**2.2 The Concept Tutor (No-Answers, Just Understanding)** · Medium · Level 2
*Helps students build conceptual intuition — analogies, walkthroughs, "what does this mean" reframings — explicitly without giving away problem solutions or doing graded work.*
**Best on Claude · decent on ChatGPT, weaker on Copilot and Gemini.** The spoiler-protection guardrail is the entire recipe. Claude is most consistent at staying in role under student rephrasing; ChatGPT also holds well. Copilot and Gemini have been observed to give in to persistent rephrasing. Faculty deploying for graded courses should test under student pressure.

**2.3 The Adaptive Concept-Practice Partner** · Heavy · Level 2
*Asks students conceptual questions, listens to their answers, adjusts follow-ups based on what the student understood — a Socratic practice partner students use before exams.*
**Best on Claude · decent on ChatGPT, weaker on Copilot and Gemini.** Adaptive Socratic questioning is dialogue-quality-sensitive. Faculty wanting visual-avatar versions need a separate platform like HeyGen, outside this catalog's scope.

**2.4 The Reusable Course Assistant** · Heavy · Level 2
*Grounded on a faculty member's course materials — slides, readings, syllabus, past assignments — that students use throughout the semester for review and asynchronous study support.*
**Best on ChatGPT (custom GPT with Projects) · similar performance on Claude (Projects), strong knowledge-grounding on Gemini but with sharing constraints, advanced on Copilot Studio for faculty with tenant access.** ChatGPT offers the most accessible deployment path for individual faculty. Gemini holds the largest grounding materials but with constrained sharing. NotebookLM is the lightweight alternative.

### Family 3 — Discussion and case-method (3 recipes)

**3.1 The Discussion Question Generator** · Light · Level 2
*Takes a reading and produces a tiered set of discussion questions: opening, probing, application, meta-questions about the reading itself.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Among the most beginner-friendly recipes.

**3.2 The Socratic Case-Method Facilitator** · Medium · Level 2
*Helps faculty rehearse a case-method discussion before class — plays a skeptical student, surfaces where the discussion will go off-track.*
**Best on Copilot · similar performance on Gemini and ChatGPT, slightly stronger on Claude for sustained skeptical voice.** All four can play "thoughtful student" for a rehearsal session; Claude holds the register more consistently across long rehearsals.

**3.3 The Case-Discussion Debrief Synthesizer** · Medium · Level 2
*Takes notes from a case discussion that just happened and synthesizes a debrief document students can review afterward.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Synthesis of messy notes into structure works well across all four.

### Family 4 — Course architecture and conversion (3 recipes)

The highest-lift recipes per build. Workshop data showed three independent course-architecture asks (two "in-person to async" conversions plus one course-design ask) — small in count but high in importance per request.

**4.1 The Course Format Converter** · Heavy · Level 2
*Converts a course from one format to another — in-person to async online, semester to compressed, lecture-heavy to flipped — preserving learning outcomes while restructuring delivery.*
**Best on Gemini for large courses, Claude or ChatGPT (Projects) for moderate-sized · decent on Copilot.** Gemini's very large context window holds an entire semester's materials simultaneously. Claude and ChatGPT Projects work well for moderate courses. Copilot can do conversions on smaller courses but may lose fidelity on very large ones.

**4.2 The Syllabus Modernizer** · Medium · Level 2
*Takes an existing syllabus and produces a revised version — clearer learning objectives, modernized tone, aligned assignments, updated policies — while preserving the faculty member's voice.*
**Best on Copilot · similar performance on Gemini and ChatGPT, slightly stronger on Claude for voice preservation.** Claude is a touch better at preserving distinctive voice; the others tend to standardize toward "professional academic" register.

**4.3 The Module Architect** · Medium · Level 2
*Helps faculty design or restructure a course module from scratch — outcomes, sequence, in-class activities, assessments, materials list.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Structured-output task; pick by access.

### Family 5 — Assessment and feedback (3 recipes)

**5.1 The Rubric Builder** · Light · Level 2
*Interviews the faculty member about an assignment and produces a rubric with clear performance levels and criteria.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Interview-then-produce-rubric works across all four.

**5.2 The Formative Check Generator** · Light · Level 2
*Produces a short formative-assessment instrument calibrated to a topic and student level, with explanations for why each item tests what it tests.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Short-form item generation is highly platform-agnostic.

**5.3 The Feedback Tone Matcher** · Medium · Level 2
*Helps a faculty member calibrate written feedback on student work — paste your draft and a sample of how you usually write, get suggestions that match your voice.*
**Best on Claude · decent on ChatGPT, weaker on Copilot and Gemini.** Voice imitation is the central value. Claude is meaningfully better at matching a faculty member's existing register; the others tend to flatten toward generic-instructor voice.

### Family 6 — Examples, cases, and content (3 recipes)

**6.1 The Discipline-Specific Example Generator** · Light · Level 2
*Takes a concept and produces mini-cases or examples tuned to a specific industry, student level, or current relevance.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Generative variety task; pick by access.

**6.2 The Current-Events Case Freshener** · Light · Level 2
*Takes a recent news event and translates it into a mini-case or in-class discussion vehicle for a specific course.*
**Best on Copilot · similar performance on Gemini and ChatGPT, weaker on Claude for current-events freshness.** The first three pull recent news directly via web search; Claude handles framing well once the source is pasted but doesn't browse independently in the same way.

**6.3 The Concept Explainer With Multiple Framings** · Medium · Level 3 (cross-disciplinary by design)
*Explains a concept through the lens of multiple disciplines — for instance, "explain risk" with framings from Finance, Marketing, Real Estate, and Management — so faculty can pick the framing that fits or use the contrast as the teaching moment.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** One-shot multi-perspective generation works across all four.

### Family 7 — AI-policy (1 recipe)

**7.1 The Course AI-Policy Drafter** · Medium · Level 2
*Interviews the faculty member about their course, values, and concerns; produces draft AI-use policy language for the syllabus, assignment-level guidance, and student-facing disclosure norms, calibrated to the specific course.*
**Best on Copilot · similar performance on Gemini, ChatGPT, and Claude.** Copilot has a slight institutional advantage: faculty drafting AI-use policy may want it to align with VT IT guidance, and Copilot's institutional embedding helps surface that alignment.

### Distribution summary

| Dimension | Count |
|---|---|
| Total recipes | 23 |
| Light tier | 8 |
| Medium tier | 12 |
| Heavy tier | 3 |
| Level 2 | 21 |
| Level 3 | 2 (1.5, 6.3) |
| Best-on Copilot (alone or named) | 14 |
| Best-on ChatGPT (alone or named) | 5 |
| Best-on Claude (alone or named) | 5 |
| Best-on Gemini (alone or named) | 1 (named on 4.1) |

---

## 7. Recipe Page Anatomy

Each recipe page renders six fields, in this fixed order:

1. **Title** — the recipe name (also the page `<h1>`)
2. **Description** — one or two sentences. What the agent does and for whom.
3. **Instructions** — the system prompt; load-bearing field. Long-form (200–800 words depending on recipe).
4. **Knowledge Base** — what to upload as grounding sources, or "none."
5. **Tools** — platform-specific tools or actions to enable, or "none." (Most v1 recipes will have "none.")
6. **Recommended Platforms** — the badge ("Best on X · …") plus the trade-off sub-line.

### Page header (above the field stack)

- Breadcrumb: `Home › Family Name › Recipe Title`
- `<h1>` Recipe title
- Tier badge (Light / Medium / Heavy) and Family pill, side by side
- One-paragraph framing (3–4 sentences) — what this recipe does, who it's for, what success looks like

### Field rendering

Each field renders as:

- Field label (e.g., "Instructions") in `--c-muted` uppercase letterspacing — matches `tri-review-label` from workshop platform
- Field content in a bordered card (white background, `--c-meta-border`, 8px radius)
- Copy button in the top-right of the card; uses the workshop platform's `plib-copy-btn` pattern with success state
- Field-level platform indicator below the copy button, where applicable: small text like "Compatible with Copilot, ChatGPT, Claude, Gemini" or "Knowledge Base only on platforms supporting file uploads."

### Field-level platform support

Some fields don't apply on some platforms (e.g., a recipe with no Tools field doesn't render Tools per platform). For v1, the rule is simpler than the original CONTEXT_TRANSFER suggested:

- **Title, Description, Instructions** — always render, always copyable, supported on all four platforms.
- **Knowledge Base** — renders only if the recipe specifies grounding materials. Sub-text notes which platforms support file uploads in their agent-creation flow (all four do, but with different limits).
- **Tools** — renders only if the recipe specifies tools or actions. Sub-text notes which platforms support each tool. For most v1 recipes, this field is "none."
- **Recommended Platforms** — renders as the badge + trade-off, not as copyable text. This field is for the faculty member's decision, not for paste-into-platform.

### After the field stack

- "How to use this recipe" mini-section (3–5 sentences): "Open [primary platform] → click [agent creation entry point]. Paste each field into the corresponding form input. The Tutorial section (link) walks through the UI for each platform if you haven't built an agent before."
- Cross-link: "Related recipes in this family" — 2–3 other recipes from the same family, as small cards.

The recipe page is dense but not crowded. Target reading time: 3–5 minutes for a faculty member doing the build immediately.

---

## 8. Tutorial Section

Four platform tutorials plus one NotebookLM appendix.

### Each platform tutorial covers

- **Step 1: Entry point.** How to navigate to the agent-creation UI. Screenshot showing the menu/button location.
- **Step 2: Creation form.** Annotated screenshot mapping each field on the platform's form to the recipe's terminology (Title → Name, Description → Description, Instructions → Instructions/System Prompt, Knowledge Base → Sources/Files, Tools → Tools/Actions).
- **Step 3: Save and share.** Screenshot of the share dialog. Explains how to get a shareable link, who can access it, and what to know about access tiers.

Each tutorial:
- 3 screenshots (12 total across the four primary tutorials)
- Tight crops, light theme on all platforms (Copilot forced to light mode)
- No personal information visible in screenshots
- Annotations baked into the PNG (numbered circles, arrows). Snagit or equivalent. Standardized arrow style across all four platforms.
- 1–2 minute scan, not a deep walkthrough
- "Last updated" date in the page footer (faculty know what era they're looking at)

### Copilot vs. Copilot Studio note

The Copilot tutorial covers **Copilot Chat's** built-in agent creation feature, available to any VT faculty member. It does **not** cover Copilot Studio (the enterprise agent-builder), which requires elevated tenant access most faculty don't have.

The Copilot tutorial includes a one-paragraph note at the bottom:
> "Faculty wanting to build agents at the institutional tier — for instance, deploying to all students in a course with Pamplin IT support — should look at Copilot Studio. This is a separate, more advanced product that requires tenant access. Coordinate with Jim Dickhans (Pamplin IT) for that path."

### NotebookLM appendix

A separate, shorter page (roughly half the length of a primary tutorial). Frames NotebookLM honestly:
- Not a peer to the four primary platforms in the agent-creation paradigm.
- A "shareable grounded chat" pattern: upload sources, configure chat behavior, share a notebook link.
- Best for recipes where a faculty member wants to share grounded Q&A over uploaded materials without building a full agent.
- One screenshot showing a notebook's chat interface and share dialog.

Two recipes in the catalog (2.1 The Course FAQ Answerer, 2.4 The Reusable Course Assistant) reference NotebookLM as a "lightweight alternative" — those references link to this appendix page.

### Tutorial placement

Tutorials sit **below the catalog** on the home page (per ideation decision: catalog is the value, tutorials are the reference). Tutorials are also accessible from a top nav link from any page.

### Screenshot timing

Onur produces the screenshots **after** SPEC and platform skeleton are built, not before. Filenames specified in this SPEC for Jim and CC to know what files to expect:

```
assets/tutorials/copilot/step1-entry.png
assets/tutorials/copilot/step2-form.png
assets/tutorials/copilot/step3-share.png
assets/tutorials/chatgpt/step1-entry.png
assets/tutorials/chatgpt/step2-form.png
assets/tutorials/chatgpt/step3-share.png
assets/tutorials/claude/step1-entry.png
assets/tutorials/claude/step2-form.png
assets/tutorials/claude/step3-share.png
assets/tutorials/gemini/step1-entry.png
assets/tutorials/gemini/step2-form.png
assets/tutorials/gemini/step3-share.png
assets/tutorials/notebooklm/notebook-overview.png
```

---

## 9. Build Pipeline

```
recipes/
  001-stakeholder-roleplay-partner.json
  002-live-case-discussion-facilitator.json
  ...
  023-course-ai-policy-drafter.json

tutorials/
  copilot.json
  chatgpt.json
  claude.json
  gemini.json
  notebooklm.json

site_content.json    (catalog metadata, family descriptions, About page)
templates/
  recipe.html        (per-recipe page template)
  tutorial.html      (per-platform tutorial template)
  catalog.html       (home page)
  about.html
  base.html          (header/footer/CSS)

build.py             (Python 3 script; reads JSON + templates → writes dist/)
config.json          (site config: form submission URL, agent-recipe family ordering,
                      analytics flags, last-updated dates per tutorial)

dist/                (built site; committed to repo, served by GitHub Pages)
```

### Build command

```bash
python3 build.py
```

Reads all sources in `recipes/` and `tutorials/`, plus `site_content.json` and `config.json`. Renders all pages to `dist/`. Idempotent (running twice produces identical output).

### Dependencies

Single dependency: **Jinja2** (template rendering). Installed via `pip install jinja2`. No other external dependencies. Build runs in under 5 seconds for 23 recipes.

### Recipe JSON schema

```json
{
  "id": "stakeholder-roleplay-partner",
  "number": "1.1",
  "title": "The Stakeholder Roleplay Partner",
  "family_id": "in_class_activity_engines",
  "tier": "medium",
  "level": 2,
  "description": "Plays a specific stakeholder...",
  "framing_paragraph": "This recipe lets you build an agent that...",
  "fields": {
    "instructions": "You are a [stakeholder type]. ...",
    "knowledge_base": "Optional. If you want the agent grounded on a specific stakeholder's past statements or documents (e.g., investor letters, regulatory rulings), upload those.",
    "tools": "None for v1.",
    "recommended_platforms": {
      "best_on": ["claude"],
      "comparative_phrase": "decent on Copilot, Gemini, and ChatGPT",
      "tradeoff_subline": "Claude holds a single character voice across long roleplay..."
    }
  },
  "related_recipes": ["case-discussion-facilitator", "structured-debate-moderator"]
}
```

### Per-recipe field validation

`build.py` validates each recipe JSON against this schema before rendering. Missing fields cause a build error with a clear message indicating which file and which field. Unknown fields cause a warning but not an error (forward-compatible for future field additions).

---

## 10. Configuration

`config.json` at repo root:

```json
{
  "site": {
    "title": "Pamplin AI Agent Recipes",
    "tagline": "Concrete agent designs for Pamplin faculty.",
    "base_url": "https://contextmaps.github.io/agent-recipes/",
    "iframe_compatible": true
  },
  "families": [
    {"id": "in_class_activity_engines", "label": "In-class activity engines", "order": 1},
    {"id": "student_facing_always_on", "label": "Student-facing always-on agents", "order": 2},
    {"id": "discussion_case_method", "label": "Discussion and case-method", "order": 3},
    {"id": "course_architecture", "label": "Course architecture and conversion", "order": 4},
    {"id": "assessment_feedback", "label": "Assessment and feedback", "order": 5},
    {"id": "examples_cases_content", "label": "Examples, cases, and content", "order": 6},
    {"id": "ai_policy", "label": "AI-policy", "order": 7}
  ],
  "platforms": [
    {"id": "copilot", "label": "Microsoft Copilot", "tutorial_path": "/tutorials/copilot.html"},
    {"id": "chatgpt", "label": "ChatGPT", "tutorial_path": "/tutorials/chatgpt.html"},
    {"id": "claude", "label": "Claude", "tutorial_path": "/tutorials/claude.html"},
    {"id": "gemini", "label": "Google Gemini", "tutorial_path": "/tutorials/gemini.html"}
  ],
  "tutorials": {
    "last_updated": {
      "copilot": null,
      "chatgpt": null,
      "claude": null,
      "gemini": null,
      "notebooklm": null
    }
  },
  "form": {
    "submission_url": "PLACEHOLDER_FORM_URL",
    "entry_event_type": "PLACEHOLDER_ENTRY_ID",
    "entry_session_id": "PLACEHOLDER_ENTRY_ID",
    "entry_timestamp": "PLACEHOLDER_ENTRY_ID",
    "entry_payload": "PLACEHOLDER_ENTRY_ID"
  }
}
```

Tutorial last-updated dates are populated when Onur produces the screenshots and verifies the page is current.

Form submission IDs need to be created (a new Google Form for the recipes site, separate from the workshop's). Onur creates this; placeholder values surface in HANDOFF_01 as a known follow-up.

---

## 11. Behavioral Analytics

Same architecture as the workshop platform: a Google Form with four fields (`type`, `session_id`, `timestamp`, `payload`) that the site POSTs to with `mode: "no-cors"`. Faculty don't see anything; data lands in a Google Sheet for offline analysis.

### Event types captured

- `page_view` — payload: `{"page_type": "catalog" | "recipe" | "tutorial" | "about", "recipe_id": <slug or null>}`
- `field_copied` — payload: `{"recipe_id": <slug>, "field_name": "instructions" | "description" | "knowledge_base" | "tools"}`
- `tutorial_step_viewed` — payload: `{"platform": "copilot" | ..., "step": 1 | 2 | 3}`. Optional; only fires if step-anchored navigation is implemented.
- `family_section_expanded` — payload: `{"family_id": <id>}`. Only if family sections are collapsible (TBD in v0.1.x).

### Session ID

UUID v4 generated client-side at first page load. Persists for the browser session via `sessionStorage`. New tab → new session. (This differs slightly from the workshop platform's session model, which committed sessions on a specific click; the recipes site has no commit point, so per-tab sessions are the closest analog.)

---

## 12. Calibration Plan

The Instructions field is the load-bearing artifact of every recipe. Faculty success depends on the agent built from the recipe behaving as expected. This requires deliberate calibration before launch.

### Calibration method

For each recipe:

1. Author the Instructions field as a draft.
2. Build the agent on the primary recommended platform.
3. Run 2–3 representative prompts at a faculty member would.
4. Evaluate against a checklist:
   - Does the agent stay in role across multiple turns?
   - Does it produce specific, course-relevant output rather than generic?
   - Does it handle edge cases (off-topic asks, ambiguous inputs) gracefully?
   - For student-facing recipes (Family 2): does the agent maintain its guardrails under pressure?
5. If the agent fails on a recurring axis, revise the Instructions field.
6. Repeat until 3 consecutive runs pass without intervention.

### Calibration sequencing

Calibrate Family 2 (student-facing) recipes first — they have the highest stakes (guardrails matter, faculty deploy to real students) and the longest Instructions fields. Then Family 1 (in-class activity engines) — highest demand from workshop. Then 3, 5, 6, 4, 7 in roughly that order.

### Calibration not in v0.1 SPEC

Specific Instructions text for each of the 23 recipes is not in this SPEC. That content is the work of the next several handoffs. SPEC v0.1 establishes the architecture and inventory; subsequent SPECs (v0.2, v0.3) will reflect the calibrated Instructions text as it stabilizes.

---

## 13. Artifact Inventory

| File | Purpose |
|---|---|
| `SPEC.md` | This file. Current state of the system. |
| `CONTEXT_TRANSFER.md` | Initial briefing from prior project; reference only after v0.1. |
| `recipes/*.json` | One file per recipe. Authoring source for catalog. |
| `tutorials/*.json` | One file per platform tutorial; one for NotebookLM appendix. |
| `site_content.json` | Catalog metadata, family descriptions, About page text. |
| `config.json` | Site configuration; form submission URLs; tutorial last-updated dates. |
| `templates/*.html` | Jinja2 templates for catalog, recipe, tutorial, about, base. |
| `build.py` | Python build script. |
| `dist/` | Built static site, committed to repo and served by GitHub Pages. |
| `JIM_INTEGRATION_NOTES.md` | Operational notes for Pamplin IT (iframe wrapping if applicable, agent URL not relevant for this project, data capture). |

Per-iteration `HANDOFF_*.md` and `CC_PROMPT_HANDOFF_*.md` files created as needed.

---

## 14. Open Questions

Carried forward from the ideation conversation; to resolve in subsequent handoffs:

- **Final repo URL.** Likely `contextmaps.github.io/agent-recipes/` or similar. Onur picks the path before HANDOFF_01.
- **Google Form creation.** A new form needs to be created for the recipes site (separate from the workshop's). Onur creates and provides the four `entry_*` IDs and submission URL.
- **About page content.** Brief origin story (workshop follow-up, Pamplin context, who built it). Draft in HANDOFF_01 or HANDOFF_02; not load-bearing for the platform skeleton.
- **Family sections collapsible or always-expanded.** TBD based on usability feel after platform skeleton is built.
- **Whether to add a "share this recipe" button.** Considered for v2 if analytics show recipes are being shared.
- **Mobile screenshot strategy for tutorials.** All four platforms have mobile UIs that look different from desktop. v1 ships desktop-screenshot-only; mobile coverage deferred to v2.
- **Iframe wrapper coordination with Jim.** If Jim has bandwidth to wrap the recipes site in a Pamplin page, do it; if not, the site is fine as a standalone destination. No blocking dependency.

---

## 15. Out-of-Scope Reminders

- No live AI agents on the site.
- No research-focused recipes in v1.
- No user accounts, ratings, or comments.
- No in-browser recipe editor.
- No cross-recipe search.
- No mobile-specific tutorial screenshots.
- No "copy entire recipe as one block" button (per-field is the workflow).

---

## Change log

- **v0.1 (2026-05-08):** Initial draft. Project scope defined: 23 teaching-focused recipes across 7 families, derived from May 7 workshop demand data (98 submissions). Catalog, family ordering, tier distribution, platform recommendations, and architectural decisions all locked. Build pipeline (Python + Jinja2 → static HTML) specified. Tutorial section structure (4 primary platforms + NotebookLM appendix) specified. Behavioral analytics carried over from workshop platform pattern. Open questions enumerated for resolution in subsequent handoffs.
