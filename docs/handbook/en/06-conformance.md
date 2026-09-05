# 06 — Make Completion an Auditable Conclusion

[Previous](05-differential-testing.md) · [Contents](README.md) · [Next](07-agent-workflows.md)

Conformance means a candidate passes a versioned contract within its declared acceptance scope. It is not an unconditional guarantee about an entire system. The subject of CONFORMED should be “this candidate version against this specification,” not an unversioned “project complete.”

## A report someone can audit

```text
Target/candidate identity: versions, commits, binary hashes
Specification: ID, version, acceptance scope, exclusions
Oracle: kind, version, inputs, configuration
Run: ID, starting state, input sequence, observation artifacts
Comparison: rule version, fields, checkpoints, coverage denominator
Results: exact, tolerated, mismatched, missing, skipped counts
Stop reason: completed / unimplemented / timeout / capture failure / divergence
Limits: untested platforms, unknown fields, approximations, non-blocking reasons
Decision: whether declared conditions were met; reviewer and date
Revalidation: input, tool, contract, or candidate changes that invalidate applicability
```

This is a manual report template, not evidence that `osa report` exists. The appendix shows how to report a paper exercise honestly when there are no execution artifacts.

## Audit backward from the requirements

Begin with “completion is not yet established.” Enumerate the original requirements, then find evidence for each. Do not infer requirements only from existing tests: anything without a test would disappear.

| Required outcome | Adequate evidence | Inadequate substitute |
|---|---|---|
| Normal operation completes | Delivered artifact, normal entry, full input route, output | Test-only entry directly into the result |
| Reference behavior agrees | Same-state observations, rules, differential records | Passing unit tests or a plausible screenshot |
| Boundary and error semantics | Discriminating cases and state after failure | Normal inputs only |
| Supported platforms and data versions | Necessary samples per scope with pinned inputs | A build for another platform |
| Required observations are complete | Actual count meets the contract and artifacts are locatable | One overall success exit code |

Uncomparable data is not passing, but it is not automatically a product defect either. It may be an evidence gap. Distinguish the two; a missing required observation still blocks CONFORMED.

## Early stops and excluded unknowns

Parhelion P1 reports 306 matching instructions before an unimplemented instruction stopped the run. This supports that compared trace, not full p-System compatibility. Talos T1's large CPU corpus count likewise does not substitute for unfinished machine boot.

If the contract originally requested a fixed instruction slice, other instructions may be outside scope. If the user requested complete boot, they remain incomplete work. Reducing the goal after testing is a change of question, not completion.

Separate “remake work completed,” “exact original behavior unknown,” and “optional polish.” Whether an unknown blocks delivery follows the user objective. Difficult research must not be relabeled polish, and non-blocking unknowns must not keep delivery open indefinitely.

## New versions cannot borrow old conclusions

Changes to the decoder, observer, tolerance, input version, or package may invalidate a report. Revalidate the affected scope proportionately, with an explicit dependency argument. Preserve old reports as evidence about old versions; new candidates need their own evidence. A newer file timestamp does not establish build provenance or binary identity.

When delivering, distinguish handbook completion, toolkit completion, and a real case passing. Editorial checks can establish chapter, example, and source consistency; they do not recertify historical results as newly reproduced experiments.

### Sources and claim scope

[P1, P3, T1, W1](../../inventory.md#固定來源索引) support bounded slices, stopping reasons, and artifact-identity concerns. Records are `CONFIRMED`; the reporting and audit method is `STRONG_INFERENCE`. This book uses declared, finite validation scopes rather than claiming universal mathematical proof from samples.
