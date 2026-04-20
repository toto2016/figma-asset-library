# Atome 设计词汇表 (AI Design Vocabulary)

> 数据来源：DesignOps 提取 + Figma MCP 导入验证
> 更新时间：2026-04-15
> 用途：AI 出图时的组件与 Token 查找手册

---

## 1. Token 体系

### 1.1 颜色 Token（68 个）

#### 品牌色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/brand/primary` | `#f0ff5f` | 品牌主色（黄色） |
| `color/interaction/active-#` | `#f6ff7e` | 选中/激活态 |
| `color/interaction/pressed` | `#e3f90a` | 按压态 |
| `color/interaction/disabled` | `#e6e8f5` | 禁用态 |

#### 灰阶

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/greyscale/dark-1` | `#141c30` | 主文字 |
| `color/greyscale/dark-3` | `#3e4459` | 次要文字 |
| `color/greyscale/dark-4` | `#878d9c` | 辅助文字/图标 |
| `color/greyscale/grey-1` | `#b6b9cb` | 占位文字 |
| `color/greyscale/grey-2` | `#cfd2e3` | 边框 |
| `color/greyscale/light-1` | `#eaeaea` | 分割线 |
| `color/greyscale/light-2` | `#f7f8ff` | 浅底色 |
| `color/greyscale/surface` | `#f6f6f6` | 页面背景 |
| `color/greyscale/white` | `#ffffff` | 卡片背景 |

#### 功能色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/others/blue` | `#2247ff` | 链接/可交互文字 |
| `color/others/success` | `#25bc73` | 成功状态 |
| `color/others/error` | `#ed816e` | 错误状态 |
| `color/others/yellow` | `#f8c705` | 警告 |
| `color/others/pink` | `#ff3075` | 强调 |
| `color/others/dark-green` | `#089d4e` | 深绿 |
| `color/others/turquoise` | `#00f078` | 霓虹绿 |
| `color/error-pressed` | `#df6a56` | 错误按压态 |

#### 图表色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/charts/trust-1` | `#2247ff` | 图表蓝 1 |
| `color/charts/trust-2` | `#7092fe` | 图表蓝 2 |
| `color/charts/trust-3` | `#a2b7ff` | 图表蓝 3 |
| `color/charts/trust-4` | `#d1dbff` | 图表蓝 4 |
| `color/charts/passion-1` | `#ff5741` | 图表红 1 |
| `color/charts/passion-2` | `#ff9d8f` | 图表红 2 |
| `color/charts/passion-3` | `#ffbdb6` | 图表红 3 |
| `color/charts/passion-4` | `#ffdfdb` | 图表红 4 |

#### 补充色

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/complementary/light-blue` | `#60d2fa` | 补充浅蓝 |
| `color/complementary/dark-blue` | `#002a5e` | 补充深蓝 |
| `color/complementary/pink` | `#ff3075` | 补充粉 |
| `color/complementary/neon-green` | `#00f078` | 补充霓虹绿 |
| `color/complementary/lilac` | `#c6b2f3` | 补充淡紫 |

#### 遮罩

| Token 路径 | 值 | 用途 |
|-----------|-----|------|
| `color/overlay/light` | `#000000` (含透明度) | 浅色遮罩 |
| `color/overlay/dark` | `#000000` (含透明度) | 深色遮罩 |

### 1.2 字体 Token（28 个）

字体系列：**GT Walsheim Pro**

#### Mobile 字体

| Token 路径 | 字重 | 字号 | 用途 |
|-----------|------|------|------|
| `typography/title/large-title(24pt)` | Bold (700) | 24px | 大标题 |
| `typography/title/title-1(21pt)` | Bold (700) | 21px | 一级标题 |
| `typography/title/title-2(18pt)` | Bold (700) | 18px | 二级标题 |
| `typography/title/title-3(16pt)` | Bold (700) | 16px | 三级标题 |
| `typography/title/title-4(15pt)` | Bold (700) | 15px | 四级标题 |
| `typography/title/headline(14pt)` | Bold (700) | 14px | 小标题 |
| `typography/title/subhead(12pt)` | Bold (700) | 12px | 副标题 |
| `typography/body/body-1(16pt)` | Medium (500) | 16px | 正文 1 |
| `typography/body/body-2(15pt)` | Regular (400) | 15px | 正文 2 |
| `typography/body/body-3(14pt)` | Regular (400) | 14px | 正文 3 |
| `typography/button/button-1(16pt)` | Medium (500) | 16px | 按钮文字 1 |
| `typography/button/button-2(15pt)` | Bold (700) | 15px | 按钮文字 2 |
| `typography/caption/caption-1(13pt)` | Regular (400) | 13px | 说明文字 1 |
| `typography/caption/caption-2(12pt)` | Regular (400) | 12px | 说明文字 2 |
| `typography/caption/caption-3(10pt)` | Regular (400) | 10px | 说明文字 3 |

#### Desktop 字体

| Token 路径 | 字重 | 字号 |
|-----------|------|------|
| `typography/desktop/title/large-title-(38pt)` | Bold | 38px |
| `typography/desktop/title/title-1-(30pt)` | Bold | 30px |
| `typography/desktop/title/title-2-(24pt)` | Bold | 24px |
| `typography/desktop/title/title-3-(20pt)` | Bold | 20px |
| `typography/desktop/title/title-4-(18pt)` | Bold | 18px |
| `typography/desktop/title/title-5-(16pt)` | Bold | 16px |
| `typography/desktop/body/body-1-(18pt)` | Regular | 18px |
| `typography/desktop/body/body-2-(16pt)` | Regular | 16px |
| `typography/desktop/body/body-3-(14pt)` | Regular | 14px |
| `typography/desktop/button/button-1-(16pt)` | Bold | 16px |
| `typography/desktop/button/button-2-(14pt)` | Bold | 14px |
| `typography/desktop/caption/caption-1-(12pt)` | Regular | 12px |
| `typography/desktop/caption/caption-2-(10pt)` | Regular | 10px |

### 1.3 阴影 Token（3 个）

| Token 路径 | 用途 |
|-----------|------|
| `shadow/shadow-01-8%` | 卡片阴影（主要） |
| `shadow/shadow-02-4%` | 轻量阴影 |
| `shadow/screen` | 全屏遮罩阴影 |

### 1.4 固定规范

| 属性 | 值 | 来源 |
|------|-----|------|
| lineHeight | 150% | DesignOps 标准 |
| 卡片圆角 | 8px | DesignOps Button 组件 |
| 字体 | GT Walsheim Pro | DesignOps 全局字体 |
| 按钮组件内字体 | Plus Jakarta Sans Bold | Button (Web) 组件内置 |

---

## 2. 组件清单

### 2.1 基础交互组件（可导入 ✅）

| 组件名 | 来源库 | Component Key | 变体数 | 常用变体 |
|--------|--------|---------------|--------|---------|
| **Button** | Web | `0d1fe70a...` | 24 | `Type=Big, Class=Primary, Active=Yes` |
| **Checkbox** | Web | `526c219c...` | 8 | `Status=Selected, Active=Yes` |
| **Radio** | Web | `51952c25...` | 6 | `State=Selected, Active=Yes` |
| **Switch** | Web | `5edec187...` | 2 | `Selected=Yes` / `Selected=No` |
| **Tab** | Web | `1f033ed9...` | 2 | `Count=2 tab` |
| **Tag** | Web | `82ffa3b1...` | 2 | `On Color=yes` / `no` |
| **Selection** | Web | `25e52d4e...` | 2 | `Active=Yes` / `No` |
| **Quick Filter** | Web | `02559978...` | 4 | `Active=Yes, Counter=No` |
| **button** (Mobile) | Mobile | `d45ef476...` | 12 | `Property 1=basic, Property 2=normal` |
| **checkbox** (Mobile) | Mobile | `5a8cdf68...` | 3 | `status=selected` |
| **button** (MC) | MC | `d935a6e9...` | 30+ | `Size=medium, Type=primary, State=normal` |
| **checkbox** (MC) | MC | `480f377e...` | 4 | `Check=true, Disabled=false` |

### 2.2 输入组件（可导入 ✅）

| 组件名 | 来源库 | Component Key | 变体数 | 常用变体 |
|--------|--------|---------------|--------|---------|
| **Input Field** | Web | `836d5a56...` | 12 | `Type=Default` / `Typing` / `Error` |
| **Input Area** | Web | `3c4012a4...` | 6 | `Type=Default` / `Filled` |
| **Input Amount** | Web | `615e8217...` | 8 | `Type=eWallet` |
| **Search Box** | Web | `0452d409...` | 4 | `State=Active` |
| **Input OTP** | Web | `792a7297...` | 6 | OTP 输入框 |
| **Input Phone Number** | Web | `679244e3...` | 1 | 电话号码输入 |

### 2.3 导航组件（可导入 ✅）

| 组件名 | 来源库 | Component Key | 变体数 | 常用变体 |
|--------|--------|---------------|--------|---------|
| **page-header** | Web | `977c681d...` | 12 | `Type=with Icons, On Color=Yes` |
| **Bottom Navigation** | Web | `97a2cdbd...` | 3 | `Navigation=Home` |
| **Status bar** | Web | `220e8779...` | 2 | `Size=Dark` / `Light` |
| **home Indicator** | Web | `59ea6015...` | 2 | `On Color=No` |
| **Stepper** | Web | `abc39b5a...` | 2 | 步骤指示器 |
| **Pagination** | Web | `0c1f79ff...` | 3 | `State=First` / `Second` |

### 2.4 反馈组件（可导入 ✅）

| 组件名 | 来源库 | Component Key | 变体数 | 常用变体 |
|--------|--------|---------------|--------|---------|
| **Notice** | Web | `0d83c402...` | 4 | `Type=Success` / `Error` |
| **Notification** | Web | `080ecfd5...` | 10 | 通知列表 |
| **Loading** | Web | `65b5bcfc...` | 1 | 加载动画 |
| **Loading Toast** | Web | `61857fc2...` | 1 | 加载提示 |
| **Message Container** | Web | `57fa4025...` | 4 | 消息容器 |
| **Progress Bar** | Web | `9a985202...` | 1 | 进度条 |

### 2.5 容器组件（可导入 ✅）

| 组件名 | 来源库 | Component Key | 变体数 | 常用变体 |
|--------|--------|---------------|--------|---------|
| **Bottom Sheet** | Web | `7f1b2375...` | 1 | 底部弹窗 |
| **Action Sheet** | Web | `669aafcd...` | 1 | 操作选项 |
| **Consent** | Web | `bdf173da...` | 1 | 协议同意 |
| **Keyboard** | Web | `65e5abc1...` | 2 | `Type=Number` |

### 2.6 品牌组件（可导入 ✅）

| 组件名 | 来源库 | Component Key | 变体数 | 常用变体 |
|--------|--------|---------------|--------|---------|
| **Atome-Logo** | Web | `0df8fd9f...` | 8 | `Color=Brand` / `White` / `Black` |
| **Atome-Logo Compact** | Web | `0d6971c0...` | 8 | `Color=Brand, Plus=No` |
| **Avatar** | Web | `1da2e978...` | 4 | `Type=Merchant logo` |
| **Bank Logo** | Web | `4cea9627...` | 6 | `Bank=BCA` / `BNI` 等 |
| **Wallet Logo** | Web | `2480a879...` | 7 | `Bank=OVO` 等 |
| **Counter** | Web | `d109459a...` | 1 | 数字角标 |

### 2.7 图标（可导入 ✅，66 个）

常用图标一览：

| 图标名 | Key 前缀 | 尺寸 |
|--------|----------|------|
| `icon.check` | `520c6af7...` | 24×24 |
| `icon.close` | `0c9370f3...` | 24×24 |
| `icon.lock` | `7279c238...` | 24×24 |
| `icon.search` | `4931125e...` | 24×24 |
| `icon.arrow-left` | `f6da59d1...` | 24×24 |
| `icon.arrow-right` | `ee63714f...` | 24×24 |
| `icon.caret-down` | `3b43bd21...` | 24×24 |
| `icon.caret-up` | `8ace2a1b...` | 24×24 |
| `icon.heart-filled` | `aadb289d...` | 24×24 |
| `icon.home` | `dcc0ca4c...` | 24×24 |
| `icon.profile` | `912a34e3...` | 24×24 |
| `icon.settings` | `7f8a5d33...` | 24×24 |
| `icon.wallet` | `291fc76d...` | 24×24 |
| `icon.creditcard` | `55a91e8c...` | 24×24 |
| `icon.secure` | `14342de4...` | 24×24 |
| `icon.info` | `bb61f987...` | 24×24 |
| `icon.copy` | `6820d6b3...` | 24×24 |
| `icon.download` | `e2e8b06b...` | 24×24 |
| `icon.share` | `b361c748...` | 24×24 |
| `icon.trash` | `a30d37e8...` | 24×24 |

### 2.8 不可导入组件（Mobile 库，5 个）

| 组件名 | 原因 | 替代方案 |
|--------|------|---------|
| Navigation Bars (Mobile) | 未发布到团队库 | 用 Web 库 `page-header` |
| Tab Bars (Mobile) | 未发布到团队库 | 用 Web 库 `Tab` |
| Input (Mobile) | 未发布到团队库 | 用 Web 库 `Input Field` |
| toast (Mobile) | 未发布到团队库 | 用 Web 库 `Notice` |
| snack bar (Mobile) | 未发布到团队库 | 用 Web 库 `Message Container` |

---

## 3. 业务场景 → 组件 + Token 映射

### 3.1 Merchant Checkout 页面

| 页面元素 | 组件 | Token |
|---------|------|-------|
| 状态栏 | `Status bar (Dark)` | — |
| 导航栏 | `page-header (with Icons)` | `typography/title/title-3` |
| 关闭按钮 | `icon.close` | `color/greyscale/dark-1` |
| 返回箭头 | `icon.arrow-left` | `color/greyscale/dark-1` |
| 订单卡片背景 | 手建 Frame | `color/greyscale/white` + `shadow/shadow-01-8%` |
| 商户名称 | 文本 | `typography/title/title-3` + `color/greyscale/dark-1` |
| 订单编号 | 文本 | `typography/caption/caption-1` + `color/greyscale/dark-4` |
| 商品图片占位 | 手建 Frame | `color/greyscale/surface` + 圆角 4px |
| 商品名称 | 文本 | `typography/body/body-2` + `color/greyscale/dark-1` |
| 商品数量 | 文本 | `typography/caption/caption-1` + `color/greyscale/dark-4` |
| 价格 | 文本（右对齐） | `typography/body/body-1` + `color/greyscale/dark-1` |
| 分期选项卡 | `Selection` 或手建 | `color/brand/primary` (选中底色) |
| 分期选中高亮 | 手建 Frame | `color/brand/primary` 底色 |
| 分期金额 | 文本 | `typography/title/title-2` + `color/greyscale/dark-1` |
| "0% interest" | 文本 | `typography/caption/caption-1` + `color/others/success` |
| 付款方式卡片 | 手建 Frame | `color/greyscale/white` + `shadow/shadow-01-8%` |
| 银行 Logo | `Bank Logo` | — |
| "Change" 链接 | 文本 | `typography/body/body-3` + `color/others/blue` |
| 协议勾选 | `Checkbox (Selected)` | — |
| 协议文本 | 文本 | `typography/caption/caption-1` + `color/greyscale/dark-3` |
| 确认按钮 | `Button (Big Primary)` | 内置品牌色 |
| Atome Logo | `Atome-Logo Compact (Brand)` | — |
| 安全提示 | 文本 | `typography/caption/caption-3` + `color/greyscale/dark-4` |
| Home Indicator | `home Indicator` | — |

---

## 4. AI 出图规则

### 4.1 组件选择优先级

1. **优先使用 DesignOps 已发布组件**（通过 `importComponentByKeyAsync`）
2. **同类组件优先 Web 库**（Mobile 库有 5 个未发布）
3. **无对应组件时用 Token 手建**，严格遵循 Token 值
4. **禁止使用硬编码颜色**，所有颜色必须对应 Token

### 4.2 文本样式规则

| 场景 | Token | GT Walsheim Pro Style |
|------|-------|----------------------|
| 页面标题 | `title/title-3(16pt)` | Bold |
| 卡片标题 | `title/title-3(16pt)` | Medium（非 Bold） |
| 正文 | `body/body-2(15pt)` | Regular |
| 辅助文字 | `caption/caption-1(13pt)` | Regular |
| 小标签 | `caption/caption-3(10pt)` | Regular |
| 按钮文字 | `button/button-1(16pt)` | Medium |

### 4.3 颜色使用规则

| 场景 | Token |
|------|-------|
| 品牌主色/选中态背景 | `color/brand/primary` (#f0ff5f) |
| 主文字 | `color/greyscale/dark-1` (#141c30) |
| 次要文字 | `color/greyscale/dark-3` (#3e4459) |
| 辅助文字/图标 | `color/greyscale/dark-4` (#878d9c) |
| 可点击文字 | `color/others/blue` (#2247ff) |
| 成功状态 | `color/others/success` (#25bc73) |
| 错误状态 | `color/others/error` (#ed816e) |
| 页面背景 | `color/greyscale/surface` (#f6f6f6) |
| 卡片背景 | `color/greyscale/white` (#ffffff) |
| 分割线 | `color/greyscale/light-1` (#eaeaea) |
| 按钮禁用 | `color/interaction/disabled` (#e6e8f5) |

### 4.4 间距规范（从组件推断）

| 场景 | 值 |
|------|-----|
| 页面水平 padding | 20px |
| 卡片内 padding | 16px |
| 卡片间距 | 12px |
| 元素行间距 | 8px |
| 紧凑行间距 | 4px |
| 卡片圆角 | 8px |
| 小元素圆角 | 4px |
