# OpenSpec Phase Guide

Use this reference to align design-pattern work with the current OpenSpec phase.

## Explore

Goal:
- understand the design problem well enough to decide what should be proposed

Ask:
- what capability is changing
- what change pressure is already visible in code
- which contracts must remain stable
- which patterns are plausible candidates
- what still needs clarification before a proposal is credible

Deliver:
- key design analysis
- candidate patterns or explicit no-pattern decision
- risk list
- test obligations
- open questions

## Proposal

Goal:
- turn analysis into an explicit design that can guide apply work

Ask:
- what pattern or seam is actually chosen
- where boundaries move or stay fixed
- how compatibility is preserved
- what migration path is required
- what tests prove the design is safe

Deliver:
- actual design choice
- boundary plan
- compatibility and migration plan
- test plan
- rejected alternatives

## Apply

Goal:
- implement the chosen design while continuing to observe code-shape problems in real time

Ask:
- is the implementation still following proposal truth
- what new code pressure appeared during coding
- what local correction is justified now
- which tests protect moved behavior
- does the relevant spec need a factual update

Deliver:
- implementation aligned to proposal
- observed code issues and narrow fixes
- tests added or updated
- explicit spec sync notes when needed

## Archive

Goal:
- close out the change without inventing extra work

Default:
- no special action

Only add work when:
- the user asks for a retrospective
- a final design summary is requested
- unresolved follow-up design debt must be recorded intentionally
