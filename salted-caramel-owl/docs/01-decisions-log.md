# Decisions Log — Lead rulings (v0.2, 23 Nov 2026)

> Binding for all agents until the Owner overrides. Each ruling names the docs it supersedes.
> Status: **D** = decided by Lead · **O** = waiting on Owner · **X** = Owner-confirmed.

## Product
| # | Topic | Ruling | Why | Status |
|---|---|---|---|---|
| 1 | Studio name | **Salted Caramel Owl** (not "Salty Carmel Owl") | Correct spelling, cleaner as a brand | D |
| 2 | Working title | **Hollowguard** (placeholder) | No exact match found, but the "Hollow-" prefix is crowded (Hollow Ward 2026, Hollowgrace) and close to a famous trademark. Final title at the G1 gate | O |
| 3 | Hook | **Light is territory**: build and upgrade only on lit ground. Night creeps in from the top. Saboteur enemies snuff lights. Owls fight in the dark; Lightbound towers go dormant | The "lantern reveals hidden enemies" idea already exists (Glowkeep, Oct 2026, plus jam games). Territory light makes a spatial decision every wave (01, 02) | D |
| 4 | Banned terms | "shade(s)", "Flare", "Gloom King", and lantern-reveal as a core identity | Competitor overlap (01) | D |
| 5 | Orientation & maps | Portrait, one thumb. **Every map fits one screen**, with no pan, zoom or pinch | Readability pillar (02, 03) | D |
| 6 | Default darkness | **Balanced and readable.** Dark tiles get a light violet tint, never near-black | Pillar 1. A colorblind-safe palette needs luminance headroom (03, 05) | D |
| 7 | Enemy tone | **Cute-spooky**: rounded silhouettes, big eyes, no gore | Fits "cozy look"; keeps Apple 9+ / PEGI 7 / ESRB E10+ in reach (02, 06) | D |
| 8 | Hero | **Umber the Lamplighter** is a named character with no voice lines. Cosmetic skins come later | Personality for marketing; VO is costly and localization-heavy | D |

## Design reconciliations (where team docs disagreed)
| # | Conflict | Ruling | Supersedes |
|---|---|---|---|
| 9 | Build menu: GDD says ring/arc at the spot; UX says bottom tray | **Bottom tray.** Tap a lit spot, then pick a card in the tray: first tap previews on the map, second tap confirms. Upgrade and branch choice also happen in the tray. Sell is press-and-hold with a 3 s undo, plus the GDD's 100% refund within 10 s | GDD §4 ring menu |
| 10 | Unit names: UX placeholders (Archer Owl, Thornspitter, Moonbell, Lantern Owl, Ember) | **GDD names are canonical**: Talon Roost, Burrow Gate, Screech Spire, Glowcap Lantern, Pinecone Lobber, Moonglass Prism; hero Umber | screens.json placeholders (fixed) |
| 11 | Currencies: GDD "sap / Amber / Stars"; Economy "Glow / Amber Sap" | **Sap** = in-level build currency (resets each level). **Amber** = meta soft currency (research tree, cosmetics). **Stars** = skill score, spent only in the capped, refundable Roost perks. Nothing is ever sold for money. "Glow" is reserved for the *light* mechanic so light and money never share a word | 06 §2 naming |
| 12 | HUD top: UX Light meter vs GDD moon-arc wave bar | Both. Row 1: Pause · Hearts · Sap · Wave. Row 2: **Light meter** (% lit, trend, a forecast tick for the next creep) | — |

## Business & production
| # | Topic | Ruling | Status |
|---|---|---|---|
| 13 | Model | **Fair Free + Supporter**: free campaign, opt-in rewarded ads only, a one-time $4.99 Supporter Pack, fixed-price cosmetics. No energy, no loot boxes, no countdown offers | D |
| 14 | Campaign paywall test | **No.** Worlds 2+ stay free on principle | D |
| 15 | Kids store listing | **No** Kids/Families listing. Target audience 13+ | D |
| 16 | Growth | **Organic first** (store optimization, community, creators). Small UA tests only after soft-launch KPIs | D |
| 17 | Engine | **Godot 4.7 (GDScript, typed)**. Runner-up: Phaser 4 + Capacitor | D |
| 18 | Art | Lantern-lit flat vector (SVG) with runtime glow and cut-out animation; palette `research/05-palette.json` | D |
| 19 | Monthly AI and tooling budget | Ops proposes $3–5k/mo agents + ~$50/mo tooling + paid asset-tool plans | O |
| 20 | Publisher identity | Organization vs individual developer accounts | O |
| 21 | Human-authored key assets | Logo, key art and main theme need human creative input for copyright | O |
