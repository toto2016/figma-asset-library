# UI/UX 专业角色可行性评审报告

**项目**: Atome UED Figma 全量素材库
**评审日期**: 2026-04-15
**数据基础**: 13 个项目 / 558 个文件 / P0 项目 47 文件已全量扫描

---

## 数据摘要（评审依据）

| 维度 | 数值 |
|------|------|
| Figma 项目总数 | 13 |
| 文件总数 | 558 |
| P0 项目文件数 | 47（DesignOps 16 + Flow Library 31） |
| 已发布组件 | 1,164（集中在 4 个文件） |
| 已发布样式 | 68（23 色彩 + 15 文字 + 1 效果 + 29 Merchant） |
| 核心设计库 | Design library - Mobile（541 组件 / 39 样式） |
| 辅助库 | Merchant Centre Library（367 组件 / 29 样式） |
| 图标库 | open-peeps（172）+ Gesture Icons（65） |
| 品牌字体 | GT Walsheim Pro（非 Inter） |
| Button 组件 | 4 类型 × 3-4 状态 = 13 变体 |
| 单组件集完整 JSON | ~3,085 行 |

### 核心设计库结构（Design library - Mobile）

```
components/        ← 主组件页
  buttons/         ← button(13变体), bgd
  icons/           ← 图标集
  icon assets/     ← 图标资源
  others/          ← 其他组件
  popup/           ← 弹窗组件
  Tab view/        ← 标签视图
  controls/        ← 控件（分类器等）
  charts/          ← 图表
  ...

Patterns/          ← 设计模式
assets/            ← 资源
WIP components/    ← 进行中
tag/               ← 标签Œ
```

---

## 角色 1：UI 组件设计师

**身份**: 日常使用 Figma 组件库搭建界面的一线设计师
**核心关注**: 组件好不好找、属性全不全、能不能即拿即用

### 评估

**可行性: 6/10**

**肯定的部分：**

- 终于能看清全局了。之前 558 个文件散在 13 个项目里，我根本不知道哪些组件
  已经有了、在哪里。现在扫描出来 1,164 个已发布组件，终于有了全景图。
- button 组件的数据提取很完整：4 种类型（basic/secondary/outlined/text）、
  每种 3-4 个状态、padding/cornerRadius/颜色值全有。
  理论上用这些数据可以完整重建组件。

**担忧的部分：**

- 这个项目最终输出的是什么？如果只是一个 JSON 索引文件，对我日常工作
  没有帮助。我需要的是**在 Figma 里能直接拖拽使用的组件**。
- 完整属性提取 541 个组件要产生 ~160 万行 JSON，这些数据谁来消费？
  我不会去读 JSON。
- 当前 Design library - Mobile 已经是可用的组件库了，我已经在用。
  这个项目是要建一个**新的统一库**还是**整理现有库**？区别很大。
- GT Walsheim Pro 是品牌字体，字体许可证和可用性需要确认。

**建议：**

1. 先明确最终交付物——是新 Figma 文件里的组件库，还是本地索引？
2. 如果是新组件库，优先迁移 Design library - Mobile 的 541 个组件
3. 组件命名需要规范化（现在有 `Property 1=basic` 这种自动命名，不友好）

---

## 角色 2：UX 设计主管 / Design Lead

**身份**: 管理 Atome UED 团队，负责设计一致性和团队效率
**核心关注**: ROI、团队采纳率、设计规范统一

### 评估

**可行性: 7/10**

**看好的部分：**

- 数据揭示了一个重要事实：**设计资产高度集中**。1,164 个组件里，
  541 个在 Design library - Mobile，367 个在 Merchant Centre Library。
  两个文件占 78%。这意味着治理成本比想象的低。
- Flow Library 的 31 个文件几乎没有可复用组件（只有 19 个），
  说明它们是**消费者**不是**生产者**——它们引用主库的组件来搭流程图。
  这验证了我们的组件库策略是对的。
- 自动化扫描的速度令人印象深刻：47 个文件全量扫描在几分钟内完成。
  如果手动梳理，至少需要一个设计师一周的时间。

**担忧的部分：**

- 项目当前产出的是**元数据索引**，不是**设计规范文档**。
  团队需要的是"什么场景用什么组件"的使用指南，不只是"有哪些组件"的清单。
- 558 个文件中可能有大量过时/废弃的设计。看到 Flow Library 里有
  2021 年的文件（"PH User Journey" 上次修改 2021-08-25），
  需要机制标记活跃 vs 归档。
- Merchant Centre Library 有 367 个组件但在 DesignOps 项目下，
  与 Design library - Mobile 有什么关系？是否有重复组件？
  组件间的依赖关系（如 button 被哪些 pattern 引用）无法从当前数据看出。

**建议：**

1. 增加"最后修改时间"维度，自动标记 >1 年未更新的文件为"可能废弃"
2. 做组件去重分析——Merchant Library 的 367 个组件和 Mobile Library 的
   541 个组件有多少重叠？
3. 输出给团队的不应该是 JSON，而是一个可视化的组件目录页面
   （可以用 Figma 本身做，也可以是一个网页）

---

## 角色 3：设计系统架构师 / Design System Lead

**身份**: 负责设计系统的架构、Token 体系、组件规范
**核心关注**: Token 完整性、组件原子化程度、跨平台一致性

### 评估

**可行性: 8/10**

**很有价值的发现：**

- REST API 完整属性提取是**设计系统审计**的利器。从 button 的样本数据看，
  我能获取到：
  - 精确的颜色值（如 `#CFD2E3` 的 disable 边框色）
  - 精确的间距值（padding 10/10/6/6）
  - 精确的圆角值（6px）
  - 精确的字体规格（GT Walsheim Pro Bold 15px / lineHeight 17.17px）
- 这些数据可以直接生成 Design Token JSON：

```json
{
  "button.outlined.borderRadius": "6px",
  "button.outlined.padding": "6px 10px",
  "button.outlined.borderColor.disabled": "#CFD2E3",
  "button.outlined.textColor.disabled": "#B7BACB",
  "button.basic.height": "48px",
  "font.family.brand": "GT Walsheim Pro",
  "font.weight.button": 700
}
```

- 当前 Design library - Mobile 有 39 个已发布样式（23 色彩 + 15 文字 + 1 效果），
  这是一个**初具雏形但不完整**的 Token 体系。
  23 个颜色样式对一个支持 10 个国家的产品来说偏少。

**架构层面的问题：**

- **Variable 体系缺失**。扫描脚本在测试文件上能创建 Variable，
  但 Design library - Mobile 的 Variable 情况未知
  （REST API 的 `GET /variables/local` 端点可以补充这个数据）。
- **组件属性命名不规范**。看到 `Property 1=basic, Property 2=normal`
  这种自动生成的属性名，说明组件创建时没有规范命名。
  规范应该是 `Type=basic, State=normal`。
- **没有 Mode（模式）支持的证据**。一个成熟的设计系统应该有
  Light/Dark 模式、多密度（compact/default）支持。
  从 39 个样式来看，目前只有单模式。
- **平台覆盖不全**。只有 "Mobile" 库和 "Merchant Centre" 库。
  缺少 Web 通用组件库。

**建议：**

1. **立即做**：用 REST API 提取 Design library - Mobile 的完整 Variable 数据，
   评估现有 Token 体系的成熟度
2. **短期**：基于完整属性数据，生成 Design Token JSON（可以用 Style Dictionary 格式）
3. **中期**：重构组件属性命名（`Property 1` → `Type`、`Property 2` → `State`）
4. **长期**：建立 Variable Collection，支持 Light/Dark 模式和多品牌

---

## 角色 4：DesignOps 工程师 / 设计运营

**身份**: 负责设计工具链、效率提升、流程自动化
**核心关注**: 自动化程度、可维护性、工具链集成

### 评估

**可行性: 9/10**

**这个项目的技术栈设计得很好：**

- **REST API 是正确选择**。MCP 的 `use_figma` 在 View 权限下无法运行，
  但 REST API 没有这个限制。而且 REST API 没有每日调用次数上限
  （只有速率限制），可以全量提取。
- **增量更新可行**。每个文件有 `version` 字段和 `lastModified` 时间戳，
  可以只重新扫描有变化的文件。比如 Design library - Mobile 的
  version 是 `2342618242577714693`，下次扫描只要 version 没变就跳过。
- **脚本复用性强**。`scan-rest-api.sh` 已经验证了 47/47 文件 100% 成功率，
  直接可以扫描剩余 511 个文件。
- **PAT Token 有效期 90 天**（到 2026-07-14），足够完成全量提取。

**运营层面的建议：**

- **监控仪表盘**。当前的 `extraction-log.json` 是手动更新的，
  应该在扫描脚本中自动更新。
- **定期巡检**。每周自动运行一次轻量扫描，对比 version 变化，
  检测新增/删除/修改的组件。可以用 cron 或 GitHub Actions。
- **数据管道**。当前是"扫描 → JSON 文件"，
  后续应该考虑入库（SQLite 就够），支持查询和统计。
- **截图资产管理**。如果要用 `get_screenshot` 批量截图，
  需要 MCP 调用（每截一张消耗 1 次额度），
  541 个组件至少需要 541 次调用 = 约 3 天。应该优先只截核心组件。

**风险点：**

- PAT Token 90 天后过期，需要轮换机制
- Figma REST API 的速率限制没有明确文档（经验值约 30 req/min），
  批量扫描需要控制节奏
- 如果 DesignOps 团队更新了组件库但没有通知，索引会过时

---

## 角色 5：交互设计师 / UX Designer

**身份**: 负责产品交互流程、用户体验设计
**核心关注**: 流程模板复用、交互规范一致性

### 评估

**可行性: 5/10**

**对我有用的部分有限：**

- Flow Library 的 31 个文件是我最关心的——它们包含各国的用户流程图。
  但扫描结果显示只有 1 个文件有组件（"Happy flow | All countries (updated)"
  有 19 个组件），其余 30 个文件是纯流程图，没有可复用的组件。
- 这说明流程图主要是**视觉参考**，不是结构化数据。
  JSON 属性提取对流程图帮助不大——流程图的价值在于"看"，不在于节点属性。

**我真正需要的是：**

- "Atome APP Happy Flow" 有 **48 个页面**，是最大的流程文件。
  但 JSON 只告诉我有哪些页面，不告诉我页面之间的连接关系（用户流转路径）。
- 各国流程之间的差异对比（如 ID vs PH 的 KYC 流程有什么不同），
  但当前数据只有文件级别的信息，没有页面级别的内容对比。
- 一个能搜索的流程库："我想找 onboarding 的流程"
  → 应该返回所有国家的 onboarding 流程截图和链接。

**建议：**

1. Flow Library 的价值不在组件提取，而在**截图 + 结构化标签**
2. 用 `get_screenshot` 截取每个流程的关键页面，加上国家/模块/平台标签
3. 建立一个"流程导航器"——输入功能名→ 返回所有相关流程的截图和 Figma 链接

---

## 角色 6：设计质量负责人 / Design QA

**身份**: 负责设计走查、视觉一致性、规范落地检查
**核心关注**: 组件使用合规性、设计偏差检测

### 评估

**可行性: 8/10**

**这个项目对 Design QA 有巨大潜力：**

- **一致性审计自动化**。有了完整的 Token 数据，可以自动检测：
  - 哪些页面用了非标准颜色（不在 23 个已发布色彩样式中）
  - 哪些文字用了非标准字号（不在 15 个文字样式中）
  - 哪些按钮的 padding 与标准组件不一致
- **组件使用统计**。REST API 的 `depth=999` 提取可以检测
  每个设计稿中使用了哪些组件实例、哪些是 detached 的
  （detach 后会失去与主库的同步，是设计偏差的主要来源）。
- **跨国一致性**。Flow Library 有 ID/PH/TH/MY/SG/HK/JP/TW 各国流程，
  可以自动对比同一模块在不同国家的视觉差异。

**落地路径：**

1. 第一步：完整提取 Design library - Mobile 的所有 Token 值（颜色、字号、间距）
2. 第二步：随机抽样 5-10 个设计稿（从 APS/Online Integration 项目），
   对比实际使用值 vs Token 标准值
3. 第三步：输出"设计偏差报告"——哪些文件、哪些节点偏离了设计规范

---

## 综合评审结论

### 评分汇总

| 角色 | 评分 | 核心诉求 |
|------|------|---------|
| UI 组件设计师 | 6/10 | 需要可拖拽使用的组件，不是 JSON |
| UX 设计主管 | 7/10 | 需要使用指南 + 可视化目录 + 去重 |
| 设计系统架构师 | 8/10 | Token 审计利器，可生成 Design Token |
| DesignOps 工程师 | 9/10 | 技术栈合理，自动化程度高 |
| 交互设计师 | 5/10 | 流程图需要截图，不是 JSON 属性 |
| Design QA | 8/10 | 一致性审计自动化潜力巨大 |

**加权平均: 7.2 / 10**

### 共识

1. **项目技术可行性高**——REST API 扫描已验证 100% 成功率
2. **核心价值在 4 个高价值文件**——集中精力在这 4 个库文件上
3. **最终交付物不能是 JSON**——需要转化为设计师可消费的形式

### 分歧

| 议题 | 主张方 | 反对方 |
|------|--------|--------|
| 要不要全量提取 558 文件 | DesignOps、Design QA | 交互设计师（Flow Library 不需要） |
| 完整属性提取 vs catalog 级别 | 设计系统架构师 | UI 设计师（看不懂 JSON） |
| 建新统一组件库 vs 整理现有库 | 设计主管 | UI 设计师（别打断现有工作流） |

### 建议的项目调整

1. **拆分两个产出线**：
   - **线 A（数据索引）**：当前路径继续，服务于 DesignOps 和 Design QA
   - **线 B（可视化目录）**：基于索引数据，生成设计师友好的目录页面
2. **重新定义 Wave 优先级**：
   - 不再按项目分 Wave，改为按价值分：
   - **Wave A**：4 个高价值库文件完整提取（1,164 组件）
   - **Wave B**：截图资产（核心组件截图）
   - **Wave C**：剩余文件的 catalog 级别扫描
3. **增加 Token 提取**：
   - 补充 Variable/Token 数据的完整提取
   - 输出 Style Dictionary 格式的 Design Token
