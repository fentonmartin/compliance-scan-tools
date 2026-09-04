# compliance/ — normative content

Product-agnostic compliance content verified by the scan methodology.
This directory names no product, repository, tenant, or vendor.

| File | Role |
|---|---|
| [`scan-methodology.md`](scan-methodology.md) | **Binding procedure.** 7-phase evidence-based scan protocol + existence protocol. The agent's brain — start here. |
| [`adr-compliance-matrix.md`](adr-compliance-matrix.md) | **Verification baseline.** 31 architectural commitments mapped to ISO 27001:2022, GDPR, and UU PDP No. 27/2022. Verified one-by-one in Phase 3. |
| `references/` | **Source texts** (offline audit convenience). GDPR regulation text + ISO 27001 Annex A 93-control reference. |

Executable instrument: [`../tools/cscan.py`](../tools/cscan.py) — evidence
freeze, inventory, pattern search with receipts, report scaffolding, and
report validation. See [`../prompts/compliance-scan-agent.md`](../prompts/compliance-scan-agent.md)
for the copy-paste invocation.
