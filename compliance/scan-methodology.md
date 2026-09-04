---
type: topic
title: Full Project Scan — Evidence-Based Audit Methodology
status: active
version: 1.1.0
claim_type: reference
subtype: reference
updated: 2026-09-04
sources: [compliance/adr-compliance-matrix.md, compliance/references/]
---

# Full Project Scan — Evidence-Based Audit Methodology

> **Design rule: this document contains zero project-specific values.**
> Every target-specific value is a `<PLACEHOLDER>` listed in Section 1.
> If you find a hard-coded repo name, directory, tenant, region, or
> product name in this file, treat it as a bug and fix it before scanning.

## Table of contents

1. [How to use this document (copy-paste agent)](#1-how-to-use-this-document-copy-paste-agent)
2. [What and why](#2-what-and-why)
3. [Document control (required on every report)](#3-document-control-required-on-every-report)
4. [The evidence principle](#4-the-evidence-principle)
5. [Scan protocol](#5-scan-protocol)
    - [Phase 0 — Scope definition & authorization](#phase-0--scope-definition--authorization)
    - [Phase 1 — Inventory (what exists)](#phase-1--inventory-what-exists)
    - [Phase 2 — Structure analysis (architecture from disk)](#phase-2--structure-analysis-architecture-from-disk)
    - [Phase 3 — Compliance verification (commitments vs implementation)](#phase-3--compliance-verification-commitments-vs-implementation)
    - [Phase 4 — Security scan](#phase-4--security-scan)
    - [Phase 5 — Documentation coverage](#phase-5--documentation-coverage)
    - [Phase 6 — Data integrity (conditional)](#phase-6--data-integrity-conditional)
    - [Phase 7 — Reporting](#phase-7--reporting)
6. [Report template](#6-report-template)
7. [Rules for the scanner](#7-rules-for-the-scanner)
8. [Search pattern library](#8-search-pattern-library)
9. [Cross-platform notes](#9-cross-platform-notes)
10. [References](#10-references)

---

## 1. How to use this document (copy-paste agent)

This methodology is designed to be pasted into any AI coding agent
as its operating instruction for auditing an arbitrary target repository.

### 1.1 Fill in the variables first

Before the scan starts, the operator **MUST** fill in every variable.
There are no defaults for target-specific fields.

| Variable | Meaning | Example |
|---|---|---|
| `<TARGET_REPO_URL>` | Clone URL or repo identifier of the system under audit | `https://github.com/<org>/<repo>.git` |
| `<TARGET_BRANCH>` | Branch under audit | `main` |
| `<SCAN_START_COMMIT>` | Commit hash when the scan starts (`git rev-parse HEAD`) | `a1b2c3d…` |
| `<SCAN_END_COMMIT>` | Commit hash when evidence collection ends | `e4f5g6h…` |
| `<SCOPE_DIRS>` | Directories in scope, discovered from the repo itself | `./src ./internal ./docs` (see Phase 0) |
| `<EXCLUDED_PATHS>` | Paths the scanner must not open (secrets, keys, PII dumps) | `.env* *.pem *.key secrets/` |
| `<STANDARDS>` | Compliance frameworks in scope for this engagement | `ISO 27001:2022, GDPR, UU PDP No. 27/2022` |
| `<CLASSIFICATION>` | Handling caveat for the report | `Confidential` |
| `<SCAN_TYPE>` | One of: Initial / Periodic / Incident-triggered / Change-triggered | `Initial` |
| `<OPERATOR>` | Human or agent identity running the scan | `AI Agent — <agent-name>` |
| `<REVIEWER>` | Human reviewer name (mandatory before release) | `<full name>` |
| `<APPROVER>` | Human approver name (mandatory before release) | `<full name>` |
| `<SCAN_DATE>` | Evidence freeze date, `YYYY-MM-DD` | `2026-09-04` |
| `<EVIDENCE_DIR>` | Directory holding machine-generated evidence (`cscan` output + receipts), stored outside the target tree | `./.evidence/SCAN-260904-01/` |

### 1.2 Invoke the agent

Paste the following block (with variables filled in) together with
this methodology file:

```text
You are a compliance scan agent. Follow the methodology in
compliance/scan-methodology.md exactly.
Verify the commitments in compliance/adr-compliance-matrix.md against the code.

Variables:
- Target repo: <TARGET_REPO_URL> (branch <TARGET_BRANCH>)
- Scope: <SCOPE_DIRS> | Exclusions: <EXCLUDED_PATHS>
- Standards: <STANDARDS> | Type: <SCAN_TYPE> | Date: <SCAN_DATE>
- Operator: <OPERATOR> | Reviewer: <REVIEWER> | Approver: <APPROVER>

Rules: evidence for every claim (file:line + commit hash),
negative results are findings, quote don't paraphrase,
never fabricate, stop and report limits honestly.
Preferred instrument: tools/cscan.py (freeze/inventory/search/scaffold/validate)
— attach its JSON outputs and receipts.json in Appendix B.
Deliver the report using templates/compliance-scan-report-template.md.
```

### 1.3 Exit criteria

The scan is done when **all** of these hold:

- [ ] Phase 0 scope table is filled and authorized.
- [ ] Phase 1 inventory counts reconcile with `git ls-files`.
- [ ] Every in-scope commitment in `compliance/adr-compliance-matrix.md` has a
      Phase 3 verdict of IMPLEMENTED / PARTIAL / NOT FOUND / UNCLEAR
      with dated evidence.
- [ ] Every Phase 4 check has either evidence or an explicit
      "not searched because …" statement.
- [ ] The report validates: no hard-coded prior-engagement values,
      every finding has file:line + commit + date + standard reference.
- [ ] A human reviewer and approver are named in Document Control.

---

## 2. What and why

A standard methodology for scanning an arbitrary software project that
produces a **compliance audit report** — a document defensible before an
internal auditor, an external auditor, or a regulator. Every finding
traces to concrete evidence; every piece of evidence traces to an
immutable version-control commit.

An ordinary scan report is useful to the team. A compliance audit report
is useful in front of an ISO 27001 auditor or a data-protection
regulator asking "where is the evidence?" The difference is
**document control, chain of evidence, and formal sign-off.**

This methodology is intentionally project-agnostic:

- It never names a product, tenant, customer, region, or repository.
- It never assumes a language, framework, or directory layout.
  Directory lists in examples are illustrative and marked as such.
- Normative commitments (what "should" hold) live in
  `compliance/adr-compliance-matrix.md`. This file defines *how to verify them*.

---

## 3. Document control (required on every report)

Every audit report **MUST** open with this control table. Without it,
the report carries no authority. Copy it from
`templates/compliance-scan-report-template.md` — do not retype it.

```markdown
| Field | Value |
|---|---|
| Document ID | SCAN-[YYMMDD]-[seq] (e.g. SCAN-260904-01) |
| Version | 1.0 |
| Classification | <CLASSIFICATION> |
| Author | <OPERATOR> |
| Reviewed by | <REVIEWER> — required, must be human |
| Approved by | <APPROVER> — required, must be human |
| Date of scan | <SCAN_DATE> |
| Commit hash (scan start) | <SCAN_START_COMMIT> |
| Commit hash (scan end) | <SCAN_END_COMMIT> |
| Repository | <TARGET_REPO_URL> |
| Branch | <TARGET_BRANCH> |
| Scope | Full project scan (<SCOPE_DIRS>) |
| Standards | <STANDARDS> |
| Scan type | <SCAN_TYPE> |
```

**Why commit hashes are mandatory:** the report freezes evidence at a
point in time. Without hashes, anyone can correctly object that "the
code changed since the scan." The hashes prove exactly which code was
examined. If the working tree is dirty at scan start, record that fact
and the output of `git status --porcelain` in Appendix B.

---

## 4. The evidence principle

```text
IF you claim something EXISTS      → cite the file, line range, AND commit hash
IF you claim something NOT EXISTS  → list where you searched, what you found, AND the exact search command
IF you DID NOT SEARCH              → say so explicitly; do not guess either way
```

### Rules for evidence

1. **Every finding must have a traceable evidence record.** Format:

   ```text
   [FINDING-001] Title
   Evidence: <path>:<line-range> OR <search command → results>
   Commit: <SCAN_END_COMMIT>
   Date: <SCAN_DATE>
   Standard reference: <e.g. GDPR Art. 32 / ISO 27001 Annex A 8.24 / UU PDP Art. 35>
   ```

2. **Negative results are findings.** "No authorization middleware
   found after searching `<SCOPE_DIRS>` with patterns X, Y, Z" is
   valuable evidence of a gap — provided the search is documented.

3. **Quote, don't paraphrase.** Reproduce the code or the search
   output. Summaries follow quotations; they never replace them.

4. **Timestamp everything.** Code changes; evidence is frozen at the
   commit hash plus `<SCAN_DATE>`.

5. **Separate observation from judgment.** "`auth.py` has 500 lines"
   is observation. "`auth.py` is too long" is judgment. Record the
   observation first, then the judgment if needed.

6. **Never assert absence without exhaustive search.** Before writing
   "feature X is not implemented," document:
   - all directories traversed (must be within `<SCOPE_DIRS>`);
   - all file extensions covered;
   - all patterns tried (exact strings);
   - all configuration files checked;
   - all entry points reviewed (if applicable).

### The existence protocol (do not assume — collect evidence)

Every verdict about the target is exactly one of three states. There is
no fourth state ("probably", "likely", "assumed"). The scanner's job is
to move claims out of UNCLEAR by collecting evidence, not by reasoning
about what "must" be there.

| Verdict | Meaning | Minimum proof required |
|---|---|---|
| IMPLEMENTED / EXISTS | The behavior or artifact is present in the target at `<SCAN_END_COMMIT>` | Direct observation: quoted file content with `<path>:<line-range>` + commit + date. One sighting is enough — but cite the strongest (enforcement point, not a comment mentioning it). |
| NOT FOUND / ABSENT | The behavior or artifact is absent from the search scope | A **search receipt**: every pattern tried (exact strings), every directory traversed with file/extension counts, the exact command + working directory + tool version, timestamp, exclusions honored, and the 0-match result. Absence is proven by the receipt, never by silence. |
| UNCLEAR / NOT SEARCHED | No verdict is possible yet | An explicit statement of what was not searched and why (tool missing, path excluded, binary asset, time-box hit). UNCLEAR is a valid, reportable outcome. Guessing in either direction is a failed scan. |

Rules:

1. **Comments, docs, and names are not implementations.** A code comment
   saying "encrypts data", a README promising MFA, or a function named
   `deleteUser` is a *lead*, not evidence. Follow the lead to the
   enforcement point (the code path that actually executes) and quote that.
2. **One positive sighting does not prove coverage.** Finding auth on one
   route does not prove "all routes require auth" — that universal claim
   needs an exhaustive route-table review (list every route + verdict) or
   it stays PARTIAL/UNCLEAR.
3. **One pattern is not an exhaustive search.** A NOT FOUND for "erasure"
   after grepping a single keyword is UNCLEAR, not NOT FOUND. The pattern
   library (Section 8) gives starting sets; extend them from Phase 2
   observations (framework idioms, ORM names, queue/topic names) and record
   every extension in the receipt.
4. **Excluded paths are UNCLEAR, never NOT FOUND.** Anything under
   `<EXCLUDED_PATHS>` was not opened, so no claim — positive or negative —
   may rest on it. Name the exclusion and escalate per engagement rules.
5. **Machine receipts beat memory.** `cscan search` writes per-group
   receipts (`receipts.json`: command, cwd, timestamps, file universe,
   files searched/skipped, match counts). Paste them into Appendix B.
   A finding whose receipt is missing is UNCLEAR until the search is
   re-run and recorded.

---

## 5. Scan protocol

Seven phases, in order. Do not skip a phase because "it's probably
fine." The purpose of the protocol is to replace "probably" with
"verified." Record Phase 0–1 output even when the repo looks trivial —
that record is what makes a clean report credible.

### Phase 0 — Scope definition & authorization

Before opening any source file, fill in and freeze:

| Field | Required | Value |
|---|---|---|
| Scan scope | Yes | `<SCOPE_DIRS>` — enumerate from `git ls-files`, see Phase 1. Do not invent directory names. |
| Exclusions | Yes | `<EXCLUDED_PATHS>` — secret/key material, credential dumps, PII fixtures the engagement rules forbid opening. Name the rule source (e.g. engagement letter, security policy). |
| Depth | Yes | Full (every tracked file) or Targeted (named subsystems + rationale) |
| Scan type | Yes | `<SCAN_TYPE>` |
| Authorization | Yes | Who requested this scan, when, and under what authority |
| Standards referenced | Yes | `<STANDARDS>` |

**Exit criteria:** the table is complete; exclusions have a stated
authority; any targeted (non-full) scope states what was left out and why.

> Anti-hard-coding check: if `<SCOPE_DIRS>` contains a directory that
> does not exist in the target repo, stop — you copied scope from a
> previous engagement. Re-derive it from Phase 1.

### Phase 1 — Inventory (what exists)

**Goal:** a complete, verifiable map of every file in the target project.

Preferred instrument: `cscan freeze` + `cscan inventory --target <path>
--out <EVIDENCE_DIR>/01-inventory` (writes tracked/untracked lists,
counts, and summary JSON). The commands below are the manual equivalent —
Appendix B must record whichever actually ran.

Discover scope from the repo itself. Illustrative commands (run against
the *target* checkout; adapt flags to the local shell — see Section 9):

```bash
# Freeze the evidence point
git rev-parse HEAD
git status --porcelain

# All tracked files
git ls-files > /tmp/inventory-tracked.txt
wc -l /tmp/inventory-tracked.txt

# Untracked files (potential secrets or unauthorized additions)
git ls-files --others --exclude-standard > /tmp/inventory-untracked.txt
wc -l /tmp/inventory-untracked.txt

# Files by extension
git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Files by top-level directory (derive <SCOPE_DIRS> from this, don't assume it)
git ls-files | cut -d'/' -f1 | sort | uniq -c | sort -rn

# Large files (>100KB) — candidates for generated artifacts / checked-in dumps
git ls-files -z | xargs -0 ls -la 2>/dev/null | awk '$5 > 100000 {print}'
```

> Never open a file matching `<EXCLUDED_PATHS>` to "check whether it's
> a secret." List its name, size, and tracking status only, and escalate
> per the engagement rules.

**Report output** (paste into Appendix A):

```text
INVENTORY REPORT
================
Scan date: <SCAN_DATE>
Commit: <SCAN_END_COMMIT>
Total tracked files: N
Total untracked files: N

By top-level directory:            (derived, not assumed)
| Directory   | Files | Total lines | Largest file |
|-------------|-------|-------------|--------------|
| <dir>       | N     | N           | N bytes      |

Anomalies:
- [empty files: list]
- [files >1MB: list]
- [untracked files: list with reason sought]
- [unexpected extensions: list]
```

**Exit criteria:** total counts reconcile with `git ls-files`;
`<SCOPE_DIRS>` matches observed top-level directories; anomalies are
listed or explicitly marked "none."

### Phase 2 — Structure analysis (architecture from disk)

**Goal:** document the *actual* architecture, not the assumed one.

For each directory in `<SCOPE_DIRS>`, record:

| Aspect | Evidence required |
|---|---|
| Purpose | The directory's own README/config, or "no self-description found at `<path>`" |
| Key files | List with one-line descriptions grounded in file content |
| Entry points | Main files, route tables, CLI definitions, job schedules — with file:line |
| Dependencies | Manifests actually present (`package.json`, `go.mod`, `requirements.txt`, `Cargo.toml`, …) — do not assume a stack |
| Configuration | Config files present and env vars referenced (names only; never print values) |

**Do not guess from file names.** Open the file. If the file does not
explain itself, write "no self-description found" — that sentence is
evidence, not failure.

**Exit criteria:** every `<SCOPE_DIRS>` entry has a row; every claim
has a file:line or an explicit "not found" note.

### Phase 3 — Compliance verification (commitments vs implementation)

**Goal:** for every normative commitment in `compliance/adr-compliance-matrix.md`
(ADR matrix), find the implementation in the target code — or prove its
absence with a documented search.

This is the most critical phase for compliance evidence.

For **each** commitment record in `compliance/adr-compliance-matrix.md`, produce:

```markdown
#### <ID>: [Commitment name]

| Field | Value |
|---|---|
| ID | <ID> |
| Commitment | [one-line description from the matrix] |
| Severity if absent | [Critical / High / Medium / Low — per report template scale] |
| Standards | [e.g. GDPR Art. 32, ISO 27001 Annex A 8.24] |

**Implementation status:** IMPLEMENTED / PARTIAL / NOT FOUND / UNCLEAR

**Evidence:**
| # | What was checked | Where | Result |
|---|---|---|---|
| 1 | [specific search] | [<path>:<lines> or "not found in <SCOPE_DIRS>"] | [what was found] |
| 2 | [specific search] | [<path>:<lines> or "not found in <SCOPE_DIRS>"] | [what was found] |

**Search methodology:**
- Command: `[exact command used, with working directory]`
- Files searched: [count + extensions + directories — all within <SCOPE_DIRS>]
- Date: <SCAN_DATE>
- Commit: <SCAN_END_COMMIT>

**Gaps identified:**
- [partial implementations or missing pieces, or "none observed within scope"]

**Conclusion:** [one paragraph: verdict + confidence level + what would raise confidence]
```

**Evidence format examples** (paths below are illustrative only —
use paths observed in the target repo):

```text
IMPLEMENTED:
  Evidence: <path-to-auth-middleware>:<line-range>
  Commit: <SCAN_END_COMMIT>
  Date: <SCAN_DATE>
  Code: [paste the relevant block verbatim]

NOT FOUND:
  Searched for: 'DSAR', 'data_subject_access', 'erasure_request', 'right_to_delete'
  Directories: <SCOPE_DIRS subset actually traversed>
  Files checked: N files (<extensions>)
  Command: [exact grep/rg command with working directory]
  Result: 0 matches
  Commit: <SCAN_END_COMMIT>
  Date: <SCAN_DATE>
```

Map each verdict to a finding in the report (Section 6) with a severity
per the Risk Rating Scale. A PARTIAL implementation is a finding, not a pass.

**Exit criteria:** every in-scope matrix row has a verdict block;
every NOT FOUND names the exact patterns and scope searched.

### Phase 4 — Security scan

Run each check against `<SCOPE_DIRS>`, respecting `<EXCLUDED_PATHS>`.
Record the exact command, its working directory, and either
file:line hits with surrounding context or an explicit "0 matches."

Preferred instrument: `cscan search --target <path> --out
<EVIDENCE_DIR>/02-search --exclude '<pattern>'` (repeat `--exclude` per
excluded path; writes `<group>.txt` hits plus `receipts.json`). `cscan`
never opens excluded paths — it records their names only.

| # | Check | Method (adapt to shell; Section 9) | Evidence format |
|---|---|---|---|
| 4.1 | Secrets in code | Pattern search for `password\|secret\|api_key\|token\|credential` across code/config extensions present in the repo | file:line of every match + context; never reproduce live secret *values* beyond what is needed to prove the finding — prefer redacted excerpts + entropy/location metadata |
| 4.2 | Secret files tracked | `git ls-files \| grep -iE 'env\|pem\|key\|secret\|credential'` | List of hits or explicit "none" |
| 4.3 | Credential/tabular dumps | Inspect column headers of checked-in CSV/Excel fixtures (headers only) | Column names + whether cells appear populated (yes/no, no values) |
| 4.4 | Hardcoded endpoints | Pattern search for `https?://` and IPv4 literals | file:line; distinguish public docs URLs from internal/service endpoints |
| 4.5 | CORS / security headers | Pattern search for `Access-Control\|Content-Security-Policy\|Strict-Transport-Security\|X-Frame-Options` | file:line or documented absence with search scope |
| 4.6 | Dependency risk surface | Read manifests actually present; report lockfile presence/absence and known-audit tooling (`npm audit`, `pip audit`, `cargo audit`, `govulncheck`, …) if run | Manifest paths + tool output or "tool not run because …" |
| 4.7 | AuthN/Z surface | Pattern search for `auth\|login\|session\|jwt\|bearer\|permission\|role\|policy` scoped to entry points from Phase 2 | file:line map of enforcement points, or gap finding |

If a check cannot be run (tool missing, scope excluded, binary asset),
record it under report Section 2.4 (Limitations) — never silently drop it.

**Exit criteria:** all seven rows have evidence or a limitations entry.

### Phase 5 — Documentation coverage

| Check | Method | Evidence |
|---|---|---|
| Code without docs | For each implemented subsystem in `<SCOPE_DIRS>`, check the target's own docs tree for coverage | List of undocumented subsystems (paths) |
| Docs without code | For each feature the target's docs promise, check `<SCOPE_DIRS>` for implementation | List of unimplemented documented features |
| Commitments without implementation | Cross-reference `compliance/adr-compliance-matrix.md` verdicts from Phase 3 | List of NOT FOUND / PARTIAL IDs |

**Exit criteria:** the three lists exist (possibly "none observed").

### Phase 6 — Data integrity (conditional)

Run this phase **only** if the target repo checks in tabular, fixture,
or seed data (CSV/JSON/SQL/Excel). Otherwise record
"Phase 6 not applicable — no tabular fixtures observed in
`<SCOPE_DIRS>` at `<SCAN_END_COMMIT>`" and move on. Never invent directory names to satisfy this phase.

| Check | Method | Evidence |
|---|---|---|
| Row counts | Line/object counts per fixture file | File → count |
| Referential integrity | Spot-check foreign-key-style columns against referenced files | Broken references found (file:line) or "none in sample of N" |
| Placeholder vs real data | Pattern search for `test\|dummy\|placeholder\|example\|synthetic` + header inspection | Files containing placeholder markers |
| Date ranges | First/last records per time-ordered fixture | Range per file |

**Exit criteria:** applicability statement present; if applicable, the
four rows have evidence.

### Phase 7 — Reporting

Assemble the report **exclusively** from `templates/compliance-scan-report-template.md`:

1. Fill Document Control from Section 3 (no empty fields except
   signatures, which are wet/digital-sign applied outside the file).
2. Write the Executive Summary last (3–5 sentences + metrics table).
3. Promote every Phase 3 PARTIAL / NOT FOUND and every Phase 4 hit
   to a numbered finding (F-001…) with severity, impact,
   recommendation, owner, and target date.
4. Include the full commitment-verification matrix (one row per
   in-scope commitment ID).
5. Append Appendices A–D from phase outputs (inventory, commands +
   full output, files reviewed, methodology reference).
6. Run the pre-release self-check (mechanically assisted by
   `cscan validate --report <report>`, which fails on unfilled
   placeholders, incomplete FINDING blocks, missing Document Control
   fields, and prior-engagement token leakage):
   - [ ] No prior-engagement names, URLs, directories, or model names remain.
   - [ ] Every finding has evidence location + commit + date + standard ref.
   - [ ] Limitations (Section 2.4) lists everything not checked and why.
   - [ ] Reviewer and approver are named humans.

---

## 6. Report template

The normative template lives at
`templates/compliance-scan-report-template.md` and is summarized here.
If the two disagree, the `templates/` file governs and this section
must be updated to match.

Required sections: Document Control → Executive Summary (with metrics:
files scanned, commitments verified N/N, findings by severity,
compliance score) → Scope & Methodology (scope table, tools table,
limitations) → Findings (rating scale, summary table, detailed
F-001… records with Description / Evidence / Impact / Recommendation /
Owner / Target date) → Commitment-verification matrix → Conclusion →
Appendices (A: inventory, B: commands+results, C: files reviewed,
D: methodology reference) → Sign-off table.

Severity scale (binding):

| Rating | Definition | Action required |
|---|---|---|
| Critical | Direct compliance violation, data exposure, or breach risk | Immediate remediation (within 24 hours) |
| High | Significant gap in compliance controls | Remediation within 7 days |
| Medium | Partial implementation or documentation gap | Remediation within 30 days |
| Low | Minor improvement opportunity | Next scheduled release |
| Informational | Observation, no immediate action required | Track and monitor |

---

## 7. Rules for the scanner

1. **Every finding must have evidence.** No file:line (or documented
   exhaustive search) → hypothesis, not a finding. Label it as such.
2. **Negative results are findings.** "Not found after searching X, Y,
   Z" is reportable — with the search attached.
3. **Never skip a phase because "it's probably fine."** The protocol
   replaces assumption with verification.
4. **Search breadth before depth.** Inventory first, then specifics.
5. **Quote, don't paraphrase.** Show the code and the search output.
6. **Timestamp everything.** "As of `<SCAN_DATE>`, at commit
   `<SCAN_END_COMMIT>`, this code at these lines."
7. **Separate observation from judgment.**
8. **Never fabricate evidence.** Unopened files are never cited;
   unrun commands never report results.
9. **Preserve the chain.** Every finding links:
   file:line → commit hash → scan date → report section.
10. **Human review is mandatory.** No report is final without a named
    human reviewer and approver.
11. **No hard-coded engagement values.** Repo names, directory names,
    regions, tenants, product names, and model names appear only as
    `<PLACEHOLDERS>` filled per engagement, or as quoted evidence from
    the target itself. Copied scope from a prior engagement is a
    failed scan — re-derive from Phase 1.
12. **Respect exclusions and handle secrets safely.** Never open
    `<EXCLUDED_PATHS>`; never paste live secret values into reports,
    chat, or tickets beyond the minimum redacted excerpt that proves
    the finding. Escalate suspected live credentials immediately.

---

## 8. Search pattern library

Scope every pattern to the target's own directories. Replace
`<SCOPE>` with the relevant subset of `<SCOPE_DIRS>` actually
traversed, and record the substitution in the Phase 3/4 methodology
note. Patterns below are starting points — extend them from Phase 2
observations (framework idioms, ORM names, queue names) and record
extensions.

Matching is **case-insensitive** in every engine (`cscan` default;
add `-i` to manual `grep`/`rg` invocations). Audit search favors
recall — `API_TOKEN`, `Password`, and `secret` must all hit the same
pattern. Case-sensitive refinement, if ever needed, must be justified
in the receipt.

```bash
# Secrets (restrict --include to extensions observed in Phase 1)
grep -rn "password\|secret\|api_key\|apikey\|token\|credential" <SCOPE>

# TODOs and tech debt
grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMP\|WORKAROUND" <SCOPE>

# Authentication & authorization
grep -rn "auth\|login\|session\|jwt\|bearer\|permission\|role\|policy\|allow\|deny" <SCOPE>

# Data protection
grep -rn "encrypt\|decrypt\|hash\|pseudonym\|anonymize\|redact\|mask\|crypto-shred" <SCOPE>

# Data-subject & lifecycle keywords
grep -rn "DSAR\|data.subject\|erasure\|right.to.forget\|consent\|retention\|breach\|purge\|legal.hold" <SCOPE>

# Destructive data operations
grep -rn "DELETE\|DROP\|TRUNCATE\|CASCADE\|soft.delete\|hard.delete" <SCOPE>

# Network exposure
grep -rn "https\?://\|Access-Control\|Content-Security-Policy\|cors\|csrf" <SCOPE>

# File structure sanity
git ls-files | sort | uniq -c | sort -rn | head -50
```

`ripgrep` equivalents (`rg -n "pattern" <SCOPE>`) are preferred on
large trees; record which tool and version ran (report Section 2.3).

---

## 9. Cross-platform notes

- Target checkouts may be scanned from Linux/macOS shells or Windows
  PowerShell. Prefer `git ls-files` + `grep`/`rg` where available;
  on PowerShell use `Select-String -Path "<SCOPE>/*" -Pattern "…"`
  and record the substitution.
- POSIX text utilities (`sed`, `awk`, `xargs -0`) may be absent on
  Windows. Appendix B must record the actual commands run on the
  actual shell — portability of the report matters more than
  uniformity of the commands.
- Line-ending differences (CRLF/LF) do not change verdicts; note the
  dominant convention once in Appendix A if mixed endings are observed.

---

## 10. References

- `compliance/adr-compliance-matrix.md` — normative commitment matrix verified by this methodology.
- `compliance/references/` — source texts (GDPR, ISO 27001 Annex A controls).
- `templates/compliance-scan-report-template.md` — normative report skeleton.
- `prompts/compliance-scan-agent.md` — short copy-paste invocation wrapper.
- `tools/cscan.py` — evidence instrument (freeze/inventory/search/scaffold/validate); `tools/cscan` + `tools/cscan.ps1` are thin shims.
- `tests/test_cscan.py` — executable specification of the instrument (`python -m unittest discover -s tests`).
- `AGENTS.md` — contributor conventions for humans and agents editing this kit.
