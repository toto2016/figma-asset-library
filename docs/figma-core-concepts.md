# Figma 核心概念手册

与素材库建设直接相关的 Figma 概念，从大到小讲解。

---

## 一、组织层级（文件管理）

```
Organization（组织）          ← Neuroncredit Pte Ltd
  └── Team（团队）            ← Atome UED
        └── Project（项目）   ← Flow Library、DesignOps、Atome AI Test...
              └── File（文件） ← 每个具体的设计文件
                    └── Page（页面） ← 文件内的画布页面
```

| 层级 | 说明 |
|------|------|
| **Organization** | 公司级别，管理所有团队和权限 |
| **Team** | 设计团队，共享资源和库 |
| **Project** | 按工作类型分组（流程库、设计走查等） |
| **File** | 独立的设计文档，有唯一的 fileKey |
| **Page** | 画布的"标签页"，可按场景/版本组织 |

---

## 二、画布节点类型

打开一个文件后，画布上所有可见元素都是**节点（Node）**。

### Frame（框架）

最基础的容器，相当于 HTML 的 `<div>`。

- 设置固定尺寸或自适应
- 添加背景色、圆角、阴影
- 嵌套其他元素
- 开启 Auto Layout 变成弹性布局

**用途**: 页面布局、卡片、按钮外壳、任何"容器"

### Section（区块）

比 Frame 更高层的组织单元，用于在画布上划分区域。

**用途**: 把一个页面上的多个设计方案分区管理，如"方案 A"、"方案 B"

### Text（文本）

文字节点，属性包括：字体、字号、字重、行高、字间距等。

### 基础图形

Rectangle（矩形）、Ellipse（椭圆）、Line（线条）、Vector（矢量路径）、
Polygon（多边形）、Star（星形）等。

---

## 三、组件系统（核心重点）

### Component（组件）

可复用的设计模板。创建一次，可在任何地方引用。修改源组件，所有引用同步更新。

```
Component（主组件）     → 设计模板，只有一份
  └── Instance（实例）  → 引用副本，可以有多份
```

类比代码：Component = class，Instance = object。

### Component Set（组件集）+ Variants（变体）

一个组件的多种状态/规格打包在一起。

```
Button 组件集
  ├── Size=Small, Style=Primary, State=Default
  ├── Size=Small, Style=Primary, State=Hover
  ├── Size=Medium, Style=Primary, State=Default
  ├── Size=Medium, Style=Secondary, State=Default
  └── ...
```

每种属性组合是一个 Variant（变体），通过属性值区分。

### Instance（实例）

组件的引用副本，保持与主组件关联。可以：

- **覆盖文本**（如 "Button" → "Submit"）
- **切换变体**（如 Primary → Secondary）
- **交换组件**（替换为另一个组件）
- 不能改变结构（不能删除子元素）

**素材库意义**: 出图时就是创建组件实例、覆盖文本、选择变体。

---

## 四、Design Token

### Variable（变量）

设计中的变量，和代码中的概念一致。

```
变量名: color/primary
值:     #3B59F5 (Light 模式) / #6B8AFF (Dark 模式)
```

变量类型：

| 类型 | 用途 | 示例 |
|------|------|------|
| COLOR | 颜色 | 品牌色、背景色、文字色 |
| FLOAT | 数值 | 间距、圆角、字号 |
| STRING | 字符串 | 字体名称 |
| BOOLEAN | 布尔值 | 是否可见 |

### Variable Collection（变量集合）

变量的分组容器，典型组织方式：

```
Primitives 集合（原始值）
  ├── blue/500 = #3B82F6
  ├── gray/900 = #111827
  └── ...

Color 集合（语义化，支持模式切换）
  ├── color/bg/primary   → Light: white, Dark: gray-900
  ├── color/text/primary  → Light: gray-900, Dark: white
  └── ...

Spacing 集合
  ├── spacing/xs = 4
  ├── spacing/sm = 8
  └── spacing/md = 16
```

### Mode（模式）

一个变量集合可以有多个模式，典型场景：

- **Light / Dark** -- 主题切换
- **Mobile / Desktop** -- 响应式
- **中文 / English** -- 多语言

**素材库意义**: 提取变量时需记录每个模式下的具体值。

---

## 五、样式（Style）

### Text Style（文字样式）

预定义的排版规范：字体、字号、字重、行高、字间距。

```
Heading/H1 → Inter Bold 32px / 行高 40px
Body/Regular → Inter Regular 14px / 行高 20px
Caption → Inter Medium 12px / 行高 16px
```

### Effect Style（效果样式）

预定义的视觉效果，主要是阴影和模糊。

```
Shadow/Small → Drop Shadow: 0 1px 2px rgba(0,0,0,0.1)
Shadow/Large → Drop Shadow: 0 4px 16px rgba(0,0,0,0.15)
Blur/Background → Background Blur: 8px
```

**素材库意义**: 样式和变量一样是 Design Token 的一部分，需要完整提取。

---

## 六、Auto Layout（自动布局）

Figma 的弹性布局系统，类似 CSS Flexbox。

| Auto Layout 属性 | CSS 对应 | 说明 |
|------------------|---------|------|
| layoutMode: HORIZONTAL | flex-direction: row | 水平排列 |
| layoutMode: VERTICAL | flex-direction: column | 垂直排列 |
| itemSpacing | gap | 子元素间距 |
| paddingLeft/Right/Top/Bottom | padding | 内边距 |
| primaryAxisAlignItems | justify-content | 主轴对齐 |
| counterAxisAlignItems | align-items | 交叉轴对齐 |

子元素尺寸模式：

| 模式 | CSS 类比 | 说明 |
|------|---------|------|
| FIXED | width: 200px | 固定宽高 |
| FILL | flex: 1 | 撑满父容器 |
| HUG | fit-content | 包裹内容 |

---

## 七、Library（库）

### Team Library（团队库）

把一个文件中的组件、变量、样式**发布**出去，团队中的其他文件可以引用。

```
Design System 文件（发布为库）
  ├── Button 组件
  ├── Input 组件
  └── color/primary 变量

Product A 文件（引用库）
  └── 使用 Button 的实例（保持同步）
```

**素材库意义**:

- `search_design_system` 搜索的是已发布的库资产
- Phase 4 创建的统一组件库要发布为团队库
- 出图时通过 `importComponentSetByKeyAsync(key)` 导入库组件

---

## 八、MCP 工具与概念对应关系

| Figma 概念 | 提取工具 | 提取内容 | 素材库价值 |
|-----------|---------|---------|-----------|
| File/Page | get_metadata | 页面结构、顶层 frame | 了解设计稿组织方式 |
| Component | use_figma | 名称、key、description | **核心素材**，出图时直接导入 |
| Component Set | use_figma | 变体列表、属性定义 | 组件的多种状态规格 |
| Variable | use_figma | 颜色、间距、圆角 token | 保证视觉一致性 |
| Text Style | use_figma | 字体规范 | 排版标准 |
| Effect Style | use_figma | 阴影/模糊 | 视觉效果标准 |
| Instance | use_figma | 使用了哪些组件 | 了解组件实际使用场景 |
| Library | search_design_system | 已发布的库资产 | 可直接复用的组件和 token |

---

## 九、key 和 ID 的区别

这两个概念容易混淆，但在素材库中非常重要：

| 属性 | 作用域 | 稳定性 | 用途 |
|------|-------|--------|------|
| **id** | 文件内唯一 | 不稳定，可能变化 | 在同一次 use_figma 中引用节点 |
| **key** | 全局唯一 | 稳定，不会变化 | 跨文件导入组件/样式 |

- 用 `id` 在一个脚本中找到和操作节点
- 用 `key` 从库中导入组件：`figma.importComponentSetByKeyAsync(key)`
- 素材库索引应记录 `key`（跨文件复用）和 `id`（定位源位置）
