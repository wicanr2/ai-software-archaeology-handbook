# AGENTS.md — Oracle-Driven Software Archaeology

## 撰寫語言與版本順序

依專案負責人指示，手冊、研究文件與工作紀錄先以繁體中文撰寫。
中文版完成並審查後，最後再擴充英文與日文版本；翻譯沿用同一組證據識別碼、
來源版本與信心等級，不另立技術結論。程式識別字、檔名及固定狀態名稱保留原文。
本節保留階段閘門。第 0 階段已交付；專案負責人後續明確要求「完成手冊」，
目前授權為第 1 階段正文、完整教學例子與三語版本。這不授權自動進入第 2 階段工具工作。

後續另已授權 PDF 發行與宣傳網站。使用者確認以「王俊又 wicanr2、三語手冊＋七個案例」
為宣傳範圍，採深色版面，網站完成後公開本儲存庫並啟用 GitHub Pages；不擴充完整個人
作品集、不改變其他案例儲存庫設定，也不因此授權 `osa` 工具實作。決定見 `docs/site-release.md`。

## 0. Project Mission

Build a reusable, evidence-first methodology and reference toolkit for **AI-assisted software archaeology**.

The project is not another remake. Its purpose is to make reverse engineering and reimplementation:

- observable
- reproducible
- falsifiable
- provenance-preserving
- explicit about uncertainty
- suitable for human + AI collaboration

The canonical lifecycle is:

**Evidence → Hypothesis → Specification → Oracle → Implementation → Differential Validation → Conformance**

The central engineering problem is not whether AI can generate plausible code.
The problem is whether the project can **prove that the generated implementation matches the original behavior**.

---

## 1. Prime Directive

**Do not code ahead of evidence.**

For every non-trivial technical claim, preserve enough provenance that another engineer or agent can independently verify it.

Never convert a plausible interpretation into a fact merely because:

- the code compiles
- tests pass
- the output looks reasonable
- several samples agree
- an LLM says it is likely
- a decompiler gives a convincing name
- no contrary evidence has yet been observed

Absence of evidence is not evidence of absence.

---

## 2. Confidence Model

Every technical claim MUST be classified as exactly one of:

- `CONFIRMED`
- `STRONG_INFERENCE`
- `HYPOTHESIS`
- `UNKNOWN`

### CONFIRMED
Directly supported by authoritative evidence or reproducible observation.

Examples:
- exact bytes at a known address
- deterministic original-program behavior
- trace/log output
- emulator state
- documented checksum
- independently reproduced oracle result

### STRONG_INFERENCE
Multiple independent observations strongly support the claim, but direct proof is incomplete.

### HYPOTHESIS
A plausible explanation requiring testing.

### UNKNOWN
Insufficient evidence.

Rules:

1. Never silently promote confidence.
2. Every promotion MUST record the reason.
3. Contradictory evidence MUST reduce confidence or reopen the claim.
4. `UNKNOWN` MUST remain representable in schemas and reports.
5. Never invent a default value just to make implementation or tests succeed.

---

## 3. Specification Gate

Every subsystem progresses through:

`DRAFT → READY → CONFORMED`

### DRAFT
Evidence or understanding is incomplete.

Allowed:
- investigation
- exploratory scripts
- data capture
- temporary experiments

Not allowed:
- presenting the subsystem as understood
- broad production implementation based on assumptions

### READY
The implementation contract is sufficiently evidence-backed.

A subsystem may become `READY` only when the following are explicit:

- relevant evidence
- unresolved unknowns
- input/output behavior
- invariants
- observable state
- oracle cases
- acceptance criteria
- known unsupported cases

### CONFORMED
The candidate implementation has passed the declared oracle/differential checks.

`CONFORMED` MUST NOT mean merely:

- unit tests pass
- code compiles
- smoke test passes
- UI looks approximately right

Conformance requires comparison against the original system, an authoritative oracle, or another declared reference.

---

## 4. Control Protocol

This repository uses a gated agent workflow.

Authority order:

1. `AGENTS.md`
2. `PLAN.md`
3. current task issued by the project owner/reviewer
4. existing implementation

The agent MUST:

- work only inside the currently authorized phase/task
- not automatically continue into the next phase
- stop at every gate
- report missing evidence instead of guessing
- preserve disagreements and unresolved questions
- avoid broad refactors unrelated to the current task

At the end of each task, report:

1. files created/modified
2. evidence collected
3. `CONFIRMED` claims
4. `STRONG_INFERENCE` claims
5. `HYPOTHESIS` items
6. `UNKNOWN` items
7. tests/checks executed
8. failures encountered
9. unresolved questions
10. recommended next task

Then STOP for review.

---

## 5. Case-Study Repositories

The following wicanr2 repositories are source material for discovering the methodology:

- `mm2_cht`
- `shard_of_spring_cht`
- `fd2_re`
- `wincv-remake`
- `onepce-ai-pacifista`
- `atari-talos-ai-toolkit`
- `Parhelion-PME86`

Treat them as **case studies**, not code to merge indiscriminately.

If a repository is unavailable:

- record it as unavailable
- do not invent findings
- if network access is allowed, clone it separately for read-only inspection
- do not modify the source case-study repository unless explicitly authorized

---

## 6. Provenance Requirements

Every significant extracted lesson SHOULD preserve:

- repository
- commit SHA
- file path
- heading / symbol / function / address / test name where applicable
- observation method
- raw evidence reference
- interpretation
- confidence level

Prefer evidence such as:

- raw bytes
- addresses
- hashes
- screenshots
- framebuffers
- emulator state
- traces
- log output
- test vectors
- executable behavior

Semantic names are navigation aids, not proof.

---

## 7. Evidence vs Interpretation

Keep raw observations separate from derived claims.

Example:

**Evidence**
- Original executable SHA256: `...`
- At address `0x1234`, bytes are `...`
- Input sequence X produces output Y
- Frame 120 has register/state values Z

**Interpretation**
- This routine probably performs inventory sorting

The second statement must not overwrite the first.

---

## 8. Legal / Redistribution Boundary

Do NOT commit:

- copyrighted ROM images
- commercial game binaries
- proprietary executables without redistribution rights
- copyrighted manuals
- artwork/assets extracted from proprietary software
- keys or credentials

Allowed examples:

- hashes
- offsets
- schemas
- public metadata
- small lawful test vectors
- synthetic fixtures
- user-supplied runtime paths
- openly licensed examples

The toolkit should work with user-provided originals without bundling them.

---

## 9. Engineering Rules

Default implementation language for the reference toolkit: **Go**.

Use another language only when there is a concrete technical reason.

General rules:

- deterministic before convenient
- headless before GUI
- reproducible before clever
- fail closed on unsupported/ambiguous input
- stable JSON for machine-facing output
- preserve raw observations
- do not hide unknowns
- avoid unnecessary abstractions
- avoid premature plugin frameworks
- create one working vertical slice before generalizing
- small reviewable commits
- no unrelated refactors

Where practical, state-changing commands should support a dry-run mode.

---

## 10. Working CLI Name

Use `osa` as the working CLI name:

**Oracle-driven Software Archaeology**

The name is provisional.

Potential commands:

- `osa init`
- `osa evidence add`
- `osa evidence list`
- `osa evidence show`
- `osa claim add`
- `osa claim promote`
- `osa claim reject`
- `osa spec check`
- `osa oracle run`
- `osa compare`
- `osa report`

Do NOT implement all commands at once.

The first implementation milestone is a minimal vertical slice:

`init → oracle run → compare → report`

---

## 11. Testing Philosophy

Tests must state what they prove and what they do **not** prove.

Separate at least these layers:

1. parser/unit correctness
2. deterministic replay
3. oracle/differential agreement
4. conformance coverage

Examples:

- unit test pass ≠ original parity
- deterministic output ≠ correct semantics
- matching one frame ≠ matching all behavior
- matching N samples ≠ proof of a general rule

Where possible, deliberately include falsification tests.

---

## 12. Documentation Rules

Documentation is a first-class project artifact.

Important design decisions SHOULD explain:

- what is known
- what is inferred
- what is unknown
- why the current design was selected
- what evidence could falsify the decision

Do not write retrospective certainty into documents.

If history shows that a previous assumption was wrong, preserve the failure pattern as a lesson.

---

## 13. Commit Discipline

Prefer this progression:

1. repository inventory
2. evidence/failure pattern analysis
3. methodology
4. schemas
5. synthetic fixtures
6. minimal CLI
7. one real oracle adapter
8. differential comparison
9. conformance report
10. agent protocol
11. case studies
12. packaging

Commit messages should be concise and scoped.

Do not mix unrelated phases in one commit.

---

## 14. First Authorized Work

Unless the project owner explicitly says otherwise, the initial authorized phase is:

**Phase 0 — Repository Inventory and Method Extraction**

During Phase 0:

DO:
- inspect repositories
- collect evidence
- document repeated patterns
- document failure modes
- draft the methodology

DO NOT:
- implement the CLI
- create a plugin framework
- refactor case-study repositories
- create speculative generic abstractions
- claim cross-project patterns without evidence

Expected Phase 0 outputs:

- `docs/inventory.md`
- `docs/pattern-matrix.md`
- `docs/failure-patterns.md`
- `docs/methodology-draft.md`

Then STOP for review.

---

## 15. Definition of Done for v0.1

v0.1 is successful when:

- the methodology is documented
- confidence states are explicit
- specification gates are defined
- schemas can represent evidence → claim → spec → observation → comparison → conformance
- a deterministic oracle adapter exists
- one real case study can be represented without redistributing copyrighted software
- `osa compare` generates machine-readable and human-readable mismatch results
- provenance is retained
- unresolved unknowns remain visible
- another agent can follow the protocol without hidden project knowledge
- at least three reusable lessons from wicanr2 projects are documented with source provenance
