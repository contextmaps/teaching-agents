# FORM_SETUP_GUIDE

A short procedure for creating the Google Form that backs the recipes site's behavioral analytics, and wiring its IDs into `config.json`.

Run this once. Total time: ~10 minutes.

## 1. Form structure

Create a new Google Form (Forms → Blank). Add **four short-answer questions in this order**:

1. `type`
2. `session_id`
3. `timestamp`
4. `payload`

Field labels are arbitrary — only the order and the four corresponding entry IDs matter. Don't make any of the four required (the site posts every event without validation, and a field flagged "required" will reject submissions if the payload is briefly missing).

## 2. Why no `name` / `email` fields

The site captures **anonymous behavioral signal only** — no user identity, no faculty roster matching. A new browser tab gets a fresh UUID v4 session ID and that's the only correlation key.

## 3. How to extract the four entry IDs

1. In the form editor, click the kebab menu (⋮) → **Get pre-filled link**.
2. Fill the four fields with distinguishable placeholder strings:
   - `type` → `TYPE_MARKER`
   - `session_id` → `SESSION_MARKER`
   - `timestamp` → `TIMESTAMP_MARKER`
   - `payload` → `PAYLOAD_MARKER`
3. Click **Get link** → **Copy link**. The URL looks like:

   ```
   https://docs.google.com/forms/d/e/1FAIpQLSxxxxxxxxxxxxxxxx/viewform?usp=pp_url
     &entry.123456789=TYPE_MARKER
     &entry.234567890=SESSION_MARKER
     &entry.345678901=TIMESTAMP_MARKER
     &entry.456789012=PAYLOAD_MARKER
   ```

4. Read the entry IDs off the URL: each `entry.NNNNNNNN=MARKER` tells you which entry ID corresponds to which field. Note all four pairs.

5. Get the **submission URL** by replacing `viewform?usp=pp_url&...` with `formResponse`:

   ```
   https://docs.google.com/forms/d/e/1FAIpQLSxxxxxxxxxxxxxxxx/formResponse
   ```

   This is the URL the site POSTs to.

## 4. Where to put the values

Edit `config.json`'s `form` block. Replace the five placeholder values with what you captured above:

```json
"form": {
  "submission_url": "https://docs.google.com/forms/d/e/1FAIpQLSxxxxxxxxxxxxxxxx/formResponse",
  "entry_event_type": "entry.123456789",
  "entry_session_id": "entry.234567890",
  "entry_timestamp":  "entry.345678901",
  "entry_payload":    "entry.456789012"
}
```

Re-run `python3 build.py`. Commit the change. Done.

## 5. How to verify

From a terminal, post a synthetic test submission with `curl`. Substitute your real form ID and entry IDs:

```bash
curl -X POST 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse' \
  -d 'entry.XXXX=test' \
  -d 'entry.YYYY=test-session' \
  -d 'entry.ZZZZ=2026-05-09T12:00:00Z' \
  -d 'entry.WWWW=test-payload'
```

Expect HTTP 200 (Google sometimes returns a redirect; either is fine for this purpose). Open the form's linked Google Sheet and confirm the row arrived. If you see it, the wiring is correct.

## 6. What to do if a test submission doesn't appear

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| HTTP 4xx / page redirects you to the form's view URL | Wrong submission URL | Use the `formResponse` endpoint, not `viewform` |
| HTTP 200 but no row in the sheet | Wrong entry IDs | Re-extract from the prefilled URL; entry IDs are unique per form |
| Form requires sign-in | Form access setting too tight | In form settings, uncheck "Restrict to … users" / "Collect email addresses" |
| Submission appears for one event type but not another | One of the entry IDs in `config.json` was copied wrong | Double-check each `entry.NNNNN` matches the URL output exactly |

Once a single curl submission lands in the sheet, the site's analytics are live. The site fires `page_view` and `field_copied` events automatically; you should see rows accumulate as faculty browse.
