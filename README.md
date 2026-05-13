# AI Incident Card

> **The CVE-equivalent for AI agent failures.**
> Vendor-published, machine-readable post-incident disclosure that cross-references every other affected document in the Kinetic Gain Protocol Suite.

A draft specification for **AI Incident Cards** — what a vendor publishes when one of their AI agents, tutors, tools, or models misbehaves. Today these disclosures live in ad-hoc blog posts (Anthropic incident reports, OpenAI postmortems) or third-party curated databases (OECD AI Incidents Monitor, MIT AI Incident Database). This spec gives vendors a canonical machine-readable format they can publish *themselves* at a well-known URL.

## Why it matters

| Buyer | What they get |
|---|---|
| **CISO / Trust & Safety** | Monitor their AI vendor stack via a single JSON poll per vendor — `/.well-known/ai-incidents.json` |
| **Procurement / Risk** | Track vendor reliability across procurement cycles with a machine-readable history |
| **Regulators** | EU AI Act Article 73 serious-incident filings + US OMB M-24-10 inventory updates in a structured format |
| **AI Safety researchers** | Public corpus of self-disclosed vendor failures |
| **Insurance / underwriters** | Price AI-tool risk against a public claims history |
| **LMS / agent platforms** | Auto-disable affected versions when a vendor publishes a critical card |

## The cross-spec composition

An Incident Card is the closing artifact that ties the rest of the Kinetic Gain Protocol Suite together. A typical incident touches multiple specs; the card carries URIs into each:

```
Incident Card                                    
   ├── affected.agent_card_uris ────────→ Agent Card        (capability surface)
   ├── affected.tutor_card_uris ────────→ Tutor Card        (EdTech audience + pedagogy)
   ├── affected.tool_card_uris  ────────→ Tool Card         (MCP tool that was abused)
   ├── evidence.prompt_provenance_uri ─→ Prompt Provenance  (the prompt that failed)
   └── evidence.evidence_uris ──────────→ AI Evidence       (capturing the bad output)
```

A single Incident Card lets a reviewer chain through to every affected document in one graph walk.

## What's declared

| Section | What it does |
|---|---|
| **Incident** | ID, title, severity (`low` / `medium` / `high` / `critical`), categories, discovered / disclosed / resolved timestamps, status (`active` / `mitigated` / `resolved` / `withdrawn`) |
| **Affected** | Vendor, products, versions, back-refs to Agent / Tutor / Tool Cards, affected user count + populations |
| **Root cause** | One of 10 categories (training_data, prompt_injection, refusal_taxonomy_gap, etc.) + free-text description |
| **Harm** | Severity justification, manifested vs. near-miss, optional narrative |
| **Mitigation** | Actions taken, permanent-fix boolean, rollout status, user workaround |
| **Evidence** | AI Evidence Format URIs, Prompt Provenance URI, public reproduction, internal postmortem |
| **References** | Blog posts, regulatory filings, academic papers, customer notices |
| **Regulatory** | What authorities were notified (EU AI Act Art. 73, GDPR, FERPA, COPPA, …), deadline-met boolean, filing URIs |
| **Withdrawal** | First-class retraction — preserves the URL while marking the report withdrawn with a documented reason |
| **Published by** | Vendor / third-party-researcher / user / regulator / auditor |

## Conditional rules enforced by the schema

- `incident.status = resolved` ⇒ `incident.resolved_at` required
- `incident.status = withdrawn` ⇒ `withdrawal` block required
- `regulatory.reported_to` non-empty ⇒ `regulatory.regulatory_filing_uris` non-empty
- `root_cause.category = other` ⇒ `root_cause.category_other_text` required
- `incident.categories` contains `other` ⇒ top-level `categories_other_text` required

Beyond the schema, the spec specifies a **SHOULD** for critical severity: `affected.affected_populations` should be populated. Consumers may downgrade trust if a vendor declares critical severity without naming affected populations.

## Quickstart

1. Mint an incident ID. Convention: `INC-<YYYY-MM-DD>-<vendor>-<seq>` (e.g. `INC-2026-05-12-anthropic-001`).
2. Author an Incident Card conforming to [`incident-card.schema.json`](incident-card.schema.json). Start from one of the [examples](examples/).
3. Validate with any JSON Schema 2020-12 validator:
   ```bash
   npx -p ajv-cli -p ajv-formats ajv validate \
     -s incident-card.schema.json \
     -d examples/tutor-mandated-reporter-failure.json \
     -c ajv-formats --spec=draft2020 --strict=false
   ```
4. Serve at `https://<vendor-domain>/.well-known/ai-incidents/<incident_id>.json`.
5. Maintain an index at `https://<vendor-domain>/.well-known/ai-incidents.json` listing all cards. Consumers poll the index.

## Files in this repo

- [`SPEC.md`](SPEC.md) — full v0.1 specification (11 sections)
- [`incident-card.schema.json`](incident-card.schema.json) — JSON Schema (draft 2020-12) with conditional rules
- [`examples/`](examples/) — reference incident cards covering the canonical failure modes:
  - [`tutor-mandated-reporter-failure.json`](examples/tutor-mandated-reporter-failure.json) — critical · K-12 tutor missed a self-harm disclosure inside a word problem; FERPA + state-AG filings; resolved
  - [`prompt-injection-support-agent.json`](examples/prompt-injection-support-agent.json) — high · base64-encoded log block hijacked the planning step; tool-abuse + refusal-taxonomy violation; mitigated
  - [`pii-leak-cite-check.json`](examples/pii-leak-cite-check.json) — high · whitespace bug in robots.txt parsing surfaced cached PII; GDPR Art. 33 filing; resolved

## Status

**v0.1 draft.** Issues and pull requests welcome.

## License

MIT-licensed. The specification text, JSON Schema, and example documents in this repository may be freely implemented, extended, redistributed, or incorporated into commercial or non-commercial products with attribution. Reference implementations of this spec (such as [mcp-kinetic-gain](https://github.com/mizcausevic-dev/mcp-kinetic-gain)) are licensed separately under AGPL-3.0.

## Kinetic Gain Protocol Suite

A family of open specifications for the answer-engine and agent era:

| Spec | What it does |
|---|---|
| [AEO Protocol](https://github.com/mizcausevic-dev/aeo-protocol-spec) | Entity declaration at `/.well-known/aeo.json` |
| [Prompt Provenance](https://github.com/mizcausevic-dev/prompt-provenance-spec) | Versioned, lineaged, reviewable LLM prompt records |
| [Agent Cards](https://github.com/mizcausevic-dev/agent-cards-spec) | Declarative agent capability + refusal disclosure |
| [AI Evidence Format](https://github.com/mizcausevic-dev/ai-evidence-format-spec) | Structured citations for LLM-generated claims |
| [MCP Tool Cards](https://github.com/mizcausevic-dev/mcp-tool-card-spec) | Per-tool disclosure for Model Context Protocol servers |
| [AI Tutor Cards](https://github.com/mizcausevic-dev/ai-tutor-card-spec) | EdTech-specialized agent disclosure (vendor-side) |
| [Student AI Disclosure](https://github.com/mizcausevic-dev/student-ai-disclosure-spec) | Student-side disclosure attached to submitted work |
| [Classroom AI AUP](https://github.com/mizcausevic-dev/classroom-ai-aup-spec) | District / school / course AI policy (third leg of the EdTech trio) |
| **AI Incident Card** (this) | Post-incident disclosure for AI agents — references every other affected document |
| [Clinical AI Disclosure](https://github.com/mizcausevic-dev/clinical-ai-disclosure-spec) | **HealthTech vertical** — vendor disclosure for healthcare AI. References Incident Cards via `audit.incident_card_index_uri`. |

### Related testing artifact

| Repo | What it does |
|---|---|
| [`prompt-injection-bench`](https://github.com/mizcausevic-dev/prompt-injection-bench) | 30-attack open corpus + Python harness. Failed runs become natural inputs for Incident Cards filed under `categories: ["prompt_injection_success"]`. |

Single landing: [`kinetic-gain-protocol-suite`](https://github.com/mizcausevic-dev/kinetic-gain-protocol-suite).

---

**Connect:** [LinkedIn](https://www.linkedin.com/in/mirzacausevic/) · [Kinetic Gain](https://kineticgain.com) · [Medium](https://medium.com/@mizcausevic/) · [Skills](https://mizcausevic.com/skills/)
