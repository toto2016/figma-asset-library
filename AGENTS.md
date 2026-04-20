# Figma Asset Library - AI Agent 指引

## 共享记忆系统

本项目使用分层记忆系统，详细上下文存储在 `~/.shared-memory/figma-asset-library/`：

| 文件 | 内容 | 读取时机 |
|------|------|---------|
| **CORE.md** | 热摘要：当前阶段、最近决策、阻塞项 | 每次启动必读 |
| **OPS.md** | 操作规则：MCP 规范、API 陷阱、编码规范 | 需要时查阅 |
| **FACTS.md** | 项目事实：范围、组件统计、设计系统关系 | 需要时查阅 |
| **PREFS.md** | 用户偏好：沟通/工作流/操作偏好 | 每次启动必读 |
| **timeline/** | 每日摘要：YYYY-MM-DD.md | 需要历史时查阅 |

## Learned User Preferences

- 每次完成 Figma MCP / `use_figma` 任务后，汇总调用次数与额度使用情况。
- **每次任务执行后必须更新 `reports/operation-log.md`**，记录操作内容、思路、决策、发现和消耗。
- 用户要求"大白话"时，用通俗语言解释，避免堆砌术语。
- 先打地基再建库，不急于发布；测试与写入须在 Atome AI Test 的指定测试项目内进行，勿放在草稿区。
- **Figma 文件分类规范**：不同类型的内容必须分文件存放，同一文件内按页面（Page）分类。禁止把所有内容堆在一个文件里。
  - `AI Generated Screens` (fileKey: `tZfhizmsTeqIrP6Qnq0V86`) — AI 出图专用文件，组织空间，分页：Cover / Checkout Flow / Components Test / Archive
  - 旧文件 `Atome AI Test` (fileKey: `1nHpzMjQjLzCMO8kMhjL6g`) — 仅保留历史记录，不再追加新内容
  - 已作废 fileKey `4vMTl37Ea35TYLpM6gtzoG` 落在个人 Starter 团队，禁止使用
- 设计师标注的项目范围要严格执行。
- 说明项目优先级、范围或纳入/排除清单时，直接列出项目名称，避免仅用绿勾/红线等标注而缺少明确对应关系。

## Learned Workspace Facts

- 重点项目（4 个）：Handover # 需求沟通+对接、DesignOps # 团队工具、Flow Library # 流程库、Online Integration。
- 跳过项目（3 个）：APB（含 KP 品牌复制内容，品牌色错误）、Research & Exploration # 游乐园、Design QA # 设计走查。
- 仅凭 Catalog/扫描 JSON 等结构化输出不足以完整还原视觉稿，需结合截图或设计上下文类能力作为补充。
- **Atome 品牌色是黄色**（DesignOps 中 `brand/primary: #f0ff5f`），不是绿色。APB 中的绿色 `#00D26A` 来自 KP 品牌的复制数据。
- Atome Design Token 项目不在重点关注范围内，扫描与方案中可忽略。
- 统一库范围：DesignOps(1,588) + Handover(1,612) = 3,200 组件。APB 数据已全部删除。
- DesignOps 为统一库核心（GT Walsheim Pro），17 组去重全部以 DesignOps 为主版本。
- Figma Variables 为 0，团队用传统 Styles 管理 Token。
- Online Integration 是页面参考标准，不用于组件提取。
- Figma MCP 调用额度按文件所属团队/计划计数；在组织 Full seat 下的文件中操作才使用该额度，与个人 Starter 额度相互独立。仅 View 权限的文件无法通过 `use_figma` 执行 Plugin API（read-only）；批量发现与只读提取宜用 Figma REST API（PAT）。
