# PLAN.md — Oracle-Driven Software Archaeology

## 語言安排

先完成並審查繁體中文版，再擴充英文與日文版。第 0 階段的四份研究文件
同樣使用繁體中文；第 1 階段以前不提前產出正式手冊章節。

## 目前授權與交付邊界

專案負責人在第 0 階段交付後要求「完成手冊」。據此完成第 1 階段的九章正文，
並依先前語言指示先審讀繁體中文版、最後擴充英文與日文；完整教學例子及閱讀入口
隨手冊提供。驗收紀錄見 [docs/handbook-review.md](docs/handbook-review.md)。
後續第 2–7 階段仍是整體工具計畫，不以本次手冊完成代替其交付或自動取得實作授權。

## 1. Project Goal

Extract the recurring engineering method from the wicanr2 reverse-engineering/remake projects and turn it into:

1. a reusable **methodology / handbook**
2. a small **reference toolkit**
3. a machine-readable **evidence and conformance model**
4. an **agent protocol** for evidence-driven reverse engineering

This project is not another game remake and not a general-purpose decompiler.

The project thesis is:

> AI can generate plausible implementations quickly.
> The engineering challenge is building an observable, reproducible, evidence-based environment in which the agent can falsify its own assumptions and verify behavioral parity.

Canonical loop:

**Evidence → Hypothesis → Specification → Oracle → Implementation → Differential Validation → Conformance**

---

# Phase 0 — Repository Inventory and Method Extraction

## Purpose

Study the existing projects before creating abstractions.

Case-study repositories:

- `mm2_cht`
- `shard_of_spring_cht`
- `fd2_re`
- `wincv-remake`
- `onepce-ai-pacifista`
- `atari-talos-ai-toolkit`
- `Parhelion-PME86`

## Questions for each repository

Capture:

- what system/software was investigated
- what counted as raw evidence
- how reverse-engineering notes were stored
- how assumptions/hypotheses were handled
- what acted as the oracle
- what observations were machine-readable
- how original/candidate behavior was compared
- how failures falsified earlier assumptions
- how uncertainty was represented
- what patterns appear reusable
- what patterns are project-specific

## Deliverables

Create:

- `docs/inventory.md`
- `docs/pattern-matrix.md`
- `docs/failure-patterns.md`
- `docs/methodology-draft.md`

### `docs/inventory.md`

Per repository:

- repository/commit
- objective
- evidence sources
- RE workflow
- oracle strategy
- validation strategy
- known failure lessons
- reusable practices

### `docs/pattern-matrix.md`

Cross-project matrix.

A practice should be called a recurring pattern only when:

- observed in multiple projects, or
- supported by strong evidence that it is intentionally generalized

Suggested rows:

- evidence preservation
- provenance
- confidence levels
- raw vs semantic separation
- deterministic replay
- oracle usage
- screenshot/frame comparison
- state comparison
- spec gating
- test layering
- failure documentation
- agent instructions

### `docs/failure-patterns.md`

Document concrete examples where:

- tests passed but parity failed
- a plausible heuristic failed
- incomplete observation caused a wrong conclusion
- semantic naming created false confidence
- one platform/sample failed to generalize
- generated code looked correct but behavior differed

Each failure pattern should include:

1. initial assumption
2. evidence
3. how the assumption was falsified
4. corrected understanding
5. reusable lesson

### `docs/methodology-draft.md`

Draft the lifecycle:

**Evidence → Hypothesis → Specification → Oracle → Implementation → Differential Validation → Conformance**

For each stage define:

- inputs
- outputs
- confidence requirements
- exit criteria
- failure modes
- machine-readable artifacts

## Phase 0 Gate

PASS only if:

- at least 3 recurring patterns are source-backed
- at least 3 failure patterns are source-backed
- repository-specific practices are not falsely generalized
- provenance is present
- uncertainty is explicit

No implementation is authorized before this gate.

---

# Phase 1 — Handbook

## Purpose

Turn the Phase 0 findings into a readable engineering methodology.

Create:

- `docs/handbook/00-principles.md`
- `docs/handbook/01-evidence.md`
- `docs/handbook/02-hypotheses.md`
- `docs/handbook/03-specification-gates.md`
- `docs/handbook/04-oracles.md`
- `docs/handbook/05-differential-testing.md`
- `docs/handbook/06-conformance.md`
- `docs/handbook/07-agent-workflows.md`
- `docs/handbook/08-failure-patterns.md`

The handbook must explain clearly why:

> “tests pass” is weaker than “behavior matches the original.”

## Phase 1 Gate

A new engineer should be able to understand:

- what evidence means
- how claims gain confidence
- when implementation is allowed
- what qualifies as an oracle
- how parity is tested
- when a subsystem is `CONFORMED`

---

# Phase 2 — Machine-Readable Model

## Purpose

Represent the methodology in versioned schemas.

Create:

`schema/v1/`

with schemas for:

- `evidence.json`
- `claim.json`
- `spec.json`
- `oracle-run.json`
- `observation.json`
- `comparison.json`
- `conformance-report.json`

## Required concepts

### Evidence
Must support:

- ID
- source
- target
- hash
- location/address/path
- capture method
- raw artifact reference
- timestamp when relevant
- provenance

### Claim
Must support:

- statement
- confidence
- supporting evidence IDs
- contradicting evidence IDs
- promotion history
- unresolved questions

### Specification
Must support:

- subsystem
- state: `DRAFT | READY | CONFORMED`
- inputs
- outputs
- invariants
- known unknowns
- oracle cases
- acceptance criteria

### Observation
Must be deterministic and machine-readable where possible.

### Comparison
Must represent:

- exact matches
- mismatches
- tolerated differences
- missing observations
- unknown/uncomparable fields

## Fixtures

Use synthetic fixtures only.

Do not bundle proprietary binaries or assets.

## Phase 2 Gate

A fixture must represent a complete chain:

**evidence → claim → spec → oracle run → observation → comparison → report**

---

# Phase 3 — Minimal Reference CLI

## Language

Go.

## Working command

`osa`

## First vertical slice

Implement only:

### `osa init`
Create an OSA workspace.

### `osa oracle run`
Execute a declared adapter and capture observations.

### `osa compare`
Compare reference and candidate observation sets.

### `osa report`
Produce:

- human-readable summary
- machine-readable report

## Non-goal

Do NOT build a generic plugin ecosystem yet.

One adapter must work end-to-end before introducing generalized plugin abstractions.

## Phase 3 Gate

A deterministic synthetic example must run in CI:

`init → oracle run → compare → report`

---

# Phase 4 — One Real Oracle Adapter

## Purpose

Demonstrate the method on a real historical software target.

Choose exactly one case study.

Selection criteria:

- legally safe repository design
- user can supply original binary at runtime
- target can be identified by hash
- deterministic/headless observation is practical
- a small stable state vector is available

Possible candidates may come from:

- OnePCE
- Atari Talos
- Parhelion
- another approved wicanr2 case study

Do not choose until evidence from Phase 0/1 supports the decision.

## Adapter requirements

The adapter must:

- accept user-provided target path
- hash and identify the target
- reject unknown versions unless explicitly allowed
- run deterministically where practical
- replay a fixed input sequence
- capture machine-readable observation state
- emit `observation.json`
- preserve logs/provenance
- produce repeated identical results for identical conditions

## Phase 4 Gate

Reference vs candidate must produce a meaningful mismatch report.

---

# Phase 5 — Agent Protocol

## Purpose

Make the methodology executable by AI agents.

Create:

- `docs/agent-protocol.md`
- `examples/prompts/`

Protocol steps:

1. inspect available evidence
2. create or update a hypothesis
3. identify missing observations
4. collect evidence
5. promote/demote confidence explicitly
6. prepare a specification
7. pass the `READY` gate
8. implement
9. execute oracle/differential checks
10. record mismatches
11. revise
12. mark `CONFORMED` only if declared criteria pass

The agent must be taught to say:

`UNKNOWN`

instead of fabricating certainty.

## Phase 5 Gate

A fresh Codex/Claude session must be able to follow the protocol without hidden project knowledge.

---

# Phase 6 — Case Studies

Create at least three concise case studies.

Preferred themes:

## MM2
**Internal tests pass ≠ real parity**

Show:
- original assumption
- passing internal validation
- real-world/original mismatch
- revised verification rule

## Shard of Spring or FD2
**Disciplined uncertainty**

Show:
- evidence preservation
- subsystem reconstruction
- known unknowns
- confidence separation

## OnePCE / Atari Talos / Parhelion
**Make the original observable to agents**

Show:
- deterministic execution
- structured observation
- replay
- state capture
- oracle use

Each case study should contain:

1. problem
2. initial assumption
3. evidence
4. falsification/validation method
5. corrected model
6. generalized lesson

---

# Phase 7 — Packaging

Add:

- project README
- architecture diagram
- 5-minute demo
- example workspace
- CI
- schema validation
- Go tests
- `CONTRIBUTING.md`
- non-goals
- legal/redistribution guidance

## v0.1 Non-Goals

Not included:

- full emulator framework
- automatic decompiler
- automatic semantic naming
- universal binary analysis
- speculative AI truth score
- autonomous “accept my own output” loop
- redistribution of proprietary software

---

# v0.1 Success Criteria

The project is successful when:

1. a reader understands the methodology
2. an AI agent can follow the methodology
3. confidence and unknowns are machine-readable
4. evidence provenance is retained
5. one deterministic oracle adapter works
6. one candidate can be compared with the oracle
7. mismatches are visible and reproducible
8. `CONFORMED` has an objective declared meaning
9. the project does not require trust in the AI’s interpretation
10. the repository demonstrates the method without redistributing proprietary software

---

# Initial Codex Instruction

When starting the project for the first time, give Codex this instruction:

```text
Read AGENTS.md and PLAN.md completely before doing anything.

Execute Phase 0 only.

Do not implement the CLI.
Do not create a plugin framework.
Do not modify source case-study repositories.
Do not generalize a pattern without source evidence.
Do not invent findings from unavailable repositories.

Create only:

docs/inventory.md
docs/pattern-matrix.md
docs/failure-patterns.md
docs/methodology-draft.md

Preserve repository/file/commit provenance where available.

Classify technical conclusions as:

CONFIRMED
STRONG_INFERENCE
HYPOTHESIS
UNKNOWN

When Phase 0 is complete, stop and report:

1. files created
2. strongest recurring patterns
3. strongest failure patterns
4. disagreements between repositories
5. missing evidence
6. unresolved questions
7. recommended changes to PLAN.md

Do not begin Phase 1 without review.
```
