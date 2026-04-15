# Figma Asset Library - AI Agent 指引

## 项目概述

Atome UED 团队的 Figma 全量素材库建设项目。从 12 个 Figma 项目（~914 个文件）中
系统化提取 UI 设计资产，建立本地索引 + Figma 统一组件库，实现需求描述到自动出图。

## 关键配置

- **Figma MCP Server**: `plugin-figma-figma`（不是 `user-figma`）
- **用户**: 甄晓龙 (xiaolong.zhen@advancegroup.com)
- **组织**: Neuroncredit Pte Ltd（View 权限）
- **团队**: Atome UED
- **测试项目**: Atome AI Test
- **个人 planKey**: `team::1109442467248292453`
- **组织 key**: `organization::1001709743790382367`
- **POC 文件 fileKey**: `7bnSNqge0DPalc6hJ0XF5U`

## MCP 调用规范

- Starter 计划仅 6 次/月，Professional Full seat 审批中
- Professional 升级后 200 次/天，10 次/分钟
- `whoami`、`generate_figma_design`、`add_code_connect_map` 免计费
- **失败的调用也计次**，脚本必须先验证逻辑
- 一次 `use_figma` 尽量多做事，但不要超复杂导致出错

## Figma API 常见陷阱

- 颜色值用 0-1 范围（不是 0-255）
- `counterAxisAlignItems` 不支持 `STRETCH`，只有 MIN/MAX/CENTER/BASELINE
- `layoutSizingHorizontal/Vertical = 'FILL'` 必须在 `appendChild` 之后设置
- 字体必须先 `loadFontAsync`，Inter 的 Semi Bold 中间有空格：`'Semi Bold'`
- 每次 `use_figma` 调用后页面上下文重置到第一页
- `figma.notify()` 会抛异常，禁止使用
- `figma.currentPage = page` 不支持，必须用 `await figma.setCurrentPageAsync(page)`
- 用 `return` 返回数据，`console.log` 不会返回任何内容

## 语言

- 始终使用中文回复
- 代码注释使用中文
- 文件名和变量名使用英文
