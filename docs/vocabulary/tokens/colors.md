# 颜色 Token（68 个）

> [词汇表](../../design-vocabulary.md) › Tokens › Colors

来源：DesignOps 设计系统，所有 AI 出图必须使用 Token 路径，不允许硬编码 hex。

---

## 品牌色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/brand/primary` | `#f0ff5f` | 品牌主色（黄色） |
| `color/interaction/active-#` | `#f6ff7e` | 选中/激活态 |
| `color/interaction/pressed` | `#e3f90a` | 按压态 |
| `color/interaction/disabled` | `#e6e8f5` | 禁用态 |

## 灰阶

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/greyscale/dark-1` | `#141c30` | 主文字 |
| `color/greyscale/dark-3` | `#3e4459` | 次要文字 |
| `color/greyscale/dark-4` | `#878d9c` | 辅助文字/图标 |
| `color/greyscale/grey-1` | `#b6b9cb` | 占位文字 |
| `color/greyscale/grey-2` | `#cfd2e3` | 边框 |
| `color/greyscale/light-1` | `#eaeaea` | 分割线 |
| `color/greyscale/light-2` | `#f7f8ff` | 浅底色 |
| `color/greyscale/surface` | `#f6f6f6` | 页面背景 |
| `color/greyscale/white` | `#ffffff` | 卡片背景 |

## 功能色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/others/blue` | `#2247ff` | 链接/可交互文字 |
| `color/others/success` | `#25bc73` | 成功状态 |
| `color/others/error` | `#ed816e` | 错误状态 |
| `color/others/yellow` | `#f8c705` | 警告 |
| `color/others/pink` | `#ff3075` | 强调 |
| `color/others/dark-green` | `#089d4e` | 深绿 |
| `color/others/turquoise` | `#00f078` | 霓虹绿 |
| `color/error-pressed` | `#df6a56` | 错误按压态 |

## 图表色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/charts/trust-1` | `#2247ff` | 图表蓝 1 |
| `color/charts/trust-2` | `#7092fe` | 图表蓝 2 |
| `color/charts/trust-3` | `#a2b7ff` | 图表蓝 3 |
| `color/charts/trust-4` | `#d1dbff` | 图表蓝 4 |
| `color/charts/passion-1` | `#ff5741` | 图表红 1 |
| `color/charts/passion-2` | `#ff9d8f` | 图表红 2 |
| `color/charts/passion-3` | `#ffbdb6` | 图表红 3 |
| `color/charts/passion-4` | `#ffdfdb` | 图表红 4 |

## 补充色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/complementary/light-blue` | `#60d2fa` | 补充浅蓝 |
| `color/complementary/dark-blue` | `#002a5e` | 补充深蓝 |
| `color/complementary/pink` | `#ff3075` | 补充粉 |
| `color/complementary/neon-green` | `#00f078` | 补充霓虹绿 |
| `color/complementary/lilac` | `#c6b2f3` | 补充淡紫 |

## 遮罩

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/overlay/light` | `#000000` (含透明度) | 浅色遮罩 |
| `color/overlay/dark` | `#000000` (含透明度) | 深色遮罩 |

---

## 使用规则

1. **禁止硬编码 hex** —— 所有颜色必须引用 Token 路径
2. **品牌色（#f0ff5f 黄色）只用于主操作** —— 不要满屏黄
3. **`color/others/blue` 仅用于可点击文字** —— 不要用于装饰
4. **错误/警告状态优先用 Token，不自定义红色**
