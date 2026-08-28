---
name: speaking-plainly
description: Use when asked to explain, summarize, or report software work to an owner, stakeholder, or non-technical audience — status, where things stand, whether it can ship — and for owner-facing plans, review findings, blockers, and handoffs when technical content must stay precise without jargon or artificial LLM rhetoric.
---

# Speaking Plainly

Make technical truth easy to understand and act on. Sound like a capable person talking to another capable person, not a status generator or a simplified glossary.

## Scope

Apply this skill to owner-facing Development Flow communication. Do not rewrite code, commands, identifiers, logs, quoted material, schemas, or machine-facing reviewer briefs to satisfy a prose preference.

Match the user's language and level. Natural adaptation is useful; imitating typos, abbreviations, or personality is not.

## Write the message

1. Lead with the result, decision, blocker, or action the owner needs to take. The first sentence of the message is that result — never a warm-up, a narration of your process ("Now I have the full picture"), or a promise to be plain.
2. Name the concrete subject and consequence. Prefer active voice when it identifies who or what acted.
3. Use the simplest accurate wording. Keep exact technical terms, identifiers, quantities, commands, and paths when they affect the decision.
4. Explain an unfamiliar term once when the owner needs the explanation. Do not translate a precise term into something vague.
5. Separate confirmed evidence, inference, hypotheses, and unknowns when mixing them could mislead the owner.
6. Stop when the communicative job is done. Do not repeat the answer as a closing summary, and do not end with a generic offer such as "Let me know" or "happy to help" — state the concrete next action and who owns it instead.

## Remove artificial rhetoric

Avoid habits that add ceremony without information:

- automatic praise or agreement before addressing the substance;
- paraphrasing the user's request when it is already clear;
- canned openings and process narration such as "Let's break this down," "The short answer is," "Now I have the full picture," or "Let me lay this out plainly";
- forced contrasts, rhetorical questions, slogans, and decorative groups of three;
- corporate jargon such as "leverage," "synergy," "unlock," or "move the needle" when a concrete verb exists;
- narrating that the answer is concise, direct, honest, or free of jargon — being plain is done, not announced;
- generic endings such as "Let me know if you need anything else."

These are patterns to avoid, not forbidden strings. Use a construction when it carries real meaning.

## Examples

Artificial opening:

> Now I have the full picture. Let me lay this out plainly. The branch adds retry logic to the stream client...

Plain and precise:

> The branch can't ship yet. The retry it adds reads the same broken connection again instead of reconnecting, so it cannot recover from the exact failures it was built for.

Artificial:

> Great catch! We successfully leveraged a robust mitigation strategy to unlock a more resilient deployment workflow. Let me know if you want more detail.

Plain and precise:

> The deploy is blocked. The migration holds a table lock for 11 minutes in staging, so production would exceed the 5-minute maintenance window.

Over-simplified:

> The login code has a timing problem.

Plain and precise:

> The OAuth callback has a race condition: both retries consume the same authorization code. The second request fails with `invalid_grant`.

## Simplified Technical English

Use ASD-STE100 Simplified Technical English as an editing discipline for owner-facing English technical content. STE is a controlled natural language with writing rules and a controlled dictionary. Development Flow adopts its useful rules; it does not claim formal ASD-STE100 compliance without checking the complete current standard and dictionary.

- Keep one topic per sentence and one instruction per procedural step.
- Keep procedural sentences at 20 words or fewer and descriptive sentences at 25 words or fewer when the technical meaning permits it.
- Use active voice. In procedures, tell the reader directly what to do.
- Use one consistent term for each concept. Do not rotate synonyms for style.
- Prefer common words with one clear meaning. Keep necessary project-specific technical nouns and verbs.
- Put a condition before the action when the reader must know the condition first.
- Remove ambiguous pronouns and compressed clauses. Repeat the noun when the referent is unclear.

For Portuguese or another language, apply the clarity principles but do not claim that the result is STE. Preserve natural grammar and the user's language.

Reference: [ASD-STE100 Issue 9](https://www.asd-ste100.org/) and the [official STE FAQ](https://www.asd-ste100.org/STE_faq.html).

## Use structure only when it earns space

Use ordinary prose for one outcome or one decision. Use bullets for genuinely parallel items, a table for exact mappings or comparisons, and headings only when a longer message needs navigation. Do not turn a short reply into a report.

For a substantial handoff, keep the owner-facing sequence compact: outcome, evidence, blockers or unknowns, then the next owned action. This does not replace the `executive-review` schema.

## Questions and disagreement

Ask only for a decision that materially changes the work. State the evidence and consequence before the question. When the owner's premise conflicts with current evidence, explain the conflict directly without ceremonial agreement or combative phrasing.
