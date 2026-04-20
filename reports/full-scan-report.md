# Figma 全量扫描报告

> 生成时间: 2026-04-15
> 范围: Atome UED 12 个项目, 555 个文件
>
> **⚠️ 注意**: APB 项目数据已于 2026-04-16 全部删除（含 KP 品牌复制内容）。
> 本报告为历史扫描记录，APB 相关数据不再有效。

## 扫描概览

| 指标 | 数值 |
|------|------|
| 项目总数 | 12 |
| 文件总数 | 555 |
| 扫描成功 | 544 (98%) |
| 扫描失败 | 11 (超时/权限) |
| 已发布组件 | 4,351 |
| 已发布样式 | 111 |
| 高价值文件 | 14 |
| 深度提取完成 | 12 |
| 核心截图完成 | 21 张 |
| Design Token | 163 (100 颜色 + 58 字体 + 5 效果) |

## 项目分布

| 项目 | 文件 | 成功 | 组件 | 样式 | 高价值 |
|------|------|------|------|------|--------|
| APB | 33 | 31 | 1,682 | 43 | 5 |
| DesignOps | 16 | 16 | 1,145 | 68 | 4 |
| Handover | 33 | 31 | 1,504 | 0 | 3 |
| Flow Library | 31 | 31 | 19 | 0 | 1 |
| UX Sandbox | 182 | 179 | 1 | 0 | 1 |
| Design QA | 20 | 20 | 0 | 0 | 0 |
| Misc | 41 | 39 | 0 | 0 | 0 |
| Online Integration | 21 | 21 | 0 | 0 | 0 |
| Research | 174 | 172 | 0 | 0 | 0 |
| Product 101 | 4 | 4 | 0 | 0 | 0 |

## 高价值文件 Top 10

| 文件 | 项目 | 组件 | 样式 | 深度提取 |
|------|------|------|------|----------|
| Screen library - mobile app | Handover | 1,477 | 0 | ✅ 完成 |
| [Content] Mobile | APB | 778 | 0 | ✅ 完成 |
| Design library - Mobile | DesignOps | 541 | 39 | ✅ 完成 |
| [Design System] Mobile 2.0 | APB | 508 | 22 | ✅ 完成 |
| Merchant Centre Library | DesignOps | 367 | 29 | ✅ 完成 |
| [Design System] Web | APB | 217 | 20 | ✅ 完成 |
| open-peeps (library) | DesignOps | 172 | 0 | ✅ 完成 |
| [Asset] Illustration | APB | 116 | 1 | ✅ 完成 |
| Gesture Icons (library) | DesignOps | 65 | 0 | ✅ 完成 |
| [Content] Web | APB | 63 | 0 | ✅ 完成 |
| Screen library - web | Handover | 25 | 0 | ✅ 完成 |

## 关键发现

### 组件集中度极高

4,351 个组件集中在 3 个项目:
- **APB**: 1,682 (39%) — 另一个产品线的完整设计系统
- **Handover**: 1,504 (35%) — 以 Screen library 为主的 UI 截屏库
- **DesignOps**: 1,145 (26%) — 核心组件库 + 商户端组件库

其余 9 个项目合计仅 20 个组件。

### 样式集中度

111 个已发布样式集中在:
- DesignOps: 68 (61%) — 核心颜色 + 字体 + 效果
- APB: 43 (39%) — Web + Mobile 独立样式体系

### 大量非设计资产文件

555 个文件中仅 14 个有已发布组件/样式 (2.5%)。其余 97.5% 为:
- 竞品分析、调研文档 (Research: 174 文件)
- UX 讨论和存档 (UX Sandbox: 182 文件)
- Dev handoff 交接文档 (Handover: 33 文件)
- 设计走查记录 (Design QA: 20 文件)

### Design Token 现状

5 个已深度提取的文件中, **变量数量为 0**。这意味着:
- 团队尚未使用 Figma Variables 管理 Design Token
- 颜色和字体仍以传统 Styles 方式管理
- 存在向 Variables 迁移的机会

## 截图资产

14 张核心组件截图已获取:

### Design Library Mobile (7 张)
- Buttons — 主按钮/次按钮/文字按钮/加载态
- Controls — Checkbox/Switch/Camera/Timeline/Tag/Toast
- Input — 输入框全状态 (enabled/disabled/focused/error)
- Typography — 完整字体层级 (Large title → Caption 3)
- Colors — Brand/Interaction/Grayscale/Message/Overlay
- Popup — 弹窗组件系列
- Icons — 主图标库 + 状态图标 + 安全图标

### Merchant Centre Library (7 张)
- Button — Primary/Secondary/Link/Dangerous/Dropdown × 状态矩阵
- Form & Input — Input/Password/SearchBox/RadioGroup/CheckboxTree
- Table — Column 类型 + Cell 类型 + Header
- Navigation — 菜单/子菜单/Tabs
- Charts — 饼图/环形图/柱状图/折线图
- Colors — 完整色板含 Charts 专用色
- Typography — Mobile + Desktop 对照字体层级

## 资源消耗

| 类型 | 数量 | 备注 |
|------|------|------|
| MCP 计费调用 | 32 | 含 Pilot + 审计 + 截图 |
| MCP 免费调用 | 3 | whoami + add_code_connect_map + generate_figma_design |
| REST API 调用 | ~1,650 | 555 文件 × 3 调用 (不计费) |
| 深度 REST 调用 | ~25 | 5 个高价值文件 (不计费) |
| MCP 剩余 | 168 / 200 | 当日额度 |

## 下一步建议

### 立即可做 (REST API, 零 MCP 消耗)
1. **APB 项目深度提取** — 5 个高价值文件, 2,364 组件, 43 样式
2. **Handover Screen Library 深度提取** — 1,477 组件的完整 UI 截屏库

### 需要 MCP 配额
3. **APB 核心组件截图** — 预计 10-15 次调用
4. **新发现高价值文件截图** — 预计 5-10 次调用

### 战略性工作
5. **Design Token 标准化** — 将 Styles 转换为 Variables/Token
6. **组件去重** — DesignOps vs APB 存在大量重叠组件
7. **自动化定期扫描** — 基于 lastModified 的增量更新
