# 04 — Technical Architect: Engine, Stack & Pipeline

*Author: Technical Architect · Date: 2026-11-23 · Status: recommendation for the concept gate*

## TL;DR
1. **Engine: Godot 4.7.x (pinned to 4.7.2-stable), with GDScript, the Compatibility (GLES3) renderer, and MIT licensing (no fees).** I downloaded it into this Linux container and ran a deterministic 200-entity × 6,000-tick headless simulation in under 0.5 s. I also captured a rendered PNG under Xvfb with software OpenGL, so the "no GUI" rule holds in practice.
2. **Runner-up: Phaser 4 + TypeScript + Capacitor 8.** It is the most LLM-friendly option and its tests are easy to write. It loses because rendering inside a WebView is risky for our *Light vs. Dark* hook (dynamic light, fog and particles) on low-end Android. Defold 1.14 is a close third. Unity 6 and Cocos Creator are rejected.
3. **Architecture:** the simulation is a **pure GDScript core** with no Nodes, a fixed 30 Hz tick, integer/fixed-point math and seeded RNG streams. All content is **JSON validated by JSON Schema**. Replays are `seed + content hash + input log`, so every balance claim can be reproduced.
4. **Testing has 4 layers:** lint/schema checks, then GUT unit tests, then golden replays plus headless balance bots (Monte Carlo across strategies), then screenshot regression under Xvfb. All of it runs on `ubuntu` runners. Only iOS signing and upload need macOS (`macos-26`, Xcode 26).
5. **The Owner has to do things that only a legal person can:** Apple ($99/yr) and Google Play accounts, banking and tax, AdMob payments, a domain with a privacy policy, custody of signing keys, and approving releases through a GitHub "Environment" approval button. I list everything below.

---

## 1. Findings: engine comparison

### Current versions & licensing (checked 2026-11-23)
| Option | Current version found | License / fees | Evidence |
|---|---|---|---|
| **Godot** | 4.7.2-stable (master branch is 4.8-beta). Android template targets SDK 36, min SDK 24 | MIT, no royalties | Binary downloaded & run; `version.py`; `config.gradle` |
| **Unity 6** | 6.3 LTS (Dec 2025); later 6.x streams exist | Personal is free under $200k revenue+funding; Pro is **$2,310/seat/yr** above that; Runtime Fee cancelled | search results (unity.com) |
| **Defold** | 1.14.1 stable (1.14.2 in dev) | Defold License (Apache-2-derived), free | `VERSION`, `LICENSE.txt` in repo |
| **Phaser + Capacitor** | phaser 4.2.1, @capacitor/core 8.6.2 | MIT / MIT | npm registry |
| **Cocos Creator** | engine 3.8.8 (3.9 in dev) | Free; custom engine license | repo `package.json` |
| *Also considered* | Flutter+Flame, Solar2D, MonoGame, Bevy | — | Excluded: weaker ad/IAP ecosystems or immature mobile toolchains for our scope (judgment) |

### Scored matrix (1–5; weighted)
| Criterion (weight) | Godot 4.7 | Phaser 4 + Capacitor | Defold 1.14 | Unity 6.3 | Cocos 3.8 |
|---|---|---|---|---|---|
| **AI-agent friendliness** (20): text sources, LLM knowledge, CLI | 4: `.gd`/`.tscn`/`.tres` are plain text and the CLI is complete; LLMs sometimes mix up Godot 3 and 4 APIs | 4.5: TypeScript is the language LLMs know best, but Phaser 4 is new and gets confused with v3 | 3: text formats and Lua, but much less training data | 3: C# is well known, but scenes are GUID-heavy YAML and the editor is central | 3: TypeScript, but the editor-centric scene JSON is fragile |
| **Headless testing** (15) | 4.5: *verified here*, `--headless --script` and Xvfb screenshots; GUT and gdUnit4 for tests | 5: Vitest, plus Playwright for headless Chrome | 3: headless engine exists; thin tooling | 3: batchmode tests need license activation and ~10 GB images | 3 |
| **Mobile 2D performance & FX** (20): 100+ entities, particles, lights | 5: native, Light2D/occluders and GPU/CPU particles built in | 3: WebGL inside a WebView, which varies across low-end Android devices | 5: very lean native runtime | 5 | 4 |
| **CI export iOS/Android** (15) | 4: Android AAB builds headless on Linux (keystore via env vars); iOS needs macOS + Xcode | 4: Gradle on Linux; iOS on macOS | 4: `bob.jar` CLI | 3: license activation, slow and large builds | 3 |
| **License/fees** (5) | 5 | 5 | 5 | 3 | 4 |
| **Ads/IAP/analytics SDKs** (10) | 3: AdMob (Poing, 4.5+, UMP, mediation), official Android billing, community StoreKit 2 plugin, official Sentry and GameAnalytics SDKs; Firebase only via community | 4: AdMob, RevenueCat and Firebase plugins all on npm | 4: official extensions | 5 | 4 |
| **App size** (5) | 3: ~25–40 MB baseline (est., unverified) | 4 | 5: few-MB runtime (unverified) | 3 | 4 |
| **Live content/hot update** (10) | 4: runtime-loaded JSON and PCK resource packs | 4: data live; JS code-push conflicts with App Store 2.5.2 | 5: built-in Live Update | 4: Addressables | 5 |
| **Weighted total** | **4.18** | 4.10 | 4.05 | 3.70 | 3.60 |

### Why Godot wins when the scores are this close
- **It fits the core hook.** *Light vs. Dark* needs dynamic 2D lights, occluders, fog-of-war shaders and particles on top of 100–300 entities. Godot provides these natively. In Phaser we would build them ourselves on WebView WebGL, and that is the hardest kind of problem to fix late.
- **Its risks show up early in CI.** Godot's main weakness is that LLMs write outdated APIs, which fails right away in CI: `godot --check-only`, `gdlint`, and `--doctool` to dump the exact 4.7 API reference into the repo for agents. Phaser's main weakness is low-end device performance, which only shows up on real phones, late.
- **One runtime for everything.** The same binary runs the game, the headless sim, balance bots, screenshot tests, store screenshots and a **web build** the Owner can play from a link at every gate.
- **No licensing exposure.** MIT means no seat fees, no revenue thresholds, and no closed source we can't patch.

**Defold** is a credible alternative: the smallest builds and built-in Live Update. It is held back by thin LLM knowledge of Defold and Lua, which matters most when agents write 100% of the code. **Unity** costs too much in agent friction: binary-ish assets, license activation in CI, and heavy images.

**Switch trigger:** if the Week-1 spike (below) misses its performance gate on a low-end Android device even after optimization, **or** agents spend more than 20% of their time on Godot API hallucinations over the first two sprints, re-evaluate against Phaser 4.

---

## 2. Recommendations (decisive)

### 2.1 Stack decision
| Layer | Choice |
|---|---|
| Engine | **Godot 4.7.2-stable**, pinned in `.godot-version`. Upgrade only by a deliberate PR that passes golden replays |
| Language | **GDScript, statically typed** (`:=`, typed arrays; warnings as errors). No C#: it would add a .NET build step and more platform caveats for no gain at our scale |
| Renderer | **Compatibility (GLES3)**: widest low-end Android coverage, it also drives the web build, and it matches the Xvfb software-GL CI renderer |
| Lint/format | `gdtoolkit` 4.5.0 (gdlint/gdformat), `godot --check-only`, `check-jsonschema` |
| Tests | **GUT 9.x** (has a CLI) for unit and sim tests; custom headless runners for balance and screenshots |
| Ads | AdMob via **Poing Studios godot-admob-plugin** (Godot 4.5+, rewarded, UMP consent, mediation) |
| IAP | Android: **official GodotGooglePlayBilling**. iOS: **godot-iap** (OpenIAP, StoreKit 2; the repo has just moved into the OpenIAP monorepo, so pin a commit). Everything sits behind one `Store` interface |
| Crash/errors | **Sentry for Godot** (official; Android and iOS; SDK 1.x/2.x needs Godot 4.5+) |
| Analytics | **GameAnalytics Godot SDK** (official, Godot 4.5+, free): progression, resource source/sink and ad events |
| Remote config / live content | Signed, versioned **static JSON on a CDN** (Cloudflare R2/Pages or GitHub Pages), with a bundled fallback (§2.6) |

### 2.2 Architecture
```
 content/*.json ──(schema-validated, hashed)──► ContentDB
                                                  │
 Input (taps) ─► Command{tick, type, args} ─► SIM CORE (pure GDScript, no Nodes)
                                                  │  fixed 30 Hz tick, int/fixed-point
                                                  ▼
                                    SimState (arrays) ──► Events (spawned, hit, died, sap+)
                                                  │                    │
                       Presentation (Nodes/.tscn) reads state,   Audio/FX/Analytics
                       interpolates, never writes back           subscribe to events
```
- **Entity model: data-oriented "simple ECS-lite", not a full ECS.** Each kind (`enemies`, `towers`, `projectiles`, `zones`) is held as parallel typed arrays indexed by a stable id. Systems run in a fixed order: `spawn → move → light/reveal → target → fire → resolve → economy → cleanup`. A few hundred entities don't need an archetype ECS, and flat arrays are easy for agents to reason about and to hash.
- **Determinism rules:**
  - Positions are distance-along-path integers (milli-tiles). Lanes are precomputed polylines.
  - No `sin/cos/sqrt` in the sim. Use lookup tables or squared integer distances.
  - Use our own PCG32 RNG with named streams (`waves`, `crit`, `loot`), seeded per run, instead of engine RNG globals.
  - Iterate in spawn-id order, use no wall-clock time, and never call into Nodes or the physics engine from the sim.
  - 2×/3× game speed simply runs more ticks per frame.
- **Light vs. Dark as data:** each tile has an integer `light` value from lantern auras. Enemies have `visible`/`shadowed` flags that change targeting and damage multipliers. The presentation renders this with Light2D and a fog shader, but the *rules* live in the sim, so bots can balance them.
- **Data-driven content (JSON, not YAML).** Godot parses JSON natively, the same format serves remote config, and JSON Schema tooling is mature.
  - Files: `towers.json` (tiers, cost, range, dps, light radius, targeting), `enemies.json` (hp, speed, armor, shadow traits, bounty), `waves/<level>.json` (timed spawn groups per lane), `levels/<id>.json` (path polylines, build spots, start sap, lives, star thresholds), `economy.json`.
  - A content hash (SHA-256 of canonicalized JSON) is stamped into every save, replay and analytics session.
- **Replay format:** `{sim_version, content_hash, level, seed, commands[]}`. The end state is an `int` hash of SimState. Replays drive golden tests, bug reports (Sentry attachments) and balance analysis.

### 2.3 Project folder structure
```
hollowguard/
├─ project.godot · export_presets.cfg (no secrets) · .godot-version
├─ sim/            # pure deterministic core (no Node deps) — systems/, rng.gd, fixed.gd, replay.gd
├─ game/           # presentation: scenes/*.tscn, ui/, fx/ (Light2D, particles, shaders), audio/
├─ platform/       # adapters behind interfaces: ads.gd, store.gd, analytics.gd, crash.gd, remote_config.gd (+ fakes for tests)
├─ content/        # *.json + schemas/*.schema.json + content.lock (hash)
├─ assets/         # art/, audio/, fonts/ + LICENSES.csv (every asset: source, license, generator, date)
├─ addons/         # gut, admob, iap, sentry, gameanalytics — vendored at pinned versions
├─ tests/
│  ├─ unit/        # GUT tests for sim systems & content loaders
│  ├─ replays/     # golden replays + expected state hashes
│  ├─ balance/     # bots/ + thresholds.json (owned by Game Designer)
│  └─ visual/      # scenarios.json + baselines/*.png
├─ tools/          # python: validate_content, license_check, balance_report, img_diff, api_dump
├─ docs/api/       # godot --doctool XML for 4.7.2 (agent reference, prevents API hallucination)
├─ fastlane/       # Fastfile, Appfile, Matchfile, metadata/ (store text + generated screenshots)
└─ .github/workflows/  pr.yml · nightly.yml · release.yml · promote.yml
```
Agents author `.tscn` files mostly by script or template, and keep scenes small: one scene per tower or enemy view, with all logic in `.gd`.

### 2.4 Automated testing strategy
| Layer | What | Tooling | Gate |
|---|---|---|---|
| 0. Static | gdformat/gdlint, `--check-only` on all scripts, JSON Schema, asset license manifest (no asset without a license row), export preset sanity | gdtoolkit, check-jsonschema, python | every PR |
| 1. Unit | Each sim system, fixed-point math, RNG streams, content loader, economy rules, platform fakes | GUT CLI headless | every PR |
| 2. Golden replays | ~30 recorded replays must reproduce the exact end-state hash. Any intentional change must regenerate them in the same PR, with a diff report | headless runner | every PR |
| 3. Balance bots | Strategies: *Random*, *Greedy-DPS*, *Coverage/Light-heuristic*, *Scripted-expert*, plus Monte Carlo over N seeds per level. Metrics: win %, lives lost, sap curve, tower pick rate, clear time, light-coverage %. The Game Designer sets target bands per level (e.g. naive bot loses L5+, expert wins ≥ 95%, ≥ 3 viable openings) | headless, CI matrix shards | smoke on PR (5 seeds); full sweep nightly with markdown/CSV report |
| 4. Visual regression | Scripted scenarios (menus, HUD, each level at tick T with fixed seed and `TEST_MODE` freezing time-based shaders) rendered at 1080×1920 under **Xvfb + `--rendering-driver opengl3`** (verified here), then compared to baselines with a perceptual diff tolerance. Baselines change only in PRs labelled `visual-update` | Godot + Xvfb + python diff | every PR |
| 5. Perf | Headless sim tick budget (e.g. < 2 ms/tick at 300 entities), plus an on-device **stress scene** (300 enemies, 40 towers, particles, lights) whose FPS/frame-time is logged to GameAnalytics/Sentry from internal-track testers | bench script; Play internal track | nightly; device check at each gate |

Rough throughput: the GDScript micro-benchmark ran 1.2M entity-updates in about 0.2 s, so a full level run should take around 1 s headless and a 2,000-run nightly sweep fits in about 10–15 min across 4 shards. This is an estimate to confirm in the spike.

### 2.5 CI/CD pipeline (GitHub Actions)
| Workflow | Runner | Steps |
|---|---|---|
| `pr.yml` | `ubuntu-24.04` (official Godot binary and templates, cached; or the `barichello/godot-ci:4.7.2` image, updated 2026-08-18) | import → lint → unit → replays → balance smoke → visual diff → **web export to a preview URL** → debug APK artifact. Target ≤ 15 min |
| `nightly.yml` | ubuntu matrix | full balance sweep, perf bench, content and asset audit. Opens an issue when anything is out of band |
| `release.yml` (tag `v*`) | ubuntu → **Android**: `--export-release` AAB, signed via `GODOT_ANDROID_KEYSTORE_RELEASE_*` secrets, fastlane `supply` to the **internal** track. `macos-26` (arm64, Xcode 26) → **iOS**: Godot iOS export → `xcodebuild archive` → fastlane `match` (certificates in an encrypted private repo) → `pilot` to **TestFlight**. Both: Sentry release and debug symbols upload |
| `promote.yml` (manual) | ubuntu/mac | Protected by a **GitHub Environment `production` whose required reviewer is the Owner**, so the Owner approves a gate with one click. Play: closed → production with staged rollout 5→20→50→100%. iOS: `deliver` with phased release |

- **iOS constraints:**
  - Godot's docs require macOS + Xcode for iOS export.
  - Apple has required Xcode 26 / iOS 26 SDK builds since 2026-04-28.
  - GitHub retired its macOS 14 runners on 2026-11-02, so pin `macos-26`, not `-latest`.
  - macOS minutes cost about 10× Linux (around $0.062/min per search results, not fetched). Run mac jobs **only on release tags**, which comes to roughly $1–2 per iOS build.
- **Fallback:** Codemagic. Personal accounts get 500 free M2 minutes/month; teams pay $0.095/min (per search results). Only the iOS job would move there.
- **Android:** Google Play requires target API 36 by 2026-08-31, which Godot 4.7.2's template already meets.
- **Automation auth:**
  - App Store Connect API key (`.p8` + key id + issuer id; no 2FA prompts in CI).
  - Google Play service-account JSON.
  - Agents never hold the Owner's personal Apple or Google passwords.

### 2.6 Store release & live content
- **Store assets live in the repo:** metadata is in `fastlane/metadata`, and store screenshots are *generated* by the visual-test harness at store resolutions.
- **Release train:** Concept → (web previews) → **Vertical slice**: TestFlight + Play internal → **Soft launch**: 1–2 markets, staged rollout → **Launch**.
- **Live content is data-only, to comply with App Store 2.5.2,** which bans downloading code that changes features.
  - We may push remote JSON: tuning values, events, offers, wave tweaks for existing levels, and new level layouts that reference **bundled** scenes and art.
  - New scripts or features ship as store updates.
  - Godot PCK resource packs are allowed **only for art/audio**, never scripts. CI rejects any `.gd` file in a live pack.
  - Remote payloads are signed (verified with Godot `Crypto`), schema-validated, cached with a TTL, and fall back to bundled content.
- **A/B and remote config:** start with our own signed JSON. GameAnalytics also offers remote configs and A/B testing (unverified), which we will evaluate at soft launch.

### 2.7 Services
| Need | Service | Cost |
|---|---|---|
| Crash + script errors + replay attachments | Sentry (official Godot SDK) | free tier to start |
| Product analytics / funnels / economy | GameAnalytics (official Godot SDK) | free |
| Ads | AdMob + UMP consent (+ mediation later) | revenue share |
| IAP | Store-native billing via plugins; server receipt validation deferred until revenue justifies it | store fees |
| Remote config / live JSON / web previews | Cloudflare Pages/R2 or GitHub Pages | ~free |
| CI | GitHub Actions (+ Codemagic fallback for iOS) | ~$10–40/mo estimated |

### 2.8 What the human Owner must do personally
| # | Task | Why it can't be delegated |
|---|---|---|
| 1 | Enroll in the **Apple Developer Program** ($99/yr). For an *Organization* account: legal entity, **D-U-N-S number**, website, and a domain email | Identity/legal verification |
| 2 | In App Store Connect: accept the **Paid Apps agreement** and enter **banking + tax** details. Create an **App Store Connect API key** (App Manager) and put it in GitHub secrets | Legal contracts and payouts |
| 3 | Create a **Google Play Console** account (one-time fee, amount unverified) and complete identity verification. *Organization* accounts skip the "12 testers × 14 days" closed-test rule that applies to personal accounts | Identity |
| 4 | Set up a Play **payments profile** (merchant, tax). Create the **Google Cloud service account** for the publishing API and grant it access in Play Console | Payouts and access grants |
| 5 | **Signing keys:** approve Play App Signing enrollment. Keep an offline backup of the Android upload keystore and the `match` encryption passphrase in a password manager | Losing them blocks updates |
| 6 | Create an **AdMob** account with payment and tax details. Publish `app-ads.txt` on a domain you own | Payouts and domain ownership |
| 7 | Buy a **domain**. Approve the **privacy policy**, support URL, Apple privacy labels, Play Data Safety form and age ratings (agents draft all of these) | Legal attestations |
| 8 | Accounts for **Sentry, GameAnalytics, Cloudflare/GitHub billing** (macOS minutes) | Billing ownership |
| 9 | Own one **low-end Android** phone (~2 GB RAM) and one recent **iPhone** for gate checks, and install TestFlight / Play internal builds | Real-device feel and performance sign-off |
| 10 | Be the **required reviewer** on the `production` GitHub Environment, which is how gates get approved | The gate is the Owner's decision |

### 2.9 Week-1 technical spike (exit criteria)
1. `ubuntu` CI: lint, unit tests, a golden replay, one Xvfb screenshot, a signed AAB and a web export, all green.
2. A stress scene (300 enemies, 40 towers, particles, 8 Light2D, fog shader) holds **≥ 55 fps on a ~2 GB RAM Android device** using the Compatibility renderer.
3. An iOS TestFlight build from `macos-26` works once the Owner's accounts exist.
4. The AdMob test rewarded ad and a sandbox IAP work behind the `platform/` interfaces.

---

## 3. Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| LLMs write Godot 3-style or hallucinated APIs | High | Commit the `--doctool` 4.7.2 API dump; `--check-only` and gdlint in pre-commit and CI; enforce static typing; keep an agent style guide with Godot 3 → 4 pitfalls |
| Community plugins (AdMob, iOS IAP) lag new Godot or SDK versions | Medium | Vendor and pin plugins; keep them behind `platform/` adapters; upgrade Godot only on our schedule; fallback is a thin custom plugin |
| 2D lights and fog too costly on low-end GPUs | Medium | Week-1 spike; baked light textures + shader fallback; quality tiers |
| Software-GL screenshots differ from device GPUs | Medium | Visual tests only guard *regressions*; device screenshots get checked at gates |
| Determinism broken by engine upgrade or float use | Low–Med | Integer sim, no trig, golden replays block upgrades |
| Apple 2.5.2 rejection from live content | Low | Data-only remote content; no scripts in packs (CI check) |
| CI cost creep on macOS | Low | Run mac only on tags; Codemagic free minutes as overflow |
| Play 12-tester/14-day rule for a personal account delays launch | Medium if personal | Use an Organization account (Owner question 1) |

## 4. Open questions for the Owner
1. **Will you publish as an organization** (company + D-U-N-S) or as an individual? An organization account avoids Google's 12-tester/14-day rule and shows a studio name as seller, but enrollment takes longer.
2. **Monthly tooling budget ceiling** for CI and services: is roughly **$50/month** acceptable to start? That decides whether iOS builds go to GitHub macOS runners or Codemagic's free tier.

## 5. Sources
**Retrieved and read this session (curl or download):**
- https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip (downloaded and executed headless)
- https://raw.githubusercontent.com/godotengine/godot/master/version.py
- https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/platform/android/java/app/config.gradle
- https://raw.githubusercontent.com/godotengine/godot/master/LICENSE.txt
- https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/editor/command_line_tutorial.rst
- https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/export/exporting_for_ios.rst
- https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/export/exporting_for_android.rst
- https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/export/exporting_pcks.rst
- https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/platform/android/android_in_app_purchases.rst
- https://raw.githubusercontent.com/actions/runner-images/main/README.md
- https://developer.apple.com/support/enrollment/
- https://developer.apple.com/programs/enroll/
- https://developer.apple.com/news/upcoming-requirements/
- https://developer.apple.com/app-store/review/guidelines/
- https://raw.githubusercontent.com/poingstudios/godot-admob-plugin/master/README.md
- https://raw.githubusercontent.com/hyochan/godot-iap/main/README.md
- https://raw.githubusercontent.com/getsentry/sentry-godot/main/README.md
- https://raw.githubusercontent.com/GameAnalytics/GA-SDK-GODOT/master/README.md
- https://raw.githubusercontent.com/bitwes/Gut/main/README.md
- https://raw.githubusercontent.com/MikeSchulze/gdUnit4/master/README.md
- https://raw.githubusercontent.com/fastlane/docs/master/docs/app-store-connect-api.md
- https://pypi.org/pypi/gdtoolkit/json
- https://hub.docker.com/v2/repositories/barichello/godot-ci/tags
- https://hub.docker.com/v2/repositories/unityci/editor/tags
- https://raw.githubusercontent.com/defold/defold/master/VERSION · https://raw.githubusercontent.com/defold/defold/dev/VERSION · https://raw.githubusercontent.com/defold/defold/dev/LICENSE.txt
- https://raw.githubusercontent.com/cocos/cocos-engine/v3.8.8/package.json
- https://registry.npmjs.org/phaser/latest · https://registry.npmjs.org/@capacitor/core/latest · https://registry.npmjs.org/@capacitor-community/admob/latest · https://registry.npmjs.org/@revenuecat/purchases-capacitor/latest · https://registry.npmjs.org/@capacitor-firebase/crashlytics/latest

**Seen only as web-search results.** The pages themselves were blocked by this session's network policy, so I did not open them; treat as secondary:
- https://unity.com/pricing-updates · https://unity.com/blog/unity-6-3-lts-is-now-available · https://unity.com/blog/unity-is-canceling-the-runtime-fee
- https://godotengine.org/releases/4.6/ · https://defold.com/2026/01/12/Defold-1-12-0/
- https://support.google.com/googleplay/android-developer/answer/14151465 (12 testers / 14 days)
- https://support.google.com/googleplay/android-developer/answer/11926878 (target API 36 by 2026-08-31)
- https://docs.codemagic.io/billing/pricing/ · https://docs.github.com/en/billing/reference/actions-runner-pricing

**Unverified:** Google Play registration fee amount; Godot and Defold app-size baselines; GameAnalytics remote-config and A/B features; 2D light performance of the Compatibility renderer on low-end GPUs (Week-1 spike).
