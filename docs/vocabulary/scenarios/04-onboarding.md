# 场景 04：Onboarding（新手引导）

> [词汇表](../../design-vocabulary.md) › Scenarios › Onboarding
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：onboarding
> **数据**：catalog 中 onboarding 模块 [仅 6 个组件](../by-module/onboarding.md)（数据少 ⚠️）

---

## 1. 典型页面

```
1. Welcome Screen   →  2. Slide 1/3       →  3. Slide 2/3   →  4. Slide 3/3 + CTA
   (Logo + 欢迎)        (插画 + 标语)         (插画 + 标语)      (插画 + Get Started)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| Atome Logo | Atome-Logo Compact (Brand) | `0d6971c0412f9fbbaf82c4a9bac5c5ba6d05ce94` |
| 步骤指示器 | Pagination | `0c1f79ff7847725e6aac537eed7c50097149b7dd` |
| 主按钮 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| 跳过链接 | （文本，无组件） | — |
| Home Indicator | home Indicator | `59ea6015ee3db5633c4739d786314a318dad6d35` |

## 3. Token

| 元素 | Token |
|------|-------|
| 页面背景 | `color/greyscale/white` 或品牌渐变 |
| 大标题 | `typography/title/large-title(24pt)` + `color/greyscale/dark-1` |
| 副标题 | `typography/body/body-2` + `color/greyscale/dark-3` |
| 跳过链接 | `typography/body/body-3` + `color/others/blue` |
| 当前页指示 | `color/brand/primary` |
| 未达页指示 | `color/greyscale/grey-2` |

## 4. 待补充（TODO）

- [ ] 插画风格规范（DesignOps 是否有插画库？需查 [`by-type/image.md`](../by-type/image.md)）
- [ ] 引导页文案模板（每页几个字、字号、最大行数）
- [ ] 滑动手势 + 自动播放规则
- [ ] 跳过按钮位置（顶右 vs 底部）
- [ ] 完成 onboarding 后的跳转路径
