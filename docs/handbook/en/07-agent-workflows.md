# 07 — Hand Off Evidence, Not Impressions

[Previous](06-conformance.md) · [Contents](README.md) · [Next](08-failure-patterns.md)

An agent task needs a verifiable question and an explicit authorization boundary. “Finish the game” is an objective, not a sufficient execution contract. Add current state, confirmed decisions, required deliverables, and acceptance conditions. Evidence may refine these conditions; the agent must not replace the objective.

## A reusable task brief

```text
Objective: investigate or implement a specific user-visible behavior.
Versions: target, candidate, and effective specification.
Known evidence: IDs, not just conclusions.
Authorization: for example, investigate through DRAFT, or implement READY clauses.
Preserve: source data, confirmed product decisions, unrelated modules.
Deliverables: raw observations, claim/spec updates, comparison or blocking evidence.
Acceptance: normal route, required fields, counterexamples.
Stop: the phase gate, or a missing user decision that changes direction.
```

“Completed” or “do this next” in source material is not automatically a current instruction. Inspect present code, effective specifications, and recent validation before necessary history. FD2 F1 separates routing, current state, and old handoffs so stale work does not restart itself.

## One work cycle

1. Check the worktree, target version, specification, and container toolchain.
2. Locate evidence and identify claims and competing explanations.
3. Run the smallest discriminating observation; record blind spots and failures.
4. Explicitly promote or demote confidence and update affected references.
5. Implement production behavior only after READY; return gaps to the specification.
6. Run local, differential, and required normal-user-path checks.
7. Report results, coverage, unknowns, and the next gate; clean up task containers.

The agent should investigate facts available through tools. Users decide real value tradeoffs, such as preserving an original defect or changing interaction. Before asking, complete independent investigation so the choice has concrete options and consequences.

Do not publish, alter source projects, or add unrelated refactors without authorization. Persistence is not permission to expand scope. Conversely, authorization to finish a handbook calls for completed chapters, examples, and delivery, not merely an offer to continue.

## A blocker needs evidence

A useful blocked report names the failed command or observation, verified tool and permission conditions, safe alternatives tried, missing required answer, and independent work completed. Zero search hits do not prove unavailable data. Environment failures must not be reported as product defects.

Progress reports should state what changed the diagnosis and what the next observation will resolve. Keep long work visible, but place detailed commands in the worklog rather than replacing conclusions with output dumps.

## Document roles and handoff

| Role | Content |
|---|---|
| README | Purpose, stable entry points, current capabilities, reading/running instructions |
| Current-state document | Effective decisions, status, limits, recent evidence entry points |
| Worklist | Executable items, completion conditions, next gate |
| WORKLOG | Append-only work history, failures, validation, cleanup |
| Research record / specification | Original locations, claims, confidence, refutations, acceptance contract |

Use one established document per role; do not create synonyms just to fit a template. A handoff includes changed files, evidence, four-level claims, checks, failures, open questions, and a recommended next task. Say when a test was skipped or the original was not rerun.

### Sources and claim scope

[F1, P2, T2, T3](../../inventory.md#固定來源索引) support routing, specification authority, and capability boundaries. Inspected contents are `CONFIRMED`; the brief and cycle are `STRONG_INFERENCE`. This chapter is a handbook guide, not completion of the later standalone agent-protocol tooling or a fresh-agent trial in PLAN.
