# 场景 01：Merchant Checkout（商户支付页）

> [词汇表](../../design-vocabulary.md) › Scenarios › Merchant Checkout
>
> **状态**：✅ 完整（已通过 L2 实装验证）
> **平台**：Mobile（390 × 844）
> **业务模块**：payment
> **最近 L2 实装**：[Stage 38 / 39 见 operation-log.md](../../../reports/operation-log.md)

---

## 1. 页面结构

```
┌─────────────────────────────────────┐
│ Status bar (Dark)                   │
│ page-header (with Icons, ←  Title) │  ← 顶部
├─────────────────────────────────────┤
│ Order Summary Card                  │
│   - Merchant Avatar + Name + Ref   │
│   - Product list (image + qty + ¥) │
│   - Order Total                    │
│                                     │
│ Payment Plan Card                   │
│   - Radio · 3 / 6 / 12 months      │
│   - 6m highlighted (brand color)   │
│   - "0% interest" hint             │
│                                     │
│ Payment Method Card                 │
│   - Bank Logo + DBS PayLah!        │
│   - "Change" link                  │
│                                     │
│ Agreement Card                      │
│   - Checkbox + legal text          │
├─────────────────────────────────────┤
│ Confirm Button (Big Primary)        │  ← 底部
│ 🔒 Atome secure · Atome Logo        │
│ home Indicator                      │
└─────────────────────────────────────┘
```

## 2. 组件 → Component Key 映射

> 全部为 DesignOps Web 库（`Design library - web`），可通过 `importComponentByKeyAsync` 导入。

| # | 元素 | 组件名 | Component Key |
|---|------|--------|---------------|
| 1 | 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 2 | 顶部导航 | page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| 3 | 关闭图标 | icon.close | `0c9370f3ee466b1ce52e4461e7ce0c24372453f8` |
| 4 | 返回箭头 | icon.arrow-left | `f6da59d17b106f343fdc7bfe983eb5c0af4c8e96` |
| 5 | 商户头像 | Avatar (Merchant logo) | `1da2e978cc392829adfe16315fdffa110a0347ad` |
| 6 | 分期选项 | Radio (Selected/Default) | `51952c258821247c831e6f8bcdcae320de4887ec` |
| 7 | 展开图标 | icon.caret-down | `3b43bd215dbc0464b755ccf5dd832a40c7c220cb` |
| 8 | 银行 Logo | Bank Logo (BCA/BNI 等) | `4cea9627c25de4ce324004c3df70f62dc89770b9` |
| 9 | 协议勾选 | Checkbox (Selected) | `526c219c0ff0720466dec4a0b120e3b40482c79b` |
| 10 | 确认按钮 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| 11 | 安全锁图标 | icon.secure | `14342de4ed7265d4c4e93a5b9ed5d33f8dc22952` |
| 12 | Atome Logo | Atome-Logo Compact (Brand) | `0d6971c0412f9fbbaf82c4a9bac5c5ba6d05ce94` |
| 13 | Home Indicator | home Indicator (No On Color) | `59ea6015ee3db5633c4739d786314a318dad6d35` |

> **注**：表中 key 来自 catalog 全量提取，以 [`catalog/vocabulary-data.json`](../../../catalog/vocabulary-data.json) 为准。
> 如有不符以 catalog 数据为权威，并修订本表。

## 3. Token 映射

| 元素 | Token |
|------|-------|
| 页面背景 | `color/greyscale/surface` (`#f6f6f6`) |
| 卡片背景 | `color/greyscale/white` |
| 卡片阴影 | `shadow/shadow-01-8%` |
| 卡片圆角 | 8px |
| 商户名称 | `typography/title/title-3` + `color/greyscale/dark-1` |
| 订单编号 | `typography/caption/caption-1` + `color/greyscale/dark-4` |
| 商品名称 | `typography/body/body-2` + `color/greyscale/dark-1` |
| 价格（右对齐） | `typography/body/body-1` + `color/greyscale/dark-1` |
| 分期选中底色 | `color/brand/primary` (`#f0ff5f`) |
| 分期金额 | `typography/title/title-2` + `color/greyscale/dark-1` |
| "0% interest" | `typography/caption/caption-1` + `color/others/success` |
| "Change" 链接 | `typography/body/body-3` + `color/others/blue` |
| 协议文本 | `typography/caption/caption-1` + `color/greyscale/dark-3` |
| 安全提示 | `typography/caption/caption-3` + `color/greyscale/dark-4` |

## 4. 间距规范

| 区域 | 值 |
|------|-----|
| 页面水平 padding | 20px |
| 卡片之间 | 12px |
| 卡片内 padding | 16px |
| 卡片内行间距 | 8px |

## 5. 已知坑

1. **page header 标题**：`page-header` 默认变体不显示 title 文字，需手动设置实例属性 `Title=Order Summary`
2. **状态 chip 必须 HUG 不能 FILL**：否则会铺满父容器变成大圆球
3. **page frame 不能用 fixed 高度**：内容易超出，必须 `primaryAxisSizingMode='AUTO'`
4. **`appendChild()` 链式赋值会 null**：必须拆两行

## 6. 相关文件

- L2 实装截图：`screenshots/L2_Merchant_Checkout/`（待补）
- 实装记录：[reports/operation-log.md Stage 38 & 39](../../../reports/operation-log.md)
- Figma 文件：`AI Generated Screens` (`tZfhizmsTeqIrP6Qnq0V86`) › Checkout Flow 页
