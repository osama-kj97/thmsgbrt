# 01 — Market & Competitor Analysis: Mobile Tower Defense (Market Analyst)

> Date: 2026-11-23. Status: v1 for Lead review.
> **Method caveat:** This session could not open web pages. Direct fetches to sensortower.com, gamedeveloper.com and play.google.com were blocked by the network policy. Every figure below comes from **search-result excerpts seen this session**, not from full pages I read. All numbers are third-party estimates and should be treated as directional. Each one carries the date of its data.

---

## TL;DR

1. **TD money sits in hybrids, not in pure lane TD.** The biggest earners blend TD with gacha (Arknights, ~$1B lifetime), cards and PvP (Rush Royale, $500M+ and 105M+ downloads, Jun 2026), luck or co-op merge (Lucky Defense, $45M+ in Korea alone, 2024), roguelite (Wittle Defender, ~$10M in its first month, 2025) or idle (The Tower, ~$65M lifetime). Classic premium lane TD (Kingdom Rush, Bloons TD6) lasts for years but is a niche whose owner says it is "less viable each year".
2. **Players reward fairness and punish four things:** paid towers, energy timers, paywalled speed-up, and late-game difficulty walls that push spending. "No energy, no pay-to-win, optional ad removal" is itself a selling point in reviews.
3. **The benchmarks are harsh.** The median mobile game reaches D1 ~22%, D7 ~4% and D30 <1% (GameAnalytics, 2025 data). The strategy genre averages ~25% D1, 8% D7 and 3% D30. US strategy CPI runs ~$4–18. Paid UA is out of reach for us at launch, so the plan must be **organic-first** (store featuring, community, creators).
4. **The Light-vs-Dark mechanic is not fresh, but the owl theme is.** "A lantern tower reveals and weakens hidden shadow enemies" already exists. Glowkeep (a browser/CrazyGames app, pre-release Oct 2026) has a lantern tower that alone reveals "shades", a "Flare" spell and a "Gloom King". Several jam games and older titles (Shad'O, 2012) do the same. No scaled mobile title owns this mechanic, and I found no owl-themed mobile TD. **Keep the theme. Rebuild the mechanic** so light is territory and build-space, not a stealth-reveal tag.
5. **Portrait one-thumb is mainstream and right for our audience,** but it costs strategic density. Most of the top hybrid TDs are portrait, and PvZ 3 moved to portrait "for one hand". The crunchy-strategy players (Kingdom Rush, BTD6) play landscape. Portrait therefore needs vertical maps designed for it, not a squeezed landscape map.

---

## 1. State of the mobile TD market (late 2026)

### Sub-genre map

| Sub-genre | Reference titles (data date) | Commercial signal | Trend | Fit for a small studio |
|---|---|---|---|---|
| **Classic lane TD (premium or premium-ish)** | Kingdom Rush series. KR6: Genesis launched 24 Sep 2026 at $6.99 mobile and added a "Classic Mode" after fan feedback. Bloons TD 6 earns ~$100–147K/week in the US alone (Q2 2025). | Durable and loved, with the best critic scores in the genre. Ironhide's co-founder says premium is "becoming less viable each year". KR5 was criticised for its IAP. | Stable, mature niche | **High creative fit, low revenue ceiling.** This is our genre core. |
| **Hero/RPG TD with gacha** | Arknights (~$1B lifetime mobile, Jul 2026; 62% Japan; ~$40 revenue per download in Naavik's 2023 analysis) | Dominant revenue per user | Mature, China/Japan-led | Low: needs a large content and liveops budget, and gacha conflicts with our fair-F2P promise |
| **Merge/card PvP TD** | Rush Royale ($500M+ and 105M+ DL, Jun 2026), Random Dice (111%) | Very large, but concentrated in incumbents | **Saturated** (many clones) | Low: PvP needs servers, balance and liquidity |
| **Luck/co-op merge TD** | Lucky Defense (111%): $45M+ in Korea by Oct 2024 and still #1 grossing in Korea 6 months after launch. 111%'s parent grew H1 2025 revenue 38%. | Strong, Asia-centric | Growing (in Korea) | Low or medium: online co-op |
| **Roguelite / hybridcasual TD** | Wittle Defender (Habby, Jun 2025): ~$10M gross in about a month and ~3M installs, mostly in China, Taiwan and the US. Plus many 2026 entrants (Evo Defense, Wall Brawl). | Hybridcasual was "the standout monetization gainer" of 2025 (Sensor Tower). A market report names roguelike TD the fastest-growing TD sub-genre. | **Growing** | Medium: ad-driven UA economics favour big publishers, but **roguelite run structure is cheap, data-driven replayability** we can borrow |
| **Idle TD** | The Tower (Tech Tree Games): ~$65M lifetime, **4 full-time staff**, est. $700–800K/month, 5M+ Android installs, revenue rising in 2025 with little UA | Exceptional for a tiny team | Growing or stable | **High: the best small-team analog** |
| **TD as 4X ad bait** | Kingshot (Century Games): #7 worldwide by IAP revenue in Dec 2025, ~$32M US ad spend in Q3 2025, ~1,500+ ad creatives per day, with TD-style ad footage | Strategy was "the only mobile category to gain across revenue, downloads and time spent" in 2025 | Growing | **This is a threat.** 4X giants buy "TD-intent" users at prices we cannot match. |

**Market size:** Analyst forecasts disagree. One puts global mobile TD at $3.08B in 2025 and another at $4.75B. Neither is traceable to Sensor Tower or AppMagic data, so treat both as noise. The whole mobile games market grew ~1% YoY to ~$82B in 2025 (Sensor Tower, State of Gaming 2026).

**Analysis:**
- **Growing:** roguelite and hybridcasual TD, idle TD, strategy as a whole, and TD mechanics embedded in 4X.
- **Saturated:** merge/card PvP TD and generic F2P "Kingdom-Rush-likes" with heavy IAP. US weekly grossing for mid-tier F2P TDs (Raid Rush, Kingdom Guard, Galaxy Defense) is only ~$85–530K/week, which leaves the long tail very thin.
- **Our lane:** a premium-quality lane TD with modern F2P fairness and a roguelite or daily replay layer. That spot sits between Kingdom Rush (quality, but IAP backlash) and The Tower (fair, long-tail, small team).

---

## 2. What players love and hate

Sources here are store-review aggregators, critic reviews and editorial roundups. **No Reddit threads were surfaced by search,** so this is not a Reddit consensus.

| Topic | Loved | Hated (evidence) | Design implication |
|---|---|---|---|
| **Monetization** | Paying once for ad-free play is seen as "reasonable and ethical" (Sky TD). The Infinitode 2 model (free with optional ads, plus a $2.99 premium unlock) is cited as offline-friendly. | Paying for towers ("towers behind a separate paywall is a strange and worrying move", PocketGamer). KR5 was "ruined by very expensive microtransactions". "Watching a million ads should exempt me from pay to win" (Allies TD). | Never sell towers or power. Sell cosmetics plus a one-time "Supporter" unlock. |
| **Energy systems** | Games with no energy cap are called out positively. | "Ran out of energy after a few battles, watch ads or wait" (Tower Conquest). Energy combined with a paywalled 3× speed frustrates players (Tower King). | **No energy.** Free 2× speed. |
| **Ads** | Rewarded ads that are opt-in and fair. Unity finds "resource-depleted" moments drive the highest opt-in (38.1%). | Forced or random interstitials (Mega Tower). Excessive ads (Raid Rush). Games that start ad-free and later get "overrun with ads" (TD King). | Rewarded only: retry, double reward, revive. No interstitials. |
| **Difficulty / pacing** | Higher difficulty tiers add longevity (KR5). Finding hero combos per map is "exceptionally fun" (GamingTrend). | An "insane difficulty spike later on" (KR Frontiers). Hard modes that "tempt players into dropping cash" (KR5 critic). Progress becomes "a slog" without spending (Escapist). | Difficulty via optional modifiers (stars, challenge modes), never a gate that implies spending |
| **Content and depth** | Large, offline-playable content (BTD6 is "bottomless" and plays fully offline). | Too few levels for the price (KR5). Shallow upgrade systems (GamingTrend on KR5). No endless mode or extra modes (PvZ3 soft-launch feedback). | Ship endless or daily modes early. Give tower upgrade paths a real choice. |
| **Offline** | Offline play is a frequent "best of" criterion in roundups | Online-only F2P | Offline-first: this also suits our headless, data-driven stack. |
| **Orientation** | Portrait for one-handed play on transit, landscape on the couch (Game Accessibility Guidelines) | No hard data for TD specifically | See §4 |

---

## 3. Benchmarks

| Metric | Value | Scope and date | Confidence |
|---|---|---|---|
| D1 / D7 / D30 (median game) | ~22% / ~4% / ~0.7–0.8% | GameAnalytics, 2025 data (2026 report). Retention declined again in 2025. | Medium-high |
| D1 / D7 (top 10%) | ~40% / ~12% | Same | Medium-high |
| D1 / D7 / D30, strategy genre | 25.4% / 8.1% / 3.1% | Mistplay data via Segwise blog, date unclear | Low |
| D1 / D7 / D30, marketed titles avg → top tier | 25–30 / 10–15 / 3–6% → 45+ / 25+ / 12+% | AppFollow (vendor), 2026 | Low-medium |
| TD playtime | "Almost double" platformer and idle playtime. GameAnalytics treats D7 as the key TD stat. | GameAnalytics TD article (undated). The full TD snapshot (May 2025) is gated. | Medium (qualitative) |
| Session length | Hybridcasual ~21.6 min/session (Adjust, 2025). Another playbook gives ~6.2 min (2020–22 data). | Conflicting definitions | Low |
| CPI, US strategy | iOS ~$18.45, Android ~$11.17 (AppsFlyer, Q3 2026). Alternatively ~$5.50 iOS / $4.00 Android (Business of Apps via FoxData). Midcore: iOS $3.86, Android $0.73 (Liftoff 2025). | Mixed channels and definitions | Low-medium |
| ROAS | Strategy D30 ROAS: 60% iOS vs 27% Android | 2025–26, vendor summary | Low |
| ARPDAU | Hybridcasual (ads + IAP) $0.15–0.50. Casual $0.10–0.30. | Vendor blogs, 2025–26 | Low |
| Revenue per download (top end) | Arknights ~$40 RPD, ~4× the next TD | Naavik, 2018–22 data | Medium |

**Soft-launch targets I recommend (stretch but credible for a polished lane TD):** D1 ≥ 40%, D7 ≥ 15%, D30 ≥ 5%, 2+ sessions per day at 6–12 min, ARPDAU $0.08–0.20. At US strategy CPIs, LTV will not cover paid UA early, so **budget for organic and featuring, not UA**.

---

## 4. Differentiation: hook and portrait evaluation

### 4a. "Light vs Dark (owls + lantern vision vs shadow creatures)": freshness check

| Existing title | Platform / status | Overlap with our hook |
|---|---|---|
| **Glowkeep** | CrazyGames browser game with a CrazyGames app (iOS/Android). Pre-release Oct 2026, 7.3 rating from a handful of votes. | **Very high.** Night setting. The LANTERN tower slows foes and is "the only thing that reveals SHADES", upgrading to Beacon or Sunflare. A FLARE spell lights an area and reveals shades. Boss is the "Gloom King". Has Endless mode and a Daily Siege. |
| **Lantern Watch** | Google Play listing seen via a mirror (apkcombo), latest version Oct 2026. **Unverified:** a direct search did not confirm it. | High. Towers don't shoot, tiles have light levels, and anything in the dark can't be harmed. 15 nights. |
| **Shad'O** | 2012 | Fog covers the map and you expand from light beacons |
| **Interstellar Defenders** | itch.io | Enemies are hidden until they enter a tower's light. Beacons push the darkness back. |
| Radiating Tower, Night Watch (×2), Of Shadow and Light, LanternKeep, Darkest Defense | itch.io / jam games | Spotlight or flashlight reveal mechanics. A recurring jam theme. |
| Underdark: Defense; Nighty Knight; Nightfall: Kingdom Frontier TD | iOS/Android | Night or dark *setting*, but light is not the core mechanic |
| Birds Camp (iOS); Owlet, TOwls vs. Demons (PC/itch) | — | Birds or owls as defenders. **No scaled owl-themed mobile TD found.** |

**Verdict:**
- **The theme (owls, Hollow Tree, caramel sap, cozy night) is fresh and ownable.** Owls are under-used in TD, and "cozy look, crunchy strategy" is an unoccupied store position. Cozy is a growing tag: "cozy" in Steam descriptions rose from 0.4% (2022) to 3.1% (2025).
- **The mechanic as written ("lantern towers reveal & weaken shadows") is not fresh.** It is a known jam trope and very close to Glowkeep in particular. **Hard constraint #1 risk:** avoid the terms "Shade", "Gloom King", "Flare", "Beacon" and "Sunflare" and a lantern tower that "reveals" with the same 2-branch shape.
- **Reframe proposal:** make light **territory and economy**, not stealth detection.
  - Darkness creeps forward each wave.
  - Towers can only be built and powered inside lit ground.
  - Lanterns cost upkeep in sap.
  - Shadow creatures *extinguish* light, which shrinks your build space mid-wave.
  - Owl heroes are the exception: they act in darkness (night vision), so they become the counterplay to darkness, not just stat carriers.

  The result is a spatial resource tension that fits portrait and one thumb (you place light on a vertical map). It is distinct from "reveal invisible units", and it is a strong, legible ad and screenshot visual: a lit path against encroaching dark.

### 4b. Portrait one-thumb

| For | Against |
|---|---|
| The most successful modern TD hybrids are portrait. This is my observation from the store listings of Rush Royale, Random Dice, Lucky Defense, The Tower and Wittle Defender; it is not a sourced statistic. | Kingdom Rush and BTD6, the reference "crunchy strategy" titles, are landscape. Their fans are our mid-core core. |
| PvZ 3 switched to portrait explicitly "to more easily play with one hand" | PvZ 3 was pulled from soft launch twice and criticised as thin. Portrait was not the reason given, but it shows portrait lane TD is not a guaranteed win. |
| Fits the commute and short-session use case (3–6 min levels) | Less horizontal space limits the number of paths, build spots and readability of long maps |
| Easier store screenshots and short-form vertical video for organic marketing | Tablet players expect landscape. Accessibility guidance recommends supporting both. |

**Verdict: keep portrait one-thumb.** Design maps vertically from the start: enemies flow top to bottom, 1–2 lanes, 6–10 build spots, with build and upgrade menus in the bottom thumb zone. Do not port landscape-style layouts. Treat tablet landscape as post-launch.

---

## 5. Small and indie TD case studies

| Case | Team | Result (date) | Lesson for us |
|---|---|---|---|
| **The Tower – Idle TD** (Tech Tree Games, US) | ~4 full-time staff plus contractors | ~$65M lifetime. Est. $700–800K/month. Revenue rising in 2025 with little UA. | Deep, fair, numbers-driven progression plus community leads to a long tail without UA. **Closest analog to our AI-run, data-driven model.** |
| **Ironhide / Kingdom Rush** (Uruguay) | Small-to-mid indie | 30M+ copies sold across titles. KR6 launched Sep 2026 at $6.99. | Craft and charm win critics and loyalty. But premium is getting harder, and adding IAP to premium caused backlash (KR5). |
| **Infinitode 2** | Solo/indie | Free with optional ads, $2.99 premium unlock. Recommended in 2026 "best TD" lists. | The fair hybrid model is credible to players |
| **Mindustry** (Anuke) | Solo, open source | Recurrent in "best offline TD" lists. No ads, no IAP. | Depth and systemic play earn organic word of mouth |
| **Tangy TD** (Cakez), PC | Solo | ~$200–250K in week 1 (Mar 2026), ~10K wishlists before launch | Creator- and streamer-driven launches work in TD (PC evidence) |
| **Core Defense**, PC | Solo | $67K gross in year 1 | A realistic indie baseline. Most indies sell modestly. |
| **Wittle Defender** (Habby) | Large publisher | ~$10M in its first month (2025), heavy pre-launch ad spend | Roguelite TD works, but at the top end it is a UA game. Borrow its structure, not its go-to-market. |

---

## Recommendations (decisive)

1. **Positioning:** "Cozy night-time lane TD with a fair deal." Use it in store copy, verbatim in spirit: *no energy, no paid towers, free speed-up, plays offline.*
2. **Mechanic:** Replace "lantern reveals and weakens" with **"light is your territory"** (creeping darkness, buildable lit ground, enemies that extinguish light, owls that fight in the dark). The Game Designer should prototype this first. It is the make-or-break differentiator.
3. **Replay layer from vertical slice onward:** add a daily seeded "Night Watch" challenge plus roguelite run modifiers (pick 1 of 3 blessings between waves). It is cheap to build data-driven and addresses the "no endless mode" complaint. It is also the main lever for D7 and D30.
4. **Monetization guardrails** (input to the Economy Designer):
   - Rewarded ads only, at resource-depleted moments (retry, revive, double sap).
   - No interstitials.
   - A one-time Supporter unlock (removes ads, cosmetic bonus) plus cosmetics.
   - The premium pass is optional and cosmetic or convenience only.
   - Never sell towers, heroes' power or speed.
5. **Portrait:** keep it. Make all maps vertical-native. Do not plan landscape before launch.
6. **Go-to-market:** organic first. Target editorial featuring (Apple and Google like fair, crafted games), vertical short-video content of the light-vs-dark visual, and TD creators. Don't plan around paid UA at $4–18 US CPIs.
7. **Avoid:** PvP, gacha, merge-PvP, and online-required co-op. These sub-genres are saturated, server-heavy, or both.

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| The light mechanic reads as derivative of Glowkeep and jam games | High | Use the territory reframe and distinct naming, and review against Glowkeep before the concept gate |
| Classic lane TD has a low monetization ceiling under fair F2P | High | Set expectations: a sustainable long tail (The Tower path), not a hit. Track ARPDAU in soft launch. |
| 4X games (Kingshot and others) inflate CPI for TD-intent users | Medium | Organic and featuring strategy. ASO on "cozy", "owl" and "offline TD" rather than generic "tower defense". |
| Portrait limits the strategic depth that mid-core players expect | Medium | Vertical map design rules. Depth comes from tower upgrade choices and modifiers, not map width. |
| Benchmark data is weak (vendor blogs, fetch blocked this session) | Medium | Re-validate with GameAnalytics TD snapshot and AppMagic once network access allows |
| "Cozy" audiences monetize ~27% below strategy/RPG (market research, unverified) | Low-medium | Keep the strategy crunch as the retention driver. Cozy is the wrapper. |

## Open questions for the Owner

1. **Success definition:** is the goal a sustainable small-revenue game grown organically (The Tower / Infinitode path, no paid UA), or a game designed to scale with paid UA? This changes monetization, scope and genre choices.
2. **Hook pivot:** do you approve reframing "lanterns reveal shadows" into "light is territory" (creeping darkness, build only in light), given that a near-identical lantern-reveal TD (Glowkeep) appeared in Oct 2026?

## Sources

**All sources below were seen as search results this session. Page bodies could not be fetched because the network policy blocked page retrieval, so the figures are unverified excerpts.**

- https://www.pocketgamer.biz/rush-royale-surpasses-500m-in-lifetime-revenue/ (unverified)
- https://about.my.games/news/567 (unverified)
- https://www.pocketgamer.biz/rush-royale-surpasses-100m-downloads-and-over-470m-in-lifetime-revenue (unverified)
- https://sensortower.com/blog/2025-q4-ios-top-5-tower-defense-games-revenue-us-6012932d241bc16eb85e0db8 (unverified)
- https://sensortower.com/blog/2025-q2-unified-top-5-tower%20defense%20games-revenue-us-6012932d241bc16eb85e0db8 (unverified)
- https://sensortower.com/blog/2025-q1-unified-top-5-tower%20defense%20games-revenue-us-6012932d241bc16eb85e0db8 (unverified)
- https://sensortower.com/blog/2025-q2-unified-top-5-paid%20games-revenue-us-61f43af0afb48b4f71b2ba3f (unverified)
- https://sensortower.com/blog/state-of-mobile-games-in-korea-2024 (unverified)
- https://www.invenglobal.com/articles/24501/superfast-reports-h1-revenue-of-1065-billion-up-38-yoy (unverified)
- https://www.marketresearch.com/Diligence-Insights-v4290/Mobile-Tower-Defense-Games-Size-41621882 (unverified)
- https://www.globenewswire.com/news-release/2025/11/04/3180032/0/en/Mobile-Tower-Defense-Games-Market-to-Reach-USD-9-74-Billion-by-2033-Driven-by-Rising-Smartphone-Penetration-and-5G-Expansion-Research-by-SNS-Insider.html (unverified)
- https://respawn.outlookindia.com/gaming/gaming-news/mobile-games-82-billion-revenue-2025-sensor-tower-report (unverified)
- https://www.globalgamesforum.com/news/state-of-gaming-heres-what-the-mobile-data-actually-says (unverified)
- https://investgame.net/wp-content/uploads/2026/02/2026-02-26-sensor_tower__state_of_mobile_2026__en_wp.pdf (unverified)
- https://socialpeta.com/en/blog/with-2000-ai-creatives-daily-century-games-kingshot-dominates-mobile-charts-in-the-us-japan-and-korea-in-june (unverified)
- https://www.gamigion.com/4x/ (unverified)
- https://dataintelo.com/report/mobile-tower-defense-game-market (unverified)
- https://www.pocketgamer.biz/wittle-defender-hits-10m-in-player-spending (unverified)
- https://segwise.ai/blog/wittle-defender-creative-analysis-habby-mobile-game-strategy (unverified)
- https://www.deconstructoroffun.com/blog/2025/7/31/habbys-hybridcasual-empire-the-template-that-built-a-powerhouse (unverified)
- https://naavik.co/deep-dives/arknights-tower-defense-redefined/ (unverified)
- https://www.pocketgamer.biz/arknights-endfield-surpasses-125m-in-six-months-on-mobile/ (unverified)
- https://adapty.io/paywall-library/the-tower/ (unverified)
- https://sensortower.com/blog/2025-q1-android-top-5-idler%20games-revenue-us-602ae7fb241bc16eb874f8e1 (unverified)
- https://www.baijing.cn/article/54549 (unverified)
- https://www.appbrain.com/dev/Tech+Tree+Games/ (unverified)
- https://gameanalytics.com/blog/metrics-behind-successful-tower-defense-games/ (unverified)
- https://gameanalytics.com/reports/sub-genre-snapshot-tower-defense-games/ (unverified)
- https://www.pocketgamer.biz/ironhide-co-founder-pablo-realini-talks-kingdom-rush-5-and-premiums-place-in-2024 (unverified)
- https://www.benzinga.com/topic/level-uy-2022 (unverified)
- https://www.gamedeveloper.com/press-release/ironhide-celebrates-15-years-of-kingdom-rush-with-the-introduction-of-classic-mode-in-kingdom-rush-6-genesis (unverified)
- https://www.gamedeveloper.com/press-release/ironhide-announces-kingdom-rush-6-genesis-td-steam-demo-mobile-pre-orders-new-trailer-and-september-24-launch-date (unverified)
- https://www.pocketgamer.com/kingdom-rush-5-alliance/review (unverified)
- https://gamingtrend.com/feature/reviews/kingdom-rush-5-alliance-td-review-lacking-depth-where-it-matters (unverified)
- https://gamebrain.co/game/kingdom-rush-5-alliance-td (unverified)
- https://www.pocketgamer.com/kingdom-rush-vengeance/app-army-assembles-is-kingdom-rush-vengeance-another-classic-tower-defence/ (unverified)
- https://gamebrain.co/game/tower-conquest-tower-defense (unverified)
- https://gamebrain.co/game/mega-tower-casual-td-game-1 (unverified)
- https://gamebrain.co/game/sky-td-hardcore-tower-defense (unverified)
- https://gamebrain.co/game/allies-td-tower-defense-games (unverified)
- https://gamebrain.co/game/tower-defense-king (unverified)
- https://gamebrain.co/game/raid-rush-tower-defense-td (unverified)
- https://escapistmagazine.com/?p=28891 (unverified)
- https://vgtimes.com/top-and-the-best/168597-best-tower-defense-games-mobile.html (unverified)
- https://www.pocketgamer.com/android/best-tower-defence-games-android/ (unverified)
- https://en.wikipedia.org/wiki/Bloons_TD_6 (unverified)
- https://investgame.net/wp-content/uploads/2026/01/2026-01-27-2026-mobile-pc-benchmarks_compressed.pdf (unverified)
- https://gamedevreports.substack.com/p/gameanalytics-mobile-and-pc-game (unverified)
- https://segwise.ai/blog/mobile-gaming-app-user-retention-strategies (unverified)
- https://appfollow.io/blog/mobile-game-retention (unverified)
- https://www.appsflyer.com/?p=549948 (unverified)
- https://foxdata.com/en/blogs/2026-mobile-game-user-acquisition-cost-benchmarks-how-much-should-you-spend/ (unverified)
- https://blog.playio.co/arpdau-benchmarks-mobile-games (unverified)
- https://gamedevreports.substack.com/p/adjust-mobile-games-insights-report (unverified)
- https://dataconomy.com/2025/11/25/how-rewarded-advertising-became-a-core-growth-engine-for-mobile-games (unverified)
- https://unity.com/blog/rewarded-ad-systems (unverified)
- https://www.crazygames.com/game/glowkeep-ydr (unverified)
- https://apkcombo.com/id/lantern-watch/com.lantern_watch/ (unverified; existence not confirmed by a second search)
- https://destructoid.com/reviews/review-shado (unverified)
- https://markcooperdev.itch.io/interstellardefenders (unverified)
- https://philxd.itch.io/radiating-tower (unverified)
- https://justdezt.itch.io/nightwatch (unverified)
- https://lgwv.itch.io/of-shadow-and-light (unverified)
- https://www.pocketgamer.com/underdark-defense/out-now (unverified)
- https://apps.apple.com/us/app/-/id1660736608 (Birds Camp; unverified)
- https://buas.itch.io/owlet (unverified)
- https://darkplace.itch.io/towls-vs-demons (unverified)
- https://kotaku.com/popcap-soft-launches-plants-vs-zombies-3-1841951761 (unverified)
- https://www.pocketgamer.com/plants-vs-zombies-3/pulled-from-soft-launch-again (unverified)
- https://gameaccessibilityguidelines.com/allow-play-in-both-landscape-and-portrait/ (unverified)
- https://www.pocketgamer.biz/how-portrait-mode-trumped-tablet-first-gaming (unverified)
- https://newsletter.gamediscover.co/p/case-study-making-core-defense-a (unverified)
- https://www.indie-games.eu/indie-tower-defense-tangy-td-earns-250k-in-a-week/ (unverified)
- https://www.intelmarketresearch.com/online-cozy-game-market-6937 (unverified)
- https://www.kocca.kr/global/2026_3+4/sub03_06.html (unverified)
