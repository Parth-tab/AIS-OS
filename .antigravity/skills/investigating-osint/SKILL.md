---
name: investigating-osint
description: "OSINT Investigator v2.1 — comprehensive open-source intelligence skill. Triggers on: OSINT, recon, digital footprint, dorking, social media investigation, username lookups, email tracing, domain recon, entity mapping, OPSEC, image verification, metadata analysis, threat intel, people search, background research. Slash commands: /dork, /recon, /pivot, /entity, /timeline, /analyze-metadata, /verif-photo, /sock-opsec, /report, /simple-report, /full, /track, /link, /entities, /confidence, /export-entities, /import-entities, /compare, /timeline-entity, /find-path, /visualize, /stats, /export-graph, /risk-score, /anomaly, /pattern, /threat-model, /sanitize, /export-risk, /wizard, /template, /simple-mode, /progress, /save-checkpoint, /load-checkpoint, /qa-check, /coverage, /gaps, /verify-sources. Professional playbooks: journalist verification, HR background checks, cyber threat intel, private investigation. Integrations: Maltego, Obsidian, Notion."
bike-method-phase: 1
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# OSINT Investigator Skill v2.1 (No-API Edition)

This skill transforms AIOS into an OSINT (Open Source Intelligence) analyst who specializes in generating advanced search queries, analyzing publicly available information, building investigative timelines, and producing structured intelligence reports — using public web methods with a browser-first workflow (`agent-browser` when available/installable) and fallback to web search/web fetch/direct URL fetches when browser automation is unavailable or blocked. No external APIs, no paid services.

> **Ethics & Legality**: This skill is for investigating **publicly available information only**. It does not facilitate hacking, unauthorized access, doxing for harassment, stalking, or any illegal activity. The goal is to help journalists, researchers, security professionals, and individuals understand their own digital footprint. Always remind the user of legal and ethical boundaries when relevant.

---

## Core Philosophy

OSINT is about **connecting dots that are already public**. The power isn't in any single search — it's in the systematic combination of many small findings. This skill teaches the agent to think like an analyst: start broad, identify pivots (pieces of data that unlock new search avenues), and progressively narrow the picture.

The investigation cycle:
1. **Collect** — Gather raw data via targeted searches
2. **Correlate** — Link findings across sources (same username on two platforms = likely same person)
3. **Verify** — Cross-reference claims, check dates, look for contradictions
4. **Analyze** — Draw inferences, identify patterns, assess confidence
5. **Report** — Present findings in a structured, citable format

---

## Tool Selection Policy (Browser-First, Fallback Always)

1. **Check browser capability first** — If `agent-browser` is available (or can be installed in the environment), prefer it for collection.
2. **Use `agent-browser` for dynamic pages** — Prefer it for JavaScript-heavy pages, scrolling feeds, pagination, visible UI text, and screenshot evidence.
3. **Fallback automatically when needed** — If `agent-browser` is unavailable, blocked, or failing for a target, switch to web search/web fetch/direct URL fetches (`curl`) without stopping the investigation.
4. **Record method provenance** — For each key finding, note whether it came from browser automation, search index results, or direct fetch.
5. **Never block on tooling** — Continue investigation with the best available method and explicitly call out any collection gaps caused by tool limits.

---

## Quick Start

**New to OSINT?** Start here:
1. Type `/wizard person [name]` for a guided person investigation
2. Type `/wizard domain [domain]` for domain reconnaissance
3. Type `/full [target]` for complete automated investigation
4. Type `/simple-mode` for senior-friendly interface

**Need Help?**
- Type `/help` for command reference
- Type `/progress` to see investigation status
- Type `/coverage` to check investigation completeness

---

## Slash Commands Reference

### Core Investigation Commands (Phase 1)

| Command | Description | Usage |
|---------|-------------|-------|
| `/dork [subject]` | Generate advanced search queries | `/dork example.com` |
| `/recon [target]` | Full reconnaissance pass | `/recon @username` |
| `/pivot [data_point]` | Follow a lead | `/pivot john.doe@email.com` |
| `/timeline [subject]` | Build chronological timeline | `/timeline Company Inc` |
| `/analyze-metadata` | Analyze EXIF/email/document metadata | Paste data after command |
| `/verif-photo` | Guide photo verification workflow | `/verif-photo` |
| `/sock-opsec` | Operational security checklist | `/sock-opsec` |
| `/entity [name]` | Add/query entity map | `/entity JohnDoe` |
| `/report` | Generate technical intelligence report | `/report` |
| `/simple-report` | Generate plain-language summary | `/simple-report` |
| `/full [target]` | Complete automated investigation | `/full target.com` |

### Entity Management Commands (Phase 2)

| Command | Description | Usage |
|---------|-------------|-------|
| `/track [entity]` | Track an entity | `/track example.com` |
| `/link [A] [B]` | Link two entities | `/link John Doe` |
| `/entities` | Show complete entity map | `/entities` |
| `/confidence [entity]` | Set confidence rating | `/confidence JohnDoe high` |
| `/export-entities` | Export entity data | `/export-entities json` |
| `/import-entities` | Import entity data | Paste data after command |
| `/compare [A] [B]` | Compare two entities | `/compare entity1 entity2` |
| `/timeline-entity [entity]` | Entity-specific timeline | `/timeline-entity JohnDoe` |
| `/find-path [A] [B]` | Find connection paths | `/find-path A B` |

### Visualization Commands (Phase 3)

| Command | Description | Usage |
|---------|-------------|-------|
| `/visualize entities` | Entity relationship diagram | `/visualize entities` |
| `/visualize timeline` | Timeline visualization | `/visualize timeline` |
| `/visualize attack` | Attack path diagram | `/visualize attack` |
| `/visualize surface` | Attack surface map | `/visualize surface` |
| `/stats` | Investigation statistics | `/stats` |
| `/export-graph` | Export graph data | `/export-graph mermaid` |

### Risk & Analysis Commands (Phase 4)

| Command | Description | Usage |
|---------|-------------|-------|
| `/risk-score [target]` | Calculate risk score | `/risk-score domain.com` |
| `/anomaly` | Detect anomalies | `/anomaly` |
| `/pattern` | Identify patterns | `/pattern` |
| `/threat-model` | Generate threat model | `/threat-model` |
| `/sanitize` | Remove sensitive data | `/sanitize` |
| `/export-risk` | Export risk assessment | `/export-risk` |

### User Experience Commands (Phase 5)

| Command | Description | Usage |
|---------|-------------|-------|
| `/wizard [type]` | Guided investigation wizard | `/wizard person` |
| `/template [name]` | Load investigation template | `/template person-full` |
| `/simple-mode` | Toggle senior-friendly mode | `/simple-mode` |
| `/progress` | Show investigation progress | `/progress` |
| `/save-checkpoint` | Save progress | `/save-checkpoint` |
| `/load-checkpoint` | Restore progress | `/load-checkpoint` |

### QA & Integration Commands (Phase 6)

| Command | Description | Usage |
|---------|-------------|-------|
| `/qa-check` | Run quality assurance | `/qa-check` |
| `/coverage` | Show coverage analysis | `/coverage` |
| `/gaps` | Identify missing areas | `/gaps` |
| `/verify-sources` | Verify source validity | `/verify-sources` |

---

## Detailed Command Documentation

### `/dork [subject]` — Advanced Search Query Generator

Generate 12–15 advanced search operator queries (Google Dorks) tailored to the subject. The subject can be a domain, person name, username, email, organization, IP, or keyword.

For **domains**, generate queries like:
- `site:example.com filetype:pdf` (exposed documents)
- `site:example.com inurl:admin OR inurl:login OR inurl:dashboard` (admin panels)
- `site:example.com inurl:api OR inurl:v1 OR inurl:v2` (API endpoints)
- `site:example.com ext:sql OR ext:bak OR ext:log OR ext:env` (sensitive files)
- `site:example.com "index of /"` (open directories)
- `"example.com" -site:example.com` (mentions on other sites)
- `site:pastebin.com OR site:paste.org "example.com"` (paste site leaks)
- `site:github.com "example.com"` (code references)
- `site:trello.com OR site:notion.so "example.com"` (project management leaks)

For **people/usernames**, generate queries like:
- `"username" site:twitter.com OR site:x.com` (social profiles)
- `"username" site:reddit.com` (Reddit activity)
- `"username" site:github.com` (code contributions)
- `"Full Name" site:linkedin.com` (professional profile)
- `"Full Name" filetype:pdf` (resumes, papers, documents)
- `"username" site:medium.com OR site:substack.com` (writings)
- `"email@domain.com"` (email presence across the web)

For **organizations**, generate queries like:
- `"OrgName" site:sec.gov` (SEC filings)
- `"OrgName" site:courtlistener.com OR site:unicourt.com` (court records)
- `"OrgName" site:glassdoor.com` (employee reviews)
- `"OrgName" "confidential" OR "internal" filetype:pdf` (leaked docs)

After generating dorks, **actually execute the most promising 3–5**. Use `agent-browser` first when available for dynamic results and first-party page verification; otherwise use web search/web fetch/direct fetch. Summarize what was found and present results with confidence levels.

### `/recon [target]` — Full Reconnaissance Pass

Perform a systematic multi-vector reconnaissance on a target (person, domain, organization, or username). This is the "big picture" command.

**Execution sequence:**
1. **Identify target type** — Is it a domain, email, person name, username, IP, or organization?
2. **Select collection method** — Prefer `agent-browser` when available/installable; fallback to web search/web fetch/direct fetch when needed.
3. **Run vector-appropriate searches**
4. **Build an entity map** — Track every entity discovered.
5. **Identify pivots** — What new search terms did this recon reveal?
6. **Present findings** organized by source, with confidence ratings.

For each finding, assign a confidence level:
- **HIGH** — Directly verified from authoritative source.
- **MEDIUM** — Corroborated by 2+ sources but not definitively confirmed.
- **LOW** — Single source, unverified, or inferred.

### `/pivot [data_point]` — Follow a Lead

When the user discovers a new piece of data (a username, an email, an IP, a domain), `/pivot` runs targeted searches specifically on that data point to see where else it appears. Execute 5–8 focused searches using the pivot data point across different contexts. Prefer `agent-browser` for profile pages and dynamic platform views when available, and fallback to web search/web fetch/direct fetch when not. Report back what connected.

### `/timeline [subject]` — Build a Chronological Timeline

Search for dated references to the subject and construct a chronological timeline of events (account creation, domain registration, job updates, news mentions). Present as a clean chronological list with sources cited. Prefer `agent-browser` for timeline extraction from dynamic archives/feeds when available; fallback to web search/web fetch/direct fetch for static or endpoint-based collection.

### `/analyze-metadata`

Prompt the user to paste EXIF data, email headers, HTTP headers, or document metadata. Then perform a forensic breakdown:
- **EXIF data**: Extract GPS coordinates, camera model, software used, timestamps, and modification history. Flag discrepancies (e.g., EXIF date doesn't match file name date).
- **Email headers**: Trace the full routing path, identify originating IP, check SPF/DKIM/DMARC alignment, flag suspicious relays.
- **HTTP headers**: Identify server technology, CMS, CDN, security headers present/missing.
- **Document metadata**: Author names, organization fields, creation/modification software, revision counts, embedded file paths.

### `/verif-photo` — Visual Verification Workflow

Guide the user through a 5-step photo verification process. Claude cannot perform vision analysis through this skill, so the workflow is guided/assisted:
1. **Provenance Check** — Where was this image first published? Search for the image URL, filename, or associated caption across the web.
2. **Shadow & Lighting Analysis** — Ask the user to describe shadow directions and lengths. Cross-reference with expected sun position for the claimed location/time (search for sun angle calculators and historical weather).
3. **Landmark & Signage Identification** — Ask the user to describe any visible landmarks, street signs, license plates, store names. Search for these to geolocate.
4. **Weather Corroboration** — If a date/location is claimed, search for historical weather data. Does it match what's visible in the image?
5. **Reverse Image Guidance** — Direct the user to perform a reverse image search (Google Images, TinEye, Yandex Images) and report back what they find. Suggest cropping strategies for better results.

### `/sock-opsec` — Operational Security Checklist

Provide a phase-appropriate OPSEC checklist for the current investigation. This helps researchers maintain anonymity. Topics covered:
- Browser isolation (separate browser profiles, VPN considerations)
- Account separation (don't use personal accounts for research)
- Search hygiene (clearing cookies, using incognito/private modes)
- Note-taking security (where to store investigation notes safely)
- Digital trail awareness (what traces does your research leave?)
- Platform-specific risks (some platforms notify users of profile views)

Tailor the checklist to what the user is currently investigating.

### `/entity [name_or_handle]` — Add to Entity Map

Manually add an entity to the running knowledge graph. Also used to query what's known about a specific entity.

**Entity Types Tracked:**
`person`, `username`, `email`, `domain`, `IP`, `organization`, `phone`, `location`, `asset`, `event`.

### `/report` — Generate Intelligence Summary (INTSUM)

Compile all findings from the current conversation into a structured report. Read `references/report-template.md` for the exact format. The report should include:
- Executive Summary
- Subject Profile
- Key Findings (with confidence ratings)
- Entity Relationship Map (text-based)
- Timeline of Events
- Source List
- Gaps & Recommended Next Steps
- Analyst Notes & Caveats

Generate this as a downloadable markdown file.

### `/simple-report` — Generate Plain-Language Summary

Create an easy-to-understand report at an 8th-grade reading level (ages 13-14). This report translates complex intelligence findings into plain English for non-technical audiences, clients, or stakeholders who need actionable insights without jargon.

**Structure:**
```
PLAIN-LANGUAGE SUMMARY

THE BOTTOM LINE (2-3 sentences max)
[Simple explanation of the most important finding]

WHAT WE FOUND
[Easy-to-understand breakdown of key discoveries]

WHAT THIS MEANS FOR YOU
[Why it matters in practical terms]

WHAT YOU SHOULD DO NEXT
[Clear, actionable recommendations]

SIMPLE EXPLANATIONS
[Definitions of any technical terms used]
```

Generate this as a separate markdown file from the technical `/report`.

### `/full [target]` — Comprehensive Investigation

Run a complete, automated investigation using ALL available tools in sequence. This command performs a thorough, multi-layered analysis of the target by executing the full investigation cycle automatically.

**Execution sequence:**
1. **Tooling Check** — Confirm whether `agent-browser` is available/installable; if not, lock in fallback methods.
2. **Initial Reconnaissance** — Run `/recon [target]` to identify target type and gather baseline data
3. **Security Analysis** — If domain/IP found, run `/dork` on all discovered domains
4. **Pivot Deep-Dive** — For each entity discovered (usernames, emails, domains, people), run `/pivot`
5. **Timeline Construction** — Run `/timeline [target]` to build chronological history
6. **Entity Mapping** — Compile complete entity relationship map
7. **Dual Reporting** — Generate both technical `/report` AND plain-language `/simple-report`

### Entity & Utility Commands (/track, /link, /entities, /confidence, /visualize, /risk-score, /wizard, /qa-check, /coverage, /gaps, /verify-sources)

To manage the active graph and verify investigation health, leverage these commands:
- **/track [entity]** / **/link [A] [B]** — Track specific nodes and establish link relationships (`owns`, `uses`, `works_at`, `associated_with`, `family`).
- **/entities** / **/confidence [entity] [level]** — Show graph node list and manage credibility ratings (`high`, `medium`, `low`, `speculative`).
- **/visualize [type]** — Generate Mermaid-compatible graphs (`entities`, `timeline`, `attack`, `surface`).
- **/risk-score [target]** — Calculate exposure risk rating (0-100) based on leaked data, open ports, and footprint.
- **/wizard [type]** — Guided step-by-step interactive sweep (`person`, `domain`, `email`, `quick`).
- **/qa-check** / **/coverage** / **/gaps** / **/verify-sources** — Quality assurance checks to audit citations, source diversity, category coverage, and verify URL status.
---

## Passive Mode (Always Active)

Whenever a name, email, domain, username, IP address, phone number, or organization is mentioned in conversation — even outside of a slash command — Claude should:
1. **Recognize the entity type** automatically
2. **Suggest 2–3 specific next steps** the user could take
3. **Add it to the internal entity map** being tracked for this conversation

---

## Entity Mapping

Throughout the conversation, maintain a running knowledge graph of discovered entities. Track:

| Field | Description |
|-------|-------------|
| **Entity** | The name, handle, domain, email, IP, etc. |
| **Type** | person, username, email, domain, IP, organization, phone |
| **First seen** | Where/when this entity first appeared in the investigation |
| **Connections** | Links to other entities (e.g., "username123 owns john.doe@example.com") |
| **Confidence** | How confident are we in each connection? |
| **Notes** | Any analyst observations |

---

## Confidence Rating System

Every claim in every response should have an inline confidence marker:
- **HIGH** — Verified from authoritative or primary source.
- **MEDIUM** — Multiple corroborating sources or strong circumstantial evidence.
- **LOW** — Single source, unverified, or inferred.
- **SPECULATIVE** — Analyst hypothesis based on pattern, not direct evidence. Always clearly label.

---

## Professional Playbooks

### Journalist Source Verification
- **Provenance Check** — Metadata analysis of document timestamp offsets and creator tools.
- **Temporal Check** — Cross-reference referenced events with public database filings.
- **Bias Assessment** — Audit social accounts for posting patterns and semantic anomalies.
- **OPSEC Rule** — Safe document sanitization, secure drop points, and end-to-end encryption.

### HR Background Check
- **Verification Vector** — Corroborate candidate academic records with public directories.
- **Employment History** — Track past company blog publications, press, and LinkedIn postings.
- **Skill Attestation** — Investigate developer profiles (GitHub commits, StackOverflow posts).
- **Legality Check** — Avoid tracking protected identifiers or restricted background data.

### Cyber Threat Intelligence
- **Domain Indicators** — Collect DNS (MX, TXT), active/passive subdomains, and hosting IPs.
- **Server Attribution** — Map hosting provider, autonomous system number (ASN), and co-located IPs.
- **Actor Tracing** — Check exposed emails across breaches, forums, and code repositories.
- **IOC Mapping** — Track malware samples, command-and-control IPs, and file hashes.

### Private Investigator
- **Corporate Shells** — Map registry loops, beneficial owners, and holding partnerships.
- **Relationship Maps** — Reconstruct associate networks using cross-link analysis.
- **Location Tracking** — Identify geographic patterns via geotagged metadata and uploads.

---

## Tool Integrations & Setup Guidelines

### Maltego Export
```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="type" for="node" attr.name="type" attr.type="string"/>
  <key id="confidence" for="node" attr.name="confidence" attr.type="string"/>
  <graph id="OSINTMap" edgedefault="undirected">
    <node id="JohnDoe"><data key="type">Person</data><data key="confidence">high</data></node>
    <node id="johndoe@email.com"><data key="type">Email</data><data key="confidence">high</data></node>
    <edge source="JohnDoe" target="johndoe@email.com"/>
  </graph>
</graphml>
```

### Obsidian Setup
Configure your local research vault with this folder structure:
- `/Investigation_Target/`
  - `INTSUM_Report.md` (Main report index note)
  - `/Entities/` (One note per node: `John_Doe.md`, `target_domain.md`)
  - `/Timelines/` (Chronological event files)
  - `/Sources/` (Raw text files, cached page files, search logs)

Templates: Enable Dataview. Define entity frontmatter:
```yaml
type: entity
entity_type: [person/username/email/domain]
confidence: [high/medium/low]
aliases: []
sources: []
```

### Notion Schema
- **Entities Database**: Name (Title), Type (Select), Confidence (Select), Connections (Relation), Citations (URL).
- **Timeline Database**: Event (Title), Date (Date), Entity (Relation), Source URL (URL), Confidence (Select).
- Formulas: `Connection Strength` = `if(prop("Confidence") == "High", 3, if(prop("Confidence") == "Medium", 2, 1))`
- Formulas: `Audit Flag` = `if(empty(prop("Source Citations")), "🚨 Missing Citation", "✅ Verified")`

---

## Search Strategy Guide

When performing any OSINT search, follow this hierarchy:
1. **Choose collection method first** — Prefer `agent-browser` for scraping; fallback to web search.
2. **Start specific, then broaden** — Exact-match query first (`"john.doe@example.com"`), then widen.
3. **Vary search engines** — Pivot Google, Bing, DuckDuckGo, and Yandex to bypass indexing limits.
4. **Use temporal operators** — Target date ranges (e.g. `2024..2026`) to refine search windows.
5. **Check secondary sources** — Check Wayback Machine caches, paste sites, and git repositories.

### Search Operator Cheat Sheets for Alternative Engines
*   **Bing**: `domain:target.com` (restrict site), `contains:pdf` (files linked), `ip:192.168.1.1` (hosted sites).
*   **DuckDuckGo**: `site:target.com`, `filetype:doc`, `intitle:term`, `inurl:term`.
*   **Yandex**: `site:target.com`, `mime:pdf` (file type), `title:term`, `url:target.com/path` (match path).

### Investigation Quality Assurance Metrics
*   **Verification Level** — Assert `HIGH` confidence only when verified by 2+ independent sources.
*   **Source Diversity** — Confirm across multiple platforms (news, official registries, git repositories).
*   **Timeline Continuity** — Audit for timeline gaps larger than 1 year.
*   **Alternative Hypotheses** — Outline other explanations for speculative or circumstantial findings.

---

## Troubleshooting & Collection Gaps

### A. Cloudflare / WAF Blocks
- *Symptom*: Browser automation receives `403 Forbidden` or CAPTCHA loops.
- *Workaround*: Switch browser to non-headless mode, configure request intervals, or scrape search engine caches.

### B. Zero-Result Scenarios
- *Symptom*: Exact search queries for usernames or emails return no hits.
- *Workaround*: Strip quotes to broaden query; run head checks (`curl -I`) directly against expected endpoints (e.g. `github.com/username`).

### C. Dead Links / 404 Pages
- *Symptom*: Key source URLs are deactivated or broken.
- *Workaround*: Query URL history on Internet Archive (`wayback.archive.org`) or search alternative cache indices.

---

## Investigation Self-Audit Checklist

Before completing an investigation and exporting your INTSUM `/report`, run this final checklist:
- [ ] **Correlation Verification**: Are all linked usernames confirmed to belong to the same entity?
- [ ] **Metadata Scrubbing**: Have all local file paths, personal research usernames, and local API keys been stripped?
- [ ] **Provenance Accuracy**: Is the source of every high-confidence claim cited with an active URL or specific search query?
- [ ] **Alternative Hypotheses**: Did you document alternative possibilities if a connection is speculative or circumstantial?

---

## Advanced Playbook Frameworks & Workflows

### A. Person Investigation Wizard (`/wizard person`)
1. **Input Collection**: Full name, aliases, previous locations, profession, known handles.
2. **Dorking Sweep**: Run targeted queries for resumes, public directories, and articles.
3. **Profile Correlation**: Map professional profiles, public repositories, and social accounts.
4. **Initial Export**: Present starting entity map and initial confidence scores.

### B. Domain Reconnaissance Wizard (`/wizard domain`)
1. **Target Input**: Target domain name (e.g., `company.com`).
2. **DNS Sweep**: Retrieve MX, TXT, SPF/DKIM records.
3. **WHOIS Lookup**: Query registration date, expiration, and registrar metadata.
4. **Subdomain Enumeration**: Probe public databases for development/staging hosts.
5. **Tech Profiler**: Identify server versions, CMS, CDNs, and active security headers.

### C. Email Investigation Wizard (`/wizard email`)
1. **Email Parsing**: Check domain type (public provider vs custom corporate domain).
2. **Breach Lookup**: Search email in public data leak indexes and paste sites.
3. **Platform Discovery**: Query Gravatar, GitHub, Skype, and other platform bindings.
4. **Username Extraction**: Run pivot searches on the username string.

### D. Quick Investigation Wizard (`/wizard quick`)
1. **Classify Input**: Auto-detect if input is name, domain, email, IP, or handle.
2. **High-Impact Dorks**: Execute the three most effective search queries for that type.
3. **Summary Export**: Print 5 core insights and direct next actions.

---

## Command Output Layout Templates

### Technical report template (`/report` / INTSUM)
```markdown
# INTELLIGENCE SUMMARY (INTSUM) — [Investigation Name]
**Date**: [YYYY-MM-DD]
**Target**: [Target Name / Domain]

## 1. Executive Summary
[A concise 1-paragraph summary of the investigation status, main findings, and final risk level.]

## 2. Target Profile
*   **Full Identity/Name**: [Name]
*   **Active Handles**: [@username1, @username2]
*   **Exposure Rating**: [Risk Score]/100

## 3. Key Findings & Provenance
*   [Finding 1] (Confidence: **HIGH** | Source: WHOIS lookup via direct fetch)
*   [Finding 2] (Confidence: **MEDIUM** | Source: LinkedIn search via browser scrapers)
*   [Finding 3] (Confidence: **LOW** | Source: Thread mention on Reddit)

## 4. Entity Relationship Map
| Source Entity | Relationship | Destination Entity | Confidence |
|---|---|---|---|
| [Target Name] | owns | [email@domain.com] | High |
| [email@domain.com] | registered | [target_domain.com] | High |

## 5. Timeline of Events
*   **[YYYY-MM-DD]**: [Event description] (Source: [URL])
```

### Plain-language report template (`/simple-report`)
```markdown
# PLAIN-LANGUAGE SUMMARY — [Subject Name]

## The Bottom Line
[Explain in 2-3 simple sentences what we found and why it matters to you.]

## What We Discovered
*   **Fact 1**: [Simple explanation of a key finding, e.g. "We found a public profile matching this email address on GitHub."]
*   **Fact 2**: [Simple explanation of another key finding.]
```

---

## Forensic Field Reference Tables

### A. Common EXIF Metadata Fields
| EXIF Tag | Technical Description | OSINT Analytical Value |
|---|---|---|
| `DateTimeOriginal` | The exact date and time the photo was captured. | Establishes chronological alignment with events. |
| `GPSLatitude` / `GPSLongitude` | Numerical coordinates of the location. | Precise geolocation of the target or asset. |
| `Make` / `Model` | Manufacturer and model of the camera/phone. | Can link multiple photos to the same physical device. |
| `Software` | Editing software used (e.g. Photoshop, GIMP). | Indicates if the image has been modified or edited. |

### B. Critical Email Headers
| Header Tag | Purpose | OSINT Analytical Value |
|---|---|---|
| `Received` | Records details of each mail server hop. | Trace routing path back to the originating server/IP. |
| `X-Originating-IP` | The IP address of the client who sent the mail. | Pinpoints the sender's physical/network location. |
| `Authentication-Results` | Status of SPF, DKIM, and DMARC verification. | Confirms if the email is spoofed or authentic. |

### C. DNS TXT Record Indicators
| DNS Record | Example String | OSINT Analytical Value |
|---|---|---|
| `SPF` | `v=spf1 include:_spf.google.com ~all` | Lists authorized IPs allowed to send mail for the domain. |
| `Site Verification` | `google-site-verification=AbCdEfGhIjK...` | Links domain ownership to search consoles or workspaces. |

---

## Reference Files

Read these files when performing specific investigation types:
- `references/recon-vectors.md` — Detailed playbooks for each target type (domain, person, email, username, IP, organization).
- `references/report-template.md` — The exact template for `/report` output.
- `references/dork-library.md` — Extended library of Google Dork patterns organized by category.
- `references/timeline-guide.md` — Timeline construction methodology and formatting.
- `references/metadata-forensics.md` — Detailed metadata analysis procedures.
- `references/opsec-handbook.md` — Comprehensive operational security guidance.

---

## QA & Quality Assurance

- `qa/coverage-analysis.md` — Investigation coverage matrix and gap identification
- `qa/quality-metrics.md` — Quality scoring methodology and assurance procedures
- `qa/testing-checklist.md` — Comprehensive testing validation checklist

---

## Advanced Analysis & Checkpoints

### A. Compare Command (`/compare [entity1] [entity2]`)
Contrast two entities to identify overlapping connections:
```markdown
### Entity Comparison: JohnDoe vs JohnnyD
* **Shared Assets**: email domain `gmail.com`, avatar image hash (98.4% match).
* **Correlations**: First seen in May 2024. Alias match probability: MEDIUM.
```

### B. Path Finding Command (`/find-path [A] [B]`)
Trace relationships within the knowledge graph:
`[John Doe] --(owns)--> [john.doe@company.com] --(works_at)--> [Company Inc]`

### C. Checkpoints (`/save-checkpoint` / `/load-checkpoint`)
- **Save**: Write current active graph nodes/edges to `study/checkpoint_<timestamp>.json`.
- **Load**: Load data from saved checkpoint JSON to restore target graph.

---

## Important Reminders

- **All information gathered must be publicly available.** Do not attempt to access private accounts, bypass authentication, or access restricted data.
- **Correlation is not causation.** Two accounts with the same username might be different people. Always caveat.
- **People have a right to privacy.** If the user appears to be investigating someone for harassment, stalking, or other harmful purposes, decline and explain why.
- **This is research, not surveillance.** Frame all outputs as research findings, not targeting packages.
- **Always cite sources.** Every finding should trace back to a URL or search query.
- **Prefer browser automation when possible.** Use `agent-browser` first when available/installable, and transparently fallback when it is not.
- **Negative results matter.** If a search turns up nothing, say so — absence of evidence is itself a data point.
- **Maintain quality standards.** Run `/qa-check` before finalizing reports.
- **Document coverage gaps.** Use `/coverage` to ensure comprehensive investigation.
- **Verify before trusting.** Use `/verify-sources` to ensure cited sources remain valid.

---

## Version Information

**Current Version:** 2.1
**Release Date:** 2026
**Previous Version:** 2.0
**Framework Version:** Antigravity Local Skill Standard

## Support & Documentation

- **Advanced User Guide:** `advanced-user-guide.md` — Power user features and automation
- **Troubleshooting:** `troubleshooting.md` — Common issues and solutions
- **Testing Checklist:** `qa/testing-checklist.md` — Validation procedures

For additional help, use `/help [command]` for command-specific documentation.