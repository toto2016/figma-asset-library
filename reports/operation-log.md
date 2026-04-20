# Figma 素材库建设 — 操作记录稿

> 项目: Atome UED Figma 全量素材库
> 启动时间: 2026-04-15
> 最后更新: 2026-04-16（含项目全局总结）

---

## 项目目标

从 Atome UED 团队的 Figma 项目中系统化提取全部 UI 设计资产（组件、样式、Token），
建立本地索引，最终实现"需求描述 → 自动出图"的能力。

---

## Day 1 — 2026-04-15

### 阶段 1: 账号确认与权限验证

**背景**: 项目启动前需确认 Figma MCP 的调用额度。此前为 Starter 计划（6次/月），
用户已申请升级到 Professional Full seat。

**操作**:
1. 调用 `whoami` 确认身份和计划 → 发现有两个计划：个人团队（Starter/View）和组织（Full/Expert）
2. 用组织 key 创建测试文件 `create_new_file` → 确保调用计费走组织额度
3. 在测试文件上运行 `get_metadata` + `use_figma` → 读写权限正常

**关键决策**: 必须使用 `organization::1001709743790382367` 创建文件，
否则会计入个人 Starter 额度（6次/月）。

**踩坑记录**:
- `use_figma` 创建带 `DROP_SHADOW` 的元素时报错 — 缺少 `blendMode: 'NORMAL'` 字段（API 文档未提及）

**消耗**: 3 次 MCP 计费 + 1 次免费（whoami）

---

### 阶段 2: MCP 工具全量审计

**思路**: 在投入大量额度做正式提取前，先把 17 个 MCP 工具全部测试一遍，
搞清楚每个工具能做什么、不能做什么、有什么坑。这比盲目开始正式工作更划算。

**操作**: 逐个测试 17 个工具，按 读取/写入/Code Connect/FigJam/免费 分类。

**关键发现**:

| 发现 | 影响 |
|------|------|
| `get_variable_defs` 要求桌面端选中图层 | MCP 自动化不可用，改用 REST API 或 Plugin API |
| `use_figma` 在 View 权限文件上报 read-only | 组织文件只有 View 权限，无法用 Plugin API 提取 |
| `add_code_connect_map` 需组件已发布 | Code Connect 映射需先在 Figma 中发布组件 |
| `get_design_context` 触发 Code Connect 提示 | 加 `disableCodeConnect: true` 可跳过 |
| `search_design_system` 搜索全组织库 | 可用于跨项目组件发现 |
| `generate_figma_design` 免费 | 网页捕获能力，不消耗额度 |

**架构转折点**: 发现 `use_figma` 无法在组织文件上执行（View 权限限制），
这意味着**无法用 Plugin API 批量提取数据**。必须转向 Figma REST API。

**产出**: `reports/tool-audit-report.md` — 完整的 17 工具测试报告

**消耗**: 13 次 MCP 计费

---

### 阶段 3: 可行性评估（多角色）

**思路**: 在投入大量时间做全量扫描前，先请 6 个 UI/UX 相关角色评估方案可行性，
确保方向正确、产出有价值。

**角色**: UI Designer, UX Lead, Design System Architect, DesignOps Engineer,
Interaction Designer, Design QA Lead

**共识**: 项目可行（平均 7.2/10），但原始 JSON 对设计师不友好，
需增加可视化目录和标准化 Token 导出。

**争议**: Design QA 和 Interaction Designer 对纯结构化数据的实用性存疑，
认为需要截图和 Token 才有真正价值。

**决策调整**: 采纳建议，增加截图资产（Wave B）和 Token 标准化导出。

**产出**: `reports/uiux-feasibility-review.md`

---

### 阶段 4: 文件发现（REST API）

**思路**: MCP 没有"列出项目文件"的工具，需用 Figma REST API 发现全部文件。

**前置条件**: 用户提供 Figma Personal Access Token（PAT），
勾选 `file_content:read`, `file_metadata:read`, `library_content:read`, `projects:read` 等 scope。

**操作**:
1. 编写 `scripts/discover-files.sh` — 用 curl + python 遍历组织下所有团队、项目、文件
2. 用户提供 PAT token
3. 执行发现脚本

**结果**: 12 个项目，555 个文件（用户最初估计 914 个，实际少了 39%）

**踩坑**: 脚本中 Python heredoc 无法直接使用 bash 变量，
改用 `python3 - "$VAR1" "$VAR2" << 'PYEOF'` + `sys.argv` 传参。

**产出**: `sources/` 目录下 12 个项目的 JSON 文件清单

**消耗**: 0 次 MCP（纯 REST API）

---

### 阶段 5: 三线并行执行

**思路**: 将剩余工作拆成三条并行线路，最大化效率：
- **Wave A**: 高价值库文件完整 Token 提取（REST API，零 MCP 消耗）
- **Wave B**: 核心组件截图（MCP `get_screenshot`，消耗额度）
- **Wave C**: 剩余文件的 Catalog 扫描（REST API，零 MCP 消耗）

#### Wave A — 深度提取（REST API）

**操作**:
1. 从已扫描的 DesignOps + Flow Library 中识别 5 个高价值文件
2. 编写 `scripts/deep-extract.sh` — 用 REST API 提取文件结构(depth=3)、
   已发布组件（含前 50 个的节点属性）、样式（含节点属性）、本地变量
3. 执行提取

**结果**: 5/5 成功，1,164 组件（219 有详情），68 样式，变量全为 0

#### Wave B — 核心截图（MCP）

**操作**:
1. 从深度提取数据中选出最有代表性的 Frame/Section 节点 ID
2. 策略：截分组级 Frame，一张图覆盖该分组所有组件变体

**截图目标选取原则**:
- Design Library Mobile: buttons, controls, input, types, colors, popup, icons（7 个核心分组）
- Merchant Centre Library: button, form input, table, navigation, charts, colors, typography（7 个核心分组）

**结果**: 14/14 全部成功

**消耗**: 14 次 MCP 计费

#### Wave C — 全量 Catalog 扫描（REST API）

**操作**:
1. 编写 `scripts/scan-rest-api.sh` — 对每个文件做 3 个 REST 调用：
   文件结构(depth=2) + 已发布组件 + 已发布样式
2. 分两批并行执行：小项目 5 个 + 大项目 3 个
3. 等待完成（research 174 文件约 17 分钟，ux-sandbox 182 文件约 20 分钟）

**结果**: 12 个项目全部完成，544/555 成功（98%），11 个失败（超时或权限）

**重要发现**: APB 项目有 1,682 组件 + 43 样式，是之前完全不知道的第二套设计系统！

**消耗**: 0 次 MCP（~1,650 次 REST API 调用，不计费）

---

### 阶段 6: 方法论沉淀 → Skill

**思路**: 这套"探测 → 测绘 → 分层提取 → 多角色评估 → 大白话翻译"的方法论
不仅适用于 Figma，可以泛化到任何系统的审计场景。

**操作**:
1. 创建 `systematic-auditor` skill（从 `figma-asset-auditor` 升级为通用方法论）
2. 部署到三个位置：`~/.cursor/skills/`、`~/.workbuddy/skills/`、`~/.openclaw/workspace/`
3. 更新 openclaw 的 SKILLS.md 注册表

**Skill 结构**:
- `SKILL.md` (280 行) — 5 阶段通用方法论
- `references/role-templates.md` — 4 类审计场景的角色预设
- `references/extraction-patterns.md` — 分层提取模板
- `references/figma-recon.md` — Figma 参考实现

---

### Day 1 总结

| 指标 | 数值 |
|------|------|
| MCP 计费调用 | 32 次 |
| MCP 免费调用 | 3 次 |
| MCP 剩余 | 168 / 200 |
| REST API 调用 | ~1,675 次 |
| 文件扫描完成 | 544 / 555 (98%) |
| 深度提取完成 | 5 个高价值文件 |
| 截图完成 | 14 张 |
| 产出文件 | 审计报告、可行性评估、扫描报告、Skill |

---

## Day 2 — 2026-04-16

### 阶段 7: APB + Handover 深度提取

**背景**: Day 1 全量扫描发现 APB 是第二套完整设计系统（1,682 组件 + 43 样式），
Handover 有 Screen Library（1,477 组件），都需要深度提取。

**操作**:
1. 编写 `scripts/deep-extract-wave2.sh` — 增加 APB 5 文件 + Handover 2 文件
2. 执行深度提取（REST API，零 MCP 消耗）

**结果**: 7/7 全部成功
- APB: 5 文件 → 1,682 组件（250 有详情）+ 43 样式
- Handover: 2 文件 → 1,502 组件（75 有详情）

**发现**:
- APB 用 `Plus Jakarta Sans` 字体，DesignOps 用 `GT Walsheim Pro` — 两套独立体系
- APB 有标准化 10 级色阶（brand-50 到 brand-900），比 DesignOps 更规范
- 所有文件变量数仍为 0

**消耗**: 0 次 MCP

---

### 阶段 8: APB 核心组件截图

**操作**:
1. 从深度提取数据中选出 APB Mobile 2.0 的 7 个核心分组节点
2. 用 MCP `get_screenshot` 批量截图

**截图内容**:
- Color Palette — 完整 10 级色阶（White/Neutral/Brand/Success/Warning/Error/Information）
- Main Components — Published Component 图标库 + Container
- Typography — 完整字体层级（Amount → Tag），含字号/行高/字重规格
- Buttons — Primary/Secondary/Tertiary/Small Primary/Text Link/Icon Button × 3 状态
- Input Fields — Input/Password/Amount 全状态矩阵
- Icons + Transaction List — 列表项/交易记录/营销卡片
- OTP/Rating — 验证码输入 + 星级评分组件

**结果**: 7/7 全部成功

**消耗**: 7 次 MCP 计费

---

### 阶段 9: 统一索引构建

**思路**: 把分散在 12 个 `*-scan.json` 中的数据整合成一个统一索引，
方便后续按项目/组件/样式查询。

**操作**:
1. 编写 `scripts/build-index.js` — 聚合所有 scan 数据 + 关联 deep 数据
2. 执行生成 `catalog/assets.json`

**产出**: 统一索引包含：
- `summary` — 全局汇总（544 文件, 4,351 组件, 111 样式, 14 高价值, 12 深度提取）
- `componentIndex` — 组件按分组排序的索引（Top 100）
- `highValueFiles` — 14 个高价值文件详情
- `allFiles` — 544 个文件的完整列表

---

### 阶段 10: Design Token 导出

**思路**: 从 12 个深度提取文件的 styleDetails 中，提取所有颜色、字体、效果的标准化 Token。

**操作**:
1. 遍历所有 deep extraction JSON 中的 `styleDetails`
2. 颜色：SOLID fill → HEX + RGBA
3. 字体：textStyle → fontFamily + fontSize + fontWeight + lineHeight
4. 效果：effects 原样保留
5. 保存到 `catalog/tokens/design-tokens.json`

**结果**:
- 100 个颜色 Token（含 Brand/Interaction/Grayscale/Message/Overlay + Charts 专用色）
- 58 个字体 Token（含 DesignOps GT Walsheim Pro + APB Plus Jakarta Sans 两套体系）
- 5 个效果 Token（Shadow/Drop Shadow）

**关键发现 — 两套字体体系**:

| 体系 | 字体 | 范围 | 特点 |
|------|------|------|------|
| DesignOps | GT Walsheim Pro | Mobile + Desktop + Merchant | 传统 Atome 品牌字体 |
| APB | Plus Jakarta Sans | Mobile 2.0 + Web | 新品牌字体，字号更大 |

---

### 阶段 11: 文档更新

**操作**:
1. 更新 `README.md` — 所有阶段状态从"待开始"改为"✅ 完成"
2. 更新 `AGENTS.md` — 补充 APB 项目发现、字体体系差异、Variables=0 等事实
3. 更新 `reports/extraction-log.json` — Day 2 的 8 次 MCP 调用详情
4. 更新 `reports/full-scan-report.md` — 需要更新（深度提取已从 5 → 12）
5. 创建本文档 `reports/operation-log.md` — 完整操作记录稿

---

### Day 2 总结

| 指标 | 数值 |
|------|------|
| MCP 计费调用 | 8 次（7 截图 + 1 whoami 免费） |
| MCP 剩余 | 192 / 200 |
| REST API 调用 | ~35 次（深度提取） |
| 新增深度提取 | 7 个文件 |
| 新增截图 | 7 张 |
| Design Token | 163 个（100 颜色 + 58 字体 + 5 效果） |
| 新增产出 | 统一索引 + Token 文件 + 操作记录稿 |

---

## 累计产出总览

### 数据资产

| 资产 | 路径 | 说明 |
|------|------|------|
| 项目文件清单 | `sources/*.json` | 12 个项目的文件 ID 列表 |
| Catalog 扫描 | `reports/extractions/*-scan.json` | 544 文件的结构+组件+样式 |
| 深度提取 | `reports/extractions/deep/*.json` | 12 个高价值文件的完整属性 |
| 统一索引 | `catalog/assets.json` | 全量聚合索引 |
| Design Token | `catalog/tokens/design-tokens.json` | 163 个标准化 Token |
| 截图 | 21 张（MCP 返回，未保存到本地文件） | 核心组件可视化 |

### 脚本工具

| 脚本 | 用途 |
|------|------|
| `scripts/discover-files.sh` | REST API 文件发现 |
| `scripts/scan-rest-api.sh` | REST API Catalog 批量扫描 |
| `scripts/deep-extract.sh` | REST API 深度提取 (Wave 1: DesignOps) |
| `scripts/deep-extract-wave2.sh` | REST API 深度提取 (Wave 2: APB + Handover) |
| `scripts/build-index.js` | 统一索引构建 |
| `scripts/pilot-test.js` | Plugin API 权限测试 |
| `scripts/extract-lite.js` | Plugin API 轻量扫描（受 View 权限限制，已弃用） |

### 报告文档

| 文件 | 说明 |
|------|------|
| `reports/tool-audit-report.md` | 17 个 MCP 工具全量测试报告 |
| `reports/uiux-feasibility-review.md` | 6 角色可行性评估 |
| `reports/full-scan-report.md` | 全量扫描汇总报告 |
| `reports/extraction-log.json` | 逐条 API 调用日志 |
| `reports/operation-log.md` | 本文档 — 操作记录稿 |

### Skill

| Skill | 路径 | 说明 |
|------|------|------|
| `systematic-auditor` | `~/.cursor/skills/` + `~/.workbuddy/skills/` + `~/.openclaw/workspace/` | 通用系统审计方法论 |

---

## 资源消耗汇总

| 日期 | MCP 计费 | MCP 免费 | REST API | 剩余额度 |
|------|---------|---------|----------|---------|
| 4/15 | 32 | 3 | ~1,675 | 168/200 |
| 4/16 | 7 | 1 | ~35 | 192/200 |
| **累计** | **39** | **4** | **~1,710** | — |

---

## 关键决策与转折点

1. **Plugin API → REST API 转向**（4/15）
   - 原因：`use_figma` 在 View 权限文件上报 read-only，无法用于组织文件
   - 影响：REST API 无日调用限制，反而更适合批量提取
   - 教训：永远先测试工具能力，再投入正式工作

2. **发现 APB 第二套设计系统**（4/15）
   - 原因：全量扫描发现 APB 有 1,682 组件，是用户未提及的独立体系
   - 影响：项目范围从"1 套设计系统"扩展为"2 套"，且字体体系不同
   - 教训：用户的预期 vs 实际数据总是有差距

3. **Styles → Variables 迁移机会**（4/15-16）
   - 发现：所有文件 Variables = 0，颜色/字体全用传统 Styles 管理
   - 机会：迁移到 Variables 后可支持 Light/Dark Mode、响应式等现代能力

4. **97.5% 文件无设计资产**（4/15）
   - 发现：555 文件中仅 14 个有已发布组件/样式
   - 影响：大幅缩小真正需要关注的范围，聚焦 14 个核心文件即可

---

## Day 2 续 — 2026-04-16 组件去重与多维分类

### 阶段 12: 全量组件列表获取

**背景**: 此前深度提取中 `componentDetails` 每文件限 50 个，无法做准确去重分析。

**操作**:
- 编写 `scripts/fetch-components.sh`，通过 REST API `GET /v1/files/:key/components` 获取全量组件
- 对 12 个高价值文件逐一调用，每个返回完整的 published components 列表
- 数据保存到 `reports/extractions/components/` 目录

**结果**:
- 总计获取 **4,348** 个组件的完整信息（name, key, node_id, containing_frame, containingComponentSet）
- DesignOps: 1,588 | APB: 1,148 | Handover: 1,612
- REST API 调用 12 次，**不消耗 MCP 额度**

**关键发现**: 每个组件的 `containingComponentSet` 字段提供了组件集名称，这是去重的关键——
同一组件集下的变体共享一个名称（如 "Button"），变体名如 "Type=Big, Class=Primary" 才是唯一标识。

### 阶段 13: 组件去重分析

**背景**: DesignOps 和 APB 是两套独立演化的设计体系，需要识别重叠组件为统一库做准备。

**方法**:
- 编写 `scripts/component-dedup.py`，按 containingComponentSet 聚合组件
- 标准化名称后跨体系匹配，同时检测体系内跨文件重复
- 自动分类为 22 种 UI 类型（button, icon, input, card...）

**结果** (`reports/component-dedup-report.md`):
- 发现 **17 组跨体系重复**，涉及 283 个变体
- 重叠最严重: Button (84 变体, 4 处定义), Avatar (56), Checkbox (19)
- 体系内重复 **9 组**（主要在 DesignOps 的 Mobile/Web/Merchant 三个库之间）
- 所有重复均在 DesignOps ↔ APB 之间，Handover 几乎无重叠

**决策**:
1. Button/Avatar/Checkbox 等核心控件优先以 APB [Design System] Web 为基础（更现代的变体命名规范）
2. DesignOps 独有的 icon/navigation/form 组件补充进统一库
3. Handover 的 1,571 个独立组件多为页面级截图，不纳入原子组件库
4. Merchant Centre Library 有独立的控件体系（Switch/Pagination 等），需单独评估

### 阶段 14: 多维度分类索引

**背景**: 4,348 个组件需要多维度检索能力，支持"按类型查"、"按平台查"、"按业务模块查"。

**操作**:
- 编写 `scripts/build-classified-index.py`
- 构建 5 个维度索引: UI类型、平台、设计体系、业务模块、类型×平台交叉

**结果** (`catalog/classified/` + `catalog/classified-index.json`):
- **22 种 UI 类型**: other(2150), icon(503), typography(202), button(198), input(171)...
- **4 种平台**: mobile, web, shared, unknown
- **10 种业务模块**: general(2394), payment(989), kyc(461), profile(160)...
- **61 种类型×平台组合**
- 每个维度值生成独立 JSON 文件，可直接查询

**发现**:
- payment 相关组件最多 (989)，占比 22.7%——说明支付是产品核心
- KYC 模块 461 个组件，占比 10.6%——身份验证也是重点
- "other" 分类仍有 2,150 个（49.4%），后续可进一步细化分类规则

### 阶段 15: 重复组件主版本选择方案

**背景**: 17 组跨体系重复组件需要逐一裁决主版本，为统一组件库建设提供明确蓝图。

**方法**:
- 建立 5 维评分体系：命名规范(0-2)、变体完整度(0-2)、体系结构(0-2)、维护活跃度(0-2)、跨平台潜力(0-2)
- 逐组对比所有实例，打分后选出最高分版本
- 对特殊情况（不同业务场景、假重复）做定性判断

**结果** (`reports/version-selection-plan.md`):
- **APB Web 胜出 11 组**：Button, Avatar, Checkbox, Wallet Logo, Bank Logo, Radio, Search Box, Switch, loader-wheel, Country Flag, Indonesian KTP
- **DesignOps Web 胜出 4 组**：Transaction Status, Atome-Logo, Pagination, Top Up
- **两者保留 1 组**：Status（消费者 vs 商户，不同业务语义）
- **非真重复 1 组**：Component 1（仅同名占位，需重命名）
- 输出了统一组件库的架构蓝图（Foundations / Controls / Data Display / Brand Assets / Navigation / Icons / Merchant Specific / Mobile Adaptations 八大分区）
- 规划了 6 阶段执行路线图

**关键决策**:
1. ~~APB [Design System] Web 作为统一库的骨架~~（已废弃：APB 后被 Fox Hu 标记为跳过项目）
2. DesignOps 为统一库核心来源：icon 库(415)、navigation(132)、form(49) 等丰富组件
3. Merchant Centre Library 独立命名空间处理（B2B 与 C2C 分开）
4. ~~Handover 的组件不纳入原子组件库~~（已修正：Handover 确认为重点项目）

### 本阶段资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| REST API | 0 | 纯数据分析，无新调用 |
| MCP 调用 | 0 | 纯数据分析 |

---

## 资源消耗汇总（更新）

| 日期 | MCP 计费 | MCP 免费 | REST API | 剩余额度 |
|------|---------|---------|----------|---------|
| 4/15 | 32 | 3 | ~1,675 | 168/200 |
| 4/16 | 7 | 1 | ~59 | 192/200 |
| **累计** | **39** | **4** | **~1,734** | — |

---

## 关键决策与转折点（更新）

5. **深度提取 50 条限制的发现**（4/16）
   - 发现：深度提取脚本的 componentDetails 每文件只取 50 个，实际有数百到上千个
   - 影响：REST API `/files/:key/components` 端点无限制，可获取完整列表
   - 教训：API 端点选择直接影响数据完整性，要用专用端点而非通用文件端点

6. **APB 的设计规范更现代化**（4/16）
   - 发现：APB [Design System] Web 的变体使用语义化命名（Type=Big, Class=Primary），
     而 DesignOps 混用 Property 1/2 占位名
   - ~~结论：两套体系合并时，APB 为"骨架"，DesignOps 为"补充"~~
   - **修正**：APB 后被 Fox Hu 标记为跳过项目，统一库以 DesignOps 为核心

7. **"containingComponentSet"是去重关键**（4/16）
   - 发现：组件的个体名（如 "Type=Big, Class=Primary"）是变体名，
     `containingComponentSet.name` 才是真正的组件组名（如 "Button"）
   - 影响：必须按组件集聚合后再比较，否则会把同一组件集的变体误判为独立组件
   - 教训：Figma 的组件 = 组件集(ComponentSet) + 变体(Variant) 两层结构

### 阶段 16: "other" 分类细化

**背景**: v1 分类中 2,150 个组件被归为 "other"（49.4%），需要更精确的分类规则。

**方法**:
- 分析 "other" 组件的名称关键词频率分布
- 新增 10 个细分类别：gesture、screen、chart、error-state、payment-flow、kyc-flow、account、security、onboarding、empty-content
- 编写 `scripts/refine-classification.py`，增强分类规则

**结果** (`catalog/classified-v2/`):
- "other" 从 2,150 降至 **595**（"uncategorized"），减少 **72.3%**
- 新增分类 Top 5：payment-flow(347)、screen(247)、kyc-flow(174)、error-state(123)、gesture(71)
- 总分类从 22 种扩展到 **30 种**

**发现**:
- payment-flow (347) 成为第四大分类，验证了支付是产品核心
- gesture (71) 全部来自 open-peeps 手势图标库
- screen (247) 多为页面级截图组件（含 /sub. 前缀）

### 阶段 17: Styles → Variables 迁移方案

**背景**: 所有 12 个文件 Variables = 0，163 个 Token 全部用传统 Styles 管理，无法支持 Light/Dark Mode。

**操作**: 基于现有 Token 数据分析，设计三层 Variable 架构

**结果** (`reports/variables-migration-plan.md`):
- **三层结构**: Primitive（原始值 ~40）→ Semantic（语义别名 ~30，支持 Light/Dark）→ Component（组件级 ~8）
- 发现 100 个颜色 Token 只有 **34 个唯一色值**——大量重复定义
- 字体统一方案：Plus Jakarta Sans（APB）为主，GT Walsheim Pro（DesignOps）为兼容
- 预估实施仅需 **~10 次 MCP 调用**
- 规划了 8 个 Variable Collection

**关键决策**:
- 采用 CSS custom property 风格命名（`text/primary`, `bg/surface`），便于设计开发对接
- Light/Dark Mode 仅在 Semantic 层实现，Primitive 层不分 Mode

### 阶段 18: 增量扫描机制

**背景**: 需要持续监测 Figma 文件变更，但不想每次全量扫描。

**操作**: 编写 `scripts/incremental-scan.sh`
- 通过 REST API 获取每个文件的 `version` 字段
- 与 `reports/scan-versions.json` 中的历史版本对比
- 仅对版本变更的文件重新获取组件列表

**结果**:
- 首次运行建立了 12 个文件的版本基线
- 后续运行只扫描变更文件，预计可减少 80%+ API 调用
- 版本记录保存在 `reports/scan-versions.json`

### 阶段 19: 截图本地化

**背景**: 此前 MCP 截图仅存在响应中，未保存到文件系统。

**操作**:
- 编写 `scripts/download-screenshots.sh`（REST API `GET /v1/images/:key`）
- 对 3 个核心库文件各取 5 个 ComponentSet 缩略图

**结果** (`screenshots/` 目录):
- 下载 **15 张** PNG 截图（@2x 分辨率）
- 覆盖：DesignOps Mobile（tags/icons/tab）、APB Web（KTP/Radio/Pagination）、DesignOps Web（icons/indicator）
- REST API 调用 3 次（images 端点）

### 本阶段资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| REST API (files/components) | 12 | 增量扫描初始化 |
| REST API (files?depth=1) | 12 | 版本检查 |
| REST API (images) | 3 | 截图下载 |
| MCP 调用 | 0 | 本阶段未使用 MCP |

---

## 资源消耗汇总（更新）

| 日期 | MCP 计费 | MCP 免费 | REST API | 剩余额度 |
|------|---------|---------|----------|---------|
| 4/15 | 32 | 3 | ~1,675 | 168/200 |
| 4/16 | 7 | 1 | ~86 | 192/200 |
| **累计** | **39** | **4** | **~1,761** | — |

---

### 阶段 20: 12 人工程评审委员会

**背景**: 项目已完成全部前置任务（19 个阶段），需要多角度评估方案质量和完善度。

**操作**: 邀请 12 位不同领域工程师进行专业评审

**评审人员**:
1. 前端架构师(7.5) | 2. DevOps(6.5) | 3. 数据工程师(8.0) | 4. API工程师(8.5)
5. 安全工程师(5.0) | 6. QA工程师(5.5) | 7. 产品经理(7.0) | 8. AI/ML工程师(6.0)
9. 设计系统工程师(8.0) | 10. 平台工程师(6.5) | 11. 技术写作(7.5) | 12. SRE(5.5)

**综合得分**: **6.8/10**

**关键发现**:
- 最高分(8.5): API 策略——REST API 转向决策获得一致好评
- 最低分(5.0): 安全——PAT 管理、密钥轮换需立即改进
- 共识短板: 零测试代码(QA)、零 CI/CD(DevOps)、零监控(SRE)

**产出**: `reports/engineering-review-panel.md`（含 15 项优先改进建议）

---

### 阶段 21: 工程评审改进项落地

**背景**: 12 人评审产出 15 项改进建议，按优先级逐一落实。

**完成的改进项**:

| # | 改进项 | 产出 | 评审来源 |
|---|--------|------|---------|
| 1 | PAT 移入 .env | `.env` + `.env.example` | 安全工程师 |
| 2 | W3C Token 格式 | `catalog/tokens/w3c-design-tokens.json` | 前端架构师 |
| 3 | 单元测试 22 cases | `tests/test_core.py`（全通过） | QA 工程师 |
| 4 | README 同步 | README.md 完全重写 | 技术写作 |
| 5 | .env.example | 新人可直接复制 | 安全工程师 |
| 6 | Makefile 编排 | `Makefile`（11 个命令） | DevOps 工程师 |
| 7 | API 重试+缓存 | `scripts/lib/figma_api.py` | API 工程师 |
| 8 | Phase 5 三级定义 | `reports/phase5-auto-design-spec.md` | 产品经理 |
| 9 | 组件语义描述 | `catalog/component-descriptions.json`（248 个） | AI/ML 工程师 |

**测试修复过程**:
- 首次 21/22 通过，`KYC/sub.Selfie` 被 screen 规则抢先匹配
- 调整规则优先级：业务流程(kyc-flow/payment-flow) 排在通用 screen 之前
- 新增 `test_classify_onboarding_takes_priority` 验证优先级正确性
- 最终 22/22 全部通过

**关键产出说明**:
- `figma_api.py`: 统一 API 模块，3 次指数退避重试 + 本地 JSON 缓存（1 小时 TTL）+ 429 限流自动等待
- Phase 5 spec: 定义了 L1(线框图) / L2(组件拼装) / L3(像素级还原) 三个级别，含技术路径和前置条件
- 组件描述: 248 个 ComponentSet 的自然语言描述，可直接用于 RAG 检索

### 本阶段资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 调用 | 0 | 纯本地开发 |
| REST API | 0 | 纯本地开发 |

---

## 资源消耗汇总（最终）

| 日期 | MCP 计费 | MCP 免费 | REST API | 剩余额度 |
|------|---------|---------|----------|---------|
| 4/15 | 32 | 3 | ~1,675 | 168/200 |
| 4/16 | 7 | 1 | ~86 | 192/200 |
| **累计** | **39** | **4** | **~1,761** | **161/200** |

---

## 阶段 22: Phase 4 — 统一组件库启动

**时间**: 2026-04-15
**目标**: 在 Atome AI Test 文件中建立统一组件库框架
**fileKey**: `7bnSNqge0DPalc6hJ0XF5U`

### 执行过程

#### Step 1: 检查文件现状
- 文件仅有 1 页（Login Page）和 0 个 Variable Collection
- 发现 **Starter 计划限制 3 页**（原计划 23 页需调整）

#### Step 2: 创建页面结构（3 页 + Section 分区）
- `Foundations`（原 Login Page 重命名）— 色彩/字体/间距示例
- `Components`（新建）— 所有组件，用 7 个 Section 分区
- `Screens`（新建）— 组合示例/演示

Components 页面内 7 个 Section：
| Section | 用途 |
|---------|------|
| Controls | 按钮/输入/开关等 |
| Data Display | 头像/状态/事务 |
| Brand Assets | Logo/国旗/KTP |
| Navigation | 导航栏/菜单 |
| Icons | 图标集 |
| Merchant Specific | 商户定制 |
| Mobile Adaptations | 移动端适配 |

#### Step 3: 创建 Primitive Color Variables（35 个）
- Collection: `Primitives/Color`，单 Mode（Value）
- 从提取的 34 个唯一色值 + 1 个 black 建立色阶
- 分组：gray(10) / brand(3) / green(3) / blue(5) / red(5) / pink(1) / purple(1) / yellow(1) / neutral(2) / black+white(2)
- 每个变量设置了精确的 scopes（不污染选择器）

#### Step 4: 创建 Semantic Color Variables（22 个，Light/Dark Mode）
- Collection: `Semantic/Color`，双 Mode（Light + Dark）
- 所有值通过 `VARIABLE_ALIAS` 引用 Primitive 层（不硬编码）
- 语义分组：
  - `text/*`（7 个）：primary / secondary / disabled / inverse / link / error / success
  - `bg/*`（7 个）：primary / secondary / surface / inverse / brand / error / success
  - `border/*`（4 个）：default / strong / focus / error
  - `interactive/*`（4 个）：default / hover / pressed / disabled
- Dark Mode 自动映射（如 text/primary: Light=black → Dark=white）

#### Step 5: Typography + Spacing（触达限额，未完成）
- 准备好的代码包含：13 个间距、7 个圆角、10 个字号、3 个行高、4 个字重
- 等待额度恢复后继续

### 架构决策

1. **3 页 + Section 替代 23 页**：Starter 限制 3 页，用 Section 分区同样有效
2. **三层 Token 架构**：Primitive → Semantic(alias) → Component(alias)，不硬编码颜色
3. **变量 scopes 精确控制**：text 颜色仅限 TEXT_FILL，背景仅限 FRAME_FILL，避免选择器污染
4. **Light/Dark Mode 从第一天支持**：Semantic 层天然支持主题切换

### 资源消耗

| 类型 | 数量 |
|------|------|
| MCP 调用（成功） | 5 |
| MCP 调用（失败） | 1（页面超限） |
| MCP 调用（限额触达） | 1 |
| 创建页面 | 3 |
| 创建 Section | 7 |
| 创建 Variable Collection | 2（Primitives/Color + Semantic/Color） |
| 创建变量 | 57（35 Primitive + 22 Semantic） |

### 已创建节点 ID 索引

```
页面:
  Foundations: 0:1
  Components: 15:2
  Screens: 15:3

Section:
  Controls: 16:2
  Data Display: 16:3
  Brand Assets: 16:4
  Navigation: 16:5
  Icons: 16:6
  Merchant Specific: 16:7
  Mobile Adaptations: 16:8

Variable Collection:
  Primitives/Color: VariableCollectionId:17:2 (modeId: 17:0)
  Semantic/Color: VariableCollectionId:18:2 (lightModeId: 18:0, darkModeId: 18:1)
```

### 教训：文件必须在组织空间下

旧 POC 文件 `7bnSNqge0DPalc6hJ0XF5U` 属于个人 Starter 团队，仅有 6 次/月 MCP 额度。
5 次成功调用 + 1 次页面超限错误即用尽。

**解决方案**：在组织 `Neuroncredit Pte Ltd` 下创建新文件。

---

## 阶段 23: Phase 4 — 迁移到组织空间 + 完整建设

**时间**: 2026-04-15 (续)
**目标**: 在组织空间新文件中完成统一组件库核心框架
**新 fileKey**: `1nHpzMjQjLzCMO8kMhjL6g`
**文件 URL**: https://www.figma.com/design/1nHpzMjQjLzCMO8kMhjL6g

### 执行过程

#### Step 1: 在组织空间创建新文件
- 使用 `create_new_file` + `organization::1001709743790382367`
- 获得 200 次/天额度

#### Step 2: 重建页面 + Section 结构
- 3 页：Foundations / Components / Screens
- 7 个 Section：Controls / Data Display / Brand Assets / Navigation / Icons / Merchant Specific / Mobile Adaptations

#### Step 3: 创建 4 个 Variable Collection（共 94 变量）

| Collection | 变量数 | Modes | 内容 |
|------------|--------|-------|------|
| Primitives/Color | 35 | Value | 完整色阶 9 组 |
| Semantic/Color | 22 | Light + Dark | text/bg/border/interactive |
| Primitives/Spacing | 20 | Value | 13 间距 + 7 圆角 |
| Primitives/Typography | 17 | Value | 10 字号 + 3 行高 + 4 字重 |

#### Step 4: 构建核心 Controls 组件（共 30 变体）

| 组件 | 变体数 | 属性 |
|------|--------|------|
| Button | 18 | Style(3) × Size(3) × State(2), Label 属性 |
| Checkbox | 4 | Checked(2) × State(2), Label 属性 |
| Radio | 4 | Selected(2) × State(2), Label 属性 |
| Switch | 4 | Toggle(2) × State(2) |

所有组件颜色均通过 Semantic Variable 绑定，支持 Light/Dark Mode 自动切换。

#### Step 5: Foundations 展示页

创建三大展示区：
1. **Color Palette** — 5 组原始色阶（Gray/Brand/Green/Blue/Red），每色带标签
2. **Semantic Colors (Light Mode)** — Text/Background/Border/Interactive 四大分组
3. **Typography Scale** — 10 级字号从 xs(10px) 到 6xl(40px)

### 资源消耗

| 类型 | 数量 |
|------|------|
| MCP 调用（成功） | 12 |
| MCP 调用（失败） | 1（Switch layoutSizing 顺序） |
| 创建文件 | 1 |
| 截图验证 | 3 |
| 创建页面 | 3 |
| 创建 Section | 7 |
| 创建 Variable Collection | 4 |
| 创建变量 | 94 |
| 创建组件集 | 4 |
| 创建变体 | 30 |

### 已创建节点 ID 索引（新文件）

```
文件: 1nHpzMjQjLzCMO8kMhjL6g

页面:
  Foundations: 0:1
  Components: 1:2
  Screens: 1:3

Section (Components 页面):
  Controls: 1:4
  Data Display: 1:5
  Brand Assets: 1:6
  Navigation: 1:7
  Icons: 1:8
  Merchant Specific: 1:9
  Mobile Adaptations: 1:10

Variable Collection:
  Primitives/Color: VariableCollectionId:2:2 (modeId: 2:0)
  Semantic/Color: VariableCollectionId:3:2 (lightModeId: 3:0, darkModeId: 3:1)
  Primitives/Spacing: VariableCollectionId:4:2 (modeId: 4:0)
  Primitives/Typography: VariableCollectionId:4:23 (modeId: 4:0)

组件集:
  Button: 6:38 (18 变体)
  Checkbox: 7:16 (4 变体)
  Radio: 7:31 (4 变体)
  Switch: 9:14 (4 变体)

展示节点 (Foundations):
  Color Palette: 10:2
  Semantic Colors: 11:2
  Typography Scale: 11:76
```

---

## 阶段 24: Phase 4 — 扩展组件集

**时间**: 2026-04-16
**目标**: 补充 Avatar / Status Badge / Input / SearchBox / Pagination / Navigation 组件
**文件**: `1nHpzMjQjLzCMO8kMhjL6g`（已移入 🤖 Atome AI Test 项目）

### 文件位置修正

用户确认测试项目为 `project/587185541`（🤖 Atome AI Test）。
`create_new_file` API 只能创建到 Drafts，用户已手动移动到项目中。
已更新 AGENTS.md 记录正确的项目路径。

### 新增组件

| 组件 | 分区 | 变体数 | 属性/说明 |
|------|------|--------|----------|
| Avatar | Data Display | 6 | Type(Image/Initial) × Size(SM/MD/LG)，Initials 文本属性 |
| Status Badge | Data Display | 5 | Success/Pending/Failed/Loading/Cancelled，带状态圆点 |
| Input | Controls | 5 | Default/Focused/Filled/Error/Disabled，带 Label + Error Message |
| Search Box | Controls | 5 | Inactive/Active/Typing/Filled/Disabled，带搜索图标 |
| Pagination | Controls | 3 | Default(第1页)/Middle(第5页)/End(末页)，省略号分页 |
| Bottom Navigation | Navigation | 4 | Active=Home/Shop/Activity/Profile，底部 Tab 栏 |

所有组件颜色均通过 Semantic Variable 绑定，支持 Light/Dark Mode 自动切换。

### 资源消耗

| 类型 | 数量 |
|------|------|
| MCP 调用（成功） | 4（创建组件） |
| 截图验证 | 3 |
| 总计 | 7 |

### 更新节点 ID 索引

```
新增组件集:
  Avatar: 15:14 (6 变体) — Data Display 区
  Status Badge: 16:17 (5 变体) — Data Display 区
  Input: 17:23 (5 变体) — Controls 区
  Search Box: 17:39 (5 变体) — Controls 区
  Pagination: 18:51 (3 变体) — Controls 区
  Bottom Navigation: 18:104 (4 变体) — Navigation 区
```

### 累计统计

| 项目 | 数量 |
|------|------|
| Variable Collection | 4 |
| 变量总数 | 94 |
| 组件集 | **10** |
| 变体总数 | **58** |
| 展示区 | 3（色板 + 语义色 + 字体） |

---

## 阶段 25: Phase 4 — 完善主流程场景

**时间**: 2026-04-16
**目标**: 补齐 Brand Assets、交互组件、完整页面示例

### 新增组件

| 组件 | 分区 | 变体数 | 说明 |
|------|------|--------|------|
| Atome-Logo | Brand Assets | 6 | Color(3) × Plus(2) |
| Bank Logo | Brand Assets | 6 | BCA/BNI/BRI/Jago/Jenius/Mandiri |
| Wallet Logo | Brand Assets | 7 | OVO/GoPay/Dana/ShopeePay/LinkAja/iSaku/AstraPay |
| Country Flag | Brand Assets | 6 | ID/PH/MY/TH/VN/SG |
| Transaction Card | Data Display | 3 | Success/Pending/Failed |
| Info Card | Data Display | 3 | Default(阴影)/Highlighted(品牌色)/Outlined |
| Modal | Controls | 3 | Confirm/Alert/Info |
| Toast | Controls | 4 | Success/Error/Info/Warning |
| Top App Bar | Navigation | 3 | Default/WithBack/Search |
| List Item | Controls | 3 | Default/WithDescription/Simple |
| Tab Bar | Navigation | 3 | Two/Three/Four tabs |

### 完整页面示例

| 页面 | 节点 ID | 包含元素 |
|------|---------|---------|
| Home Screen | 25:2 | Logo + 额度卡 + 快捷操作 + 交易列表 + 底部导航 |
| Transaction Detail | 26:2 | 返回栏 + 成功状态 + 订单详情 + 分期计划 + CTA |

### 资源消耗

| 类型 | 数量 |
|------|------|
| MCP 调用（成功） | 5（组件创建） |
| MCP 调用（失败） | 2（effects缺blendMode + layoutSizing顺序） |
| 截图验证 | 3 |
| 总计 | 10 |

### 新增节点 ID 索引

```
Brand Assets:
  Atome-Logo: 19:14 (6 变体)
  Bank Logo: 19:27 (6 变体)
  Wallet Logo: 19:42 (7 变体)
  Country Flag: 19:61 (6 变体)

Data Display (新增):
  Transaction Card: 22:26 (3 变体)
  Info Card: 22:36 (3 变体)

Controls (新增):
  Modal: 23:22 (3 变体)
  Toast: 23:35 (4 变体)
  List Item: 24:31 (3 变体)

Navigation (新增):
  Top App Bar: 24:14 (3 变体)
  Tab Bar: 24:56 (3 变体)

Screens:
  Home Screen: 25:2
  Transaction Detail: 26:2
```

---

## 阶段 26: Phase 4 — 模板库扩展（Day 2）

**日期**: 2026-04-16
**目标**: 丰富组件库覆盖面，补充表单、反馈、内容、覆盖层组件和更多页面示例。

### 新增组件

#### Form 组件（3 个组件集，14 变体）

| 组件 | 节点 ID | 变体数 | 变体说明 |
|------|---------|--------|---------|
| OTP Input | 28:82 | 6 | Digits(4/6) × State(Default/Filled/Error) |
| Dropdown | 29:35 | 4 | Closed/Open/Selected/Disabled |
| Stepper | 30:26 | 4 | Default/Min/Max/Disabled |

#### Feedback 组件（4 个组件集，20 变体）— 新增 Feedback Section

| 组件 | 节点 ID | 变体数 | 变体说明 |
|------|---------|--------|---------|
| Progress Bar | 31:33 | 6 | Type(Default/Slim) × Progress(25%/50%/75%/100%) |
| Skeleton Loader | 31:48 | 3 | Card/Text/Avatar |
| Empty State | 32:28 | 4 | NoData/NoResults/Error/NoNetwork |
| Chip | 32:45 | 7 | Style(Default/Brand/Error/Warning/Info) × Closable |

#### Content 组件（3 个组件集，12 变体）

| 组件 | 节点 ID | 变体数 | 变体说明 |
|------|---------|--------|---------|
| Product Card | 33:36 | 4 | Default/WithDiscount/WithInstalment/Full |
| Merchant Card | 33:75 | 4 | Default/WithRating/WithTag/Full |
| Banner | 34:42 | 4 | Brand/Purple/Orange/Dark |

#### Overlay 组件（3 个组件集，9 变体）

| 组件 | 节点 ID | 变体数 | 变体说明 |
|------|---------|--------|---------|
| Bottom Sheet | 35:43 | 3 | List/Form/Confirm |
| Action Sheet | 36:33 | 3 | Share/Destructive/Report |
| Tooltip | 36:46 | 3 | Top/Bottom/Left |

### 新增页面示例（4 个）

| 页面 | 节点 ID | 展示场景 |
|------|---------|---------|
| Login Screen | 37:2 | 登录 → Logo/手机号/密码/第三方登录/注册入口 |
| KYC Verification | 38:2 | 身份验证 → 步骤进度/证件上传/拍照提示 |
| Payment Screen | 39:2 | 支付确认 → 订单摘要/分期方案/支付方式/CTA |
| Shop Screen | 40:2 | 商城浏览 → 搜索/分类Tab/Banner/产品网格/导航 |

### 资源消耗

| 类型 | 数量 |
|------|------|
| MCP use_figma（成功） | 12 |
| MCP use_figma（失败） | 0 |
| 截图验证 | 2 |
| 文件检查 | 1 |
| 总计 | 15 |

### 决策记录

1. **新增 Feedback Section** — 之前没有专门的反馈组件分区，新建 Section 放置 Progress Bar、Skeleton、Empty State、Chip
2. **Product Card 和 Merchant Card** 放入 Data Display 而非新分区 — 保持分类简洁
3. **Bottom Sheet 和 Action Sheet** 放入 Controls — 属于交互控制类组件
4. **Banner** 放入 Data Display — 属于内容展示类
5. **所有新 Screen 按业务流排列** — Login → KYC → Shop → Payment，覆盖注册登录、风控、购物、支付四大核心场景

---

## 待完成任务

| 优先级 | 任务 | 状态 |
|--------|------|------|
| ~~P0~~ | ~~Phase 4: 统一组件库~~ | ✅ 完成 |
| ~~P1~~ | ~~Phase 4: 模板库扩展~~ | ✅ 完成 |
| P1 | Phase 4: 组件库发布为团队库 | 待做（用户要求不急） |
| P0 | Phase 5: 需求描述 → 自动出图 | 方案已定义（L1/L2/L3） |

### Phase 4 完整组件清单（34 个组件集，160 个变体）

| 组件 | 变体 | 分区 |
|------|------|------|
| Button | 18 | Controls |
| Checkbox | 4 | Controls |
| Radio | 4 | Controls |
| Switch | 4 | Controls |
| Input | 5 | Controls |
| Search Box | 5 | Controls |
| Pagination | 3 | Controls |
| Modal | 3 | Controls |
| Toast | 4 | Controls |
| List Item | 3 | Controls |
| OTP Input | 6 | Controls |
| Dropdown | 4 | Controls |
| Stepper | 4 | Controls |
| Bottom Sheet | 3 | Controls |
| Action Sheet | 3 | Controls |
| Tooltip | 3 | Controls |
| Avatar | 6 | Data Display |
| Status Badge | 5 | Data Display |
| Transaction Card | 3 | Data Display |
| Info Card | 3 | Data Display |
| Product Card | 4 | Data Display |
| Merchant Card | 4 | Data Display |
| Banner | 4 | Data Display |
| Progress Bar | 6 | Feedback |
| Skeleton Loader | 3 | Feedback |
| Empty State | 4 | Feedback |
| Chip | 7 | Feedback |
| Bottom Navigation | 4 | Navigation |
| Top App Bar | 3 | Navigation |
| Tab Bar | 3 | Navigation |
| Atome-Logo | 6 | Brand Assets |
| Bank Logo | 6 | Brand Assets |
| Wallet Logo | 7 | Brand Assets |
| Country Flag | 6 | Brand Assets |
| **合计** | **160** | |

### 完整页面示例（6 个）

| 页面 | 展示场景 |
|------|---------|
| Home Screen | 主页 → 额度/快捷入口/交易列表/导航 |
| Transaction Detail | 交易详情 → 状态/订单信息/分期计划 |
| Login Screen | 登录 → Logo/手机号密码/第三方/注册入口 |
| KYC Verification | 身份验证 → 步骤进度/证件上传 |
| Payment Screen | 支付确认 → 订单/分期/支付方式 |
| Shop Screen | 商城 → 搜索/分类/Banner/产品网格 |

---

## 阶段 27: 工程结构重整

**日期**: 2026-04-16
**目标**: 清理过期文件、消除冗余、统一命名、优化目录层次。

### 执行操作

| # | 操作 | 变更 |
|---|------|------|
| 1 | .gitignore 补全 | 添加 `__pycache__/`、`.pytest_cache/`、`reports/.api-cache/` |
| 2 | 清理 `__pycache__/` | 删除 scripts/ 和 tests/ 下的编译缓存 |
| 3 | 合并 classified 索引 | v1 的 `by-type/`(22种) 替换为 v2(30种)，保留 v1 的 by-module/by-platform/by-system |
| 4 | 清理旧索引 | 删除 `classified-v2/` 目录、旧 `classified-index.json`(v1)、旧 `by-type-platform/` |
| 5 | 清理空目录 | 删除 `catalog/by-business/`、`by-country/`、`by-flow/`、`by-project/` (空) |
| 6 | `taxonomy.json` 归位 | 根目录 → `catalog/taxonomy.json` |
| 7 | 脚本分组 | 6 个已废弃脚本移入 `scripts/legacy/` |
| 8 | 文档归位 | `scripts/batch-runner.md` → `docs/batch-runner.md` |
| 9 | 扫描数据归组 | 9 个 `*-scan.json` 从 `reports/extractions/` 移入 `reports/extractions/scans/` |
| 10 | 脚本路径更新 | `scan-rest-api.sh`、`build-index.js`、`refine-classification.py` 路径同步 |
| 11 | README.md 重写 | 项目结构树完全重新绘制，阶段 14 标记为 ✅ |

### 重整前后对比

```
重整前:
├── taxonomy.json              ← 游离在根目录
├── catalog/
│   ├── classified/            ← v1（22 种类型 + 过期交叉索引）
│   ├── classified-v2/         ← v2（30 种类型，与 v1 并存）
│   ├── classified-index.json  ← v1 索引
│   ├── classified-index-v2.json ← v2 索引
│   ├── by-business/           ← 空
│   ├── by-country/            ← 空
│   └── ...
├── scripts/
│   ├── pilot-test.js          ← 废弃脚本混在活跃脚本中
│   ├── batch-runner.md        ← 文档混在脚本中
│   └── __pycache__/           ← 编译缓存
└── reports/extractions/
    ├── designops-scan.json    ← 9 个 scan 松散堆放
    ├── components/
    └── deep/

重整后:
├── catalog/
│   ├── taxonomy.json          ← 归位
│   ├── classified/            ← 合并：v2 by-type + v1 by-module/platform/system
│   ├── classified-index.json  ← 唯一索引
│   └── ...（干净）
├── scripts/
│   ├── (10 个活跃脚本)
│   ├── lib/                   ← 共享库
│   └── legacy/                ← 6 个废弃脚本
├── docs/
│   └── batch-runner.md        ← 归位
└── reports/extractions/
    ├── scans/                 ← 9 个 scan 归组
    ├── components/
    └── deep/
```

### 验证

- 22/22 单元测试全部通过
- 所有脚本路径引用已同步更新
- `make test` 正常运行

---

## 项目全局总结

> 随项目进展持续更新

### 项目概况

| 指标 | 数值 |
|------|------|
| 项目名称 | Atome UED Figma 全量素材库 |
| 时间跨度 | 2 天（2026-04-15 ~ 04-16） |
| 完成阶段 | 26 个 |
| Figma 项目数 | 12 个 |
| 源文件总数 | 555 个（544 成功扫描） |
| 高价值文件 | 14 个（有已发布组件/样式） |
| 深度提取文件 | 12 个 |

### 核心产出

#### 统一组件库（Figma 文件 `1nHpzMjQjLzCMO8kMhjL6g`）

| 资产类型 | 数量 | 明细 |
|----------|------|------|
| Variable Collection | 4 | Primitives/Color(35) + Semantic/Color(22) + Primitives/Spacing(20) + Primitives/Typography(17) |
| 变量总数 | 94 | 含 Light/Dark 双 Mode 语义色 |
| 组件集 | 34 | 分布在 6 个 Section |
| 组件变体 | 160 | 覆盖 Controls/Data Display/Feedback/Brand/Navigation |
| 页面示例 | 6 | Home/Transaction/Login/KYC/Payment/Shop |
| Section 分区 | 8 | Controls/Data Display/Brand Assets/Navigation/Feedback/Icons/Merchant Specific/Mobile Adaptations |

#### 本地数据资产

| 资产 | 路径 | 说明 |
|------|------|------|
| 项目文件清单 | `sources/*.json` | 12 个项目的文件 ID 列表 |
| Catalog 扫描 | `reports/extractions/*-scan.json` | 544 文件的结构+组件+样式 |
| 深度提取 | `reports/extractions/deep/*.json` | 12 个高价值文件完整属性 |
| 全量组件列表 | `reports/extractions/components/*.json` | 4,348 个组件完整信息 |
| 统一索引 | `catalog/assets.json` | 全量聚合索引 |
| Design Token (原始) | `catalog/tokens/design-tokens.json` | 163 个 Token（100 色+58 字+5 效） |
| Design Token (W3C) | `catalog/tokens/w3c-design-tokens.json` | W3C 标准格式 |
| 分类索引 v2 | `catalog/classified-v2/` | 30 种分类，595 未分类 |
| 组件描述 | `catalog/component-descriptions.json` | 248 个组件的自然语言描述 |
| 截图 | `screenshots/` | 15 张 PNG + MCP 截图 28 张 |

#### 报告文档

| 文件 | 说明 |
|------|------|
| `reports/tool-audit-report.md` | 17 个 MCP 工具全量测试报告 |
| `reports/uiux-feasibility-review.md` | 6 角色 UI/UX 可行性评估（7.2/10） |
| `reports/engineering-review-panel.md` | 12 人工程评审（6.8/10） |
| `reports/component-dedup-report.md` | 跨体系组件去重分析 |
| `reports/version-selection-plan.md` | 17 组重复组件主版本裁决方案 |
| `reports/variables-migration-plan.md` | Styles → Variables 三层迁移方案 |
| `reports/phase5-auto-design-spec.md` | Phase 5 自动出图 L1/L2/L3 规格 |
| `reports/operation-log.md` | 本文档 — 完整操作记录 |

#### 脚本工具

| 脚本 | 用途 |
|------|------|
| `scripts/discover-files.sh` | REST API 文件发现 |
| `scripts/scan-rest-api.sh` | REST API 批量扫描 |
| `scripts/deep-extract.sh` | REST API 深度提取 Wave 1 |
| `scripts/deep-extract-wave2.sh` | REST API 深度提取 Wave 2 |
| `scripts/fetch-components.sh` | REST API 全量组件获取 |
| `scripts/build-index.js` | 统一索引构建 |
| `scripts/component-dedup.py` | 组件去重分析 |
| `scripts/build-classified-index.py` | 多维分类索引 |
| `scripts/refine-classification.py` | 分类细化（v1→v2） |
| `scripts/incremental-scan.sh` | 增量扫描（版本比对） |
| `scripts/download-screenshots.sh` | REST API 截图下载 |
| `scripts/lib/figma_api.py` | 统一 API 模块（重试+缓存） |
| `tests/test_core.py` | 22 个单元测试 |
| `Makefile` | 11 个编排命令 |

### 资源消耗总计

| 资源 | Day 1 | Day 2 | 累计 |
|------|-------|-------|------|
| MCP 计费调用 | 32 | ~33 | ~65 |
| MCP 免费调用 | 3 | ~2 | ~5 |
| REST API 调用 | ~1,675 | ~125 | ~1,800 |

### 关键问题与解决方案

| # | 问题 | 原因 | 解决方案 |
|---|------|------|---------|
| 1 | Plugin API 无法操作组织文件 | 用户在组织文件只有 View 权限，`use_figma` 需 Edit | 转用 REST API（只需 View + PAT，无日调用限制） |
| 2 | Starter 计划 6 次/月限额 | 旧文件属于个人团队（Starter），MCP 按文件所属团队计费 | 在组织空间新建文件，走 200 次/天的组织额度 |
| 3 | 文件无法从 Drafts 移到项目 | Figma 无公开的"移动文件"API | 用户手动在 Figma UI 拖拽到目标项目 |
| 4 | Starter 限 3 页 | 计划 23 页超限 | 改为 3 页 + 7 Section 分区方案 |
| 5 | DROP_SHADOW 缺 blendMode | API 文档未明确，effects 验证失败 | 补充 `blendMode: 'NORMAL'` |
| 6 | layoutSizing 设置报错 | 必须先设 layoutMode，FILL 需在 appendChild 之后 | 严格遵循 layoutMode → appendChild → layoutSizing 顺序 |
| 7 | 深度提取限 50 组件/文件 | 通用文件端点返回量有限 | 改用专用端点 `GET /v1/files/:key/components`（无限制） |
| 8 | 发现第二套设计系统 APB | 全量扫描发现 1,682 组件的独立体系 | 5 维评分裁决主版本（APB 后被标记为跳过，策略需调整） |

### 关键决策记录

1. **Plugin API → REST API 转向**：View 权限无法用 Plugin API，REST API 反而更适合批量提取
2. **~~APB 为统一库骨架~~**（已废弃）：APB 后被 Fox Hu 标记为跳过项目，统一库策略改为以 DesignOps 为核心
3. **三层 Token 架构**：Primitive → Semantic(alias, Light/Dark) → Component(alias)
4. **3 页 + Section 替代 23 页**：规避页面限制，实际效果相同
5. **先打地基再建库**：完善主流程场景后再发布，不急于求成
6. **"other" 从 49.4% 降至 13.7%**：通过增加业务流程分类规则大幅减少未分类
7. **97.5% 文件无设计资产**：聚焦 14 个核心文件，避免全量处理的浪费
8. **项目范围精简**：Fox Hu 确认重点项目为 Handover、DesignOps、Flow Library、Online Integration（4 个）；跳过 APB、Research & Exploration、Design QA（3 个）

---

## Stage 28: 项目范围精简 — 按设计师 Fox Hu 的标注重整方案

**日期**: 2026-04-15
**触发**: 用户向 UI 工程师 Fox Hu 确认"哪些项目有新旧体系或以哪个为主"
**MCP 调用**: 0（纯文档/数据分析操作）

### 背景

Fox Hu 确认的项目优先级：
- **重点项目（4 个）**：Handover、DesignOps、Flow Library、Online Integration
- **跳过项目（3 个）**：APB、Research & Exploration、Design QA

### 操作内容

#### Step 1: 范围影响分析

| 分类 | 项目数 | 文件数 | 已提取组件 |
|------|--------|--------|-----------|
| 重点项目（Handover/DesignOps/Flow Library/Online Integration） | 4 | 101 | 2,668 |
| 跳过项目（APB/Research & Exploration/Design QA） | 3 | - | - |

> 注：此表为 Stage 28 时的初始分析。项目分类后经用户确认修正——APB 从重点移至跳过。

#### Step 2: Handover 定位修正

**旧定位**："Handover 仅作参考，不纳入组件库"
**新定位**："Handover 是重点项目，包含实际交付的 Screen Library + Style Guide"

原因：Fox Hu 确认 Handover 为重点项目。分析其 1,612 个组件：
- 1,139 个 "other" 类 → 页面级设计稿/插图（Screen library 中的画面）
- 473 个明确 UI 类型 → voucher(116)、modal(66)、card(64)、input(48) 等
- 代表**实际落地到开发的设计规范**，与 DesignOps 的"设计系统"互补

#### Step 3: 识别数据缺口

以下重点项目存在严重数据缺口：

| 项目 | 文件数 | 已提取文件 | 提取率 | 状态 |
|------|--------|-----------|--------|------|
| Atome Design token | 待确认 | 0 | 0% | source 清单为空，需与 UI 工程师确认 |
| Online Integration | 21 | 0 | 0% | 未进行任何深度提取 |
| Flow Library | 31 | 1 | 3.2% | 仅提取了 1 个文件 (19 组件) |
| *(对比) Handover* | *33* | *2* | *6%* | *1,504 组件* |
| *(对比) DesignOps* | *16* | *4* | *25%* | *1,145 组件* |

> 注：APB 在后续确认中被标记为跳过项目，不再列入此对比。

#### Step 4: 文档更新

- ✅ `docs/figma-core-concepts.md` — 更新为"四个重点项目+三个跳过项目"
- ✅ `AGENTS.md` — 项目概述、Workspace Facts 更新
- ✅ `README.md` — 项目范围说明精简
- ✅ `reports/component-dedup-report.md` — 修正第 3 条结论关于 Handover 的定性

### 下一步：数据补充扫描计划

**优先级排序**：

1. **P0 — Atome Design token**
   - 问题：sources 清单中 0 个文件，可能是 REST API 未扫描到
   - 行动：向 UI 工程师确认该项目是否有文件、是否权限受限
   - 预期收益：可能包含统一的 token 定义，直接对接三层 Variable 架构

2. **P1 — Online Integration（21 文件）**
   - 问题：完全没有提取任何数据
   - 行动：用 REST API 批量扫描 + 对有组件的文件做深度提取
   - 预期收益：合作伙伴集成界面的设计模式和组件
   - 注意：大量文件是 2022 年的归档（Amazon/Lazada 等），活跃文件约 5-6 个

3. **P2 — Flow Library（31 文件，仅 1 个提取）**
   - 问题：31 个文件中只提取了 1 个（Happy flow）
   - 行动：扫描剩余 30 个文件，重点关注最近更新的：
     - Atome APP Happy Flow (2026-04)
     - Cash Masterfile (2026-02)
     - Happy flow | All countries (2025-10)
   - 预期收益：完整的用户操作流程模式

---

## Stage 29: 补充扫描 — 三个数据缺口项目

**日期**: 2026-04-16
**MCP 调用**: 0（全部使用 REST API）
**REST API 调用**: ~156 次（Online Integration 63 + Flow Library 93）

### 扫描执行

#### 1. Atome Design token（P0）

**方法**: REST API `GET /v1/projects/587275263/files`
**结果**: **项目为空，0 个文件**

该项目在 Figma 中存在但没有任何文件。可能的原因：
- Token 定义已合并到 APB 或 DesignOps 中
- 项目已迁移但名称保留
- 需向 UI 工程师确认

#### 2. Online Integration（P1）

**方法**: `scan-rest-api.sh` 批量扫描 21 个文件
**结果**:
- 20/21 成功，1 超时（Gateway Configuration）
- **0 组件，0 样式** — 所有 21 个文件均无已发布组件或样式
- 内容性质：合作伙伴集成的纯设计稿（Amazon、Lazada、TikTok、DBS 等）
- 页面级参考价值：Merchant integration Guideline (72 节点)、Tiktok x Atome (64 节点)

#### 3. Flow Library（P2）

**方法**: `scan-rest-api.sh` 批量扫描 31 个文件
**结果**:
- 30/31 成功，1 超时（Cash Masterfile）
- **19 组件，0 样式** — 仅 "Happy flow | All countries (updated)" 1 个文件有组件
- 该文件此前已做过深度提取，无新增
- 页面级参考价值丰富：
  - 🐉 UX Flow | Onboarding | All Countries (4583 节点)
  - All countries User Flow (33 页, 474 节点)
  - Atome APP Happy Flow (48 页, 364 节点)

### 扫描汇总

| 项目 | 文件数 | 成功 | 已发布组件 | 已发布样式 | 高价值文件 |
|------|--------|------|-----------|-----------|-----------|
| Atome Design token | 0 | - | 0 | 0 | 0 |
| Online Integration | 21 | 20 | 0 | 0 | 0 |
| Flow Library | 31 | 30 | 19 | 0 | 1（已提取） |

### 核心发现

**组件分布**（注：APB 后被标记为跳过项目）：

| 项目 | 组件 | 样式 | 价值类型 | 状态 |
|------|------|------|---------|------|
| Handover | 1,504 | 0 | 页面级组件 + Screen Library | 重点 |
| DesignOps | 1,145 | 68 | 原子组件 + 设计系统 | 重点 |
| APB | 1,682 | 43 | 原子组件 + 设计系统 | **已跳过** |
| Flow Library | 19 | 0 | 流程连接器组件 | 重点 |
| Online Integration | 0 | 0 | 纯页面级设计稿 | 重点（参考） |

**两层价值体系**：
1. **组件层**（可直接复用）：DesignOps + Handover Screen Library → 2,649 组件（重点项目范围内）
2. **参考层**（页面级模式）：Flow Library 用户流程 + Online Integration 集成方案 → 无独立组件但有丰富的页面布局参考

### 索引更新

重新构建 `catalog/assets.json`：542 文件，4,351 组件，111 样式，14 高价值文件。

### UI 工程师确认结果

1. **Atome Design token** — 不在重点关注范围，直接忽略（空项目）。
2. **Online Integration** — 定位为后续**生成页面时的参考标准**，不用于组件提取。
   内含 Amazon、Lazada、TikTok、DBS PayLah 等合作方的集成界面设计稿。

### 最终项目范围

| 用途 | 项目 | 组件 | 说明 |
|------|------|------|------|
| 组件提取 | Handover | 1,504 | Screen Library + 实际交付规范 |
| 组件提取 | DesignOps | 1,145 | 设计系统，统一库核心来源 |
| 流程参考 | Flow Library | 19 | 用户操作流程图 |
| 页面参考 | Online Integration | 0 | 自动出图时的页面参考标准 |

> APB（1,682 组件）已被 Fox Hu 标记为跳过，不纳入最终范围。

---

## Stage 30: Phase 5 前置准备 — 页面模板 + 组件共现 + 参考索引

**日期**: 2026-04-16
**MCP 调用**: 0（纯本地数据分析）

### 目标

为 Phase 5（需求 → 自动出图）构建三大核心数据资产：
1. 页面模板 — 定义每种页面类型包含哪些屏幕和组件
2. 组件共现矩阵 — 哪些 UI 类型经常一起出现
3. Online Integration 参考索引 — 集成场景的页面布局模式

### 产出

#### 1. 页面模板 (`catalog/page-templates.json`)

从 Handover Screen Library（1,477 组件 / 9 国家 / 1,788 节点）和
Flow Library Happy Flow（48 页）中提取 5 个核心页面模板：

| 模板 | 屏幕数 | 关联组件类型 | 平台 |
|------|--------|------------|------|
| **Login** | 7 | input(73), button(3), error-state(7) | Mobile + Web |
| **KYC** | 12 | kyc-flow(174), input(56), error-state(68), modal(50) | Mobile |
| **Home** | 5 | navigation(75), card(8), voucher(9), list(4) | Mobile |
| **Payment** | 12 | payment-flow(260), card(42), modal(41), voucher(24) | Mobile + Web |
| **Profile** | 9 | list(55), modal(108), account(68), icon(73) | Mobile + Web |

每个模板包含：
- 屏幕列表（必选/可选标记）
- 关联的组件类型及数量
- Mobile 和 Web 端的布局结构描述

数据来源分析：
- Handover Mobile 的页面命名遵循 `{国家}/{流程}/{子页面}` 格式
- 最高频流程：KYC(28 screens) > LogIn(23) > Payment(21) > Home(5)
- Web 端以 Payment 相关为主：PaymentConfirmation(24) > Profile(20)

#### 2. 组件共现矩阵 (`catalog/component-co-occurrence.json`)

分析 30 种 UI 类型在 12 个文件中的共现关系：

Top 5 共现对：
- icon ↔ uncategorized: 8（图标几乎与所有类型共现）
- button ↔ icon: 8（按钮 + 图标最常见搭配）
- form ↔ icon: 7
- icon ↔ toast: 7
- card ↔ icon: 6

#### 3. Online Integration 参考索引 (`catalog/online-integration-reference.json`)

17 个有效文件（筛除节点 < 5 的文件），993 个顶层节点：
- Amazon x Atome (308 nodes) — 最大的集成参考
- Merchant integration Guideline (72 nodes, 8 pages) — 集成规范文档
- Tiktok x Atome (64 nodes, 10 pages) — TikTok 集成设计
- APP guideline (57 nodes) — App 设计规范

### Phase 5 资产就绪度

| 资产 | L1 线框图 | L2 组件拼装 | 状态 |
|------|----------|-----------|------|
| 页面模板 (5 模板 / 45 屏幕) | ✅ | ✅ | **本次完成** |
| 组件共现矩阵 | — | ✅ | **本次完成** |
| Online Integration 参考 | ✅ | ✅ | **本次完成** |
| 分类索引 (30 种 UI 类型) | ✅ | ✅ | 已有 |
| 组件语义描述 (248 个) | — | ✅ | 已有 |
| 统一组件库 (34 组件集) | — | ✅ | 已有 |
| Variables (94 变量) | — | ✅ | 已有 |

**结论**: L1 线框图所需数据资产已全部就绪，可进入实现阶段。

---

## Stage 31: DesignOps 核心策略重建

**日期**: 2026-04-16
**触发**: 用户确认 Fox Hu 的项目分类——APB 为跳过项目，之前"APB 为骨架"的策略全部作废
**MCP 调用**: 0（纯文档/数据分析操作）

### 背景

原方案中 17 组去重裁决有 11 组选了 APB Web 作为主版本，统一组件库以 APB 为骨架。
APB 被标记为跳过后，这些结论全部需要翻转。

### 操作内容

#### Step 1: 去重裁决翻转

`reports/version-selection-plan.md` 中 11 组原 APB 主版本全部改为 DesignOps Web：

| 组件 | 原主版本 | 新主版本 |
|------|---------|---------|
| Button | APB Web | DesignOps Web（24 变体） |
| Avatar | APB Web | DesignOps Web（4 变体） |
| Checkbox | APB Web | DesignOps Web（8 变体） |
| Wallet Logo | APB Web | DesignOps Web（需补 ShopeePay/LinkAja） |
| Bank Logo | APB Web | DesignOps Web |
| Radio | APB Web | DesignOps Web |
| Search Box | APB Web | DesignOps Web（需后补 Filled 状态） |
| Switch | APB Web | DesignOps Web |
| loader-wheel | APB Web | DesignOps Web |
| Country Flag | APB Web | DesignOps Web |
| Indonesian KTP | APB Web | DesignOps Web |

Status 组件原为"两者保留"（Consumer + Merchant），APB 跳过后仅保留 DesignOps Merchant 版。
Component 1 原为"两者保留重命名"，APB 跳过后仅保留 DesignOps 版（TreeLevel）。

#### Step 2: Token/字体策略调整

`reports/variables-migration-plan.md` 更新：
- 字体：GT Walsheim Pro + Plus Jakarta Sans **并存**，待设计师最终定夺（不再指定单一主字体）
- 颜色 Token：APB 来源 40 个标记为参考保留，DesignOps 55 个为统一库主要来源

#### Step 3: 数据资产标记

- `catalog/classified-index.json` — 添加 scopeNote 说明 APB 为参考
- `catalog/classified/by-system/APB.json` — 添加 status: reference-only
- `catalog/tokens/w3c-design-tokens.json` — 元数据添加来源标记说明

#### Step 4: 统一库架构调整

新架构全部以 DesignOps 为来源：
- Controls: Button/Checkbox/Radio/Switch/SearchBox/Pagination/loader-wheel ← 全部 DesignOps Web
- Data Display: Avatar/Transaction Status/Status ← DesignOps
- Brand Assets: Atome-Logo/Bank Logo/Wallet Logo/Country Flag/Indonesian KTP ← DesignOps Web
- Navigation: 132 个组件 ← DesignOps 独有
- Icons: 415 个 ← DesignOps 独有

### 决策

1. APB 数据**保留为参考**（不删除），方便后续设计师如需查阅
2. 字体**不指定主从关系**，两套并存待设计师决定
3. 需补充的缺口：Wallet Logo 补 ShopeePay/LinkAja、Search Box 补 Filled 状态、Status 补 Consumer 版

#### Step 5: Atome AI Test 统一组件库评估

使用 `use_figma` 检查现有组件库（fileKey: `1nHpzMjQjLzCMO8kMhjL6g`），结构如下：

**页面**: Foundations / Components / Screens
**Variable Collections**: 4 个（Primitives/Color 35 变量, Semantic/Color 22 变量含 Light/Dark, Spacing 20, Typography 17）
**组件集**: 34 个，160+ 变体，分布在 8 个 Section 中

评估结论：

| 类别 | 组件 | 影响 | 处理 |
|------|------|------|------|
| 通用 UI（不依赖 APB/DesignOps） | Button, Input, Modal, Toast, List Item, OTP Input, Dropdown, Stepper, Bottom Sheet, Action Sheet, Tooltip, Progress Bar, Skeleton Loader, Empty State, Chip, Product Card, Merchant Card, Banner | 无影响 | **保留不动** |
| 来自去重裁决翻转 | Checkbox, Radio, Switch, Search Box, Pagination, Avatar, Status Badge, Transaction Card, Atome-Logo, Bank Logo, Wallet Logo, Country Flag | 命名和变体结构通用，不强绑定 APB | **保留不动**（结构有效） |
| Bottom Navigation, Top App Bar, Tab Bar | DesignOps 独有 | 无影响 | **保留不动** |

**结论**: 现有 34 组件集全部可保留，它们是基于通用 UI 模式创建的，结构和命名不依赖特定设计系统。
Variable Collections 中的颜色值是通用色阶，字体策略已标注为"并存待定"，不需要立即修改。

### 资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 1 | use_figma 检查组件库结构 |
| REST API | 0 | 无新扫描 |

---

## Stage 32: L1 线框图 — 首次自动出图

**日期**: 2026-04-16
**MCP 调用**: 5（1 检查 + 3 创建 + 1 截图）

### 业务场景

**Atome 商户支付结账页（Merchant Checkout）**

用户在线上商城（Lazada Singapore）购物后选择 Atome 分期付款，
跳转到 Atome 支付确认页面。包含以下模块：

1. **Status Bar** — 系统状态栏
2. **Top App Bar** — Checkout 标题 + 返回/关闭
3. **Order Summary** — 商户信息 + 商品列表（AirPods Pro + 硅胶壳）+ 订单合计 S$378
4. **Installment Plan** — 3期/6期/12期选择（6期选中态，绿色高亮）
5. **Payment Method** — DBS PayLah! 已关联 + Change 入口
6. **Agreement** — 协议勾选（已勾选态）
7. **Bottom Bar** — 确认按钮（Confirm Payment · S$63.00）+ 安全提示

### 技术实现

- 标准 iPhone 尺寸（375×812）
- 全 Auto Layout 响应式布局
- 分期选项用选中/未选中双态区分
- 商品列表使用缩略图 + 名称 + 数量 + 价格的标准布局
- 3 次 `use_figma` 调用完成全页创建（分为订单摘要、分期方案、底部操作栏）

### 生成结果

- 文件：Atome AI Test（fileKey: `1nHpzMjQjLzCMO8kMhjL6g`）
- 页面：Screens → Merchant Checkout（nodeId: `45:2`）
- 位置：x=2925, y=0（排列在现有 6 个页面示例右侧）
- 截图验证：结构完整，布局合理

### 意义

这是项目的**第一张完全由 AI 自动生成的 UI 页面**，验证了从"自然语言需求 → Figma 设计稿"的端到端能力。

### 资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 5 | 1 检查 + 3 use_figma 创建 + 1 get_screenshot |
| REST API | 0 | — |

---

## Stage 33: 设计师反馈 — 品牌色错误与 APB 污染根因

**日期**: 2026-04-16
**MCP 调用**: 0（纯分析与文档修正）

### 背景

将 L1 线框图分享给设计团队后，收到以下关键反馈：

| 人员 | 反馈 |
|------|------|
| Fox Hu（UXD lead） | "最基础的都不太对，Atome 品牌色是黄色" |
| Jimmy Xue | "跟 Atome 不一样"，确认 KP 是独立 Figma team |
| Fox Hu | "我怀疑那个 APB 里面 PJP 的设计师有 copy KP 的内容" |

### 根因分析

AI 从 APB 项目中学习到的品牌色 `#00D26A`（绿色）**来自 KP 品牌的设计内容**，
不是 Atome 的真正品牌色。APB 被 Fox Hu 标记为跳过的深层原因正是如此。

- **Atome 真正品牌色**：黄色（DesignOps Mobile 中 `brand/primary` = `#f0ff5f`）
- **APB 中的绿色**：来自 KP 的设计资产复制
- **KP 与 Atome 的关系**：KP 是独立的 Figma team，工作区已隔离

### 影响范围

1. `reports/variables-migration-plan.md` — `color/brand/primary` 原值 `#00D26A` 已标记为错误，修正为 `#f0ff5f`
2. `catalog/tokens/w3c-design-tokens.json` — DesignOps 来源的 `brand/primary: #f0ff5f` 本身是正确的
3. Figma 统一组件库中的 Variables — 如果引用了 APB 的绿色值需要修正
4. L1 线框图 — Merchant Checkout 页面使用灰色占位（L1 不含品牌色），影响有限
5. `interactive/primary` 语义 Token — 原映射到 `{color/brand/green}`，应改为 `{color/brand/primary}`

### 修正操作

- [x] `FACTS.md`、`CORE.md` — 记录 Atome 品牌色为黄色
- [x] `AGENTS.md` — 更新 APB 跳过原因（含 KP 复制内容）
- [x] `docs/figma-core-concepts.md` — APB 跳过原因改为具体描述
- [x] `reports/variables-migration-plan.md` — 标记错误色值，补充正确品牌色

### 教训

1. 从 Figma 项目提取设计 Token 时，必须验证来源项目的"纯度"——是否有跨品牌复制
2. 品牌色等基础视觉要素应优先向设计师确认，而非仅依赖数据提取
3. Fox Hu 标记 APB 为"跳过"的决策有深层原因，表面上看是优先级，本质是数据质量问题

### 资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 0 | 纯文档分析与修正 |
| REST API | 0 | — |

---

## Stage 34: APB 数据全量清除

**日期**: 2026-04-16
**MCP 调用**: 0（纯本地数据操作）

### 背景

设计师反馈后确认：APB 项目不仅品牌色错误，其内容整体来自 KP 品牌的复制，
不能作为任何学习来源。用户明确要求**全部删除，不保留为参考**。

### 操作内容

#### 删除的文件（10+ 个）

| 类别 | 文件 | 大小 |
|------|------|------|
| 源文件清单 | `sources/apb.json` | 8KB |
| 分类索引 | `catalog/classified/by-system/APB.json` | 283KB |
| 扫描报告 | `reports/extractions/scans/apb-scan.json` | 481KB |
| 组件提取 | 5 个文件（FpqdumoL6.., Q8bFuMu.., YNeBaTL.., g9F3TwB.., jqprInB..） | 1,148 组件 |
| 深度提取 | 5 个文件（3FiNujs.., D4UDNtl.., FpqdumoL.., YNeBaTL.., g9F3TwB..） | 样式+组件详情 |
| 截图 | 50+ 个 PNG（6 个目录） | APB 组件截图 |

#### 清洗的数据文件

| 文件 | 操作 |
|------|------|
| `catalog/tokens/w3c-design-tokens.json` | 移除 64 个 APB 来源 Token，剩 96 个 |
| `catalog/tokens/design-tokens.json` | 移除 64 个 APB 来源 Token |
| `catalog/component-descriptions.json` | 248 → 226 个组件集 |
| `catalog/component-co-occurrence.json` | 4348 → 3200 组件 |
| `reports/component-dedup-report.json` | 移除 APB 体系数据和分类分布 |
| `catalog/classified/by-type/*.json` | 9 个文件清理 APB 条目 |
| `catalog/classified-index.json` | 重新构建（体系从 3 个降为 2 个） |

#### 重写的报告

| 文件 | 说明 |
|------|------|
| `reports/component-dedup-report.md` | 移除 16 组 APB vs DesignOps 对比，仅保留 1 组 DesignOps vs Handover |
| `reports/version-selection-plan.md` | 原 17 组裁决已无意义，简化为体系内重复处理 |
| `reports/variables-migration-plan.md` | 移除 APB Token 引用，修正品牌色为 #f0ff5f |
| `reports/full-scan-report.md` | 添加历史警告标注 |

#### 更新的文档

- `AGENTS.md` — APB 数据已删除，品牌色为黄色
- `README.md` — APB 数据已删除
- `docs/figma-core-concepts.md` — APB 跳过原因和数据删除说明
- `~/.shared-memory/figma-asset-library/FACTS.md` — 组件数和体系关系
- `~/.shared-memory/figma-asset-library/CORE.md` — 品牌色已修正

### 清理前后对比

| 指标 | 清理前 | 清理后 |
|------|--------|--------|
| 总组件数 | 4,348 | **3,200** |
| 设计体系 | 3（DesignOps/APB/Handover） | **2**（DesignOps/Handover） |
| 组件集 | 248 | **226** |
| Token 数 | ~163 | **96**（68 色 + 28 字体） |
| 跨体系重复组 | 17 | **1** |
| 品牌色 | #00D26A（绿，错误） | **#f0ff5f（黄，正确）** |

### 教训

1. **数据来源验证最重要**——从 Figma 项目提取前必须确认内容"纯度"
2. **设计师反馈是第一道防线**——基础视觉要素（品牌色）应优先向设计师确认
3. **"参考保留"不够彻底**——被污染的数据不应有任何保留价值，直接删除更安全

### 资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 0 | 纯本地数据操作 |
| REST API | 0 | — |

---

## Stage 35: L1 线框图 v2 — 使用正确品牌色重新设计

**日期**: 2026-04-16
**MCP 调用**: 6（1 whoami + 1 检查 + 1 删除旧版 + 3 创建新版 + 1 截图 + 1 调整布局）

### 背景

设计师反馈后确认 Atome 品牌色为黄色(#f0ff5f)，不是绿色。
旧版 Merchant Checkout（nodeId: 45:2）使用了错误的品牌色，需要全部重做。

### 设计色彩系统（全部来自 DesignOps Token）

| Token | 色值 | 用途 |
|-------|------|------|
| brand/primary | #f0ff5f | 品牌黄：按钮、checkbox、商户 logo 背景 |
| interaction/active | #f6ff7e | 交互活跃态：选中方案说明背景 |
| interaction/pressed | #e3f90a | 按下态 |
| greyscale/dark-1 | #141c30 | 主要文本 |
| greyscale/dark-3 | #3e4459 | 次要文本 |
| greyscale/dark-4 | #878d9c | 辅助文本 |
| greyscale/surface | #f6f6f6 | 页面背景 |
| greyscale/light-1 | #eaeaea | 分割线 |
| others/success | #25bc73 | 成功/利好信息 |
| others/blue | #2247ff | 银行图标 |

### 页面结构

- **Status Bar** — 系统状态栏（9:41）
- **Top App Bar** — Checkout 标题 + 返回/关闭
- **Order Summary** — Lazada Singapore + 2 件商品 + S$378 合计
- **Payment Plan** — 3/6/12 期选择（6 期选中态 = 品牌黄背景+深色描边）
- **Selected Plan Detail** — 首期 S$63 + "0% interest · No hidden fees"（成功绿）
- **Payment Method** — DBS PayLah! 已关联 + Change 入口
- **Agreement** — 品牌黄 checkbox（已勾选态 ✓）
- **Bottom Bar** — 品牌黄确认按钮 + 安全提示

### 技术实现

- iPhone 14 尺寸（390×HUG）
- 全 Auto Layout 响应式布局
- GT Walsheim Pro 字体（DesignOps 主字体）
- 卡片使用圆角 12 + 微阴影
- 3 次 use_figma 调用完成创建 + 1 次布局调整

### 生成结果

- 文件：Atome AI Test（fileKey: 1nHpzMjQjLzCMO8kMhjL6g）
- 页面：Screens → Merchant Checkout（nodeId: 62:2）
- 截图验证：品牌色正确（黄色），布局完整

### 与 v1 对比

| 方面 | v1（错误） | v2（正确） |
|------|----------|----------|
| 品牌色 | #00D26A 绿 | #f0ff5f 黄 |
| 字体 | 未指定 | GT Walsheim Pro |
| 色彩来源 | APB Token（KP 污染） | DesignOps Token |
| 分期选中态 | 绿色高亮 | 品牌黄背景+深色描边 |
| 确认按钮 | 绿色 | 品牌黄 |
| Checkbox | 绿色 | 品牌黄 |
| 设备尺寸 | 375×812 | 390×HUG |

### 资源消耗

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 6 | 1 whoami + 1 检查布局 + 1 删旧 + 2 创建 + 1 截图 |
| REST API | 0 | — |

---

## Stage 36: 设计师反馈优化 — 组件实例导入 + 视觉规范修正

**时间**: 2026-04-15
**触发**: 5 位模拟设计师评审反馈（平均 6.0/10），核心问题："没有使用 DesignOps 组件实例，全部手绘"

### 修复清单

| # | 问题 | 修复方式 | 状态 |
|---|------|----------|------|
| 1 | 未使用 DesignOps 组件实例 | `importComponentByKeyAsync` 导入 Button/Checkbox/Atome-Logo | ✅ |
| 2 | 缺少分期明细展开区域 | 新增 6 期 Instalment Schedule（含序号圆点、日期、金额） | ✅ |
| 3 | lineHeight 140% → 150% | 遍历全部 TEXT 节点统一修正 | ✅ |
| 4 | "Change" 文字应为蓝色 | 改为 others/blue (#2247ff) | ✅ |
| 5 | Atome Logo 使用手绘 | 替换为 `Atome-Logo Compact (Brand)` 组件实例 | ✅ |
| 6 | 卡片圆角 12px → 8px | 遍历全部 FRAME 修正 cornerRadius | ✅ |
| 7 | 卡片阴影 6% → 8% | 修正 DROP_SHADOW opacity | ✅ |
| 8 | 卡片标题 Bold → Medium | Payment Plan/Payment Method 改为 Medium | ✅ |
| 9 | 缺少 Atome 交易编号 | 添加 `Atome Ref: ATM-20260415-0382` | ✅ |
| 10 | 价格未右对齐 | 所有 S$ 文本设 textAlignHorizontal: RIGHT | ✅ |
| 11 | 按钮文字 "Button Name" | 修改为 "Confirm Payment · S$63.00" | ✅ |

### 导入的 DesignOps 组件

| 组件 | 来源 | Component Key | 变体 |
|------|------|---------------|------|
| Button | Design library - web | `59b6375c...` | Type=Big, Class=Primary, Active=Yes |
| Checkbox | Design library - web | `6bd4f728...` | Status=Selected, Active=Yes |
| Atome-Logo Compact | Design library - web | `4a6a8bc3...` | Color=Brand, Plus=No |

### 遇到的问题

1. **`search_design_system` 返回错误的组件 key** — 搜索 "Button" 返回的 `bt_camera` 和 `ic_status` 是相机按钮和状态图标，而非通用 Button。解决方案：从本地 `reports/extractions/components/` 提取数据中精确匹配组件名。
2. **字体加载错误** — Button 组件内部使用 `Plus Jakarta Sans Bold`，首次调用未预加载导致失败。解决方案：补充 `figma.loadFontAsync`。
3. **`Semi Bold` vs `SemiBold`** — `figma.loadFontAsync` 的 style 参数中，Plus Jakarta Sans 使用 `SemiBold`（无空格），与 GT Walsheim Pro 的 `Semi Bold`（有空格）不同。
4. **组件实例内文本节点 ID 变化** — 重新导入组件后，实例内部文本节点的 ID 路径改变（多层嵌套 SLOT）。解决方案：通过遍历实例子树定位正确的 TEXT 节点。

### 优化前后对比

| 维度 | v2 (优化前) | v3 (优化后) |
|------|------------|------------|
| 组件实例数 | 0 | 3 (Button + Checkbox + Logo) |
| lineHeight | 140% | 150% |
| 卡片圆角 | 12px | 8px |
| 按钮来源 | 手绘 Frame + Text | DesignOps `Button` 组件实例 |
| Checkbox 来源 | 手绘圆角矩形 | DesignOps `Checkbox` 组件实例 |
| Logo 来源 | 手绘矩形 + 文字 | DesignOps `Atome-Logo Compact` 实例 |
| 分期明细 | 无 | 6 期完整展开 |
| "Change" 颜色 | 品牌黄 | others/blue (#2247ff) |

### MCP 调用统计

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 10 | 2 search_ds + 6 use_figma + 2 screenshot |
| REST API | 0 | — |

---

## Stage 37: 设计师反馈 — 三层架构认知 + 设计词汇表构建

**时间**: 2026-04-15
**触发**: 设计师 Jimmy Xue 评审 5 位模拟评审员的反馈，指出被忽略的三层架构

### Jimmy Xue 核心观点

> 评审整体合理，但忽略了三层划分：
> 1. **设计系统层（组件/Token）** — AI 建模需要优先对齐
> 2. **UI 视觉细节层** — 因未引用已发布组件，很多细节不准确
> 3. **业务逻辑层** — 超出当前验证范围
>
> 建议：先从第 1 层切入，理顺组件和 Token 使用一致性

### 执行内容

#### 1. DesignOps 全量盘点

| 维度 | 数量 |
|------|------|
| 组件集 | 484 个 |
| 组件变体 | 1,588 个 |
| 颜色 Token | 68 个 |
| 字体 Token | 28 个 |
| 阴影 Token | 3 个 |
| Token 总计 | 99 个 |

来源文件：
- Design library - web: 177 组件集, 508 变体
- Design library - Mobile: 46 组件集, 541 变体
- Merchant Centre Library: 97 组件集, 367 变体
- Icon Library: 169 组件集, 172 变体

#### 2. 组件可导入性验证

批量测试 47 个组件的 `importComponentByKeyAsync` 结果：

| 来源 | 可导入 | 不可导入 | 原因 |
|------|--------|----------|------|
| Design library - web | **全部可导入** | 0 | 已发布团队库 |
| Design library - Mobile | 2 (button, checkbox) | 5 | 大部分未发布 |
| Merchant Centre Library | 2 (button, checkbox) | 1 | 部分未发布 |
| Icon Library | 0 | 1 | 未发布 |

**关键发现**：之前验证时 8 个组件"失败"是因为使用了**截断的 component key**，
用完整 key 后 Web 库组件 **100% 可导入**。

#### 3. 设计词汇表产出

创建 `docs/design-vocabulary.md`，包含：
- Token 体系（颜色/字体/阴影完整映射表）
- 组件清单（按类别分组，含 key、变体、可导入性）
- 业务场景映射（Merchant Checkout 页面 → 具体组件 + Token）
- AI 出图规则（优先级、文本样式、颜色使用、间距规范）

### 遇到的问题

1. **Component key 截断** — REST API 提取的 key 和 `search_design_system` 返回的 key 格式不同（后者是截断版）。解决方案：始终使用本地提取数据中的完整 key。
2. **Design library - Mobile 发布率低** — 46 个组件集中仅 2 个可导入。但 Web 库有完整替代品。

### MCP 调用统计

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 4 | 1 search_ds + 3 use_figma (导入验证) |
| REST API | 0 | — |

---

## Stage 38: L2 组件装配 — 用 DesignOps 组件重建 Merchant Checkout

**时间**: 2026-04-15
**触发**: 设计词汇表构建完成后，按 Jimmy Xue 建议优先对齐第 1 层（组件/Token）

### 核心理念

> v3 = 手绘形状 + 3 个组件实例（Band-Aid 修补）
> L2 = 从框架到细节全部基于 DesignOps 组件实例 + Token（正确的工程化路径）

### 导入的 DesignOps 组件实例

| # | 组件名 | 来源 | 变体 | 用途 |
|---|--------|------|------|------|
| 1 | page-header | Web | Type=with Page Title | 导航栏（含 Status bar + 标题 + 图标） |
| 2 | home Indicator | Web | On Color=No | 底部安全区 |
| 3 | Avatar | Web | Type=Merchant logo | 商户头像 |
| 4 | Radio (Selected) | Web | State=Selected, Active=Yes | 6 期选中态 |
| 5 | Radio (Unselected) | Web | State=Unselected, Active=Yes | 3/12 期未选中 |
| 6 | icon.caret-down | Web | — | 分期明细展开图标 |
| 7 | Bank Logo | Web | Bank=BCA | 支付方式银行图标 |
| 8 | Checkbox (Selected) | Web | Status=Selected | 协议勾选 |
| 9 | Button (Big Primary) | Web | Type=Big, Class=Primary | 确认付款按钮 |
| 10 | icon.lock | Web | — | 安全标识 |
| 11 | Atome-Logo Compact | Web | Color=Brand | 底部品牌标识 |

**总计**: 19 个组件实例（含 page-header 内部嵌套的 icon.arrow-left 等 7 个）

### Token 使用对照

| 属性 | Token | 值 |
|------|-------|-----|
| 卡片背景 | `color/greyscale/white` | #ffffff |
| 页面背景 | `color/greyscale/surface` | #f6f6f6 |
| 主文字 | `color/greyscale/dark-1` | #141c30 |
| 次文字 | `color/greyscale/dark-3` | #3e4459 |
| 辅助文字 | `color/greyscale/dark-4` | #878d9c |
| 链接色 | `color/others/blue` | #2247ff |
| 品牌色 | `color/brand/primary` | #f0ff5f |
| 成功色 | `color/others/success` | #25bc73 |
| 分割线 | `color/greyscale/light-1` | #eaeaea |
| 卡片阴影 | `shadow/shadow-01-8%` | drop-shadow 8% |
| 字体 | GT Walsheim Pro | lineHeight 150% |
| 卡片圆角 | 8px | DesignOps 标准 |

### 版本演进对比

| 维度 | v1 (L1) | v2 (修色) | v3 (修补) | **L2 (重建)** |
|------|---------|-----------|-----------|-------------|
| 品牌色 | ❌ 绿色 | ✅ 黄色 | ✅ 黄色 | ✅ 黄色 |
| 组件实例 | 0 | 0 | 3 | **19** |
| Token 对齐 | ❌ | 部分 | 部分 | **全部** |
| 导航栏 | 手绘 | 手绘 | 手绘 | **page-header 组件** |
| 确认按钮 | 手绘 | 手绘 | Button 组件 | **Button 组件** |
| 勾选框 | 手绘 | 手绘 | Checkbox 组件 | **Checkbox 组件** |
| 分期选择 | 手绘方块 | 手绘方块 | 手绘方块 | **Radio 组件** |
| 分期明细 | ❌ | ❌ | ✅ 手绘 | ✅ Token |
| 合规信息 | ❌ | ❌ | ✅ 部分 | ✅ icon.lock |

### 遇到的问题

1. **Figma effects API 格式变更** — `DROP_SHADOW` 需要 `blendMode: 'NORMAL'` 字段，否则报 validation error。
2. **page-header Default 变体无标题** — `Type=Default` 只有返回箭头，需改用 `Type=with Page Title`。
3. **page-header 自带 Status bar** — 导致双重 Status bar，需删除手动添加的那个。

### MCP 调用统计

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 9 | 7 use_figma + 2 screenshot |
| REST API | 0 | — |

---

## Stage 39: 新文件 AI Generated Screens 落地 — Cover + L2 Merchant Checkout 迁移

**时间**: 2026-04-20
**触发**: 闭环 Jimmy Xue 三层架构反馈 — 把 L2 从旧测试文件迁到正式 AI 出图文件，建立分页结构

### 背景与障碍

旧 fileKey `4vMTl37Ea35TYLpM6gtzoG`（CORE.md 4-15 记录的 AI Generated Screens）首次写入时
即报 **Starter plan limit reached**，证明该文件实际落在个人 Starter 团队，并非组织 Atome UED。
直接作废该 fileKey，按用户决策在组织空间重建。

### 关键操作

| # | 操作 | 结果 |
|---|------|------|
| 1 | `create_new_file` 用组织 key 重建 | 新 fileKey: `tZfhizmsTeqIrP6Qnq0V86`（默认落 Drafts，需手动移到 Atome AI Test） |
| 2 | 重命名首页 + 新建 3 页 | Cover / Checkout Flow / Components Test / Archive 全部就位 |
| 3 | Cover 页生成项目封面卡片 | 含三层架构进度状态（IN PROGRESS / NEXT / OUT OF SCOPE） |
| 4 | L2 Merchant Checkout 重建 | 11 个 DesignOps 组件实例 + 全 Token 对齐 |

### 三层架构状态卡片（Cover 页）

| 层 | 名称 | 状态 |
|---|------|------|
| 1 | 设计系统层（组件 / Token） | **IN PROGRESS**（L2 已落地） |
| 2 | UI 视觉细节层 | **NEXT**（与线上页面像素级对齐） |
| 3 | 业务逻辑 + 交互设计 | **OUT OF SCOPE**（Jimmy 标注超出验证范围） |

### L2 重建组件清单（与 Stage 38 一致 + 完整 component key）

| # | 组件 | 完整 Component Key |
|---|------|--------------------|
| 1 | page-header (with Page Title, On Color=No) | `fa0542dab067b13b46869fd98daafee3d0583e48` |
| 2 | home Indicator (On Color=No) | `59ea6015ee3db5633c4739d786314a318dad6d35` |
| 3 | Avatar (Merchant logo) | `24fbe8ccdb00cfd2d2193d649ff7d1a1e2de0f8d` |
| 4 | Radio (State=Selected, Active=Yes) | `670edc08c72489afebd160d527a8f82bc51011eb` |
| 5 | Radio (State=Unselected, Active=Yes) | `58382cc9857d89a1547d6913be0b5278e800d809` |
| 6 | icon.caret-down | `3b43bd215dbc0464b755ccf5dd832a40c7c220cb` |
| 7 | Bank Logo (Bank=BCA) | `4cea9627c25de4ce324004c3df70f62dc89770b9` |
| 8 | Checkbox (Selected, Active=Yes) | `6bd4f728580115413cb41e33df1fdfaa98714ce8` |
| 9 | Button (Big Primary, Active=Yes) | `59b6375c270cc9c3d9cf5d3520f861582c7386b5` |
| 10 | icon.lock | `7279c238f9904939a29f17737fbbb8b6e64238d9` |
| 11 | Atome-Logo Compact (Brand) | `4a6a8bc3d867de1ae697974584e2aac8af0b5d5f` |

### 遇到的问题

1. **旧 AI Generated Screens fileKey 走 Starter 额度** — 4-15 创建时未验证文件归属团队。教训：每次 `create_new_file` 后必须立即在 CORE.md 记录所属团队（不仅是 fileKey）。
2. **`appendChild()` 返回 null** — Plugin API 的 appendChild 不返回被 append 的节点，链式调用 `parent.appendChild(child).foo = bar` 会触发 `cannot set property of null`。改用 `parent.appendChild(child); child.foo = bar;` 模式。
3. **page frame fixed 高度 844 截断内容** — 移动设计稿应该 `primaryAxisSizingMode = 'AUTO'` 让 frame HUG 内容（最终 1107px 高）。
4. **状态 chip 默认渲染为大圆球** — auto-layout frame 内 chip 必须显式 `layoutSizingHorizontal/Vertical = 'HUG'`，否则被父级拉伸。

### 文件结构对照

| 项目 | 旧 fileKey（已作废） | 新 fileKey（生效） |
|------|---------------------|--------------------|
| AI Generated Screens | `4vMTl37Ea35TYLpM6gtzoG` | `tZfhizmsTeqIrP6Qnq0V86` |
| 团队归属 | 个人 Starter | 组织 Atome UED（待用户从 Drafts 移到 Atome AI Test 项目） |
| MCP 额度 | 6/月 | 200/天 |

### 待用户操作

1. 在 Figma 桌面端把新文件 `AI Generated Screens` 从 Drafts 拖到 `Atome AI Test` 项目下
2. 确认旧 fileKey `4vMTl37Ea35TYLpM6gtzoG` 是否需要保留（建议归档或删除）
3. 把 L2 截图发给 Jimmy Xue 闭环确认"组件/Token 一致性"

### MCP 调用统计

| 类型 | 次数 | 说明 |
|------|------|------|
| MCP 计费 | 8 | 1 create_new_file + 5 use_figma + 2 screenshot |
| REST API | 0 | — |

### 下一阶段（第 2 层启动条件）

待 Jimmy 确认 L2 第 1 层达标后启动：
- 与线上 Lazada/Shopee/TikTok Shop checkout 页面像素级对齐
- 间距 / 微交互态 / 多语言适配
- 异常态（Network error / 分期不可用 / 协议未勾选）

## Stage 40: 设计词汇表大补 — 双层架构（自动数据 + 人工语义）

**时间**：2026-04-20
**触发**：Jimmy Xue 三层架构反馈第 1 层（组件/Token 一致性）需要可检索的词汇表；旧版仅 ~40% 完整、key 全部截断。

### 目标

把旧 `docs/design-vocabulary.md` 单文件升级为**双层架构**：
- **数据层（机器维护）**：`catalog/vocabulary-data.json` + 脚本生成的 by-type / by-module / icons markdown
- **语义层（人工协作）**：总入口 + 4 个 Token 子文件 + 10 个业务场景模板

### 关键设计

| 决策 | 取舍 |
|------|------|
| 范围 | 仅 DesignOps 1,588 组件（不含 Handover 业务页） |
| 业务场景 | 按 catalog 现有 10 个 module 一一对应 |
| 文件大小 | 全部 ≤ 200 行（满足用户规则） |
| 完整 key | 通过自动化生成保证不再截断 |
| markdown 紧凑度 | 每组件集 1 行 + 首个变体 key；完整变体 keys 放 JSON |

### 产出

| 类别 | 数量 | 说明 |
|------|------|------|
| 总入口 | 1 | `docs/design-vocabulary.md` |
| Token 子文件 | 4 | colors / typography / shadows / conventions |
| by-type 索引 + 详情 | 26 | 22 类型 × 1 详情页 + 4 拆分子页 |
| by-module 索引 + 详情 | 15 | 10 模块 × 1 详情页 + 5 拆分子页 |
| icons 索引 + 字母分组 | 17 | 1 README + 16 by-letter |
| 业务场景 | 11 | 1 完整 (Merchant Checkout) + 9 骨架 + 1 README |
| 完整数据 JSON | 1 | `catalog/vocabulary-data.json` (488 KB) |
| 自动化脚本 | 3 | `scripts/build-vocabulary.js` + `scripts/vocab/{load-data,render-md}.js` |
| 旧版备份 | 1 | `docs/design-vocabulary.legacy.md` |

合计 **73 个 markdown** + 1 JSON + 3 脚本，全部 ≤ 200 行。

### 关键 Component Key 校准（实测从 vocabulary-data.json 提取）

| 组件 | 真实 Key |
|------|---------|
| Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| home Indicator | `59ea6015ee3db5633c4739d786314a318dad6d35` |
| Avatar | `1da2e978cc392829adfe16315fdffa110a0347ad` |
| Bank Logo | `4cea9627c25de4ce324004c3df70f62dc89770b9` |
| Wallet Logo | `2480a879fdb30a665c27a18c52b6c3f3c94dc5ba` |
| Atome-Logo Compact | `0d6971c0412f9fbbaf82c4a9bac5c5ba6d05ce94` |
| Checkbox / Radio | `526c219c...` / `51952c25...` |
| Input Phone Number / OTP / Amount | `679244e3...` / `792a7297...` / `615e8217...` |

### 遇到的问题

1. **markdown 控制 200 行难度大** — 数据本身 1,588 组件，需要"分级 + 紧凑表格"两层策略；最终方案：markdown 给每个组件集 1 行（首个 key），完整变体放 JSON。
2. **图标 415 个变体大量重名** — 改为按 (file, name) 聚合后只剩 96 个唯一图标，markdown 大幅缩短。
3. **超长文件 by-module/general.md (3694 行)** — 增加按 file 自动二次拆分逻辑，统一控制 < 180 行。
4. **场景文档 key 不能靠猜** — 全部通过 `jq` 从 `catalog/vocabulary-data.json` 实测提取。

### 下一阶段

- [ ] Jimmy 审阅词汇表，反馈结构是否够用、scenarios 是否需要补
- [ ] 9 个骨架 scenarios 由设计师补全 TODO 段
- [ ] 词汇表纳入 AI 出图工作流（每次出图前 must read）
- [ ] L2 实装新场景时，按词汇表模板装配并把状态升为 ✅
