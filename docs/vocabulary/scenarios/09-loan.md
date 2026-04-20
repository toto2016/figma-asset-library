# 场景 09：Loan Apply（贷款申请）

> [词汇表](../../design-vocabulary.md) › Scenarios › Loan Apply
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：loan
> **数据**：catalog 中 loan 模块 [仅 3 个组件](../by-module/loan.md)（数据极少 ⚠️，需补全）

---

## 1. 典型流程

```
1. Loan Intro       →  2. Amount Input  →  3. Term Select   →  4. Confirm
   (额度展示 + CTA)     (金额输入 + 限制)    (期限单选 + 利率)    (协议 + 提交)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 顶部导航 | page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| 金额输入 | Input Amount | `615e82175afbc9de79daefa7dc81fe794c7157a1` |
| 期限单选 | Radio | `51952c258821247c831e6f8bcdcae320de4887ec` |
| 协议勾选 | Checkbox | `526c219c0ff0720466dec4a0b120e3b40482c79b` |
| 提交按钮 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| 信息图标 | icon.info（待查） | 见 [`icons/`](../icons/README.md) |
| Home Indicator | home Indicator | `59ea6015ee3db5633c4739d786314a318dad6d35` |

## 3. Token

| 元素 | Token |
|------|-------|
| 可用额度数字 | `typography/title/large-title(24pt)` + `color/greyscale/dark-1` |
| 金额输入字号 | `typography/title/title-1(21pt)` + `color/greyscale/dark-1` |
| 货币符号 | `typography/title/title-2` + `color/greyscale/dark-3` |
| 期限选项卡 | 选中 `color/brand/primary`，未选 `color/greyscale/white` |
| 利率说明 | `typography/caption/caption-1` + `color/others/blue` |
| 还款总额 | `typography/body/body-1` + `color/greyscale/dark-1` |
| 协议链接 | `typography/caption/caption-1` + `color/others/blue` 下划线 |

## 4. 待补充（TODO）

- [ ] 各国货币符号与格式（RM/RP/Php/MX$）
- [ ] 金额限制提示（最低 / 最高）的展示位置
- [ ] 期限选项与利率的对应表
- [ ] 风控失败/额度不足的错误页 UI
- [ ] 提交成功后的等待审核页（Loading + 文案）
- [ ] catalog 中 loan 仅 3 个组件 → 是否要从 Handover 项目补提取
