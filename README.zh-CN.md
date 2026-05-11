# Spec-Driven AI Workflow Kit 使用说明

[English](README.md)

这是一组可分发使用的 AI 开发工作流 skills，已经做过基础脱敏和路径参数化处理。
它们的工作流思想是通用的，当前安装脚本和 skill 格式首选适配 Codex。

包内分为两部分：

- `portable-core`：推荐默认安装。包含可通用的工程设计、OpenSpec 协作、`ai-context` 设计记忆和 skill 治理能力。
- `personal-overlay`：可选安装。包含本机环境预检和跨项目工作流管理。这里已经改成模板版，接收者需要填自己的环境信息。

## 包含的 Skills

### Portable Core

| Skill                        | 作用                             |
| ---------------------------- | ------------------------------ |
| `design-pattern-engineering` | 维护性审查、重构纪律、设计模式选择、兼容性边界和测试要求。  |
| `design-spec`                | 把 OpenSpec 阶段流程和工程设计判断结合起来。    |
| `project-design-init`        | 为仓库初始化 `ai-context/`，记录当前实现架构。 |
| `project-design-sync`        | 在结构变化后刷新 `ai-context/`。        |
| `skill-evolution-governor`   | 从真实 Agent 使用案例中记录和改进 skills。   |

### Personal Overlay

| Skill                   | 作用                                | 注意                                   |
| ----------------------- | --------------------------------- | ------------------------------------ |
| `preflight-dev-context` | 在开发、调试、部署、语言工具链、包管理、网络、远程服务器任务前建立环境上下文。 | 只带模板环境文件，接收者必须填写自己的机器、工具链和服务器信息。 |
| `workstream-hub`        | 管理跨项目工作流、中断恢复、任务交接。               | 默认使用 `$CODEX_HUB` 指定的目录。             |

## 安装方式

在 `spec-driven-ai-workflow-kit` 目录下打开 PowerShell：

```powershell
.\install.ps1 -Package portable-core
```

安装全部 skills：

```powershell
.\install.ps1 -Package all
```

安装到自定义 Codex Home：

```powershell
.\install.ps1 -Package portable-core -CodexHome "D:\codex-home"
```

默认安装位置：

```text
<CodexHome>\skills\<skill-name>
```

`CodexHome` 的默认解析顺序：

1. `$CODEX_HOME`
2. `$HOME/.codex`

如果目标目录已有同名 skill，安装脚本默认不会覆盖。需要覆盖时使用：

```powershell
.\install.ps1 -Package portable-core -Force
```

安装前预览：

```powershell
.\install.ps1 -Package all -DryRun
```

## 发布包

发布打包产物放在 GitHub Release，不存放在仓库目录里。

发布方式是推送版本 tag：

```powershell
git tag v0.1.0
git push origin v0.1.0
```

GitHub Actions 会自动生成类似下面的 zip：

```text
spec-driven-ai-workflow-kit-v0.1.0.zip
```

发布包会排除 `.git/`、`.github/`、本地临时文件和已生成压缩包。

## 推荐首次使用

安装 `portable-core` 后，建议先在一个仓库里初始化设计记忆：

```text
Use $project-design-init to create ai-context for this repository.
```

如果仓库已经使用 OpenSpec：

```text
Use $design-spec. Phase: explore. Read the relevant openspec change and ai-context before proposing implementation.
```

做代码质量审查：

```text
Use $design-pattern-engineering in review mode. Focus on maintainability, compatibility, and test gaps.
```

结构性改动后刷新设计记忆：

```text
Use $project-design-sync. Refresh ai-context for the modules changed in the last commit.
```

## 常用环境变量

| 变量                                | 使用方                        | 含义              |
| --------------------------------- | -------------------------- | --------------- |
| `CODEX_HOME`                      | 安装脚本和多个 skills             | Codex Home 根目录。 |
| `CODEX_SKILL_LAB`                 | `skill-evolution-governor` | skill 演进记录目录。   |
| `CODEX_HUB`                       | `workstream-hub`           | 跨项目工作流记录目录。     |
| `CODEX_PRIVATE_HOME`              | `preflight-dev-context`    | 本机私有数据根目录。      |
| `CODEX_PREFLIGHT_CREDENTIAL_FILE` | `preflight-dev-context`    | 本机私有远程凭据文件路径。   |

## Optional Overlay 使用前配置

### preflight-dev-context

安装后需要补充环境 profile，但这件事不需要完全手工做，可以交给 AI 引导完成。

先让 AI 编码助手执行。使用 Codex 时可以这样说：

```text
Use $preflight-dev-context to initialize my environment profile. Inspect common toolchains, network/proxy state, storage preferences, and remote-host conventions. Ask before recording any uncertain or sensitive information.
```

AI 编码助手应该先运行环境采集脚本，生成工作摘要；对不确定或敏感信息提出简短问题；得到确认后再更新：

```text
<CodexHome>/skills/preflight-dev-context/references/environment-profile.md
```

这里最终应写入接收者自己的：

- 操作系统和 shell
- Python/Node/Android 等常用工具入口
- 网络、VPN、代理、镜像源
- 远程服务器别名和用途
- 本地存储偏好

不要写入：

- 密码
- token
- 私钥
- 客户敏感信息

如需保存本机私有远程凭据，使用本机环境变量：

```powershell
$env:CODEX_PREFLIGHT_CREDENTIAL_FILE = "<path-to-local-private-credentials-json>"
```

### workstream-hub

建议先指定工作流记录目录：

```powershell
$env:CODEX_HUB = "<path-to-your-workstream-root>"
```

然后让 Codex 初始化：

```text
Use $workstream-hub to initialize my workstream hub.
```

## 如果你再分发，做预检

把这个包发给别人前，建议检查：

1. 没有复制 `.system/` 或插件缓存 skills。
2. 没有真实服务器清单、客户名称、内网 IP、账号密码。
3. `preflight-dev-context/references/environment-profile.md` 仍是模板。
4. 安装脚本可以 `-DryRun` 正常运行。
5. 告诉接收者默认只安装 `portable-core`，除非明确需要 overlay。

## 推荐安装策略

一般用户：

```powershell
.\install.ps1 -Package portable-core
```

深度使用 AI 编码助手管理多个项目的用户：

```powershell
.\install.ps1 -Package all
```

只想试用，不覆盖已有 skills：

```powershell
.\install.ps1 -Package all -DryRun
```

## 重要注意事项

- 不要把凭据写入 skill 文件。
- 不要把个人环境 profile 原样发给别人。
- `portable-core` 应保持通用。
- 个人偏好的工作流、服务器、路径和客户信息应放在接收者自己的本地 overlay/profile 中。
- 如果某个 skill 引用了未安装的系统能力，AI 编码助手应明确提示缺少依赖，而不是静默失败。
