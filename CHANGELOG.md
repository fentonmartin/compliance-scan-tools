# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/fentonmartin/compliance-scan-tools/releases/tag/v1.0.0
