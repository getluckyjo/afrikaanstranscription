# Wat sê jy: commercial opportunities and ROI

_One-page view, October 2026. Market figures come from the feasibility report; revenue and cost figures are estimates at R17.50 per US dollar and should be treated as planning assumptions, not forecasts._

## The opening

- **6.4 million first-language Afrikaans speakers** in South Africa (Census 2022), concentrated in the Western Cape (41%) and Northern Cape (55%), plus roughly a tenth of Namibia.
- **WhatsApp reaches about 95% of South Africa's 52 million internet users**, and voice notes are a primary way Afrikaans speakers communicate.
- **Nobody serves this well.** WhatsApp's own transcripts skip Afrikaans. Generic tools run stock Whisper, which gets a third to two thirds of Afrikaans words wrong. Afrikaans-tuned models reach 9–16% error, and nothing packages them for ordinary users. The only Afrikaans-first competitor is pre-launch at $24 a month.
- **The moat is data, not models.** The public models are free to anyone. A few hours of consented, corrected real-world Afrikaans makes a model nobody else has.

## Where the money is

| Opportunity | Who pays | Price point | Why they buy | Realism |
|---|---|---|---|---|
| **Consumer freemium** (voice notes, meetings) | Individuals | Free tier; R90–R180/month | Convenience, Afrikaans done right | High reach, low conversion (1–3%) |
| **Churches** (sermons, council minutes) | Congregations | R250–R500/month | Weekly content, tight community, word of mouth | Strong: roughly a thousand NG Kerk congregations plus other Afrikaans denominations |
| **Legal and accounting practices** | Firms, per seat | R500–R1,500/seat/month | Client meetings and dictation; audio never leaves the machine | Strong: privacy is the pitch, local-only is the differentiator |
| **Medical** (consult notes) | Practices, per seat | R1,000+/seat/month | Afrikaans-speaking patients in the Cape; POPIA-safe | Good, slower sales cycle, attorney review first |
| **Public and education** (municipalities, school bodies, universities) | Institutions | Per seat or per audio hour | Minutes and records in Afrikaans; in-country processing | Good, tender-driven, slow |
| **Media and creators** (podcasts, YouTube, radio, subtitles) | Producers | Per audio hour | Captions and show notes | Medium; Buitelyn is the first test |
| **Call centres and BPO** | Enterprises | API, per minute | QA and analytics on Afrikaans lines | Contested: Vulavula and Botlhale already sell here |
| **Model and data licensing** | AI companies, enterprises | Licence or acquisition | The only Afrikaans model tuned on real conversational data | Optional upside after 12–18 months |

## Unit economics

- **Cost to transcribe an hour of audio:** R0 on the user's own machine; about R0.20–R0.50 in the cloud. Gross margin is above 90% on any paid tier.
- **Fixed running costs:** R500–R2,000 a month at small scale (domain, hosting, storage, signing certificates), rising with support and cloud fallback.
- **Cash to launch:** roughly R50,000–R110,000 over 12 months. Attorney review R15–30k, data lead work R10–40k, marketing R10–20k, GPU time R2–5k, Apple and Windows signing R5–10k, domain and hosting R3k. Your own time is the largest input and is not counted here.

## ROI scenarios, 12 months after launch

| | Conservative | Base | Upside |
|---|---|---|---|
| Paying consumers at R120/month | 50 | 300 | 1,000 |
| Churches at R350/month | 5 | 25 | 80 |
| Professional seats at R700/month | 6 | 30 | 120 |
| Enterprise or API deals | 0 | 0 | 2 at R15k/month |
| **Monthly revenue** | **≈ R12,000** | **≈ R66,000** | **≈ R260,000** |
| **Annual run rate** | ≈ R140,000 | ≈ R790,000 | ≈ R3.1 million |
| Monthly running cost | R5,000 | R15,000 | R60,000 |
| Payback on R80k cash | ~12 months | ~2 months | ~1 month |

Even the conservative case covers its costs. The base case is a solid one-person business. The upside case is a small company with a part-time team and an asset, the dataset and tuned model, that is worth more than the revenue: Afrikaans speech data of this kind does not exist elsewhere, and software businesses of this shape typically trade at three to six times annual revenue.

## What caps the value

- **Meta could add Afrikaans** to WhatsApp's built-in transcripts at any time. That erases the voice-note hook but not the meeting, professional and institutional business, which is where most of the revenue sits anyway.
- **One language.** Growth beyond the base case means isiZulu and isiXhosa, where open models are weaker and the data moat would be larger.
- **Models commoditise.** Each year the free models improve, so the lead comes from corrected data and customer relationships, not from the engine.
- **Low consumer willingness to pay** in South Africa. Business and institutional tiers carry the plan.

## The bet, with gates

1. **Month 1–2:** accuracy under 20% word error on your own meetings and voice notes, measured with the benchmark harness. If not reached, fine-tune before building further.
2. **Month 4:** 50 weekly active beta users across two or three community groups, and a visible stream of corrected transcripts flowing back.
3. **Month 8:** ten paying business or church customers. This is the point to register the company, sign the data-processing agreements and commit to the desktop app.
4. **Month 12:** base-case run rate in sight, or a clear decision to keep it as a free community tool and data asset.
