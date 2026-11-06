---
name: modulize
description: Whole-codebase refactor skill for AI agents. Hunts leaky abstractions, copy-paste, temporary workarounds and useless wrappers — then redesigns the system from first principles.
disable-model-invocation: true
argument-hint: "[optional area or concern to focus on]"
---

# Modulize

**Say goodbye to messy code.**

Modulize asks one question of everything in the repository — *should these pieces change together?* — finds every place the answer is wrong, redesigns the system from first principles, and fixes it all. Behavior stays identical apart from logged bug fixes.

**What you get**

- **A change that lands in one place** — not five folders by layer; a finished feature is a slice, not a scavenger hunt
- **A full catalog of the messes** — hidden links, needless links, surplus code and special cases — every entry triaged by leverage, blast radius and risk
- **A decision log worth reading** — every fix written above the problems it solves; the one behind many
- **A pass that doesn't stop at "good enough"** — it loops until a fresh-eyes sweep finds nothing worth fixing

The named enemies: leaky abstractions, copy-paste, temporary workarounds, useless wrappers. The full taxonomy lives in [catalog.md](catalog.md).

## Principles

1. **Zero special cases is the goal.** Every `if` for one value, swallowed exception, sleep or disabled test is a requirement the design never accounted for. You don't clean them up one by one; you design the system that doesn't need them, and what's left keeps a recorded reason.
2. **One fix behind many problems.** Never patch problem by problem. Find the single change that makes a whole cluster of problems impossible, and make it.
3. **Behavior is sacred.** The refactor changes structure, not intent. Apart from bugs it fixes — all logged — intended behavior when you start equals intended behavior when you finish.
4. **Evidence over taste.** Git history, imports, greps and tests decide. "It feels cleaner" never justifies a change; "these two changed together in 14 of the last 20 commits" does.
5. **Leave it better, prove it works.** Every fix ends in a green suite and a decision log entry. If you can't state why a change was safe, it hasn't happened.

## Phase 0 — Safety net (always first)

Nothing gets edited before the net is in place. In order:

1. **Tree state.** Commit or stash pending changes with the user's git conventions. If the tree is dirty and the user didn't ask you to touch those files, stop and ask.
2. **Baseline.** Detect the project's test command (`package.json` scripts, `Makefile`, CI config, `Cargo.toml`, `go.mod`) and run it. Record the result. Pre-existing failures go in the log under **Baseline failures** — they are not yours, and chasing them is out of scope unless asked.
3. **No baseline possible?** If the project has no tests at all, stop and ask the user how behavior should be verified before editing anything: a snapshot harness, a list of golden paths to exercise by hand, or a mandatory pair of refactor + test. Do not proceed blind.
4. **Hot spots.** If this is a git repo with history, rank files by churn:

   ```bash
   git log --since='12 months' --name-only --format= | sort | uniq -c | sort -rn | head -30
   ```

   These paths are where fixes pay back most; weight them first in phases 2–4.
5. **Decision log.** Create it and keep it: `LOG="${TMPDIR:-/tmp}/modulize-$(date +%Y%m%d-%H%M%S).md"`. Every phase writes into it. It survives compaction, and it's the report at the end.

## Phase 1 — Ask (one question, besides scope)

If the user invoked you with an area argument (e.g. `/modulize checkout`), scope is set — confirm it in one sentence and move on.

Ask exactly one question about the two optional additions. Present them with these exact descriptions:

- **Comments** — Remove comments that only restate the code, even when they read as a "why". Keep comments about something outside the code (`// the proxy drops websockets, so we poll`). Workaround comments (`// wait 100ms because the cache isn't ready yet`) go when the redesign removes the problem behind them.
- **Tests** — Remove tests that wouldn't catch a real bug and rewrite internals-coupled tests to depend on behavior. Done in Phase 5, never before: tests are the regression safety net.

Do only what the user picks. If they pick neither, that's a valid answer — say so and continue.

## Phase 2 — Map the codebase

You cannot redesign what you can't see whole. Do all three:

1. **Skeleton.** Produce a digest of the codebase with the bodies stripped — imports, exports, public signatures, types — so the whole thing fits in context. Use a structural tool if one exists (`ctags`, a tree-sitter query, the language server); otherwise read the files and write the surface down. The skeleton is your map, not a replacement for reading critical files as you touch them.
2. **Import graph.** Script it with whatever fits the ecosystem — `npx madge --circular`, `npx dependency-cruiser`, `go list -deps ./...`, `cargo` + `cargo-modules`, or a small ad-hoc script. Record: dependency cycles, layer violations, and any module imported by everything (candidate shared ground — or candidate god module).
3. **Subagents, in parallel, fixed briefs.** One lens each, evidence only, no fixes:

   > **Brief:** Read the paths I give you. Return bullet points with `file:line`, each anchored to one of: (a) duplicated logic or values — closest matches and copy count; (b) circular imports, wrong-direction imports, deep reach into another module's internals; (c) swallowed errors, sleeps or retries, disabled tests, `TODO`/`FIXME`/`HACK` markers, `any` casts and `@ts-ignore`; (d) unreferenced exports and wrapper modules that only forward calls. Do not propose fixes. Do not read outside the given paths. Report nothing you cannot point to.

   Split paths so lenses don't overlap (e.g. by top-level directory). You own every decision; subagents only gather evidence. Deduplicate their findings before writing the log.

## Phase 3 — List every problem

Read [catalog.md](catalog.md) now if you haven't — it defines the three ways code gets this wrong, every named mess to look for, and the special-case grep set.

Ask one question of every pair of pieces of code: **should these change together?** Write down every place the answer is wrong, in the log, as raw problem entries — no fixes yet:

- **Hidden links** — must change together; nothing in the code says so.
- **Needless links** — change for different reasons; tied anyway.
- **Surplus** — no reason of their own to change at all.
- **Special cases** — one-off code for one situation. (Grep set in catalog.md.) Every special case is a requirement the design never accounted for — record it as such, because it's evidence for Phase 4.

Then triage each problem in the log:

| Verdict | Meaning | What happens |
|---|---|---|
| **Fix now** | Low risk, or high leverage | Executed in Phase 5, leverage first |
| **Fix with another** | Only worth doing as part of a bigger fix | Tagged with the fix it rides with |
| **Note and leave** | Real, but fixing pays nothing (or the risk is the user's call) | Log entry with the reason; code untouched |
| **Ask the user** | Requires a behavior, API, data or security change | Parked until the user decides |

Leverage comes first: a fix that erases twelve problems outranks ten cheap ones. Risk comes first for order: money, auth, permissions, migrations and data loss never ride along in a structure commit.

No problem goes unlisted, and none gets silently dropped — if it's not worth fixing, it gets "Note and leave" with a reason. Completeness of the list is the deliverable of this phase.

## Phase 4 — Redesign from first principles

Work out the fixes as if the system had known today's requirements from the start. **Do not fix problems one by one.** Find the one fix behind several problems — it often looks nothing like them (the fix for a focus bug, a swallowed flag and a 100ms sleep is usually "the dialog restores focus, full stop").

Hold every candidate fix to three tests:

1. **Change-together test.** The pieces that change together end up together.
2. **Untied test.** The pieces that don't change together end up untied — no shared internals knowledge.
3. **Volatility test.** Nothing depends on something more volatile than itself; shared ground is pushed down, never sideways.

And the deletion test for any suspected shallow module: delete it in your mind's eye. If callers are left holding the same complexity explicitly — it was transparent; the code it hid is still required, just relocated. If nothing breaks and the code falls into a simpler shape — it earned nothing; inline it.

Write the fixes in the log, **above** the problems they solve, in this shape:

```markdown
- Define a `PaymentProvider` interface that Stripe and PayPal implement, so checkout
  and refunds translate one shape instead of branching per provider.
  - `checkout/submit.ts:9` depends directly on `payments/stripe.ts`.
  - `refunds/refund.ts:22` wraps every call in `if (order.provider === "paypal")`.
```

Delete the special cases the redesign makes unnecessary. Keep the ones the system still needs, and record beside each kept one the reason it stays. Special cases left without a reason are unfinished work; special cases invented during the refactor are failures.

Fixes only leave this phase when every listed problem is either attached to a fix, parked as "Ask the user", or carries a written "Note and leave" reason.

## Phase 5 — Fix

In leverage order, one concern per commit (`refactor: <what and why, one line>`), suite green between commits. If the suite goes red, check it against the Baseline failures list: yours gets fixed; pre-existing stays red and stays listed.

- A fix that would change observable behavior — function signatures used across package boundaries, error modes, output formats, migrations — stops and becomes an "Ask the user" entry, even mid-phase.
- Drive-by fixes don't ride along; they get their own entry and commit.
- Comments, if the user chose them: comments restating the code are removed, even phrased as a why; comments about something outside the code stay; workaround comments die with the workaround.
- Tests, if the user chose them — **last, always**, after the structure is done: internals-coupled tests are rewritten against behavior (which changes least); tests that repeat the implementation are deleted; tests that can't fail are deleted. The suite is the regression net — don't tear holes in it mid-refactor.
- Do not go hunting for new bugs. A structural fix may expose some; log them, fix them in their own commits, mark them **Bug** in the log.

## Phase 6 — Verify, and loop until done

One pass is never enough. Repeat until the log stops growing:

1. **Fresh-eyes sweep.** New subagents, same briefs as Phase 2. New findings go back to Phase 3 — unless they're "Note and leave" calibre, which get logged as such.
2. **Import audit.** Nothing imports anything more volatile than itself. Script the layers (domain core < infrastructure < providers; adjust to the repo) and list every reverse edge. Each one is a finding, or a waiver with a reason.
3. **One-place check.** Pick two or three representative changes — from the churn list, the open issue tracker, or ask the user. Trace where each would land. Each must land in one place. If not, the refactor missed a seam; back to Phase 3.
4. **Suite vs baseline.** Same or better. No new failures. List the delta explicitly.
5. **Special-case count.** Count what's left. Each one carries a recorded reason. This number is the honest measure of how done this is — drive it down.
6. **Report.** Summarize from the log: what changed, commits, bugs fixed, tests status, remaining special cases and why, what you deliberately did not touch. Put the decision log path at the top.

## Exit criteria

All of these, or you're not done:

- Every log entry is attached to a fix, parked as "Ask the user", or carries a written reason to leave it.
- Special cases remaining: as few as the codebase supports, each justified.
- A typical change lands in one place — demonstrated on two or three traced examples.
- Import audit clean or waived with reasons.
- Suite ≥ baseline; delta stated; nothing unverified claimed as passing.
- Fresh-eyes sweep found nothing worth fixing, or the remainder is logged as "Note and leave".

## Red flags — stop and ask the user

- A fix wants to change behavior, a public API, a data format or a migration.
- The baseline can't run, or isn't green enough to trust a comparison.
- Money, auth, permissions or data-loss risk enter the diff.
- The loop is not converging — each sweep finds a new layer of the same problem class. Pause; present what you have; ask whether to keep going or narrow scope.
- Something in the repo contradicts the user's stated goals (dead code being load-bearing, a disabled test guarding a known bug).

## Anti-rationalization

| The excuse | The rebuttal |
|---|---|
| "Too many problems to catalog properly." | The catalog is the deliverable. A missed entry is a bug you shipped on purpose. |
| "This wrapper is harmless." | Harmless is irrelevant — it has no reason to change, so it leaves. If it has a reason, write it down. |
| "I'll fix the special case directly, it's quick." | Every quick fix here is a requirement the design refused to account for. Fix the design; the case disappears or earns its entry. |
| "Tests are slow, I'll verify at the end." | The suite runs between commits or you can't tell what broke. Baseline failures are your license, not a shield. |
| "The subagents found nothing, we're done." | Verify the sweep's paths actually covered the changed areas — then Phase 6.1 still applies. |
| "This would change behavior, but only slightly." | Slightly is still a change. It becomes "Ask the user", every time. |
| "One big commit, it's all one thing." | One concern per commit. Reviewers and `git bisect` are not optional extras. |
| "Someone else's mess — not in scope." | It's in the log. Scope decides whether it's fixed now — not whether it's seen. |

## Done looks like

A developer opens a task and finishes it without grep-ing five folders. A caller never learns an implementation detail. Nothing in the repo changes when its neighbor does. And the next agent — or human — finds the system boring, in the best way.
