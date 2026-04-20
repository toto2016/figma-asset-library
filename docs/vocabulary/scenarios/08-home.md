# 场景 08：Home Dashboard（首页）

> [词汇表](../../design-vocabulary.md) › Scenarios › Home
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：home
> **数据**：catalog 中 home 模块 [65 个组件](../by-module/home.md)

---

## 1. 典型页面

```
┌─────────────────────────────────────┐
│ Status bar + 用户头像 + 通知图标       │
├─────────────────────────────────────┤
│ 信用额度卡片（已用/总额度）              │
│ ┌─ 总可用 / 已用 / 下次还款日 ─┐      │
├─────────────────────────────────────┤
│ 快捷入口（4-6 个 icon + 文字）          │
│ [Pay] [Voucher] [History] [Help]    │
├─────────────────────────────────────┤
│ 推广 Banner / 优惠券滚动              │
│ 商户推荐列表                          │
├─────────────────────────────────────┤
│ Bottom Navigation (Home/Pay/Profile)│
└─────────────────────────────────────┘
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 用户头像 | Avatar | `1da2e978cc392829adfe16315fdffa110a0347ad` |
| 通知图标 | icon.bell（待查） | 见 [`icons/`](../icons/README.md) |
| 入口图标 | icon.* | 见 [`icons/`](../icons/README.md) |
| 优惠券 | Voucher 系列 | 见 [`by-type/voucher.md`](../by-type/voucher.md) |
| 列表 | List | 见 [`by-type/list.md`](../by-type/list.md) |
| 标签 | Tag | `82ffa3b164fc4e04605893b1ee7943b207459dc8` |
| 底部导航 | Bottom Navigation | `97a2cdbd49aba76abf260aedc9403293554e54f4` |
| Home Indicator | home Indicator | `59ea6015ee3db5633c4739d786314a318dad6d35` |

## 3. Token

| 元素 | Token |
|------|-------|
| 页面背景 | `color/greyscale/surface` |
| 信用额度卡片 | 品牌渐变（待定）或 `color/greyscale/dark-1` 深色卡 |
| 总可用金额 | `typography/title/large-title(24pt)` + `color/greyscale/white`（深卡上）|
| 入口图标背景 | `color/greyscale/white` 圆形 + `shadow/shadow-02-4%` |
| 入口文字 | `typography/caption/caption-1` + `color/greyscale/dark-3` |
| Banner 圆角 | 8px |
| 商户列表项 | `typography/body/body-2` |

## 4. 待补充（TODO）

- [ ] 信用额度卡片的视觉模板（已用比例进度条、CTA 位置）
- [ ] 入口图标的固定数量与排序规则
- [ ] Banner 轮播规则与文字模板
- [ ] 商户列表的卡片密度（图片大小 / 行高）
- [ ] 不同信用状态的视觉差异（正常 / 即将逾期 / 已逾期）
- [ ] 各国首页差异（ID/PH/MX）
