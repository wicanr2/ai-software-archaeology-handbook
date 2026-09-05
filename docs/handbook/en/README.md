# AI-Assisted Software Archaeology Handbook

[繁體中文](../README.md) · English · [日本語](../ja/README.md)

This handbook is for engineers who can read code but may be new to reverse engineering, and for the AI agents working with them. You do not need to know IDA or an emulator first. Start by asking what supports a conclusion; then choose a tool that can obtain the necessary evidence.

The goal is to help you write a falsifiable hypothesis, an evidence-backed specification, reproducible comparison conditions, and a conformance statement that does not overreach. This is not a guide to translating an entire executable line by line. Finite tests are not a mathematical proof of every behavior.

## Contents

| Chapter | Topic | Practical outcome |
|---|---|---|
| 00 | [Principles](00-principles.md) | Distinguish internal consistency, reference agreement, and usability |
| 01 | [Evidence](01-evidence.md) | Preserve observations and check what the tools can actually see |
| 02 | [Hypotheses](02-hypotheses.md) | Design tests that distinguish competing explanations |
| 03 | [Specification gates](03-specification-gates.md) | Decide when implementation is authorized |
| 04 | [Oracles](04-oracles.md) | Select a reference with an explicit scope of authority |
| 05 | [Differential testing](05-differential-testing.md) | Locate divergence and handle missing data and tolerances |
| 06 | [Conformance](06-conformance.md) | Write an auditable, bounded completion claim |
| 07 | [Agent workflows](07-agent-workflows.md) | Scope tasks, respect gates, and leave useful handoffs |
| 08 | [Failure patterns](08-failure-patterns.md) | Recognize how eight documented mistakes developed |
| Appendix | [A complete worked example](worked-example.md) | Follow a whole chain, including a wrong candidate and a missing observation |

Read in order the first time. When investigating a mismatch, start with chapters 04–06, then revisit the assumptions in 01–03. The appendix includes self-check questions and answers; no historical software is needed.

## Evidence and translation policy

This edition follows the Traditional Chinese manuscript. Chapter numbers, source IDs, confidence levels, and example values are shared across editions. Historical cases use IDs such as M1, S3, and O2 from the [fixed source registry](../../inventory.md#固定來源索引). The registry is in Traditional Chinese; its commit-pinned links, paths, and hashes are language-independent.

Source documents and selected code were inspected. Historical run results remain reports by the original projects, not new executions performed for this book. Each chapter states that boundary. General engineering recommendations are usually `STRONG_INFERENCE`; mandatory repository rules are policies, not empirical laws. The synthetic example defines its own contract and makes no claim about a historical program.

## Terminology

| Term | Meaning |
|---|---|
| Evidence / raw observation | A locatable record of what was observed, separate from interpretation |
| Claim / hypothesis | A scoped assertion / an explanation still requiring a discriminating test |
| Provenance | The chain identifying sources, versions, locations, and capture methods |
| Oracle | A reference qualified to decide a particular comparison |
| Candidate implementation | The implementation being evaluated |
| Differential validation | Comparing reference and candidate under declared conditions |
| Conformance | Meeting a versioned contract within its declared acceptance scope |
| Observation boundary | The event or point at which state is captured |
| `CONFIRMED` | Directly supported within the stated scope |
| `STRONG_INFERENCE` | Strong support with a missing direct link |
| `HYPOTHESIS` | A plausible explanation awaiting testing |
| `UNKNOWN` | Insufficient or unresolved evidence |

`DRAFT`, `READY`, and `CONFORMED` are specification states, not replacements for confidence levels. Worksheets are for reading and planning; they are not released schemas or APIs. The planned `osa` CLI is not implemented by this handbook.
