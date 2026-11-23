# Salted Caramel Owl — Studio Brief (v0.1, Lead)

> Every team member reads this first. It is the single source of truth for direction.
> If your research contradicts a hypothesis here, say so explicitly — that is the point.

## Who we are
- **Studio:** Salted Caramel Owl (an AI-run mobile game studio).
- **Owner / Creative Director:** the human. The only human. Talks only to the Lead.
- **Lead (Producer/Director):** translates owner intent into requirements and tasks.
- **Team:** Market Analyst, Game Designer, UX/UI Designer, Technical Architect,
  Art & Audio Director, Economy & LiveOps Designer, AI Production Ops.
- **Operating principle:** AI agents do the work end-to-end (design, code, art, QA, release ops).
  The human approves at **gates** (concept, vertical slice, soft launch, launch) — nothing else should need them.

## Stage
**Pre-production: planning + wireframing.** No production code yet.

## Product hypotheses (Lead's calls — challenge with evidence)
| Topic | Hypothesis |
|---|---|
| Genre | Tower defense, fixed paths + build spots (lane TD), short sessions (3–6 min/level) |
| Platform | iOS + Android, **portrait, one-thumb play** |
| Theme | Owls guard the Great Hollow Tree at night against shadow creatures. Amber "caramel" sap = soft currency. Cozy look, crunchy strategy. |
| Hook (to validate) | **Light vs. Dark**: enemies are shadow creatures; light/vision is a core resource. Owls see in the dark; lantern towers reveal & weaken. |
| Working title | *Hollowguard* (placeholder) |
| Audience | Mid-core strategy players 18–40 + cozy-game crossover |
| Business model | Fair F2P: no pay-to-win; rewarded ads + cosmetics + optional premium pass. Economy Designer to confirm vs. premium. |
| Scope | Vertical slice: 1 world, 10 levels, 6 towers, 1 hero owl, 8 enemy types, 1 boss |
| Production | AI-friendly stack: text-based sources, headless build & test in Linux CI, data-driven content (JSON/YAML) |

## Hard constraints
1. No cloning existing games (names, characters, art, levels, look). Learn from genre conventions only.
2. All assets must be legally shippable (clear licenses for AI-generated or third-party assets).
3. Everything must be buildable/testable by agents in a Linux container without a human GUI.
4. Respect Apple App Store & Google Play policies (ads, loot boxes, privacy, kids).

## Deliverable conventions for every team member
- Write your doc to `salted-caramel-owl/docs/research/<NN>-<role>.md`.
- Sections: **TL;DR (5 bullets)** → findings → **Recommendations (decisive)** → **Risks** → **Open questions for the Owner (max 3, only real ones)** → **Sources**.
- **Sources must be real URLs you actually retrieved this session.** No URLs from memory. If unverified, say "unverified".
- Be concise: aim for 1,200–2,500 words. Tables over prose.
