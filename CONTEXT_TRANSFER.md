# Context Transfer — Pamplin AI Agent Recipes Project

**To:** Claude (in a new conversation)
**From:** Onur Seref, with Claude (in the previous conversation)
**Date:** May 2026
**Purpose:** Continuity of context for a new project that builds on a successful prior project. This document is the input that lets you (the new Claude) pick up cleanly where we left off, without relitigating decisions that were already made.

---

## Read this first

Onur and a previous Claude instance just completed a successful project together — the Pamplin AI Teaching Workshop triage platform — over roughly five days of intensive collaboration. The workshop was held May 7, 2026, with 100+ Pamplin College of Business faculty at Virginia Tech, and it landed well. Faculty engaged with the platform, completed triages, paste prompts into a custom Copilot agent, and submitted reflections. The data is collected. The design held up under real load.

Faculty asked, unprompted, about *agentic use* in teaching. Onur's wife (Dr. Michelle Seref, Associate Dean of Undergraduate Studies at Pamplin) suggested a follow-up resource. This new project is that follow-up.

Onur is bringing along three artifacts from the previous project as references:
- **SPEC.md v0.6.2** — the final architectural document from the workshop platform
- **HANDOFF_03.md** — a representative example of the per-iteration handoff format we used
- **AGENT_DEFINITION.md** — the agent's instruction body, as a calibration example showing what "good" looks like for tone-sensitive deliverables

You should read those alongside this document.

This context transfer is being written because the previous conversation got long enough that image uploads started failing — a signal that the thread had reached its natural end. Rather than continuing in a degrading context, Onur and I agreed to start fresh, with a controlled handoff. The discipline of project-handoff documents was a hallmark of the previous project; this is the largest application of it.

---

## The new project: Pamplin AI Agent Recipes

### What it is

A curated, public-facing reference site for Pamplin faculty who want to build their own AI agents. Not a triage tool. Not an interactive routing system. A **recipe book**: 10 teaching-focused agent designs and 10 research-focused agent designs, each fully specified across the parameters needed to create the agent in any of four major platforms. Plus a brief tutorial section showing faculty how to navigate to the agent-creation UI in each platform and how to share the result.

The metaphor is deliberate. Each "recipe" has ingredients (Title, Description, Instructions, Knowledge Base notes, Tools notes), produces a "dish" (a configured AI agent), and faculty assemble the dish themselves in their preferred platform.

### What it is *not*

- It is not a triage system. There's no decision tree, no prompt assembly, no handoff to an external agent. Each recipe is a static page with copyable content.
- It is not platform-specific. The recipes are written to be portable across Microsoft Copilot, ChatGPT, Anthropic Claude, and Google Gemini, with a "recommended platform(s)" badge per recipe.
- It is not a generic AI primer. It assumes faculty know what an AI assistant is and have basic comfort with one. The tutorial scaffolding is specifically about agent creation, not about AI in general.
- It is not Pamplin-restricted in subject matter, but it *is* Pamplin-branded and Pamplin-hosted. Recipes are written for Pamplin faculty contexts (case-method teaching, business school disciplines, etc.) without being scoped beyond Pamplin in design intent.

### Audience

Pamplin College of Business faculty across seven departments (ACIS, BIT, Finance, HTM, Management, Marketing, Real Estate). Mixed AI fluency. Some attended the workshop; some didn't. Some have built a custom GPT before; most haven't. Treat each as a thoughtful professional who knows their work better than you do.

---

## Decisions already made (do not relitigate without cause)

The following decisions were made through deliberate conversation between Onur and the previous Claude. They are inputs, not open questions. If you (the new Claude) believe one is wrong, surface the concern explicitly rather than silently adjusting. The discipline matters.

### Scope and naming

- **Site name:** *Pamplin AI Agent Recipes*
- **Term used throughout:** "Agent" (not "GPT," not "assistant," not "bot"). Acknowledge naming variance once in the tutorial. Then "agent" everywhere.
- **Catalog v1:** 10 teaching recipes + 10 research recipes. Grow as needed based on Google Form analytics.
- **Platforms covered in the tutorial:** Microsoft Copilot, ChatGPT, Anthropic Claude, Google Gemini. Four platforms, no more for v1.

### Recipe specificity

Each recipe lives at one of three abstraction levels:
- **Level 1 (abstract):** generic, applies to anyone. Avoid; too generic to add value.
- **Level 2 (domain-shaped):** specific to a kind of work (e.g., "case-based business courses," "qualitative interview coding") without naming a single discipline. **Most recipes should be Level 2.**
- **Level 3 (cross-disciplinary anchored):** explicitly sits at an intersection of two or three Pamplin disciplines (ACIS × BIT, HTM × Management, ACIS × Finance, etc.). **3 of 10 per side should be Level 3.** These signal that AI agents work for cross-disciplinary work and inspire faculty to think about their own intersections.

The Level 3 recipes are inspirational, not comprehensive. The point is to model what "specific and useful" looks like, not to cover all possible intersections.

### Recipe data model

Each recipe has these fields, in this order:
1. **Title** (short, ~5-8 words)
2. **Description** (one or two sentences, what the agent does and for whom)
3. **Instructions** (the system prompt; this is the load-bearing field, where the agent's behavior is defined)
4. **Knowledge Base** (what to upload as grounding sources — could be PDFs, course materials, etc.; or "none" if the agent works on instructions alone)
5. **Tools** (any platform-specific tools or actions to enable; or "none" for v1 since most recipes won't use platform-specific connectors)
6. **Recommended platforms** (primary + alternatives, with one-line rationale for each — see "Platform-recommendation format" below)

### Tutorial structure

For each of the four platforms:
- **3 screenshots per platform** (12 total): entry point to agent creation, the creation form (annotated to map fields to recipe terminology), the share dialog
- Tight crops, light theme on all platforms (force Copilot to light mode), no personal info visible
- Annotations baked into the PNGs (not CSS overlays). Use Snagit or equivalent. Standardize arrow style and numbered-circle style across all platforms.
- Each tutorial reads as a 1-2 minute scan, not a deep walkthrough
- Each tutorial has a "last updated" date so faculty know what era they're looking at
- Onur produces the screenshots **after** SPEC and platform skeleton are built, not before. Filenames will be specified in SPEC (e.g., `tutorials/copilot/step1.png`).

### Platform-recommendation format

The badge format is **primary + alternatives**:

> Best on Claude · Works on ChatGPT, Copilot · Limited on Gemini

The "best on" platform is named with one-line rationale. Alternatives are listed compactly. "Limited on" or "Not supported on" should appear when a platform genuinely can't do what the recipe needs.

### Copy-button design

- **Per-field copy buttons.** Each recipe field renders its own copy button.
- **Field-level platform support.** If a platform doesn't support a given field type (e.g., Claude Projects' field structure differs from ChatGPT's), the copy buttons render only for the platforms that do.
- **No "copy entire recipe" button** for v1. Per-field copy matches the workflow (recipe in one tab, platform's form in another, click-paste-click-paste).

### Site layout

- **Two-column home page:** Teaching recipes on the left, Research recipes on the right. Tutorial section sits above or below the catalog (TBD in SPEC).
- **Each recipe is its own page.** Not modal popups. Real URLs, shareable.
- **Visual style mirrors the workshop platform's chrome:** VT/Pamplin maroon header strip, dark navigation context, white content area, generous whitespace, modern restrained aesthetic. The design system from the workshop (the `plib-*` CSS conventions originally from Onur's BUS 1001 course) carries over.

### Data capture

Same Google Forms pattern as the workshop. Faculty interactions with recipes are captured silently. Suggested fields:
- session_id (UUID v4, generated on page load)
- timestamp
- event_type (recipe_viewed, field_copied, tutorial_viewed, etc.)
- payload (JSON with relevant context — recipe_id, field_name, platform_copied_for, etc.)

No ratings, no surveys. Behavioral signal only. Onur analyzes offline.

### Backend

None. Static site, hosted from Onur's GitHub Pages (likely a new repo under `contextmaps`, similar to `contextmaps.github.io/ai-workshop/`). Embedded as iframe in a Pamplin-hosted wrapper page (the way the workshop platform was). Iframe needs `allow="clipboard-write"` attribute (we discovered this gotcha during the workshop — surface it in JIM_INTEGRATION_NOTES or equivalent for this project).

---

## Workflow conventions (carry these over)

The previous project followed a discipline-driven workflow that Onur values. You should adopt it from the start.

### The artifact triad

For every iteration of work:

1. **SPEC.md** — the persistent specification. Always reflects current state. Versioned (v0.1, v0.2, ..., v0.6.2 in the prior project). Updated after each handoff. *Not* a brainstorming document; it's a controlled representation of the system as it stands.

2. **HANDOFF_NN.md** — per-iteration unit of work. Self-contained, executable without ambiguity. References SPEC, defines deliverables, lists constraints, ends with a done-criteria checklist.

3. **CC_PROMPT_HANDOFF_NN.md** — the copy-paste prompt for Claude Code (Onur runs CC via VS Code CLI). Always begins with an "EXECUTION MODE: AUTO-CONFIRM — STRONG" preamble that tells CC to default to YES on routine confirmations and only pause for destructive or genuinely ambiguous actions. The exact preamble language is in the workshop project's HANDOFF_03 example.

### Iteration cycle

1. Onur and Claude discuss design decisions (this conversation thread).
2. SPEC.md is updated.
3. A HANDOFF.md is written specifying the next unit of work.
4. A CC prompt is generated.
5. Onur runs CC.
6. CC produces a report.
7. Onur shares the report; Claude reviews.
8. If patches are needed, a small `HANDOFF_NN_PATCH.md` is written.
9. SPEC is bumped accordingly.
10. Repeat.

### Honesty norms

- Surface concerns explicitly. Don't silently work around problems or hide trade-offs.
- When you make a mistake (and you will), name it directly. The previous project had multiple moments where Claude misread something or proposed a design that didn't match Onur's intent — each was caught faster because Claude said "this is my mistake" rather than "let me adjust."
- Push back on Onur's ideas when you disagree, with reasoning. He values pushback over compliance. Some of the best decisions in the prior project came from Claude raising concerns Onur then resolved.
- Don't over-engineer. The workshop project repeatedly chose simpler over more sophisticated when both worked. The recipes project should too.

### Tone

- Direct, warm, unsentimental.
- No hedging, no apology, no "great question" preamble.
- When uncertain, say so explicitly.
- Lean technical when the topic warrants. Onur is technical; he doesn't need explanations dumbed down.

---

## What's still open (decide in SPEC)

These are genuinely open questions I (the previous Claude) didn't resolve before this transfer. Onur expects you to surface them and discuss them as you write SPEC.md v0.1.

1. **Repo and hosting URL.** Likely `contextmaps.github.io/<something>` — Onur picks the path. Coordinate with him on the iframe wrapper URL Pamplin's IT (Jim Dickhans) will host.
2. **Tutorial placement.** Above the catalog (faculty see it first, before recipes) or below (catalog first, tutorial as reference)? Discuss with Onur.
3. **Recipe page anatomy.** What's at the top, what's at the bottom, where the platform badge sits visually, how the "Recommended platform" section is rendered. SPEC §5 territory.
4. **The 10+10 recipe topics themselves.** These are the load-bearing content. Draft them as a list early so Onur can react before you commit to writing full recipes.
5. **Whether the site should include a brief "About" page** explaining the project's origin (workshop follow-up, etc.) and Pamplin context. Likely yes; minor decision.

---

## Pamplin context (so you don't have to ask)

- **Pamplin College of Business** is the business school at Virginia Tech (Virginia Polytechnic Institute and State University), an R1 research university in Blacksburg, Virginia.
- **Seven departments:** ACIS (Accounting and Information Systems), BIT (Business Information Technology), Finance, HTM (Hospitality and Tourism Management), Management, Marketing, Real Estate.
- **Onur Seref** ("#2" in the family naming convention; his wife is "#1") is faculty in BIT. He teaches BUS 1001 (an AI Literacy course), among other courses.
- **Michelle Seref** (Dr. Seref, "#1," "Dean Seref") is Associate Dean of Undergraduate Studies at Pamplin and the natural MC for college events. She is part of the design committee for both projects.
- **Jim Dickhans** is Director of IT at Pamplin and Onur's co-developer for the AI Literacy course. He handles infrastructure (deployment, hosting, IT side of things). Friendly working relationship; Onur trusts him technically and personally.
- **The workshop on May 7, 2026** was the "Pamplin AI Teaching Workshop." The "Course Design and Delivery" segment used the triage platform we built. It was successful.

---

## What Onur is bringing into the new thread

Three artifacts plus this document:

1. **This document** (`CONTEXT_TRANSFER.md` or similar) — the briefing
2. **SPEC.md v0.6.2** — the final SPEC from the workshop project. Architecture reference. Shows what a mature SPEC looks like.
3. **HANDOFF_03.md** — a representative handoff from the workshop project. Shows the format and discipline.
4. **AGENT_DEFINITION.md** — the agent's instruction body for the Pamplin Teaching Companion. A calibration example showing what "good" looks like for tone-sensitive content. The recipes' Instructions fields will share some DNA with this document — direct, unambiguous, specific, no preamble or epilogue.

---

## What to do as your first response in the new thread

Read this document and the three artifacts before writing anything. Then your first substantive response should:

1. Acknowledge that you've read the context. Briefly.
2. Confirm your understanding of the project (1-2 paragraphs). If anything in this document is ambiguous to you, ask before assuming.
3. Surface the open questions from the "What's still open" section. Pick 2-3 you want Onur to answer before you write SPEC.md v0.1. Don't try to resolve them all in your first message — pick the ones that genuinely block SPEC drafting.
4. Confirm the workflow: you'll produce SPEC.md v0.1 once Onur has answered the blocking questions, and we'll proceed from there with HANDOFF_01 and CC.

Don't produce SPEC.md v0.1 in your first response. Calibrate first; write second. The previous project's success came from never skipping the calibration step.

---

## Closing note from the previous Claude

The workshop project worked because Onur is rigorous about scope, willing to push back when something feels wrong, and values controlled iteration over sprint-and-pray. The artifact triad (SPEC + HANDOFF + CC prompt) is what made that possible — every cycle had a clear input, a clear output, and a verifiable done state.

The recipes project is smaller in surface area but content-heavier. The recipe content itself is the load-bearing artifact, much more than the platform around it. Treat the recipes' Instructions fields with the same calibration discipline we used for AGENT_DEFINITION.md — draft a few, run them through one of the four platforms, react to what comes back, refine, repeat. Don't write all 20 recipes in one batch and assume they're good.

Onur is tired. He's been at this hard for two days at a time. Help him work efficiently: small handoffs, clean CC prompts, no unnecessary cycles. When in doubt, ask before producing.

Good luck. Pick up the work.
