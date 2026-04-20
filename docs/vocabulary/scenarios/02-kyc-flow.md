# 场景 02：KYC Flow（实名认证）

> [词汇表](../../design-vocabulary.md) › Scenarios › KYC Flow
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：kyc
> **数据**：catalog 中 kyc 模块共 [334 个组件](../by-module/kyc.md)

---

## 1. 流程页面（典型 4 步）

```
1. KYC Intro     →  2. ID Card Scan  →  3. Selfie       →  4. Confirm Info
   (说明 + 开始)     (相机 + 提示)        (人脸框 + 拍照)    (字段确认 + 提交)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 顶部导航 | page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| 步骤指示器 | Stepper | `abc39b5a2ceb816871806b3c962c2a4598a8d3f4` |
| 拍照按钮 | Camera Button | `450af281a6b5a5587002044cc8a46eb991110f26` |
| 信息输入 | Input Field | `836d5a56a46aacbb5736466a9ae81fa26977f3c8` |
| 主操作按钮 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| Home Indicator | home Indicator | `59ea6015ee3db5633c4739d786314a318dad6d35` |

> 完整 KYC 模块组件清单见 [`by-module/kyc.md`](../by-module/kyc.md)

## 3. Token

| 元素 | Token |
|------|-------|
| 页面背景 | `color/greyscale/surface` |
| 卡片背景 | `color/greyscale/white` |
| 步骤当前态 | `color/brand/primary` |
| 步骤未达态 | `color/greyscale/grey-2` |
| 拍照框边框 | `color/greyscale/dark-4` 虚线 |
| 提示文字 | `typography/caption/caption-1` + `color/greyscale/dark-3` |
| 主标题 | `typography/title/title-2` + `color/greyscale/dark-1` |

## 4. 待补充（TODO）

- [ ] 拍照页相机框尺寸 / 安全提示文字标准
- [ ] 信息确认页字段清单（姓名 / 身份证号 / 出生日期 / 地址）
- [ ] 错误态 UI（光线不足 / 模糊 / 反光）
- [ ] 各国 KYC 差异（ID/PH/MX 等的身份证类型）
- [ ] L2 实装截图与设计师对齐
