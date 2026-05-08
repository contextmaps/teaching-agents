# JIM_INTEGRATION_NOTES

Operational notes for Pamplin IT regarding the Pamplin AI Agent Recipes site.

## 1. Site URL

The site is hosted at:

> <https://contextmaps.github.io/teaching-agents/>

Hosted by Onur Seref via GitHub Pages. **No deployment is needed by Pamplin IT.** Updates ship as commits to the `contextmaps/teaching-agents` repo and propagate automatically.

## 2. Optional iframe wrapping

If Pamplin IT wants to embed the recipes site inside a Pamplin-branded page, here's the suggested markup:

```html
<iframe src="https://contextmaps.github.io/teaching-agents/"
        style="width:100%; height:1800px; border:0;"
        title="Pamplin AI Agent Recipes"
        loading="lazy"
        allow="clipboard-write"></iframe>
```

> **`allow="clipboard-write"` is required.** Without it, the per-field copy buttons fail silently inside the iframe. This was the same gotcha the workshop platform hit; mention it explicitly in any embed instructions you ship.

The site itself doesn't need any header-suppression flag — the maroon header is part of the site identity and renders fine inside or outside a wrapper.

## 3. Data capture

Behavioral analytics (page views, copy clicks) post to a Google Form owned by `contextmaps@gmail.com`. Submissions land in a Google Sheet for offline analysis. **No backend infrastructure to maintain.** No personally identifying information is captured — only an anonymous per-tab session ID, event type, timestamp, and a small JSON payload (e.g., the recipe slug and field name on a copy event).

## 4. What can fail

| Failure mode | Impact | Likelihood |
| --- | --- | --- |
| GitHub Pages outage | Site unreachable | Low; Pages is well cached |
| Google Form outage | Analytics events silently fail; site keeps working | Very low |
| Clipboard API denied | Copy button falls back to a hidden textarea + execCommand | Rare on supported browsers |

Recipe content is static, so faculty browsing and copying is **never** blocked by infrastructure.

## 5. Updates over time

Recipe content is calibrated and refined post-launch. Updates ship as commits to `contextmaps/teaching-agents`; GitHub Pages picks them up automatically. No coordination with Pamplin IT is required for content changes.

## 6. Contact

- **Onur Seref** (Pamplin BIT) — design, content, repo ownership.
- **Jim Dickhans** (Pamplin IT) — institutional and IT questions, including **Copilot Studio** access for faculty who want to deploy at the institutional tier (Copilot Studio is the path called out at the bottom of the Copilot tutorial page; the v1 site links faculty to Jim for that path).
