# 阴影 Token（3 个）

> [词汇表](../../design-vocabulary.md) › Tokens › Shadows

---

## 阴影列表

| Token 路径 | 透明度 | 用途 |
|-----------|--------|------|
| `shadow/shadow-01-8%` | 8% | 卡片阴影（主要，订单卡片/支付卡片） |
| `shadow/shadow-02-4%` | 4% | 轻量阴影（辅助容器/悬浮元素） |
| `shadow/screen` | — | 全屏遮罩阴影（Modal 背景） |

---

## 使用规则

1. **卡片用 `shadow-01-8%`**，配合 `color/greyscale/white` 卡片背景
2. **多层卡片嵌套时**，外层用 `shadow-01-8%`，内层不再叠加阴影
3. **底部 sheet / modal 用 `shadow/screen`** 作为遮罩
4. **禁止自定义阴影 hex / blur 参数**

## 与组件配合

| 组件 | 阴影 |
|------|------|
| Order Summary Card | `shadow/shadow-01-8%` |
| Payment Method Card | `shadow/shadow-01-8%` |
| Bottom Sheet 内卡片 | `shadow/shadow-02-4%` |
| Modal 蒙层 | `shadow/screen` |
| Toast / Notice | 无阴影（用边框） |
