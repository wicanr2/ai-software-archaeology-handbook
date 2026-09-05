# 02 — Give a Hypothesis a Chance to Fail

[Previous](01-evidence.md) · [Contents](README.md) · [Next](03-specification-gates.md)

A useful hypothesis identifies the next observation worth making. A readable name, running code, or lack of objections must not turn it into fact. If a test passes for two different explanations, it establishes only that neither has yet been excluded.

Shard of Spring once identified a field as health because it increased with level. Experience could follow the same trend. What distinguished the explanations was the field read and written by damage and death handling, not more monotonic samples (S3).

## One assertion per claim

“This field is health, is an unsigned 16-bit value, and is unused after death” contains at least three claims. Direct evidence for one does not confirm the others. Give each an ID, scope, and supporting and contrary evidence.

| Confidence | Appropriate use | Inappropriate use |
|---|---|---|
| `CONFIRMED` | Direct evidence under stated conditions, or direct support from the declared authoritative contract | A universal rule inferred from finite samples |
| `STRONG_INFERENCE` | Multiple relevant, discriminating observations with a direct link still missing | Confident wording in place of a missing access site |
| `HYPOTHESIS` | A plausible candidate with a proposed test | A hidden default in production |
| `UNKNOWN` | Insufficient, unobservable, or contradictory evidence | Zero or nonexistence substituted for uncertainty |

There is no automatic percentage conversion. Several notes copied from one old conclusion are not independent evidence. Even `CONFIRMED` can be reopened by a wrong input version, observer defect, or contradictory result.

## Design a discriminating experiment

In the appendix's synthetic accumulator, starting at 10 and adding 1 gives 11 under both saturation and 8-bit wraparound. Starting at 250 and adding 10 predicts 255 versus 4. That input can distinguish them. These are invented teaching values, not historical game observations.

Write predictions before execution:

```text
Claim: C-SAT, additions above the limit stop at 255.
Scope: the v1 teaching accumulator's addition operation.
Alternatives: saturation / wraparound / rejection without state change.
Input: initial value 250, request 01 0A.
Predictions: 255 / 4 / error with value still 250.
Required observations: value and result code after the request; neither may be missing.
```

Precommitting predictions makes it harder to invent an explanation after seeing the result. If none predicts the observation, check the input and observer, then propose another hypothesis instead of forcing the result into the nearest candidate.

## Promotion, withdrawal, and dependencies

Record old and new confidence, date, reason, evidence IDs, and affected specifications and tests whenever confidence changes. Withdrawing “this is health” requires revisiting derived damage formulas, labels, and save interpretations. Correct current prose while preserving the old claim and the index to its refutation.

A counterexample invalidates the scope it contradicts. One non-mirrored sample refutes “all samples are mirrored,” not “every other sample is mirrored.” MM2's later images overturned a local symmetry inference; sample counts are not guarantees (M1).

## Turn uncertainty into an actionable question

“Spells are not understood” is a weak handoff. “C-17's charge timing is unknown; the effect function has no deduction, its caller remains untraced; next follow the stored cost through later reads and writes” tells the next person what to do. It distinguishes an observer's blind spot from absent behavior.

If an unknown changes the formal rule, the specification remains DRAFT. If it cannot affect the authorized slice, document the exclusion and why it is non-blocking.

### Sources and claim scope

[S3, M1](../../inventory.md#固定來源索引) document field misclassification, extrapolation, and missed caller behavior. The existence of those records is `CONFIRMED`; the experimental and dependency-tracking method is `STRONG_INFERENCE`. S3's experience interpretation is not promoted beyond the evidence available in that note.
