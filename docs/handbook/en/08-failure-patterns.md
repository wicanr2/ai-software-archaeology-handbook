# 08 — Use Failure Mechanisms to Choose the Next Observation

[Previous](07-agent-workflows.md) · [Contents](README.md) · [Worked example](worked-example.md)

A failure case should help decide what to inspect next, not teach a game-specific answer to memorize. These eight cases have [pinned sources](../../inventory.md#固定來源索引); their full research records are retained in the [Phase 0 analysis](../../failure-patterns.md). This chapter turns them into diagnostic decisions.

## An uncovered output boundary: MM2 text layer (F01 / M1)

The internal canvas looked correct and packages kept running, but users saw empty text boxes. The source attributes the fault to an extra Flush in the final display transfer, bypassed by offscreen tests. When tests pass and users still see errors, compare the test route with the delivered route and locate their final difference. Repeating checks at the same layer is insufficient. This is an integration-coverage counterexample, not a full historical-parity measurement.

## Output shape passes while content is wrong: MM2 decompression (F02 / M1, M2)

A decoder padded exhausted input with zeros until output reached the declared length. The source rejected that interpretation using format and legal-termination checks. If output looks plausible but lacks direct support, ask whether code is filling in missing evidence. Length, range, and semantics are separate checks; shape alone is not enough.

## A display name hides real bytes: Shard call scanning (F03 / S2)

Mnemonic filtering excluded existing calls, and zero hits became a claim of non-use. Checking bytes and instruction starts revealed the blind spot. For something expected but not found, supply a known positive example and inspect representation, coverage, and skip counts. A readable tool label does not replace the underlying bytes.

## The test cannot distinguish candidates: Shard health (F04 / S3)

Both health and experience may rise with level. The source instead traced damage and death accesses and retained uncertainty about the other field. When many samples agree, ask whether a competing explanation would also pass all of them. If so, change the discriminating condition rather than collecting more similar samples.

## Measurement errors contaminate interpretation: WinCV capture (F05 / W1)

Misaligned image channels caused zero template matches, initially blamed on Wine font substitution. After conversion was repaired, the font claim needed a separate recheck. For cross-tool disagreement, validate the observation chain with known inputs. Then list all claims contaminated by the broken observer, not only the most recent one.

## Same frame, stale picture: OnePCE capture (F06 / O1, O3)

Reference state advanced while drawing could be skipped, leaving an old image. The source disabled frame skipping and checked replay. If memory agrees but images do not, first inspect the rendering update boundary. Wall-clock-driven presentation and deterministic simulation progress are not the same thing.

## The reference has a defect: Talos corpus (F07 / T4)

The external corpus had a known timing limitation. Another reference supported a local correction while other comparisons remained intact. For an isolated field mismatch, examine the reference's authority for that field before imitating its defect. Changing expectations still needs independent evidence: “the oracle might be wrong” is not a general escape from counterexamples.

## A static endpoint hides the sequence: FD2 opening (F08 / F2)

Static menu assets could not rule out earlier scaling and transitions. Continuous capture revised the interpretation; an incorrectly identified starting frame later forced withdrawal of the time origin. Separate assets, playback sequence, and capture coverage. Unobserved audio cannot be reconstructed as a synchronization claim from images alone.

## A reusable diagnostic order

Check input and version, then observer and sampling boundary, then comparator coverage, then the specification and candidate data flow. This is an investigative order, not a requirement to recalibrate every tool for every change. Direct evidence may narrow the slice. Without it, preserve uncertainty; fixing the candidate does not prove the old explanation was correct.

### Sources and claim scope

The existence of the eight records is `CONFIRMED`; the portability of their lessons is `STRONG_INFERENCE`. These events were not rerun for the book. Benefits for other authors or software categories remain `UNKNOWN`. Seven projects by one author are not seven independent-team experiments.
