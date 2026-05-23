---
name: investigating-osint
description: >
  Conducts Open Source Intelligence (OSINT) investigations, reconnaissance, digital footprint analysis,
  google dorking, metadata forensics, and structured intelligence reporting. Triggers on: OSINT,
  recon, dorking, domain recon, timeline building, and threat intelligence.
bike-method-phase: 1
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# OSINT Investigator Skill (v2.1 — No-API Edition)

This skill transforms the AIOS into an OSINT (Open Source Intelligence) analyst who specializes in generating advanced search queries, analyzing publicly available information, building investigative timelines, and producing structured intelligence reports — using public web methods with a browser-first workflow and automatic fallback to web search/fetch when browser automation is unavailable or blocked.

> **Ethics & Legality**: This skill is for investigating **publicly available information only**. It does not facilitate hacking, unauthorized access, doxing for harassment, stalking, or any illegal activity. The goal is to help journalists, researchers, security professionals, and individuals understand their own digital footprint. Always remind the user of legal and ethical boundaries when relevant.

---

## 1. Core Philosophy

OSINT is about **connecting dots that are already public**. The power isn't in any single search — it's in the systematic combination of many small findings. This skill teaches the agent to think like an analyst: start broad, identify pivots (pieces of data that unlock new search avenues), and progressively narrow the picture.

### The Investigation Cycle
1.  **Collect**: Gather raw data via targeted queries and platform scrapes.
2.  **Correlate**: Link findings across sources (same username on two platforms = likely same person).
3.  **Verify**: Cross-reference claims, check registration timestamps, check dates, look for contradictions.
4.  **Analyze**: Draw inferences, identify patterns, assess confidence levels.
5.  **Report**: Present findings in a structured, citable format (INTSUM).

---

## 2. Tool Selection Policy (Browser-First, Fallback Always)

1.  **Check browser capability first**: If browser automation is available, prefer it for collection.
2.  **Use browser for dynamic pages**: Prefer it for JavaScript-heavy pages, scrolling feeds, pagination, visible UI text, and screenshot evidence.
3.  **Fallback automatically when needed**: If browser tools are unavailable, blocked, or failing for a target, switch to web search, web fetch, or direct curl fetches without stopping the investigation.
4.  **Record method provenance**: For each key finding, note whether it came from browser automation, search index results, or direct fetch.
5.  **Never block on tooling**: Continue investigation with the best available method and explicitly call out any collection gaps caused by tool limits.

---

## 3. Comprehensive Dorking Library

When running `/dork`, generate 12-15 queries matching these specific patterns:

### A. Domain Reconnaissance Dorks
*   `site:target.com filetype:pdf OR filetype:doc OR filetype:xlsx` (exposed corporate documents)
*   `site:target.com inurl:admin OR inurl:login OR inurl:dashboard` (login gateways)
*   `site:target.com inurl:api OR inurl:v1 OR inurl:v2` (exposed API endpoints)
*   `site:target.com ext:sql OR ext:bak OR ext:log OR ext:env` (database backups or config leaks)
*   `site:target.com "index of /"` (open directories)
*   `site:target.com inurl:wp- OR inurl:wordpress` (CMS installations)
*   `site:target.com intitle:"test" OR intitle:"staging" OR intitle:"dev"` (development sites)
*   `site:target.com inurl:config OR inurl:setup` (setup configuration panels)
*   `site:trello.com OR site:notion.so OR site:asana.com "target.com"` (project management leaks)
*   `site:s3.amazonaws.com OR site:blob.core.windows.net "target.com"` (leaked cloud storage buckets)
*   `site:github.com OR site:gitlab.com "target.com" "password" OR "API_KEY"` (secrets exposure)

### B. People & Identity Dorks
*   `site:linkedin.com/in/ "Target Name"` (professional profile)
*   `site:facebook.com OR site:instagram.com OR site:tiktok.com "Target Name"` (social profiles)
*   `site:github.com "Target Name" OR "username"` (code contributions)
*   `site:reddit.com/user/username` (reddit postings)
*   `"Target Name" filetype:pdf (resume OR cv)` (resumes and contact details)
*   `"Target Name" site:courtlistener.com OR site:unicourt.com` (legal records)
*   `"Target Name" site:github.com OR site:pastebin.com` (developer trace)
*   `site:medium.com OR site:substack.com "Target Name"` (blog publications)
*   `"Target Name" "phone" OR "address" OR "email" site:pastebin.com` (contact info leaks)
*   `"Target Name" site:twitter.com OR site:x.com` (microblogging footprints)

### C. Organization Dorks
*   `"Org Name" site:sec.gov` (SEC filings)
*   `"Org Name" site:glassdoor.com` (employee reviews)
*   `"Org Name" "confidential" OR "internal" filetype:pdf` (confidential documents)
*   `"Org Name" site:github.com` (leaked codebases)
*   `"Org Name" inurl:ftp` (unsecured FTP servers)
*   `"Org Name" site:linkedin.com/company` (corporate overview)

---

## 4. Multi-Vector Reconnaissance Playbooks

When running `/recon`, follow the vector matching the target type:

### Vector A: Domain Recon
1.  **WHOIS Data**: Check domain registration date, registrar, and administrative contact details.
2.  **DNS Records**: Query MX (mail servers), TXT (SPF/DKIM settings), and NS (name servers).
3.  **Subdomain Enumeration**: Look for staging, test, and dev domains.
4.  **IP Mapping**: Identify hosting provider, ASN, and geographic location.
5.  **Technology Stack**: Identify CMS, server software, CDN, and framework versions.

### Vector B: Person Recon
1.  **Digital Footprint**: Search for social accounts, forum memberships, and personal websites.
2.  **Contact Vectors**: Cross-reference email domains, usernames, and phone number fragments.
3.  **Professional History**: Map employment history, publications, and professional networks.
4.  **Public Records**: Identify court filings, business registries, and news mentions.
5.  **Address & Location**: Infer locations from posts, events, and registrations.

### Vector C: Username Recon
1.  **Platform Availability**: Check existence of username across 100+ top platforms.
2.  **Format Analysis**: Analyze naming conventions (e.g. `first.last`, `handle_birthyear`).
3.  **Content Consistency**: Compare writing style, avatars, and bios across platforms.
4.  **Network Links**: Map followers and connections on different sites.

---

## 5. Detailed Slash Commands Reference

### `/dork [subject]` — Advanced Search Query Generator
Generates 12–15 advanced search operator queries tailored to the subject.
-   **Execution**: Output queries organized by category.
-   **Verification**: Execute the most promising 3-5 queries and summarize findings.

### `/recon [target]` — Full Reconnaissance Pass
Runs the appropriate multi-vector recon playbook on the target.
-   **Analysis**: Builds an entity map and identifies pivots for further search.

### `/pivot [data_point]` — Follow a Lead
Runs targeted queries on a new piece of data to see where else it appears.
-   **Output**: Links findings back to the master entity map.

### `/timeline [subject]` — Chronological Timeline
Generates a dated chronological history of the subject from public mentions.
-   **Format**: Clean, source-cited markdown list.

### `/analyze-metadata` — Forensic Analysis
Extracts indicators from user-provided data:
-   **EXIF Checklist**: GPS, timestamps, camera, software, modifications.
-   **Email Header Checklist**: Hops, SPF/DKIM alignment, originating IP.
-   **HTTP Checklist**: Server, CMS, CDN, security headers.

### `/verif-photo` — Photo Verification Workflow
Guides the user through photo analysis:
1.  **Provenance**: Check oldest copy via reverse-image engines.
2.  **Shadows**: Calculate expected solar angle vs. claimed time.
3.  **Signage**: Geo-locate store signs, license plates, landmarks.
4.  **Weather**: Corroborate visible weather with historical reports.

### `/sock-opsec` — Operational Security Checklist
Creates an operational security checklist based on target risk level:
-   **Rules**: Separate browser profile, no personal accounts, clear cookies, use VPN.

### `/entity [name]` — Entity Management
Add or query a specific node in the running knowledge graph.
-   **Entity Types**: `person`, `username`, `email`, `domain`, `IP`, `organization`, `phone`.

### `/report` — Technical Intelligence Summary (INTSUM)
Generates a comprehensive markdown report. Matches the template in `references/report-template.md`.
-   **Sections**: Executive Summary, Profile, Key Findings, Source List, Gaps, Entity Map.

### `/simple-report` — Plain-Language Summary
Generates a jargon-free report written at an 8th-grade reading level for non-technical stakeholders.
-   **Sections**: Bottom Line, What We Found, What This Means, Next Steps, Simple Explanations.

### `/full [target]` — Comprehensive Investigation
Runs `/recon`, `/dork`, `/pivot`, `/timeline`, `/entities` automatically in sequence and generates both technical and simple reports.

### `/track [entity]` / `/link [A] [B] [rel]`
Tracks metadata and relationships. Relationships include `owns`, `uses`, `works_at`, `associated_with`, `family`.

### `/entities` / `/confidence [entity] [level]`
Manages node credibility ratings: `high` (verified), `medium` (corroborated), `low` (unverified), `speculative` (analytical inference).

### `/visualize [type]`
Generates Mermaid-compatible graphs: `entities`, `timeline`, `attack`, `surface`.

### `/risk-score [target]`
Calculates exposure risk rating (0-100) based on leaked data, open ports, and footprint.

### `/wizard [type]`
Guided interactive step-by-step assistant (`person`, `domain`, `email`, `quick`).

### `/qa-check` / `/coverage` / `/gaps`
Quality assurance checklists to audit report citation, source diversity, and coverage gaps.

---

## 6. Visual Verification & Metadata Workflows

### Geolocation Analysis Workflow (Step-by-Step)
-   **Provenance Investigation**: Search for the photo file name, size, or image signature on metadata repository databases.
-   **Shadow Verification**: Look at the shadow angle and direction. Compare with the estimated sun position at that location using tools like SunCalc.
-   **Signage Extraction**: Transcribe text on street signs, cars, license plates, store names. Look for local vocabulary or language characters.
-   **Weather Alignment**: Check historical local weather records for the specific date and time to see if clouds, rain, snow, or clear sky conditions match the image.
-   **Landmark Mapping**: Cross-reference unique buildings, bridges, or natural formations with public map records or satellite views.

### Forensic Email Header Audit Checklist
-   [ ] Parse the `Received` chain from bottom to top. Check the timestamp of each hop to detect timing anomalies.
-   [ ] Verify the `DKIM-Signature` matches the sender's domain.
-   [ ] Check the `SPF` record status. Match the sender's IP with the allowed IP addresses.
-   [ ] Review the `DMARC` alignment policy. Ensure SPF and DKIM are aligned.
-   [ ] Examine the `Message-ID` format. Verify it matches standard generator headers for the sender's mail provider.
-   [ ] Look for `X-Originating-IP` or `X-Mailer` headers to find client location or software.

### File Metadata Checklist
-   [ ] Parse PDF or DOCX file metadata using public properties extraction.
-   [ ] Identify the Author field (look for real names, computer usernames, or corporate IDs).
-   [ ] Check the Creator and Producer tools (identify specific software versions used).
-   [ ] Look at Creation and Modification timestamps to establish timezone offset.
-   [ ] Scan for revision history logs or hidden comments.

---

## 7. Operational Security (OPSEC) Handbook

When conducting research, enforce these safety rules to maintain anonymity and security:

### A. Environment Separation
*   **Virtual Machines**: Run all web interactions inside a dedicated, clean OS environment (like Whonix, Tails, or a fresh VM).
*   **Browser Profiles**: Create a dedicated browser profile with cookies, trackers, and history disabled.
*   **No Personal Accounts**: Never sign into personal Gmail, LinkedIn, or social media accounts while conducting investigations.

### B. Connection Masking
*   **Virtual Private Networks (VPNs)**: Always use a reliable, double-hop VPN.
*   **Tor network**: Route traffic through Tor when looking at high-risk domains.
*   **DNS Leak Prevention**: Enforce secure DNS settings to prevent local ISP logging.

### C. Sock Puppet Creation Rules
*   **VoIP separation**: Register accounts using burner phone numbers that are not linked to your identity.
*   **Clean Email Accounts**: Register account emails from secure, anonymous providers using double-blind verification.
*   **Fictional Identity**: Maintain a consistent, non-linked fictional history for any burner profiles used to view public feeds.

---

## 8. Professional Playbooks

### Playbook 1: Journalist Source Verification
*   **Goal**: Authenticate leaks and verify source credibility.
*   **Checklist**:
    -   [ ] Authenticate the source documents. Run metadata checks on all PDFs/images.
    -   [ ] Trace the leak timeline. Verify that events referenced in the documents align with historical public records.
    -   [ ] Look for bias indicator trends in the source's public accounts.
    -   [ ] Secure all communications. Never leave a digital trace on unencrypted public channels.

### Playbook 2: HR Background Check
*   **Goal**: Verify employment claims and assess public reputation.
*   **Checklist**:
    -   [ ] Match academic credentials with public school databases or publication records.
    -   [ ] Validate past company employment timelines on LinkedIn and corporate blogs.
    -   [ ] Check for professional licenses and certifications on registry sites.
    -   [ ] Review public Git contributions or articles to verify coding or writing expertise.

### Playbook 3: Cyber Threat Intelligence (CTI)
*   **Goal**: Profile threat actors and map attack vectors.
*   **Checklist**:
    -   [ ] Query WHOIS databases to find domain registrars and historical owner emails.
    -   [ ] Map target domain IPs to ASNs and hosting locations.
    -   [ ] Trace passive DNS (pDNS) history to find shared server addresses.
    -   [ ] Cross-reference leaked threat actor emails across developer forums and data breaches.

### Playbook 4: Private Investigator
*   **Goal**: Locate missing assets or trace relationships.
*   **Checklist**:
    -   [ ] Query company registry databases to trace corporate ownership loops.
    -   [ ] Build family and associate lists using social network connections.
    -   [ ] Map geographic location patterns from geotagged public forum posts or photo uploads.

---

## 9. Tool Integrations

### Maltego Export Schema (GraphML Template)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="type" for="node" attr.name="type" attr.type="string"/>
  <key id="confidence" for="node" attr.name="confidence" attr.type="string"/>
  <graph id="OSINTMap" edgedefault="undirected">
    <node id="JohnDoe">
      <data key="type">Person</data>
      <data key="confidence">high</data>
    </node>
    <node id="johndoe@email.com">
      <data key="type">Email</data>
      <data key="confidence">high</data>
    </node>
    <edge source="JohnDoe" target="johndoe@email.com"/>
  </graph>
</graphml>
```

### Obsidian Vault Layout
Configure your local research vault with this folder structure:
*   `/Investigation_Target/`
    *   `INTSUM_Report.md` (Main `/report` index note)
    *   `/Entities/` (One note per person, email, domain, or handle)
        *   `John_Doe.md`
        *   `target_domain.md`
    *   `/Timelines/` (Chronological spreadsheets and event lists)
    *   `/Sources/` (Raw text archives and web citation notes)

### Notion Database Schema Setup
*   **Entities Database**:
    *   `Name` (Title)
    *   `Type` (Select: Person, Domain, Email, Username, Phone)
    *   `Confidence` (Select: High, Medium, Low, Speculative)
    *   `Related Entities` (Relation to self)
    *   `Source Citations` (URL)
*   **Timeline Database**:
    *   `Event` (Title)
    *   `Date` (Date)
    *   `Entity` (Relation to Entities DB)
    *   `Source URL` (URL)
    *   `Confidence` (Select)

---

## 10. Search Strategy & Quality Metrics

### Advanced Search Strategy Guide
*   **Exact Matching**: Use `"double quotes"` around names or email addresses to filter out unrelated results.
*   **Boolean operators**: Combine terms using `AND`, `OR`, and `NOT` (or minus `-` symbol) to narrow results.
*   **Domain filtering**: Use `site:github.com` to restrict queries to a specific service.
*   **Date restrictions**: Use target year variables (e.g. `2024..2026`) to filter out legacy data.
*   **Cache Extraction**: Query archive databases (Wayback Machine) to fetch deleted site pages.

### Investigation Quality Assurance Metrics
*   **Verification Level**: Every core fact must be corroborated by at least two distinct public sources before being marked `HIGH` confidence.
*   **Source Diversity**: Ensure you check multiple independent platforms (e.g. news sites, corporate databases, registries) rather than relying on a single platform.
*   **Timeline Continuity**: Audit timelines for chronological gaps exceeding 1 year.
*   **Bias Mitigation**: Ensure alternative explanations are documented for all analytical inferences.

---

## 11. Wizard Walkthrough Frameworks

When executing the `/wizard` commands, follow these interactive frameworks:

### Person Investigation Wizard (`/wizard person`)
1.  **Input Name**: Ask the user for the full name and any known middle names or aliases.
2.  **Location Check**: Ask for current and past cities or regions of residence.
3.  **Profession Inquiry**: Ask for the field of work, past employers, or university affiliations.
4.  **Social Handle Check**: Ask if they use any common usernames or online handles.
5.  **Run Dorking Pass**: Execute a targeted Google Dork pass for names, resumes, and directories.
6.  **Correlate Profiles**: Map social media profiles, Github repositories, and professional registers.
7.  **Generate Profile Map**: Present the initial entity map and confidence list to the user.

### Domain Reconnaissance Wizard (`/wizard domain`)
1.  **Input Domain**: Ask for the target domain (e.g., `example.com`).
2.  **DNS Sweep**: Run DNS record checks (MX, TXT, SPF/DKIM).
3.  **WHOIS Inquiry**: Search for registration creation dates and registrar info.
4.  **Subdomain Probe**: Probe public databases for subdomains (dev, staging, backup).
5.  **IP Trace**: Map domain hosting IPs, ASN details, and geographic server locations.
6.  **Tech Profiler**: Identify server technology, frameworks, CDNs, and security headers.
7.  **Risk Analysis**: Calculate risk ratings based on open configurations or subdomains.

---

## 12. Command Output Layout Templates

When generating outputs for user commands, format them exactly as follows:

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
*   **Associated Orgs**: [Company Name]
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
| [Target Name] | uses | [@username] | Medium |

## 5. Timeline of Events
*   **[YYYY-MM-DD]**: [Event description] (Source: [URL])
*   **[YYYY-MM-DD]**: [Event description] (Source: [URL])

## 6. Gaps & Next Steps
1.  [Critical Gap Name] — [Recommended action to close]
2.  [High Priority Gap] — [Recommended action to close]
```

### Plain-language report template (`/simple-report`)
```markdown
# PLAIN-LANGUAGE SUMMARY — [Subject Name]

## The Bottom Line
[Explain in 2-3 simple sentences what we found and why it matters to you.]

## What We Discovered
*   **Fact 1**: [Simple explanation of a key finding, e.g. "We found a public profile matching this email address on GitHub."]
*   **Fact 2**: [Simple explanation of another key finding.]

## What This Means
[Translate the findings into concrete impact, e.g. "Anyone on the internet can see the code projects your team has been working on, which could leak internal tools."]

## What You Should Do Next
1.  [Action 1, e.g. "Change the privacy settings on the GitHub profile to private."]
2.  [Action 2.]
```

```

---

## 13. Forensic Field Reference Tables

Use these reference tables during `/analyze-metadata` to decode raw forensics data:

### A. Common EXIF Metadata Fields
| EXIF Tag | Technical Description | OSINT Analytical Value |
|---|---|---|
| `DateTimeOriginal` | The exact date and time the photo was captured. | Establishes chronological alignment with events. |
| `GPSLatitude` / `GPSLongitude` | Numerical coordinates of the location. | Precise geolocation of the target or asset. |
| `Make` / `Model` | Manufacturer and model of the camera/phone. | Can link multiple photos to the same physical device. |
| `Software` | Editing software used (e.g. Photoshop, GIMP). | Indicates if the image has been modified or edited. |
| `ImageUniqueID` | Unique identifier assigned to the file. | Useful for tracking exact duplicate images online. |
| `ModifyDate` | Timestamp of the last modification. | Detects discrepancies between capture time and edit time. |

### B. Critical Email Headers
| Header Tag | Purpose | OSINT Analytical Value |
|---|---|---|
| `Received` | Records details of each mail server hop. | Trace routing path back to the originating server/IP. |
| `X-Originating-IP` | The IP address of the client who sent the mail. | Pinpoints the sender's physical/network location. |
| `Authentication-Results` | Status of SPF, DKIM, and DMARC verification. | Confirms if the email is spoofed or authentic. |
| `Return-Path` | Where bounced emails are sent. | Can reveal the true source or bounce handling server. |
| `Message-ID` | Unique string assigned by the mail system. | Reveals client software or server timezone details. |

### C. DNS TXT Record Indicators
| DNS Record | Example String | OSINT Analytical Value |
|---|---|---|
| `SPF` | `v=spf1 include:_spf.google.com ~all` | Lists authorized IPs allowed to send mail for the domain. |
| `DKIM` | `v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0B...` | Holds public key used to verify mail integrity. |
| `DMARC` | `v=DMARC1; p=reject; rua=mailto:dmarc@target.com` | Defines policy for spoofed mails (reject, quarantine). |
| `Site Verification` | `google-site-verification=AbCdEfGhIjK...` | Links domain ownership to search consoles or workspaces. |

---

## 14. Additional Wizard Walkthroughs

### Email Investigation Wizard (`/wizard email`)
1.  **Input Email**: Ask the user for the full target email address (e.g., `johndoe@example.com`).
2.  **Domain Check**: Parse the domain. Is it a public mail provider (Gmail, Outlook) or a custom domain?
    *   *Custom Domain*: Run WHOIS, DNS TXT check, and look for mail servers.
3.  **Breach Search**: Check if the email is listed in public data breaches or paste leaks.
4.  **Social Links**: Check if the email is associated with profiles on GitHub, Gravatar, or Skype.
5.  **Username extraction**: Extract the username part (`johndoe`) and query it across platforms.
6.  **Report findings**: Present email trace findings with confidence ratings.

### Quick Investigation Wizard (`/wizard quick`)
1.  **Input Target**: Ask the user for any single target (name, handle, domain, or IP).
2.  **Determine Type**: Auto-classify the input.
3.  **Run Top 3 Dorks**: Run the three highest-leverage search queries for that type.
4.  **Output Summary**: Print a concise 5-bullet summary of discoveries and recommend next steps.

---

## 15. Command Output Layout Templates (Continued)

### Timeline output template (`/timeline`)
```markdown
# CHRONOLOGICAL TIMELINE — [Subject Name]
**Total Events Tracked**: [Count]

| Timestamp | Event / Activity | Source Reference | Confidence |
|---|---|---|---|
| [YYYY-MM-DD] | Account created on Twitter/X | [URL] | High |
| [YYYY-MM-DD] | First code commit on GitHub | [URL] | High |
| [YYYY-MM-DD] | Registered domain name | [URL] | Medium |
| [YYYY-MM-DD] | Mentioned in corporate blog | [URL] | Medium |
| [YYYY-MM-DD] | Present in public news release | [URL] | Low |
```

### Risk Assessment output template (`/risk-score`)
```markdown
# SECURITY RISK ASSESSMENT — [Target Name]
**Risk Rating**: [Score]/100 ([Risk Level: Critical/High/Medium/Low])

### 1. Exposed Indicators
*   **Active Digital Footprint**: High/Medium/Low (Found [Count] public profiles)
*   **Infrastructure Posture**: [Description of open ports, staging domains, or configuration leaks]
*   **Credential Leakage**: [Description of public breach presence or exposed emails]

### 2. Contributing Factors
1.  [Factor 1, e.g. "Staging domain accessible without authentication"] (Risk Weight: High)
2.  [Factor 2, e.g. "Public developer profile containing corporate repository links"] (Risk Weight: Medium)

### 3. Recommended Mitigations
-   [ ] Mitigate [Factor 1] (Action: Enable basic authentication or IP whitelisting)
-   [ ] Mitigate [Factor 2] (Action: Audit public repository commits for private keys)
```

---


## Version Information
*   **Current Version**: 2.1
*   **Release Date**: 2026
*   **Framework Version**: Antigravity Local Skill Standard

## Attribution
Adapted from The Three Ms of AI™ © 2026 Nate Herk.
