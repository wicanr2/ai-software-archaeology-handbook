# Appendix — A Complete Chain from Evidence to a Report

[Contents](README.md) · [Failure patterns](08-failure-patterns.md)

This accumulator is an invented teaching example, not a historical program. `SPEC-ACC-v1` is its authoritative contract. The values below are calculated from that contract, not fabricated execution results. There is no binary, real run ID, or tested implementation, so the final decision remains an exercise rather than an actual CONFORMED candidate.

## 1. Question and evidence

Suppose you must reimplement an accumulator accepting two-byte requests. Its teaching contract defines an integer value in 0..255. `01 n` performs saturating addition; `02 00` resets. Other `02 n` requests return `invalid_operand`; other opcodes return `unknown_operation`. A request whose length is not 2 returns `invalid_length` before opcode validation. Errors preserve state; success returns `ok`. Observe value and result code after every request.

`E-CONTRACT` is this explicit artificial contract, authoritative only for the exercise. Real archaeology also requires source versions and input/tool hashes. Desired behavior cannot simply be written down as an original-program rule.

## 2. Hypotheses and discrimination

`C-SAT` claims that addition above 255 returns 255. Before reading the contract, saturation, wraparound, and rejection are alternatives. After obtaining `E-CONTRACT`, `C-SAT` can be `CONFIRMED` within the narrow assertion “the teaching contract defines this behavior.” A single sample is not promoting a universal empirical rule.

Starting at 10 and adding 1 can give 11 under all three candidates. Starting at 250 and adding 10 predicts 255, 4, or an error leaving 250. This exposes the wrong implementation.

## 3. Conditions for READY

The contract defines format, operations, error precedence, and observation boundary. Display, persistence, timing, and concurrency are excluded because this exercise never requested them, not to avoid an existing requirement. Required cases cover ordinary addition, the limit, reset, malformed requests, and a valid request after errors.

This is enough to illustrate a READY review. A real project still needs a recorded review and implementation authority. Comparison requires exact equality of value and result code: no tolerance, sorting, or omitted fields.

## 4. Calculate the reference sequence first

Case A starts independently at 10. Case B starts independently at 250, with B01–B08 executed in order. Each row observes state after its request. Request bytes are hexadecimal; state values are decimal.

| Checkpoint | Input bytes | Value before | Reference value | Result code |
|---|---|---:|---:|---|
| A01 | `01 01` | 10 | 11 | `ok` |
| B01 | `01 0A` | 250 | 255 | `ok` |
| B02 | `01 00` | 255 | 255 | `ok` |
| B03 | `02 00` | 255 | 0 | `ok` |
| B04 | `01 FF` | 0 | 255 | `ok` |
| B05 | `02 01` | 255 | 255 | `invalid_operand` |
| B06 | `03 00` | 255 | 255 | `unknown_operation` |
| B07 | `01` | 255 | 255 | `invalid_length` |
| B08 | `02 00` | 255 | 0 | `ok` |

B08 checks recovery after errors; B03 cannot substitute for it. Nine checkpoints with two required fields each make eighteen field comparisons. Missing fields must not count as agreement. These are declared samples, not exhaustive coverage of every possible input.

## 5. Introduce a wrong candidate

`CAND-WRAP` uses `(value + n) mod 256`; assume its other behavior follows the contract. It is a paper candidate, not an executed artifact. A01 passes, but B01 has value 4 instead of 255. The first divergence is:

```text
Specification: SPEC-ACC-v1
Candidate: CAND-WRAP (teaching assumption)
Checkpoint: B01
Input: 01 0A
Field: value
Reference: 255
Candidate: 4
Result code: both ok
Conclusion: value mismatch; a success code cannot replace content comparison.
```

At B03 both candidates reset to zero, hiding the earlier error if only that endpoint is checked. If execution stops at the first divergence, B02–B08 remain unexecuted and incomplete; they must not disappear from the report.

## 6. Correction and missing observations

Correct the formula to `min(255, value + n)`, adding in an integer wide enough before applying the limit. Converting to eight bits first would still wrap. This reasoning is directly supported by the artificial contract.

Now suppose B05 records value but omits the result code. Value 255 does not tell you whether the candidate rejected the invalid request or accepted a no-op. Report a missing observation, not a pass. Required comparison remains incomplete until the missing field is obtained in a new run.

## 7. What the report may say

A paper report may state:

> By calculation under SPEC-ACC-v1, CAND-WRAP disagrees at B01's value. The corrected formula removes this counterexample. Nine reference checkpoints and eighteen required fields are specified. No actual candidate, execution record, or captured artifacts exist; no CONFORMED decision has been made.

A future execution must add candidate identity, reference/observer versions, input and artifact hashes, actual observation counts, differential results, stopping reasons, and review. Once all required conditions pass, the claim may be “this candidate conforms to SPEC-ACC-v1's declared cases,” still not historical software compatibility.

## 8. Self-check with answers

1. Does A01 exclude wraparound? No; both formulas agree there. Use B01.
2. Does B05 pass if only value is correct? No; the result code is required.
3. Does agreement at B03 cancel B01? No; each checkpoint is required.
4. Do nine matching cases prove all states? No; they support the declared cases. A universal claim needs additional reasoning or coverage.
5. Is this a successful execution report? No; it is calculable teaching material with no real run.
6. Which unknown blocks this example? A missing required result code does. Unrequested display timing does not, and is not thereby confirmed.

### Sources and claim scope

There is no historical input. `E-CONTRACT` is an artificial contract, and the values follow from it. Separating observations from interpretation, preserving missing-data failures, and identifying first divergence reflect lessons from [S3, O2, P3](../../inventory.md#固定來源索引), without importing those projects' behavior into this accumulator.
