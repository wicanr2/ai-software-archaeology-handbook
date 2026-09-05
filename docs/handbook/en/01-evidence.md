# 01 — Make Evidence Findable by Someone Else

[Previous](00-principles.md) · [Contents](README.md) · [Next](02-hypotheses.md)

Evidence starts with a locatable observation, not its semantic name. “A memory location decreased after damage” and “this field is health” are different statements. The first needs inputs, a location, and a capture method. The second also needs alternatives to be excluded.

A screenshot alone is incomplete evidence. Identify the program version, initial state, input sequence, capture boundary, and any scaling or color conversion. Incomplete records can remain useful leads, but must not be presented as precisely replayable experiments.

## A minimal evidence card

This is a manual worksheet, not a formal schema. Write `UNKNOWN` for missing information; do not fill in fabricated sample hashes.

| Field | Record |
|---|---|
| Evidence ID and question | A stable ID and the issue this observation addresses |
| Input identity | Original filename, SHA-256, version; repository and full commit for documents |
| Original location | Path, page, or symbol; tool and address space for addresses |
| Environment and method | Tool version, image ID, configuration, command, input sequence, and budget |
| Starting and sampling conditions | Save or state, randomness, event/frame boundary, before/after state |
| Raw artifact | Path, hash, size; dimensions and pixel format for images |
| Raw observation | Actual values, before attaching semantic names |
| Claim and confidence | Interpretation, supporting and contrary evidence, confidence, missing links |

A document hash identifies the notes you read, not the executable those notes discuss. A Git commit pins the source version, while a working tree can advance during inspection. Capture and validation must use the same pinned version.

## Preserve locations; attach semantics

Keep original function names, operands, bytes, and addresses in disassembly. Custom names can look authoritative. Attach meaning, confidence, and provenance through comments or a version-controlled index, and automatically merge that annotation into exports. An index that depends on the next reader remembering to consult it is an incomplete handoff.

Prefer a record like this over an isolated name such as `health`:

| Original location | Attached interpretation | Confidence | Evidence |
|---|---|---|---|
| Original file, operand, and explicit address space | Possibly participates in a state update | `HYPOTHESIS`, not confirmed | Capture and access-site references, with missing links listed |

An IDA linear address, segment offset, and file offset are not interchangeable numbers. Cross-tool mappings need their own bases and justification. Use the analysis database for function and data-flow relationships. Flattened assembly text is a search aid, not proof of all indirect accesses.

## Prove the search can see before trusting zero hits

Shard of Spring's scanner missed calls displayed as `wait` because it accepted only the `int` mnemonic (S2). Before interpreting a negative search, check:

1. Positive control: can the tool find a known instance?
2. Scope: did it inspect all relevant regions, or only bytes already classified as code?
3. Representation: does it cover symbols, direct operands, offsets folded into bases, and indirect access?
4. Denominator: how many entries were scanned, skipped, or unparseable?

If there are many reads but few writes, trace address-taking and subsequent indirect writes. Missing direct cross-references do not establish that writes do not exist. Report “this method found no instance” and retain `UNKNOWN`, rather than asserting absence of behavior.

## Calibrate the observer

Use a synthetic image of known geometry and colors to check image conversion, and a known event to check tracing. Confirm the tool actually started, completed, and produced the expected artifacts. WinCV's conversion bug contaminated a later font interpretation (W1). Repairing the observer also requires revisiting conclusions based on its old output.

Under this repository's shared-host rules, analysis and capture run in Docker with resource limits, an outer timeout, and a bounded lifecycle. Mount inputs read-only, check output UID/GID before writes, and remove the task's containers afterward. Preserve necessary source references and original summaries; source access does not justify importing the source project's proprietary assets.

### Sources and claim scope

[S2, W1, O3](../../inventory.md#固定來源索引) support the scanner, capture-error, and hash-recording examples. Their inspected contents are `CONFIRMED`; the card and diagnostic checks are `STRONG_INFERENCE` recommendations. Non-destructive annotation and Docker requirements are repository policy.
