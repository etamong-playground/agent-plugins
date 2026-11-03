---
name: korean-prose
description: Write and edit natural Korean technical prose, guides, planning documents, PR descriptions, and UI copy while preserving meaning and the requested register.
---

# Korean technical prose

Write for the reader's task and keep terminology consistent with the project.
This sharing edition contains writing rules, without personal correction history or internal examples.

## Preserve meaning

Keep the actor, object, conditions, exceptions, sequence, units, and strength of each claim.
Distinguish an observation, an inference, a proposal, and an accepted decision.
Do not make a statement more certain merely to shorten it.
Use the user's supplied text as the base when asked; do not silently replace its tone or structure.

## Structure

Give each paragraph one purpose and put information in the order the reader needs it.
State prerequisites before commands and expected results after them.
Use headings for distinct topics, lists for parallel facts, and tables for comparisons.
A connective should express an actual relationship; do not add one to disguise unrelated sentences.
Use one sentence per source line rather than wrapping paragraphs at a fixed column.

## Sentences and register

Prefer short active sentences with familiar words.
In prose, retain particles and complete predicates; do not shorten a sentence into a clipped noun phrase.
Choose a register appropriate to the artifact and keep it consistent.
Explain actions with verbs instead of stacking abstract nouns or unnecessary possessive phrases.
Do not translate idioms literally or invent Korean terms for established technical vocabulary.
Keep identifiers, command names, UI strings, paths, and error messages exact.
Avoid exaggerated claims, rhetorical introductions, automatic praise, and redundant conclusions.
Keep proposals visibly provisional instead of writing them as completed decisions.

## Technical instructions

Name the target and the operation explicitly when a pronoun could be ambiguous.
Mark examples and placeholder values as examples; do not present them as measured facts.
Put code in fenced blocks with the correct language.
State which environment an example applies to and whether it was actually tested.
Preserve relevant failure states and limits rather than removing them for brevity.

## Titles and fragments

Use a short noun phrase for a document heading.
For a Korean change title, use the repository's established action noun, such as 추가, 변경, 수정, or 제거.
Give one claim per title; put secondary details in the body.
Use fragments in a list only when the artifact's established format calls for them.

## Punctuation

Use ASCII hyphens, and avoid em dashes, en dashes, ellipses characters, and middle-dot list separators in Korean prose.
Separate a long list with commas or restructure it instead of chaining conjunctions.
Use bold for meaningful emphasis, not as a substitute for a heading or an introductory sentence.

## Final pass

Read adjacent sentences together and confirm that their relationship is clear.
Remove repetition and empty qualifiers without losing grammar or constraints.
Check that a Korean-speaking colleague could use the result without interpreting an English sentence structure.
