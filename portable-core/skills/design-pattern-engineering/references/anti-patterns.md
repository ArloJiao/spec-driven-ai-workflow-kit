# Anti-Patterns

Use this reference when code feels heavy, muddy, or difficult to evolve. The goal is to recognize failure modes early and recover with smaller, clearer structure.

## Pattern Worship

Symptom:
- pattern names appear in discussion before the change points are understood

Risk:
- architecture chosen for prestige rather than problem fit

Correction:
- restate the unstable behavior, then select the lightest abstraction that addresses it

## Speculative Interfaces

Symptom:
- many interfaces exist only to mirror concrete classes with no real substitution boundary

Risk:
- indirection grows but flexibility does not

Correction:
- keep the concrete type until a real seam appears; add interfaces where dependencies truly need inversion

## God Service / Fat Handler

Symptom:
- one service or controller performs validation, orchestration, policy, mapping, persistence, and notifications

Risk:
- every change becomes risky and tests become broad and fragile

Correction:
- split orchestration from domain rules and isolate infrastructure concerns behind boundaries

## Branch Hub

Symptom:
- one central method decides every behavior with long type or mode conditionals

Risk:
- each new variant increases edit risk in an already crowded hotspot

Correction:
- move varying behavior to strategies, state objects, or polymorphic collaborators

## Fake Layering

Symptom:
- the codebase has controllers, services, repositories, and managers, but business rules still leak across all of them

Risk:
- the project looks structured but behaves as a ball of mud

Correction:
- redefine layers by responsibility and dependency direction, not by naming convention alone

## Inheritance For Convenience

Symptom:
- subclasses exist mainly to reuse helpers or avoid passing collaborators

Risk:
- behavior becomes fragile and base classes accumulate accidental contracts

Correction:
- prefer composition unless the subtype relationship is both real and stable

## Utility Sinkhole

Symptom:
- generic utility modules become a dumping ground for unrelated behavior

Risk:
- domain meaning disappears and reuse becomes accidental coupling

Correction:
- move logic back near the concept it belongs to and rename around explicit intent

## Configuration As Hidden Logic

Symptom:
- critical business policy is embedded in untyped maps, magic strings, or scattered config tables with no model around them

Risk:
- behavior becomes hard to validate and easy to break silently

Correction:
- model policy explicitly and validate configuration at the boundary

## Over-Abstracted MVP

Symptom:
- the first implementation already contains factories, multiple interfaces, and plugin points without evidence of change pressure

Risk:
- simple work becomes slow to understand and maintain

Correction:
- collapse unnecessary layers until a real extension point emerges

## Recovery Questions

When you suspect an anti-pattern, ask:
- what change is currently hard?
- which abstraction is paying rent, and which is only ceremony?
- where does the real business concept live?
- what is the smallest refactor that restores clarity?
