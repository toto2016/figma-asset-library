# Styles → Variables 迁移方案

> 基于 163 个现有 Design Token 的分析
> 目标：将传统 Styles 迁移到 Figma Variables，支持 Light/Dark Mode 和响应式
>
> **2026-04-16 修订**：APB 数据已全部删除（含 KP 品牌复制内容）。Atome 品牌色为黄色(#f0ff5f)，非绿色。字体策略调整为 GT Walsheim Pro + Plus Jakarta Sans 并存（待设计师最终定夺）。

---

## 一、现状分析

### 当前 Token 分布

| 类型 | 数量 | 唯一值 | 来源 |
|------|------|--------|------|
| 颜色 | 60 | DesignOps 唯一色值 | DesignOps(55) + 其他(5)，APB 40 个已删除 |
| 字体 | 28 | 1 个主字体家族 | GT Walsheim Pro(28, DesignOps)，Plus Jakarta Sans 待设计师定夺 |
| 效果 | 5 | Shadow 相关 | 少量 |

### 发现的问题

1. **100 个颜色 Token 只有 34 个唯一色值**——大量重复定义
2. **字体**：DesignOps 用 GT Walsheim Pro（重点项目），Plus Jakarta Sans 是否保留待设计师定夺
3. **颜色命名不规范**：混用 `greyscale/dark 1 #141C30`（含色值）和 `Button/Default`（语义化）
4. **Variables = 0**：全部用传统 Styles，无法支持 Mode 切换

### 颜色分组现状

| 分组 | 数量 | 说明 |
|------|------|------|
| Desktop | 13 | 桌面端专用 |
| Title | 11 | 标题文字色 |
| Body / Body-Bold | 16 | 正文文字色 |
| greyscale | 9 | 灰度色阶 |
| Charts | 8 | 图表配色 |
| Others | 8 | 杂项 |
| Button | 7 | 按钮色 |
| Caption | 5 | 说明文字 |
| complementary | 5 | 辅助色 |
| brand | 1 | 品牌色 |

---

## 二、Variables 架构设计

### 三层 Token 结构（行业最佳实践）

```
Layer 1: Primitive（原始值）
  → color/gray/900: #141C30
  → color/brand/primary: #00D26A  ← 错误！此为 KP 品牌色，Atome 品牌色是黄色

Layer 2: Semantic（语义别名）
  → text/primary: {color/gray/900}
  → bg/surface: {color/white}
  → interactive/default: {color/brand/primary}

Layer 3: Component（组件级）
  → button/bg/primary: {interactive/default}
  → card/bg: {bg/surface}
```

### Variable Collection 规划

| Collection | 用途 | Mode 支持 | 变量数(预估) |
|-----------|------|-----------|-------------|
| `primitives/color` | 原始颜色色阶 | — | ~40 |
| `primitives/spacing` | 间距基础值 | — | ~12 |
| `primitives/radius` | 圆角基础值 | — | ~6 |
| `primitives/typography` | 字号/行高/字重 | — | ~15 |
| `semantic/color` | 语义颜色映射 | Light / Dark | ~30 |
| `semantic/spacing` | 语义间距 | Compact / Default | ~10 |
| `component/button` | Button 专用 | — | ~8 |
| `component/card` | Card 专用 | — | ~5 |
| **合计** | | | **~126** |

---

## 三、颜色 Token 迁移映射

### Primitive 层（从 34 个唯一值推导）

| Variable 名 | 值 | 对应旧 Style |
|-------------|-----|-------------|
| `color/gray/900` | #141C30 | greyscale/dark 1 |
| `color/gray/800` | #3D4659 | greyscale/dark 2 |
| `color/gray/600` | #6B7280 | greyscale/medium |
| `color/gray/400` | #9CA3AF | greyscale/light 2 |
| `color/gray/200` | #E5E7EB | greyscale/light 1 |
| `color/gray/50` | #F9FAFB | greyscale/lightest |
| `color/brand/primary` | **#f0ff5f** | **Atome 品牌色 — 黄色**（来自 DesignOps Mobile） |
| `color/brand/red` | #FF5844 | complementary/error |
| `color/brand/blue` | #3B82F6 | Interaction/link |
| `color/brand/yellow` | #FBBF24 | complementary/warning（可能就是品牌主色） |

### Semantic 层（支持 Light/Dark Mode）

| Variable 名 | Light Mode | Dark Mode |
|-------------|-----------|-----------|
| `text/primary` | {color/gray/900} | {color/gray/50} |
| `text/secondary` | {color/gray/600} | {color/gray/400} |
| `text/disabled` | {color/gray/400} | {color/gray/600} |
| `bg/surface` | #FFFFFF | {color/gray/900} |
| `bg/subtle` | {color/gray/50} | {color/gray/800} |
| `border/default` | {color/gray/200} | {color/gray/600} |
| `interactive/primary` | {color/brand/primary} | {color/brand/primary} |
| `interactive/danger` | {color/brand/red} | {color/brand/red} |
| `interactive/info` | {color/brand/blue} | {color/brand/blue} |
| `status/success` | ~~{color/brand/green}~~ 需确认 | ~~{color/brand/green}~~ 需确认 |
| `status/error` | {color/brand/red} | {color/brand/red} |
| `status/warning` | {color/brand/yellow} | {color/brand/yellow} |

---

## 四、字体 Token 迁移

### 现状：两套字体体系

| 体系 | 字体 | Token 数 | 使用范围 |
|------|------|---------|---------|
| DesignOps（重点项目） | GT Walsheim Pro | 28 | Mobile/Web/Merchant |

### 迁移策略

> **修订**：APB 已删除。GT Walsheim Pro 为当前主字体，Plus Jakarta Sans 是否需要保留待设计师决定。

统一库保留**两套字体**，均设为一级变量：

| Variable 名 | 值 | 对应旧 Style | 来源 |
|-------------|-----|-------------|------|
| `font/family/walsheim` | GT Walsheim Pro | DesignOps 系列 | 重点项目 |
| `font/family/jakarta` | Plus Jakarta Sans | 待设计师定夺 | 是否保留 |
| `font/size/xs` | 10 | Caption/Caption |
| `font/size/sm` | 12 | Body/Small |
| `font/size/md` | 14 | Body/Default |
| `font/size/lg` | 16 | Body/Large |
| `font/size/xl` | 20 | Title/Small |
| `font/size/2xl` | 24 | Title/Default |
| `font/size/3xl` | 32 | Title/Large |
| `font/weight/regular` | 400 | Regular |
| `font/weight/medium` | 500 | Medium |
| `font/weight/semibold` | 600 | Semi Bold |
| `font/weight/bold` | 700 | Bold |

---

## 五、效果 Token 迁移

| Variable 名 | 值 | 对应旧 Style |
|-------------|-----|-------------|
| `shadow/sm` | 0 1px 2px rgba(0,0,0,0.05) | Shadow/light |
| `shadow/md` | 0 4px 6px rgba(0,0,0,0.07) | Shadow/default |
| `shadow/lg` | 0 10px 15px rgba(0,0,0,0.1) | Shadow/heavy |
| `shadow/card` | 0 2px 8px rgba(0,0,0,0.08) | Shadow/card |
| `shadow/modal` | 0 20px 25px rgba(0,0,0,0.15) | Shadow/modal |

---

## 六、执行步骤

### Phase 1: 创建 Variable Collections（在 Atome AI Test 中）

通过 `use_figma` 调用 Plugin API：

```javascript
// 步骤 1: 创建 Collection
const primitives = figma.variables.createVariableCollection('primitives/color')
primitives.renameMode(primitives.modes[0].modeId, 'Value')

// 步骤 2: 创建 Variables
const gray900 = figma.variables.createVariable('color/gray/900', primitives, 'COLOR')
gray900.setValueForMode(primitives.modes[0].modeId, {r: 0.078, g: 0.11, b: 0.188, a: 1})
```

### Phase 2: 创建 Semantic 层（带 Light/Dark Mode）

```javascript
const semantic = figma.variables.createVariableCollection('semantic/color')
const lightMode = semantic.modes[0]
semantic.renameMode(lightMode.modeId, 'Light')
const darkModeId = semantic.addMode('Dark')

const textPrimary = figma.variables.createVariable('text/primary', semantic, 'COLOR')
textPrimary.setValueForMode(lightMode.modeId, gray900AliasValue)
textPrimary.setValueForMode(darkModeId, gray50AliasValue)
```

### Phase 3: 绑定组件属性到 Variables

```javascript
const button = figma.currentPage.findOne(n => n.name === 'Button')
button.setBoundVariable('fills', 0, 'color', buttonBgPrimary)
```

### 预估调用量

| 步骤 | MCP 调用 | 说明 |
|------|---------|------|
| 创建 Primitive Collection | 1 | ~40 变量 |
| 创建 Semantic Collection | 1 | ~30 变量 + 2 Modes |
| 创建 Spacing/Radius/Typography | 3 | 各 1 次调用 |
| 绑定组件属性 | ~5 | 每批绑定 5-10 个组件 |
| **合计** | **~10** | 控制在 MCP 日额度内 |

---

## 七、收益评估

| 能力 | 迁移前 | 迁移后 |
|------|--------|--------|
| Light/Dark Mode | ❌ 不支持 | ✅ 一键切换 |
| 品牌换肤 | ❌ 手动改色 | ✅ 换 Mode 即可 |
| 响应式间距 | ❌ 固定值 | ✅ Compact/Default 切换 |
| 颜色一致性 | ⚠️ 34 个值分散在 100 个 Style | ✅ 40 个 Primitive 统一管理 |
| 设计开发交接 | ⚠️ 靠截图标注 | ✅ Variable 名直接对应代码 Token |
| 字体统一 | ❌ 两套并存无管理 | ✅ 两套字体均注册为变量，待设计师统一决策 |

---

## 八、风险与缓解

| 风险 | 概率 | 缓解措施 |
|------|------|---------|
| use_figma 权限不足 | 低 | 在 Atome AI Test（有编辑权限）中操作 |
| Variable 命名与开发不一致 | 中 | 命名采用 CSS custom property 风格，与前端 Token 映射 |
| GT Walsheim Pro 字体加载失败 | 中 | 先用 `loadFontAsync` 测试，失败则跳过 |
| 迁移后旧文件引用断裂 | 低 | 仅在新统一库中使用 Variables，旧文件保持不动 |
