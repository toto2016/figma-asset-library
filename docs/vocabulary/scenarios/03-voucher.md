# 场景 03：Voucher Claim（优惠券领取/使用）

> [词汇表](../../design-vocabulary.md) › Scenarios › Voucher Claim
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：voucher
> **数据**：catalog 中 voucher 类型组件 [118 个](../by-type/voucher.md)，voucher 模块 [74 个](../by-module/voucher.md)

---

## 1. 典型页面

```
A. Voucher List       B. Voucher Detail      C. Voucher Applied
   (优惠券列表)          (券面 + 使用规则)      (结算页插槽 + Tag)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 顶部导航 | page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| 优惠券卡片 | （118 个 voucher 变体） | 见 [`by-type/voucher.md`](../by-type/voucher.md) |
| 标签 | Tag | `82ffa3b164fc4e04605893b1ee7943b207459dc8` |
| 计数器 | Counter | `d109459a8447cb213d85ca8cc5f0a722a9b605c8` |
| 主操作 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| 通知反馈 | Notification | `080ecfd53cbfdbe4f803e99b953655488b1062c5` |

## 3. Token

| 元素 | Token |
|------|-------|
| 页面背景 | `color/greyscale/surface` |
| 券面底色 | `color/brand/primary`（已用券）/ `color/greyscale/white`（待用） |
| 券面金额 | `typography/title/title-1` + `color/greyscale/dark-1` |
| 有效期 | `typography/caption/caption-1` + `color/greyscale/dark-4` |
| "Claim" 按钮 | `button/button-1` + `color/brand/primary` 底 |
| 已过期态 | `color/greyscale/grey-2` 灰化 + `color/greyscale/dark-4` 文字 |

## 4. 待补充（TODO）

- [ ] Voucher 卡片视觉模板（满减 / 折扣 / 现金券 三类样式）
- [ ] 已用 / 未用 / 已过期 三态视觉
- [ ] 券码展示（条形码/二维码）规范
- [ ] 多券叠加场景的 UI 规则
- [ ] 在 Checkout 页中插入 voucher 的位置
