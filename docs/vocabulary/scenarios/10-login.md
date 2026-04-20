# 场景 10：Login & Signup（登录注册）

> [词汇表](../../design-vocabulary.md) › Scenarios › Login & Signup
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：general（账号相关在 general 大类下）
> **数据**：DesignOps 通用模块 [1,259 个组件](../by-module/general.md)（含 Input Phone/OTP）

---

## 1. 典型流程

```
A. Phone Input    →  B. OTP Verify    →  C. Set Password  →  D. (新用户) Profile Setup
   (手机号 + 国旗)     (6 位验证码)         (密码 + 确认)        (姓/名 + 生日)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| Atome Logo | Atome-Logo Compact (Brand) | `0d6971c0412f9fbbaf82c4a9bac5c5ba6d05ce94` |
| 手机号输入 | Input Phone Number | `679244e3191b106dc611b111731b6843da023be6` |
| OTP 输入 | Input OTP | `792a72976c84a8bda25175586fd4d4165d252e43` |
| 密码输入 | Input Field | `836d5a56a46aacbb5736466a9ae81fa26977f3c8` |
| 主操作按钮 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| 协议勾选 | Checkbox | `526c219c0ff0720466dec4a0b120e3b40482c79b` |
| 错误提示 | Notice (Error) | `0d83c402b7480ad2a200c1f03ba687795bc68ca3` |
| Home Indicator | home Indicator | `59ea6015ee3db5633c4739d786314a318dad6d35` |

## 3. Token

| 元素 | Token |
|------|-------|
| 页面背景 | `color/greyscale/white` |
| 大标题 | `typography/title/large-title(24pt)` + `color/greyscale/dark-1` |
| 副标题 | `typography/body/body-2` + `color/greyscale/dark-3` |
| 手机号输入字号 | `typography/title/title-3` |
| OTP 单格字号 | `typography/title/title-2` |
| "Resend in Xs" | `typography/caption/caption-1` + `color/greyscale/dark-4`，可点后变 `color/others/blue` |
| 协议文本 | `typography/caption/caption-1` + `color/greyscale/dark-3` |
| "Terms" 链接 | `color/others/blue` |
| 错误态边框 | `color/others/error` |

## 4. 待补充（TODO）

- [ ] 国旗 + 区号选择器的 UI（Bottom Sheet 列表）
- [ ] OTP 倒计时 60s 的视觉规范
- [ ] 密码强度指示器 UI（弱/中/强 分段条）
- [ ] 第三方登录入口（Apple/Google/Facebook）的位置与图标
- [ ] 各国手机号格式与校验规则
- [ ] "忘记密码" 找回流程作为子场景
- [ ] 风控触发图形验证码 UI
