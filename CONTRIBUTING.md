# Contributing to CSCAN Tools

Thank you for considering a contribution — corrections are the product here.
A wrong pattern, a mis-mapped ISO control, an unclear methodology step:
each one you fix makes someone else's audit more honest.

## Ways to contribute

| Contribution | Example | What to include |
|---|---|---|
| 🔍 New search pattern | A secret format `cscan search` misses | The regex, which group it joins, and a fixture proving it hits (see `tests/test_cscan.py`) |
| 📐 New / fixed commitment | A control the ADR matrix mis-maps | The matrix row with GDPR article + ISO Annex A control + UU PDP clause, each with a verbatim quote |
| 📝 Clearer docs | A methodology step agents misread | The paragraph, why it misleads, and the replacement wording |
| ⚙️ Tool improvement | A faster engine, a better receipt | Code + tests; must stay stdlib-only (Python 3.8+) |
| 🐛 Bug report | `validate` false-positives on your report | The minimal report snippet that reproduces it |

Don't ask permission first for small fixes — open the PR. For large changes
(new subcommand, new standard, new template section), open an issue so the
shape can be agreed before you build it.

## The five rules (from AGENTS.md)

1. **No hard-coded engagement values.** No product, repo, tenant, region,
   customer, or model names outside `<PLACEHOLDERS>`, marked
   `[Example: … — replace …]` illustrations, or quoted evidence.
2. **Template is normative.** `templates/compliance-scan-report-template.md`
   governs; if the methodology disagrees, fix the methodology.
3. **Existence protocol applies here too.** A claim a check "works" needs a
   test; a claim a pattern "finds X" needs a fixture.
4. **POSIX + PowerShell.** Both command forms where they differ; keep
   `tools/cscan.ps1` Windows PowerShell 5.1 compatible.
5. **Stdlib-only tool.** No dependencies in `tools/cscan.py`, ever.

## Dev loop

```bash
# verify the instrument (must pass before any PR)
python -m unittest discover -s tests -v

# validate a finished report
python tools/cscan.py validate --report <report>.md

# leak-guard the kit (must print nothing — see AGENTS.md for the command
# and its content-only scope)
```

Keep PRs small and single-purpose: one pattern, one mapping, one section.
A 20-line PR with a fixture merges in hours; a 500-line redesign needs the
issue conversation first.

## What makes a PR merge quickly

- It cites sources: control numbers, article numbers, or test output.
- It updates every cross-reference it breaks (prompts, template,
  methodology §10, README tree, CHANGELOG).
- Version strings stay in lockstep: `tools/cscan.py` (`VERSION`),
  `prompts/compliance-scan-agent.md`, `templates/…template.md`, README badges.
- Commit messages follow the existing style: `feat: …`, `fix: …`, `docs: …`.

## Conduct

Be kind, be precise, cite your sources. Disagree with findings, never with
people. Practice what the tool preaches: observation first, judgment second,
evidence always.
