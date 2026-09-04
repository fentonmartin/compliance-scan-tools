# compliance-scan-tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v1.1.0-blue.svg)](CHANGELOG.md)
[![Standards](https://img.shields.io/badge/standards-ISO%2027001%20%7C%20GDPR%20%7C%20UU%20PDP-green.svg)](compliance/adr-compliance-matrix.md)

A **project-agnostic, evidence-based compliance scanning kit** for software
repositories. Paste the agent prompt into any AI coding assistant, point it
at a target repo, and get back an **auditor-grade compliance report** where
every finding traces to `file:line` + commit hash + date + standard reference.

Covers **ISO/IEC 27001:2022 (all 93 Annex A controls)**, the **EU GDPR**, and
**Indonesia's UU PDP No. 27/2022** — with 31 reusable architectural
commitments (ADR matrix) as the verification baseline.

No product names. No hard-coded repos. No assumed stacks. Just evidence.

---

## Table of contents

- [Why this exists](#why-this-exists)
- [Features](#features)
- [Repository structure](#repository-structure)
- [Requirements](#requirements)
- [Quickstart](#quickstart)
- [How to use (copy-paste AI agent)](#how-to-use-copy-paste-ai-agent)
- [What you get (report anatomy)](#what-you-get-report-anatomy)
- [Standards & coverage](#standards--coverage)
- [Configuration reference](#configuration-reference)
- [Security & privacy](#security--privacy)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Versioning](#versioning)
- [License](#license)

---

## Why this exists

Ordinary scan reports tell your team "looks fine." Audit reports must
answer a regulator asking **"where is the evidence?"** — with document
control, a frozen evidence point (commit hashes), quoted code, documented
negative searches, stated limitations, and human sign-off.

This kit packages that discipline into three reusable pieces:

1. **Methodology** — a 7-phase scan protocol any agent (or human) can execute.
2. **Commitment matrix** — 31 ADRs mapped to GDPR articles, ISO 27001 Annex A
   controls, and UU PDP clauses, each with verbatim normative quotes.
3. **Report template + agent prompt** — copy-paste wrappers that keep every
   engagement consistent and free of prior-project leakage.

It was extracted from a real project engagement and scrubbed of every
hard-coded value (see [Audit note](#audit-note)) so it works on *your* repo.

## Features

- 🔍 **7-phase evidence protocol** — authorization → inventory → structure →
  commitment verification → security scan → docs coverage → reporting.
- 🧾 **Auditor-grade reports** — document control, risk-rated findings
  (Critical → Informational), commitment matrix, appendices, sign-off.
- 📐 **31-commitment ADR matrix** — tenant isolation to crypto-shredding to
  deletion-propagation state machines, each with standard references.
- 📚 **Bundled source texts** — GDPR (CELEX 32016R0679) + ISO 27001:2022
  Annex A 93-control reference, offline-ready.
- 🤖 **Copy-paste agent prompt** — one block + variable table works with any
  repo-aware AI assistant; no custom tooling required.
- ⚙️ **Executable evidence tool (`tools/cscan.py`)** — stdlib-only, zero
  dependencies: evidence freeze, inventory, case-insensitive pattern search
  with machine receipts, report scaffolding, and pre-release validation.
  Enforces the existence protocol: no receipt, no verdict.
- ✅ **Self-testing kit** — `python -m unittest discover -s tests` plus a CI
  leak-guard that fails on prior-engagement token leakage.
- 🧼 **Zero hard-coding by design** — every engagement value is a
  `<PLACEHOLDER>`; the methodology fails the scan if prior-engagement scope leaks in.
- 🪟🐧 **Cross-platform** — git/grep/rg commands with PowerShell equivalents noted.

## Repository structure

```text
compliance-scan-tools/
├── README.md                              ← you are here
├── AGENTS.md                              ← contributor conventions (humans + agents)
├── LICENSE                                ← MIT
├── CHANGELOG.md                           ← release history
├── .gitignore
├── compliance/
│   ├── README.md                          ← section index
│   ├── scan-methodology.md                ← binding 7-phase procedure + existence protocol
│   ├── adr-compliance-matrix.md           ← 31 commitments → ISO 27001 / GDPR / UU PDP
│   └── references/
│       ├── gdpr-celex-32016R0679-en.md    ← GDPR source text
│       └── iso27001-2022-annex-a-93-controls.md ← Annex A 93-control reference
├── prompts/
│   └── compliance-scan-agent.md           ← copy-paste invocation wrapper (+ worked example)
├── templates/
│   └── compliance-scan-report-template.md ← normative report skeleton (Document Control → Sign-off)
├── tools/
│   ├── cscan.py                           ← executable evidence tool (stdlib-only)
│   ├── cscan                              ← POSIX shim
│   └── cscan.ps1                          ← PowerShell shim (5.1 compatible)
└── tests/
    └── test_cscan.py                      ← instrument tests + kit hygiene guards
```

## Requirements

- **Target repo** under version control (`git`) — the agent freezes evidence
  with `git rev-parse HEAD` at scan start/end.
- **An AI coding agent with repository access** (or a human following the
  methodology by hand). No proprietary scanner, no SaaS, no API keys.
- Optional but recommended: `grep` or `ripgrep` (`rg`) for pattern search;
  PowerShell `Select-String` works where POSIX tools are absent.

## Quickstart

```bash
# 1. Clone this kit (read-only reference; the scan runs against YOUR target repo)
git clone https://github.com/fentonmartin/compliance-scan-tools.git

# 2. Collect machine evidence against the target (writes .evidence/ + receipts)
python compliance-scan-tools/tools/cscan.py freeze --target /path/to/<target> --out .evidence/00-freeze
python compliance-scan-tools/tools/cscan.py inventory --target /path/to/<target> --out .evidence/01-inventory
python compliance-scan-tools/tools/cscan.py search --target /path/to/<target> --out .evidence/02-search --exclude "secrets/*"

# 3. Fill the 14 variables in prompts/compliance-scan-agent.md, paste the
#    block into your agent along with the files in "Attachments",
#    and let it execute compliance/scan-methodology.md.
```

First run should take one directory + two commitments as a trial, then
expand to full scope (see `prompts/compliance-scan-agent.md → Tips`).

## The evidence tool (`cscan`)

`tools/cscan.py` is stdlib-only Python 3.8+ — no install step, runs on any
checkout with Python and git (`tools/cscan` and `tools/cscan.ps1` are thin
shims). It is the preferred instrument for Phases 1, 4, and 7:

| Command | Phase | Output |
|---|---|---|
| `cscan freeze --target <dir> --out <EVIDENCE_DIR>/00-freeze` | 0–1 | HEAD, branch, dirty-tree status, tool versions (`freeze.json/md`) |
| `cscan inventory --target <dir> --out <EVIDENCE_DIR>/01-inventory` | 1 | tracked/untracked lists, by-extension/dir counts, large files |
| `cscan search --target <dir> --out <EVIDENCE_DIR>/02-search --exclude '<glob>'` | 3–4 | per-group hits + `receipts.json` (command, file universe, skips, counts) |
| `cscan scaffold --set KEY=VALUE --out <report>.md` | 7 | report draft from the template; warns on unfilled placeholders |
| `cscan validate --report <report>.md` | 7 | pre-release gate: placeholders, FINDING completeness, Document Control, token leakage |

Core guarantee: the search universe is `git ls-files` (the same universe as
Phase 1), matching is case-insensitive, and `--exclude` paths are recorded
by name but **never opened** — the receipt proves what was *not* looked at,
which is what makes a NOT FOUND verdict valid. See the existence protocol
in `compliance/scan-methodology.md §4`.

## How to use (copy-paste AI agent)

1. **Derive scope from the target, not from memory.** Run Phase 0–1 first:
   `git ls-files | cut -d'/' -f1 | sort | uniq -c | sort -rn` gives you the
   real `<SCOPE_DIRS>`. If a directory in your plan doesn't exist in the
   target, you copied it from somewhere else — start over.
2. **Fill every variable.** The 14 placeholders (`<TARGET_REPO_URL>`,
   `<TARGET_BRANCH>`, `<SCAN_START_COMMIT>`, `<SCAN_END_COMMIT>`,
   `<SCOPE_DIRS>`, `<EXCLUDED_PATHS>`, `<STANDARDS>`, `<CLASSIFICATION>`,
   `<SCAN_TYPE>`, `<OPERATOR>`, `<REVIEWER>`, `<APPROVER>`, `<SCAN_DATE>`,
   `<EVIDENCE_DIR>`)
   are documented with examples in the methodology (§1.1) and the prompt file.
3. **Paste and run.** Give the agent the prompt block + the five attachment
   files. It works through Phases 0–7 and delivers a report built only from
   `templates/compliance-scan-report-template.md`.
4. **Release requires humans.** No report is final without a named human
   reviewer and approver in Document Control and the Sign-off table.

Worked example with illustrative values lives in
[`prompts/compliance-scan-agent.md`](prompts/compliance-scan-agent.md#worked-example-illustrative-values--replace-all-of-them).

## What you get (report anatomy)

| Section | Contents |
|---|---|
| Document Control | ID, version, classification, author/reviewer/approver, dates, commit hashes, repo, branch, scope, standards |
| Executive Summary | 3–5 sentence posture + metrics (files scanned, commitments N/N, findings by severity, compliance score) |
| Scope & Methodology | In/out-of-scope tables, 7-phase description, tools table, **Limitations** |
| Findings | Rating scale, F-001… summary table, detailed records (Description / verbatim Evidence / Impact / Recommendation / Owner / Target date) |
| Compliance Matrix | One row per commitment: ✅ Implemented / ⚠️ Partial / ❌ Not found / ❔ Unclear + evidence + gap |
| Conclusion | Verdict within scope, biggest risks, what-first ordering |
| Appendices | A: inventory · B: commands + full output · C: files reviewed · D: methodology ref |
| Sign-off | Scanner / Reviewer / Approver signatures + dates |

Severity scale: **Critical** (24h) · **High** (7d) · **Medium** (30d) ·
**Low** (next release) · **Informational** (track).

## Standards & coverage

| Framework | Coverage in this kit |
|---|---|
| ISO/IEC 27001:2022 | All 93 Annex A controls as reference text; matrix rows cite Organizational (5.x), People (6.x), Physical (7.x), Technological (8.x) controls |
| EU GDPR (Reg. 2016/679) | Full regulation text bundled; matrix cites principles (Art. 5), rights (Art. 12–22), design/security/breach (Art. 25, 32–34), transfers (Ch. V) |
| UU PDP No. 27/2022 (Indonesia) | Clause mapping alongside GDPR (rights, minimization, breach notification, residency); sectoral regimes assessed per-engagement in Phase 0, never assumed |

The matrix's 31 commitments span tenant isolation, deny-by-default
authorization, field-level ABAC, encryption (TLS 1.3 / AES-256 envelope),
crypto-shredding key hierarchies, transactional outbox PII isolation,
versioned consent provenance, WORM audit trails, and a five-state deletion
propagation machine (`CREATED → ACTIVE → ARCHIVED → LEGAL_HOLD → PURGED`).

## Configuration reference

| Variable | Required | Notes |
|---|---|---|
| `<TARGET_REPO_URL>` | Yes | Clone URL / identifier of the system under audit |
| `<TARGET_BRANCH>` | Yes | Branch under audit |
| `<SCAN_START_COMMIT>` / `<SCAN_END_COMMIT>` | Yes | `git rev-parse HEAD` at evidence-freeze boundaries; disclose dirty trees |
| `<SCOPE_DIRS>` | Yes | Derived from `git ls-files` in the target — never copied between engagements |
| `<EXCLUDED_PATHS>` | Yes | Secret/key/PII paths the scanner must list but never open (with authority) |
| `<STANDARDS>` | Yes | Subset of ISO 27001 / GDPR / UU PDP (or extended) for this engagement |
| `<SCAN_TYPE>` | Yes | Initial / Periodic / Incident-triggered / Change-triggered |
| `<OPERATOR>` / `<REVIEWER>` / `<APPROVER>` | Yes | Agent identity + two humans (review/approval cannot be the agent) |
| `<SCAN_DATE>` / `<CLASSIFICATION>` | Yes | `YYYY-MM-DD`; handling caveat (e.g. Confidential) |

## Security & privacy

- The scanner **reads code; it must not exfiltrate secrets.** Paths matching
  `<EXCLUDED_PATHS>` are listed by name/size/tracking status only.
- Findings redact live credential *values* to the minimum excerpt proving the
  issue; suspected live credentials are escalated immediately, not pasted
  into tickets or chat.
- Reports themselves are classified artifacts — handle per `<CLASSIFICATION>`
  and store/sign them outside the scanned tree unless your policy says otherwise.

## Limitations

- This kit performs **static, evidence-based verification** — it does not
  replace penetration testing, dynamic analysis, or a certified ISO 27001
  Stage 1/2 audit.
- Reference texts are bundled for offline convenience; always confirm article/
  control numbering against the current official publication before citing to
  a regulator.
- UU PDP secondary regulation is evolving; jurisdiction-specific residency and
  sectoral obligations must be scoped per engagement (Phase 0), not assumed
  from examples.

## Audit note

v1.0.0 scrubbed all prior-engagement coupling found in the export:
hard-coded product name, source repository URL, agent/model name,
assumed directory layouts, region/sector/domain examples presented as
defaults, internal doc links and wiki syntax, and mixed-language prose. The
methodology now fails closed on any such leakage (§7 rule 11) and every
command takes scope as a variable.

## Contributing

Issues and PRs are welcome. Please:

1. Keep the kit project-agnostic — no product, repo, tenant, region, or
   vendor names outside quoted evidence or explicitly marked `[Example: …]`.
2. Keep `templates/compliance-scan-report-template.md` normative; if it and
   the methodology disagree, update the methodology to match the template.
3. Add commands with both POSIX and PowerShell forms where they differ.
4. Sign off reports in examples with placeholder names, never real people.

## Versioning

Semantic versioning (`CHANGELOG.md`). Current release: **v1.1.0** —
executable evidence tool (`cscan`), existence protocol, purpose-aligned
filenames, report validation gate, tests + CI leak-guard.

## License

MIT — see [LICENSE](LICENSE). Reference texts in `compliance/references/`
retain their original sources and are bundled for convenience; the GDPR text
is an official EU publication.
