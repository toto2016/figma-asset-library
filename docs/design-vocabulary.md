# Atome 设计词汇表（AI Design Vocabulary）

> 一份给 AI 与设计师**共同使用**的词汇表，所有 AI 出图必须从这里查 Token、查组件、查场景映射。
>
> 数据来源：DesignOps 全量提取（catalog/classified）· 维护脚本：`scripts/build-vocabulary.js`
> 最近构建：见 [`vocabulary/.build-summary.json`](vocabulary/.build-summary.json)

---

## 为什么有这份词汇表

> Jimmy Xue 的反馈：AI 出图缺乏**"组件 / Token 一致性"**这一关。
> 词汇表把 1,588 个 DesignOps 组件 + 99 个 Token + 业务场景映射，全部摊在一个可检索的地方，
> 让 AI 出图不再凭直觉，而是按照设计系统**已定义的词汇**来组合。

### 三层架构定位

| 层 | 名称 | 词汇表的作用 | 状态 |
|----|------|------------|------|
| L1 | 设计系统层（组件/Token） | **直接服务于此层** —— 提供完整可查的 key 与 token 路径 | IN PROGRESS |
| L2 | UI 视觉细节（像素/间距/微交互） | 间接支撑 —— 通过 §3 场景模板提供基线 | NEXT |
| L3 | 业务逻辑 + 交互设计 | 不在范围 —— 由产品/设计师主导 | OUT OF SCOPE |

---

## 1. Token 体系（共 99 个）

| 子集 | 数量 | 文档 |
|------|------|------|
| 颜色 Color | 68 | [`vocabulary/tokens/colors.md`](vocabulary/tokens/colors.md) |
| 字体 Typography | 28 | [`vocabulary/tokens/typography.md`](vocabulary/tokens/typography.md) |
| 阴影 Shadow | 3 | [`vocabulary/tokens/shadows.md`](vocabulary/tokens/shadows.md) |
| 固定规范 Conventions | — | [`vocabulary/tokens/conventions.md`](vocabulary/tokens/conventions.md) |

---

## 2. 组件清单（共 1,588 个 DesignOps 组件 / 415 个图标变体）

数据由脚本从 `catalog/classified/` 自动生成，含每个组件的**完整 40 位 Component Key**。
所有变体的全量 keys 见 [`catalog/vocabulary-data.json`](../catalog/vocabulary-data.json)。

### 2.1 按 UI 类型查（22 类）

| 入口 | 说明 |
|------|------|
| [`vocabulary/by-type/`](vocabulary/by-type/README.md) | 按 button / input / card / modal 等组件类型导航 |

### 2.2 按业务模块查（10 模块）

| 入口 | 说明 |
|------|------|
| [`vocabulary/by-module/`](vocabulary/by-module/README.md) | 按 payment / kyc / merchant 等业务模块导航 |

### 2.3 图标库（96 唯一图标 / 415 变体）

| 入口 | 说明 |
|------|------|
| [`vocabulary/icons/`](vocabulary/icons/README.md) | 按首字母分组的 DesignOps Icon Library |

---

## 3. 业务场景 → 组件 + Token 映射（10 场景）

每个场景一份模板，AI 出图时按模板装配，设计师按模板审阅。

| # | 场景 | 状态 | 文档 |
|---|------|------|------|
| 01 | Merchant Checkout | ✅ 完整（含 L2 实测数据） | [`scenarios/01-merchant-checkout.md`](vocabulary/scenarios/01-merchant-checkout.md) |
| 02 | KYC Flow | 骨架 | [`scenarios/02-kyc-flow.md`](vocabulary/scenarios/02-kyc-flow.md) |
| 03 | Voucher Claim | 骨架 | [`scenarios/03-voucher.md`](vocabulary/scenarios/03-voucher.md) |
| 04 | Onboarding | 骨架 | [`scenarios/04-onboarding.md`](vocabulary/scenarios/04-onboarding.md) |
| 05 | Payment Method | 骨架 | [`scenarios/05-payment-method.md`](vocabulary/scenarios/05-payment-method.md) |
| 06 | Profile | 骨架 | [`scenarios/06-profile.md`](vocabulary/scenarios/06-profile.md) |
| 07 | Notification | 骨架 | [`scenarios/07-notification.md`](vocabulary/scenarios/07-notification.md) |
| 08 | Home Dashboard | 骨架 | [`scenarios/08-home.md`](vocabulary/scenarios/08-home.md) |
| 09 | Loan Apply | 骨架 | [`scenarios/09-loan.md`](vocabulary/scenarios/09-loan.md) |
| 10 | Login & Signup | 骨架 | [`scenarios/10-login.md`](vocabulary/scenarios/10-login.md) |

---

## 4. AI 出图规则（铁律）

### 4.1 组件选择优先级

1. **优先**：DesignOps 已发布组件（通过 `importComponentByKeyAsync`）
2. **次选**：同类组件优先 Web 库（Mobile 库有 5 个未发布，见 [`vocabulary/tokens/conventions.md`](vocabulary/tokens/conventions.md)）
3. **兜底**：用 Token 手建 Frame，**禁止硬编码颜色 / 字号 / 圆角**

### 4.2 文本样式速查

| 场景 | Token |
|------|-------|
| 页面标题 | `typography/title/title-3(16pt)` Bold |
| 卡片标题 | `typography/title/title-3(16pt)` Medium |
| 正文 | `typography/body/body-2(15pt)` Regular |
| 辅助文字 | `typography/caption/caption-1(13pt)` Regular |
| 按钮文字 | `typography/button/button-1(16pt)` Medium |

完整字体表：[`vocabulary/tokens/typography.md`](vocabulary/tokens/typography.md)

### 4.3 颜色速查

| 场景 | Token | 值 |
|------|-------|-----|
| 品牌主色 | `color/brand/primary` | `#f0ff5f` |
| 主文字 | `color/greyscale/dark-1` | `#141c30` |
| 可点击文字 | `color/others/blue` | `#2247ff` |
| 页面背景 | `color/greyscale/surface` | `#f6f6f6` |
| 卡片背景 | `color/greyscale/white` | `#ffffff` |

完整颜色表：[`vocabulary/tokens/colors.md`](vocabulary/tokens/colors.md)

### 4.4 间距与圆角

| 场景 | 值 |
|------|-----|
| 页面水平 padding | 20px |
| 卡片内 padding | 16px |
| 卡片间距 | 12px |
| 元素行间距 | 8px |
| 卡片圆角 | 8px |

---

## 5. 维护说明

### 5.1 自动化数据

`vocabulary/by-type/`、`vocabulary/by-module/`、`vocabulary/icons/` 与 `catalog/vocabulary-data.json` 由脚本生成，**不要手动编辑**。

```bash
node scripts/build-vocabulary.js
```

### 5.2 人工维护内容

| 文件 | 维护者 | 维护节奏 |
|------|--------|---------|
| `design-vocabulary.md`（本页） | AI + 设计师 | 季度 |
| `vocabulary/tokens/*.md` | 设计师为主 | Token 变更时 |
| `vocabulary/scenarios/*.md` | AI + 设计师协作 | 新场景上线时 |

### 5.3 历史版本

旧版单文件备份：[`design-vocabulary.legacy.md`](design-vocabulary.legacy.md)
