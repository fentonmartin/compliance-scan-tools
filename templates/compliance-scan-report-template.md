# COMPLIANCE SCAN REPORT

> Fill this template exclusively from evidence collected under
> `compliance/FULL-PROJECT-SCAN-METHODOLOGY.md`. Every finding needs
> file:line + commit + date + standard reference. Delete these
> instruction callouts before release.

## Document Control

| Field | Value |
|---|---|
| Document ID | SCAN-YYMMDD-NN |
| Version | 1.0 |
| Classification | <CLASSIFICATION> |
| Author | <OPERATOR> |
| Reviewed by | <REVIEWER> (human — required) |
| Approved by | <APPROVER> (human — required) |
| Scan date | <SCAN_DATE> |
| Commit (start) | <SCAN_START_COMMIT> |
| Commit (end) | <SCAN_END_COMMIT> |
| Repository | <TARGET_REPO_URL> |
| Branch | <TARGET_BRANCH> |
| Scope | <SCOPE_DIRS> (exclusions: <EXCLUDED_PATHS>) |
| Standards | <STANDARDS> |
| Scan type | <SCAN_TYPE> |
| Methodology version | compliance-scan-tools v1.0.0 (`compliance/FULL-PROJECT-SCAN-METHODOLOGY.md`) |

---

## 1. Executive Summary

<!-- Write last. 3–5 sentences: overall posture, critical gaps, immediate actions. -->

| Metric | Value |
|---|---|
| Total files scanned | N (tracked N + untracked N, at <SCAN_END_COMMIT>) |
| Commitments verified | N / N (IMPLEMENTED N, PARTIAL N, NOT FOUND N, UNCLEAR N) |
| Critical findings | N |
| High findings | N |
| Medium findings | N |
| Low findings | N |
| Informational observations | N |
| Compliance score | N / N commitments fully implemented |

---

## 2. Scope & Methodology

### 2.1 Scope

| In scope | Out of scope |
|---|---|
| <SCOPE_DIRS> (derived from `git ls-files` at <SCAN_END_COMMIT>) | <EXCLUDED_PATHS> + authority for each exclusion |

Depth: Full / Targeted (delete as applicable; if Targeted, state what was
left out and why).

Authorization: requested by <name>, on <date>, under <authority>.

### 2.2 Methodology

Six evidence phases per `compliance/FULL-PROJECT-SCAN-METHODOLOGY.md`
v1.0.0: 0 Authorization & scope → 1 Inventory → 2 Structure →
3 Commitment verification → 4 Security scan → 5 Docs coverage →
6 Data integrity (conditional) → 7 Reporting. Each phase met its exit
criteria (or the deviation is logged in Section 2.4).

### 2.3 Tools & Commands

| Tool | Version | Purpose |
|---|---|---|
| git | <version> | Version control, file inventory, evidence freezing |
| grep / ripgrep / Select-String | <version> | Pattern matching, code search |
| <other tool> | <version> | <purpose> |

Working directory and shell for every command are recorded in Appendix B.

### 2.4 Limitations

<!-- Critical for credibility. List everything NOT checked and why.
Examples: excluded secret paths, binary assets not inspected, DAST not run,
dependency audit tool unavailable, targeted scope. Never leave empty —
write "None beyond <EXCLUDED_PATHS>" only if true. -->

- …

---

## 3. Findings

### 3.1 Risk Rating Scale

| Rating | Definition | Action required |
|---|---|---|
| Critical | Direct compliance violation, data exposure, or security breach risk | Immediate remediation (within 24 hours) |
| High | Significant gap in compliance controls | Remediation within 7 days |
| Medium | Partial implementation or documentation gap | Remediation within 30 days |
| Low | Minor improvement opportunity | Next scheduled release |
| Informational | Observation, no immediate action required | Track and monitor |

### 3.2 Findings Summary

| ID | Rating | Title | Commitment / Standard | Status |
|---|---|---|---|---|
| F-001 | <rating> | <title> | <ID / standard ref> | Open |
| F-002 | <rating> | <title> | <ID / standard ref> | Open |

### 3.3 Detailed Findings

<!-- Copy this block per finding. Evidence is verbatim; impact and
recommendation are specific and actionable. -->

#### FINDING F-001: <Title>

| Field | Value |
|---|---|
| Rating | Critical / High / Medium / Low / Informational |
| Commitment reference | <ID from compliance/README.md, or "—" for general security findings> |
| Standard reference | <e.g. GDPR Art. 32 / ISO 27001 Annex A 8.24> |
| Evidence location | <path>:<line-range> or search scope + command |
| Commit | <SCAN_END_COMMIT> |
| Date discovered | <SCAN_DATE> |

**Description:**

<What was found, in plain language. Observation first, judgment second.>

**Evidence:**

```text
<Paste exact code, search results, or file contents. Redact live secret
values to the minimum excerpt proving the finding.>
```

**Impact:**

<What this means for compliance / security.>

**Recommendation:**

<Specific, actionable remediation step.>

**Owner:** <who should fix this>
**Target date:** YYYY-MM-DD

---

## 4. Compliance Matrix (Commitment Verification)

<!-- One row per in-scope commitment in compliance/README.md.
Status: ✅ Implemented | ⚠️ Partial | ❌ Not found | ❔ Unclear -->

| ID | Commitment | Status | Evidence | Gap |
|---|---|---|---|---|
| <ID> | <one-line commitment> | ✅/⚠️/❌/❔ | <path>:<lines> or search ref + commit | <gap or "None observed within scope"> |

---

## 5. Conclusion

<!-- Overall assessment: is the target compliant within the stated scope?
Biggest risks? What must be done first, by whom, by when? -->

---

## 6. Appendices

### Appendix A: Full Inventory

<!-- Paste Phase 1 INVENTORY REPORT verbatim. -->

### Appendix B: Search Commands & Results

<!-- Every command with working directory, shell, timestamp, and full
output (or output file reference). Include the evidence-freeze commands:
git rev-parse HEAD, git status --porcelain. -->

### Appendix C: Files Reviewed

<!-- Every file opened during the scan, with the phase that required it. -->

### Appendix D: Methodology Detail

<!-- Reference: compliance/FULL-PROJECT-SCAN-METHODOLOGY.md v1.0.0,
plus any per-engagement deviations with rationale. -->

---

## Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Scanner | <OPERATOR> | _____________ | <SCAN_DATE> |
| Reviewer | <REVIEWER> | _____________ | YYYY-MM-DD |
| Approver | <APPROVER> | _____________ | YYYY-MM-DD |

*No report is final without human reviewer and approver signatures.*
