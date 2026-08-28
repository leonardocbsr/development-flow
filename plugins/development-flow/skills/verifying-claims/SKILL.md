---
name: verifying-claims
description: Use when the agent is about to say done, complete, fixed, passing, deployed, ready, production-ready, or successful about software work.
---

# Verifying Claims

Make the smallest claim supported by fresh evidence from the exact artifact and environment in question.

`Production-ready` is forbidden unless fresh evidence covers the relevant production gates: integrated critical journeys, operational configuration, data safety or migrations, security, observability, rollout, and rollback proportional to risk. A regression test plus a passing unit suite can confirm a bounded fix; it cannot establish production readiness.

## Before a claim

1. State the claim precisely.
2. Identify what observation or command could falsify it.
3. Run that check fresh and read its complete result, including exit status and failures.
4. Compare the result with the design's acceptance criteria.
5. Report the claim, evidence, scope, and any unresolved gap separately.

Never upgrade evidence silently: a unit test does not prove integration; a mocked test does not prove a live service; a build does not prove a user journey; a reviewer report does not prove the diff; a prior run does not prove the current tree.

Never upgrade the lane in status language. An MVP does not become `production-ready` because its MVP tests pass. A PoC proves only its named claim. `Ready` must always name the destination and the gates actually exercised.

## Evidence by lane

- **Research Spike:** reproducible probe, inputs, controls, measurements, source identity, uncertainty, and whether stop criteria were met.
- **PoC:** the exact technical claim exercised end to end, plus deliberate shortcuts and unsupported cases.
- **MVP:** critical journeys work for the intended user in a representative environment; core stable-contract tests pass; known gaps are explicit.
- **Production:** relevant unit, integration, and critical end-to-end checks; operational configuration; migrations; observability; rollout and rollback evidence proportional to the risk.

## Status language

Distinguish:

- **confirmed:** directly supported by fresh evidence;
- **inferred:** conclusion from evidence that did not observe the claim directly;
- **hypothesis:** plausible but untested;
- **unknown:** evidence unavailable or contradictory.

If verification fails, report the actual state and continue investigating within scope. Do not express completion or readiness first and qualify it afterward.
