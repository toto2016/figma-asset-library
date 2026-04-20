# 设计规范与约定

> [词汇表](../../design-vocabulary.md) › Tokens › Conventions

非 Token 但同等强制的设计约束。

---

## 1. 全局规范

| 属性 | 值 | 来源 |
|------|-----|------|
| 行高 lineHeight | 150% | DesignOps 标准 |
| 卡片圆角 | 8px | DesignOps Button 组件 |
| 小元素圆角 | 4px | DesignOps Tag/Badge |
| 字体 | GT Walsheim Pro | DesignOps 全局字体 |
| 按钮组件内字体 | Plus Jakarta Sans Bold | Button (Web) 内置 |

## 2. 间距体系（8 倍数）

| 场景 | 值 |
|------|-----|
| 页面水平 padding | 20px |
| 卡片内 padding | 16px |
| 卡片间距 | 12px |
| 元素行间距 | 8px |
| 紧凑行间距 | 4px |

## 3. 圆角体系

| 元素 | 圆角 |
|------|------|
| 卡片 / 按钮 | 8px |
| Tag / Badge / Chip | 4px |
| 状态 chip（圆形） | 999px |
| Modal / Bottom Sheet 顶部 | 16px |

## 4. 平台与库的取舍

### 优先级

1. **Web 库**（`Design library - web`）—— 默认首选，覆盖最全
2. **Mobile 库**（`Design library - Mobile`）—— 仅 Mobile 专属组件用（如 home Indicator）
3. **Merchant Centre Library** —— 商户后台专用，不要混用到消费者端
4. **Icon Library** —— 仅图标用

### Mobile 库的 5 个未发布组件（不可导入）

| 组件名 | 替代方案 |
|--------|---------|
| Navigation Bars (Mobile) | 用 Web 库 `page-header` |
| Tab Bars (Mobile) | 用 Web 库 `Tab` |
| Input (Mobile) | 用 Web 库 `Input Field` |
| toast (Mobile) | 用 Web 库 `Notice` |
| snack bar (Mobile) | 用 Web 库 `Message Container` |

## 5. AI 出图的禁忌清单

| 禁忌 | 替代 |
|------|------|
| 硬编码颜色 hex | 用 `color/*` Token |
| 硬编码字号/字重 | 用 `typography/*` Token |
| 自定义阴影参数 | 用 `shadow/*` Token |
| 截断的 8 字符 Component Key | 用完整 40 字符 key |
| 把所有内容堆在一个文件 | 按页面分类，按 file 分库 |
| 不调用 `loadFontAsync` 直接 setText | 必须先 await `loadFontAsync` |
| 用 `appendChild().property = x` 链式赋值 | 拆成两行：先 append，后赋值 |

## 6. Frame 命名约定

- 页面级 Frame：`<场景名> · <平台>`，如 `Merchant Checkout · Mobile`
- 卡片 Frame：`<卡片名> Card`，如 `Order Summary Card`
- 占位 Frame：`<内容> Placeholder`
