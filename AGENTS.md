# Figma Asset Library - AI Agent 指引

## 项目上下文

关键决策和操作记录见 `reports/operation-log.md`；设计词汇表见 `docs/design-vocabulary.md`。

## Learned User Preferences

- 每次完成 Figma MCP / `use_figma` 任务后，汇总调用次数与额度使用情况。
- **每次任务执行后必须更新 `reports/operation-log.md`**，记录操作内容、思路、决策、发现和消耗。
- 用户要求"大白话"时，用通俗语言解释，避免堆砌术语。
- 给设计师或外部验收方指引文档时，用仓库内路径、已推送的远程/在线可访问位置；避免只给本机绝对路径。
- 面向设计师的交付物（如设计词汇表、场景清单）倾向「大补」一版可全量审阅，再迭代，而不是只交付零散增量。
- 先打地基再建库，不急于发布；测试与写入须在 Atome AI Test 的指定测试项目内进行，勿放在草稿区。
- **Figma 文件分类规范**：不同类型的内容必须分文件存放，同一文件内按页面（Page）分类。禁止把所有内容堆在一个文件里。
  - `AI Generated Screens` (fileKey: `tZfhizmsTeqIrP6Qnq0V86`) — AI 出图专用文件，组织空间，分页：Cover / Checkout Flow / Components Test / Archive
  - 旧文件 `Atome AI Test` (fileKey: `1nHpzMjQjLzCMO8kMhjL6g`) — 仅保留历史记录，不再追加新内容
  - 已作废 fileKey `4vMTl37Ea35TYLpM6gtzoG` 落在个人 Starter 团队，禁止使用
- 设计师标注的项目范围要严格执行。
- 说明项目优先级、范围或纳入/排除清单时，直接列出项目名称，避免仅用绿勾/红线等标注而缺少明确对应关系。
- 大范围设计落地或全量替换时，若选「全量改」方向，则倾向整体改而非局部打补丁，避免新老风格混用、观感不统一。
- 给 OpenClaw / WorkBuddy 用的 Atome 设计资产 skill 以**仓库根目录** `SKILL.md` 为真源并随 git 管理；用 `~/.openclaw/skills/atome-design-assets` 与 `~/.workbuddy/skills/atome-design-assets` 软链到本仓库即可，不宜只把 skill 放在 `~/.cursor/skills/` 等与仓库解耦的位置。

## Learned Workspace Facts

- 重点项目（4 个）：Handover # 需求沟通+对接、DesignOps # 团队工具、Flow Library # 流程库、Online Integration。
- 跳过项目（3 个）：APB（含 KP 品牌复制内容，品牌色错误）、Research & Exploration # 游乐园、Design QA # 设计走查。
- 仅凭 Catalog/扫描 JSON 等结构化输出不足以完整还原视觉稿，需结合截图或设计上下文类能力作为补充。
- 工作方法参考 Jimmy Xue 的**三层拆分**：第1层为组件与 Token 使用一致性，第2层为 UI 视觉细节，第3层为业务逻辑与交互。当前范围优先第1层，第2/3 层待前置闭环后再推进。
- **Atome 品牌色是黄色**（DesignOps 中 `brand/primary: #f0ff5f`），不是绿色。APB 中的绿色 `#00D26A` 来自 KP 品牌的复制数据。
- Atome Design Token 项目不在重点关注范围内，扫描与方案中可忽略。
- 统一库范围：DesignOps(1,588) + Handover(1,612) = 3,200 组件。APB 数据已全部删除。
- DesignOps 为统一库核心（GT Walsheim Pro），17 组去重全部以 DesignOps 为主版本。
- Figma Variables 为 0，团队用传统 Styles 管理 Token。
- Online Integration 是页面参考标准，不用于组件提取。
- 对外以 README 为入口（GitHub、飞书设计词汇表镜像；语义层真源在 `docs/`）。OpenClaw/WorkBuddy 的 bot 经 `~/.openclaw/skills/atome-design-assets` 与 `~/.workbuddy/skills/atome-design-assets` 软链到本目录后，读取同一套 `SKILL.md` 与 `docs/` / `catalog/`；**勿在仓库内再建自指/嵌套软链**（曾导致 IDE 里出现重复嵌套目录名）。协作者复现「AI 在 Figma 出图」需：支持 MCP 的 IDE、Figma MCP、有写权限的 PAT、对目标文件的编辑权；仅克隆仓库不能替代该环境。
- Figma MCP 调用额度按文件所属团队/计划计数；在组织 Full seat 下的文件中操作才使用该额度，与个人 Starter 额度相互独立。仅 View 权限的文件无法通过 `use_figma` 执行 Plugin API（read-only）；批量发现与只读提取宜用 Figma REST API（PAT）。另：DesignOps 中带 SLOT 的组件（如主按钮）在 API 下常难改实例文案/部分变体，出图后多需设计在 Figma 内手调。为省调用：已知 key/token 时优先用本地 `catalog/assets.json` 与 `catalog/tokens/design-tokens.json`，少调 `search_design_system` / `get_variable_defs`；多组件写入尽量用单次 `use_figma` 批量脚本；验证可优先用 SKILL 中的 Canvas/本地预览，非必需不调 `get_screenshot`。
