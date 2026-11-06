# Why agents fail in tangled codebases — and why this skill exists

Agents don't fail at writing code. They fail at writing code *into tangled places* — and then inherit the tangle as their new normal.

Every tangle shares one root question, asked of no piece of code in particular: **should these pieces change together?** Structure is nothing but the accumulated answer. modulize audits the answer everywhere and rewrites the code until it's consistent.

## The three ways code gets it wrong

**Hidden links.** Pieces that must change together, where nothing says so:
copies of logic and values; a module that reads a global set by another; a feature chopped up by layer, or scattered by convention; a call order only the brave learn. Change one half and the other half breaks in silence.

**Needless links.** Pieces tied together that change for different reasons:
callers reaching past a module's interface; stable code importing something volatile; a general function carrying a knob only one caller understands; the shallow module whose interface breaks every time its implementation does.

**Surplus.** Pieces with no reason of their own to change:
wrappers that only forward calls, extension points configured for a future that never arrived, code nobody calls but everyone fears to delete.

## Special cases are the interesting part

A codebase littered with `if` for one value, retries, sleeps and disabled tests isn't merely untidy — it's *unfinished business*. Each special case is a requirement the design never accounted for, which is why nobody knew where to put it. modulize doesn't delete them one by one; it asks what the system would look like if it had known, builds that, and lets the cases fall. The ones that remain carry written reasons.

## Modular, defined operationally

Not "many files". Not "clean architecture, well, the diagram". Concretely:

1. **Pieces that change together live together.** A feature is a slice, not five files in five folders.
2. **Pieces that change apart don't know each other.** Direction points from volatile to stable, and seams are owned by the stable side.
3. **A typical change lands in one place.** If yours doesn't, your module boundaries are story, not structure.
4. **Everything depends on what changes less.** The reverse is how a one-line bug fix drags half the repo.
5. **Nothing changes without a reason to change.** No wrappers, no speculation — the change log is the design.

## Why this pays off for agents

- **Context is finite.** An agent that can see the whole codebase as ~a hundred public surfaces reasons globally instead of guessing locally.
- **Verification scales locally.** In a deep module, tests through the interface prove the whole thing; at a tangle, nothing proves anything until the diff breaks production.
- **Failures become loud, early and local.** Tangled code fails anonymously and far away. Modular code fails at the seam, on the change that caused it.
- **Review becomes rare and easy.** A typical diff is one file's behavior plus its tests — the reviewer can actually hold it.

## What the skill does, briefly

Safety net first, always: clean tree, baseline suite, checkpoint. Then evidence: skeleton, import graph, subagents with fixed briefs. Then the list — every hidden link, needless link, surplus and special case, triaged by leverage, blast radius and risk. Then the redesign, not the patch. Then one-concern-per-commit, suite green between. Then it loops until a fresh-eyes sweep finds nothing worth fixing — and the decision log says exactly what moved and why.

Read [the catalog](../skills/modulize/catalog.md) for the full taxonomy, or [the sample run](../examples/sample-run.md) to see it end-to-end.
