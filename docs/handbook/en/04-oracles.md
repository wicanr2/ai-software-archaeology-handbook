# 04 — An Oracle Has Limits Too

[Previous](03-specification-gates.md) · [Contents](README.md) · [Next](05-differential-testing.md)

An oracle is a reference qualified to decide a particular question. It may be the original program, an external emulator, a specification, or an independent implementation. Explain why it can decide the field under examination. “Another tool agrees” is insufficient if both tools share the same mistaken assumption.

## Match the reference to the question

| Question | Suitable reference | Limitations to retain |
|---|---|---|
| How does the original menu respond? | Pinned original version replayed from normal entry | Environment, initial state, input acceptance timing |
| Does decoding produce the same content? | Independent decoder with the same input | Versions, encodings, errors, and shared code ancestry |
| Does an instruction make the same transition? | Original/external core with known starting state | Only compared registers, memory, and instructions |
| What is a reasonable hardware approximation? | Public hardware contract | Specification approximation, not physical cycle parity |
| What should a synthetic exercise output? | Explicit contract and independent arithmetic | Only the exercise; no historical compatibility claim |

Manuals, walkthroughs, and user recollections can identify useful questions. Distinguish descriptions, observations, and actual program state. “Battlefield size” might describe a viewport or an internal array; establish the layer before declaring a contradiction.

## A traceable run

Pin original and candidate identities, oracle version, tool image ID, configuration, initial save/state, inputs, and stop conditions. Set an execution budget and prevent failed work from leaving background processes. Preserve raw observations before comparison; normalization must not overwrite them.

Use identifiable boundaries such as “after request 17,” “at the next instruction entry,” or “after the specified frame has been rendered.” Waiting one second after a keypress does not guarantee the same state. When only time-driven control is practical, record uncertainty, repetitions, and alignment conditions rather than inventing determinism.

Parhelion captures at a dispatch boundary and accounts for instruction fetch having advanced state. This is useful for core differential tests, not a substitute for reaching a game state through its normal menus (P3).

## Check replay before judging the candidate

Run the reference twice under the same conditions and compare it with itself. If results differ, investigate randomness, scheduling, configuration, sampling, or explicitly nondeterministic fields before blaming the candidate. Two matching runs support those conditions; they do not prove universal determinism.

OnePCE records that Mesen2's full-speed mode can skip rendering: memory reaches the requested frame while the captured image remains old. Its script disables frame skipping (O1, O3). Simulation completion and observation freshness are separate checks.

Give the observer positive controls and error cases. Missing tools and required artifacts must fail; an empty directory cannot mean zero differences. For image capture, use known synthetic content to check geometry, stride, channels, and cropping.

## Resolve conflicts between references

Align versions and definitions, then assess authority per field. Talos's TAS specification records timing limitations in an external corpus, uses another reference to support a local correction, and retains other field comparisons (T4). External does not mean infallible.

Preserve the original expectation, corrected value, reason, supporting evidence, affected cases, and unresolved scope. If evidence cannot decide, mark `UNKNOWN` and block the corresponding conformance claim. Do not choose the reference that most easily accepts the candidate.

For PCM/DAC/PIT timing, this repository's stop line prioritizes public contracts and the label `hardware-spec approximation`. Reopening hardware archaeology requires separate explicit authorization.

### Sources and claim scope

[O1, O3, T4, P3, W2](../../inventory.md#固定來源索引) provide capture, corpus-correction, state-boundary, and decoder examples. Inspected source contents are `CONFIRMED`; reference selection and replay practice are `STRONG_INFERENCE`. Emulator results are not presented as measurements on original hardware.
