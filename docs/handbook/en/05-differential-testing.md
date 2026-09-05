# 05 — Compare the Same Thing and Preserve the First Divergence

[Previous](04-oracles.md) · [Contents](README.md) · [Next](06-conformance.md)

Differential testing compares reference and candidate observations under the same conditions. The comparator also needs a contract: alignment, permitted transformations, treatment of missing data, and stopping rules. If it silently ignores missing observations, a correct candidate and an untested candidate can receive the same success signal.

## Align before comparing

Check target versions, starting state, request sequence, checkpoint IDs, sampling points, and field meanings. Parhelion compares IPC, SP, and TOS after the same p-code instruction. Comparing a pre-instruction state with a post-instruction state would be an observation error, not an implementation defect (P3).

Before sorting output or moving pixels, determine whether order and location are meaningful. Sorting a list whose order controls action priority would erase behavior under test.

## Distinguish at least six outcomes

These are reporting concepts, not released enum values or schemas.

| Outcome | Meaning | Effect on required acceptance |
|---|---|---|
| Exact agreement | Required observations exist and match exactly | Counts toward the declared denominator |
| Tolerated difference | Complete observations meet a pre-reviewed tolerance or mapping | Report separately; not raw-value equality |
| Mismatch | Comparable values violate the rule | Blocks acceptance for that scope |
| Missing observation | A required artifact, field, or checkpoint is absent | Blocks acceptance; not zero or agreement |
| Uncomparable / unknown | Versions, semantics, or boundaries are incompatible | Investigate or apply a predeclared exclusion; do not lower the gate after the fact |
| Skipped / unsupported | The test did not run or the capability is absent | Separate from passing; a required item remains incomplete |

OnePCE O2 skips the test when required environment variables are missing and skips some memory sections when their files are absent. This is an inspected control-flow risk, not a claim that its historical acceptance run lacked those files. It explains why actual coverage must be reported.

## The first divergence is often the best clue

For stateful systems, capture the first deviating checkpoint: specification and run IDs, step, input, field, reference value, candidate value, and raw artifacts. You may continue for diagnosis, but accumulated downstream errors are not necessarily independent defects.

The appendix's wrong candidate turns 250 into 4 after `01 0A`; the reference is 255. That is already a counterexample. A later `02 00` resets both to zero, so comparing only the final state would miss the error.

A parser may benefit from collecting several independent field differences. A temporal trace must preserve event order. Choose the strategy for the behavior; not every comparison requires the same first-difference algorithm.

## Declare tolerances and transformations in advance

OnePCE O1 uses a display window and color mapping, excluding the last row outside the reference. Its report must retain 76,480 compared pixels, 320 uncovered pixels per frame, and the mapping rule. Zero differences cannot be rewritten as complete equality of all native RGB values.

A displacement search may diagnose where an image matches best. Acceptance still uses the position predicted by the specification. If the best position is two pixels away, revisit geometry or sampling rather than moving the expectation. Version tolerance changes and rerun affected cases while retaining the old results.

## Test the comparator and the final output path

Give the comparator matching data, intentionally altered data, a missing field, and a misaligned checkpoint. Confirm that it rejects a wrong candidate and incomplete observations. Such deliberate defects reveal comparators that always pass. Do not generate all expected values from the same candidate being evaluated.

Products also need their final output exercised: display, file, save, or delivered package. MM2's text-layer failure shows why useful offscreen comparisons do not cover a display transfer they never execute (M1). Sample normal and alternative paths separately, and do the same for supported platforms.

### Sources and claim scope

[O1, O2, P3, M1](../../inventory.md#固定來源索引) support the denominator, skip branches, divergence, and output-boundary examples. Source inspection is `CONFIRMED`; the six-outcome reporting model and comparator counterexamples are `STRONG_INFERENCE`. No source project's tests were executed for this chapter.
