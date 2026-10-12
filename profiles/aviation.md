# Aviation profile for AI Incident Card v0.1

**Status:** draft, informative. **Reviewed against public sources:** 2026-10-12.

Use the existing Incident Card and its optional `aviation_profile` member. This profile supplies context and links to an Aviation ML Assurance Card or MRO AI Sign-off Card when those documents exist. It does not create an aviation incident standard or change the Incident Card's severity, publication, or withdrawal rules.

| Field | Meaning |
| --- | --- |
| `profile_version` | `0.1` for this optional profile. |
| `domain` | The publisher's broad context: aircraft system, maintenance, ATM/ANS, UAS, or other. |
| `incident_scope` | Plain-language description of the AI behavior and aviation workflow affected. |
| `aviation_ml_card_uri` | Optional reference to the vendor's system disclosure. |
| `mro_signoff_card_uris` | Optional references to artifact-bound AI-assisted maintenance review records. |
| `adrep_category_refs` | Optional, publisher-asserted ICAO ADREP category codes. The schema checks only the token shape, not whether a code exists or fits the occurrence. |
| `maintenance_release_note` | Optional explanation of how the AI finding was handled by the separate authorised maintenance process. |

The [ICAO ADREP taxonomy is used by ECCAIRS](https://www.easa.europa.eu/en/domains/safety-management/European%20Coordination%20Centre%20for%20Accident%20and%20Incident%20Reporting%20Systems%20%28ECCAIRS%29%202). A category reference here does **not** establish correct ADREP coding, ECCAIRS/E5X format compatibility, a regulatory report, or submission to any authority. Consult the applicable authority and current taxonomy for real reporting. Keep restricted maintenance records, personal data, proprietary aircraft details, and export-controlled data out of public cards.

An AI review card or cryptographic signature is not a certificate of release to service or approval for return to service. [EASA Part-145](https://www.easa.europa.eu/en/document-library/easy-access-rules/online-publications/easy-access-rules-continuing-airworthiness?erules-id=ERULES-1963177438-272) requires appropriately authorised certifying staff for the release. [14 CFR § 43.9](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-C/part-43/section-43.9) specifies maintenance-record and signer information in the U.S. Where relevant, keep the organisation's actual release record and authorisation checks in its controlled system.

[`profiles/aviation/examples/aviation-maintenance-synthetic.json`](aviation/examples/aviation-maintenance-synthetic.json) is fictional and uses intentionally non-resolving `example.invalid` links. It asserts no real incident, ADREP category, approval, or regulator notification.
