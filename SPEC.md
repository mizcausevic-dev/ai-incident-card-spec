# AI Incident Card v0.1 — Specification

**Status:** Draft
**Version:** 0.1.0
**Editor:** Miz Causevic
**License:** AGPL-3.0 (this document, schema, and examples). Implementations are unrestricted.

RFC 2119 keywords (**MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**) apply throughout.

---

## 1. Scope

This specification defines a JSON document format for **AI Incident Cards** — vendor-published, machine-readable post-incident disclosures for AI agents, tutors, tools, and models that misbehaved.

Today, AI incidents are disclosed in ad-hoc blog posts (Anthropic incident reports, OpenAI postmortems, Google AI Studio blog) or in curated third-party databases (OECD AI Incidents Monitor, MIT AI Incident Database, AI Vulnerability Database). There is no canonical machine-readable format a vendor can publish *themselves* at a well-known URL — which is the gap this spec fills.

**Think CVE, but for AI agents.**

An Incident Card is consumed by:

- **CISO / Trust & Safety teams** monitoring their AI vendor stack for new incidents
- **Procurement / Risk teams** tracking vendor reliability across procurement cycles
- **Regulators** receiving EU AI Act Article 73 serious-incident reports (15-day window) and US OMB M-24-10 AI Use Case Inventory updates
- **AI Safety researchers** building corpora of disclosed failures
- **Insurance / cyber underwriters** pricing AI-tool risk
- **Downstream LMS / agent platforms** that should disable affected versions

An Incident Card **SHOULD** cross-reference every Kinetic Gain Protocol Suite document the incident touches:

| Field | Points at |
|---|---|
| `affected.agent_card_uris[]` | [Agent Cards](https://github.com/mizcausevic-dev/agent-cards-spec) |
| `affected.tutor_card_uris[]` | [AI Tutor Cards](https://github.com/mizcausevic-dev/ai-tutor-card-spec) |
| `affected.tool_card_uris[]` | [MCP Tool Cards](https://github.com/mizcausevic-dev/mcp-tool-card-spec) |
| `evidence.evidence_uris[]` | [AI Evidence Format](https://github.com/mizcausevic-dev/ai-evidence-format-spec) |
| `evidence.prompt_provenance_uri` | [Prompt Provenance](https://github.com/mizcausevic-dev/prompt-provenance-spec) |

When an incident touches every layer of the stack, an Incident Card is the single document that points at every other affected document.

## 2. Terminology

- **Incident** — a single AI failure event that warrants public disclosure: privacy leak, safety violation, mandated-reporter failure, jailbreak success, content-filter gap, hallucination with downstream harm, refusal-taxonomy breach, etc.
- **Severity** — one of `low` / `medium` / `high` / `critical`.
- **Status** — one of `active` / `mitigated` / `resolved` / `withdrawn`.
- **Withdrawal** — formal retraction of an incident report (e.g. when investigation determined no incident occurred).
- **Well-known location** — `/.well-known/ai-incidents/<incident_id>.json` for the card itself, with an aggregated index at `/.well-known/ai-incidents.json`.

## 3. Design philosophy

### 3.1 Vendor-published, not third-party-curated

The OECD AI Incidents Monitor and MIT AI Incident Database aggregate human-curated reports from news coverage. That's valuable but lags reality. Incident Cards push the source of truth to the vendor, on the vendor's own domain, in a format every consumer can read. Third-party aggregators can ingest them.

### 3.2 Bind to every affected document

Software CVEs reference affected versions; that's enough because software is mostly stable. AI failures are different — they involve specific agent configurations, tool combinations, prompts, and (sometimes) tutoring scenarios. An Incident Card carries URIs into every Kinetic Gain Suite document type so a consumer can chain through to the precise affected disclosure.

### 3.3 Regulatory hooks first-class

EU AI Act Article 73 requires "serious incident" reporting to national authorities within 15 days. US OMB M-24-10 mandates federal-agency AI Use Case Inventory updates. The spec carries a `regulatory` block listing filings so a consumer can prove the legal obligations were met.

### 3.4 Withdrawal is normal

Some published incidents turn out not to be incidents after investigation. Withdrawals **MUST** be first-class — preserving the original record while marking it `withdrawn` with a documented reason. The history matters more than the live state.

## 4. Document structure

### 4.1 `incident_card_version` (required)

A semver string. **MUST** be `"0.1"` for documents conforming to this draft.

### 4.2 `incident` (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Stable identifier. Convention: `INC-<YYYY-MM-DD>-<vendor>-<seq>`, e.g. `INC-2026-05-12-anthropic-001`. Kebab-case characters and digits only. |
| `title` | string | yes | One-line human-readable title. |
| `severity` | enum | yes | `low` / `medium` / `high` / `critical`. |
| `categories` | array of enum | yes | One or more harm categories (see §5). Non-empty. |
| `discovered_at` | ISO 8601 | yes | When the vendor became aware. |
| `occurred_at` | ISO 8601 | no | When the incident first happened, if known. |
| `disclosed_at` | ISO 8601 | yes | When this Incident Card was first published. |
| `resolved_at` | ISO 8601 | conditional | Required when `status` is `resolved`. |
| `status` | enum | yes | `active` / `mitigated` / `resolved` / `withdrawn`. |

### 4.3 `affected` (required)

What the incident touched.

| Field | Type | Required | Description |
|---|---|---|---|
| `vendor` | string | yes | Vendor name, e.g. `"Anthropic"`. |
| `products` | array of string | yes | Product / agent / tutor names. Non-empty. |
| `versions` | array of string | no | Affected model / product version identifiers. |
| `agent_card_uris` | array of URI | no | Back-references to Agent Cards. |
| `tutor_card_uris` | array of URI | no | Back-references to Tutor Cards. |
| `tool_card_uris` | array of URI | no | Back-references to MCP Tool Cards. |
| `affected_user_count` | object | no | `{ kind: "exact" \| "approximate" \| "unknown", count?: integer }`. |
| `affected_populations` | array of string | no | E.g. `["k12-students-under-13", "users-in-eu"]`. |

### 4.4 `summary` (required)

A 1–3 paragraph human-readable plain-text summary. **SHOULD** be 200–800 characters. Reviewers read this first.

### 4.5 `root_cause` (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `category` | enum | yes | `training_data` / `prompt_injection` / `tool_abuse` / `refusal_taxonomy_gap` / `content_filter_gap` / `retrieval_failure` / `evaluation_gap` / `deployment_misconfiguration` / `supply_chain` / `other`. |
| `description` | string | yes | Technical description of the failure mode. |
| `category_other_text` | string | conditional | Required when `category` is `other`. |

### 4.6 `harm` (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `severity_justification` | string | yes | Why the chosen severity is appropriate. |
| `manifested` | boolean | yes | Whether the harm actually manifested (vs. being a near-miss / theoretical exploit). |
| `narrative` | string | no | Optional narrative explaining the user-visible effect. |

### 4.7 `mitigation` (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `actions_taken` | array of string | yes | Bullet list of remediation steps. Non-empty. |
| `permanent_fix` | boolean | yes | Whether the fix is permanent (`true`) or a temporary mitigation pending full fix (`false`). |
| `rollout_status` | enum | yes | `planned` / `in_progress` / `deployed`. |
| `workaround_for_users` | string | no | What customers / users should do until the fix rolls out. |

### 4.8 `evidence` (optional but recommended)

Cross-references into the rest of the Kinetic Gain Protocol Suite plus generic references.

| Field | Type | Required | Description |
|---|---|---|---|
| `evidence_uris` | array of URI | no | [AI Evidence Format](https://github.com/mizcausevic-dev/ai-evidence-format-spec) documents capturing the failure. |
| `prompt_provenance_uri` | URI | no | [Prompt Provenance](https://github.com/mizcausevic-dev/prompt-provenance-spec) record of the offending prompt. |
| `reproduction_uri` | URI | no | Public reproduction or proof-of-concept URL. |
| `internal_postmortem_uri` | URI | no | Internal (gated) postmortem; preserves audit chain even when content is not public. |

### 4.9 `references` (optional)

External writeups, blog posts, regulatory filings, press releases, academic papers.

Each entry:

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | enum | yes | `blog_post` / `regulatory_filing` / `academic_paper` / `press_release` / `customer_notice` / `other`. |
| `title` | string | yes | Human-readable title. |
| `uri` | URI | yes | Where to read it. |
| `published_at` | ISO 8601 | no | |

### 4.10 `regulatory` (optional)

Regulatory filings the vendor made (or chose not to make, with justification).

| Field | Type | Required | Description |
|---|---|---|---|
| `reported_to` | array of enum | no | One or more of `eu-ai-act-art-73` / `us-omb-m-24-10` / `ferpa` / `coppa` / `hipaa` / `gdpr` / `state-attorney-general` / `fda-21-cfr-11` / `other`. |
| `reporting_deadline_met` | boolean | no | Whether the vendor met the regulatory reporting window (15 days for EU AI Act Art. 73, etc.). |
| `regulatory_filing_uris` | array of URI | conditional | Required when `reported_to` is non-empty. |
| `not_reportable_justification` | string | no | When the vendor determined no regulator needed notification, the rationale. |

### 4.11 `withdrawal` (conditional)

**Required** when `incident.status` is `withdrawn`.

| Field | Type | Required | Description |
|---|---|---|---|
| `withdrawn_at` | ISO 8601 | yes | |
| `reason` | string | yes | Why the incident report was withdrawn. |
| `replacement_incident_uri` | URI | no | If the withdrawal is because the report was reissued as a different incident. |

### 4.12 `published_by` (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Publisher name. |
| `role` | enum | yes | `vendor` / `third-party-researcher` / `user` / `regulator` / `auditor`. |
| `contact_uri` | URI | no | Contact (mailto:, security.txt URL, etc.). |
| `pgp_fingerprint` | string | no | For sensitive coordination, a PGP fingerprint. |

### 4.13 `published_at` (required)

ISO 8601 timestamp of when this version of the Incident Card was published.

### 4.14 `last_updated_at` (required)

ISO 8601 timestamp of the latest update to this card. Equal to `published_at` for v1.

### 4.15 `revision` (optional)

| Field | Type | Required | Description |
|---|---|---|---|
| `number` | integer | yes | 1, 2, 3, ... — increments on each update. |
| `change_summary` | string | yes | What changed since the previous revision. |

## 5. Harm category enum

`incident.categories[]` **MUST** contain one or more of:

| Value | Meaning |
|---|---|
| `misinformation` | False or misleading factual claims |
| `pii_leak` | Personally identifiable information disclosed |
| `bias` | Discriminatory behavior toward a protected class |
| `copyright_violation` | Outputs verbatim or near-verbatim from copyrighted training data |
| `mandated_reporter_failure` | Tutor or agent failed to escalate a disclosure (self-harm, abuse, etc.) — see [AI Tutor Cards](https://github.com/mizcausevic-dev/ai-tutor-card-spec) |
| `prompt_injection_success` | External text successfully overrode the system prompt |
| `tool_abuse` | An MCP / function-call tool was used outside its declared scope |
| `jailbreak_success` | Safety guardrails bypassed via known-class attack |
| `hallucination_with_consequences` | Confident false output that caused downstream harm |
| `refusal_taxonomy_violation` | Agent did not behave according to its declared [Agent Card refusal taxonomy](https://github.com/mizcausevic-dev/agent-cards-spec) |
| `content_filter_failure` | Content the filter was supposed to block reached a user |
| `availability_outage` | The agent was unavailable when contractually obligated |
| `tampering` | Output was altered after the model emitted it |
| `other` | Used with `categories_other_text` |

## 6. Conditional rules

### 6.1 Resolved requires resolved_at

If `incident.status` is `resolved`, then `incident.resolved_at` **MUST** be present and later than `incident.discovered_at`.

### 6.2 Withdrawn requires withdrawal block

If `incident.status` is `withdrawn`, then `withdrawal` **MUST** be present with `withdrawn_at` and `reason`.

### 6.3 Regulatory filings require URIs

If `regulatory.reported_to` is non-empty, then `regulatory.regulatory_filing_uris` **MUST** be non-empty.

### 6.4 Root-cause "other" requires category_other_text

If `root_cause.category` is `other`, then `root_cause.category_other_text` **MUST** be present.

### 6.5 Categories "other" requires categories_other_text

If `incident.categories` contains `other`, then a top-level `categories_other_text` field **MUST** be present.

### 6.6 Critical severity triggers a SHOULD on affected_populations

If `incident.severity` is `critical`, then `affected.affected_populations` **SHOULD** be present. Consumers MAY downgrade trust if a vendor declares critical severity without naming affected populations.

### 6.7 K-12 tutor incidents require Tutor Card refs

If any of `incident.categories` is `mandated_reporter_failure` and the incident touches a tutor, then `affected.tutor_card_uris` **MUST** be non-empty.

## 7. Well-known location

A vendor publishing Incident Cards **SHOULD** serve each card at:

```
https://<vendor-domain>/.well-known/ai-incidents/<incident_id>.json
```

A vendor with multiple incidents **SHOULD** also publish an index:

```
https://<vendor-domain>/.well-known/ai-incidents.json
```

The index is a JSON array of entries:

```json
[
  {
    "id": "INC-2026-05-12-vendor-001",
    "title": "Mandated-reporter escalation failure in K-12 math tutor",
    "severity": "critical",
    "status": "resolved",
    "disclosed_at": "2026-05-12T16:00:00Z",
    "uri": "/.well-known/ai-incidents/INC-2026-05-12-vendor-001.json"
  }
]
```

Consumers can poll the index and pull individual cards on update.

## 8. Cross-spec composition

An Incident Card is the closing artifact that ties the Suite together. A typical incident touches multiple specs; the card carries URIs into each:

```
Incident Card                                    
   ├── affected.agent_card_uris ────────→ Agent Card  (capability surface)
   ├── affected.tutor_card_uris ────────→ Tutor Card  (EdTech audience + pedagogy)
   ├── affected.tool_card_uris  ────────→ Tool Card   (MCP tool that was abused)
   ├── evidence.prompt_provenance_uri ─→ Prompt Provenance  (the prompt that failed)
   └── evidence.evidence_uris ──────────→ AI Evidence (capturing the bad output)
```

A reviewer pulling an Incident Card can chain through to every affected document in a single document graph walk.

## 9. Security & policy considerations

- **Coordinated disclosure.** Vendors **SHOULD** practice 90-day coordinated-disclosure conventions when the incident involves a discoverable exploit. The Incident Card is the *public* artifact at the end of that window.
- **Sensitive details.** Reproduction steps for a still-exploitable vulnerability **MUST NOT** be embedded in the publicly served card. Use `evidence.internal_postmortem_uri` (gated) for restricted distribution.
- **Withdrawal preserves history.** A withdrawn card **MUST NOT** be deleted from `/.well-known/`. The URL continues to resolve, with `status: "withdrawn"` and a `withdrawal` block explaining why.
- **Signing.** v0.1 does not require cryptographic signatures. v0.2 may add an optional detached-signature field using BLS or Ed25519.

## 10. Open questions for v0.2

- **CVSS-style scoring.** v0.2 may add a structured severity score (impact × likelihood) parallel to CVSS, calibrated for AI-specific harm vectors.
- **Subscription model.** A standard webhook or Webfinger-style discovery so consumers can subscribe to a vendor's Incident Card stream.
- **Aggregator handshake.** A handshake convention so OECD / MIT / AVID-style aggregators can ingest Incident Cards directly.
- **Anonymized aggregation.** A field for anonymous incident reporting by third-party researchers who haven't yet completed coordinated disclosure.

## 11. Versioning

The `incident_card_version` field identifies the spec revision. v0.1 is a draft; consumers **SHOULD** treat unknown future versions as an error rather than attempting forward-compatible parsing.
