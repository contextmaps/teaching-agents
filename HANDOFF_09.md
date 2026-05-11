# HANDOFF_09 — Tutorial Page Revision

**Project:** Pamplin AI Agent Recipes (`teaching-agents`)
**Spec reference:** `SPEC.md` v0.1.3 (this handoff introduces a structural change to tutorials reflected in SPEC v0.1.4 after the handoff lands)
**Cut:** Operational — convert tutorial pages from screenshot-anchored UI walkthroughs to orientation-focused text that uses platform terminology and an "ask-the-platform" fallback for UI navigation.

---

## Why

Tutorial pages currently include an anchor screenshot per platform. Maintaining those screenshots is unrealistic — the four major platforms (Copilot, ChatGPT, Claude, Gemini) update their UIs frequently, and walking through them with the project lead confirmed the existing tutorial text already doesn't match the current UIs in several places.

The screenshot was solving the wrong problem. The faculty member doesn't need a visual walkthrough; they need orientation: what's this platform's agent paradigm called, how does the configuration flow work, how do you share the result. Once oriented, faculty use the recipe page's copy buttons to populate the form.

The new tutorial design:

- **Drops the entry-point screenshot.** No screenshots on the four main platform tutorials.
- **Uses platform terminology** (Agents, GPTs, Projects, Gems) as the durable navigation anchor, since terminology is stickier than UI element locations.
- **Embeds an "ask the platform" fallback** where UI navigation matters (Steps 1 and 3 — entry point and sharing). When a faculty member can't find what the tutorial names, they're directed to ask the platform itself, which always knows its own current UI.
- **Keeps the recipe-field-to-platform-field mapping table.** This table is durable (platforms rarely rename core form fields) and is the part of the tutorial most directly useful when faculty are mid-flow.
- **Drops the "tutorial content under review" banner.** Tutorials are now durable by design; the banner is misleading.
- **Preserves institutional notes** where they exist (e.g., the Copilot Studio / Jim Dickhans note).

NotebookLM gets a structurally different tutorial because NotebookLM is a structurally different tool — no "agent configuration" paradigm. Its workflow (create notebook → add sources → query) has been stable since launch and is described directly.

---

## Inputs

**Repo path:** `contextmaps/teaching-agents`.

**Files to modify:**

```
tutorials/copilot.json
tutorials/chatgpt.json
tutorials/claude.json
tutorials/gemini.json
tutorials/notebooklm.json
templates/tutorial.html
build.py                       # if any tutorial-status logic exists
```

**Files to delete:**

```
docs/assets/tutorials/copilot/entry-point.png
docs/assets/tutorials/chatgpt/entry-point.png
docs/assets/tutorials/claude/entry-point.png
docs/assets/tutorials/gemini/entry-point.png
docs/assets/tutorials/notebooklm/notebook-overview.png
assets/tutorials/copilot/entry-point.png
assets/tutorials/chatgpt/entry-point.png
assets/tutorials/claude/entry-point.png
assets/tutorials/gemini/entry-point.png
assets/tutorials/notebooklm/notebook-overview.png
```

(The `assets/tutorials/<platform>/` directories themselves can also be removed if they're empty after the PNG deletions. CC should verify path locations — placeholder PNGs may live in either `assets/` or `docs/assets/` or both depending on how the original skeleton was set up.)

---

## Deliverables

### D1 — Replace tutorial content for the five tutorials

For each of the five tutorial JSONs, replace the existing step content with the new orientation-focused content provided in the "Tutorial content" section below. Each tutorial has:

- A short framing paragraph (intro)
- Three numbered steps (with embedded "ask the platform" escape hatches in Steps 1 and 3 for the four main platforms)
- A recipe-field-to-platform-field mapping table (preserved as-is or lightly updated per the content below)
- An institutional note where one exists (preserved as-is or updated per content below)

The tutorial JSON schema is unchanged. Step text gets replaced; the table content gets verified; everything else stays.

If a tutorial JSON has a `tutorial_status` field (or similar) parallel to recipes' `content_status`, set it to whatever value indicates "final / verified" (or remove the field if absence means the banner doesn't show). The point is: no "under review" banner on any tutorial page after this handoff.

### D2 — Update the tutorial.html template

Remove the screenshot block. The template currently renders a placeholder image at the top of each tutorial page; that whole `<figure>` (or equivalent block) gets deleted.

Remove the "tutorial content under review" banner block. If the banner is controlled by a `tutorial_status != "verified"` conditional, the conditional and its rendered HTML get removed. If the banner is hardcoded, the hardcoded markup gets removed.

The rest of the template (page header, breadcrumb, framing paragraph, numbered steps, mapping table, institutional note) stays as-is.

### D3 — Delete the placeholder screenshot PNGs

Remove the five placeholder PNGs from `assets/tutorials/<platform>/`. If `docs/assets/tutorials/<platform>/` directories exist with the same PNGs (because they were committed via the build), remove those too. After this handoff, no entry-point screenshots are referenced or stored anywhere in the repo.

If the `assets/tutorials/<platform>/` directories become empty after PNG deletion, remove the directories as well. Don't leave empty husks.

### D4 — Update build.py if necessary

If `build.py` has any logic that references the screenshot PNGs (e.g., copying them from `assets/` to `docs/assets/` during the build), remove that logic. The build no longer touches tutorial screenshots.

### D5 — Rebuild and verify

After making the changes:

- `python build.py` runs clean and idempotent.
- All five tutorial pages render: framing paragraph, three numbered steps, mapping table, institutional note where applicable.
- No tutorial page shows: a screenshot, a placeholder image, an "under review" banner, or a broken `<img>` tag.
- All 23 recipe pages still render correctly (no regression).
- Catalog home page renders identically.

### D6 — Commit and push

A single commit:

```
HANDOFF_09: Tutorial pages converted to orientation-focused text

- Replaces step content in all five tutorial JSONs with new
  orientation-focused content; embeds "ask the platform" fallbacks
  for UI navigation in Steps 1 and 3 of the four main platforms
- Drops entry-point screenshot block from tutorial.html template
- Drops "tutorial content under review" banner from tutorial.html
- Removes five placeholder PNGs and their directories
- Preserves recipe-field-to-platform-field mapping tables
- No changes to recipes, schema, or build pipeline beyond
  screenshot-asset removal
```

---

## Tutorial content

The five tutorials follow. Replace each tutorial JSON's step content with the content below verbatim. The schema fields (probably `framing_paragraph`, `steps`, `field_mapping`, `institutional_note` or similar) stay; only the text inside changes.

CC should map the content below to the existing JSON structure. If the existing JSON uses different field names than I've assumed, surface the mapping in the final report rather than restructuring the schema.

---

### Microsoft Copilot — `tutorials/copilot.json`

**framing_paragraph:**

```
Microsoft Copilot's consumer-tier agent flow lets any VT faculty member create a custom agent using their institutional Microsoft account. This tutorial covers that consumer flow, not Copilot Studio (a separate, more advanced product for institutional deployments). Expect a guided form, light-weight knowledge grounding, and a shareable link at the end.
```

**Step 1 — Find the agent-creation entry point:**

```
Sign in to Copilot at copilot.microsoft.com with your VT account. Look for "Agents" or "Create an agent" — typically in the left rail. The exact label and location shift with Microsoft's UI updates; if you can't find it, ask Copilot in the chat: "How do I get to the page where I can create a custom agent?" and follow the directions it gives.

If you land in Microsoft 365 Copilot search instead of the chat experience, switch to the chat experience first — agent creation is part of the chat product.
```

**Step 2 — Fill in the configuration:**

```
Copilot walks you through a guided form. Open your chosen recipe in a separate tab and use the copy buttons to fill each field on the form. Use the mapping table below to know which recipe field goes where. Save and preview as you go — Copilot lets you test the agent in a side panel before publishing.

Skip the Capabilities / Tools section unless your recipe specifies tools to enable. Most recipes in this catalog don't need them.
```

**Step 3 — Save and share:**

```
Choose Publish, then pick the visibility level. "Just me" is the default; for a faculty-built agent you want students to use, choose "Shared with people I choose" and add specific accounts or distribution lists. Copy the resulting link and paste it where students can find it (LMS, syllabus, course page).

If you can't find the visibility options or sharing controls, ask Copilot: "How do I share my custom agent with specific people?" — the platform knows its current sharing UI.
```

**Recipe-field-to-platform-field mapping table:**

```
Recipe field          → Microsoft Copilot field
Title                 → Name
Description           → Description
Instructions          → Instructions / System message
Knowledge Base        → Knowledge / Files
Tools                 → Capabilities
```

**Institutional note:**

```
Faculty wanting to build agents at the institutional tier — for instance, deploying to all students in a course with Pamplin IT support — should look at Copilot Studio. This is a separate, more advanced product that requires tenant access. Coordinate with Jim Dickhans (Pamplin IT) for that path.
```

---

### ChatGPT — `tutorials/chatgpt.json`

**framing_paragraph:**

```
ChatGPT calls custom agents "GPTs." Any user with a paid ChatGPT account (Plus, Team, Enterprise, or Edu) can create one. This tutorial covers the consumer GPT creation flow. Expect a conversational builder, file uploads for knowledge grounding, and a shareable link.
```

**Step 1 — Find the GPT creation entry point:**

```
Sign in to ChatGPT at chatgpt.com. Look for "GPTs" or "Explore GPTs" — usually in the left sidebar. From there, "Create" or "+ Create GPT" opens the builder. The exact location shifts with UI updates; if you can't find it, ask ChatGPT: "How do I create a custom GPT?" and follow the directions it gives.

If you're on the free plan, you'll be able to use GPTs but not create them — creation requires a paid plan.
```

**Step 2 — Fill in the configuration:**

```
ChatGPT's builder has two panes: a Create tab with conversational prompts ("What should this GPT do?") and a Configure tab with a structured form. Use the Configure tab — it maps directly to recipe fields.

Open your chosen recipe in a separate tab and use the copy buttons to fill each field on the form. Use the mapping table below to know which recipe field goes where. Test in the side preview as you go.

If your recipe's Instructions are long, paste them into the Instructions field anyway — ChatGPT's Configure tab handles longer system prompts well. Leave Capabilities (web browsing, code interpreter, image generation) at their defaults unless your recipe specifies otherwise.
```

**Step 3 — Save and share:**

```
Click Create or Save in the top right. Pick a visibility setting: "Only me," "Anyone with a link," or "GPT Store." For faculty sharing with students, "Anyone with a link" is usually right — copy the link and distribute it through your LMS or syllabus.

If you don't see the sharing options or visibility controls, ask ChatGPT: "How do I share my GPT with specific people?" — the platform will direct you to the current UI.
```

**Recipe-field-to-platform-field mapping table:**

```
Recipe field          → ChatGPT GPT Configure field
Title                 → Name
Description           → Description
Instructions          → Instructions
Knowledge Base        → Knowledge (file uploads)
Tools                 → Capabilities (web browsing, code interpreter, etc.)
```

**Institutional note:** *(none for ChatGPT — the consumer flow is the deployment path for individual faculty.)*

---

### Claude — `tutorials/claude.json`

**framing_paragraph:**

```
Claude calls custom agents "Projects." A Project bundles a system prompt (called "Custom instructions") with a knowledge base (called "Project knowledge") and gives every conversation in the Project access to both. Projects are available on Claude Pro, Team, and Enterprise plans. This tutorial covers the standard Projects flow.
```

**Step 1 — Find the Project creation entry point:**

```
Sign in to Claude at claude.ai. Look for "Projects" in the left sidebar, then "+ Create Project" or "New Project." The exact label shifts with UI updates; if you can't find it, ask Claude in any conversation: "How do I create a new Project?" and follow the directions it gives.

Note: Claude's Projects are scoped contexts with custom instructions and knowledge, not autonomous agents in the way Copilot or GPTs are. The mental model is "a workspace pre-loaded with instructions and reference material" rather than "an agent that acts on its own."
```

**Step 2 — Fill in the configuration:**

```
Claude's Project setup is simpler than the other platforms — just two text fields and a knowledge area. Open your chosen recipe in a separate tab and use the copy buttons to fill each section. Use the mapping table below.

The Project's "Custom instructions" field takes the recipe's Instructions verbatim. The "Project knowledge" area is where you upload files specified in the recipe's Knowledge Base — Claude reads them at the start of every conversation in this Project.

There's no separate Tools or Capabilities section in standard Projects. Most recipes in this catalog don't need it.
```

**Step 3 — Save and share:**

```
Projects save automatically as you edit. Sharing depends on your plan: Pro Projects are individual-only (you'd need to share an exported version of the instructions and knowledge with another user manually); Team and Enterprise plans let you share Projects within your workspace.

For VT faculty sharing with students, the practical path is usually: give the student your recipe's Title, Description, and Instructions, plus the same knowledge files, and have them create their own Project on their own Claude account. The recipe is the durable artifact; the Project is one instantiation of it.

If your VT account has Claude Team or Enterprise access, ask Claude: "How do I share this Project with my workspace?" for the current sharing flow.
```

**Recipe-field-to-platform-field mapping table:**

```
Recipe field          → Claude Project field
Title                 → Project name
Description           → (no dedicated field; include in Custom instructions if needed)
Instructions          → Custom instructions
Knowledge Base        → Project knowledge (file uploads)
Tools                 → (not applicable in standard Projects)
```

**Institutional note:**

```
Claude's Projects are most useful when faculty want a personal teaching workspace — a Project per course, with that course's materials uploaded, and your teaching instructions saved. For broad student-facing deployment, Copilot or ChatGPT often have cleaner sharing flows.
```

---

### Google Gemini — `tutorials/gemini.json`

**framing_paragraph:**

```
Google Gemini calls custom agents "Gems." Gem creation requires a paid Google Workspace account or Google AI Pro / Ultra subscription. Most VT faculty have access to Gemini through their VT Google Workspace account; check with VT IT if you're unsure. This tutorial covers the standard Gems creation flow.
```

**Step 1 — Find the Gem creation entry point:**

```
Sign in to Gemini at gemini.google.com with your VT account. Look for "Gems" or "Gem manager" — typically accessible from the sidebar. From there, "+ New Gem" or "Create Gem" opens the builder. The exact location shifts with Google's UI updates; if you can't find it, ask Gemini: "How do I create a new Gem?" and follow the directions it gives.

If you don't see Gems in your account, your VT Workspace tier may not include Gemini access — check with VT IT.
```

**Step 2 — Fill in the configuration:**

```
Gemini's Gem builder has a structured form for Name, Description, and Instructions, plus a knowledge file upload area. Open your chosen recipe in a separate tab and use the copy buttons to fill each field. Use the mapping table below.

Gemini handles long instructions well; paste the recipe's full Instructions text into the Instructions field. For Knowledge Base materials, upload the files specified in the recipe — Gemini supports PDFs, Docs, and several other formats.

Gemini doesn't have a separate Tools or Capabilities section in standard Gems. Most recipes in this catalog don't need one.
```

**Step 3 — Save and share:**

```
Save the Gem. Sharing in Gemini works through Google Workspace — share with specific email addresses or with a group. Pick the visibility that fits your use: a specific class roster, a department group, or a broader VT group depending on the recipe.

If you can't find the sharing controls, ask Gemini: "How do I share this Gem with specific people?" — the platform will direct you to the current sharing UI.
```

**Recipe-field-to-platform-field mapping table:**

```
Recipe field          → Gemini Gem field
Title                 → Name
Description           → Description
Instructions          → Instructions
Knowledge Base        → Knowledge / Files
Tools                 → (not applicable in standard Gems)
```

**Institutional note:**

```
Gemini's Gem sharing is tied to Google Workspace permissions, which means VT-internal sharing works well but external sharing (e.g., students who don't have VT accounts) is more constrained. For courses with external participants, Copilot or ChatGPT may be cleaner.
```

---

### NotebookLM — `tutorials/notebooklm.json`

**framing_paragraph:**

```
NotebookLM is structurally different from the four main platforms — it doesn't create an "agent" in the same sense. A notebook is a knowledge base you query: you add source materials (PDFs, docs, websites, audio), and NotebookLM grounds its responses in those sources. The "agent" behavior comes from how you ask questions and the sources you've uploaded, not from a configured system prompt. NotebookLM is included in this catalog as an alternative for recipes that are primarily knowledge-grounded (course FAQ answerers, reading-discussion agents, syllabus-based assistants).
```

**Step 1 — Create a new notebook:**

```
Sign in to NotebookLM at notebooklm.google.com with your VT account. Click "Create new" or the "+ New notebook" button on the home page. Give the notebook a name reflecting your recipe — typically the recipe's Title and the course it's for (e.g., "FIN 3104 Course FAQ").
```

**Step 2 — Add sources:**

```
NotebookLM's central feature is the sources panel. Upload the materials your recipe specifies in its Knowledge Base field — syllabus, schedule, readings, assignment descriptions, lecture slides. NotebookLM supports PDF, text files, Google Docs, web pages, and audio.

Each source you add becomes part of what NotebookLM can answer from. Sources are the recipe's grounding; without them, NotebookLM has nothing course-specific to draw on.

You can add and remove sources at any time — NotebookLM re-indexes automatically.
```

**Step 3 — Use the notebook:**

```
Once sources are uploaded, ask questions in the chat panel. NotebookLM grounds every response in your sources and cites which source each claim comes from. For faculty use, the recipe's Instructions field can serve as the first prompt — paste the Instructions text into the chat to set up the notebook's behavior for the session.

For student-facing deployment, share the notebook by clicking the share icon and adding student emails or a class group. Students get read-only access to the notebook and can ask their own questions.

If you can't find the share controls, ask NotebookLM: "How do I share this notebook with my class?" — the platform will direct you to the current sharing UI.
```

**Recipe-field-to-platform-field mapping table:**

```
Recipe field          → NotebookLM mapping
Title                 → Notebook name
Description           → (use as the notebook's stated purpose; no dedicated field)
Instructions          → First prompt or pinned note (no dedicated system-prompt field)
Knowledge Base        → Sources (uploaded materials)
Tools                 → (not applicable)
```

**Institutional note:**

```
NotebookLM is best when the recipe is fundamentally about querying course materials (the recipe's Knowledge Base is large and central). For recipes that depend on behavioral instructions (roleplay, debate moderation, structured feedback), one of the four main platforms is a better fit.
```

---

## Constraints

- **Preserve any tutorial JSON schema fields not mentioned above.** If a tutorial JSON has fields beyond what this handoff specifies, leave them as-is.
- **No content authoring by CC.** All tutorial content comes from this handoff verbatim.
- **Preserve line breaks within step text.** The blank lines between paragraphs in the step content are intentional.
- **No changes to recipes, recipe schema, or recipe templates.** This handoff is purely about tutorials.
- **No new dependencies.**
- **Single commit.**

---

## Done criteria

**Content:**
- [ ] All five tutorial JSON files have updated `framing_paragraph` and step content matching this handoff verbatim.
- [ ] Recipe-field-to-platform-field mapping tables are present and match the handoff.
- [ ] Institutional notes are present where the handoff specifies them.
- [ ] `tutorial_status` or equivalent set so that no "under review" banner renders.

**Template:**
- [ ] Screenshot block removed from `tutorial.html`.
- [ ] "Under review" banner block removed from `tutorial.html`.
- [ ] All other template structure preserved.

**Assets:**
- [ ] Five placeholder PNGs deleted from `assets/tutorials/<platform>/`.
- [ ] Same PNGs deleted from `docs/assets/tutorials/<platform>/` if present there.
- [ ] Empty `assets/tutorials/<platform>/` directories removed.

**Build:**
- [ ] `python build.py` runs clean and idempotent.
- [ ] No new schema validation errors.
- [ ] No broken `<img>` tags in rendered tutorial pages.
- [ ] Build time still under 5 seconds.

**Visual verification:**
- [ ] All five tutorial pages render: framing, three numbered steps, mapping table, institutional note where applicable.
- [ ] No screenshot, no placeholder image, no "under review" banner on any tutorial page.
- [ ] All 23 recipe pages still render correctly (no regression).
- [ ] Catalog home page renders identically.

**Hygiene:**
- [ ] Single commit with the message specified in D6.
- [ ] CC's final report includes: confirmation of done criteria, sample HTML excerpt of one of the new tutorial pages, list of files deleted, any decisions made.

---

## Notes for CC

- **The schema field names** for tutorial JSONs may not match what I've assumed in this handoff. The existing tutorial JSONs were created in HANDOFF_01 with placeholder content; whatever field names were used then are the field names to preserve now. CC should open one tutorial JSON before applying to confirm the field structure, then map the content from this handoff onto whatever the existing fields are called.
- **The "ask the platform" fallback phrasing is part of the recipe.** Don't soften it ("you might want to ask...") or strengthen it ("you must ask..."). The wording is calibrated to be a clean escape hatch without sounding like a hedge.
- **Institutional notes are intentional content, not afterthoughts.** Don't move them to a generic "Resources" section or strip them. They convey context that the platform's own help system won't surface (Copilot Studio being a separate product, NotebookLM being better for knowledge-grounded recipes than behavioral ones, Gemini's external-sharing limitations).
- **The placeholder PNG deletion needs care.** Verify the paths before deleting — the actual placeholder files may live in `assets/tutorials/<platform>/` or `docs/assets/tutorials/<platform>/` (or both). Use the repo's existing file structure as ground truth, not the path examples in this handoff.
- **If you find any logic in `build.py` that depends on the screenshots existing**, surface it in the final report. The screenshots being absent shouldn't cause build errors after this handoff.
