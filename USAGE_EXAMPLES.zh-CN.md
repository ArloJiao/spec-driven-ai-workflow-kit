# 使用示例

## 初始化仓库设计记忆

```text
Use $project-design-init for this repository. Create ai-context with current implementation facts. Keep it concise and mark uncertain areas as needing review.
```

用途：

- 为当前仓库创建 `ai-context/`
- 记录真实代码结构、模块边界、接口、运行时流程
- 避免 Agent 每次都从零读取 README/reference/历史文档

## 在 OpenSpec 仓库中做设计提案

```text
Use $design-spec.
Phase: proposal.
Change: openspec/changes/<change-id>

Read only:
- openspec/project.md
- openspec/changes/<change-id>/proposal.md
- openspec/changes/<change-id>/design.md if present
- ai-context modules relevant to the touched area
- code and tests in the touched area

Produce:
- chosen design
- compatibility boundary
- test plan
- rejected alternatives
```

用途：

- 把需求变更收敛到 OpenSpec change
- 明确设计边界、兼容性和测试计划
- 避免 Agent 直接跳到实现

## 应用一个 OpenSpec 变更

```text
Use $design-spec.
Phase: apply.
Change: openspec/changes/<change-id>

Implement tasks.md in order. If code differs from proposal assumptions, report drift before broadening scope. Update tasks.md and recommend $project-design-sync if module boundaries changed.
```

用途：

- 按 `tasks.md` 顺序实现
- 发现 spec 与代码不一致时先报告 drift
- 完成后更新任务状态
- 如模块边界变化，刷新或建议刷新 `ai-context/`

## 做维护性代码审查

```text
Use $design-pattern-engineering in review mode.
Focus on bugs, maintainability risks, compatibility risks, and missing tests. Findings first, ordered by severity, with file/line references.
```

用途：

- 优先发现 bug、兼容性风险、维护性问题和测试缺口
- 输出以 findings 开头
- 适合 PR review、重构前评估、AI 生成代码审计

## 重构后刷新设计记忆

```text
Use $project-design-sync. Refresh ai-context for the modules changed in the last commit. Preserve high-confidence evidence and mark heuristic conclusions separately.
```

用途：

- 在结构性改动后更新 `ai-context/`
- 让后续 Agent 读取到最新实现事实
- 防止设计记忆和代码漂移

## 记录一次 Skill 行为问题

```text
Use $skill-evolution-governor.
Classify this agent failure, update the skill lab if appropriate, and suggest the smallest skill patch or experiment.
```

用途：

- 记录 Agent 误触发、上下文过载、输出不符合预期等真实案例
- 判断是否需要更新 skill
- 避免同类问题反复出现

## 可选：使用环境预检

安装 `preflight-dev-context` 后，可以让 Codex 帮你初始化环境 profile，而不是手工一次性填写。

```text
Use $preflight-dev-context to initialize my environment profile. Inspect common toolchains, network/proxy state, storage preferences, and remote-host conventions. Ask before recording any uncertain or sensitive information.
```

Codex 应该先采集当前机器信息，再对不确定项提问，确认后更新：

```text
<CodexHome>/skills/preflight-dev-context/references/environment-profile.md
```

然后可以这样提示：

```text
Use $preflight-dev-context before starting this toolchain/server/debugging task. Build a 5-10 bullet working summary, then proceed.
```

用途：

- 在 Java/Android、Python、Node、Go、Rust、.NET、服务器、网络、部署等任务前确认本机环境
- 避免使用错误运行时、错误包管理器、错误网络、错误服务器
- 让 Agent 根据接收者自己的环境 profile 做决策

## 可选：使用 Workstream Hub

先指定工作流记录根目录：

```powershell
$env:CODEX_HUB = "<path-to-your-workstream-root>"
```

然后提示：

```text
Use $workstream-hub to resume the relevant workstream, update the handoff notes, and then continue the repo task.
```

用途：

- 管理多个项目、客户、分支和中断任务
- 在切换任务前写短 handoff
- 下次恢复时快速找到当前目标、下一步和风险
