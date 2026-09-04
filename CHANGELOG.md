# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-09-04

### Changed
- **CSCAN Tools** is now the brand across the kit: README, agent prompt,
  report template, tool `--version` output, and shims. The command stays
  `cscan`; the repository name is unchanged.
- Root README rewritten: hero + positioning, overview, "what it is not",
  quick start with real commands, existence-protocol summary, `cscan`
  command table, 4-step first-scan tutorial, annotated structure with
  "why these names", roadmap, and acknowledgments.

### Added
- `CONTRIBUTING.md`: contribution paths, the five rules, dev loop, and
  PR guidance — open source is a correction mechanism, documented as one.

## [1.1.0] - 2026-09-04

### Added
- `tools/cscan.py`: executable evidence instrument, stdlib-only
  (Python 3.8+, zero dependencies) with five subcommands — `freeze`,
  `inventory`, `search` (case-insensitive, `git ls-files` universe,
  per-group `receipts.json`), `scaffold`, `validate` — plus `tools/cscan`
  (POSIX) and `tools/cscan.ps1` (Windows PowerShell 5.1) shims.
- Existence protocol in `compliance/scan-methodology.md`: three-state
  verdicts (EXISTS / NOT FOUND / UNCLEAR), search-receipt requirements,
  lead-vs-evidence rule, and `<EVIDENCE_DIR>` engagement variable.
- `tests/test_cscan.py`: 9 unit tests (fixture-repo evidence collection,
  exclusion discipline, scaffold/validate round-trip, kit hygiene guard).
- `.github/workflows/ci.yml`: cross-OS test matrix + prior-engagement
  token leak-guard.
- `AGENTS.md`: contributor conventions for humans and agents.
- `templates/…`: `Evidence bundle` row in Document Control; all
  placeholders normalized to UPPERCASE so `cscan validate` catches them.

### Changed
- Purpose-aligned filenames (old → new):
  - `compliance/FULL-PROJECT-SCAN-METHODOLOGY.md` → `compliance/scan-methodology.md`
  - `compliance/README.md` (matrix) → `compliance/adr-compliance-matrix.md`
    (new slim `compliance/README.md` is a section index)
  - `prompts/scan-agent-prompt.md` → `prompts/compliance-scan-agent.md`
- All cross-references, badges, and invocation blocks updated to match.

## [1.0.0] - 2026-09-04

### Added
- Initial open-source release of the project-agnostic compliance scanning kit.
- `compliance/FULL-PROJECT-SCAN-METHODOLOGY.md`: 7-phase evidence-based audit
  procedure with variables table, exit criteria, and cross-platform notes.
- `compliance/README.md`: 31-commitment ADR matrix mapped to ISO 27001:2022,
  GDPR, and UU PDP No. 27/2022 (generalized, product-agnostic).
- `compliance/references/`: bundled GDPR source text and ISO 27001 Annex A
  93-control reference (kebab-case filenames).
- `templates/compliance-scan-report-template.md`: normative auditor-grade
  report skeleton (Document Control → Findings → Matrix → Sign-off).
- `prompts/scan-agent-prompt.md`: copy-paste AI agent invocation wrapper.
- Root `README.md`, `LICENSE` (MIT), `.gitignore`, `CHANGELOG.md`.

### Changed
- Scrubbed all prior-engagement coupling from the export: hard-coded product
  name, repository URL, agent/model name, assumed directories, region/sector
  examples, internal doc links, wikilinks, and mixed-language prose.
- Every scan command now takes scope as a variable; methodology fails closed
  on copied scope (Rule 11).

[1.2.0]: https://github.com/fentonmartin/compliance-scan-tools/releases/tag/v1.2.0
[1.1.0]: https://github.com/fentonmartin/compliance-scan-tools/releases/tag/v1.1.0
[1.0.0]: https://github.com/fentonmartin/compliance-scan-tools/releases/tag/v1.0.0
