# The Modulize Catalog

Reference for **Phase 3 — List every problem** and **Phase 4 — Redesign from first principles**.

One question decides every entry here: **should these pieces change together?** There are exactly three ways to get it wrong — plus the special case, which is the design asking for a requirement it never had.

Every entry is: what it is · how you find it · the senior fix. "Delete" means delete — git remembers.

---

## Hidden links — must change together, nothing says so

### Copy-paste (logic or values)
- **What:** the same logic in N places; strings or numbers repeated across files.
- **Find:** `jscpd`, or `grep -rniE '<distinctive snippet>'`; for values, grep repeated literals of 4+ chars.
- **Fix:** one home — shared module or named constant. Change one place means change all by construction. N→1, then the shared piece gets a name a human would search for.

### Leaky abstraction
- **What:** using the module requires knowing its internals — call order, required follow-up calls, error shapes it can't contain, ORM rows leaking across boundaries.
- **Find:** ask of each module: *can a caller use this correctly without reading its source?* Every "no" is an entry.
- **Fix:** deepen the interface until the internals stop leaking (ordering, state, error policy move inside) — or delete the abstraction and inline. A leaky abstraction is worse than none: it charges rent and leaks anyway.

### Module reads something another module sets
- **What:** globals, files, env vars, singletons, shared mutable state set elsewhere. Change the setter, break the reader in silence.
- **Find:** grep `process.env`, `globalThis`, `fs.readFileSync` outside init/config, module-level mutable `let`.
- **Fix:** pass it in. If both sides need it, one owns it; the other receives it as an argument. Nothing loves a global — it just outlives every refactor.

### Feature split by layer across folders
- **What:** one user-visible change means touching `controllers/`, `services/`, `repositories/` — three files, zero domain naming.
- **Find:** pick your last five real changes; count the folders each touched. Two or more folders each time is the smoking gun.
- **Fix:** colocate by domain slice (vertical). Layers may exist inside a slice; they may not be the top-level skeleton.

### Call order / convention callers must know
- **What:** init before use, close before exit, method A then B — enforced by comments or hope.
- **Find:** grep `init()`, `setup`, `close`, `dispose`, `beforeEach` conventions; read every "must call this first" comment.
- **Fix:** encode it — constructor injection, required parameters, state machine, builder, or a single entry point. Make the wrong order unrepresentable, not documented.

### Format / schema coupling
- **What:** two modules both know the shape of one file, payload or protocol. The format changes; both break.
- **Find:** grep the distinctive field names of the format across the diff surface; two modules in different layers matching is the signal.
- **Fix:** one parser module owns the shape and produces typed values; everyone else consumes those. Parse at the boundary, once.

### Temporal coupling (init before use)
- **What:** half-built objects that only work after a second call; `new Foo(); foo.init()` patterns.
- **Fix:** required constructor arguments and complete objects. If construction is heavy or contextual, make `create()` synchronous and pure, or make invalid states unrepresentable.

### Knowledge lives only in comments
- **What:** invariants, orderings and "don't do X" rules that exist nowhere but `// don't do X`.
- **Fix:** if it's code-shaped, make it code. If it's an outside-the-code fact (the proxy drops websockets), keep the comment. If nobody outside and nobody inside can violate it anymore, the comment retires with the problem.

---

## Needless links — change for different reasons, tied anyway

### Callers depend on internals
- **What:** imports of deep paths, private members, mutable fields — things an author would rename freely.
- **Fix:** narrow the interface at the seam; hide the guts; export exactly what's meant to persist.

### Stable imports something volatile
- **What:** your core business rules import a provider SDK, a fetch client, a date library wrapped ad hoc — anything that changes for reasons that aren't yours.
- **Fix:** invert the arrow — the volatile side depends on a narrow core-defined port (an interface the core owns); adapters implement it. If you can't, push shared ground down until both sides depend on stable ground instead of each other.

### A parameter only one workflow understands
- **What:** `save(doc, { skipNotifications, asDraft, fromImport })` — general function, one caller's vocabulary.
- **Fix:** split the function or the workflow; move the caller-specific knob behind its own type or into the caller. General code speaks no dialect.

### Shallow module
- **What:** interface nearly as complex as implementation — callers change when internals change.
- **Find:** the deletion test: *would deleting it concentrate complexity into fewer places, or scatter it?* Concentrate → fewer modules, deeper ones. Scatter → the interface is fake; deepen it or inline it.
- **Fix:** fold behavior in behind the seam, or inline the module and admit there was never a module there.

### God module
- **What:** three or more unrelated reasons to change (three teams, three concerns, three rates of change). Every PR touches it; every rebase fights it.
- **Fix:** split along the reasons to change, not along technical layers. If you can't name the reasons separately, you don't understand it yet — map it first.

### Circular imports
- **What:** A imports B imports A. Build tools tolerate it; humans can't reason about it; module-level side effects love it.
- **Fix:** extract the shared ground into a lower module, or invert one edge (event, callback, injected dependency). Never silence it with a re-export.

### Inheritance used for reuse / coupling
- **What:** base classes carrying shared behavior "for convenience" — children coupled to every future change in the parent.
- **Fix:** composition, or an adapter at a real seam. Inheritance encodes "is-a"; if the record can't say that honestly, it doesn't inherit.

---

## Surplus — no reason of their own to change

### Pass-through wrapper
- **What:** a function/class/module that forwards arguments and returns the result untouched; adds a name, nothing else.
- **Fix:** delete it; callers use the wrapped thing directly. If it earned a name, move the name; if it earned policy, it wasn't a wrapper.

### Speculative generality
- **What:** options, strategies, plugin hooks, config for things that never vary — built for a future that didn't arrive.
- **Fix:** collapse to the one real case. One real choice beats five pretend ones; re-adding flexibility later costs nothing like maintaining fake flexibility costs now.

### Dead code
- **What:** unreferenced exports, unreachable branches, unused dependencies, flags nobody toggles, features disabled in every config.
- **Find:** unused-exports tooling (`ts-prune`, `knip`, `vulture`, `deadcode`), coverage gaps, grep for the export name.
- **Fix:** delete. Git remembers. If "someone might need it someday", that's what history is for.

### Re-export barrels that only re-export
- **What:** `index.ts` that re-exports; deep import churns whenever any member moves.
- **Fix:** drop the barrel; import from where the thing lives. Barrels for a *public package entry point* are fine — that's a contract; that's a different thing.

### One-implementation interfaces
- **What:** a seam with one adapter, introduced "for flexibility". No force has ever pulled there.
- **Find:** count implementations per interface; `1` everywhere is speculation.
- **Fix:** one adapter = a hypothetical seam, not a real one. Inline the single implementation until the second shows up — or until the second is imminent and named.

### Stale shims and compat aliases
- **What:** `// deprecated, use X` that nothing calls anymore; aliases for a migration finished long ago.
- **Fix:** finish the migration in this pass — migrate every remaining call site or record why one remains — then delete the shim.

---

## Special cases — each is a requirement the design never accounted for

Hunt these across the repo (Phase 2/3) and log every hit. Each one tells you what the system *needs* — answer the need, don't patch the instance.

| Grep / smell | What it reveals | The design question |
|---|---|---|
| `if` for one literal value | A rule expressed as an exception | What's the general rule this value bypasses? Make the value data. |
| A single-case `switch` | A missing polymorphism or table | What actually decides the case? |
| Parameter only one caller passes | One workflow's dialect in shared code | Split the function, or give the workflow its own entry point. |
| `catch {}` / log-and-continue / bare `except` | The error path was never designed | Design the failure mode, or fail loudly at the boundary. |
| `sleep` / `retry` / `setTimeout` guessing | Unsynchronized timing | Where does the system know it's ready? Express that instead of guessing. |
| `it.skip` / `xfail` / commented-out tests | A behavior known-wrong, or setup that can't fail | Which is it — and when will it be resolved? |
| `TODO` / `FIXME` / `HACK` / `XXX` | An admitted requirement nobody owned | Give it an owner, a design, or a delete. |
| `any` / `@ts-ignore` / `eslint-disable` | The checker told you something | Believe it, or exclude it explicitly with a recorded reason. |
| Scattered `process.env` / config reads | No single source of configuration | One config module owns every read; the rest receive values. |
| "temporary" / "for now" / "until we" comments | A promise nobody kept | Design the end, or admit the permanence and build for it. |
| `*-v2` / `*-legacy` / `.bak` beside originals | A migration the design can't finish | Finish it or remove the coexistence; two truths is one too many. |
| Null checks "that can't happen" | An unclear contract | Define optionality at the boundary; inside, the types say it. |
| Feature flag nobody toggles | Dead in both states | Delete one path. |
| Special-case test fixture | A workaround codified | If it encodes a bug, fix the bug; if it encodes a requirement, name it. |

Kept, not deleted? Then beside each survivor write the reason it survives — or the design isn't finished.

---

## The one fix behind several problems

Don't repair instances; repair the cause and delete the span of consequences. Workflow:

1. Cluster the logged problems (by files, by seam, by mechanism).
2. For each cluster, ask what the system would look like with today's requirements known from day one.
3. Write the cluster's fix **above** them in the log (format in SKILL.md Phase 4).
4. Re-derive what remains — some "problems" were the same problem wearing different coats.

The test of a real fix: it's usually *smaller* than the sum of the patches, passes the three tests (change-together / untied / volatility), and makes at least one special case unnecessary.

## Dependency direction (imports audit)

Rank what can change — cheap ideas, stable vocabulary at the bottom:

```
domain / core logic        (changes when business rules change)
infrastructure             (changes when tech or delivery does)
providers / vendors         (changes when the outside world does)
```

Draw the arrows: everything may depend on *less* volatile things than itself; nothing may depend on *more* volatile ones. Invert with a core-owned narrow interface (a **port**) at the seam; the volatile side adapts to it. When two peers share ground, push the ground down a level — never import sideways.

Script the audit (Phase 6). Every reverse edge is a finding, or a waiver with a written reason and an owner.

## Triage

Weights, verdicts and ordering live in SKILL.md Phase 3 — follow them as written. Order is leverage under risk control: money and auth never ride in a structure commit.

## Waivers

"Leave it" is a legitimate verdict — with a reason in the log, never by silence. Good reasons: the cost is real and the leverage is nil; the change risks what it can't cover; the user decided. Bad reasons: "it's fine", "not my job", "looked hard".
