# WhatsApp voice-note and meeting-audio ingestion paths for a free Afrikaans transcription tool (as of 19 October 2026)

Scope note: everything below was checked against live pages on 19 Oct 2026. Where only third-party or secondary sources were found, this is flagged. Prices are USD unless stated. South Africa is billed by Meta in USD (per a third-party rate aggregator; see gaps), with 15% VAT typically added on top.

---

## Key Question 1: WhatsApp Business Platform (Cloud API) — receiving a voice note, formats, limits, pricing, free tier, access hurdles

### Takeaway
A Cloud API bot receives a forwarded voice note as an inbound webhook `messages[].type = "audio"` with `mime_type: "audio/ogg; codecs=opus"` and `voice: true`; the bot then fetches a short-lived (5-minute) download URL by media ID and downloads with a bearer token. The commercial picture changed materially on 1 October 2026: free-form "service" replies inside the 24-hour window are no longer free beyond 1,000 messages per business phone number per month — Meta now charges per delivered message at the market's fixed rate (third-party sources put South Africa at roughly $0.0076–$0.0095 per message; Meta's own page confirms the SA utility/auth rate "increased" on 1 Oct 2026 but the USD figure is only in the CSV/PDF rate card). Inbound user messages remain free (users never pay; Meta charges only delivered business messages). A solo developer can get a Meta-provided test number quickly, but production requires a Meta Business Portfolio, a registered phone number, display-name review, a payment method (now mandatory for service messages beyond the free tier), and business verification for scaling beyond 250 business-initiated recipients/day.

### Cited Findings

**Webhook / media flow and formats**
- Inbound audio webhooks carry an audio object with `mime_type "audio/ogg; codecs=opus"`, a media `id`, and `voice: true` for voice notes (as opposed to attached audio files) — [Meta webhook reference: audio messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/audio/); third-party confirmation that `voice` distinguishes a recorded voice note from an attached audio file and that type should be read from `mime_type`, not a URL extension — [Bird docs](https://bird.com/docs/guides/whatsapp/receiving-whatsapp/audio)
- Webhook envelope structure: `object: "whatsapp_business_account"` → `entry[]` → `changes[]` → `value` (with `metadata.phone_number_id`, `contacts[]`, `messages[]`), `field: "messages"`; message objects vary by `type` — [Meta webhook payload examples](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples)
- Retrieve media URL: `GET https://graph.facebook.com/<API_VERSION>/<MEDIA_ID>?phone_number_id=<ID>` with `Authorization: Bearer <ACCESS_TOKEN>`; then `GET` the returned URL with the same bearer header (fails without token). Media URLs expire after **5 minutes**; media IDs delivered in **webhooks expire after 7 days**; media IDs from API uploads expire after 30 days. A 404 on download means fetch a fresh URL and retry, then renew the token — [Meta Cloud API media reference](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- Supported audio MIME types: `audio/aac`, `audio/amr`, `audio/mpeg`, `audio/mp4`, `audio/ogg` (OPUS codec only; mono input only; base `audio/ogg` without opus is rejected). Max audio size 16 MB. **Incoming media messages are limited to 100 MB; larger files trigger webhook error 131052** — [Meta Cloud API media reference](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- Voice messages sent *by the business* must be `.ogg` with OPUS codec or the `voice` flag is ignored and a regular audio message is delivered; the inline play icon only appears for files ≤ 512 KB — [Meta audio messages doc](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages); [360dialog voice message beta](https://docs.360dialog.com/docs/messaging/media/voice-message-beta-program)
- Since 17 March 2026 business-sent voice messages receive a "played" status webhook on first play — [Meta audio messages doc](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages)

**Pricing model (Meta, primary source)**
- Per-message pricing effective **1 July 2025** ("Meta charges on a per-message basis, aligned to industry standards"), charged only on delivery; users never pay to message businesses — [Meta pricing](https://developers.facebook.com/docs/whatsapp/pricing)
- Service (free-form, non-template) messages were free from **1 Nov 2024 through 30 Sep 2026**. **From 1 Oct 2026 Meta "resumed charging, on a per-message basis, for messages that were previously free"**; the pricing type changed from `free_customer_service` to `regular`. Affected: service messages beyond the free tier, and "utility messages sent in response to users (thus in an open customer service window)" (which had been free since 1 July 2025) — [Meta pricing](https://developers.facebook.com/docs/whatsapp/pricing); [Meta pricing updates](https://developers.facebook.com/docs/whatsapp/pricing/updates-to-pricing)
- **Free tier: "Meta provides every business phone number with a free tier of 1,000 service messages per month."** Unused messages do not roll over; Meta "charges as of the 1,001st service message per month." Businesses without a payment method on file by 30 Sep 2026 have service messages stop being delivered once the free tier is used — [Meta pricing updates](https://developers.facebook.com/docs/whatsapp/pricing/updates-to-pricing); [Meta pricing](https://developers.facebook.com/docs/whatsapp/pricing)
- Eligible governments and non-profits keep free service messages beyond the tier through 31 Dec 2027 — [Meta pricing updates](https://developers.facebook.com/docs/whatsapp/pricing/updates-to-pricing)
- Free entry point (FEP): when a user messages from a Click-to-WhatsApp ad, "the FEP window may remain open for up to 7 days" and marketing/utility/authentication/service messages are not charged within it — [Meta pricing](https://developers.facebook.com/docs/whatsapp/pricing). (An older guide describes this as a 72-hour window — [Omnichat](https://blog.omnichat.ai/whatsapp-pricing-2025/); Meta's current page says up to 7 days.)
- Volume tiers apply only to utility and authentication messages, reset monthly — [Meta pricing](https://developers.facebook.com/docs/whatsapp/pricing)
- Oct '26 rate card updates table: South Africa row shows utility and authentication marked "Increase"; 40 rates updated; nine markets moved out of regional pricing. Exact USD values are only in the linked CSV/PDF rate cards — [Meta pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)
- Other 2026 timeline items: 1 Jul 2026 "Meta Business Agent" became a message category; 16 Feb 2026 "AI Providers" pricing policy took effect — [Meta pricing updates](https://developers.facebook.com/docs/whatsapp/pricing/updates-to-pricing)

**South Africa rates (secondary sources — Meta's SA USD figures not directly retrievable)**
- Pre-October 2026 SA rates (effective 1 Jul 2026): marketing $0.0379; utility $0.0076; authentication $0.0076; authentication-international $0.0200 — [ChatMaxima SA pricing page](https://chatmaxima.com/whatsapp-api-pricing/south-africa/) (as summarised in search snippet); ZAR equivalents ≈ R0.62 marketing and ≈ R0.12 utility — [Paton Brands](https://patonbrands.com/whatsapp-business-is-about-to-get-more-expensive-for-south-african-companies/)
- Post-1-Oct-2026 SA rates per the same aggregator page when fetched: marketing $0.0379; utility $0.0095; authentication $0.0095; authentication-international $0.0200; **service $0.0095** (first 1,000 per number/month free); "South Africa is billed in USD"; 15% VAT excluded — [ChatMaxima SA pricing page](https://chatmaxima.com/whatsapp-api-pricing/south-africa/). Note: this page also claims utility templates inside an open window "remain free", which contradicts Meta's own page (Meta says they are charged from 1 Oct 2026) — treat Meta as authoritative.
- A South African tech outlet estimated the service reply at "about $0.0076, or 12 cents [ZAR], per delivered message" from 1 Oct 2026 — [EVE Zone (19 Aug 2026)](https://evezone.evetech.co.za/daily-drop/whatsapp-business-reply-charge-sa-guide); this conflicts with ChatMaxima's $0.0095 and probably reflects the pre-increase utility rate.
- BSP-side statement that "rates for service messages will be the same as utility and authentication rates, by market" — [Picky Assist](https://pickyassist.com/blog/whatsapp-pricing-changes-october-2026/); Meta's page groups utility/authentication/service as "Fixed, per published rates" but does not explicitly say they are equal — [Meta pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)
- Alibaba Cloud's BSP notice lists South Africa among markets with utility and authentication increases on 1 Oct 2026 and confirms 1,000 free service messages per business phone number — [Alibaba Cloud ChatApp notice](https://www.alibabacloud.com/help/en/chatapp/whatsapp-message-rate-adjustments-and-service-conversation-message-billing)

**Access, verification and limits**
- Getting started requires a Meta developer account, a Business Portfolio (created during app creation), a connected WhatsApp Business Account; a test business phone number "is generated and registered for you automatically"; temporary tokens expire quickly so a System User permanent token with `whatsapp_business_messaging`, `whatsapp_business_management`, `business_management` is needed; webhooks are needed to receive messages/status — [Meta get started](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started); [Meta phone numbers](https://developers.facebook.com/docs/whatsapp/cloud-api/phone-numbers)
- Test number recipients: in App Dashboard → WhatsApp → API Setup → "Manage phone number list", each recipient verifies with a code; "up to 5 in total" — [Meta get started (as summarised)](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/); confirmed by [WANotifier](https://help.wanotifier.com/en/article/test-phone-number-limitations-kt0ly2/) and [seven.io](https://help.seven.io/en/whatsapp/whatsapp-meta-test-number). Test numbers cannot be used for customer traffic — [WANotifier](https://help.wanotifier.com/en/article/test-phone-number-limitations-kt0ly2/)
- Meta-provided 555 numbers: up to two per business; verified automatically; cannot be migrated or used outside the platform; display name must be approved before sending — [Clickatell](https://clickatell.com/help-center/whatsapp/business-accounts-profiles/can-i-set-up-a-test-number-in-whatsapp-business-api); [msg91](https://msg91.com/help/whatsapp/whatsapp-display-name-approval-required-before-sending-messages)
- New business portfolios are capped at two registered business phone numbers, raised to 20 on verification or on reaching the 2,000 messaging limit; a display name is required at registration with statuses `APPROVED`, `PENDING_REVIEW`, `DECLINED` — [Meta phone numbers](https://developers.facebook.com/docs/whatsapp/cloud-api/phone-numbers)
- Display-name rules: must represent the business; "Test" suffix allowed if associated with the business; avoid "Verified"/"Official"; personal names and slogans are common rejection reasons; review typically a day or two — [360dialog display name guidelines](https://docs.360dialog.com/partner/waba-management/waba-profile-and-compliance/whatsapp-display-name-guidelines); [3CX community](https://www.3cx.com/community/threads/how-long-does-it-take-for-the-test-whatsapp-number-to-become-a-production-number.116932/)
- Messaging limits apply to **business-initiated** messages to unique recipients "outside of a customer service window" in a moving 24-hour period: new portfolios start at **250**, then 2,000, 10,000, 100,000, unlimited. Reaching 2,000 requires business verification OR delivering 2,000 quality template messages to unique numbers in 30 days; auto-scaling above that needs high quality plus using ≥ half the limit in 7 days — [Meta messaging limits](https://developers.facebook.com/docs/whatsapp/messaging-limits). (Implication for a transcription bot: replies to user-initiated voice notes are inside the service window and do not count toward this limit.)
- Registration endpoint rate limit: 10 requests per business number per 72-hour window — [Meta registration](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration/)
- Business verification: "Meta's processing time for business verification varies by region and can take several weeks"; verification is free; required "before you can move into production" per Twilio's flow; unlocks higher limits, >2 senders, Official Business Account — [Twilio self sign-up](https://www.twilio.com/docs/whatsapp/self-sign-up)
- ToS: effective 15 Jan 2026 "AI Providers" (providers of AI/ML technologies such as LLMs, generative AI platforms, general-purpose AI assistants) may only offer general-purpose AI assistants on the WhatsApp Business Platform where Meta is legally required to permit it (EU/EEA, Brazil, Italy, Türkiye listed); service messages by AI Providers in those markets are charged from market-specific dates — [Meta AI Providers pricing policy](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/ai-providers/). The page does not say whether a narrow single-purpose tool (e.g., transcription) counts as an AI Provider.

### Inferences
- For a free end-user tool, the cost driver is the bot's *replies*, not inbound voice notes. One voice note → one transcript reply = one service message. With 1,000 free service messages/number/month, the first ~1,000 transcriptions per month are free; above that, at the SA rate (≈ $0.0076–$0.0095 + 15% VAT), 10,000 transcript replies/month would cost roughly $70–95 (≈ R1,200–1,700 at ~R17.5/USD) before BSP fees. A long transcript split across several messages multiplies this.
- Meta now requires a payment method on file for service messages to keep being delivered past the free tier, so a "free for users" bot still needs a billed Meta/BSP account.
- Since replies happen inside the 24-hour customer-service window opened by the user's voice note, the 250-recipient business-initiated limit is not a practical ceiling; the practical ceilings are the 100 MB inbound media cap (voice notes are far smaller) and the 7-day webhook media ID / 5-minute URL expiry (download promptly).
- The "AI Providers" ToS clause is a residual risk: a transcription bot is not a "general-purpose AI assistant", but the definition is broad ("providers of AI/ML technologies"), and Meta has not published guidance on narrow tools. In South Africa (not one of the listed legally-required markets), a general-purpose assistant would simply be disallowed; a transcription-only bot is more likely to be treated as an ordinary business use, but this is unconfirmed.

### Gaps
- Meta's official USD rate for South Africa after 1 Oct 2026 (utility/auth/service) is published only in a CSV/PDF rate card I could not fetch; the $0.0095 figure comes from a third-party aggregator and conflicts with another SA source quoting $0.0076.
- Whether service messages are billed at exactly the utility rate is stated by BSPs, not explicitly by Meta's page.
- I could not retrieve Meta's business-verification help article (document list, whether sole proprietors/individuals can verify). Twilio's doc confirms it is free and can take weeks.
- Meta's page does not state per-second throughput limits for Cloud API (older docs cited 80 mps default); not confirmed as current.
- No official Meta statement on whether a narrow transcription bot falls under the "AI Providers" ToS definition.

---

## Key Question 2: BSPs — Twilio (and sandbox), 360dialog, Infobip, Wati: fees on top of Meta, minimums, sandbox limits

### Takeaway
Twilio adds a flat $0.005 per message (inbound *and* outbound) with no monthly fee and passes Meta's rates through unmarked; its shared sandbox is testing-only (users must `join <code>`, joins expire after 3 days, 1 message/3 s). 360dialog charges a flat monthly fee per number (from €49) with Meta fees passed through; Wati charges $49–$349/month plus a 20–80% markup on Meta rates; Infobip pricing could not be found. Direct Cloud API (no BSP) has no platform fee at all.

### Cited Findings
- Twilio WhatsApp: "$0.005 per message, inbound or outbound"; failed-message processing fee $0.001; no platform monthly fee; Meta template fees passed through (calculator shows utility/auth "starts at $0.0034" for the US) — [Twilio WhatsApp pricing](https://www.twilio.com/en-us/messaging/channels/whatsapp/pricing); Twilio adds no markup to Meta's rates — [Customer.io WhatsApp billing](https://docs.customer.io/accounts/billing/whatsapp-billing/)
- Twilio published two notices titled "Changes to WhatsApp's Pricing October 2026" (Meta charging service messages and in-window utility from 1 Oct 2026; Twilio per-message fee unchanged) — [Twilio support notice](https://support.twilio.com/hc/en-us/articles/53100480177819-Notice-Changes-to-WhatsApp-s-Pricing-October-2026) (page returned 403 to fetch; content per search snippet)
- Twilio Sandbox: shared number +1 415 523 8886; users join by sending `join <sandbox-code>`; joins expire after 3 days; only three pre-approved templates; 24-hour window applies; sends 1 message every 3 seconds; "for testing and discovery purposes only", some countries restricted — [Twilio sandbox docs](https://www.twilio.com/docs/whatsapp/sandbox)
- Twilio sender registration: Twilio or non-Twilio number allowed (must receive OTP by SMS/voice); one WABA per Twilio account; display name reviewed by Meta — if rejected the number is limited to 250 business-initiated messages/24h; business verification "before you can move into production", can take several weeks, free — [Twilio self sign-up](https://www.twilio.com/docs/whatsapp/self-sign-up)
- 360dialog: Regular €49/number/month (24/7 support, SLA < 4h, Zapier/Make/n8n); Premium €99/number/month (business verification within 48h, bundled inbox/automation); Scale €500/number/month (up to 1,000 msg/s); messaging billed as "+Meta WhatsApp Messaging Fees"; no sandbox or trial mentioned — [360dialog pricing](https://www.360dialog.com/pricing)
- Wati: plan prices reported variously as $49/$99/$299 (annual) to $69/$149/$349 (monthly); markup on Meta rates estimated at ~20% by one source and 60–80% by another; Wati help centre confirms service messages billable from 1 Oct 2026 with 1,000 free per WABA/month — [Wati pricing guide](https://support.wati.io/articles/wati-pricing-a-complete-guide-vsQQurXlqh); [Setsmart](https://setsmart.io/blog/wati-pricing); [getmacha](https://www.getmacha.com/blog/wati-pricing-explained)
- Infobip onboarding uses Meta Embedded Signup — [Infobip docs](https://infobip.com/docs/whatsapp/get-started/embedded-signup); no per-message pricing found.

### Inferences
- Twilio's $0.005 per message applies to *inbound* voice notes too, so at scale Twilio costs more than Meta's own charges for a reply-heavy bot (inbound note + reply = $0.01 Twilio + Meta's ≈ $0.0095). Direct Cloud API avoids this entirely and is the cheapest path; Twilio's sandbox is the fastest way to prototype inbound audio before any Meta approvals.
- 360dialog's €49/month floor is pointless for a free tool unless the hosted inbox/support is needed.

### Gaps
- Infobip WhatsApp per-message and monthly pricing not found.
- Twilio's sandbox page does not state whether inbound audio/media is supported (it is widely used for this, but not documented on that page).
- The two Twilio "October 2026" notices could not be fetched (HTTP 403).

---

## Key Question 3: Unofficial libraries (Baileys, whatsapp-web.js, Cobalt-style) — ban risk, ToS, reliability

### Takeaway
Both major unofficial libraries explicitly state WhatsApp does not permit bots/unofficial clients and that bans are possible; WhatsApp's Terms prohibit auto-messaging, derivative works and software that "function[s] substantially the same as our Services", with suspension/termination as the remedy. Malicious Baileys forks on npm add supply-chain risk. This path is unsuitable for a public product that users depend on.

### Cited Findings
- whatsapp-web.js README disclaimer: "WhatsApp does not allow bots or unofficial clients on their platform, so this shouldn't be considered totally safe" and "it is not guaranteed you will not be blocked by using this method." ~22.8k stars, 901 commits, 59 open issues — [whatsapp-web.js on GitHub](https://github.com/pedroslopez/whatsapp-web.js)
- Baileys README: "not affiliated, associated, authorized, endorsed by, or in any way officially connected with WhatsApp"; maintainers "do not in any way condone the use of this application in practices that violate the Terms of Service"; "discourage any stalkerware, bulk or automated messaging usage" and do not condone business use; MIT licence; ~11.4k stars; v7.0.0 breaking-change banner — [Baileys on GitHub](https://github.com/WhiskeySockets/Baileys)
- Baileys works by emulating the WhatsApp Web WebSocket client; its docs warn misuse "can get your number banned from WhatsApp" — [Evolution API docs on Baileys](https://mintlify.com/EvolutionAPI/evolution-api/whatsapp/baileys); Chat SDK adapter warns WhatsApp may suspend or ban numbers using unofficial automation — [chat-sdk.dev](https://chat-sdk.dev/adapters/community/baileys.md)
- Malicious Baileys forks published to npm (e.g., `diezyclutch-baileys`, `@xsat10/baileys-xsat`) performing covert actions on the authenticated account or exfiltrating data — [Vulert advisory](https://vulert.com/vuln-db/malicious-code-in-diezyclutch-baileys--npm-); [Hacktron](https://www.hacktron.ai/package/npm/%40xsat10%2Fbaileys-xsat/2.0.0); [CIRCL MAL-2026-4803](https://cvepremium.circl.lu/vuln/mal-2026-4803)
- WhatsApp Terms of Service (effective 4 Jan 2021, still current): prohibits "bulk messaging, auto-messaging, auto-dialing, and the like"; prohibits reverse engineering, modifying or creating derivative works; prohibits creating "software or APIs that function substantially the same as our Services"; WhatsApp may "modify, suspend, or terminate your access… anytime for any reason" and may disable/suspend accounts — [WhatsApp Terms of Service](https://www.whatsapp.com/legal/terms-of-service)

### Inferences
- An unofficial-client bot would run on a consumer/Business-app number that could be banned without notice, taking every user's chat history with the bot with it; combined with the npm supply-chain incidents, the operational and reputational risk is high. It is only defensible for personal/single-user experiments.

### Gaps
- No quantitative data on ban rates; all evidence is maintainer disclaimers and anecdotes. No specific info found on "Cobalt" as a WhatsApp library (likely a mis-name; not covered).

---

## Key Question 4: Non-bot path — exporting a voice note via Share and sending it to a web app / PWA (share target)

### Takeaway
On Android, a voice note can be long-pressed → Share (or found on disk under `WhatsApp/Media/WhatsApp Voice Notes/<yyyyww>/PTT-YYYYMMDD-WA00NN.opus`); on iPhone it is long-press → Forward → share icon → Save to Files / share to an app. An installed PWA can register as an Android share target (Chrome ≥ 76) for files via `share_target` with `method: POST`, `enctype: multipart/form-data` and `files[].accept`; Safari/iOS does not support Web Share Target, so iOS users must use the file picker, "Save to Files" + upload, or a native app.

### Cited Findings
- Android export: open file manager → WhatsApp → Audio/"WhatsApp Audio" (or Media → "WhatsApp Voice Notes"); long-press a message in chat and share; iPhone: press-and-hold the voice message → Forward → export (share) icon → email to self or Save to Files — [IONOS guide](https://ionos.com/digitalguide/online-marketing/social-media/how-to-save-audio-from-whatsapp); iPhone does not expose the WhatsApp media folder — [AirDroid](https://airdroid.com/file-transfer/whatsapp-audio-to-mp3)
- Filename pattern "PTT-[date]-WA[sequence].opus", e.g. `PTT-20190614-WA0044.opus`, in date-stamped subfolders of `…/Media/WhatsApp Voice Notes/` — [Tasker forum thread](https://cal1.lr.ggtyler.dev/c0k9ui) (example from a modded client) and [AirDroid](https://airdroid.com/file-transfer/whatsapp-audio-to-mp3); files are Opus and most gallery/media players don't open them (VLC does) — [AirDroid](https://airdroid.com/file-transfer/whatsapp-audio-to-mp3)
- Web Share Target: manifest `share_target` with `action`, `method: "POST"`, `enctype: "multipart/form-data"`, `params.files[]` each with `name` and `accept` (MIME types and/or extensions; recommended to list both); only installed PWAs can be share targets; the service worker intercepts the POST in a `fetch` listener, reads `formData()` and typically redirects 303; feature is experimental/not Baseline — [MDN share_target](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/share_target); [Chrome developers: Web Share Target](https://developer.chrome.com/docs/capabilities/web-apis/web-share-target) (Chrome for Android 76+, desktop 89+)
- Safari/WebKit has an open feature request for Web Share Target (bug 194593); as of the last comment only Google had shipped it — [WebKit Bugzilla 194593](https://bugs.webkit.org/show_bug.cgi?id=194593). The outgoing Web Share API (navigator.share) is supported in Safari 12.1+ — [web.dev Web Share](https://web.dev/articles/web-share)

### Inferences
- A PWA share target with `accept: ["audio/ogg", ".opus", ".ogg", "audio/*", "audio/mp4", ".m4a"]` would let Android WhatsApp users share a voice note directly into the tool in two taps with zero Meta involvement, zero per-message cost and no ToS risk; this is the cheapest and most robust free path for the Android-dominant South African market.
- iOS users need an extra step (Save to Files → upload via `<input type="file" accept="audio/*">`), or the tool needs a native iOS share extension.
- Because the exported file is already Opus in an OGG container, server-side conversion is a single ffmpeg step (see Q8).

### Gaps
- No official WhatsApp documentation of the `PTT-…-WA….opus` filename pattern; evidence is user forums/blogs. Folder names vary by Android version/device.
- Could not retrieve the caniuse table for `share_target` (page returned the homepage); Chrome Android support is confirmed via Chrome docs, Safari non-support via the WebKit bug, Firefox/Samsung Internet status not confirmed.
- Whether WhatsApp iOS "Share" exposes the raw `.opus` or a converted `.m4a` was not confirmed from an authoritative source.

---

## Key Question 5: Does WhatsApp already transcribe voice notes natively — and does it support Afrikaans?

### Takeaway
WhatsApp's built-in Voice Message Transcripts (launched 21 Nov 2024) are generated on-device from downloadable language packs; as of a 17 Sep 2026 beta report, Android supports Arabic, Spanish, Hindi, Portuguese, Russian plus (newly) English, German, French, Italian and Japanese variants, and iOS relies on Apple's on-device speech languages (English, Spanish, French, German, Italian, Japanese, Korean, Portuguese, Russian, Turkish, Chinese, Arabic, plus Danish, Finnish, Hebrew, Malay, Norwegian, Dutch, Swedish, Thai on iOS 17+). **No source lists Afrikaans**, so the product rationale for an Afrikaans transcription tool stands — but mark this as "not found" rather than "confirmed absent" because the official FAQ language list could not be retrieved.

### Cited Findings
- Launch 21 Nov 2024; "Transcripts are generated on your device"; "a few select languages to start"; enable via Settings → Chats → Voice message transcripts; long-press a message → "Transcribe" — [WhatsApp blog](https://blog.whatsapp.com/introducing-voice-message-transcripts)
- Android launch languages: English, Portuguese, Spanish, Russian — [Android Central](https://androidcentral.com/apps-software/whatsapp-introduces-voice-message-transcripts); [TechCrunch](https://techcrunch.com/2024/11/21/whatsapp-rolls-out-voice-message-transcripts); Hindi added in beta — [Android Authority](https://androidauthority.com/whatsapp-voice-message-transcripts-3459477)
- iOS language list (iOS 16: English, Spanish, French, German, Italian, Japanese, Korean, Portuguese, Russian, Turkish, Chinese, Arabic; iOS 17+: Danish, Finnish, Hebrew, Malay, Norwegian, Dutch, Swedish, Thai); iPhone users need Siri enabled; transcripts off by default — [Mezha](https://mezha.media/en/2024/11/22/whatsapp-now-supports-voice-message-transcripts); [Lowyat](https://lowyat.net/2024/337926/whatsapp-voice-message-transcripts)
- 17 Sep 2026: WhatsApp beta for Android 2.26.37.5 rolling out additional language packs (English, German, French, Italian, Japanese variants) on top of Arabic, Spanish, Hindi, Portuguese, Russian; processing "entirely on the device" via downloaded packs; Afrikaans not mentioned — [WABetaInfo](https://wabetainfo.com/whatsapp-is-rolling-out-new-languages-for-voice-transcriptions/); [SammyFans](https://www.sammyfans.com/2026/09/17/whatsapp-expands-voice-message-transcription-to-more-languages/)

### Inferences
- Because Android transcription is pack-based and Meta has only added major world languages in ~2 years, Afrikaans native support looks unlikely in the near term; iOS support would depend on Apple adding Afrikaans to on-device speech recognition, which no source indicates.
- A notable UX implication: because WhatsApp's own feature is on-device, a third-party tool that uploads audio to a server must be explicit about privacy (POPIA) — this is a differentiator WhatsApp will market against.

### Gaps
- The official WhatsApp Help Center page listing supported transcript languages was not found in search results; the absence of Afrikaans is inferred from press/beta coverage, not from an authoritative list.

---

## Key Question 6: Telegram Bot API as a comparison channel

### Takeaway
Telegram's Bot API delivers voice notes as a `voice` object (`file_id`, `duration`, `mime_type`, `file_size`); the bot calls `getFile` and downloads files up to 20 MB; bots message users at no cost; no business verification, display-name review or per-message fee exists. It is the frictionless technical baseline, but Telegram penetration in South Africa is far below WhatsApp's.

### Cited Findings
- `Voice` object: "represents a voice note" with `file_id`, `file_unique_id`, `duration`, optional `mime_type`, `file_size`; `Audio` object for music-type files — [Telegram Bot API](https://core.telegram.org/bots/api)
- Bots can download files up to 20 MB via `getFile` and send files up to 50 MB; a self-hosted local Bot API server removes the download limit and raises uploads to 2,000 MB; bots message users "at no cost" subject to rate limits (≈1 msg/s per chat, 20/min in groups, ~30/s bulk) — [Telegram Bot FAQ](https://core.telegram.org/bots/faq); [Telegram Bot API](https://core.telegram.org/bots/api)

### Inferences
- Telegram voice notes are also OGG/Opus, so the same ffmpeg pipeline serves both channels; a Telegram bot is a good zero-cost fallback and demo channel, and a way to offer "no 1,000-message cap" to power users.

### Gaps
- Telegram's Bot API page did not state the voice MIME type in the fetched section; OGG/Opus for voice notes is widely documented but not quoted here. No South Africa Telegram usage statistics were researched (out of scope).

---

## Key Question 7: Meeting audio ingestion — upload, in-browser recording, meeting bots (Recall.ai, Vexa, Attendee, Meeting BaaS, Zoom SDK), cloud-recording export

### Takeaway
File upload is free and universal; browser recording works on Chrome/Android (WebM/Opus) and Safari/iOS ≥ 14.5 (MP4/AAC only) but iOS standalone-PWA recording is unreliable when backgrounded/locked; meeting bots cost $0.30–$0.50 per recording hour hosted (Recall.ai $0.50/h, Vexa $0.30/h, Meeting BaaS $0.35–0.50/h) or $0 self-hosted (Vexa Apache-2.0, Attendee open source) but a Zoom bot that joins other accounts' meetings requires Zoom App Review (≈4–6 weeks) and a raw-data entitlement; Zoom/Meet/Teams cloud recordings can be exported by the host (Zoom via API/webhook, Meet to Drive "Meet Recordings", Teams to OneDrive/SharePoint) and then uploaded.

### Cited Findings

**Meeting bots (hosted)**
- Recall.ai: Pay-As-You-Go dropped from $0.70 to **$0.50 per recording hour**; "We no longer charge a monthly platform fee"; built-in transcription $0.15/recording hour (or pay partner ASR directly); 7 days free storage then $0.05/media-hour per additional 30 days; complimentary credits on sign-up; supports Google Meet, Microsoft Teams, Zoom, Slack Huddles, Webex, GoTo (per page icons) — [Recall.ai pricing blog (updated 14 Sep 2026)](https://recall.ai/blog/new-recall-ai-pricing-for-2026). Older third-party figures ($1,000/month platform fee + ~$1/h) are outdated — [DEV Community](https://dev.to/lirim_kon/3-best-alternatives-to-recallai-398n)
- Vexa: "Build on Vexa" **$0.30 per bot-hour**, +$0.20/h for real-time transcription ($0.50 all-in); Individual $12/seat/month (1 concurrent bot, unlimited meetings); open source Apache-2.0, self-host via Docker Compose/Kubernetes, $0 licence; $2 free credit (~6 bot-hours), top-ups from $10; Google Meet, Teams, Zoom — [Vexa pricing](https://vexa.ai/pricing)
- Meeting BaaS: prepaid tokens, 1 token = 1 recording hour incl. diarization; packs $50/100 ($0.50), $100/220 ($0.45), $625/1,550 ($0.40), $1,500/4,250 ($0.35); tokens never expire; Pay-as-you-go plan free with up to 8 free hours; Pro $99/mo, Scale $199/mo, Enterprise $299/mo; transcription add-on +0.25 tokens/h (Gladia) or +0.05 tokens/h BYOK; Zoom, Meet, Teams — [Meeting BaaS pricing](https://meetingbaas.com/pricing)
- Attendee: open-source meeting bot API (Django, single Docker image, Postgres + Redis); Zoom join flow documented; Google Meet/Teams/Webex on roadmap per README; Zoom OAuth credentials + Deepgram key configured in UI; Kubernetes production guidance is part of a paid self-hosting plan; hosted instance "sign up for free"; ~761 stars — [Attendee on GitHub](https://github.com/attendee-labs/attendee)
- Zoom bots: Meeting SDK apps "need to go through our App Review process to join Meetings outside their own account"; reviewers check production credentials/scopes and whether it joins as a bot; bot must trigger the recording-consent flow — [Zoom SDK feature review requirements](https://developers.zoom.us/docs/distribute/sdk-feature-review-requirements/); [Zoom dev forum](https://devforum.zoom.us/t/how-can-i-create-a-zoom-bot-that-joins-meetings-and-interacts-as-a-participant/80937); review "typically takes 4–6 weeks", unlisted publishing still requires approval — [Recall.ai on Zoom SDK compliance](https://www.recall.ai/blog/zoom-sdk-compliance-requirements); raw audio/video needs a Raw Data entitlement requested from Zoom Developer Support (`HasRawdataLicense()` returns 0 without it) — [Zoom dev forum raw-data thread](https://devforum.zoom.us/t/request-to-enable-meeting-sdk-raw-data-entitlement-sending-external-video-audio/144868)

**Cloud-recording export**
- Zoom: subscribe to the recording-completed webhook, call the recordings endpoint for `download_url` (MP4) and transcript files (`file_type: TRANSCRIPT`, `recording_type: audio_transcript`); cloud transcripts only after the meeting; local recordings are not visible to the API — [Recall.ai: 7 APIs to get Zoom transcripts](https://recall.ai/blog/7-apis-to-get-zoom-transcripts-a-comprehensive-guide); [Zoom community](https://community.zoom.com/meetings-2/enhancement-request-for-transcripts-to-be-downloaded-via-the-api-when-the-meeting-recording-is-stored-locally-81294)
- Google Meet: recordings save to the organiser's My Drive → "Meet Recordings"; "Still processing" until ready; download via Drive's More → Download — [Google Meet help](https://support.google.com/meet/answer/9308681)
- Microsoft Teams: channel-meeting recordings go to the channel's SharePoint "Recordings" folder; other meetings to the recorder's OneDrive "Recordings" folder; no longer saved to Stream; tenant admins may set expiry; download rights depend on ownership/permissions — [Microsoft support](https://support.office.com/en-gb/article/ready-to-play-7d7e5dc5-9ae4-4b94-8589-27496037e8fa); [University of Edinburgh IS](https://information-services.ed.ac.uk/computing/comms-and-collab/office365/teams/teams-meeting-recordings-on-sharepoint-onedrive)

**Browser recording (MediaRecorder) and iOS limits**
- MediaRecorder support: Chrome 49+, Firefox 29+, Safari desktop 14.1+, **Safari iOS 14.5+** (disabled by default in 12–14.4), Samsung Internet 5+ — [caniuse MediaRecorder](https://caniuse.com/mediarecorder)
- Safari's MediaRecorder "currently supports the MP4 file format with H.264 as video codec and AAC as audio codec"; feature-detect with `MediaRecorder.isTypeSupported()`; `getUserMedia` in WKWebView only if the host app can capture natively — [WebKit blog: MediaRecorder API](https://webkit.org/blog/11353/mediarecorder-api/); mobile Safari only supports `audio/mp4` mimeType — [Obsidian forum](https://forum.obsidian.md/t/feature-recorder-audio-quality/21497)
- Safari-recorded `audio/mp4` blobs have caused problems for Whisper-based pipelines (poor transcripts vs Chrome files; timeslice `start(1000)` fragments); some developers fall back to a WAV encoder — [OpenAI community thread](https://community.openai.com/t/whisper-problem-with-audio-mp4-blobs-from-safari/322252); [second thread](https://community.openai.com/t/whisper-issues-with-mp4-saved-by-safari/545761)
- iOS background/lock behaviour (bug reports, no official doc): audio tracks go to `readyState "ended"` after ~30 s in background, fixed by re-calling `getUserMedia` on visibility change — [WebKit bug 204681](https://bugs.webkit.org/show_bug.cgi?id=204681); in standalone (home-screen PWA) mode a getUserMedia stream can stop on route change or fail on relaunch until device restart — [WebKit bug 252465](https://bugs.webkit.org/show_bug.cgi?id=252465); [Apple dev forum: MediaRecorder as PWA on iOS](https://developer.apple.com/forums/thread/797987); [WebKit bug 282327](https://bugs.webkit.org/show_bug.cgi?id=282327)

### Inferences
- For a free tool, meeting bots are the only path with meaningful per-use cost ($0.30–0.50 per meeting hour hosted; roughly R5–9/hour) and the only one with a multi-week approval gate (Zoom). Self-hosting Vexa/Attendee removes vendor fees but adds server cost and operational work (headless browsers per bot).
- The lowest-friction meeting path for the target audience (in-person meetings recorded on a phone) is: native phone recorder app → share/upload the file (m4a on iPhone, m4a/3gp/aac on Android) — the same share-target/file-upload mechanism as voice notes.
- In-browser recording is acceptable for short desktop sessions (Chrome → WebM/Opus) but should not be relied on for hour-long in-person meetings on iPhones: Safari only emits MP4/AAC, and standalone-PWA recording can silently stop when the screen locks. Recommend chunked uploads every N seconds with resumable state, and advise iOS users to use the Voice Memos app and share the file.
- Cloud-recording export is free but manual (host downloads from Zoom/Drive/OneDrive, then uploads); automating it requires OAuth integrations with each platform (Zoom API, Drive API, Microsoft Graph), which is additional scope.

### Gaps
- No official Apple/WebKit documentation on background/locked-screen MediaRecorder behaviour; evidence is bug reports.
- Attendee's licence name and hosted pricing are not shown on its README.
- Zoom's own timeline for App Review is not published (4–6 weeks is a third-party estimate); Raw Data entitlement criteria are not published.
- Google Meet and Teams REST-API download flows (Drive API / Graph API) were not researched in detail.

---

## Key Question 8: Audio handling — converting OGG/Opus, m4a, mp4 to 16 kHz mono WAV/FLAC with ffmpeg; chunking; typical sizes

### Takeaway
A single ffmpeg invocation normalises any WhatsApp/phone/meeting file to the 16 kHz mono 16-bit PCM most ASR models expect: `ffmpeg -i input -vn -ac 1 -ar 16000 -c:a pcm_s16le output.wav`. Long recordings should be chunked (hosted ASR APIs commonly cap uploads at ~25 MB) and WhatsApp itself caps outgoing audio at 16 MB and inbound media at 100 MB.

### Cited Findings
- Standard command: `ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le output.wav` (`-vn` drop video, `-ac 1` mono, `-ar 16000` 16 kHz, `-c:a pcm_s16le` 16-bit PCM); whisper.cpp downsamples higher rates automatically but lower rates degrade quality; OpenAI's Python `load_audio` runs the same pipeline internally (`-ac 1`, resample, `-f s16le`) — [whisper.rn audio formats](https://www.mintlify.com/mybigday/whisper.rn/core-concepts/audio-formats); [openai/whisper load_audio](https://www.mintlify.com/openai/whisper/api/load-audio); [swyx: Whisper for podcasts](https://swyx.io/whisper-for-podcasts.md); [360converter guide](https://www.360converter.com/blog/convert-video-audio-to-transcription-ready-file)
- Hosted Whisper-style APIs have a 25 MB per-file cap, so long recordings must be chunked (by time, ideally at silence boundaries) — [fast.io: Whisper file size limit](https://fast.io/resources/whisper-file-size-limit.md)
- WhatsApp: audio uploads max 16 MB; inbound media up to 100 MB; OGG must be Opus and mono — [Meta Cloud API media reference](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- Telegram bots can download files up to 20 MB — [Telegram Bot FAQ](https://core.telegram.org/bots/faq)
- Safari recordings arrive as MP4/AAC, Chrome as WebM/Opus (feature-detect) — [WebKit blog](https://webkit.org/blog/11353/mediarecorder-api/)

### Inferences
- WhatsApp voice notes are low-bitrate mono Opus (typically well under 1 MB per minute), so a 100 MB inbound cap is never hit by voice notes; it matters only if users forward hour-long meeting recordings as documents.
- 16 kHz mono PCM WAV is ~1.9 MB per minute (16,000 × 2 bytes × 60), so a 60-minute meeting is ~115 MB as WAV; keep the intermediate as FLAC or feed the ASR engine in ~10-minute chunks to stay under API caps and bound memory.

### Gaps
- No authoritative source found for the exact bitrate/size of WhatsApp voice notes (the ~1 MB/min figure is an inference, not a cited fact).
- Chunking at silence boundaries (e.g., ffmpeg `silencedetect`) was not researched with a citation.

---

## Overall synthesis for the report writer

1. **Cheapest, lowest-risk ingestion for a free Afrikaans tool:** (a) Android PWA share target + universal file upload (voice notes exported as `PTT-….opus`; phone-recorded meetings as m4a), and (b) a Telegram bot as a zero-cost secondary channel. Neither involves Meta fees, approvals or ToS exposure.
2. **Official WhatsApp bot (Cloud API direct, no BSP):** technically straightforward (webhook → media ID → 5-minute URL → download OGG/Opus → ffmpeg), approvals manageable for a solo developer (test number with 5 recipients immediately; production needs Business Portfolio, display-name review, payment method; verification for >250 business-initiated/day, which a reply-only bot does not need). **Commercially, since 1 Oct 2026 each transcript reply beyond 1,000/number/month costs ≈ $0.0076–0.0095 (+15% VAT) in South Africa**, so a "free" bot has a real marginal cost that scales with usage; Twilio adds $0.005 per inbound and outbound message; 360dialog adds €49+/month.
3. **Unofficial libraries:** explicit ban risk, ToS violation, supply-chain malware; unsuitable for a public product.
4. **WhatsApp's own transcription** is on-device and does not list Afrikaans in any source found (Android packs: EN/DE/FR/IT/JA/AR/ES/HI/PT/RU; iOS: Apple's list) — rationale for an Afrikaans tool holds, pending confirmation against WhatsApp's official FAQ.
5. **Meetings:** file upload/export is free; browser recording is fine on Chrome but fragile on iOS Safari (MP4/AAC only, stops when backgrounded in PWA mode); meeting bots cost $0.30–0.50 per recording hour hosted or require self-hosting plus Zoom App Review (weeks) for Zoom.
