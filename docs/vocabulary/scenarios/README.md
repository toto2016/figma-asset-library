# 业务场景索引

> [词汇表](../../design-vocabulary.md) › Scenarios

10 个业务场景的"组件 → Token → 页面结构"映射模板，AI 出图时按模板装配，设计师按模板审阅。

---

## 场景清单

| # | 场景 | 模块 | 状态 | 文档 |
|---|------|------|------|------|
| 01 | Merchant Checkout | payment | ✅ 完整 | [01-merchant-checkout.md](01-merchant-checkout.md) |
| 02 | KYC Flow | kyc | 🟡 骨架 | [02-kyc-flow.md](02-kyc-flow.md) |
| 03 | Voucher Claim | voucher | 🟡 骨架 | [03-voucher.md](03-voucher.md) |
| 04 | Onboarding | onboarding | 🟡 骨架 | [04-onboarding.md](04-onboarding.md) |
| 05 | Payment Method | payment | 🟡 骨架 | [05-payment-method.md](05-payment-method.md) |
| 06 | Profile | profile | 🟡 骨架 | [06-profile.md](06-profile.md) |
| 07 | Notification | notification | 🟡 骨架 | [07-notification.md](07-notification.md) |
| 08 | Home Dashboard | home | 🟡 骨架 | [08-home.md](08-home.md) |
| 09 | Loan Apply | loan | 🟡 骨架 | [09-loan.md](09-loan.md) |
| 10 | Login & Signup | general | 🟡 骨架 | [10-login.md](10-login.md) |

---

## 状态约定

| 标记 | 含义 |
|------|------|
| ✅ 完整 | 已经过 L2 实装验证，可作为 AI 出图的权威模板 |
| 🟡 骨架 | 已列必备组件 + Token + TODO，需设计师补全 |
| 🔴 缺失 | 尚未规划 |

## 使用方式

### AI 出图时

1. 找到对应场景文档
2. 按"必备组件"清单 `importComponentByKeyAsync` 拿组件
3. 按"Token"映射设置颜色 / 字体 / 阴影
4. 按"页面结构"装配 frame

### 设计师审阅时

1. 看场景的页面结构是否完整
2. 检查组件 key 是否还有效（catalog 数据可能更新）
3. 补全 TODO 段
4. 实装后把状态升为 ✅ 完整
