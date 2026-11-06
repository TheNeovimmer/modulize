# Contributing to modulize

Thanks for wanting to make the skill better. The bar is high because agents act on this file.

## What a change needs to be

- **Specific** — actionable steps and exit criteria, not advice ("think carefully about coupling" is rejected; "split along the reasons to change; if you can't name them, map first" merges).
- **Verifiable** — every step has a completion criterion an agent can check.
- **Battle-tested** — grounded in a real run, not a hunch. Tell us the codebase where you saw the mess.
- **Minimal** — only what's needed to steer the agent. No padding, no speculative sections, no duplicated meaning.

## How to propose a change

1. Open an issue describing the miss or the mess class you saw in the wild. Include file:line from a real repo (private is fine — describe it).
2. Small fixes (wording, broken step, wrong example): a PR directly.
3. New mess classes in `catalog.md`: pick the right wrongness (hidden / needless / surplus / special case) — if you can't, that's a sign it's not one mess but two.

## What gets rejected

- Vague aspirations, style preaching, or "best practices" with no exit criterion.
- Content an agent already obeys by default — it pays load to say nothing.
- Duplicating something already in the docs under a new name.
- Features of the skill that nobody asked for and nothing exercises.

## House rules

- MIT, in and out: contributions are licensed under the same MIT as the repo.
- Keep the user-invoked contract: `disable-model-invocation: true` stays.
- The skill never claims verification it didn't run. If a step can't be checked, it doesn't count as done.
- One voice: confident, direct, senior. No hedging, no fillers.
