# ISO 27001 Annex A Controls List: All 93 Controls by Theme 

The 2022 revision of ISO 27001 restructured its control framework from 114 controls across 14 domains into 93 controls organized under four themes and for US-based GRC and information security professionals, that reorganization carries real implications for audit readiness, NIST CSF 2.0 alignment, and certification timelines. 

Whether you’re scoping an Information Security Management System (ISMS) for the first time, preparing for a Stage 2 audit, or mapping controls to SOC 2, HIPAA, CMMC 2.0, or FedRAMP, this reference covers every control in Annex A, organized by theme, with the context needed to act on them. 

What Annex A Actually Is (and What It Isn’t) 

Annex A of ISO/IEC 27001:2022 is a reference set of information security controls not a mandatory checklist. Every control in the annex is available to you when building your ISMS, but which ones apply depends entirely on your risk assessment results and the Statement of Applicability (SoA) you produce. 

This distinction matters for certification. During a Stage 2 audit, your lead auditor will not expect every one of the 93 controls to be implemented. What they will expect is that your SoA justifies every exclusion and that the controls you have implemented are operating effectively. Selecting controls simply because they appear in the annex without tying them to identified risks is one of the most common implementation errors US organizations make. 

The 2022 version consolidated the previous 114 controls (from 14 domains in ISO 27001:2013) into 93 controls under four themes: Organizational, People, Physical, and Technological. Eleven controls are entirely new to this revision. Each control also carries one or more attributes purpose, security concept (CIA triad component), operational capability, and security domain that let organizations filter the control set by use case. 

Key Distinction: Reference vs. Requirement – Annex A controls are informative, not prescriptive. Clause 6.1.3 of the standard requires you to compare your risk treatment options against Annex A, but your organization can also implement controls not listed in the annex if your risk assessment identifies the need. 

## The Four-Theme Structure at a Glance 

The four themes in ISO 27001:2022 Annex A group controls by the nature of what they govern rather than by technical domain. That shift from domain-based to attribute-based organization is deliberate it makes the control set easier to apply across different organizational sizes and industries. 

|Theme|Control<br>Range|Number of<br>Controls|Focus Area|
|---|---|---|---|
|5 –<br>Organizational|5.1–5.37|37|Policies, roles, supplier relationships,<br>asset management, information<br>classification|
||||Screening, employment terms,|
|6 – People|6.1–6.8|8|awareness, disciplinary process, remote<br>work|
|7 – Physical|7.1–7.14|14|Secure areas, equipment, clear<br>desk/screen, cabling, asset disposal|
|8 –<br>Technological|8.1–8.34|34|Access control, cryptography, malware<br>protection, SIEM, vulnerability<br>management|



The weighting toward Organizational (37 controls) and Technological (34 controls) reflects where most information security risk actually concentrates in modern enterprises. People controls are relatively few eight controls but they represent some of the hardest to operationalize, particularly in US organizations navigating state-level privacy laws that restrict what screening and monitoring is permissible. 

## Theme 5: Organizational Controls (5.1–5.37) 

Organizational controls establish the governance foundation that everything else rests on. Without effective policies, roles, asset inventories, and supplier agreements, the technical 

controls in Theme 8 have no coherent direction. 

|Control<br>ID|Control Name|Brief Description|
|---|---|---|
|||Defined, approved, communicated, and|
|5.1|Policies for information security|regularly reviewed information security<br>policies|
|5.2|Information security roles and<br>responsibilities|Allocated and communicated security<br>roles across the organization|
|||Conflicting duties and areas of|
|5.3|Segregation of duties|responsibility separated to reduce misuse<br>risk|
|5.4|Management responsibilities|Management requires personnel to apply<br>security per organizational policies|
|5.5|Contact with authorities|Defined contacts with relevant authorities<br>(law enforcement, regulators)|
|5.6|Contact with special interest<br>groups|Maintained membership in professional<br>groups and specialist forums|
|5.7|Threat intelligence|NEW Collect and analyze threat<br>intelligence to inform security decisions|
|5.8|Information security in project<br>management|Security integrated into project<br>management methodology|
|5.9|Inventory of information and<br>other associated assets|Asset inventory developed and<br>maintained|



|Control<br>ID|Control Name|Brief Description|
|---|---|---|
|5.10|Acceptable use of information<br>and associated assets|Rules for acceptable use identified,<br>documented, and implemented|
|5.11|Return of assets|Personnel return assets upon<br>employment termination|
|5.12|Classification of information|Information classified per confidentiality,<br>integrity, availability requirements|
|5.13|Labelling of information|Labelling procedures implemented per<br>classification scheme|
|5.14|Information transfer|Transfer policies for all transfer types:<br>electronic, physical, verbal|
|5.15|Access control|Rules to control physical and logical<br>access to information and assets|
|5.16|Identity management|Full identity lifecycle management|
|5.17|Authentication information|Management of secret authentication<br>information controlled|
|5.18|Access rights|Provisioning, review, modification, and<br>removal of access rights|
|5.19|Information security in supplier<br>relationships|Defined security requirements for<br>supplier access|
|5.20|Addressing information security<br>within supplier agreements|Relevant requirements established in<br>supplier agreements|



#### Control 

#### ID 

#### Control Name 

#### Brief Description 

- Managing information security in NEW Processes to manage ICT product 

- 5.21 the ICT supply chain and service security risks Monitoring, review, and change Regular monitoring and review of 

- 5.22 management of supplier services supplier security Information security for use of NEW Processes for acquisition, use, and 

- 5.23 cloud services exit from cloud services Information security incident Planning and preparation for incident 

- 5.24 management planning and management 

- preparation Assessment and decision on Evaluating events and deciding whether 

- 5.25 information security events to classify as incidents Response to information security 

- 5.26 Responding per documented procedures incidents Learning from information Knowledge from incidents used to reduce 

- 5.27 security incidents future probability/impact Establishing and implementing 

- 5.28 Collection of evidence procedures for collecting evidence 

- Information security during Planning security continuation during 

- 5.29 disruption disruption ICT readiness for business NEW ICT readiness planned, 

- 5.30 continuity implemented, maintained, and tested 

|Control<br>ID|Control Name|Brief Description|
|---|---|---|
|5.31|Legal, statutory, regulatory, and<br>contractual requirements|Identify, document, and keep compliance<br>requirements current|
|5.32|Intellectual property rights|Procedures implementing protection of<br>intellectual property|
|5.33|Protection of records|Records protected from loss, destruction,<br>falsification, unauthorized access|
|5.34|Privacy and protection of PII|Requirements for privacy and PII<br>protection met per applicable laws|
|5.35|Independent review of<br>information security|ISMS implementation reviewed<br>independently at planned intervals|
|5.36|Compliance with policies, rules,<br>and standards|Regular reviews of compliance with<br>policies and standards|
|537|Documented operating|Operating procedures documented and|
|.|procedures|made available to authorized personnel|



For US organizations, controls 5.19–5.23 (supplier and cloud security) warrant close attention. The NIST SP 800-53 Rev. 5 Supply Chain Risk Management (SR) control family maps tightly here, and CMMC 2.0 Level 2 organizations will find significant overlap with their third-party risk management requirements. Control 5.7 (Threat Intelligence) is new to the 2022 version and often surprises implementation teams it requires a structured process, not just subscribing to threat feeds. 

## Theme 6: People Controls (6.1–6.8) 

Eight controls govern the human dimension of information security. That’s a small number, but the complexity lies in the intersection with US employment law, state privacy regulations, and the practical challenge of building genuine security awareness rather than checkbox training. 

|Control<br>ID|Control Name|Brief Description|
|---|---|---|
|||Background verification checks on|
|6.1|Screening|candidates per laws, regulations, and<br>ethics|
|6.2|Terms and conditions of<br>employment|Employment contracts state security<br>responsibilities|
|6.3|Information security awareness,<br>education, and training|Personnel receive appropriate<br>awareness and training<br>Formalized and communicated|
|6.4|Disciplinary process|disciplinary process for security<br>violations|
|6.5|Responsibilities after termination<br>or change of employment|Security responsibilities and duties<br>remain after role change|
|6.6|Confidentiality or non-disclosure<br>agreements|NDAs identified, documented, reviewed,<br>and signed|
|6.7|Remote working|Security measures when working<br>remotely implemented and|



Control ID 

Control Name 

#### Brief Description 

communicated Information security event Mechanism for personnel to report 6.8 reporting observed or suspected events 

Control 6.3 (Awareness, Education, and Training) sounds straightforward but often delivers the least value in practice. Sending annual phishing simulations and compliance videos satisfies the letter of the control but not the spirit. Effective programs target role-specific risks what a developer needs to know about secure coding differs substantially from what an HR manager needs to know about handling sensitive personal data. 

Control 6.7 (Remote Working) took on new urgency post-2020. For US organizations with distributed workforces spanning multiple states, implementation needs to account for varying state-level data protection requirements and device management policies that hold up under cross-state scrutiny. 

## Theme 7: Physical Controls (7.1–7.14) 

Physical security controls are frequently underestimated in purely cloud-focused organizations. But even organizations with no on-premises servers have physical assets endpoints, mobile devices, printed documents, and office spaces that fall within scope. 

|Control<br>ID|Control Name|Brief Description|
|---|---|---|
|7.1|Physical security perimeters|Defined security perimeters protecting<br>information and processing facilities|
|7.2|Physical entry|Secure areas protected by appropriate entry<br>controls|
|7.3|Securing offices, rooms, and<br>facilities|Physical security designed and applied to<br>offices and facilities|
|7.4|Physical security monitoring|NEW Premises continually monitored for<br>unauthorized physical access|
|7.5|Protecting against physical<br>and environmental threats|Protection against natural and deliberate<br>physical threats|
|7.6|Working in secure areas|Security measures for working in secure<br>areas designed and applied|
|7.7|Clear desk and clear screen|Rules for clear desk for papers and<br>removable media, clear screen for IT|
|7.8|Equipment siting and<br>protection|Equipment sited and protected to reduce<br>environmental risks|
|7.9|Security of assets off-<br>premises|Off-site assets protected accounting for off-<br>premises risks|
|7.10|Storage media|Storage media managed through acquisition,<br>use, transportation, disposal lifecycle|
|7.11|Supporting utilities|Protection of facilities from power failures<br>and utility disruptions|



|Contro<br>ID|l<br>Control Name|Brief Description|
|---|---|---|
|7.12|Cabling security|Power and communications cabling<br>protected from interception/damage|
|7.13|Equipment maintenance|Equipment correctly maintained to ensure<br>availability and integrity|
|7.14|Secure disposal or re-use of<br>equipment|Verified that sensitive data is deleted before<br>disposal or reuse|



Control 7.4 (Physical Security Monitoring) is new in the 2022 revision. It requires ongoing monitoring not just access logs reviewed after an incident, but active surveillance of secure areas. For organizations operating under FedRAMP or handling HIPAA-covered data, this aligns with physical safeguard requirements that auditors pay close attention to. 

Control 7.14 (Secure Disposal) deserves dedicated procedure documentation. Data remanence on solid-state storage is a known challenge standard file deletion leaves data recoverable. NIST SP 800-88 (Guidelines for Media Sanitization) provides the technical guidance that makes your 7.14 implementation defensible under audit. 

## Theme 8: Technological Controls (8.1–8.34) 

Thirty-four controls govern the technical security measures protecting information systems. This is where the 2022 revision made the most additions nine of the eleven new controls appear in Theme 8, reflecting the security landscape’s shift toward cloud infrastructure, application security, and data leakage prevention. 

|Control<br>ID|Control Name|Brief Description|
|---|---|---|
|8.1|User endpoint devices|Policies and technical measures for<br>endpoint device security|
|8.2|Privileged access rights|Allocation and use of privileged access<br>rights restricted and managed|
|8.3|Information access restriction|Information and application access<br>restricted per access control policy|
|8.4|Access to source code|Read/write access to source code and<br>tools restricted appropriately|
|8.5|Secure authentication|Secure authentication technologies<br>implemented per access restrictions|
|8.6|Capacity management|Capacity of resources monitored and<br>adjusted to meet requirements|
|8.7|Protection against malware|Protection against malware implemented<br>and supported by awareness|
|8.8|Management of technical<br>vulnerabilities|Timely identification and remediation of<br>technical vulnerabilities|
|8.9|Configuration management|NEW Configurations established,<br>documented, monitored, and reviewed|
|8.10|Information deletion|NEW Information deleted when no longer<br>required|
|8.11|Data masking|NEW Data masking per access control and<br>business/legal requirements|



#### Control 

ID 

#### Control Name 

#### Brief Description 

|8.12|Data leakage prevention|NEW DLP measures applied to systems,<br>networks, and endpoints|
|---|---|---|
|8.13|Information backup|Backups maintained and regularly tested<br>per backup policy|
|8.14|Redundancy of information<br>processing facilities|Facilities implemented with sufficient<br>redundancy|
|8.15|Logging|Logs recording activities, exceptions, and<br>events produced and stored|
|8.16|Monitoring activities|NEW Networks, systems, and applications<br>monitored for anomalous behavior|
|8.17|Clock synchronization|Clocks of systems synchronized to<br>approved time sources|
|8.18|Use of privileged utility<br>programs|Programs overriding system controls<br>restricted and tightly controlled|
|8.19|Installation of software on<br>operational systems|Installation of software on operational<br>systems managed|
|8.20|Networks security|Networks and network devices secured<br>and managed|
|||Security mechanisms, service levels, and|
|8.21|Security of network services|requirements of network services<br>identified|



|Control<br>ID|Control Name|Brief Description|
|---|---|---|
|8.22|Segregation of networks|Groups of services, users, and systems<br>segregated in networks|
|8.23|Web filtering|NEW Access to external websites<br>managed to reduce malware exposure|
|8.24|Use of cryptography|Rules for effective use of cryptography<br>implemented|
|8.25|Secure development life cycle|Rules for secure development established<br>and applied|
|8.26|Application security<br>requirements|Requirements for application security<br>specified, approved, documented|
|8.27|Secure system architecture and<br>engineering principles|Principles for engineering secure systems<br>established and applied|
|8.28|Secure coding|NEW Secure coding principles applied to<br>software development|
|8.29|Security testing in development<br>and acceptance|Security testing processes defined and<br>implemented in development|
|8.30|Outsourced development|Organization supervises and monitors<br>outsourced development|
|8.31|Separation of development, test,<br>and production environments|Environments separated and secured|
|8.32|Change management|Changes to processing facilities and<br>systems managed per change|



#### Control 

ID 

#### Control Name 

#### Brief Description 

|8.33|Test information|management procedures<br>Test information appropriately selected,<br>protected, and managed|
|---|---|---|
|834|Protection of information|Audit tests planned and agreed to|
|.|systems during audit testing|minimize disruption|



Controls 8.9–8.12 (Configuration Management, Information Deletion, Data Masking, and DLP) are entirely new to the 2022 revision and reflect hard lessons from the decade between standard editions. Together, they address a specific gap that caused real-world breaches: organizations that had strong perimeter security but no systematic controls over how data moved within or out of the environment. 

For US healthcare organizations, control 8.11 (Data Masking) directly supports HIPAA’s deidentification requirements under 45 CFR §164.514. For FedRAMP-authorized cloud providers, 8.16 (Monitoring Activities) maps to the continuous monitoring requirements that distinguish FedRAMP from a one-time authorization model. 

Security leaders responsible for designing and managing an ISMS can advance their expertise through the ISO 27001 Lead Implementer Certification, focused on practical implementation and governance. 

## The 11 New Controls: What Changed from ISO 27001:2013 

Organizations transitioning from ISO 27001:2013 certification need to assess these eleven additions against their existing ISMS. Each represents either an emerging threat category or a control gap that the previous edition’s domain structure failed to capture clearly. 

|New<br>Control|Name|Theme|Why It Was Added|
|---|---|---|---|
||||Formalized intelligence collection|
|5.7|Threat intelligence|Organizational|was absent; reactive security is<br>insufficient|
|5.21|Managing information<br>security in the ICT<br>supply chain|Organizational|Supply chain attacks (SolarWinds,<br>XZ Utils) exposed a critical gap|
|5.23|Information security for<br>use of cloud services|Organizational|Cloud adoption outpaced the 2013<br>framework’s coverage|
|5.30|ICT readiness for<br>business continuity|Organizational|<sup>Separated IT continuity from</sup><br>general BC planning for clarity|
|7.4|Physical security<br>monitoring|Physical|Continuous monitoring vs.<br>periodic review of access logs|
|8.9|Configuration<br>management|Technological|<sup>Misconfiguration is now a primary</sup><br>attack vector|



|New<br>Control|Name|Theme|Why It Was Added|
|---|---|---|---|
||||Data minimization and retention|
|8.10|Information deletion|Technological|compliance requirements<br>increased|
|8.11|Data masking|Technological|<sup>Privacy regulations (CCPA, HIPAA)</sup><br>elevated masking requirements|
|8.12|Data leakage prevention|Technological|<sup>Insider threats and exfiltration</sup><br>attacks increased substantially|
|8.16|Monitoring activities|Technological|Behavioral monitoring and SIEM<br>formalized as a distinct control|
||||Browser-based attacks became|
|8.23|Web filtering|Technological|the dominant endpoint<br>compromise vector|
||||Software supply chain and|
|8.28|Secure coding|Technological|OWASP-class vulnerabilities<br>demanded formal coverage|



Transition Deadline Passed: Action Required The transition period from ISO 27001:2013 to ISO 27001:2022 ended in October 2025. Organizations still holding 2013 certificates need to have completed their transition audit. If your organization has not yet transitioned, contact your certification body immediately your certificate may already be at risk of lapsing. 

## Mapping Annex A to US Regulatory Frameworks 

US organizations rarely operate in a single compliance framework. The practical reality is that your ISMS needs to serve ISO 27001 certification while simultaneously satisfying NIST CSF 2.0, SOC 2 Trust Service Criteria, HIPAA Security Rule requirements, CMMC 2.0 practices, and possibly FedRAMP controls often all at once. 

The good news: there’s substantial overlap. The same risk-based ISMS that satisfies ISO 27001’s requirements will cover the majority of what these frameworks demand. The key is building that overlap into your control documentation from the start rather than mapping retrospectively. 

|ISO 27001 Annex A<br>Theme|NIST CSF 2.0<br>Function|NIST SP 800-<br>53 Family|<br>SOC 2 TSC|HIPAA<br>Safeguard Type|
|---|---|---|---|---|
|5 – Organizational|<sup>GOVERN,</sup><br>IDENTIFY|PM, PL, RA,<br>SA, CA|CC2, CC9|Administrative|
|6 – People|GOVERN,<br>PROTECT|AT, PS|CC1, CC2|Administrative|
||||A1||
|7 – Physical|PROTECT|PE|(Availability),<br>CC6|Physical|
|8 – Technological|PROTECT,<br>DETECT,<br>RESPOND|AC, AU, CM,<br>IA, SC, SI, IR|CC6, CC7, CC8|Technical|



CMMC 2.0 organizations at Level 2 will find that approximately 110 of the 110 CMMC practices map to controls within ISO 27001 Annex A making simultaneous pursuit of both frameworks 

efficient rather than duplicative. The NIST SP 800-171 Rev. 3 controls that underpin CMMC Level 2 draw heavily from the same NIST SP 800-53 families that Annex A maps to. 

For SOC 2 + ISO 27001 dual compliance programs (increasingly common in US SaaS companies), the 2022 revision’s emphasis on supplier security (5.19–5.23) aligns well with CC9 (Risk Mitigation) criteria, and the new monitoring controls (8.16) support CC7 (System Operations) evidence requirements. 

## Using This List: SoA Development and Control Selection 

The Statement of Applicability is the document that connects your risk assessment to Annex A. For each of the 93 controls, your SoA must state whether the control is applicable, whether it’s implemented, and if excluded, the justification for exclusion. Getting this document right is essential; it’s often the first artifact an auditor requests. 

A structured approach to SoA development works better than reviewing controls sequentially. Start by grouping the 93 controls into four categories based on your risk assessment output: 

Controls where you have identified risks that the control directly mitigates these are included and implemented (or planned). Controls that represent legal or regulatory requirements independent of your risk assessment these are always included (relevant for US organizations with HIPAA, CMMC, or federal contract obligations). Controls that represent baseline good practice for your industry, even where specific risks aren’t identified include these and 

document the rationale. Controls that genuinely don’t apply to your operating context document why clearly. “We don’t have a server room” is a legitimate exclusion justification for control 7.1 if you’re entirely cloud-hosted, provided you’ve assessed the risk of physical access to cloud provider facilities through your supplier controls. 

The exclusion justification is where US organizations most often underinvest. Auditors are suspicious of exclusions that weren’t clearly derived from a documented risk assessment. A well-constructed SoA with 15 justified exclusions is more credible than one with 3 exclusions and no rationale. 

Practical SoA Tip For each excluded control, your SoA justification should answer three questions: What risk was assessed? What was the likelihood and impact of that risk in your context? Why does the excluded control not address a residual risk? One to two sentences per exclusion satisfies most auditors; essays do not. 

## ISO 27001 Certification and the Role of Annex A in Your Audit 

Understanding how Annex A functions in a real audit helps calibrate your implementation effort. During Stage 1, your auditor reviews documentation including the SoA, risk register, and risk treatment plan to assess readiness for Stage 2. Annex A coverage questions at Stage 1 are typically documentation-focused: Is there a control for this risk? Is it documented? 

Stage 2 is where implementation evidence matters. Auditors sample across themes they won’t test every control, but they will test a representative selection across all four themes. A common audit finding is that controls exist on paper (in the SoA and procedures) but lack objective evidence of operation: no access review records for 5.18, no documented vulnerability scan results for 8.8, no training completion records for 6.3. 

The highest-risk Annex A areas in US organization audits, based on common nonconformity patterns, tend to concentrate around: access rights reviews (5.18 and 8.2), supplier security assessments (5.19 and 5.22), vulnerability management timelines (8.8), and incident management completeness (5.24–5.27). These aren’t harder controls to implement they’re controls where implementation requires consistent operational discipline rather than one-time configuration. 

For professionals pursuing ISO 27001 Lead Implementer or Lead Auditor certification through GAICC, the ability to interpret Annex A controls in context rather than recite their names is what separates candidates who pass from those who need a retake. 

## ISO 27001 vs. ISO 27002: How They Work Together 

ISO 27001 is the certifiable standard it contains the requirements your organization is audited against, including Annex A. ISO 27002:2022 is the companion guidance document it provides detailed implementation guidance for each of the 93 controls in Annex A. 

Annex A in ISO 27001 gives you the control names and short descriptions. ISO 27002 gives you the “how” for each one including attribute tables, purpose statements, implementation guidance, and supplementary information. Neither document is sufficient alone for implementation. 

US organizations sometimes invest in ISO 27001 certification without procuring ISO 27002, then struggle to implement controls consistently because the high-level Annex A descriptions leave too much interpretation open. The two standards are designed to be used together. ISO 27002 is not required for certification but organizations that skip it typically take longer to achieve consistent control implementation and produce weaker SoA documentation. 

One more distinction worth noting: ISO 27001 is auditable and certifiable. ISO 27002 cannot be certified against. If someone claims ISO 27002 certification, that’s not a recognized credential. Compliance professionals evaluating different credential levels can compare the complete ISO <u>27001 certification path for information security professionals</u> to choose the right certification based on career goals. 

## Frequently Asked Questions 

1. How many controls are in ISO 27001 Annex A? 

ISO/IEC 27001:2022 Annex A contains 93 controls organized across four themes: 37 Organizational controls (5.1–5.37), 8 People controls (6.1–6.8), 14 Physical controls (7.1–7.14), 

and 34 Technological controls (8.1–8.34). The previous 2013 edition had 114 controls across 14 domains. The reduction reflects consolidation and restructuring, not a reduction in security requirements. 

### 2. Do all 93 ISO 27001 Annex A controls need to be implemented? 

No. Annex A controls are a reference set. Your Statement of Applicability (SoA) documents which controls are applicable based on your risk assessment results. Controls can be excluded when they don’t address any identified risk but each exclusion must be formally justified. Applicable controls must be implemented and operating effectively by your Stage 2 audit. 

### 3. What are the 11 new controls in ISO 27001:2022? 

The 11 new controls added in the 2022 revision are: 5.7 (Threat intelligence), 5.21 (ICT supply chain security), 5.23 (Cloud services security), 5.30 (ICT readiness for business continuity), 7.4 (Physical security monitoring), 8.9 (Configuration management), 8.10 (Information deletion), 8.11 (Data masking), 8.12 (Data leakage prevention), 8.16 (Monitoring activities), 8.23 (Web filtering), and 8.28 (Secure coding). These reflect security challenges that emerged or intensified between 2013 and 2022. 

4. How does ISO 27001 Annex A map to NIST CSF 2.0? 

The mapping is substantial but not one-to-one. Organizational controls (Theme 5) primarily map to the GOVERN and IDENTIFY functions. People controls (Theme 6) align with GOVERN and PROTECT. Physical controls (Theme 7) map to PROTECT. Technological controls (Theme 8) span PROTECT, DETECT, and RESPOND. The NIST CSF 2.0 Informative References document provides official crosswalk tables. 

### 5. What is the difference between ISO 27001 Annex A and ISO 27002? 

ISO 27001 Annex A lists the 93 controls with short descriptions it’s the certifiable standard. ISO 27002:2022 provides detailed implementation guidance for each of those same 93 controls. You cannot be certified against ISO 27002. For implementation purposes, ISO 27002 is the essential companion document that explains how to put each control into practice. 

### 6. Can a cloud-only organization exclude physical controls from their SoA? 

Partially. Organizations with no owned physical infrastructure can exclude controls like 7.1 (Physical security perimeters) and 7.11 (Supporting utilities) if they’ve assessed and accepted the risk, or transferred it to cloud providers via contract. However, controls like 7.7 (Clear desk/screen) and 7.9 (Security of assets off-premises) typically remain applicable since endpoints and remote work are still in scope. 

### 7. Does ISO 27001 certification help with CMMC 2.0 compliance? 

Yes, significantly. CMMC 2.0 Level 2 practices are drawn from NIST SP 800-171, which itself derives from NIST SP 800-53 the same framework that ISO 27001 Annex A maps heavily against. An organization with a mature ISO 27001 ISMS typically covers 80–90% of CMMC Level 2 requirements, though formal CMMC assessment is a separate process with its own evidence requirements. 

### 8. When did the transition deadline from ISO 27001:2013 to ISO 27001:2022 expire? 

The transition deadline was October 31, 2025. Organizations that had ISO 27001:2013 certificates were required to complete a transition audit before that date to upgrade to the 2022 version. Certificates that were not transitioned by the deadline lapsed. If your organization has not yet transitioned, contact your accredited certification body to understand your options for recertification. 

## Key Takeaway 

Annex A is ultimately a tool for thinking systematically about information security risk not a compliance checklist to tick off. The 93 controls in ISO/IEC 27001:2022 represent decades of hard-won knowledge about where information security failures actually occur, restructured in 

2022 to reflect the cloud, supply chain, and application security realities that define the current threat environment. 

For US GRC and information security professionals, the framework’s real value comes from the rigor it imposes on your risk assessment and control selection process the same rigor that makes an ISO 27001 ISMS credible to auditors, customers, and regulators alike. 

Your next concrete step: pull your current SoA (or create one if you’re starting fresh) and verify that each included control has an evidence record. That gap between documented controls and operational evidence is where most certification programs stall. 

Ready to Build or Advance Your ISO 27001 Expertise? GAICC’s ISO 27001 certification programs prepare GRC and information security professionals to lead ISMS implementations, conduct internal audits, and achieve certification with US regulatory alignment built into every module. **→** <u>Explore ISO 27001 Certifications</u> 

