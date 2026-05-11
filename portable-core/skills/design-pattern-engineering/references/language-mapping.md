# Language Mapping

Use this reference to adapt the same design intent across languages without blindly copying one language's style into another.

## General Rule

Preserve the design pressure, not the surface syntax.

Ask:
- Does this language prefer functions, interfaces, classes, protocols, or modules for the abstraction?
- What is the simplest idiomatic way to represent variation?
- How does the local codebase usually express boundaries and extension points?

## TypeScript / JavaScript

Prefer:
- composition over inheritance
- small interfaces or type contracts at dependency seams
- plain objects or functions for simple strategies
- classes only when lifecycle, invariants, or identity matter

Watch for:
- giant service classes
- logic hidden in framework decorators or route handlers
- "utils" files swallowing domain behavior

## Python

Prefer:
- protocols, callables, and small objects for strategies
- modules and functions when classes add no stateful value
- adapters and facades to isolate third-party clients

Watch for:
- implicit coupling through shared dictionaries
- broad "service" modules with mixed concerns
- runtime-only structure with unclear contracts

## Java / Kotlin / C#

Prefer:
- interfaces at explicit boundaries, not everywhere
- application services for orchestration-heavy flows
- factories or builders when construction really is complex
- package or namespace structure that mirrors business capabilities

Watch for:
- interface-per-class habits
- annotation-heavy layers that obscure actual responsibilities
- inheritance used only to share utility code

## Go

Prefer:
- small interfaces owned by the consumer
- package-level cohesion around behavior
- straightforward composition and explicit dependencies

Watch for:
- large "manager" types doing everything
- interfaces defined before the need for substitution appears
- infrastructure concerns mixed directly into core workflows

## Functional-Oriented Codebases

Prefer:
- pure functions for policy
- explicit data transformation stages
- higher-order functions instead of class-based template methods where appropriate

Watch for:
- anonymous pipelines so dense that business intent disappears
- configuration-driven branching with no explicit model
- side effects leaking into pure policy code

## Final Check

Whatever the language, the same standards still apply:
- responsibilities should be clear
- change points should be localized
- dependencies should be intentional
- names should reflect domain meaning
- patterns should lower maintenance cost, not raise it
