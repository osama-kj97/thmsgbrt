# 06 — Economy, Monetization & LiveOps (Economy & LiveOps Designer)

> Status: research + decisions for pre-production. Date: 2026-11-23.
> Network note: only `developer.apple.com` and `developer.android.com` could be fetched this session (Google Play policy center, PEGI, FTC, EU and trade-press hosts were blocked by the sandbox proxy). Claims from those hosts come from search-result summaries and are tagged **(unverified)**. Re-check them before soft launch.

## TL;DR
1. **Model: "Fair Free + Supporter".** The download and the whole campaign are free. Monetization is (a) **opt-in rewarded ads only**, with no interstitials or banners; (b) a one-time **Supporter Pack** (~$4.99) that removes all ad prompts by granting the ad rewards automatically, plus a cosmetic and a digital soundtrack; (c) **direct-priced cosmetics**. A non-expiring cosmetic **Chapter Pass** comes later, once there are ≥3 worlds. This **confirms the brief's "fair F2P" hypothesis, with changes**: no premium currency, no time-limited pass, and no rotating or countdown offers.
2. **Currencies: two, and neither is sold.** *Glow* is the in-level build currency, which ties into the Light-vs-Dark hook. *Amber Sap* is the meta soft currency for the research tree. There is **no hard currency** at launch. Stars measure progress and are not spent.
3. **Fairness rules:** we never sell power, levels, Amber Sap, energy or lives. We sell no randomized paid items and add no FOMO timers. Every gameplay item can be earned. The game can be finished with zero ads and zero spend at the default pacing.
4. **Compliance is driven by the age rating.** Paid random items now push ratings to 16+ (Apple Australia; PEGI from June 2026 (unverified)). Countdown offers push PEGI to 12 (unverified). The EU's Digital Fairness Act (DFA) proposal (Nov 2026) targets paid loot boxes and pay-to-win for minors (unverified). By selling neither, we can **target Apple 9+ / PEGI 7 / ESRB E10+** and stay out of the Kids/Families programmes, with the Play target audience set to 13+.
5. **LiveOps:** weekly challenge level, monthly level drop, quarterly world. Everything runs through **signed remote-config JSON** checked in CI by a **fairness/policy linter**. Agents automate content, balancing sims, reports and rollouts. Prices, SKUs, consent and age logic stay **human-gated**.

---

## 1. Business model comparison

| Model | Fit for tiny AI studio, no UA | Player sentiment (TD/strategy) | Revenue ceiling | Compliance load | Verdict |
|---|---|---|---|---|---|
| **Premium** ($4.99–6.99) | Poor. A price wall kills organic installs, and we have no brand. Bloons TD 6 sells at about $6.99 premium with IAP layered on top, but that rests on an established franchise (unverified) | Best ("no ads, no P2W") | Low without featuring | Lowest | Reject for launch |
| **Premium + DLC worlds** | Same funnel problem; DLC splits a small player base | Good | Low–mid | Low | Reject (revisit on PC/Switch ports) |
| **Fair F2P (rewarded ads + cosmetics + pass)** | Good funnel. Ads monetize the 97–99% who never pay (Unity puts IAP payers at about 1–3% of DAU (unverified)) | Rewarded ads are the best-tolerated format. Deloitte 2025: 52% would quit over multiple *disruptive* ad features (unverified) | Mid | Medium (ads SDK, consent, ATT) | **Base of the pick** |
| **Free + one-time ad-free unlock** | Good. Simple and liked; a familiar "pay once, own it" for premium-minded players | Very good | Low–mid alone | Low | **Merged into the pick** (Supporter Pack) |
| **Hybrid (hard currency, offers, gacha, pass)** | Needs UA, LiveOps staff and data science. Sensor Tower: IAP-first hybrids out-earn ads-first ones (unverified) | Poor in strategy communities if it touches power | Highest | **Highest**: loot-box rules, PEGI 12/16, EU CPC currency principles, DFA | Reject |

**Decision: "Fair Free + Supporter".**
- **Free funnel.** Store featuring and word of mouth are our only acquisition channels, and a free app converts browsers into installs.
- **Rewarded-only ads.** The player chooses when to watch, so ads never interrupt a 3–6 minute TD level.
- **Supporter Pack.** Premium-minded players can effectively buy the game once. The pack turns every ad bonus into an automatic bonus, so supporters lose nothing by skipping ads.
- **Cosmetics.** These cost us content only, which agents can generate cheaply. They do not affect balance.
- **No premium currency.** The EU CPC Key Principles (March 2025) cover *purchasable* virtual currencies, discourage multiple currencies and push for real-money price display (unverified). Having no purchasable currency takes us out of their scope.

**Soft-launch test (agent-run, owner approves):** the control is a fully free campaign. The variant gates worlds 2+ behind a $4.99 "Full Hollow" unlock (free-trial premium). We pick the winner on ARPU × D30.

## 2. Economy design

### 2.1 Currencies & progress meters
| Name | Type | Earned by | Spent on | Sold? |
|---|---|---|---|---|
| **Glow** | In-level, resets each level | Starting allotment, defeating shadows, lantern "reveal" bonuses, early-wave call bonus | Building, upgrading and repositioning towers; hero ability | **Never** |
| **Amber Sap** | Meta soft currency | Level clears, star bonuses, replays, weekly challenge, achievements, rewarded-ad doubling (capped) | Grove Research tree (tower tiers), hero talents | **Never** |
| **Stars** (1–3 per level) | Progress meter, not spent | Level performance | Unlocks challenge modes and Heroic difficulty | Never |
| Hero XP | Meter | Playing levels with the hero | Hero level-ups (fixed curve) | Never |

There is **no hard currency.** All IAPs are direct SKUs priced in real money, so the price shown is the price paid.

### 2.2 Sources & sinks (vertical slice, 10 levels)
| Level | 1 | 2 | 3 | 4 | 5 (mini-boss) | 6 | 7 | 8 | 9 | 10 (boss) | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| First-clear Amber | 40 | 50 | 60 | 70 | 90 | 90 | 100 | 110 | 120 | 200 | **930** |
| Star bonus (one-time, +10/★) | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 | **300** |
| New tower unlocked (free) | 2 towers | +1 | – | +1 | – | +1 | – | +1 | – | – | 6 |

- **Replays** pay 25% of the first-clear Amber. This keeps grinding possible but slow, and stops replays outpacing new content.
- **Rewarded "Double Amber"** applies to end-of-level Amber only. It is capped at 3 per day, adding at most about 20% to daily earnings.
- **Grove Research (the sink).** Each of 6 towers has 3 tiers costing **60 / 150 / 300**.
  - Tier 1 + Tier 2 for all six = **1,260 Amber**. This is about what a player earns by 3-starring the slice (1,230), so completionists can finish it.
  - Tier 3 (1,800 total) is post-slice content.
  - Hero talents use Hero XP only.
- **Free respec, always.** Experimenting with builds must never cost anything.

**Pacing targets** (enforced by headless bot sims in CI):

| Metric | Target |
|---|---|
| First-attempt win rate, L1–3 | 90%+ |
| First-attempt win rate, L4–7 | 70–80% |
| First-attempt win rate, L8–9 | 55–65% |
| First-attempt win rate, L10 boss | 40–55% |
| Win rate with zero research purchased, L1–9 | ≥50% |
| Win rate with zero research purchased, boss | ≥30% |
| Slice length, first pass | 50–70 min |
| Slice length to 30 stars | 2.5–3.5 h |

The zero-research targets prove that skill can beat the upgrades.

**Beyond the slice:** each world has 10 levels with about 1.6× the Amber of the previous world, and one new tower or hero track. Research tiers 4–5 are sidegrades (branch choices), not more raw power, which keeps power creep flat. New heroes are **earned by play** (world completion or achievement chains).

### 2.3 Rewarded-ad placements (all opt-in, labelled "Watch ad")
| Placement | Reward | Cap |
|---|---|---|
| `double_amber` | ×2 end-of-level Amber | 3/day |
| `second_dawn` | Revive on defeat: restore 5 lives and +50 Glow | 1 per level attempt |
| `lantern_start` | +60 starting Glow on a *retry* | 1 per level |
| `daily_gift` | Fixed Amber gift (deterministic, never random) | 1/day |

The Supporter Pack grants all four automatically, with the same caps.

### 2.4 What is monetized vs. never monetized
| Monetized | Never monetized (fairness rules, enforced by CI linter) |
|---|---|
| Supporter Pack (ad-prompt removal + auto-rewards + cosmetic + OST), about $4.99 | Towers, tower stats, research, heroes' power, Amber, Glow, Stars |
| Cosmetic skins (owls, towers, projectiles/lantern hues, Hollow Tree décor), $0.99–2.99 | Campaign levels/worlds (unless the soft-launch test wins *and* the owner approves) |
| Cosmetic bundles, $4.99–7.99 (fixed catalogue, no timers) | Energy/stamina/lives: **no energy system at all** |
| Later: Chapter Pass, $4.99, cosmetic + lore only, **never expires** | Paid randomized rewards of any kind. All rewards are deterministic |
| | Countdown timers, "only N left", rotating shops, fake discounts |
| | Event cosmetics that are lost forever. Each returns within 6 months |
| | Pushing purchases on players signalled as minors |

Prices are provisional and use store price tiers.

## 3. Store & legal compliance (as of Nov 2026)

| Area | Rule (source) | What we must do |
|---|---|---|
| **Apple IAP** | Unlocking features or currency must use IAP; purchased credits "may not expire"; a restore mechanism is required (Guideline 3.1.1, last updated Oct 16 2026) | StoreKit for every SKU; "Restore Purchases" button; nothing ever expires |
| **Apple loot boxes** | "Must disclose the odds of receiving each type of item … prior to purchase" (3.1.1) | N/A: we have no paid random items. Keep the linter rule |
| **Apple ads** | Ads must fit the age rating, the user must be able to see the targeting info, and interstitials must be clearly marked as ads with no tricks (2.5.18). Apps "designed predominantly for the display of ads" are rejected (3.2.2) | Rewarded only; clearly labelled; no fake close buttons; ad-network creative filters set to our rating |
| **ATT / IDFA** | Explicit ATT permission is needed to track. Apps may not require tracking (or other permissions) to get functionality or rewards (5.1.2). An EU alternative ATT prompt arrives with iOS 27.2 (Apple News, Sep 2026) | **Launch with no ATT prompt and no IDFA.** Use contextual/non-personalized rewarded ads and AdAttributionKit for attribution. Revisit only if ad revenue matters |
| **Apple age rating** | New tiers 4+/9+/13+/16+/18+. Infrequent cartoon/fantasy violence is **9+**; *frequent* is **13+**. Loot boxes force at least 9+, and **16+ in Australia**. New descriptors must be declared by Jan 12 2027 (Age rating reference; Apple News) | Target **9+**: stylized "dispelling" of shadows (no blood or death), with horror kept infrequent. Answer honestly; 13+ is acceptable if Apple judges the violence "frequent" |
| **Age assurance (US states)** | Texas SB 2420 is live for new Texas accounts (June 2026): parental consent for downloads, IAP and "significant changes". Utah and Louisiana laws are coming in 2026. Apple provides the Declared Age Range API + PermissionKit Significant Change API (Apple News) | Integrate the Declared Age Range API (iOS) and the **Play Age Signals API** (Android, global responses by Dec 11 2026). Write a "significant change" policy. Set age ratings per in-app product in Play Console for Texas (unverified) |
| **Play Age Signals terms** | Signals may be used **only** for age-appropriate experiences and legal compliance; never for ads, marketing, profiling or **analytics** (Android Age Signals page) | Age data must never be written to analytics |
| **Google Play Billing** | Billing Library **v8+** has been required for new apps and updates since Aug 31 2026 (extension to Nov 1 2026). v9 is current (developer.android.com) | Build on PBL 9 |
| **Google loot boxes** | Odds must be disclosed before purchase for paid random items (unverified, policy text not retrievable) | N/A by design |
| **Google Families** | If the target audience includes under-13s, Families policy applies and ads must come from Families Self-Certified SDKs (unverified) | Declare **13+** target audience; store art aimed at teens and adults (cozy, not toddler). Pick an ad SDK that is Families-certified anyway as a hedge |
| **IARC / PEGI** | PEGI (from June 2026): paid random items → PEGI 16; time- or quantity-limited offers → PEGI 12; NFTs → PEGI 18 (unverified) | **Target PEGI 7 / ESRB E10+ / USK 6** with the "In-game purchases" descriptor. Our "no timers, no random paid items" rules protect this rating |
| **Loot-box laws** | Brazil banned loot boxes for under-18s (Mar 2026). Belgium's 2018 gambling stance is still cited. The Netherlands' current status is unclear. UK ASA enforces loot-box disclosure in store listings (unverified) | N/A by design. Declare "no loot boxes" in store listings |
| **EU consumer law** | CPC Key Principles on virtual currencies (Mar 2025, soft law). DFA proposal (Nov 2026): ban on paid loot boxes and pay-to-win for minors, real-money price display (unverified; still a proposal) | No purchasable currency, no P2W, no pressure tactics. Ad-bonus caps keep any "pay-to-progress" claim against the Supporter Pack small; re-review when the DFA text settles |
| **GDPR / ePrivacy** | Consent is needed for non-essential processing and storage | Certified consent tool (CMP) in the EEA/UK before any ads SDK loads. First-party pseudonymous analytics with a random install ID. Privacy policy; data deletion request flow |
| **COPPA** | The amended rule has been fully enforceable since Apr 22 2026, including a written security programme (unverified) | Not child-directed. Use a neutral age screen if signals say under 13: non-personalized ads only and no data collection beyond what is essential. Keep a written data-security doc |
| **Accounts** | If accounts exist, in-app deletion is mandatory (Apple 5.1.1(v)) | **No accounts in v1.** Cloud save through Game Center / Play Games |
| **Commission** | Apple Small Business Program: 15% under $1M in proceeds | Enrol before launch |

## 4. LiveOps plan (AI-run)

**Cadence**

| Rhythm | Content | Producer |
|---|---|---|
| Weekly | "Moonrise Challenge": an existing level + 1–2 modifiers (fog, double-speed moths, limited towers), Amber reward, personal best | Agent from a modifier library; sim-validated |
| Monthly | 2–3 new levels or a Heroic remix + 3–5 cosmetics | Level-design agent + art agent; review agent |
| Quarterly | New world (10 levels, 1 tower or hero, 2 enemies, boss) + Chapter Pass (once 3 worlds exist) | Full team; **owner gate** |
| Seasonal | Long Night (Halloween), Solstice, Spring Thaw: themed levels + returning cosmetics | Calendar agent |

**Remote config architecture:** versioned JSON (economy tables, ad caps, event calendar, modifiers, A/B buckets). It is signed and hosted on static CDN storage, cached on the device, falls back to bundled defaults, and has kill switches per ad placement or event. Each player's A/B bucket comes from hashing their install ID. Rollout goes 5% → 25% → 100%.

**Automation tiers**

| Safe to automate fully | Automate + reviewer-agent sign-off | Human (owner) gate |
|---|---|---|
| Weekly challenge rotation from a vetted modifier pool | New levels (must pass the bot-sim win-rate band) | New IAP SKUs and prices |
| Daily KPI and anomaly reports; crash triage | Economy table changes within **±10%** | Economy changes beyond ±10% |
| Localization drafts; patch notes | Cosmetic releases; event calendar | Anything touching consent, age, ATT, privacy, data SDKs |
| Auto-**rollback** on tripwires (crash-free <99.5%, D1 −15%, ad fill errors) | Store text updates | Store rating questionnaires; new ad networks; launch/region changes |

**Fairness linter (runs in CI on every config/content PR)** fails the build on any of the following:
- a price on Amber or Glow;
- a timer or a stock count on any offer;
- a random reward attached to a purchase;
- a gameplay stat inside any SKU;
- ad caps above the limits in §2.3;
- an event cosmetic with no scheduled return date.

## 5. KPIs & analytics events (vertical slice)

**KPI targets** (internal goals, not industry benchmarks)

| KPI | Target |
|---|---|
| D1 / D7 / D30 retention | ≥40% / ≥15% / ≥6% |
| L1→L10 funnel completion | ≥35% of installs |
| Per-level first-attempt win rate | Within the §2.2 band |
| Avg. level duration | 3–6 min |
| Rewarded-ad opt-in (offers accepted ÷ offers shown) | ≥25% |
| Ads watched / DAU | 1.5–3 |
| Supporter Pack conversion | ≥1.5% of D7 retained players |
| IAP refund rate | <3% |
| Crash-free sessions | ≥99.5% |
| Store rating | ≥4.5 |

**Common parameters on every event:**
`ts, install_id` (random UUID, not the ad ID)`, session_id, app_version, config_version, ab_bucket, platform, os_version, device_tier, locale`.

| Event | Key params |
|---|---|
| `app_first_open` | `store, install_source` (store-provided only) |
| `session_start` / `session_end` | `session_no`, `duration_s` |
| `consent_update` | `analytics`, `ads_personalized`, `region`, `cmp_version` |
| `tutorial_step` | `step_id`, `skipped` |
| `level_start` | `level_id, world_id, attempt_no, difficulty, hero_id, research_state_hash, glow_start, modifiers` |
| `wave_end` | `level_id, wave_no, leaks, lives_left, glow_balance, towers_count` (sampled at 20%) |
| `tower_build` / `tower_upgrade` / `tower_sell` | `tower_id, tier, spot_id, wave_no, glow_delta` |
| `lantern_reveal` | `tower_id, wave_no, enemies_revealed` (validates the Light-vs-Dark hook) |
| `hero_ability_used` | `ability_id, wave_no` |
| `level_end` | `level_id, result` (win/lose/quit)`, stars, duration_s, waves_reached, lives_left, glow_unspent, leak_top_enemy_id, revive_used` |
| `currency_change` | `currency` (amber)`, delta, source_or_sink, balance_after` |
| `research_unlock` | `node_id, tier, cost, balance_after` |
| `ad_offer_shown` / `ad_offer_accepted` | `placement, level_id` |
| `ad_show_result` | `placement, network, result` (completed/skipped/failed)`, error_code, latency_ms` |
| `ad_reward_granted` | `placement, reward_type, amount, via` (ad/supporter) |
| `store_view` / `iap_item_view` | `entry_point`, `sku` |
| `iap_purchase` | `sku, result` (success/cancel/fail/pending)`, price_micros, currency_code, error_code` |
| `iap_restore` | `skus_restored` |
| `cosmetic_equip` | `item_id, slot` |
| `event_join` / `event_complete` | `event_id, modifier_ids, score` |
| `remote_config_applied` | `config_version, bucket, fallback_used` |
| `perf_sample` | `fps_p50, fps_p5, mem_mb, level_id` |
| `error` | `code, context` |

Age-signal data, IDFA/GAID and free text are never logged.

---

## Recommendations (decisive)
1. Launch as **Fair Free + Supporter**: rewarded-only ads, a $4.99 Supporter Pack, and direct-priced cosmetics. **No hard currency, no loot boxes, no energy, no timers.**
2. Lock the **two-currency economy** (Glow in-level, Amber Sap meta) with the §2.2 tables as v0 numbers. Tune them with headless bot sims before any human playtest.
3. Target the **Apple 9+ / PEGI 7 / ESRB E10+** ratings and a **13+ Play target audience**. Ship with **no ATT prompt** and contextual ads.
4. Integrate StoreKit 2, **PBL 9**, a CMP, the **Declared Age Range API** and the **Play Age Signals API** from the first build that contains IAP.
5. Build remote config, the fairness linter and auto-rollback **before** the first LiveOps content. Only human-gate prices, SKUs, privacy and age logic.

## Risks
| Risk | Mitigation |
|---|---|
| Rewarded-only, non-personalized ads earn little | Expected; the Supporter Pack and cosmetics carry revenue. Revisit personalized ads with ATT after soft launch if the data justifies it |
| Cosmetics sell poorly in a single-player TD | Make the Hollow Tree a visible "home" diorama; show skins in level-win moments; Chapter Pass later |
| Free campaign under-monetizes vs premium | The soft-launch A/B test of a "Full Hollow" unlock |
| The DFA could treat Supporter auto-bonuses as pay-to-progress for minors | Bonuses are capped at about 20%; can be switched off for minors through age signals; re-review once the DFA text is final |
| Cute owls → Play reclassifies the app as "appeals to children" | Store art and copy aimed at teens and adults; ad SDK is Families-certified as a hedge |
| Apple rates the violence "frequent" → 13+ | Acceptable; does not change the business model |
| Unverified legal claims (PEGI, DFA, Brazil, COPPA) | Re-verify against primary sources before soft launch (the hosts were blocked this session) |

## Open questions for the Owner
1. **Ads at all?** Are you comfortable with opt-in rewarded ads? The alternative is a no-ads free game monetized only by the Supporter Pack and cosmetics: simpler and cleaner, with lower revenue.
2. **Campaign gating:** should agents run the soft-launch test of a "$4.99 Full Hollow unlock" variant, or should the full campaign stay free as a studio principle?
3. **Kids:** confirm we will **not** pursue the Kids Category or a Families "designed for children" listing (recommended; it would forbid most of this monetization).

## Sources
**Retrieved this session (curl):**
- Apple App Review Guidelines (last updated Oct 16 2026): https://developer.apple.com/app-store/review/guidelines/
- Apple age ratings values & definitions: https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions
- Apple Developer News (Texas SB 2420, Declared Age Range, Australia 16+ for loot boxes, EU ATT prompt, Jan 2027 descriptors): https://developer.apple.com/news/
- Apple User Privacy & Data Use (ATT, AdAttributionKit): https://developer.apple.com/app-store/user-privacy-and-data-use/
- Apple Small Business Program: https://developer.apple.com/app-store/small-business-program/
- Google Play billing system (PBL v8 deadline): https://developer.android.com/google/play/billing
- Integrate Play Billing Library: https://developer.android.com/google/play/billing/integrate
- Play Age Signals overview & terms: https://developer.android.com/google/play/age-signals/overview

**Unverified (search-result summaries only; pages not retrievable through the proxy):**
- Sensor Tower ad monetization report: https://sensortower.com/blog/gaming-deep-dive-ad-monetization-report
- Deloitte 2025 mobile game advertising: https://www.deloitte.com/us/en/about/press-room/deloitte-improve-mobile-game-advertising.html
- Unity IAP guide (1–3% payer rate): https://unity.com/resources/in-app-purchases-guide
- Bloons TD 6 pricing: https://marlvel.ai/apps/bloons-td-6
- Google Play loot-box odds (2019): https://www.pocketgamer.biz/google-play-developers-must-now-disclose-loot-box-odds
- Families Self-Certified Ads SDK: https://support.google.com/googleplay/android-developer/answer/12918983
- Play Age Signals blog (Jul 2026): https://android-developers.googleblog.com/2026/07/google-play-age-signals-api-safer-experiences.html
- PEGI 2026 criteria: https://www.osborneclarke.com/insights/games-loot-boxes-get-16-plus-age-rating-europe-under-pegi-overhaul and https://www.lewissilkin.com/insights/2026/03/18/pegi-announces-major-update-to-age-rating-criteria-what-games-businesses-need-to-102mn9y
- EU CPC virtual currency principles: https://www.reedsmith.com/articles/qas-on-the-eu-consumer-protection-authorities-joint-guidance-paper/
- EU Digital Fairness Act proposal: https://www.pinsentmasons.com/out-law/analysis/digital-fairness-act-proposal-puts-video-game-monetisation-models-in-focus
- Brazil loot-box ban: https://www.pocketgamer.biz/brazil-bans-loot-boxes-for-under-18s-in-online-child-safety-measure
- UK ASA loot-box notice: https://www.asa.org.uk/resource/enforcement-notice-disclosure-of-loot-boxes-in-app-stores.html
- COPPA amended rule: https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule
