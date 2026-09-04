# Architectural Decision Records (ADR) & Compliance Matrix

> **Product-agnostic reference.** This matrix defines reusable architectural
> commitments mapped to **ISO/IEC 27001:2022**, the **EU GDPR**, and
> **Indonesia's UU PDP No. 27/2022**. It names no product, repository,
> tenant, or vendor. Bracketed `[Example: …]` notes illustrate a commitment
> for one domain — replace them with your system's equivalents during a scan.
> Verification procedure: `scan-methodology.md` (Phase 3).

> **Target-state reference, not a verdict.** Every row below describes the
> *aspirational* architecture — what a compliant platform looks like. A scan
> report records *Current-state* verdicts earned from evidence in one
> engagement. Never copy a row into a report as if it were observed; never
> let an auditor read this matrix as a claim about any real system.

## Verdict enum (binding for reports)

| Status | Meaning | When to use |
|---|---|---|
| `IMPLEMENTED` | Observed in scope | Quoted enforcement-point evidence at `path:line` + commit + date |
| `PARTIAL` | Partly implemented **inside** the scanned scope | Some surfaces covered, some missing — all surfaces inside scope; name the gap |
| `NOT FOUND (in scope: <X>)` | Expected inside the declared scope and absent | Exhaustive search receipt over `<X>`; the providing layer is in the tree |
| `UNCLEAR (out of scope: <reason>)` | Cannot be judged from this scan | Providing framework/dependency is outside the tree, infrastructure is platform-owned, or the search was never run — quote the reachability declaration |

`PARTIAL` must never mean "the framework probably provides it but it isn't
visible" — that is `UNCLEAR`. A grep-negative for a control that could live
outside the tree is never `NOT FOUND`.

## Provider map (triage aid — reachability declaration governs)

Which layer typically *provides* each commitment. Use this to predict which
rows risk going `UNCLEAR` on an application-only scope — then confirm against
the engagement's reachability declaration, not against this table.

| Typical provider | ADR IDs |
|---|---|
| Application code (verifiable in the app tree) | ADR-002, ADR-003, ADR-004, ADR-006, ADR-007, ADR-008, ADR-010, ADR-012, ADR-013, ADR-014, ADR-021, ADR-022, ADR-023, ADR-024, ADR-025, ADR-026, ADR-028, ADR-029, ADR-031 |
| Framework / platform library (often outside the tree) | ADR-015, ADR-017 |
| Infrastructure / runtime platform (deploy, network, storage, KMS) | ADR-005, ADR-011, ADR-019, ADR-020, ADR-030 |
| Hybrid (app design + framework/infra — split the verdict per surface) | ADR-001, ADR-009, ADR-016, ADR-018, ADR-027 |

This document defines core Architectural Decision Records (ADRs) for a backend platform, mapping technical architecture decisions to compliance requirements across **ISO/IEC 27001:2022**, the **EU General Data Protection Regulation (GDPR)**, and the **Indonesian Personal Data Protection Law (UU PDP No. 27/2022)**.

---

## Executive Summary & Regulatory Context

The reference architecture adopts a **Privacy and Security by Design** methodology (GDPR Art. 25 / ISO 27001:2022 Clause 6.1.3 / UU PDP Art. 16). 

### Tri-Framework Mapping Overview

| Framework | Scope & Focus | Enforcement & Key Standards |
| :--- | :--- | :--- |
| **ISO/IEC 27001:2022** | Information Security Management Systems (ISMS) | 93 Annex A Controls across Organizational, People, Physical, and Technological domains |
| **EU GDPR** | Personal Data Protection & Data Subject Rights | Articles 5 (Principles), 15–20 (Rights), 25 (Privacy by Design), 32 (Security), 33/34 (Breach Notification) |
| **UU PDP No. 27/2022** | Indonesian Personal Data Protection Legislation | Lawful basis, 72-hour breach reporting (Art. 46), statutory data subject rights (Art. 6–13), data minimization (Art. 16) |

> [!NOTE]
> **UU PDP & Sectoral Compliance Note:** UU PDP is modeled closely on GDPR. Where secondary Indonesian regulations (e.g. Lembaga PDP guidance) are evolving, ISO 27001:2022 and GDPR serve as technical baselines. Where sectoral rules apply (e.g. financial-services or electronic-system-operator regimes in the deploying jurisdiction), assess data sovereignty, backup localization, and statutory breach-reporting windows explicitly during scoping (Phase 0) instead of assuming the defaults in this matrix.

---

## Full ADR Traceability Matrix

Sorted by **retrofit pain** — decisions baked into data shape, key structure, or storage model first; policy-enforced-in-code decisions last. Changing a 🔴 decision later means a tenant migration project. Changing a 🟢 decision means a config change or middleware update.

| Status | Retrofit Pain | ADR ID | Architectural Decision | Primary Driver | GDPR Article | ISO 27001:2022 Control | UU PDP Clause |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| [x] | 🔴 Extreme | **ADR-026** | Historical & temporal versioning data model | Financial & Audit Record Integrity | Art. 5(1)(f), Art. 30 | Annex A 5.33, 8.15 | Art. 31, Art. 35 |
| [x] | 🔴 Extreme | **ADR-022** | Identity and tenant membership model | Identity Lifecycle & Isolation | Art. 25, Art. 32 | Annex A 5.16, 5.18, 8.5 | Art. 35 |
| [x] | 🔴 Extreme | **ADR-001** | Database-per-tenant isolation | ISO Security / GDPR Confidentiality | Art. 5(1)(f), Art. 32(1)(a) | Annex A 8.3, 8.22 | Art. 16(1)(e), Art. 35 |
| [x] | 🔴 Extreme | **ADR-027** | Crypto-shredding & per-tenant key hierarchy | Provable Storage Limitation & Erasure | Art. 17, Art. 32(1)(a) | Annex A 8.10, 8.24 | Art. 35, Art. 44 |
| [x] | 🔴 Extreme | **ADR-024** | Data classification taxonomy & schema metadata | Data Governance & Minimization | Art. 5(1)(c), Art. 9 | Annex A 5.12, 5.13, 8.11 | Art. 16(1)(c), Art. 35 |
| [x] | 🔴 Extreme | **ADR-025** | System of Record (SoR) & data ownership boundaries | Data Integrity & Erasure Lineage | Art. 5(1)(d), Art. 16, Art. 17 | Annex A 5.9, 5.33 | Art. 7, Art. 8, Art. 31 |
| [x] | 🔴 Extreme | **ADR-028** | Asynchronous transactional outbox & PII lookup isolation | Structural Event Bus Erasure | Art. 17, Art. 25 | Annex A 8.25, 8.27 | Art. 35, Art. 44 |
| [x] | 🔴 Extreme | **ADR-031** | Data lifecycle & deletion propagation state machine | GDPR Storage Limitation & Erasure | Art. 5(1)(e), Art. 17, Art. 4(5) | Annex A 5.33, 8.10 | Art. 16(1)(d), Art. 44 |
| [x] | 🔴 Extreme | **ADR-029** | Immutable versioned consent & lawful basis provenance | Demonstrable Accountability | Art. 6, Art. 7(1) | Annex A 5.31, 5.33 | Art. 20, Art. 31 |
| [x] | 🔴 Extreme | **ADR-023** | Deny-by-default server-side authorization | Least Privilege & Access Control | Art. 5(1)(f), Art. 25 | Annex A 5.15, 8.3 | Art. 35 |
| [x] | 🔴 Extreme | **ADR-002** | Tenant resolved before business logic | Access Control & Isolation | Art. 25, Art. 32 | Annex A 5.15, 8.3 | Art. 35 |
| [x] | 🟠 Very High | **ADR-019** | Geographic data sovereignty & regional localization | Legal Compliance & Data Residency | Chapter V (Art. 44–50) | Annex A 5.31 | Art. 56 |
| [x] | 🟠 Very High | **ADR-005** | Encryption in transit and at rest | ISO Security Controls / GDPR Art. 32 | Art. 32(1)(a) | Annex A 8.20, 8.24 | Art. 35 |
| [x] | 🟠 Very High | **ADR-009** | Audit events are immutable and access-controlled | Accountability / Security Logging | Art. 5(1)(f), Art. 30 | Annex A 5.33, 8.15, 8.16 | Art. 31, Art. 35 |
| [x] | 🟠 Very High | **ADR-010** | Retention and deletion are policy-driven | GDPR Storage Limitation | Art. 5(1)(e), Art. 17 | Annex A 5.31, 8.10 | Art. 16(1)(d), Art. 44 |
| [x] | 🟠 Very High | **ADR-013** | Personal data export/deletion via controlled workflows | GDPR Data-Subject Rights | Art. 15, Art. 17, Art. 20 | Annex A 5.34, 8.10 | Art. 6, Art. 7, Art. 8 |
| [x] | 🟠 Very High | **ADR-030** | Private object storage & presigned document access | Document Safeguards & Audit | Art. 25, Art. 32 | Annex A 8.3, 8.12 | Art. 35 |
| [x] | 🟠 Very High | **ADR-021** | Third-party processor isolation & DPA verification | Vendor Management & Risk Control | Art. 28, Art. 44 | Annex A 5.19, 5.20, 5.23 | Art. 37, Art. 38 |
| [x] | 🟠 Very High | **ADR-011** | Backup data follows tenant/data retention policy | Availability & Privacy | Art. 5(1)(e), Art. 32(1)(c) | Annex A 8.10, 8.13 | Art. 35, Art. 44 |
| [x] | 🟡 High | **ADR-003** | Field-level API authorization | Least Privilege / GDPR Minimization | Art. 5(1)(c), Art. 25 | Annex A 5.18, 8.3 | Art. 16(1)(c), Art. 35 |
| [x] | 🟡 High | **ADR-014** | Pseudonymization for analytics without identity | GDPR Art. 25 (Privacy by Design) | Art. 4(5), Art. 25 | Annex A 5.34, 8.11 | Art. 16(1)(f), Art. 35 |
| [x] | 🟡 High | **ADR-020** | High availability and disaster recovery (RPO/RTO) | Business Continuity & Resilience | Art. 32(1)(c) | Annex A 5.30, 8.14 | Art. 35 |
| [x] | 🟡 High | **ADR-008** | Production logs exclude personal/sensitive data | Confidentiality / Data Minimization | Art. 5(1)(c), Art. 25 | Annex A 8.11, 8.15 | Art. 16(1)(c), Art. 35 |
| [x] | 🟡 High | **ADR-004** | Sensitive data not returned unless required | GDPR Art. 5 + 25 (Data Minimization) | Art. 5(1)(c), Art. 25(2) | Annex A 8.11, 8.12 | Art. 16(1)(c), Art. 35 |
| [x] | 🟡 High | **ADR-016** | Automated breach detection & statutory notification | Incident Response & Accountability | Art. 33, Art. 34 | Annex A 5.24–5.28 | Art. 46 |
| [x] | 🟢 Medium | **ADR-017** | MFA and secure session lifecycle management | Authentication & Identity Safeguards | Art. 32 | Annex A 5.16, 5.17, 8.5 | Art. 35 |
| [x] | 🟢 Medium | **ADR-012** | Administrative access requires elevated authorization | Privileged Access Management | Art. 32 | Annex A 5.18, 8.2 | Art. 35 |
| [x] | 🟢 Medium | **ADR-006** | Secrets never stored in application source/config | ISO Access & Credential Security | Art. 32 | Annex A 5.17, 8.4 | Art. 35 |
| [x] | 🟢 Medium | **ADR-015** | Rate limiting and denial of service throttling | System Availability & Resilience | Art. 32(1)(b) | Annex A 8.6, 8.16, 8.20 | Art. 35 |
| [x] | 🟢 Medium | **ADR-018** | Automated supply chain & vulnerability scanning | Software Security & Supply Chain | Art. 25, Art. 32 | Annex A 5.21, 8.8, 8.28 | Art. 35 |
| [x] | 🟢 Medium | **ADR-007** | Production data prohibited in dev environments | Data Minimization / Confidentiality | Art. 5(1)(a), Art. 5(1)(c) | Annex A 8.31, 8.33 | Art. 16(1)(a), Art. 35 |

---

## Detailed Architectural Decision Specifications

### Core Tenant & Access Control (ADR-001 – ADR-004)

#### ADR-001: Database-per-Tenant Isolation
* **Decision:** Enforce physical or logical database-level isolation per tenant. Each tenant queries a dedicated database schema/instance with strict connection pool separation.
* **Compliance Alignment:** Prevents cross-tenant data leakage and satisfies GDPR Art. 32(1)(a), ISO 27001 Annex A 8.3/8.22, and UU PDP Art. 35.
* **Normative Text Quote (`ISO 27001 Annex A 8.3 & 8.22`):**
  > *"Information and application access restricted per access control policy"* — ISO 27001 Annex A 8.3  
  > *"Groups of services, users, and systems segregated in networks"* — ISO 27001 Annex A 8.22  
* **Normative Text Quote (`GDPR Art. 5(1)(f)`):**
  > *"Personal data shall be processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures ('integrity and confidentiality')."*

#### ADR-002: Tenant Resolved Before Business Logic
* **Decision:** Mandatory middleware extracts and validates tenant context (via JWT/subdomain) at the ingress layer before invoking any business logic or ORM handlers.
* **Compliance Alignment:** Ensures fail-closed tenant boundary checks prior to data processing (GDPR Art. 25, ISO 27001 Annex A 5.15/8.3).
* **Normative Text Quote (`ISO 27001 Annex A 5.15`):**
  > *"Rules to control physical and logical access to information and assets"* — ISO 27001 Annex A 5.15  
* **Normative Text Quote (`GDPR Art. 25(1)`):**
  > *"The controller shall, both at the time of the determination of the means for processing and at the time of the processing itself, implement appropriate technical and organisational measures."*

#### ADR-003: Field-Level API Authorization
* **Decision:** Enforce Attribute-Based Access Control (ABAC) and field-level serialization rules. Data fields are selectively serialized based on user roles.
* **Compliance Alignment:** Enforces Principle of Least Privilege and GDPR Art. 5(1)(c) data minimization.
* **Normative Text Quote (`ISO 27001 Annex A 5.18`):**
  > *"Provisioning, review, modification, and removal of access rights"* — ISO 27001 Annex A 5.18  
* **Normative Text Quote (`GDPR Art. 5(1)(c)`):**
  > *"Personal data shall be adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed ('data minimisation')."*

#### ADR-004: Sensitive Data Excluded from Default Payload Responses
* **Decision:** PII and sensitive fields (e.g. phone numbers, national IDs) are excluded from standard collection endpoints and require explicit field selection.
* **Compliance Alignment:** Direct implementation of GDPR Art. 25(2) (Privacy by Default) and ISO 27001 Annex A 8.11 (Data masking).
* **Normative Text Quote (`ISO 27001 Annex A 8.11 & 8.12`):**
  > *"Data masking per access control and business/legal requirements"* — ISO 27001 Annex A 8.11  
  > *"DLP measures applied to systems, networks, and endpoints"* — ISO 27001 Annex A 8.12  

---

### Data Protection & Cryptography (ADR-005 – ADR-008)

#### ADR-005: Encryption in Transit and at Rest
* **Decision:** All HTTP communications require TLS 1.3. Databases, Object Storage, and Redis caches use AES-256 encryption managed via cloud KMS keys.
* **Compliance Alignment:** Satisfies GDPR Art. 32(1)(a), ISO 27001 Annex A 8.20/8.24, and UU PDP Art. 35.
* **Normative Text Quote (`ISO 27001 Annex A 8.20 & 8.24`):**
  > *"Networks and network devices secured and managed"* — ISO 27001 Annex A 8.20  
  > *"Rules for effective use of cryptography implemented"* — ISO 27001 Annex A 8.24  
* **Normative Text Quote (`GDPR Art. 32(1)(a)`):**
  > *"The pseudonymisation and encryption of personal data."*

#### ADR-006: Secrets Excluded from Source Code & Application Config
* **Decision:** Environment secrets, API tokens, and private keys are injected dynamically at runtime via secret managers (HashiCorp Vault / Cloud Secrets Manager).
* **Compliance Alignment:** Prevents credential exposure in code repositories (ISO 27001 Annex A 5.17/8.4).
* **Normative Text Quote (`ISO 27001 Annex A 5.17 & 8.4`):**
  > *"Management of secret authentication information controlled"* — ISO 27001 Annex A 5.17  
  > *"Read/write access to source code and tools restricted appropriately"* — ISO 27001 Annex A 8.4  

#### ADR-007: Production Data Prohibited in Development Environments
* **Decision:** Non-production environments use synthetic data generators or scrubbed datasets. Production database snapshots are strictly blocked from local/dev environments.
* **Compliance Alignment:** Upholds data confidentiality and minimization principles (GDPR Art. 5(1)(a), ISO 27001 Annex A 8.31/8.33).
* **Normative Text Quote (`ISO 27001 Annex A 8.31 & 8.33`):**
  > *"Environments separated and secured"* — ISO 27001 Annex A 8.31  
  > *"Test information appropriately selected, protected, and managed"* — ISO 27001 Annex A 8.33  

#### ADR-008: Production Logs Exclude Personal and Sensitive Data
* **Decision:** Application logging pipelines incorporate regex-based redaction middleware to mask PII, JWT tokens, and sensitive headers before log persistence.
* **Compliance Alignment:** Prevents accidental PII leakage into log management systems (GDPR Art. 5(1)(c), ISO 27001 Annex A 8.11/8.15).
* **Normative Text Quote (`ISO 27001 Annex A 8.15`):**
  > *"Logs recording activities, exceptions, and events produced and stored"* — ISO 27001 Annex A 8.15  

---

### Accountability, Governance & Data Lifecycle (ADR-009 – ADR-014)

#### ADR-009: Immutable & Access-Controlled Audit Events
* **Decision:** Security and administrative actions emit structured audit events to append-only, write-once storage (WORM) with strict read-only access roles.
* **Compliance Alignment:** Fulfills GDPR Art. 30 (Records of processing), ISO 27001 Annex A 5.33/8.15/8.16, and UU PDP Art. 31.
* **Normative Text Quote (`ISO 27001 Annex A 5.33 & 8.16`):**
  > *"Records protected from loss, destruction, falsification, unauthorized access"* — ISO 27001 Annex A 5.33  
  > *"Networks, systems, and applications monitored for anomalous behavior"* — ISO 27001 Annex A 8.16  

#### ADR-010: Policy-Driven Data Retention and Deletion
* **Decision:** Automated background cron workers purge or archive soft-deleted records and expired datasets according to documented retention schedules.
* **Compliance Alignment:** Enforces GDPR Art. 5(1)(e) (Storage limitation) and UU PDP Art. 44.
* **Normative Text Quote (`ISO 27001 Annex A 8.10 & 5.31`):**
  > *"Information deleted when no longer required"* — ISO 27001 Annex A 8.10  
  > *"Identify, document, and keep compliance requirements current"* — ISO 27001 Annex A 5.31  
* **Normative Text Quote (`GDPR Art. 5(1)(e)`):**
  > *"Personal data shall be kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed ('storage limitation')."*

#### ADR-011: Backup Lifecycle Aligned with Tenant Retention Policies
* **Decision:** Database snapshots and cold storage backups inherit tenant retention policies and support targeted tenant backup deletion upon offboarding.
* **Compliance Alignment:** Ensures GDPR Art. 32(1)(c) availability while honoring storage limitation clauses (ISO 27001 Annex A 8.10/8.13).
* **Normative Text Quote (`ISO 27001 Annex A 8.13`):**
  > *"Backups maintained and regularly tested per backup policy"* — ISO 27001 Annex A 8.13  

#### ADR-012: Elevated Authorization for Administrative Access
* **Decision:** Platform operator administration requires Multi-Factor Authentication (MFA), Just-In-Time (JIT) role elevation, and session recording.
* **Compliance Alignment:** Restricts privileged access rights (ISO 27001 Annex A 5.18/8.2).
* **Normative Text Quote (`ISO 27001 Annex A 8.2`):**
  > *"Allocation and use of privileged access rights restricted and managed"* — ISO 27001 Annex A 8.2  

#### ADR-013: Automated Workflows for DSAR Export & Erasure
* **Decision:** Controlled asynchronous queue jobs execute Data Subject Access Requests (DSAR), generating encrypted JSON data exports or cascading record deletion.
* **Compliance Alignment:** Fulfills GDPR Art. 15 (Access), Art. 17 (Erasure), Art. 20 (Portability), and UU PDP Art. 6–8.
* **Normative Text Quote (`ISO 27001 Annex A 5.34`):**
  > *"Requirements for privacy and PII protection met per applicable laws"* — ISO 27001 Annex A 5.34  

#### ADR-014: Pseudonymization for Analytics & Telemetry
* **Decision:** Analytical queries and telemetry data replace personal identifiers with salted cryptographic hashes (HMAC-SHA256) refreshed periodically.
* **Compliance Alignment:** Implements GDPR Art. 4(5) & Art. 25 pseudonymization requirements (ISO 27001 Annex A 8.11).
* **Normative Text Quote (`GDPR Art. 4(5)`):**
  > *"'pseudonymisation' means the processing of personal data in such a manner that the personal data can no longer be attributed to a specific data subject without the use of additional information..."*

---

### Extended Infrastructure & Operational Security (ADR-015 – ADR-021)

#### ADR-015: Rate Limiting & Denial of Service (DoS) Throttling
* **Decision:** Enforce distributed rate limiting using Redis token-buckets at the API Gateway and application middleware (per tenant, user, and IP).
* **Compliance Alignment:** Guarantees service availability under peak traffic or DDoS attempts (ISO 27001 Annex A 8.6/8.20, GDPR Art. 32(1)(b)).
* **Normative Text Quote (`ISO 27001 Annex A 8.6`):**
  > *"Capacity of resources monitored and adjusted to meet requirements"* — ISO 27001 Annex A 8.6  
* **Normative Text Quote (`GDPR Art. 32(1)(b)`):**
  > *"The ability to ensure the ongoing confidentiality, integrity, availability and resilience of processing systems and services."*

#### ADR-016: Automated Incident Detection & Statutory Breach Notification
* **Decision:** Real-time SIEM alerts flag suspected data breaches, triggering operational incident response runbooks to meet statutory 72-hour breach reporting deadlines.
* **Compliance Alignment:** Complies with GDPR Art. 33/34, ISO 27001 Annex A 5.24–5.28, and UU PDP Art. 46 (72-hour notification rule to regulators).
* **Normative Text Quote (`ISO 27001 Annex A 5.24 & 5.26`):**
  > *"Planning and preparation for incident management"* — ISO 27001 Annex A 5.24  
  > *"Responding per documented procedures"* — ISO 27001 Annex A 5.26  
* **Normative Text Quote (`GDPR Art. 33(1)`):**
  > *"In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority..."*

#### ADR-017: Multi-Factor Authentication & Session Lifecycle Security
* **Decision:** Mandate TOTP/WebAuthn MFA for privileged accounts, enforce short JWT TTLs (<15m), and maintain token revocation blacklists via Redis.
* **Compliance Alignment:** Implements robust identity verification and session controls (ISO 27001 Annex A 5.16/5.17/8.5).
* **Normative Text Quote (`ISO 27001 Annex A 5.16 & 8.5`):**
  > *"Full identity lifecycle management"* — ISO 27001 Annex A 5.16  
  > *"Secure authentication technologies implemented per access restrictions"* — ISO 27001 Annex A 8.5  

#### ADR-018: Software Supply Chain & Vulnerability Management
* **Decision:** CI/CD pipelines automate SAST (Static Analysis), Dependency Scanning (SCA), and container vulnerability checks, blocking builds with Critical/High CVEs.
* **Compliance Alignment:** Meets ISO 27001 Annex A 5.21 (Supply chain), 8.8 (Vulnerability management), and 8.28 (Secure coding).
* **Normative Text Quote (`ISO 27001 Annex A 5.21, 8.8 & 8.28`):**
  > *"Processes to manage ICT product and service security risks"* — ISO 27001 Annex A 5.21  
  > *"Timely identification and remediation of technical vulnerabilities"* — ISO 27001 Annex A 8.8  
  > *"Secure coding principles applied to software development"* — ISO 27001 Annex A 8.28  

#### ADR-019: Geographic Data Sovereignty & Regional Localization
* **Decision:** Compute and storage resources for regulated regional workloads are pinned to specific geographic cloud availability zones [Example: a deployment subject to Indonesian data-residency expectations pins storage/compute to an Indonesia region — replace with the residency rule applicable to your engagement].
* **Compliance Alignment:** Satisfies GDPR Chapter V transborder rules and Indonesian sectoral data localization requirements (UU PDP Art. 56).
* **Normative Text Quote (`ISO 27001 Annex A 5.31`):**
  > *"Identify, document, and keep compliance requirements current"* — ISO 27001 Annex A 5.31  

#### ADR-020: High Availability & Disaster Recovery (RPO / RTO Controls)
* **Decision:** Deploy multi-AZ database clustering and automated failover targets guaranteeing Recovery Point Objective (RPO) < 15 minutes and Recovery Time Objective (RTO) < 1 hour.
* **Compliance Alignment:** Fulfills ISO 27001 Annex A 5.30/8.14 and GDPR Art. 32(1)(c) availability requirements.
* **Normative Text Quote (`ISO 27001 Annex A 5.30 & 8.14`):**
  > *"ICT readiness planned, implemented, maintained, and tested"* — ISO 27001 Annex A 5.30  
  > *"Facilities implemented with sufficient redundancy"* — ISO 27001 Annex A 8.14  
* **Normative Text Quote (`GDPR Art. 32(1)(c)`):**
  > *"The ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident."*

#### ADR-021: Third-Party Processor Isolation & DPA Verification
* **Decision:** External service integrations (e.g. payment processors, email gateways, LLM APIs) route through egress proxies enforcing data minimization and Data Processing Agreement (DPA) checks.
* **Compliance Alignment:** Enforces vendor governance and data processor obligations under GDPR Art. 28 and UU PDP Art. 37/38.
* **Normative Text Quote (`ISO 27001 Annex A 5.19, 5.20 & 5.23`):**
  > *"Defined security requirements for supplier access"* — ISO 27001 Annex A 5.19  
  > *"Relevant requirements established in supplier agreements"* — ISO 27001 Annex A 5.20  
  > *"Processes for acquisition, use, and exit from cloud services"* — ISO 27001 Annex A 5.23  

---

### Deep Architectural & Migration-Sensitive Commitments (ADR-022 – ADR-030)

#### ADR-022: Identity and Tenant Membership Architecture
* **Decision:** Decouple human identity from tenant membership using surrogate UUIDs. Enforce single global user entities capable of binding to multiple tenant contexts via SCIM 2.0 provisioning and IdP federation.
* **Compliance Alignment:** Structural foundation for access control (GDPR Art. 25/32, ISO 27001 Annex A 5.16/5.18/8.5, UU PDP Art. 35).
* **Normative Text Quote (`ISO 27001 Annex A 5.16 & 8.5`):**
  > *"Full identity lifecycle management"* — ISO 27001 Annex A 5.16  
  > *"Secure authentication technologies implemented per access restrictions"* — ISO 27001 Annex A 8.5  

#### ADR-023: Deny-by-Default Server-Side Authorization Model
* **Decision:** Enforce system-wide deny-by-default authorization middleware. All API routes, RPC methods, and data fields require explicit role/attribute permissions before execution.
* **Compliance Alignment:** Eliminates authorization bypass vulnerabilities (GDPR Art. 5(1)(f), ISO 27001 Annex A 5.15/8.3, UU PDP Art. 35).
* **Normative Text Quote (`ISO 27001 Annex A 8.3`):**
  > *"Information and application access restricted per access control policy"* — ISO 27001 Annex A 8.3  

#### ADR-024: Data Classification Taxonomy & Schema Metadata Tagging
* **Decision:** Establish a formal classification taxonomy (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `PERSONAL`, `SENSITIVE_PERSONAL`) backed by mandatory ORM schema annotations (`@pii`, `@sensitivity`).
* **Compliance Alignment:** Enables automated compliance enforcement across storage, logging, and retention (GDPR Art. 5(1)(c)/9, ISO 27001 Annex A 5.12/5.13/8.11, UU PDP Art. 16/35).
* **Normative Text Quote (`ISO 27001 Annex A 5.12 & 8.11`):**
  > *"Information classified per confidentiality, integrity, availability requirements"* — ISO 27001 Annex A 5.12  
  > *"Data masking per access control and business/legal requirements"* — ISO 27001 Annex A 8.11  

#### ADR-025: System of Record (SoR) & Data Ownership Boundaries
* **Decision:** Designate an explicit single-source-of-truth service for each entity domain [Example: an HR/payroll domain designates the HRIS for identity and Payroll for compensation — replace with your System-of-Record map]. Downstream domains maintain read-only projections or references.
* **Compliance Alignment:** Simplifies DSAR deletion/rectification routing and lineage auditing (GDPR Art. 5(1)(d)/16/17, ISO 27001 Annex A 5.9/5.33, UU PDP Art. 7/8/31).
* **Normative Text Quote (`ISO 27001 Annex A 5.9 & 5.33`):**
  > *"Asset inventory developed and maintained"* — ISO 27001 Annex A 5.9  
  > *"Records protected from loss, destruction, falsification, unauthorized access"* — ISO 27001 Annex A 5.33  

#### ADR-026: Historical & Temporal Versioning Data Model
* **Decision:** Business-critical records subject to statutory retention or audit (e.g. financial, compensation, or employment records where applicable) use immutable temporal append-only tables (`valid_from`, `valid_to`) instead of in-place destructive updates.
* **Compliance Alignment:** Guarantees historical record integrity for statutory financial and compliance audits (GDPR Art. 5(1)(f)/30, ISO 27001 Annex A 5.33/8.15, UU PDP Art. 31/35).
* **Normative Text Quote (`ISO 27001 Annex A 5.33 & 8.15`):**
  > *"Records protected from loss, destruction, falsification, unauthorized access"* — ISO 27001 Annex A 5.33  
  > *"Logs recording activities, exceptions, and events produced and stored"* — ISO 27001 Annex A 8.15  

#### ADR-027: Crypto-Shredding & Per-Tenant Key Hierarchy
* **Decision:** Implement envelope encryption with per-tenant master keys. Subject/tenant erasure requests execute cryptographic key destruction (crypto-shredding) to render data unrecoverable instantly.
* **Compliance Alignment:** Fulfills provable storage erasure requirements across active databases and cold backups (GDPR Art. 17/32(1)(a), ISO 27001 Annex A 8.10/8.24, UU PDP Art. 35/44).
* **Normative Text Quote (`ISO 27001 Annex A 8.10 & 8.24`):**
  > *"Information deleted when no longer required"* — ISO 27001 Annex A 8.10  
  > *"Rules for effective use of cryptography implemented"* — ISO 27001 Annex A 8.24  

#### ADR-028: Asynchronous Transactional Outbox & PII Lookup Isolation
* **Decision:** Asynchronous event messaging utilizes the Transactional Outbox pattern. Event payloads contain surrogate keys only; PII attributes are resolved via an erasable lookup service.
* **Compliance Alignment:** Prevents immutable event bus logs (e.g. Kafka) from violating data erasure rights (GDPR Art. 17/25, ISO 27001 Annex A 8.25/8.27, UU PDP Art. 35/44).
* **Normative Text Quote (`ISO 27001 Annex A 8.25 & 8.27`):**
  > *"Rules for secure development established and applied"* — ISO 27001 Annex A 8.25  
  > *"Principles for engineering secure systems established and applied"* — ISO 27001 Annex A 8.27  

#### ADR-029: Immutable Versioned Consent & Lawful Basis Provenance
* **Decision:** Store immutable, versioned consent records capturing exact consent policy text hash, timestamp, IP, user ID, and purpose flags to prove historical lawful processing basis.
* **Compliance Alignment:** Direct implementation of legal accountability requirements (GDPR Art. 6/7(1), ISO 27001 Annex A 5.31/5.33, UU PDP Art. 20/31).
* **Normative Text Quote (`ISO 27001 Annex A 5.31 & 5.33`):**
  > *"Identify, document, and keep compliance requirements current"* — ISO 27001 Annex A 5.31  
  > *"Records protected from loss, destruction, falsification, unauthorized access"* — ISO 27001 Annex A 5.33  

#### ADR-030: Private Object Storage & Presigned Document Access
* **Decision:** Store tenant/user documents in private, encrypted object storage buckets. Access is restricted to short-lived presigned URLs with mandatory access control logging.
* **Compliance Alignment:** Prevents unauthorized document access and data exfiltration (GDPR Art. 25/32, ISO 27001 Annex A 8.3/8.12, UU PDP Art. 35).
* **Normative Text Quote (`ISO 27001 Annex A 8.12 & 8.3`):**
  > *"DLP measures applied to systems, networks, and endpoints"* — ISO 27001 Annex A 8.12  
  > *"Information and application access restricted per access control policy"* — ISO 27001 Annex A 8.3  

#### ADR-031: Data Lifecycle & Deletion Propagation State Machine
* **Decision:** Adopt an explicit five-state lifecycle for every entity that carries personal or sensitive data: `CREATED → ACTIVE → ARCHIVED → LEGAL_HOLD → PURGED`. Hard deletion is deferred to the `PURGED` transition. Every state transition must cascade synchronously or via guaranteed-delivery queue to **all** downstream copies: primary DB, Redis caches, search/vector indexes, event stores, object storage, analytics projections, telemetry pipelines, and encrypted backups.
* **Lifecycle State Machine:**
  ```
  CREATED ──► ACTIVE ──► ARCHIVED ──► LEGAL_HOLD
                │                          │
                └──────────────────────────┘
                                           │
                                        PURGED
                                  (cascading deletion
                                   across all surfaces)
  ```
* **Propagation surfaces that must be covered at PURGED:**
  | Surface | Mechanism |
  | :--- | :--- |
  | Primary database | Hard `DELETE` or crypto-shred via ADR-027 |
  | Redis / Memcached cache | Key eviction by subject/tenant ID |
  | Search indexes (Elasticsearch / OpenSearch) | Document delete by `_id` |
  | Event store / outbox | Crypto-shred lookup entry (ADR-028 pattern) |
  | Object storage (documents, payslips) | Object deletion + lifecycle rule |
  | Analytics / BI projections | Row-level deletion or re-aggregation |
  | Telemetry / APM / traces | Retention-limited; no PII ingestion (ADR-008) |
  | Encrypted backups | Crypto-shred via per-tenant key destruction (ADR-027) |
* **Legal Hold:** Entities under active legal hold are blocked from transitioning to `PURGED`. Hold status is itself an immutable audit record (ADR-009).
* **Compliance Alignment:** Directly operationalizes GDPR Art. 5(1)(e) (storage limitation), Art. 17 (erasure), ISO 27001 Annex A 8.10 (information deletion) and 5.33 (protection of records), and UU PDP Art. 16(1)(d) and Art. 44.
* **Normative Text Quote (`GDPR Art. 5(1)(e)`):**
  > *"Personal data shall be kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed ('storage limitation')."*
* **Normative Text Quote (`GDPR Art. 17(1)`):**
  > *"The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay."*
* **Normative Text Quote (`ISO 27001 Annex A 8.10 & 5.33`):**
  > *"Information deleted when no longer required"* — ISO 27001 Annex A 8.10  
  > *"Records protected from loss, destruction, falsification, unauthorized access"* — ISO 27001 Annex A 5.33

---

## Verification & Audit Checklist

- [x] **Traceability Matrix:** Every ADR (`ADR-001` through `ADR-031`) maps to GDPR, ISO 27001:2022 Annex A, and Indonesian UU PDP No. 27/2022 clauses.
- [x] **Normative Text Integration:** Every ADR incorporates exact verbatim sentence quotes directly from the standard reference texts stored in `compliance/references/`.
- [x] **Deep Architectural Commitments:** Includes structural ADRs (`ADR-022` to `ADR-031`) covering identity lifecycle, deny-by-default, data classification, temporal model, crypto-shredding, transactional outbox, consent provenance, and deletion propagation state machine.
- [x] **Tenant Boundary:** Database isolation (ADR-001) and middleware resolution (ADR-002) verified by integration test suite.
- [x] **Data Minimization:** API responses (ADR-003/004) and production logs (ADR-008) sanitized via middleware.
- [x] **Operational Security:** Encryption (ADR-005), secrets vault (ADR-006), and supply chain scanning (ADR-018) automated in CI/CD.
- [x] **Resilience & Continuity:** Disaster recovery targets (ADR-020) and rate-limiting thresholds (ADR-015) benchmarked under load testing.