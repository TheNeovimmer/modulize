# Sample run — `npx modulize` on a tangled checkout app

*A condensed, illustrative run for a small TypeScript app. Abridged for readability — file names simplified, output trimmed. The value is in the shape of the pass: evidence → list → redesign → verify.*

**Input:** a real-feeling repo — React UI, Stripe checkout, an undo history, command palette, icon-font toolbar. `package.json` scripts `test` / `lint` / `typecheck`. 214 tests, **2 pre-existing failures** at baseline (recorded, ignored).

## Phase 0 — Safety net

```
tree: clean (all changes committed)
tests: 212 passing, 2 failing — baseline failures logged
churn (12m): src/ui/Toolbar.tsx ×19 · src/checkout/submit.ts ×14 · ui/CommandPalette.tsx ×11
log created: /tmp/modulize-20261106-2131.md
```

No `focus` or `payment` test touches network — all mocked at module boundary. Good enough to compare against.

## Phase 2 — Map

Skeleton: 61 modules, public surface 380 members. Import graph: **2 cycles** (ui/toolbar ↔ ui/commands), 1 layer violation (`domain/invoice.ts` imports `payments/stripe.ts`), `ui/shared/Button.tsx` imported by 44 modules.

Subagents (4 lenses, evidence only) returned 26 findings; deduped to **17 raw problem entries** in the log.

## Phase 3 — List (excerpt)

```
- checkout/submit.ts:9 depends directly on payments/stripe.ts (no seam; paypal lands by copy)
- refunds/refund.ts:22 wraps every Stripe call in if (order.provider === "paypal")
- Toolbar.tsx:40 and Menu.tsx:22 call the same actions; each has its own disabled check
- shortcuts/keymap.ts:18 has a switch with one case per action, separate from the menu's list
- CommandPalette.tsx:55 keeps its own list of actions; missing the three newest
- undo.ts:30 adds a special case for every undo-able action (currently 9)
- LogoutDialog.tsx:30 waits 100ms after close and hopes the input can take focus
- SettingsDialog.tsx:61 sets a global skipRefocus flag to stop the focus steal
- Toolbar.test.tsx and Menu.test.tsx test the same actions separately
- every handler has to call track() by hand; 4 of 21 don't
- utils/dates.ts and billing/format.ts keep near-identical money-format copies
- payments/client.ts exports fetchStripeRaw() used by exactly one caller
- config read in 14 files via process.env (no config module)
```

Triage: leverage + lowest risk first. The command-list consolidation is the keystone — 7 findings collapse into it. Two entries flagged **Ask the user** (a formatter change is user-visible; a provider seam decision on receipts).

## Phase 4 — Redesign (the one fix behind several)

```
- Make the general Dialog restore focus to the element that had it before opening.
  - ui/LogoutDialog.tsx:30 waits 100ms after closing and hopes the message input can take focus
  - ui/SettingsDialog.tsx:61 sets a global skipRefocus flag to stop the steal

- Define a PaymentProvider port the core owns; Stripe and PayPal implement it via adapters.
  - checkout/submit.ts:9 depends directly on payments/stripe.ts
  - refunds/refund.ts:22 wraps every Stripe call in if (order.provider === "paypal")
  - config read in 14 files — one config module owns them; adapters receive values

- Make every user action a command: name + handler + undo + enabled(). Menu, toolbar,
  keymap, palette and history all run from one registry; track() happens in the dispatcher.
  - Toolbar.tsx:40 / Menu.tsx:22 disabled-check drift
  - shortcuts/keymap.ts:18 one-case-per-action switch
  - CommandPalette.tsx:55 stale duplicate action list
  - undo.ts:30 per-action undo special cases
  - 4 of 21 handlers missing track()
  - duplicated money-format copies collapsed into core/money.ts
  - Toolbar.test.tsx / Menu.test.tsx replaced by one registry test through the dispatcher
```

Delete list: `utils/dates.ts` (dead after money merge), `fetchStripeRaw` (single caller; inlined at the adapter), the 100ms sleep, `skipRefocus`, 9 undo special cases.

## Phase 5 — Fix (commits, suite green between)

```
refactor: one config module owns process.env reads                    (#1)
refactor: PaymentProvider port + stripe/paypal adapters               (#2)
refactor: dialog restores focus to the previously-focused element     (#3)
refactor: single command registry; menu/toolbar/keymap/palette/run    (#4)
refactor: core/money.ts; delete dates.ts and fetchStripeRaw           (#5)
test: registry dispatcher test; retire Menu/Toolbar duplicate suites  (#6)
```

Suite between commits: red after #2 (2 pre-existing failures only — baseline confirmed), green after #4. No commit mixed an unrelated concern.

## Phase 6 — Verify

- **Fresh-eyes sweep** (4 subagents): zero new findings; one "Note and leave" (legacy `Reserved` enum member, one remaining call site, logged with reason).
- **Import audit**: domain → infrastructure reversed once; adapter now implements the port. Zero reverse edges remain. 
- **One-place check**: "add a refund shortcut" → one registry entry, one command test. "Add PayPal receipts" → adapter + two files. Both land in one place.
- **Suite vs baseline**: 213 passing / 2 pre-existing failing → unchanged delta; two bugs fixed en route (missing `track()` on 4 handlers; the palette's stale list).
- **Special cases**: 17 → **2** (the `Reserved` enum member; one deliberate provider special case in receipts — product call, logged).

**Time trade**: one evening of structure work instead of months of untangling one bugfix at a time. That's the deal modulize is offering.
