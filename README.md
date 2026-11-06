<h1 align="center">modulize</h1>

<p align="center"><strong>Say goodbye to messy code.</strong></p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-0A0A0A.svg"></a>
  <a href="CHANGELOG.md"><img alt="Release 1.0.0" src="https://img.shields.io/badge/release-1.0.0-0A0A0A.svg"></a>
  <a href="https://skills.sh/TheNeovimmer/modulize"><img alt="skills.sh" src="https://skills.sh/b/TheNeovimmer/modulize"></a>
  <img alt="Works with any Agent Skills agent" src="https://img.shields.io/badge/agent%20skills-compatible-0A0A0A.svg">
</p>

**modulize** is a whole-codebase refactor skill for AI coding agents. It asks one question of everything in your repository — *should these pieces change together?* — finds every place the code gets it wrong, redesigns the system from first principles, and fixes it.

It goes after the named enemies: **leaky abstractions, copy-paste, temporary workarounds, useless wrappers** — and the structural messes underneath them: hidden coupling, needless coupling, surplus code, special cases.

> Typical output: a change that used to touch five folders now lands in one place, and nobody needs to know your codebase's folklore to work in it.

---

## Quick start

**Install for any agent, one command** — via the [open agent skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add TheNeovimmer/modulize
```

Then run `/modulize` in your agent, or `/modulize checkout` to scope to an area.

<details>
<summary><b>Other install methods</b></summary>

**Claude Code** — install as a skill; invoke with `/modulize`:

```bash
git clone https://github.com/TheNeovimmer/modulize.git
cp -r modulize/skills/modulize ~/.claude/skills/modulize
```

**OpenCode** — copy into your skills directory; the agent loads it with the skill tool:

```bash
cp -r modulize/skills/modulize ~/.agents/skills/modulize
# or project-local: cp -r modulize/skills/modulize .agents/skills/modulize
```

**Anyone else** — the skill is plain Markdown with YAML frontmatter. Copy `skills/modulize/` into wherever your agent loads skills from. Works with Claude Code, OpenCode, Cursor, Codex, Copilot, Cline and any [Agent Skills](https://agentskills.io)–compatible tool.

</details>

---

## The mess it removes

| Enemy | What it looks like | modulize's answer |
|---|---|---|
| **Leaky abstractions** | Callers must know call order, follow-up calls, error shapes it can't contain | Deepen the interface until the internals stop leaking — or inline it |
| **Copy-paste** | The same logic in five folders; strings repeated across files | One home, one name, N→1 |
| **Temporary workarounds** | Sleeps, retries, `// wait 100ms because…`, swallowed exceptions | Design the ordering the system actually has; the workarounds delete |
| **Useless wrappers** | Functions that only forward arguments and return the result | Delete; callers reach the real thing |
| **Hidden coupling** | Split by layer, global state, format knowledge in two places | Colocate by domain; one parser owns the shape; pass it in |
| **Needless coupling** | Callers on internals, stable code importing volatile code | Depend on what changes less; core owns the seam |
| **Special cases** | `if` for one value, one-caller parameters, disabled tests | Requirements the design never had — accounted for, not patched |

## When to reach for it

- A "quick fix" turns into editing five folders by layer
- "Temporary" workarounds, sleeps and swallowed errors have become load-bearing
- You inherited the codebase — from a person, or from an agent — and trust it less every week
- You want the deep refactor *instead* of the big-bang rewrite conversation

Not for: a one-file fix or a style nit — ask your agent directly. `/modulize` is for when the problem is the **shape of the codebase**, not the code in front of you.

## How it works

Six phases, executed with evidence, not vibes:

0. **Safety net** — clean tree, baseline test run, git checkpoint, churn hot-spots from `git log`
1. **Ask** — the only question up front, plus scope
2. **Map** — skeleton of the whole codebase, import graph, parallel subagents hunting each mess class
3. **List every problem** — hidden links, needless links, surplus, special cases — triaged by leverage, blast radius and risk
4. **Redesign from first principles** — fix root causes, not instances; every fix must pass the change-together, untied and volatility tests
5. **Fix** — one concern per commit, suite green between commits
6. **Verify** — fresh-eyes subagent sweep, import-direction audit, and a loop until nothing worth fixing remains

Behavior stays identical apart from logged bug fixes. git never guesses; `git log` tells you what changes together — and the design follows.

## What done looks like

- A typical change lands in **one place**
- **Every import points at something less volatile than itself**
- Special cases remain only where they carry a written reason
- Your test suite is **green — or the exact deltas are listed**
- A decision log you can actually read: every fix above the problems it solves

## See it in action

A condensed run — the mess on disk → the log → the redesign → the verification:
[**examples/sample-run.md**](examples/sample-run.md)

## FAQ

**Is it safe to run on my codebase?**
Yes. Your tree is committed or stashed first, the suite runs before anything is touched, commits land one concern at a time, and the suite runs between them. Intended behavior stays the same — bugs the refactor fixes are logged separately.

**Will it rewrite my whole codebase?**
It catalogs everything, then fixes by leverage under risk control. What it doesn't fix, it logs with a reason — nothing changes silently and nothing is silently skipped.

**How is this different from a linter or a code-review skill?**
Linters check syntax and style. Review skills check a diff. modulize checks **structure across the whole repo** — the thing neither of those can see.

**Why user-invoked (`/modulize`) and not automatic?**
It's a deep refactor, not an ambient annoyance — you decide when to pull that lever. No permanent context cost, no false triggers.

**Does it need internet or dependencies?**
No. It optionally uses what your repo already has (jscpd, madge, ctags); it works without them.

**Does it work on any language?**
Yes — it's language-agnostic. It leans on your repo's own test command, imports and tooling.

## Why this exists

Agents don't fail at writing code; they fail at writing code into tangled places — and then inherit the tangle. Read the full argument: [**docs/why.md**](docs/why.md). The skill itself is free (MIT) — the only payment is saying goodbye to your messy code.

## Contributing

Small fixes welcome; new mess classes welcome when they come with the senior fix. See [CONTRIBUTING.md](CONTRIBUTING.md). Changes must keep the skill **specific, verifiable, battle-tested and minimal**.

## Credit

Created by [TheNeovimmer](https://github.com/TheNeovimmer) — [theneovimmer.vercel.app](https://theneovimmer.vercel.app). MIT licensed.
