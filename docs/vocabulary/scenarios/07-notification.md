# 场景 07：Notification（通知中心）

> [词汇表](../../design-vocabulary.md) › Scenarios › Notification
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：notification
> **数据**：catalog 中 notification 模块 [76 个组件](../by-module/notification.md)

---

## 1. 典型页面 / 反馈

```
A. Notification Center        B. In-page Notice           C. Toast / Snack bar
   (通知列表，已读/未读)         (页内提示，可关闭)          (短暂浮层提示)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 顶部导航 | page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| 通知列表项 | Notification（10 变体） | `080ecfd53cbfdbe4f803e99b953655488b1062c5` |
| 内联通知 | Notice（Success/Error/Info/Warn） | `0d83c402b7480ad2a200c1f03ba687795bc68ca3` |
| 加载提示 | Loading | `65b5bcfce6673d1817b0806637f2cd5aa97ce153` |
| 全屏空态 | （手建 + 插画） | 见 [`by-type/image.md`](../by-type/image.md) |

## 3. Token

| 元素 | Token |
|------|-------|
| 列表背景 | `color/greyscale/white` |
| 未读底色 | `color/greyscale/light-2` |
| 已读底色 | `color/greyscale/white` |
| 标题 | `typography/body/body-2` Medium + `color/greyscale/dark-1` |
| 时间戳 | `typography/caption/caption-2` + `color/greyscale/dark-4` |
| 未读小红点 | `color/others/error` 4×4 圆点 |
| Success Notice | `color/others/success` 边框 + 文字 |
| Error Notice | `color/others/error` 边框 + 文字 |
| Warn Notice | `color/others/yellow` 边框 + 文字 |

## 4. 通知类型分组

| 类型 | 用途 | 视觉差异 |
|------|------|---------|
| System | 系统消息（账号、安全） | 默认配色 + 锁图标 |
| Promotion | 营销活动 | 品牌色 chip + 礼物图标 |
| Transaction | 交易通知 | 默认配色 + 钱包图标 |
| Reminder | 还款提醒 | 黄色 chip + 时钟图标 |

## 5. 待补充（TODO）

- [ ] 各类型通知图标 key 清单（需查 [`icons/`](../icons/README.md)）
- [ ] 列表为空的插画与文案
- [ ] 通知中心顶部"全部已读"按钮位置
- [ ] Push 通知（系统级）的 deeplink 跳转规则
- [ ] Toast 自动消失时长（3s / 5s）
