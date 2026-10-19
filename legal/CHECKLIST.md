# Legal and privacy checklist (Phase 0, Step 1)

These are drafts and working notes, not legal advice. Have a South African attorney review the notice and consent before public launch.

## Name and domain

- [ ] Register watsejy.co.za (and watsejy.com if available) with a ZACR-accredited registrar; set up email on it.
- [ ] Reserve the @watsejy handles on the social platforms you will use.
- [ ] Search the CIPC trade mark register for "Watsejy" / "Wat sê jy" before investing in branding.

## Before any real audio is collected

- [ ] Decide the legal entity that is the "responsible party" under POPIA (individual, company, or NPO). An NPO keeps WhatsApp service messages free until end-2027 if that channel is ever built.
- [ ] Register an Information Officer with the Information Regulator via its eServices portal. Sole proprietors and small businesses are not exempt.
- [ ] Finalise `PRIVACY_NOTICE_DRAFT.md` and publish it on the project website.
- [ ] Finalise `CONSENT_RECORDING.md` (participants in recordings used for the test set and fine-tuning).
- [ ] Finalise `LICENCE_LETTER_CONTENT.md` (copyright owners of existing recordings, for example a YouTube creator).
- [ ] Draft a PAIA manual from `PAIA_MANUAL_OUTLINE.md`.
- [ ] Write the retention rule into the notice: local-first by default; cloud-processed audio deleted within 48 hours of transcription; donated audio kept only for model training under its consent.
- [ ] Keep a register of consents (`consent_id`, date, participants, scope) outside the repository.

## Positions taken (and why)

| Topic | Position | Basis |
|---|---|---|
| Voice recordings | Treated as special personal information; explicit consent obtained | POPIA's biometrics definition includes voice recognition; conservative reading |
| Household exclusion | Does not cover us | It protects the individual user's own processing, not an operator offering a service |
| Cross-border transfer (s72) | Avoided by default through on-device processing; for cloud fallback and donation, rely on consent plus a data-processing agreement with the host and short retention | POPIA s72(1) |
| Recording meetings | Lawful for a participant (single-party consent); the app shows a recording indicator and offers a notify-participants text | RICA s4 |
| WhatsApp audio | Users share their own voice notes; no scraping or unofficial clients | WhatsApp terms |
| Training data from WhatsApp bot (if ever built) | Only for a model used exclusively by us | Meta Business Platform terms |
| Model licences | Fluister MIT, BuzzASR MIT, Sunbird Apache-2.0, pyannote MIT; MMS excluded (CC-BY-NC) | Model cards |
| Dataset licences | NCHLT CC BY 3.0, FLEURS CC BY 4.0, afrikaans-30s CC-BY-4.0 pending author confirmation | Dataset cards; see `ATTRIBUTION.md` |

## Open items

- [ ] Email the afrikaans-30s dataset author to confirm commercial use (card is self-contradictory).
- [ ] Confirm the NCHLT Speech II (Hansard) corpus includes Afrikaans before planning on it for proper nouns.
- [ ] Attorney review of the notice, consent and PAIA manual.
