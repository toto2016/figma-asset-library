---
name: atome-design-assets
version: 3.0
description: >
  Atome UED 设计资产库：查 Token / 查组件 / 查场景，并按 Atome 规范生成 UI 设计稿或代码。
  4 条出图路径：Figma MCP / Cursor Canvas / HTML→PNG（Lark·微信 bot）/ 前端代码。
  3,200 组件、99 Token、10 业务场景、57 份词汇表。
target_systems: []
side_effects: read-only
triggers:
  - atome design
  - atome 设计
  - atome token
  - atome 组件
  - 设计资产
  - design asset
  - design token
  - 设计词汇
  - atome 出图
  - figma 出图
  - atome ui
  - atome 页面
  - atome 场景
  - atome canvas
  - atome 预览
  - canvas 出图
exclusive_triggers:
  - atome design
  - atome 设计资产
conflicts_with: []
trigger_disambiguation:
  - 若上下文是 InvestScope → 不触发，走 InvestScope 的 DESIGN.md
  - 若说"Figma 出图"但未指定品牌 → 先问"Atome 还是其他项目"
guardrail:
  pre_action_checkpoint: none
  content_validator:
  audit: none
priority: P2
owners: [toto]
last_reviewed: 2026-04-23
---

## Purpose

按照 Atome 设计系统规范，查询 Token / 组件 / 场景映射，并能直接生成符合品牌规范的 UI 输出（Figma 设计稿或前端代码）。

## When to use

- 需要按 Atome 品牌规范设计一个页面或模块
- 需要查 Atome 的颜色、字体、阴影等 Design Token
- 需要查组件清单或组件的 40 位 Component Key
- AI 在 Figma 中为 Atome 出图
- 零 MCP 调用，在 Cursor Canvas 中实时预览 Atome 页面设计
- 需要生成符合 Atome 规范的前端代码片段

## When NOT to use

- InvestScope 项目 → 用 InvestScope 的 `DESIGN.md` + `design-system/`
- 非 Atome 品牌
- 仅做 Figma API 操作（不涉及 Atome 规范）→ 直接用 Figma MCP

---

## AI 渲染铁律（每次出图前必读）

### 组件选择优先级

1. **优先**：DesignOps 已发布组件（通过 `figma.importComponentByKeyAsync('<40位key>')` 导入）
2. **次选**：同类组件优先 Web 库（Mobile 库有 5 个未发布）
3. **兜底**：用 Token 手建 Frame，**禁止硬编码颜色/字号/圆角**

### 颜色速查

| 场景 | Token | 值 |
|------|-------|-----|
| 品牌主色 | `color/brand/primary` | `#f0ff5f` |
| 主文字 | `color/greyscale/dark-1` | `#141c30` |
| 辅助文字 | `color/greyscale/dark-3` | `#6a7383` |
| 可点击文字 | `color/others/blue` | `#2247ff` |
| 页面背景 | `color/greyscale/surface` | `#f6f6f6` |
| 卡片背景 | `color/greyscale/white` | `#ffffff` |
| 成功 | `color/others/green` | `#1bb96b` |
| 错误 | `color/others/red` | `#ff3b3b` |
| 警告 | `color/others/yellow` | `#ffcc00` |
| 分割线 | `color/greyscale/light-3` | `#eaeaea` |

完整 68 色：`docs/vocabulary/tokens/colors.md`

### 文本样式速查

| 场景 | Token | 字号 | 字重 |
|------|-------|------|------|
| 页面标题 | `typography/title/title-3` | 16pt | Bold |
| 卡片标题 | `typography/title/title-3` | 16pt | Medium |
| 正文 | `typography/body/body-2` | 15pt | Regular |
| 辅助文字 | `typography/caption/caption-1` | 13pt | Regular |
| 按钮文字 | `typography/button/button-1` | 16pt | Medium |
| 金额大数 | `typography/title/title-1` | 22pt | Bold |

字体：GT Walsheim Pro（Figma 中需 `loadFontAsync`）
完整 28 个 Token：`docs/vocabulary/tokens/typography.md`

### 间距与圆角

| 场景 | 值 |
|------|-----|
| 页面水平 padding | 20px |
| 卡片内 padding | 16px |
| 卡片间距 | 12px |
| 元素行间距 | 8px |
| 卡片圆角 | 8px |

### 禁忌

- ❌ 硬编码 hex 色值（必须查 Token）
- ❌ 硬编码字号（必须用 typography Token）
- ❌ 自定义阴影参数（必须用 shadow Token）
- ❌ 不加载字体直接写文字（GT Walsheim Pro 需先 loadFontAsync）
- ❌ Fixed 高度做内容页（必须 `primaryAxisSizingMode='AUTO'`）
- ❌ 品牌色用绿色（品牌色是黄色 `#f0ff5f`）

---

## Workflow：生成指定场景的设计

### Step 0：确认当前环境

**环境检测（按优先级）：**
1. `playwright` 可用 + 非 Cursor 环境 → **HTML→PNG 路径**（本 skill 的默认推荐）
2. `canvases/` 目录存在 + 在 Cursor IDE 中 → **Canvas 路径**
3. 无 playwright + 非 Cursor → **代码输出路径**

**检测命令：**
```bash
python3 -c "from playwright.sync_api import sync_playwright; print('ok')" 2>/dev/null
ls ~/Library/Application\ Support/Code/Cursor/ 2>/dev/null && echo "cursor"
```

**Playwright 可用时 → 自动使用 HTML→PNG：**
```bash
# 1. 生成 HTML 文件（/tmp/atome-<场景>.html）
# 2. 截图
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 375, 'height': 900})
    page.goto('file:///tmp/atome-<场景>.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='/tmp/atome-<场景>.png', full_page=False)
    browser.close()
"
# 3. 返回 PNG 图片
```

### Step 1：确定场景

从 10 个已定义场景中选择，或描述自定义场景：

| # | 场景 | 状态 | 文档路径 |
|---|------|------|---------|
| 01 | Merchant Checkout | ✅ 完整 | `docs/vocabulary/scenarios/01-merchant-checkout.md` |
| 02 | KYC Flow | 骨架 | `docs/vocabulary/scenarios/02-kyc-flow.md` |
| 03 | Voucher Claim | 骨架 | `docs/vocabulary/scenarios/03-voucher.md` |
| 04 | Onboarding | 骨架 | `docs/vocabulary/scenarios/04-onboarding.md` |
| 05 | Payment Method | 骨架 | `docs/vocabulary/scenarios/05-payment-method.md` |
| 06 | Profile | 骨架 | `docs/vocabulary/scenarios/06-profile.md` |
| 07 | Notification | 骨架 | `docs/vocabulary/scenarios/07-notification.md` |
| 08 | Home Dashboard | 骨架 | `docs/vocabulary/scenarios/08-home.md` |
| 09 | Loan Apply | 骨架 | `docs/vocabulary/scenarios/09-loan.md` |
| 10 | Login & Signup | 骨架 | `docs/vocabulary/scenarios/10-login.md` |

### Step 2：读取场景模板

```
读 docs/vocabulary/scenarios/<场景编号>.md
从中获取：
  - 页面结构（ASCII 布局图）
  - 组件 → Component Key 映射表
  - Token → 使用位置映射表
  - 间距规格
```

### Step 3：补充组件数据

如果场景模板中缺少某个组件的 Key：

```
1. 按 UI 类型查 → docs/vocabulary/by-type/<type>.md
   例：需要 Button → docs/vocabulary/by-type/button.md
2. 按业务模块查 → docs/vocabulary/by-module/<module>.md
   例：支付相关 → docs/vocabulary/by-module/payment.md
3. 全量搜索 → catalog/assets.json（3,200 条，含 componentKey 字段）
4. 图标查找 → docs/vocabulary/icons/by-letter/<首字母>.md
```

### Step 4：选择出图路径

根据运行环境自动选择：

| 环境 | 路径 | MCP 调用 | 输出格式 |
|------|------|---------|---------|
| Cursor IDE + Figma MCP | **4A: Figma 设计稿** | 是 | Figma 文件 |
| Cursor IDE（无 MCP） | **4B: Canvas 预览** | 零 | IDE 内实时渲染 |
| Lark / 微信 / CLI bot | **4C: HTML → PNG** | 零 | PNG 图片 |
| 任意环境 | **4D: 代码输出** | 零 | React/HTML 代码 |

**环境检测规则：**
- 有 `canvases/` 目录 → Cursor IDE → 用 4B
- 无 `canvases/` 但能执行 shell → bot 环境 → 用 4C
- 仅输出文本 → 用 4D

### Step 4A：Figma 设计稿（Cursor + 官方 Figma MCP）

**⚠️ MCP 调用铁律 — 必须遵守：**
- **禁止**调用 `search_design_system` → 组件 Key 从本地 `catalog/assets.json` 查
- **禁止**调用 `get_variable_defs` → Token 从本地 `catalog/tokens/design-tokens.json` 读
- **禁止**逐组件多次调用 `use_figma` → 合并为**一次调用**
- **目标**：整个页面 = **1 次 `use_figma`**

**批量脚本模板（单次调用构建完整页面）：**
```javascript
// Step 1: 加载字体
await figma.loadFontAsync({ family: "GT Walsheim Pro", style: "Regular" });
await figma.loadFontAsync({ family: "GT Walsheim Pro", style: "Bold" });

// Step 2: 创建页面 Frame
const frame = figma.createFrame();
frame.name = "<场景名> · Light";
frame.resize(375, 812);
frame.layoutMode = "VERTICAL";
frame.primaryAxisSizingMode = "AUTO";
frame.paddingLeft = frame.paddingRight = 20;
frame.itemSpacing = 12;
frame.fills = [{ type: "SOLID", color: { r: 0.965, g: 0.965, b: 0.965 } }];

// Step 3: 并行导入所有组件（Key 来自本地 catalog/assets.json）
const [comp1, comp2, comp3] = await Promise.all([
  figma.importComponentByKeyAsync('<40位key-1>'),
  figma.importComponentByKeyAsync('<40位key-2>'),
  figma.importComponentByKeyAsync('<40位key-3>'),
]);

// Step 4: 创建实例并挂载
[comp1, comp2, comp3].forEach(c => frame.appendChild(c.createInstance()));

// Step 5: 定位到画布
figma.currentPage.appendChild(frame);
figma.viewport.scrollAndZoomIntoView([frame]);
```

**⚠️ 限制**：DesignOps 中带 SLOT 的组件（如主按钮），API 下难改文案，出图后需设计师在 Figma 中手调。

### Step 4B：Canvas 预览（仅 Cursor IDE）

```
生成 .canvas.tsx 文件，在 IDE 内实时渲染 Atome 页面预览：

1. 从 catalog/tokens/design-tokens.json 提取 Token 值
2. 将 Token 定义为命名常量（禁止匿名 hex）
3. 用手机框架（375×812）包裹页面内容
4. 用 inline style + Token 常量渲染所有视觉属性
5. 右侧附 Token 映射参考面板
6. 文件路径：<workspace>/canvases/atome-<场景名>.canvas.tsx

⚠️ 仅限 Cursor IDE。Lark / 微信 bot 无 Canvas 运行时，请用 4C。
```

### Step 4C：HTML → PNG 截图（Lark / 微信 / CLI bot 推荐）

```
适用于所有 bot 环境（OpenClaw Lark bot、WorkBuddy 微信 bot 等）：

1. 从 catalog/tokens/design-tokens.json 提取 Token 值
2. 生成自包含 HTML 文件（内联 CSS + Atome Token）：
   - 手机视口：375×812，白色背景
   - 所有颜色、字体、间距引用 Token 常量
   - 保存到 /tmp/atome-<场景名>.html
3. 用 headless 浏览器截图为 PNG：
   npx playwright screenshot --viewport-size=375,812 \
     /tmp/atome-<场景名>.html /tmp/atome-<场景名>.png
   或：
   python3 -c "from playwright.sync_api import sync_playwright; ..."
4. 返回 PNG 图片给用户

⚠️ 需要 playwright 或类似工具。若不可用，降级到 4D 输出代码。
```

### Step 4D：代码输出（任意环境）

```
根据场景模板的页面结构，生成 React/HTML 代码：
- 颜色使用 CSS 变量或 Token 值（不硬编码）
- 字号使用 Token 定义的值
- 间距遵循铁律（20px/16px/12px/8px）
- 圆角统一 8px
- 布局用 Flexbox / Auto Layout 语义
```

### Step 5：交叉验证

**验证方式（按优先级，不消耗 MCP）：**
1. **Canvas 对比**（Cursor IDE）→ 生成同场景 Canvas 预览，肉眼对比
2. **HTML 对比**（bot 环境）→ 生成同场景 HTML→PNG，对比截图
3. **`get_screenshot`**（仅用户明确要求时）→ **消耗 1 次 MCP 调用**

**验证清单：**
```
□ 所有颜色来自 Token（非硬编码）
□ 所有字号来自 Typography Token
□ 间距符合规范（20/16/12/8）
□ 组件优先用 DesignOps 已发布的（非手建）
□ 品牌色是黄色 #f0ff5f
□ Frame 命名遵循 <场景名> · <主题> 约定
□ MCP 调用总数 ≤ 预算（见 MCP 调用优化规则）
```

---

## Workflow：查询模式

### 查 Token
```
颜色 → docs/vocabulary/tokens/colors.md（68 个）
字体 → docs/vocabulary/tokens/typography.md（28 个）
阴影 → docs/vocabulary/tokens/shadows.md（3 个）
规范 → docs/vocabulary/tokens/conventions.md
机器层 → catalog/tokens/design-tokens.json
W3C 格式 → catalog/tokens/w3c-design-tokens.json
```

### 查组件
```
按类型 → docs/vocabulary/by-type/<type>.md（22 种）
按模块 → docs/vocabulary/by-module/<module>.md（10 个）
图标 → docs/vocabulary/icons/by-letter/<letter>.md
全量 → catalog/assets.json（3,200 条）
描述 → catalog/component-descriptions.json（248 条）
共现 → catalog/component-co-occurrence.json
```

### 查场景
```
索引 → docs/vocabulary/scenarios/README.md
模板 → docs/vocabulary/scenarios/<编号>-<名称>.md
页面模板 → catalog/page-templates.json
```

---

## Entrypoints

| 入口 | 路径 | 说明 |
|------|------|------|
| 词汇表总入口 | `docs/design-vocabulary.md` | 三层架构导航 + 铁律 |
| Token 数据 | `catalog/tokens/` | JSON，机器可读 |
| 组件索引 | `catalog/assets.json` | 3,200 组件含 Key |
| 分类索引 | `catalog/classified/` | 多维分类 |
| 语义文档 | `docs/vocabulary/` | 57 份 Markdown |
| 场景模板 | `docs/vocabulary/scenarios/` | 10 个业务场景 |
| 图标字典 | `docs/vocabulary/icons/` | 按字母索引 |

## MCP 调用优化规则

### 禁止调用清单

以下 Figma MCP 工具**禁止直接调用**，用本地数据替代：

| 禁止调用 | 替代方案 | 本地数据路径 |
|---------|---------|-------------|
| `search_design_system` | 本地查 Component Key | `catalog/assets.json`（3,200 条） |
| `get_variable_defs` | 本地查 Token 值 | `catalog/tokens/design-tokens.json` |
| `get_design_context` | 本地查场景结构 | `docs/vocabulary/scenarios/*.md` |
| `get_metadata` | 本地查组件分类 | `catalog/classified/*.json` |

### 允许调用的工具及上限

| 工具 | 场景 | 上限 |
|------|------|------|
| `use_figma` | 写入 Figma 页面 | **1 次/页**（批量脚本） |
| `get_screenshot` | 用户明确要求截图验证 | **1 次/页**（默认不调） |
| `create_new_file` | 创建新 Figma 文件 | **1 次/项目** |
| `get_libraries` | 首次确认库可用性 | **1 次/会话** |

### 调用预算

| 场景 | 最大调用次数 |
|------|------------|
| 预览/出图（Canvas / HTML→PNG / Code） | **0** |
| 写入 1 个 Figma 页面 | **1** |
| 写入 1 个页面 + 用户要求验证截图 | **2** |
| 写入 N 个页面 | **N**（每页 1 次批量脚本） |

### 批量脚本编写要点

1. 从 `catalog/assets.json` 预查所有组件 Key，写入脚本常量
2. 用 `Promise.all()` 并行导入所有组件
3. 所有布局、间距、文字、颜色在同一脚本中设置
4. 单次 `use_figma` 的 `code` 字段上限 50,000 字符，足够构建完整页面
5. Token 值直接内联（从 `design-tokens.json` 预查），不调 MCP 获取

---

## Guardrails

- 只读 skill，不修改文件、不调外部 API
- 品牌色为黄色 `#f0ff5f`（非绿色）
- 统一库：DesignOps(1,588) + Handover(1,612) = 3,200 组件
- Figma 写入需 Cursor 环境（官方 MCP 的 `use_figma`）
- Canvas 预览仅限 Cursor IDE，Lark/微信 bot 用 HTML→PNG 路径
- Token 统一从 `catalog/tokens/design-tokens.json` 读取
- DesignOps 中 SLOT 组件文案需设计师手调

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 3.0 | 2026-04-20 | MCP 调用优化：禁调清单 + 批量脚本（22→1 次/页）+ 调用预算 + Canvas 验证优先 |
| 2.2 | 2026-04-20 | 按运行环境区分 4 条出图路径；新增 4C HTML→PNG 适配 Lark/微信 bot |
| 2.1 | 2026-04-20 | 新增 Canvas 出图路径（Step 4B），零 MCP 调用实时预览 |
| 2.0 | 2026-04-23 | 增加生成流程：铁律 + 分步出图 Workflow + 代码输出路径 |
| 1.0 | 2026-04-23 | 初版：只读查询 |
