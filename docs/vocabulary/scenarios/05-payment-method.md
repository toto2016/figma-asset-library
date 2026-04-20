# 场景 05：Payment Method（支付方式管理）

> [词汇表](../../design-vocabulary.md) › Scenarios › Payment Method
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：payment
> **数据**：catalog 中 payment 模块 [336 个组件](../by-module/payment.md)（含 bank icon × 138 等大量变体）

---

## 1. 典型页面

```
A. Method List   →  B. Add Method        →  C. Bank/Card Linking
   (已绑列表)        (Bottom Sheet 选类型)     (输入卡号/账号)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 顶部导航 | page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| 银行 Logo | Bank Logo (BCA/BNI/DBS 等) | `4cea9627c25de4ce324004c3df70f62dc89770b9` |
| 钱包 Logo | Wallet Logo (OVO/PayLah! 等) | `2480a879fdb30a665c27a18c52b6c3f3c94dc5ba` |
| 单选项 | Radio | `51952c258821247c831e6f8bcdcae320de4887ec` |
| 添加按钮 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| 选择面板 | Bottom Sheet | `7f1b2375549ce224cb8786990ad548934aeed157` |
| 操作菜单 | Action Sheet | `669aafcd8d9b07202d5c7ec6295bb62210a48992` |
| 卡号输入 | Input Field | `836d5a56a46aacbb5736466a9ae81fa26977f3c8` |

> 银行/钱包 Logo 全部变体（BCA/BNI/Mandiri/DBS/OCBC 等）见 [`by-module/payment.md`](../by-module/payment.md)

## 3. Token

| 元素 | Token |
|------|-------|
| 卡片背景 | `color/greyscale/white` |
| 卡片阴影 | `shadow/shadow-01-8%` |
| 默认 Tag | 文字用 `color/others/blue` |
| 已绑账号文字 | `typography/body/body-2` + `color/greyscale/dark-1` |
| 账号尾号 | `typography/caption/caption-1` + `color/greyscale/dark-4` |
| "Set as default" | `typography/body/body-3` + `color/others/blue` |

## 4. 待补充（TODO）

- [ ] 各国支持的支付方式清单（ID/PH/MX/SG）
- [ ] 卡号输入格式（4-4-4-4 分组、自动识别卡组织）
- [ ] CVV 输入与安全提示位置
- [ ] 删除已绑方式的二次确认 UI
- [ ] 默认支付方式的视觉标记（Tag / Icon）
