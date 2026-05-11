# Anti-Examples (ZH / EN)

Use this reference to avoid over-design and to recognize when the smallest move is enough.

## Tiny CRUD Handler

Overbuilt shape:
- Create controller, service, repository, mapper, factory, and DTO transformer for one simple read or write with no real business rule.

Better call:
- Keep one thin handler plus one focused helper or query function if needed.

Chinese cue:
- "只是一个简单 CRUD，就不要硬拆成四五层。"

## One Provider With No Real Variation Yet

Overbuilt shape:
- Introduce strategy registry, abstract factory, and plugin loader for a single provider with no near-term second implementation.

Better call:
- Keep the concrete implementation explicit.
- Add a seam only where the second provider is most likely to land.

Chinese cue:
- "只有一个供应商实现时，不要先把策略注册中心全搭起来。"

## Trivial Data Carrier

Overbuilt shape:
- Turn every request or response field into a domain type even when it has no business rule.

Better call:
- Create value objects only where invariants, validation, or business meaning are real.

Chinese cue:
- "不是每个字符串都要包装成值对象。"

## Small React Component

Overbuilt shape:
- Split one small component into page shell, container, presenter, facade hook, context provider, and variant map with no real pressure.

Better call:
- Keep one readable component.
- Extract only the branchy or reusable part.

Chinese cue:
- "组件不复杂时，不要为了结构好看把它拆成一堆空壳。"

## Hotfix In Legacy Code

Overbuilt shape:
- Rename packages, move files, and redesign contracts while trying to fix a small bug in a fragile area.

Better call:
- Patch locally, add protection tests, and propose the larger cleanup separately.

Chinese cue:
- "遗留系统热修复时，先局部止血，不要顺手重做半个模块。"

## One Trivial API Mismatch

Overbuilt shape:
- Build a full facade and adapter stack for one small, isolated translation.

Better call:
- Keep a small local mapper or wrapper unless the mismatch is already spreading.

Chinese cue:
- "只有一个调用点的小差异，先用轻量映射，不必上完整适配层。"

## Rule Of Thumb

If the pressure is not yet visible in:
- branch growth
- repeated logic
- unstable dependencies
- business invariants
- compatibility risk

then the smaller move is usually the better move.
