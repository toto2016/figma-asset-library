# 字体 Token（28 个）

> [词汇表](../../design-vocabulary.md) › Tokens › Typography

字体系列：**GT Walsheim Pro**（按钮组件内部使用 **Plus Jakarta Sans Bold**）

---

## Mobile 字体（15 个）

| Token 路径 | 字重 | 字号 | 用途 |
|-----------|------|------|------|
| `typography/title/large-title(24pt)` | Bold (700) | 24px | 大标题 |
| `typography/title/title-1(21pt)` | Bold (700) | 21px | 一级标题 |
| `typography/title/title-2(18pt)` | Bold (700) | 18px | 二级标题 |
| `typography/title/title-3(16pt)` | Bold (700) | 16px | 三级标题（页面 Title） |
| `typography/title/title-4(15pt)` | Bold (700) | 15px | 四级标题 |
| `typography/title/headline(14pt)` | Bold (700) | 14px | 小标题 |
| `typography/title/subhead(12pt)` | Bold (700) | 12px | 副标题 |
| `typography/body/body-1(16pt)` | Medium (500) | 16px | 正文 1（强调） |
| `typography/body/body-2(15pt)` | Regular (400) | 15px | 正文 2（默认） |
| `typography/body/body-3(14pt)` | Regular (400) | 14px | 正文 3（紧凑） |
| `typography/button/button-1(16pt)` | Medium (500) | 16px | 按钮文字 1 |
| `typography/button/button-2(15pt)` | Bold (700) | 15px | 按钮文字 2 |
| `typography/caption/caption-1(13pt)` | Regular (400) | 13px | 说明文字 1 |
| `typography/caption/caption-2(12pt)` | Regular (400) | 12px | 说明文字 2 |
| `typography/caption/caption-3(10pt)` | Regular (400) | 10px | 说明文字 3 |

## Desktop 字体（13 个）

| Token 路径 | 字重 | 字号 |
|-----------|------|------|
| `typography/desktop/title/large-title-(38pt)` | Bold | 38px |
| `typography/desktop/title/title-1-(30pt)` | Bold | 30px |
| `typography/desktop/title/title-2-(24pt)` | Bold | 24px |
| `typography/desktop/title/title-3-(20pt)` | Bold | 20px |
| `typography/desktop/title/title-4-(18pt)` | Bold | 18px |
| `typography/desktop/title/title-5-(16pt)` | Bold | 16px |
| `typography/desktop/body/body-1-(18pt)` | Regular | 18px |
| `typography/desktop/body/body-2-(16pt)` | Regular | 16px |
| `typography/desktop/body/body-3-(14pt)` | Regular | 14px |
| `typography/desktop/button/button-1-(16pt)` | Bold | 16px |
| `typography/desktop/button/button-2-(14pt)` | Bold | 14px |
| `typography/desktop/caption/caption-1-(12pt)` | Regular | 12px |
| `typography/desktop/caption/caption-2-(10pt)` | Regular | 10px |

---

## 全局规范

- **字体系列**：GT Walsheim Pro（移动端 / Web 通用）
- **行高**：150% 固定
- **字距**：默认 0
- **按钮字体例外**：DesignOps Button 组件内部使用 Plus Jakarta Sans Bold

## 用法对照（AI 出图常用）

| 场景 | Token | 备注 |
|------|-------|------|
| 页面标题 | `title/title-3(16pt)` | 默认 Bold |
| 卡片标题 | `title/title-3(16pt)` | 设计师常用 Medium 字重 |
| 正文 | `body/body-2(15pt)` | 最通用 |
| 辅助文字 | `caption/caption-1(13pt)` | 灰阶 dark-4 |
| 小标签 | `caption/caption-3(10pt)` | 安全提示等 |
| 按钮文字 | `button/button-1(16pt)` | Medium |
