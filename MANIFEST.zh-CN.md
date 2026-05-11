# Spec-Driven AI Workflow Kit 清单

## 包名

`spec-driven-ai-workflow-kit`

## 适用对象

适合长期使用 Codex 做软件工程工作的开发者，尤其是希望具备以下能力的人：

- OpenSpec 驱动的变更流程
- 通过 `ai-context/` 维护仓库级设计记忆
- 面向维护性的代码审查、重构和设计模式判断
- 可选的跨项目工作流和中断恢复管理

## 安装集合

### `portable-core`

默认推荐安装。

```text
portable-core/skills/design-pattern-engineering
portable-core/skills/design-spec
portable-core/skills/project-design-init
portable-core/skills/project-design-sync
portable-core/skills/skill-evolution-governor
```

依赖说明：

- 不需要任何私有文件。
- `design-spec` 在仓库已有 `openspec/` 时效果最好。
- `project-design-init` 和 `project-design-sync` 会创建或刷新 `ai-context/`。

### `personal-overlay`

仅在接收者确实需要额外工作流时安装。

```text
personal-overlay/skills/preflight-dev-context
personal-overlay/skills/workstream-hub
```

依赖说明：

- `preflight-dev-context` 默认只是模板，接收者需要初始化自己的 `references/environment-profile.md`。这一步可以交给 Codex 通过 `$preflight-dev-context` 交互完成：先检查机器环境，再询问不确定项，只写入已确认且非敏感的信息。
- `workstream-hub` 会创建新的工作流记录目录，不包含任何个人历史记录。

## 分发前检查

分享此文件夹前，建议确认：

- 未包含 `.system/` 下的系统 skills。
- 未包含插件缓存目录。
- 未包含本机绝对路径、私有 IP、内部主机名、客户名称。
- 未包含密码、token、私钥或其他凭据。
- `preflight-dev-context/references/environment-profile.md` 仍是模板。
- 接收者知道默认应先安装 `portable-core`，只有需要时才安装 `personal-overlay`。

## 版本说明

这是一个可分享的 skills 快照。后续使用过程中，如果发现触发范围、上下文读取或输出格式有问题，应通过 `skill-evolution-governor` 记录真实案例并逐步改进。
