# 05 — Art & Audio Director: Style, AI-Asset Pipeline, Legal, Audio

**Status:** v0.1, pre-production · **Companion file:** `05-palette.json` (color tokens + validation data)

## TL;DR
- **Style: "Lantern-lit flat vector".** Flat layered shapes authored as SVG (text-based, diffable, headless-renderable), with soft light done at runtime. Characters use cut-out (skeletal) animation, not frame-by-frame drawing. This keeps everything readable at phone size and consistent across AI-made assets, and animation stays cheap.
- **Friend is warm, foe is cool.** Owls, towers, light and sap are amber/caramel. Shadow creatures are near-black bodies with a **mandatory violet rim** (`#A97BFF`). I checked every gameplay-critical color pair with simulated protan/deutan/tritan vision (method below). Hue is never the only cue: icons and patterns carry status too.
- **Pipeline:** paid vector generation (Recraft) plus agent-written SVG → automated cleanup (palette lint, part split) → rig and animation as text data → `resvg` renders atlases headless. Raster image models are used **only for moodboards**. Every asset gets a provenance-ledger entry.
- **Legal verdict: we can ship it, but we probably can't own it.** Neither store bans AI art, and our chosen tools grant commercial use. But under US law, purely AI-generated output is **not copyrightable** (USCO Part 2, Jan 2025; the Supreme Court declined *Thaler* on 2 Mar 2026). In an AI-run studio that covers almost all our assets. Mitigations: trademark the name and logo, add human authorship to a few hero assets, and keep an exclusion list of tools we never use.
- **Audio:** music is **composed as data** (MIDI/score written by agents), rendered headless with CC0 orchestral samples into layered stems. Godot's `AudioStreamSynchronized`/`AudioStreamInteractive` provide the adaptive layering. SFX: jsfxr (Unlicense) and CC0 foley, plus paid ElevenLabs SFX for organic sounds. Suno is fallback only; Udio and MusicGen are out.

---

## 1. Art direction

### 1.1 Options compared
| Criterion | A. Flat vector, layered (SVG) | B. Painterly 2D (diffusion raster) | C. Low-poly 3D pre-rendered (Blender CLI) |
|---|---|---|---|
| Small-screen readability | **High**: clean silhouettes, exact palette control | Medium: texture noise, needs heavy cleanup at 64–128 px | Medium-high: good lighting, but small renders get muddy |
| AI generation consistency | **High**: palette/stroke lint is automatable; the LLM can edit SVG text directly; vector models output SVG | **Low**: style and character drift between generations and between animation frames is the known hard problem (vendors sell custom-model training to fix it) | High once a model exists, but AI mesh generation and rigging quality is variable |
| Animation cost | **Low**: cut-out rigs in-engine, keyframes as text | **High**: frame-by-frame or AI video-to-sprite, then per-frame cleanup | Medium: rig once, re-render; atlases get large (8 directions × frames) |
| Light/dark hook support | High: glow layers + darkness overlay | High (looks great) but baked light conflicts with dynamic light | High (real lighting), but baked into sprites |
| Headless/CI fit (brief constraint 3) | **Native**: SVG → `resvg` CLI, no GUI | API-dependent; raster edits need GUI tools | Blender runs headless, but the toolchain is heavy |
| Copyright and infringement exposure | Lowest: geometric shapes rarely reproduce third-party works | Highest: diffusion models can regurgitate protected characters (see Disney/Universal v. Midjourney) | Medium |
| "Cozy" feel | Good with rounded shapes, paper grain and warm glow | Best | Okay; risks looking generic |

**Decision: A, flat vector.** Option B scores best on mood but worst on the two things an AI-run studio can't paper over: consistency and legal hygiene. We recover the coziness with a subtle paper-grain overlay, rounded forms and warm glow. Pixel art was rejected: the market is saturated with it, it fights high-DPI portrait screens, and it reads as retro rather than cozy.

### 1.2 Style guide

**Palette (tokens in `05-palette.json`)**
| Group | Tokens (hex) | Use |
|---|---|---|
| Night | `#070A1A` `#0B1026` `#141B3D` `#1F2A5A` `#2E3C78` `#4A5A9E` | Sky, scrims, UI panels, strokes |
| World | ground `#18233F`, path `#55608F`, bark `#2B1F24`/`#5C4038`, leaf `#1C3B4A` | Playfield; path vs ground 2.56:1 |
| Light / caramel | `#FFF1D0` `#FFE0A3` `#FFC15E` `#E8A33D` `#A8621E` `#5E3410` | Glow, sap currency, CTAs, tower trim |
| Owls | `#8A5A3C` `#F3E3C3` | Plumage, face disc |
| Shadow | ink `#07060F`, core `#3B2470`, rim `#A97BFF`, eye/elite `#EBDDFF` | Enemies only |
| UI | salt `#FFF8EC`, moon `#DDE6FF`, muted `#9AA6D6`, danger `#F0407A`, frost `#BFF3FF` | Text and status |

**Colorblind validation.** I simulated each color as protan, deutan and tritan viewers see it (Machado 2009 matrices, full severity), then measured CIEDE2000 distance on the results. The target was ≥15 for gameplay pairs. The rule of avoiding red+green and leaning on blue/orange plus lightness contrast comes from accessibility guidance. Key results:

| Pair | WCAG | ΔE normal / protan / deutan / tritan |
|---|---|---|
| enemy rim vs ground | 5.15 | 43 / 43 / 43 / 46 |
| enemy rim vs amber light | 1.87 | 60 / 59 / 61 / 27 |
| elite rim vs normal rim | 2.34 | 28 / 26 / 26 / 22 |
| danger vs caramel | 1.70 | 46 / 39 / 20 / 18 |
| salt text vs panel | 15.9 | n/a |

- Early drafts failed and were changed. Coral danger `#FF5A4E` vs caramel came out at **ΔE 7.7 for deutan viewers**, so it became rose `#F0407A`. A pink elite rim collapsed into the normal rim for protan viewers (ΔE 6.4), so elites now use a white-violet double rim plus a crown silhouette.
- Known weak pair: frost vs moon text (deutan ΔE 0.6). Rule: frost always comes with a shard pattern or icon.

**Silhouette rules**
| Faction | Shape language | Hard rules |
|---|---|---|
| Owls & towers | Round, vertical, rooted, symmetrical; light source on top | Each of the 6 towers has a unique **top contour** (lantern, crescent dish, bell, crystal, nest, totem) recognizable at 48 px. Owls: big amber eyes plus ear tufts. |
| Shadow creatures | Horizontal, asymmetric, jagged or wispy edges, drips and tendrils | 8 enemy types each differ in **≥2 of**: size class (S/M/L), aspect ratio, top contour, motion pattern (scuttle, float, slither, hop). No warm colors, ever. |
| Tests (automated) | Black-fill test at 25% scale; grayscale test; CVD-simulated screenshot test | A unit fails if its black silhouette's IoU with any other unit's is > 0.8. |

**Light and glow treatment (this is the hook made visible)**
- **Darkness layer:** `night-950` at about 55% opacity multiplied over the playfield. Lantern and owl light radii cut holes in it with additive radial gradients (`sap-300` → transparent). Use fake lights (additive sprites/shader), with no real-time shadows, for mobile perf.
- **Hidden → revealed:** outside light, an enemy is ink plus rim at 60% alpha. Inside light, the body lifts to `shadow-core`, the rim goes to 100%, and glowing amber "light-burn" cracks appear on the side facing the source. The player sees the "reveal & weaken" mechanic.
- **Budget:** at most 3 fully saturated glow sources plus the tree at once (the boss is the exception). Glow is never a flat fill over large areas.

**UI style**
- Panels: `night-800` at 92%, 2 px `night-600` stroke, 24 px radius. One soft top highlight; no other gradients.
- Primary CTA: caramel button with `caramel-900` text (8.3:1 on sap-300) and a small honey-drip shape language. Secondary: outlined moon.
- Icons are duotone: friendly ones caramel + cream, hostile ones violet + ink. Interaction stays in the bottom 40% thumb zone, to be aligned with the UX doc.

**Typography (all SIL OFL, verified in the google/fonts repo METADATA)**
| Role | Font | Notes |
|---|---|---|
| Display / titles / wave banners | **Fredoka** | Rounded, cozy, chunky |
| UI and body | **Nunito** | Rounded terminals match Fredoka. Min 28 px at 1080 px width. |
| Accessibility toggle and dense numbers | **Atkinson Hyperlegible** | Built for legibility. Must verify tabular figures before using it for counters. |
| Alternate display | Baloo 2 | Backup if Fredoka glyph coverage fails for localization |

---

## 2. AI-asset pipeline and legal status

### 2.1 Legal findings
| Question | Finding | Confidence |
|---|---|---|
| Is pure AI output copyrightable (US)? | **No.** USCO Part 2 (29 Jan 2025): material generated purely by AI isn't protected, and prompts alone are not enough. Human selection/arrangement, and human modifications, *can* be protected. | High (USCO report via search summary) |
| Is that settled? | The D.C. Circuit upheld the human-authorship requirement (2025), and the Supreme Court **denied cert on 2 Mar 2026** (No. 25-449). How much human input is enough is still open (*Allen v. Perlmutter* is pending). | High |
| Can arrangement/editing earn protection? | Yes, narrowly. *A Single Piece of American Cheese* (Invoke, about 35 inpainting passes) was registered for selection, coordination and arrangement only, with the AI segments excluded. | Medium |
| Infringement risk *from* outputs | Real. Disney/Universal (later joined by Warner Bros.) v. Midjourney alleges recognizable characters come out of generic prompts; the case is in discovery (mid-2026). | Medium |
| Apple App Store | Guidelines (last updated **16 Oct 2026**) contain **no AI-asset disclosure rule**. 4.1 Copycats and 5.2.1 IP apply ("submitted by the … entity that owns or has licensed the intellectual property"). The AI rules target AI *content-creation apps* (filtering and reporting). | High (fetched) |
| Google Play | Its AI-Generated Content policy targets apps that generate content at runtime (in-app reporting, filters). Pre-made game art is out of scope. | Medium (search summary, not fetched) |
| Steam (if ever on PC) | Jan 2026 rewrite: disclose AI content "consumed by players" (pre-generated or live). Dev tools are exempt. | Medium |

**Tool terms (commercial use)**
| Tool | Terms | Verdict |
|---|---|---|
| Claude (API/commercial) | Customer owns outputs; Anthropic assigns its rights; no training on customer content | Green |
| OpenAI (images/text) | "We hereby assign to you all our right, title, and interest, if any, in and to Output"; output may not be unique | Green |
| Recraft (vector/SVG) | **Paid plan:** full ownership plus commercial rights, persists after cancelling. **Free plan:** Recraft owns, non-commercial, and can't be bought later. | Green, **paid only** |
| Adobe Firefly | Commercial use OK for non-beta features. IP indemnity only on eligible enterprise plans; trained on licensed content | Green (concept use) |
| FLUX.1 [schnell] | Apache-2.0 weights | Green |
| FLUX.1 [dev]/Kontext/etc. | Non-commercial unless licensed from BFL | **Red** |
| ElevenLabs SFX/Music | Paid plans: commercial license. Free: none | Green, paid only |
| Suno | Pro/Premier: commercial rights, capped at 20/60 downloads per month (terms of 3 Sep 2026). Free: non-commercial. Ownership wording was revised after the Warner deal. | **Amber** (fallback only) |
| Udio | Downloads cut after the UMG settlement; moving to a "walled garden" | **Red** |
| Stable Audio (Community License) | Commercial use free under $1M annual revenue; above that, Enterprise license. Launch-era terms for the 1.0 weights are ambiguous | Amber |
| MusicGen/AudioCraft | Weights **CC-BY-NC 4.0** | **Red** |
| Spine | Every user of the runtime-integrated product needs their own Spine Editor license, which is awkward for an agent team | Avoid |
| DragonBones runtime / Rive runtime | MIT | Green (runtime), but editors need a GUI |

### 2.2 Recommended pipeline (legally safe and headless)
| Step | What | Tooling | Gate / check |
|---|---|---|---|
| 0 | Style bible + tokens | This doc, `05-palette.json` | Owner approves at the concept gate |
| 1 | Moodboards / exploration | Firefly or OpenAI images, FLUX schnell. **Never shipped.** | No artist names, franchises or "in the style of" in prompts. No img2img from third-party art. |
| 2 | Production vectors | Recraft **paid** vector model for characters and props; Claude writes SVG directly for UI, icons, simple props and VFX shapes | Generated on the paid plan only (ownership is fixed at the moment of generation) |
| 3 | Cleanup (agent) | Script: snap every fill to a palette token (ΔE < 3), simplify paths, enforce named groups (`head`, `wing_l`, …) | **Palette lint** and **part-naming lint** fail the CI build |
| 4 | Rig + animation | Engine-native cut-out bones (Godot `Skeleton2D`/`AnimationPlayer` if the Tech Architect picks Godot) plus procedural motion (bob, squash, sway) declared in data | Animations live as text resources |
| 5 | Render + pack | `resvg` CLI (MIT/Apache, no dependencies) → PNG at 1× (1080 px wide) and 1.5× → atlas packer | Silhouette IoU test, grayscale test, CVD screenshot test |
| 6 | Similarity screen | Perceptual-hash/embedding comparison against a reference set of top TD games and franchise characters | Flag anything above the threshold for regeneration |
| 7 | Provenance ledger | `assets/manifest.json`: file, tool, model + version, plan tier, date, prompt/seed, license ID, human edits, reviewing agent | Required for every asset; also feeds any Steam disclosure |
| 8 | Human-authored hero assets | Owner (or a contracted human) makes meaningful creative edits to the logo, key art and main theme; the edits are documented | Gives us something enforceable; trademark the name and logo |

---

## 3. Audio

### 3.1 Approach
| Need | Primary | Fallback | Why |
|---|---|---|---|
| Music | **Composed as data.** Agents write MIDI/score in code, render headless with a sampler and **VSCO-2 Community Edition orchestral samples (CC0)**, export stems | Suno Pro/Premier or ElevenLabs Music (paid), logged in the ledger | No ToS dependency, deterministic rebuilds, stems come for free for adaptive layering. Risk: can sound "MIDI-ish", which is mitigated with humanized timing and a mix pass |
| UI/combat SFX | **jsfxr** (Unlicense; `npm i jsfxr`). Sounds stored as serialized JSON params and generated in CI | Kenney audio packs (CC0) | Text-based and reproducible; the 8-bit edge gets softened by layering and filtering |
| Organic SFX (hoots, growls, wood, sap squelch) | ElevenLabs SFX (**paid plan**) | Kenney CC0 foley; the Sonniss GDC bundle (royalty-free per secondary sources, **license unverified**) | Quality where synthesis is weak |
| Processing | ffmpeg/SoX: loudness normalize (−16 LUFS music, −14 peak-safe SFX), OGG for Android and iOS (engine-dependent) | n/a | Headless |

### 3.2 Adaptive music: "Lantern Layers"
One level theme in D Dorian, 92 BPM, built as 5 synchronized stems (`AudioStreamSynchronized`: sub-streams start together, volume per stream). Clip switching (`AudioStreamInteractive`: clips plus a transition table, beat-synced fades) handles the stingers.

| Game state | Layers on | Extra treatment |
|---|---|---|
| Build phase (calm night) | Pad + celesta/music-box motif | Crickets and owl-hoot ambience bed |
| Wave active | + pizzicato ostinato + soft hand-drums | n/a |
| Dense wave (enemy count > threshold) | + low strings/bass pulse | n/a |
| Tree light low / leaks | n/a | Low-pass sweep and slight detune on the pad: **the darkness "muffles" the music** |
| Boss | Switch to boss clip (same key, brass + choir) | Beat-synced transition |
| Victory | Dawn stinger: modulates to D major, birdsong | "Night ends" payoff |
| Defeat | Pad-only cadence, wind | n/a |

---

## 4. Vertical-slice asset list
Design resolution 1080×1920 portrait; build tile ≈144 px. Sources are SVG and exports are 1× and 1.5×. "Keys" means cut-out keyframes; "baked fr" is the 12 fps frame count if we ever bake sprite sheets.

| Category | Items | Count | Size @1× | Animation |
|---|---|---|---|---|
| Towers | 6 types × 3 upgrade tiers | 18 | 144×176 | idle (procedural), attack 4–6 keys / 6 baked fr |
| Build spot | empty, highlighted, locked | 3 | 144×144 | pulse (shader) |
| Hero owl | 1 rig (~12 parts) | 1 | 128×128 | idle, fly, attack, ability, hit, rest/KO, victory = 7 anims (8 baked fr each) |
| Enemies | 8 rigs (5–9 parts) + 8 elite overlays | 16 | S 80, M 112, L 144 | move loop (8 fr), hit flash + dissolve death (shared shader), special anim on 4 types |
| Boss | 1 rig (~16 parts) | 1 | 360×360 | move, 2 attacks, phase change, hit, death = 6 |
| Projectiles + impacts | 1 per tower | 12 | 32–64 | 4–6 fr or particles |
| VFX | light radius, reveal pulse, light-burn cracks, sap pickup, build/upgrade, slow, burn, dissolve, tree hit, wave-start, victory dawn, owl vision ping | 12 | varies | particles/shaders |
| Environment kit (World 1 "Rootwood") | ground tiles 2, path spline set 1, props 20, parallax sky 3 layers, paper-grain overlay 1 | 27 | tiles 144, sky 1080×1920 | sway on 6 props |
| Great Hollow Tree | 3 damage states + glow layer | 4 | 540×720 | breathing glow |
| Level layouts | 10 (data only, reuse the kit) | 10 | n/a | n/a |
| UI kit | buttons (3 states × 3 types), panels, bars, stars, wave preview, toggles | ~30 | 9-slice | tweens |
| Icons | towers 6, enemies 8, sap currency 1, hero abilities 3, status 6, settings/system 10 | 34 | 96 (192 in the shop) | n/a |
| Brand | logo, app icon (1024), splash | 3 | n/a | n/a |
| Music | level theme (5 stems), boss clip, menu theme, victory, defeat, dawn stingers | 6 cues / 10 files | n/a | loopable |
| SFX | UI 10, tower fire+impact 12, build/upgrade/sell 3, enemy spawn/death 16, boss 6, hero 6, economy 3, tree hit/alarm 3, wave horn 1, ambience loops 2 | ~62 | n/a | n/a |

---

## Recommendations (decisive)
1. **Adopt flat vector with cut-out animation.** Lock `05-palette.json` as the single color source; CI rejects off-palette fills.
2. **Production art tools allowlist:** Recraft (paid), Claude-authored SVG, FLUX schnell. Firefly/OpenAI for concepts only. **Banned:** FLUX dev-family weights without a BFL license, MusicGen weights, Udio, any free tier, Spine.
3. **Provenance ledger is mandatory from asset #1**, along with the prompt hygiene rules (no artist names or IP names, no third-party img2img).
4. **Music as code** with VSCO-2 CE (CC0) and **SFX as jsfxr JSON plus CC0**; ElevenLabs paid for organic sounds.
5. **Protect the brand legally, not the sprites.** Trademark the name and logo, put human creative input into the hero assets, and accept that the rest of the art is effectively unprotectable.
6. Ask the Tech Architect to confirm the engine supports cut-out bones and synced audio stems (Godot 4.3+ does both natively).

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Competitors lift our unprotected sprites | Medium | Trademark, fast content cadence, human-authored hero assets |
| Vector style reads "generic clip-art" | Medium | Paper grain, glow, bespoke shape language; owner review at the concept gate |
| AI tool ToS changes (Suno did so twice in 2025–26) | High | Ledger records terms at generation time; prefer owned pipelines (code-composed music, LLM SVG) |
| Output resembles protected IP | Low-medium | Prompt hygiene, similarity screen, vector-first |
| Code-composed music sounds cheap | Medium | Humanization, mix pass, paid AI or human fallback for the menu theme |
| Dark playfield too dark on low-brightness phones | Medium | Rim-light rule, brightness/"Lantern assist" setting, device testing |

## Open questions for the Owner
1. **Will you (or a contracted human) put real creative work into 3 hero assets: logo, key art and main theme?** This is the only practical way to get enforceable copyright on anything visual or audio; everything else stays public-domain-like.
2. **Do you approve a small recurring budget for paid AI tool tiers (Recraft, ElevenLabs, optionally Suno)?** Free tiers are legally unusable for us; AI Production Ops should confirm current prices before purchase.

## Sources
**Retrieved this session (fetched via curl):**
- Apple App Store Review Guidelines (updated 16 Oct 2026): https://developer.apple.com/app-store/review/guidelines/
- jsfxr README / package.json (Unlicense): https://raw.githubusercontent.com/chr15m/jsfxr/master/README.md · https://raw.githubusercontent.com/chr15m/jsfxr/master/package.json
- AudioCraft weights license (CC-BY-NC 4.0): https://raw.githubusercontent.com/facebookresearch/audiocraft/main/LICENSE_weights · README: https://raw.githubusercontent.com/facebookresearch/audiocraft/main/README.md
- FLUX model licenses table: https://raw.githubusercontent.com/black-forest-labs/flux/main/README.md
- Spine Runtimes License: https://raw.githubusercontent.com/EsotericSoftware/spine-runtimes/4.2/LICENSE
- DragonBones runtime README: https://raw.githubusercontent.com/DragonBones/DragonBonesJS/master/README.md
- Rive runtime license (MIT): https://raw.githubusercontent.com/rive-app/rive-runtime/main/LICENSE
- Godot 2D skeletons / cut-out docs: https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/animation/2d_skeletons.rst · https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/animation/cutout_animation.rst
- Godot AudioStreamInteractive / Synchronized class docs: https://raw.githubusercontent.com/godotengine/godot/master/modules/interactive_music/doc_classes/AudioStreamInteractive.xml · https://raw.githubusercontent.com/godotengine/godot/master/modules/interactive_music/doc_classes/AudioStreamSynchronized.xml
- Google Fonts METADATA (OFL): https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/METADATA.pb · https://raw.githubusercontent.com/google/fonts/main/ofl/nunito/METADATA.pb · https://raw.githubusercontent.com/google/fonts/main/ofl/atkinsonhyperlegible/METADATA.pb · https://raw.githubusercontent.com/google/fonts/main/ofl/baloo2/METADATA.pb
- VSCO-2 CE (CC0): https://raw.githubusercontent.com/sgossner/VSCO-2-CE/master/README.md · https://raw.githubusercontent.com/sgossner/VSCO-2-CE/master/LICENSE
- resvg README (MIT/Apache, CLI): https://raw.githubusercontent.com/linebender/resvg/main/README.md

**Seen via web-search results only (the network policy blocked direct fetch; treat as unverified against the primary page):**
- USCO Part 2 release: https://copyright.gov/newsnet/2025/1060.html · LoC blog: https://blogs.loc.gov/copyright/2025/02/inside-the-copyright-offices-report-copyright-and-artificial-intelligence-part-2-copyrightability/
- Thaler cert denied: https://www.supremecourt.gov/docket/docketfiles/html/public/25-449.html · https://www.mayerbrown.com/en/insights/publications/2026/03/supreme-court-denies-review-in-ai-authorship-case
- American Cheese registration: https://petapixel.com/2025/02/12/this-is-the-first-ever-ai-image-to-be-granted-copyright-protection-a-slice-of-american-cheese
- Google Play AI-Generated Content policy: https://support.google.com/googleplay/android-developer/answer/14094294
- Steam AI disclosure rewrite: https://videogameschronicle.com/news/valve-has-significantly-rewritten-steams-rules-for-how-developers-much-disclose-ai-use
- Disney/Universal v. Midjourney: https://www.theartnewspaper.com/2026/07/09/midjourney-demands-hollywood-AI-secrets
- Anthropic Commercial Terms: https://www.anthropic.com/legal/commercial-terms · OpenAI Terms: https://openai.com/policies/row-terms-of-use/
- Recraft ownership: https://www.recraft.ai/docs/plans-and-billing/commercial-rights-ownership-and-copyright
- Adobe Firefly product description / indemnity: https://helpx.adobe.com/legal/product-descriptions/adobe-firefly.html
- Suno: https://help.suno.com/en/articles/2416769 · https://help.suno.com/en/articles/13614785 · https://www.musicinafrica.net/magazine/suno-adjusts-ai-music-ownership-terms-after-warner-music-partnership
- Udio after UMG deal: https://www.digitalmusicnews.com/2025/10/31/udio-downloads-disabled-umg-deal/
- ElevenLabs commercial use: https://help.elevenlabs.io/hc/en-us/articles/13313564601361 · https://elevenlabs.io/sound-effects-terms
- Stability AI license: https://stability.ai/license
- Scenario sprite sheets (consistency tooling): https://help.scenario.com/articles/9088582240-create-spritesheets-with-scenario
- Kenney CC0: https://kenney.nl/support · Sonniss (secondary): https://licenseorg.com/guide/music-audio/sonniss
- Colorblind guidance: https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/ · https://venngage.com/blog/color-blind-friendly-palette
- Godot adaptive music tutorial: https://uhiyama-lab.com/en/notes/godot/adaptive-music-system/

**Method note:** I computed the palette's CVD/contrast numbers myself, with a headless Python script (Machado 2009 matrices, CIEDE2000, WCAG 2.x). The values are in `05-palette.json` → `validation`.
