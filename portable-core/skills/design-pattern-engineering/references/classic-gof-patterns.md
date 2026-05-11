# Classic GoF Patterns

Use this reference when you want explicit candidates from the 23 Gang of Four patterns.

## Primary Goal

Make the classic catalog usable as a real decision tool instead of a memorized list.

## How To Use This File

For each candidate, check:
- what pressure it solves
- when it is a good fit
- when it becomes ceremony
- what its modern expression usually looks like
- how to describe its idiomatic expression briefly for the current language via `language-mapping.md`

## Creational Patterns

### Factory Method

- Solves: one product creation path varies by subtype, provider, or runtime condition
- Use when: callers should not know the exact concrete type being created
- Avoid when: construction is simple and stable
- Modern note: often appears as a factory function or registry lookup instead of an inheritance-heavy class hierarchy

### Abstract Factory

- Solves: several related products must vary together
- Use when: a family of objects changes by tenant, provider, UI theme, or environment
- Avoid when: only one object varies and the rest stay fixed
- Modern note: often pairs with dependency injection or module-level provider wiring

### Builder

- Solves: staged or highly optional object construction
- Use when: construction readability and validation matter more than direct constructor calls
- Avoid when: the object is small and required parameters are obvious
- Modern note: often shows up as fluent configuration, request assembly, or immutable object creation helpers

### Prototype

- Solves: creating new objects by cloning a configured template
- Use when: setup cost is high or preconfigured copies are easier than rebuilding from scratch
- Avoid when: cloning semantics are confusing or shared mutable state is risky
- Modern note: less common in everyday service code, but useful for template objects and document generation

### Singleton

- Solves: one process-wide instance with controlled access
- Use when: there is truly one shared stateless service or resource coordinator
- Avoid when: it becomes hidden global mutable state or blocks testing
- Modern note: prefer dependency injection and explicit lifetime management over hard-coded singletons

## Structural Patterns

### Adapter

- Solves: one contract does not match another
- Use when: third-party, legacy, or transport APIs leak the wrong shape into your core code
- Avoid when: the mismatch is trivial and local to one call site
- Modern note: often used inside integration ports, gateways, and anti-corruption layers

### Bridge

- Solves: two dimensions of variation should change independently
- Use when: abstraction and implementation both vary and inheritance would explode combinations
- Avoid when: there is only one real axis of variation
- Modern note: often appears as composition between a stable policy interface and interchangeable execution backends

### Composite

- Solves: leaf objects and groups should be treated uniformly
- Use when: tree structures or nested command sets share the same operations
- Avoid when: hierarchy depth is tiny and explicit handling is clearer
- Modern note: common in UI trees, document structures, permission trees, and rule groups

### Decorator

- Solves: optional behavior layers around a stable core object or action
- Use when: logging, caching, auth, retries, metrics, or enrichment should compose cleanly
- Avoid when: only one fixed wrapper is needed
- Modern note: often shows up as middleware, interceptors, or wrapper functions

### Facade

- Solves: a noisy subsystem needs a simpler front door
- Use when: callers keep repeating the same orchestration over many dependencies
- Avoid when: it merely renames one dependency without reducing complexity
- Modern note: common for SDK wrappers, workflow entry points, and feature-level APIs

### Flyweight

- Solves: many similar objects should share intrinsic state to reduce memory cost
- Use when: object count is massive and shared data dominates
- Avoid when: memory pressure is not actually the problem
- Modern note: less common in business apps, more relevant in editors, renderers, and caches

### Proxy

- Solves: controlled access, lazy loading, remote invocation, or protection around another object
- Use when: indirection itself is the requirement
- Avoid when: a decorator or direct call is simpler and more honest
- Modern note: appears in lazy data loaders, access-control wrappers, and remote client stubs

## Behavioral Patterns

### Chain of Responsibility

- Solves: multiple handlers may process a request in order
- Use when: validation, policy checks, filters, or fallback handlers should remain composable
- Avoid when: the chain order is rigid and one explicit workflow is easier to read
- Modern note: common in middleware stacks, rule pipelines, and request filters

### Command

- Solves: actions need to be passed around, queued, retried, logged, or undone
- Use when: making actions explicit improves orchestration or lifecycle control
- Avoid when: a plain function call with parameters is enough
- Modern note: common in jobs, workflow steps, UI actions, and task dispatchers

### Interpreter

- Solves: a small language or expression grammar must be evaluated
- Use when: the business really owns an expression syntax or rule DSL
- Avoid when: a simple config table would be enough
- Modern note: use sparingly; many modern teams prefer parser libraries plus explicit evaluators

### Iterator

- Solves: traversal should be separated from collection internals
- Use when: consumers should walk a structure without depending on its representation
- Avoid when: the language already gives a clear iteration model
- Modern note: usually provided by language features rather than custom pattern code

### Mediator

- Solves: many peers interact in ways that are becoming tangled
- Use when: centralizing coordination reduces a dense reference graph
- Avoid when: it would become a god object for every interaction
- Modern note: often expressed as an orchestrator, event hub, or workflow coordinator

### Memento

- Solves: state snapshots need to be captured and restored safely
- Use when: undo, rollback, or draft recovery matters
- Avoid when: snapshot state is small enough to store directly without a formal pattern
- Modern note: more common in editors, workflow state, and complex UI state recovery

### Observer

- Solves: one subject notifies many listeners without tight coupling
- Use when: multiple in-process reactions should follow one state change or event
- Avoid when: one direct call is clearer and enough
- Modern note: often overlaps with event emitters, listeners, and reactive state subscriptions

### State

- Solves: behavior changes with lifecycle state and transitions are getting tangled
- Use when: valid actions differ meaningfully by state
- Avoid when: only a small enum and one or two branches exist
- Modern note: common in workflow engines, order status handling, and UI state machines

### Strategy

- Solves: algorithms or policies vary behind one stable use point
- Use when: adding a variant should not extend a growing conditional chain
- Avoid when: variation is tiny and unlikely to grow
- Modern note: one of the most common patterns in service code, often implemented with functions or registries

### Template Method

- Solves: workflows share a stable skeleton with a few varying steps
- Use when: the algorithm shape is fixed and inheritance already fits the codebase
- Avoid when: composition would be simpler and less rigid
- Modern note: often replaced by higher-order functions, composition, or strategies in modern codebases

### Visitor

- Solves: new operations must be added across a stable object structure
- Use when: the object hierarchy is stable but operations keep growing
- Avoid when: the structure itself changes often
- Modern note: use carefully; many modern teams prefer explicit dispatch tables or pattern matching where available
