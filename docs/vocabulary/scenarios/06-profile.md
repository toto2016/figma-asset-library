# 场景 06：Profile（个人中心）

> [词汇表](../../design-vocabulary.md) › Scenarios › Profile
>
> **状态**：🟡 骨架（待补全）
> **平台**：Mobile
> **业务模块**：profile
> **数据**：catalog 中 profile 模块 [89 个组件](../by-module/profile.md)

---

## 1. 典型页面

```
A. Profile Home    →  B. Edit Profile     →  C. Settings
   (头像 + 菜单)        (字段编辑)             (开关 + 链接)
```

## 2. 必备组件（Component Key）

| 元素 | 组件名 | Component Key |
|------|--------|---------------|
| 状态栏 | Status bar (Dark) | `220e8779ee816360537d27c7004b356fca44d134` |
| 顶部导航 | page-header (with Icons) | `977c681d719594eb21f752d1f85b7f78c0c05472` |
| 用户头像 | Avatar | `1da2e978cc392829adfe16315fdffa110a0347ad` |
| 列表项箭头 | icon.caret-down | `3b43bd215dbc0464b755ccf5dd832a40c7c220cb` |
| 设置开关 | Switch | `5edec1871b25e1772e77ded460eec3a51a57a20a` |
| 字段输入 | Input Field | `836d5a56a46aacbb5736466a9ae81fa26977f3c8` |
| 保存按钮 | Button (Big Primary) | `0d1fe70a11b79de2ab7e6bd1704634d60527314f` |
| 底部导航 | Bottom Navigation | `97a2cdbd49aba76abf260aedc9403293554e54f4` |
| Home Indicator | home Indicator | `59ea6015ee3db5633c4739d786314a318dad6d35` |

## 3. Token

| 元素 | Token |
|------|-------|
| 头像区背景 | `color/brand/primary` 或 `color/greyscale/white` |
| 用户名 | `typography/title/title-2` + `color/greyscale/dark-1` |
| 用户 ID/手机 | `typography/caption/caption-1` + `color/greyscale/dark-4` |
| 列表项标题 | `typography/body/body-2` + `color/greyscale/dark-1` |
| 列表项右值 | `typography/body/body-3` + `color/greyscale/dark-3` |
| 分割线 | `color/greyscale/light-1` |
| Logout 按钮 | `color/others/error` 边框/文字 |

## 4. 待补充（TODO）

- [ ] 头像上传 UI（点击头像后的相机/相册选择）
- [ ] 各模块菜单项清单（My Vouchers / Notifications / Help / About / Logout）
- [ ] 编辑模式的字段校验提示
- [ ] 关联账户（Apple ID / Google）的 UI
- [ ] 注销账户的多步确认流程
