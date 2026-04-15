# Atome UED Figma 素材库

从 Atome UED 团队 12 个项目（~914 个文件）中系统化提取 UI 设计资产，
建立本地索引 + Figma 统一组件库，实现需求描述到自动出图。

## 快速开始

1. 用 Cursor 打开此项目：`cursor /Users/toto/projects/figma-asset-library`
2. 确认 Figma MCP Server 已连接
3. 按 Phase 顺序执行

## 项目结构

```
figma-asset-library/
  AGENTS.md                  # AI Agent 指引（关键配置和规范）
  taxonomy.json              # 分类维度定义
  sources/                   # 源文件清单（按项目）
  catalog/                   # 素材索引
    assets.json              # 全量索引
    by-country/              # 按国家线
    by-module/               # 按功能模块
    by-business/             # 按业务线
    by-flow/                 # 按业务流程
    by-project/              # 按源项目
  screenshots/               # 截图资产（不提交 git）
  scripts/                   # MCP 脚本
  reports/                   # 执行日志
  .cursor/rules/             # 项目级 Cursor 规则
```

## 执行阶段

| 阶段 | 状态 | 说明 |
|------|------|------|
| Phase 0: 本地准备 | 已完成 | 目录/分类/脚本 |
| Pilot: 权限测试 | 等待审批 | Professional Full seat |
| Wave 1: P0 项目 | 待开始 | Flow Library + DesignOps |
| Wave 2: P1 项目 | 待开始 | UI Sandbox + APS |
| Wave 3: P2-P3 项目 | 待开始 | 剩余项目 |
| Phase 3: 索引构建 | 待开始 | 本地多维度索引 |
| Phase 4: 组件库 | 待开始 | Figma 统一组件库 |
| Phase 5: 自动出图 | 待开始 | 需求描述 -> 设计图 |

## 数据源

| 项目 | 文件数 | 优先级 |
|------|-------|--------|
| Flow Library # 流程库 | 31 | P0 |
| DesignOps # 提效工具 | 95 | P0 |
| UI Sandbox # UI验配蓝田 | 245 | P1 |
| APS | 54 | P1 |
| Online Integration | 72 | P2 |
| Handover # 里程交通+归档 | 53 | P2 |
| 其余 5 个项目 | 361 | P3 |
| **Atome AI Test** | **3** | **测试区** |
