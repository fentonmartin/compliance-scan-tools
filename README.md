# 🛡️ CSCAN Tools

**Evidence-based compliance scanning for any repository — collect evidence, never assume.**

Point it at a codebase. Get back an auditor-grade report where every finding traces to `file:line` + commit hash + date + standard reference — and every "not found" ships the search receipt that proves it.

`freeze` · `inventory` · `search` · `scaffold` · `validate`

[![version](https://img.shields.io/badge/version-1.2.0-blue?style=flat-square)](CHANGELOG.md) [![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE) [![python](https://img.shields.io/badge/python-3.8%2B-yellow?style=flat-square)](tools/cscan.py) [![standards](https://img.shields.io/badge/standards-ISO%2027001%20%7C%20GDPR%20%7C%20UU%20PDP-lightgrey?style=flat-square)](compliance/adr-compliance-matrix.md)

**Latest: `1.2.0`** — CSCAN Tools branding, executable evidence instrument, existence protocol, report validation gate. [What changed](CHANGELOG.md#120---2026-09-04) · [Tutorial](#tutorial-your-first-scan) · [Upgrading](#already-using-an-older-version)

[**Quick start**](#quick-start) · [**Existence protocol**](#the-existence-protocol) · [Commands](#commands) · [Tutorial](#tutorial-your-first-scan) · [Structure](#repository-structure) · [Standards](#standards--coverage) · [Contributing](#contributing)

---

## Overview

Every audit starts the same way: someone opens a repo they have never seen, greps around, half-understands the architecture, and writes up confident findings built on a partial reading. The report says "encryption is implemented" because one file mentions TLS. It says "no hardcoded secrets" because nobody searched the fixtures folder. Next quarter, a regulator asks *"where is the evidence?"* — and there is none. Just confidence.

CSCAN Tools makes the **evidence** the durable artifact instead of the confidence. A frozen commit hash says which code was examined. A quoted code block says what was seen. A machine-written search receipt says exactly what was searched, with what patterns, across how many files — so "not found" is a proven fact, not an absence of looking.

**The core principle: no receipt, no verdict.** A claim about the target is either observed (cited), proven absent (receipted), or explicitly marked as not searched. There is no fourth state — no "probably", no "likely", no "assumed".

```
Target repo  →  Freeze  →  Inventory  →  Search  →  Verify  →  Report  →  Auditor-grade evidence
                (commit)   (map)       (receipts)  (matrix)    (validate + sign-off)
```

### What it is not

Not a vulnerability scanner, not a SAST engine, not a GRC platform, not a hosted service, not a penetration test. There is no database, no agent framework to install, no SaaS to send your code to, and no runtime dependency beyond Python and git. A methodology, a commitment matrix, a report template, and one stdlib-only script are the entire stack. It does not replace a certified ISO 27001 Stage 1/2 audit — it produces the evidence pack that makes that audit faster and cheaper.

---

## Why

You could ask any AI assistant to "audit this repo for compliance." You will get a fluent report. Fluency is the easy half of the problem, and it leaves the hard half untouched:

A fluent audit gives you

It does not give you

Findings that read well

Whether the finding was observed or inferred

"Checked all routes"

The list of routes, or the command that listed them

"No secrets found"

The patterns tried, the files searched, the exclusions honored

A compliance score

A frozen commit the score refers to

A report an AI assistant asked *"prove data erasure works"* answers from a comment saying `# TODO: implement erasure` — and marks it implemented. **The confidence is the bug.** CSCAN Tools records the comment as a *lead*, follows it to the enforcement point, and if there is none, writes NOT FOUND with the receipt attached — or UNCLEAR if the path was never searched.

The trade-off is honest: evidence collection costs time up front, and the methodology has rules to learn. What you get back is defensible. A fluent paragraph is not something you can show a regulator.

---

## Quick start

Commit first in the **target** repo. A scan freezes evidence at a commit, and a clean tree is how the report proves what it examined:

```bash
cd your-project
git commit -am "checkpoint"
```

### 1. Collect machine evidence · ~2 min

No install step. `cscan` is one file, stdlib-only, and runs anywhere Python 3.8+ and git exist:

```bash
# Windows PowerShell
python ..\compliance-scan-tools\tools\cscan.py freeze --target . --out .evidence\00-freeze
python ..\compliance-scan-tools\tools\cscan.py inventory --target . --out .evidence\01-inventory
python ..\compliance-scan-tools\tools\cscan.py search --target . --out .evidence\02-search --exclude "secrets/*"

# Linux / macOS
python3 ../compliance-scan-tools/tools/cscan.py freeze --target . --out .evidence/00-freeze
python3 ../compliance-scan-tools/tools/cscan.py inventory --target . --out .evidence/01-inventory
python3 ../compliance-scan-tools/tools/cscan.py search --target . --out .evidence/02-search --exclude 'secrets/*'
```

Out comes `.evidence/`: the frozen HEAD, file inventory, per-group hits, and `receipts.json` — what ran, where, when, across how many files, with what skipped. Excluded paths are recorded by name and **never opened**.

### 2. Paste this into your agent

**Works everywhere** — Claude Code, opencode, Codex, Cursor, Windsurf, or anything else with file access. Open the project you want scanned and paste this into the chat box:

```text
You are a compliance scan agent operating under CSCAN Tools v1.2.0.

1. Read compliance-scan-tools/compliance/scan-methodology.md and follow it exactly.
2. Read compliance-scan-tools/compliance/adr-compliance-matrix.md — verify each
   commitment one by one against THIS repo.
3. Use compliance-scan-tools/templates/compliance-scan-report-template.md
   as your only report skeleton.

Target repo: <URL> (branch: main) | Date: <YYYY-MM-DD>
Scope: <top-level dirs from `git ls-files`> | Exclusions: <paths + authority>
Standards: ISO 27001:2022, GDPR, UU PDP No. 27/2022
Operator: AI Agent | Reviewer: <human> | Approver: <human> | Classification: Confidential

Rules: EXISTS → file:line + commit + date. NOT FOUND → search receipt.
Not searched → UNCLEAR, stated. Leads are not evidence. Never open exclusions.
Gate release with `cscan validate` — no placeholders, no leakage, human sign-off.
```

That's the whole setup. Afterwards, **`cscan validate --report <report>.md`** is the one gate that matters — it fails on unfilled placeholders, incomplete findings, missing Document Control, and prior-engagement leakage.

Prefer to drive it yourself? The full 14-variable invocation block, attachment list, and a worked example live in [`prompts/compliance-scan-agent.md`](prompts/compliance-scan-agent.md).

### Already using an older version?

Releases are documented in [CHANGELOG.md](CHANGELOG.md) with rename maps where paths moved:

- **On 1.0.x → 1.1.0**: three files were renamed (`scan-methodology.md`, `adr-compliance-matrix.md`, `compliance-scan-agent.md`). Update any saved prompts or bookmarks; report content is unchanged.
- **On 1.1.x → 1.2.0**: branding only (`CSCAN Tools`), plus a richer README and `CONTRIBUTING.md`. No path or behavior changes — `cscan validate` keeps passing on 1.1-era reports.

---

## The existence protocol

The one idea that makes everything else work. Every statement about the target is exactly one of three verdicts:

| Verdict | Meaning | Minimum proof |
|---|---|---|
| ✅ EXISTS | Present at the frozen commit | Quoted file content with `path:line-range` + commit + date |
| ❌ NOT FOUND | Absent from the searched scope | **Search receipt** — exact patterns, directories + file counts, command + tool version, timestamp, exclusions, 0-match result |
| ❔ UNCLEAR | No verdict possible yet | Explicit "not searched because …" — a valid outcome, never a guess |

Three rules do most of the work:

1. **Leads are not evidence.** A comment saying "encrypts data", a README promising MFA, a function named `deleteUser` — follow each to the enforcement point (the code path that executes) and quote *that*.
2. **One sighting does not prove coverage.** Auth on one route never proves "all routes" — that claim needs every route listed with a verdict, or it stays PARTIAL/UNCLEAR.
3. **Excluded paths are UNCLEAR, never NOT FOUND.** Anything unopened supports no claim in either direction.

Full version in [`compliance/scan-methodology.md`](compliance/scan-methodology.md#the-existence-protocol-do-not-assume---collect-evidence) §4 — including why `cscan search` receipts exist and what a valid NOT FOUND looks like.

---

## Commands

Command

What it does

When

**`freeze`**

Records HEAD, branch, dirty-tree status, tool versions — the evidence point the whole report refers to

First, always

**`inventory`**

Maps every tracked/untracked file: counts, by-extension, by-directory, large files

Phase 1, and to derive scope honestly

**`search`**

Runs the 7-group pattern library (secrets, auth, data-protection, data-subject, destructive, network, tech-debt) with per-group receipts

Phases 3–4, instead of hand-rolled grep

**`scaffold`**

Fills the report template's variables into a draft; warns on anything left unfilled

Phase 7, to start the report

**`validate`**

Pre-release gate: placeholders, FINDING completeness, Document Control, token leakage

Before any report leaves your machine

```bash
python tools/cscan.py freeze --target /path/to/target --out .evidence/00-freeze
python tools/cscan.py search --target /path/to/target --out .evidence/02-search --exclude 'secrets/*' --group secrets --group auth
python tools/cscan.py validate --report SCAN-260904-01.md
```

`--help` on any subcommand documents the rest. Matching is case-insensitive by design (`API_TOKEN` and `password` hit the same pattern); `rg`/`grep` engines are available via `--engine` where installed, with the pure-Python default as the portable baseline. Run `python -m unittest discover -s tests -v` to verify the instrument itself.

---

## Tutorial: your first scan

A complete evidence-backed pass in about twenty minutes. Use any small repo you own — the shape is the same at any size.

### 1. Freeze and map · ~5 min

Run `freeze` and `inventory` from [Quick start](#quick-start). Open `.evidence/01-inventory/inventory.json` and read three numbers: total tracked, total untracked, files by top-level directory. **Those directories are your scope** — write them down as `<SCOPE_DIRS>`. If a directory in your head doesn't exist in that file, you imagined it. Scope comes from the repo, never from memory.

Untracked files deserve a look (by name only): an untracked `.env` or `id_rsa` is itself a finding — credentials sitting outside version control with no provenance.

### 2. Search one group, read the receipt · ~5 min

```bash
python tools/cscan.py search --target /path/to/target --out .evidence/02-search --group secrets
```

Open `.evidence/02-search/secrets.txt`, then `receipts.json`. The receipt tells you the file universe, how many files were searched, and what the 0-match (or N-match) result covers. **This receipt is what turns "no secrets found" from a shrug into a finding.** Paste it into Appendix B verbatim — reconstructing commands at the end is where fabricated evidence creeps in.

### 3. Verify one commitment end to end · ~5 min

Pick one row from [`compliance/adr-compliance-matrix.md`](compliance/adr-compliance-matrix.md) — ADR-006 (*secrets never in source*) pairs naturally with your secrets search. Follow Phase 3: quote the strongest evidence (or attach the receipt for NOT FOUND), write the verdict block, assign the severity. One commitment, fully worked, teaches the discipline faster than thirty skimmed ones.

### 4. Scaffold and gate · ~5 min

```bash
python tools/cscan.py scaffold --set TARGET_REPO_URL=<url> --set TARGET_BRANCH=main ... --out SCAN-260904-01.md
python tools/cscan.py validate --report SCAN-260904-01.md
```

Watch `validate` fail — unfilled placeholders, an empty findings section, missing sign-off. Fill one finding completely (Description / verbatim Evidence / Impact / Recommendation / Owner / Target date) and re-run. **A validator that passes on an empty draft would be decoration; this one isn't.**

### Then what

A rhythm, not a project: freeze at every release, re-run `search` on change, verify the commitments the change touches, `validate` before the report ships. Come back in three months having forgotten all of it? The methodology's Phase 7 pre-release checklist and `prompts/compliance-scan-agent.md` re-derive the whole engagement from variables — nothing lives in anyone's head.

---

## Repository structure

```text
README.md                        ← you are here
AGENTS.md                        🤖  contributor conventions — the 5 rules every edit must keep
CONTRIBUTING.md                  🙋  how anyone can add or correct anything
CHANGELOG.md                     📜  release history with rename maps
LICENSE                          ⚖️  MIT
compliance/
├── README.md                    🗺️  section index — start here if you're lost
├── scan-methodology.md          🧭  binding 7-phase procedure + existence protocol
├── adr-compliance-matrix.md     📐  31 commitments → ISO 27001 / GDPR / UU PDP, with quotes
└── references/                  📚  source texts: GDPR regulation + Annex A 93-control guide
prompts/
└── compliance-scan-agent.md     📋  copy-paste invocation: variables, attachments, worked example
templates/
└── compliance-scan-report-template.md  🧾  normative skeleton: Document Control → Sign-off
tools/
├── cscan.py                     ⚙️  the instrument: freeze/inventory/search/scaffold/validate
├── cscan                        🐧  POSIX shim
└── cscan.ps1                    🪟  PowerShell shim (5.1 compatible)
tests/
└── test_cscan.py                ✅  9 tests: fixture-repo evidence runs + kit hygiene guards
.github/workflows/ci.yml         🔁  cross-OS test matrix + prior-engagement leak-guard
```

### Why these names

Every name is doing a job:

Name

Why not something else

`scan-methodology.md`

Not `FULL-PROJECT-SCAN-…` — filenames shout when the content is a warning. This is the normal way in, so it gets the plain name.

`adr-compliance-matrix.md`

Not `README.md` — a directory index and a 31-row normative matrix are different documents with different readers. The index stays an index.

`compliance-scan-agent.md`

Not `scan-agent-prompt.md` — the file *is* the agent's standing orders for an engagement, not a one-line prompt. The name says what it does when pasted.

`cscan`

Short, typable, unambiguous in a shell history. `CSCAN Tools` is the brand you cite; `cscan` is the command you run — the same split as `GitHub`/`git`.

`receipts.json`

Not `logs/` — a log says what happened; a receipt proves a search was exhaustive. NOT FOUND verdicts rest on these files, so the name carries the legal metaphor deliberately.

the template's `F-001…` findings

Not free-form sections — stable IDs let quarter-over-quarter reports diff against each other, which is the whole point of repeated scanning.

---

## Standards & coverage

| Framework | Coverage in this kit |
|---|---|
| ISO/IEC 27001:2022 | All 93 Annex A controls as bundled reference; matrix rows cite Organizational (5.x), People (6.x), Physical (7.x), Technological (8.x) controls |
| EU GDPR (Reg. 2016/679) | Full regulation text bundled (`compliance/references/`); matrix cites principles (Art. 5), rights (Art. 12–22), design/security/breach (Art. 25, 32–34), transfers (Ch. V) |
| UU PDP No. 27/2022 (Indonesia) | Clause mapping alongside GDPR (rights, minimization, breach notification, residency); sectoral regimes are scoped per engagement in Phase 0, never assumed |

The matrix's 31 commitments span tenant isolation, deny-by-default authorization, field-level access control, encryption (TLS 1.3 / AES-256 envelope), crypto-shredding key hierarchies, transactional-outbox PII isolation, versioned consent provenance, append-only audit trails, and a five-state deletion propagation machine (`CREATED → ACTIVE → ARCHIVED → LEGAL_HOLD → PURGED`).

---

## What you get (report anatomy)

| Section | Contents |
|---|---|
| Document Control | ID, version, classification, author/reviewer/approver, dates, commit hashes, repo, branch, scope, standards, evidence bundle |
| Executive Summary | 3–5 sentence posture + metrics (files scanned, commitments N/N, findings by severity, compliance score) |
| Scope & Methodology | In/out-of-scope tables, 7-phase description, tools table, **Limitations** |
| Findings | Rating scale, F-001… summary table, detailed records (Description / verbatim Evidence / Impact / Recommendation / Owner / Target date) |
| Compliance Matrix | One row per commitment: ✅ Implemented / ⚠️ Partial / ❌ Not found / ❔ Unclear + evidence + gap |
| Conclusion | Verdict within scope, biggest risks, what-first ordering |
| Appendices | A: inventory · B: commands + receipts · C: files reviewed · D: methodology ref |
| Sign-off | Scanner / Reviewer / Approver signatures + dates |

Severity scale: **Critical** (24h) · **High** (7d) · **Medium** (30d) · **Low** (next release) · **Informational** (track).

---

## Configuration reference

Fourteen variables, no defaults for target-specific fields. Full definitions with examples: [`compliance/scan-methodology.md`](compliance/scan-methodology.md#1-how-to-use-this-document-copy-paste-agent) §1.1.

| Variable | Meaning |
|---|---|
| `<TARGET_REPO_URL>` / `<TARGET_BRANCH>` | System under audit |
| `<SCAN_START_COMMIT>` / `<SCAN_END_COMMIT>` | Evidence-freeze boundaries (`cscan freeze`); disclose dirty trees |
| `<SCOPE_DIRS>` | Derived from `git ls-files` — never copied between engagements |
| `<EXCLUDED_PATHS>` | Secret/key/PII paths: listed, never opened, with stated authority |
| `<STANDARDS>` / `<SCAN_TYPE>` | Frameworks in scope; Initial / Periodic / Incident-triggered / Change-triggered |
| `<OPERATOR>` / `<REVIEWER>` / `<APPROVER>` | Agent identity + two humans (review/approval can't be the agent) |
| `<SCAN_DATE>` / `<CLASSIFICATION>` | `YYYY-MM-DD`; handling caveat |
| `<EVIDENCE_DIR>` | Machine output + receipts, stored outside the target tree |

## Works with any AI agent

The kit assumes nothing about the agent except repository access. Claude Code, opencode, Codex, Cursor, Windsurf — anything that can read files and run `cscan` can execute the methodology, because the methodology is Markdown and the instrument is stdlib Python. The agent is not the owner of the verdict. The evidence bundle is.

---

## Security & privacy

- The scanner **reads code; it must not exfiltrate secrets.** Paths matching `<EXCLUDED_PATHS>` are listed by name/size/tracking status only — `cscan search --exclude` enforces this mechanically.
- Findings redact live credential *values* to the minimum excerpt proving the issue; suspected live credentials are escalated immediately, never pasted into tickets or chat.
- Reports are classified artifacts — handle per `<CLASSIFICATION>` and store/sign them outside the scanned tree unless policy says otherwise.

## Limitations

- **Static, evidence-based verification** — not penetration testing, dynamic analysis, or a certified ISO 27001 Stage 1/2 audit. It builds the evidence pack; auditors still audit.
- Reference texts are bundled for offline convenience; confirm article/control numbering against the current official publication before citing to a regulator.
- Pattern search favors recall over precision — expect to disposition false positives, and record the disposition. A dismissed hit without a reason is an assumption wearing a lab coat.
- UU PDP secondary regulation is evolving; jurisdiction-specific residency and sectoral obligations are scoped per engagement, never assumed from examples.

---

## Contributing

This is open source, and it gets better the way audit evidence does — by correction. Wrong pattern? Missing commitment? Bad mapping to an ISO control? Unclear methodology step? **Open an issue or a PR.** Small, precise corrections beat grand redesigns: one pattern with a fixture, one mapping with a quote, one paragraph with a reason.

Start with [`CONTRIBUTING.md`](CONTRIBUTING.md) — five rules, the dev loop, and what makes a PR merge quickly. Be kind, be precise, cite your sources. Practice what the tool preaches.

## Roadmap

In rough priority order — each is a small, reviewable release, and contributions here are especially welcome:

1. **SoA + risk-register templates** — the formal Statement of Applicability auditors ask for, generated from the ADR matrix.
2. **Re-scan diffing** — `cscan diff` across quarters: what changed since the last audit.
3. **Entropy-based secret detection** — optional `gitleaks`/`trufflehog` hook recorded in the receipt.
4. **Dependency audit linkage** — CVE/CVSS grounding for `npm`/`pip`/`cargo` findings.
5. **Signed reports** — cryptographic sign-off instead of typed names.
6. **SBOM readiness check** — one more matrix row enterprise buyers increasingly require.

## Versioning

Semantic versioning ([CHANGELOG.md](CHANGELOG.md)). Current release: **v1.2.0** — CSCAN Tools branding, rich README, `CONTRIBUTING.md`, executable instrument, existence protocol, validation gate.

## License

MIT — see [LICENSE](LICENSE). Reference texts in `compliance/references/` retain their original sources and are bundled for convenience; the GDPR text is an official EU publication.

## Acknowledgments

Built from a real engagement's scar tissue — every rule here exists because its absence once produced a confident, evidence-free paragraph. Thanks to the ISO/IEC 27001 and GDPR drafters whose texts are quoted throughout, and to every future contributor who files the correction we haven't thought of yet.
