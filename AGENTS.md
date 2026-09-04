# AGENTS.md — conventions for contributors (human or AI)

This repo is a **project-agnostic audit kit**. Every change must keep it
usable against an arbitrary target repository.

## Non-negotiable rules

1. **No hard-coded engagement values.** No product, repo, tenant, region,
   customer, or model names outside `<PLACEHOLDERS>`, explicitly marked
   `[Example: … — replace …]` illustrations, or quoted evidence. Copied
   scope from another engagement is a defect.
2. **Template is normative.** If `templates/compliance-scan-report-template.md`
   and `compliance/scan-methodology.md` disagree, the template governs —
   update the methodology to match.
3. **Existence protocol applies to kit changes too.** A claim that a check
   "works" needs a test; a claim that a pattern "finds X" needs a fixture.
   See `tests/test_cscan.py`.
4. **POSIX + PowerShell.** Document both command forms where they differ;
   keep `tools/cscan.ps1` compatible with Windows PowerShell 5.1 (no `?:`,
   no `??`).
5. **Stdlib-only tool.** `tools/cscan.py` must stay dependency-free
   (Python 3.8+) so it runs on any checkout.

## Workflows

```bash
# verify the instrument
python -m unittest discover -s tests -v

# validate a finished report
python tools/cscan.py validate --report <report>.md

# leak-guard the kit itself (must print nothing; scope is content-only —
# tools/cscan.py holds the intentional documented list, tests/ holds fixtures)
grep -rniE "nds-by-nat|fayolearn|big-pickle" \
  README.md compliance/ prompts/ templates/
```

## Cutting a release

1. Update `CHANGELOG.md` (rename map if paths moved).
2. Bump `VERSION` in `tools/cscan.py`, version strings in
   `prompts/compliance-scan-agent.md`, `templates/…template.md`,
   and badges in `README.md` — keep them in lockstep.
3. `git tag -a vX.Y.Z -m "…"` and push tag + branch.
