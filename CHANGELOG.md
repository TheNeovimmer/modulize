# Changelog

All notable changes to modulize are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-11-06

The first public release.

**The skill**
- Six-phase workflow: safety net → ask → map → list every problem → redesign from first principles → fix → verify and loop.
- Full problem taxonomy (`skills/modulize/catalog.md`): hidden links, needless links, surplus code, and the special-case grep set — each with how it's found and the senior fix.
- Triage model: leverage × blast radius × risk, with verdicts Fix now / Fix with another / Note and leave / Ask the user.
- Evidence rules: git churn hot-spots, import-direction audit, fresh-eyes subagent sweep, cycle-until-clean termination.
- Decision log with fix-above-problem entries; behavior preserved apart from logged bug fixes.
- Anti-rationalization table and red-flag stop conditions baked in.
- User-invoked (`/modulize`), zero always-on context cost. Installs via `npx skills add TheNeovimmer/modulize`.

**The repo**
- README with one-command install, per-agent instructions and an honest FAQ.
- `docs/why.md` — the argument for the skill.
- `examples/sample-run.md` — a condensed end-to-end run.
- CI validation of the skill's structure on every push.

[1.0.0]: https://github.com/TheNeovimmer/modulize/releases/tag/v1.0.0
