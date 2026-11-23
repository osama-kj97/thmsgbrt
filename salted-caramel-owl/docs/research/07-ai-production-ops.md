# 07 — AI Production Ops: how Salted Caramel Owl runs with agents

*Author: AI Production Ops · Date: 2026-11-23 · Status: v1 proposal to the Lead*

## TL;DR
- **Use one orchestrator plus specialist workers, and keep coordination in GitHub.** The Lead turns Owner intent into GitHub issues. Each worker takes **one issue → one branch → one PR**, and a separate read-only Reviewer with a fresh context reviews it. I recommend this over free-form agent "teams": Claude Code's agent teams are still experimental, and the docs say same-file edits and dependent work go better with single sessions or subagents.
- **The test harness is the real manager.** Anthropic's 16-agent C-compiler run found the task verifier has to be "nearly perfect, otherwise Claude will solve the wrong problem." Every game rule therefore runs in a **deterministic headless simulation**, so balance bots, scripted playthroughs and golden screenshots can gate every merge.
- **The Owner sees four gates and one weekly digest.** Gates: Concept **18 Dec 2026**, Vertical Slice **14 May 2027**, Soft Launch **20 Aug 2027** (go-live about 30 Aug), Launch **about 19 Nov 2027** (driven by KPIs). Between gates there is only a one-screen Monday digest.
- **Hard cost and safety rails.** Every agent run has a turn cap and a timeout, every issue has a size and budget cap, a workspace spend limit sits under everything, and 3 kill switches can be flipped in about a minute. Spending stays in a monthly envelope, which the Owner sets once (see Open questions).
- **Anti-loop rules are mechanical, not left to judgement.** A PR gets at most 3 automated fix attempts and an issue gets at most 2 fresh sessions before the Lead re-specifies it. Bots cannot trigger bots. Stale PRs are closed automatically, and tests cannot be weakened without a flag.

---

## 1. Findings: what current practice says (2025–2026)

| Finding | Implication for us | Source |
|---|---|---|
| Subagents run in their own context and can be restricted (`tools`, `disallowedTools`, `model`, `maxTurns`, `permissionMode`, `isolation: worktree`). Project agents live in `.claude/agents/`. | Define each role as a versioned agent file in the repo. Reviewer and QA get read-only tools, and the read-only limit is enforced by Claude Code, not just asked for in a prompt. | Claude Code docs: sub-agents, best practices |
| Agent teams are **experimental**: no session resumption, task status "can lag", no nested teams. Docs advise starting with 3–5 teammates, warn that two teammates editing the same file overwrite each other, and say teams "use significantly more tokens." | Don't build production on agent teams. Use cloud sessions and GitHub as the coordination layer, cap parallel workers at **4**, and give each issue explicit file ownership. | agent-teams doc |
| Cloud sessions keep running with the laptop closed and run in parallel. **Auto-fix** watches a PR and pushes fixes for CI failures and review comments, but asks first on ambiguous requests. | Workers run as cloud sessions. Auto-fix handles the CI-red loop, but with an attempt cap (§4). | claude-code-on-the-web doc |
| Scheduled tasks (formerly "routines") run on a schedule, an API call or a GitHub event. They are a research preview, owned by a **single account**, push to `claude/`-prefixed branches by default, and are subject to hourly caps. | Use them for the nightly sim, the weekly digest and triage. They are not the backbone, because preview behaviour may change. | routines doc |
| `anthropics/claude-code-action@v1` handles `@claude` mentions, automated review and cron jobs. It **rejects bot actors unless they are listed in `allowed_bots`**, which stops bot-to-bot loops. Cost controls are `--max-turns` and workflow timeouts. | CI review and agent jobs run here, under the repo's own Actions minutes and an API key with a workspace spend limit. | github-actions doc, action README |
| Claude Code Review (Team/Enterprise plans) runs several agents, verifies their findings, ranks them by severity and **never approves or blocks**. It reads `REVIEW.md` from the base branch only, and it has its own monthly spend limit. | It can serve as a second review layer if we're on a Team plan. Merges are still blocked by CI plus our own Reviewer verdict. | code-review docs |
| CLAUDE.md is context, **not enforcement**. Docs say to keep it under about 200 lines, and to use a PreToolUse hook (exit code 2) to actually block an action. | CLAUDE.md stays short (draft in §6). Protected paths are enforced with hooks and branch rules. | memory doc, hooks guide |
| Long-running agents fail in two ways: they **one-shot too much**, and they **declare victory early**. The fixes are a JSON feature list where agents only flip `passes`, one feature per session, a progress file plus git history, and end-to-end testing "as a human user would." | Acceptance criteria live as JSON checklists. Each PR covers one feature. Each issue thread carries a progress log. Scripted playthroughs serve as the end-to-end tests. | Anthropic: effective harnesses |
| Agents grading their own work "confidently praise" it. A separate evaluator tuned to be skeptical is "far more tractable." A full planner/generator/evaluator harness cost **$200 over 6 h, against $9 for a solo run**, and produced far better output. | The author never reviews their own PR. Subjective work (art, UX) is graded against written criteria by a different agent. Spend extra on review only where the model is near its limits. | Anthropic: harness design |
| C compiler: 16 agents, about 2,000 sessions, **$20k**, 2 weeks. Lessons: tests must be near-perfect; keep harness output short and log to files with grep-able `ERROR` lines; offer a `--fast` 1–10% deterministic sample for "time blindness"; give each agent its own failing target; add a de-duplication role. New features "frequently broke existing functionality" until CI enforcement was added. | Our sim and test tooling copies these patterns: short output, `--fast` sampling, one failing test or level per agent, and a weekly dedupe/cleanup agent. | Anthropic: building-c-compiler |
| Multi-agent systems use about **15× the tokens of chat**. Vague delegation leads to duplicated or missed work. Prompts should state how much effort a task deserves. | Every issue states its objective, output, tools, boundaries and a size/budget class. | Anthropic: multi-agent research system |
| Claude Code averages about $13 per developer per active day and **$150–250 per developer per month** in enterprises. API organizations cap spend with **workspace spend limits**. | Planning baseline: about 4 always-on workers plus the Lead and reviewers comes to **about $2–5k a month** (estimate). | costs doc |
| MAST studied 1,600+ annotated traces and found 14 failure modes in 3 groups: spec issues, inter-agent misalignment, and task verification. Most were system-design faults, not prompt faults. | Fix failures structurally (specs, ownership, verifiers) instead of patching prompts. | MAST (search result only; unverified: fetch was blocked) |

---

## 2. Agent roster (production phase)

| # | Role | Model / runtime | Inputs → Outputs | Decides alone | Escalates to Lead | Escalates to Owner (via Lead only) |
|---|---|---|---|---|---|---|
| 1 | **Lead (Producer)** | Strongest model; interactive cloud session | Owner words, research docs → requirements, epics, issues, merges, weekly digest | Issue split and priority, assignment, merging green PRs, scope trades inside a milestone | — | Anything on the gate checklist, budget overrun over 20%, schedule slip over 1 week, pillar or theme change, anything legal |
| 2 | **Design agent** (game, level, economy data) | Strong; cloud session | GDD, sim reports → YAML/JSON content, GDD diffs, tuning PRs | Numbers within the agreed bands, level layouts, enemy waves | New mechanic, changing a band, any monetization touchpoint | Business model, pricing, anything paid |
| 3 | **Gameplay Engineers** ×1–3 | Mid/strong; cloud sessions in parallel | Ready issues → code, tests, PRs | Implementation inside the files it owns, refactors under 200 LOC | New dependency, architecture change, schema change | — |
| 4 | **UX/UI Implementer** | Mid; cloud session | Wireframes, UI spec → screens, golden screenshots | Layout inside the safe area, copy tweaks | New screen or flow, a change to one-thumb reach | Final store screenshots and icon |
| 5 | **Art & Audio Producer** | Mid + licensed generators | Art bible → assets plus a `LICENSES/assets.yaml` provenance row for each one | Variants inside the art bible | Style drift, a new tool or license | Art direction at G1/G2, any asset with unclear license (blocks the merge) |
| 6 | **QA / Playtest agent** | Mid; nightly scheduled task plus PR checks | Builds → bug issues, scripted playthroughs, screenshot diffs | Filing and labelling bugs, adding tests | Approving golden image updates jointly with UX/Art | — |
| 7 | **Balance Analyst** | Small/mid; nightly | Sim results → balance report, data-only tuning PRs | Tuning PRs that stay inside the bands | Out-of-band results 2 nights running | — |
| 8 | **Reviewer** (read-only, fresh context) | Strong; GitHub Action on every PR | PR diff, issue, DoD → APPROVE / CHANGES with severity | Verdict on correctness, tests, scope | Disagreement after 2 rounds | — |
| 9 | **Build & Release** | Mid; CI | main → signed builds, store tracks, compliance checklist | Internal test builds | Store submission content | Every public release, release keys, privacy and ads declarations |
| 10 | **Ops Steward** (this role) | Small; scheduled | Costs, CI stats, labels → budgets, loop alarms, CLAUDE.md upkeep, weekly dedupe/cleanup PR | Throttling, closing stale PRs, flipping kill switches at 100% of budget | Changes to guardrails | Raising the monthly envelope |

The pre-production research roles (Market Analyst, UX, Tech Architect, and others) fold into roles 2, 4 and 5 above, plus a Tech Architect agent kept on call for `arch:` issues. Rule: **no agent ever talks to the Owner directly; everything goes through the Lead.**

---

## 3. Workflow

```
Owner (chat) → Lead: Requirement Brief (REQ-nnn.md, ≤1 page, acceptance in Owner's words)
  → Lead: Epic issue + child issues (each passes Definition of Ready) → label status:ready
  → Worker cloud session claims (assignee + status:in-progress) → branch → commits
  → PR (template) → CI: lint · unit · schema · headless build · sim-fast · playthrough-smoke · screenshots · perf · license · size
  → Reviewer agent (fresh context, read-only) [+ Claude Code Review if on Team plan]
  → Auto-fix loop (≤3 attempts) → all green + Reviewer APPROVE → Lead squash-merges (merge queue)
  → Nightly: full sim + full playthroughs + device-farm smoke → QA files bugs → Lead triages
  → Monday: Owner digest
```

**Naming and conventions**
| Item | Convention |
|---|---|
| Branch | `agent/<role>/<issue#>-<slug>`, e.g. `agent/gameplay/142-lantern-reveal`. Branches started by a scheduled task may keep `claude/…` but must contain `<issue#>`. |
| Commit | Conventional Commits: `feat(towers): lantern reveal aura (#142)` |
| PR title | `[#142] feat(towers): lantern reveal aura`. Body: what/why, AC checklist with evidence, test list, sim/screenshot deltas, cost used, `Closes #142` |
| Labels | `type:` feature/bug/content/tech/chore/spike · `area:` gameplay/ui/art/audio/data/economy/build · `status:` needs-spec/ready/in-progress/in-review/blocked/needs-lead/needs-owner · `size:` S/M (L = must split) · `prio:` P0–P3 · `risk:high` (second reviewer plus Lead) · `loop:stuck` · `golden-update` · `agent:halt` |
| Merge | Squash only; linear history; `main` protected (required checks, no force-push, no direct push) |

**Definition of Ready (issue)**
1. A one-sentence player-facing goal, plus the REQ or GDD link.
2. Acceptance criteria written as a JSON/checkbox list, **each one mapped to a verification type** (unit / sim / playthrough / screenshot / manual-at-gate).
3. Files or directories owned are listed, with no overlap with any in-progress issue.
4. Size S (≤150 LOC) or M (≤400 LOC, excluding data and assets). Anything larger is split.
5. Dependencies are merged and the needed data schemas exist.
6. Budget class set: S ≤ $5, M ≤ $20 (per-issue cap, from Ops Steward telemetry).

**Definition of Done (PR)**
1. Every acceptance criterion is ticked with evidence (test name, sim delta, screenshot link).
2. New logic has tests, and the full suite is green.
3. Headless builds pass for Android (and iOS on the macOS CI runner).
4. No regressions in sim bands, perf budget or golden screenshots, unless `golden-update` is approved.
5. Reviewer returns APPROVE with no blocker or major findings.
6. Asset licenses are recorded, and the docs, CHANGELOG and issue progress log are updated.
7. The PR is merged and the issue is closed with a 3-line summary.

---

## 4. Owner gates

Each gate is a **single gate pack**: a page under `docs/gates/` plus a build link. The Owner answers **GO / GO-WITH-CHANGES / NO-GO**. The Lead prepares it at least 3 days ahead.

| Gate | Date | Checklist (every item needs evidence) | Owner decides |
|---|---|---|---|
| **G1 Concept** | Fri 18 Dec 2026 | ☐ One-page pitch, 3 pillars, Light-vs-Dark hook spec ☐ Market positioning and comps (no clones) ☐ Core loop and 10-level slice scope ☐ Wireframes for the core screens (portrait, one-thumb) ☐ Art bible plus 3 sample assets with proven license provenance ☐ Tech stack chosen, with a "hello build" proving headless Linux CI ☐ Business model recommendation ☐ Roadmap, budget envelope, top-5 risks | Go to production, title direction, art direction, monthly budget |
| **G2 Vertical Slice** | Fri 14 May 2027 | ☐ 10 levels, 6 towers, 1 hero, 8 enemies, 1 boss, playable start to finish on an Owner device (TestFlight / Play internal) ☐ World-1 art and audio at final quality ☐ FTUE complete ☐ Balance bots: every level inside its win-rate band, no dominant tower (>35% usage share) ☐ 0 crashes across 1,000 bot runs; perf ≥ the Tech Architect's target on a reference mid-tier Android ☐ Save/load, settings, accessibility basics ☐ Analytics event spec ☐ Owner plays 3 levels and notes anything not fun | Is it fun? Commit to full production scope and the soft-launch plan |
| **G3 Soft Launch** | Fri 20 Aug 2027 (go-live about Mon 30 Aug) | ☐ Content count per Economy plan ☐ Economy on remote config, rewarded ads with consent flows, IAP/pass tested in sandbox ☐ Store policy compliance: privacy labels and Data safety, age rating, ads/kids rules ☐ Crash reporting and KPI dashboards live ☐ Closed beta done (Google Play's closed-test requirement for new accounts: unverified, Release agent to confirm) ☐ Store listing, rollback and hotfix runbook ☐ All asset licenses audited | Markets, store text and icon, UA test budget, go-live |
| **G4 Launch** | about Fri 19 Nov 2027 (KPI-driven) | ☐ D1/D7/D30 retention, crash-free sessions, rating and ARPDAU against targets from the Economy and Market docs ☐ LiveOps calendar for 8 weeks ☐ Scale-up plan and budget | Global launch, or another iteration |

**Weekly Owner digest** (scheduled task, Monday morning, ≤1 screen, posted to the Owner channel):
```
HOLLOWGUARD — Week 49 · Phase P1 Foundation · Next gate: G2 in 23 wks   Status: 🟢/🟡/🔴
1. Shipped (≤5 lines, player-facing): …                      ▶ Build: <link> (play 2 min: level 3)
2. Next week (≤3 lines): …
3. Needs you (0–2 items, each a yes/no or A/B, with default if no reply in 72h): …
4. Health:  Merged PRs 31 · Open 6 · Stuck 1 · CI green 94% · Sim bands 9/10 · Crashes 0
5. Spend:   $780 / $3,000 month (26%) · forecast $2,900 · top cost: gameplay-eng
6. Risks (top 2, trend ↑↓): …
```

---

## 5. Quality guardrails

| Guardrail | Rule |
|---|---|
| **Tests** | Game rules live in a pure, deterministic, seeded simulation core, separate from rendering. Every PR that touches logic adds or updates unit tests. Test output is ≤20 lines on stdout, details go to `artifacts/*.log`, and failures print `ERROR <reason>` on one line (C-compiler pattern). |
| **Balance-sim bots** | Three bot policies (greedy builder, random-valid, search-based "expert") play every level × 200 seeds at maximum speed. They produce win rate, lives lost, gold curve, tower usage share and time to clear. Each level has bands, for example expert ≥ 95% win and greedy at 40–80%. `make sim-fast` runs a deterministic 10% sample on every PR, and the full run happens nightly. |
| **Automated playtest** | Scripted input playthroughs (tap and drag recorded as JSON) for the FTUE, each level's golden path, the shop and settings. They run headless against the real game build. Nightly, a vision-capable QA agent plays 3 random levels from screenshots and files UX bugs. Those findings are advisory only, never a merge gate. |
| **Regression screenshots** | Golden PNGs at fixed seed and frame across 3 portrait resolutions (small phone, tall phone, tablet), with a per-pixel tolerance. Goldens change only in PRs labelled `golden-update`, approved by QA plus the UX or Art agent and shown in the digest. |
| **Perf / size** | Frame-time and memory budget on a reference scene, plus build size. A CI failure fires if any of them regresses more than 5%. |
| **Assets/legal** | A merge is blocked for any asset with no provenance row (tool, license, prompt or source, date). A license allowlist is checked in CI. |
| **Cost controls** | Per run: `--max-turns 40`, a 45-minute job timeout. Per issue: the S/M budget cap. Concurrency: ≤4 worker sessions and ≤1 nightly batch. API workspace spend limit = monthly envelope. Alerts go out at 50%, 80% (Lead limits work to P0–P1) and 100% (non-P0 stops). Cheaper models handle triage, the sim analyst and the digest. Agent teams stay off by default. |
| **Kill switches** | **KS1** Repo variable `AGENTS_ENABLED=false`, which every agent workflow checks in its `if:`. **KS2** Pause all scheduled tasks. **KS3** Lower the workspace spend limit to $0. **KS4** The `agent:halt` label on an issue or PR stops work on it. Release keys sit behind a GitHub environment that needs manual Owner approval. |
| **Hard enforcement** | PreToolUse hooks block agents from editing `.github/workflows/`, `CLAUDE.md`, `.claude/`, `LICENSES/`, goldens and `tests/**` deletions unless their role is allowlisted. Agents get no secrets. Branch protection plus required checks on `main`. |
| **Anti-loop** | (1) A PR gets **3 automated fix attempts**, then it is labelled `loop:stuck` and the Lead re-specifies, splits or reassigns it. (2) An issue gets **2 fresh sessions** at most before re-spec (docs: after 2 failed corrections, start fresh with a better prompt). (3) `allowed_bots` is empty except the Lead app, and only the Lead may `@claude`. (4) A PR with no green build in 48h is closed automatically and its issue returned to `ready`. (5) A "failed approaches" section in each issue's progress log is mandatory reading for the next session. (6) A PR that deletes or weakens assertions gets `risk:high` and needs Lead sign-off. (7) Ops Steward alarm: the same file touched by 3 or more PRs in a week, or the same CI failure seen 3 or more times. |
| **Reviewer quality** | The Reviewer prompt is tuned to be skeptical, uses severity levels, and says "skip style nits": a reviewer asked to find problems always finds something, so fixing every nit leads to over-engineering. Each week, Ops samples 3 merged PRs and back-checks whether bugs escaped review. |

---

## 6. Roadmap (today: Mon 23 Nov 2026)

| Phase | Dates | Duration | Key deliverables | Exit criteria |
|---|---|---|---|---|
| **P0 Pre-production** | 23 Nov → 18 Dec 2026 | 4 wk | Research docs 01–07, GDD v1, wireframes, art bible, stack decision, repo bootstrap (CLAUDE.md, agents, CI skeleton, hello-build) | **G1 Concept GO** |
| **P1 Foundation & greybox** | 21 Dec 2026 → 5 Feb 2027 | 7 wk (light over holidays) | Deterministic sim core, data schemas, 1 greybox level, 2 towers, 3 enemies, light/dark mechanic, sim bots v1, screenshot and playthrough harness, all CI checks live | **M1 (Lead sign-off):** greybox level beatable by the expert bot, all checks green 5 days running. The Owner gets a build in the digest; this is not a gate. |
| **P2 Vertical slice** | 8 Feb → 7 May 2027 | 13 wk | Full slice scope, world-1 final art and audio, FTUE, hero, boss, UX polish, analytics spec | **G2 Vertical Slice GO** (14 May) |
| **P3 Soft-launch readiness** | 17 May → 13 Aug 2027 | 13 wk | Content to plan, economy and remote config, ads/IAP/pass, compliance, LiveOps tooling, closed beta from 12 Jul | **G3 Soft Launch GO** (20 Aug) → live about 30 Aug |
| **P4 Soft launch & iterate** | 30 Aug → mid-Nov 2027 | about 11 wk | Weekly KPI-driven updates, A/B tests via remote config | **G4 Launch** decision (about 19 Nov) |

Buffer: each phase carries about 15% slack. A slip of more than 1 week goes to the Owner in the digest's "Needs you" section, not by any other route.

---

## 7. Draft `CLAUDE.md` for the game repo

```markdown
# Hollowguard (working title) — agent conventions
Portrait, one-thumb mobile tower defense by Salted Caramel Owl. Agents do all work; one human Owner approves at gates.
Read @docs/gdd/README.md for game rules and @docs/process/workflow.md for the full process.

## Golden rules
1. One issue → one branch → one PR. Never work without an issue in `status:ready` assigned to you.
2. Work on ONE acceptance criterion at a time; commit when it passes. Never one-shot a feature.
3. Never claim done without evidence: test names, `make sim-fast` delta, screenshot diff links in the PR.
4. Never delete, skip, or loosen a test/assertion/golden to make CI pass. If a test is wrong, say so in the PR and label `risk:high`.
5. Stay inside the files listed in your issue. Need others? Comment on the issue and label `status:needs-lead`.
6. You never contact the Owner. Escalate to the Lead with `status:needs-lead` + a one-paragraph question offering options A/B.
7. No clones of existing games (names, art, levels). No asset without a row in `LICENSES/assets.yaml`.

## Commands (stable interface — always use these, not engine CLIs directly)
- `make setup` — install toolchain (idempotent)
- `make test` — unit tests (≤20 lines stdout; details in artifacts/test.log; failures print `ERROR <reason>`)
- `make sim-fast` — deterministic 10% balance sample; `make sim` — full (nightly only)
- `make play-smoke` — scripted headless playthroughs
- `make shots` — render goldens and diff; `make shots-update` only on `golden-update` PRs
- `make build-android` — headless build; `make lint` — format + lint + schema validation
- `make ci` — everything CI runs, in order. Run it before opening/updating a PR.

## Layout
- `sim/` pure deterministic game rules (no rendering, no wall-clock, seeded RNG only)
- `game/` engine/presentation layer; reads data, calls `sim/`
- `data/` all content as YAML/JSON (towers, enemies, waves, levels, economy); schemas in `data/schemas/`
- `tests/` unit + playthrough scripts; `goldens/` reference screenshots
- `tools/` sim bots, screenshot diff, license check; `docs/` GDD, ADRs, gates, progress

## Content & code rules
- Gameplay numbers live in `data/`, never hard-coded. Balance changes are data-only PRs.
- `sim/` must stay deterministic: same seed + inputs → same result. No floats in persistence; use fixed-point helpers.
- Portrait only; all touch targets ≥ 48dp and within the bottom 60% of screen unless spec says otherwise.
- New dependency or architecture change → write an ADR in `docs/adr/` and get Lead approval first.
- No network calls, analytics, ads or IAP code outside `game/services/` adapters.

## Git
- Branch: `agent/<role>/<issue#>-<slug>`. Commits: Conventional Commits ending `(#<issue>)`.
- PR title `[#<issue>] <type>(<area>): <summary>`; fill the PR template completely; ≤400 changed LOC excluding data/assets.
- Never push to `main`, never force-push shared branches, never edit `.github/workflows/`, `.claude/`, or this file (Ops Steward only).

## Session discipline
- Start: read the issue, its progress log comment, "Failed approaches", and `git log -15`.
- End (or before context gets long): update the issue progress log (done / next / failed approaches) and push.
- Max 3 fix attempts on a red PR; then label `loop:stuck`, summarize what you tried, stop.
- Respect `agent:halt` immediately. Keep tool output small; write logs to `artifacts/`.

## Definition of Done
All AC ticked with evidence · tests added and `make ci` green · no sim-band, perf, or golden regressions ·
licenses recorded · Reviewer APPROVE (no blocker/major) · CHANGELOG + progress log updated.
```

---

## Recommendations (decisive)
1. **Adopt the issue→branch→PR pipeline with GitHub as the only coordination bus.** Don't use experimental agent teams for production work. Revisit them at G2.
2. **Build the verifiers before the content.** In P1, the sim core, the 3 bots, playthrough scripts and screenshot diff all ship before the second tower.
3. **The Reviewer is always a separate, read-only, fresh-context agent.** Add Claude Code Review only if we're on a Team plan, and set its own spend limit.
4. **Set the monthly agent envelope at G1** (proposal: $1.5k in P0–P1, $3–5k in P2–P3) and wire KS1–KS4 before any autonomous run.
5. **Keep CLAUDE.md under 200 lines.** Everything that must not happen goes in hooks and branch rules.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Agents "pass the tests" without fun or quality (C-compiler warning: tests pass ≠ done) | High | Owner fun check at G2, a vision playtest agent, and design criteria graded by a separate agent |
| iOS builds need macOS/Xcode, which conflicts with "Linux container only" | High | Agents work in Linux; only the signed iOS build runs on a macOS CI runner. Tech Architect to confirm. |
| Preview features change (scheduled tasks, agent teams) | Medium | Core pipeline uses GitHub Actions plus cloud sessions. Scheduled tasks are only used for convenience jobs. |
| Cost spikes from parallel or looping agents (multi-agent ≈15× tokens) | Medium | Turn, timeout, issue and workspace caps, plus the anti-loop rules in §5 |
| Merge conflicts or duplicate work between parallel workers | Medium | File ownership in the Definition of Ready, ≤4 workers, merge queue, weekly dedupe agent |
| Single-account ownership (scheduled tasks and GitHub app tied to the Owner's account) | Low/Med | Document all of them in `docs/process/automation.md`, and make KS2 a single toggle |

## Open questions for the Owner
1. **Monthly agent budget ceiling:** is $3–5k a month during production acceptable, or should we plan to a lower cap (which means slower phases)?
2. **Plan type:** will the studio run on a Claude Team plan (enables Claude Code Review and shared cloud environments) or on an individual plan plus an API key?
3. **Digest channel and time:** where do you want the Monday digest (email, Slack, GitHub issue), and in what time zone?

## Sources (retrieved this session)
- https://code.claude.com/docs/en/sub-agents.md
- https://code.claude.com/docs/en/agent-teams.md
- https://code.claude.com/docs/en/claude-code-on-the-web.md
- https://code.claude.com/docs/en/cloud-environments.md
- https://code.claude.com/docs/en/routines.md
- https://code.claude.com/docs/en/github-actions.md
- https://raw.githubusercontent.com/anthropics/claude-code-action/main/README.md
- https://code.claude.com/docs/en/code-review.md
- https://code.claude.com/docs/en/code-review-costs.md
- https://code.claude.com/docs/en/memory.md
- https://code.claude.com/docs/en/hooks-guide.md
- https://code.claude.com/docs/en/best-practices.md
- https://code.claude.com/docs/en/costs.md
- https://www.anthropic.com/engineering/building-c-compiler
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/engineering/harness-design-long-running-apps
- https://www.anthropic.com/engineering/multi-agent-research-system
- Unverified (seen in search results only; fetch blocked by network policy): MAST, https://arxiv.org/abs/2503.13657v3 · Google Play closed-testing requirement for new developer accounts
