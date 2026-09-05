# 03 — Review Evidence Before Authorizing Implementation

[Previous](02-hypotheses.md) · [Contents](README.md) · [Next](04-oracles.md)

A specification is more than a formal description of an idea. Implementer and reviewer need shared answers: which inputs are valid, how state changes, which outputs are comparable, how missing information is handled, and what counts as acceptance. Missing answers must be explicit, not delegated to the implementer's guesses.

## Three states

| State | What exists | Authorized work |
|---|---|---|
| `DRAFT` | An incomplete contract, possibly containing confirmed fragments | Investigation, isolated experiments, disposable prototypes |
| `READY` | Evidence-backed behavior and scope; reviewed unknowns, cases, and acceptance criteria | Production implementation within that scope |
| `CONFORMED` | A particular candidate version passed the declared comparisons and required checks | Citing that conformance within the same scope |

These are engineering states, not claim-confidence levels. READY may exclude an unknown feature only when it does not block the requested slice. Shrinking the specification must not turn a required feature into completed work. CONFORMED does not establish excluded behavior.

## The READY review

A specification ready for implementation contains:

1. Subsystem, target version, specification version, and the actual user objective.
2. Individual claims and sources, separating original evidence, inference, deliberate deviations, and new design.
3. Inputs, outputs, initial state, and invariants.
4. Behavior for errors, unsupported versions, and missing required data.
5. Observable fields and sampling boundaries.
6. Oracle, normal and counterexample cases, and comparison rules.
7. Known unknowns, blocking decisions and reasons, and exclusions.
8. Acceptance conditions, reviewer and decision, and conditions requiring revalidation.

A specification without counterexamples may validate only plausible output. Include at least one case that rejects a wrong candidate, and ensure the test observes the relevant difference.

## A small contract

This is the appendix's invented teaching contract, not a recovered historical format:

```text
Specification: SPEC-ACC-v1
State: one integer value in 0..255.
Input: exactly two bytes per request: opcode, operand.
01 n: value = min(255, value + n); return ok.
02 00: value = 0; return ok.
02 n with nonzero n: invalid_operand; state unchanged.
Any other opcode: unknown_operation; state unchanged.
Length other than 2: invalid_length; state unchanged; checked before opcode.
Observation: value and result code after each request.
Exclusions: persistence, display, timing, concurrency, other versions.
Required cases: ordinary addition, limit, reset, malformed input, recovery after errors.
```

“We define this contract” differs from “the original behaves this way.” A declared contract can be authoritative for a synthetic test, but cannot establish historical compatibility. In real archaeology, connect each rule to evidence or leave the gap explicit.

## Gaps discovered during implementation

Suppose evidence suggests the original changes state before reporting a malformed request, while the specification requires atomic failure. Verify that evidence, reopen the affected clauses and cases, and preserve the old report. Do not carry an old conformance label onto a changed version.

Review does not require asking the user about every line of code. Engineers should investigate factual questions. Decisions that materially change behavior, format, architecture, fidelity, or publication require the user's choice. Record authorized deviations so they are not later confused with defects or original facts.

### Sources and claim scope

[P2, T2, T3](../../inventory.md#固定來源索引) document explicit gates and coexisting specifications at different states. `CONFIRMED`: the inspected Talos control contract is READY while its receipt carrier remains DRAFT. The review checklist is `STRONG_INFERENCE`; the three-state gate is also existing repository policy.
