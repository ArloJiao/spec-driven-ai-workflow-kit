# Worked Examples (ZH / EN)

Use this reference when the skill needs more concrete trigger language or small before/after examples.

## Trigger Phrases

English:
- "Implement this feature with maintainability as a first-class goal."
- "Refactor this without breaking the existing API contract."
- "Use design patterns only where they reduce future change cost."
- "Keep the refactor incremental and protected by tests."
- "Read the repo's local project context before changing the design."

Chinese:
- "请把可维护性作为一等目标来实现这个功能。"
- "请在不破坏现有 API 合同的前提下重构这段代码。"
- "只在真正降低后续修改成本时再引入设计模式。"
- "请采用渐进式重构，并用测试保护行为。"
- "请先读取仓库里的项目上下文，再决定如何改结构。"

## Repo Context Example

Bad shape:
- The agent sees a large service module, ignores the repo's maintained project context and local capability notes, and introduces a new layered structure that conflicts with the repo's documented feature-based organization.

Better shape:
- Read the closest maintained project context doc first.
- Read the nearest capability, constraint, or architecture note for the touched area.
- Reuse the repository's documented terminology and module boundaries.
- Keep the refactor inside the local feature unless the project context explicitly allows broader cleanup.
- Update the closest maintained context doc if the capability boundary or documented workflow changed.

Chinese cue:
- "先按仓库现有的项目上下文做局部改造，不要无视仓库文档直接重写结构。"

## TypeScript Backend Example

Bad shape:
- One route handler validates input, selects provider with `switch`, calls SDKs directly, and formats the HTTP response.

Better shape:
- Keep request parsing in the route.
- Move orchestration into an application service.
- Use `Strategy` for provider-specific behavior.
- Hide SDK details behind an adapter.
- Preserve the existing HTTP response contract.

Chinese cue:
- "把路由里的供应商分支抽成策略，但保持现有响应结构不变。"

## React Example

Bad shape:
- One page component fetches data, owns multiple unrelated states, contains role-based rendering branches, and embeds business rules in JSX.

Better shape:
- Keep route-level composition in the page.
- Move async orchestration into a feature hook or facade.
- Extract pure presentational pieces.
- Move variant logic into named functions or strategies.
- Keep state at the smallest responsible scope.

Chinese cue:
- "把页面里的角色分支和状态编排拆开，但不要把组件拆得过度零碎。"

## FastAPI Example

Bad shape:
- A route parses input, loads ORM models, applies pricing rules, sends notifications, and returns response DTOs.

Better shape:
- Keep HTTP concerns in the route.
- Move workflow into a use-case module.
- Model pricing or eligibility as policy objects or strategies.
- Use adapters for notification and persistence boundaries.
- Add characterization tests before changing legacy behavior.

Chinese cue:
- "让路由只处理 HTTP 细节，把业务规则和外部调用编排移到用例层。"

## Spring Example

Bad shape:
- One `@Service` contains transactions, branching rules, repository calls, partner integration logic, and DTO mapping.

Better shape:
- Keep transaction ownership explicit in one application service.
- Extract policy strategies for partner-specific behavior.
- Push integration details behind adapters.
- Preserve existing controller contracts.
- Use a deprecation shim if older service entrypoints must remain temporarily.

Chinese cue:
- "把 `@Service` 里的交易流程、规则判断和集成细节拆开，但先保持控制器接口稳定。"

## Legacy Migration Example

Bad shape:
- Rewriting a shared module in one step because the current design is messy.

Better shape:
- Write characterization tests first.
- Add a stable seam.
- Route one slice through the new implementation.
- Keep the old contract alive with an adapter or shim.
- Propose the next migration slice separately.

Chinese cue:
- "不要一次性推倒重来，先加测试和兼容层，再逐步迁移。"
