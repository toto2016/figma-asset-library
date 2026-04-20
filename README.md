# Atome UED Figma 素材库

从 Atome UED 团队 **4 个重点项目** 中系统化提取 UI 设计资产，
建立本地索引 + Figma 统一组件库，实现需求描述到自动出图。

> 经 UI 工程师 Fox Hu 确认，重点项目：Handover、DesignOps、Flow Library、Online Integration；
> 跳过：APB（含 KP 品牌复制内容，数据已全部删除）、Research & Exploration、Design QA。

## 快速开始

```bash
# 1. 配置 Figma Token
cp .env.example .env  # 编辑 .env 填入 PAT

# 2. 运行全流程
make all

# 3. 运行测试
make test
```

## 项目结构

```
figma-asset-library/
├── catalog/                        # 素材索引（产出数据）
│   ├── assets.json                 #   全量统一索引
│   ├── classified-index.json       #   分类索引摘要
│   ├── classified/                 #   多维分类索引
│   │   ├── by-type/                #     30 种 UI 类型
│   │   ├── by-module/              #     10 种业务模块
│   │   ├── by-platform/            #     4 种平台
│   │   └── by-system/              #     3 套设计体系
│   ├── component-descriptions.json #   248 个组件自然语言描述
│   ├── taxonomy.json               #   分类规则定义
│   ├── schema.json                 #   数据 Schema
│   └── tokens/                     #   Design Token
│       ├── design-tokens.json      #     原始格式
│       └── w3c-design-tokens.json  #     W3C 标准格式
│
├── scripts/                        # 自动化脚本
│   ├── lib/figma_api.py            #   API 通用模块（重试/缓存）
│   ├── discover-files.sh           #   REST API 文件发现
│   ├── scan-rest-api.sh            #   REST API 批量扫描
│   ├── deep-extract.sh             #   深度提取 Wave 1
│   ├── deep-extract-wave2.sh       #   深度提取 Wave 2
│   ├── fetch-components.sh         #   全量组件获取
│   ├── incremental-scan.sh         #   增量扫描
│   ├── download-screenshots.sh     #   截图下载
│   ├── build-index.js              #   统一索引构建
│   ├── build-classified-index.py   #   多维分类索引
│   ├── refine-classification.py    #   分类细化
│   ├── component-dedup.py          #   组件去重分析
│   ├── export-w3c-tokens.py        #   W3C Token 导出
│   ├── generate-descriptions.py    #   组件描述生成
│   └── legacy/                     #   已废弃脚本（留存参考）
│
├── reports/                        # 分析报告 + 提取数据
│   ├── operation-log.md            #   完整操作记录（核心文档）
│   ├── component-dedup-report.md   #   组件去重分析
│   ├── version-selection-plan.md   #   主版本选择方案
│   ├── variables-migration-plan.md #   Styles→Variables 迁移方案
│   ├── engineering-review-panel.md #   12 人工程评审
│   ├── uiux-feasibility-review.md  #   6 角色可行性评估
│   ├── full-scan-report.md         #   全量扫描报告
│   ├── tool-audit-report.md        #   MCP 工具审计
│   ├── phase5-auto-design-spec.md  #   Phase 5 自动出图规格
│   ├── scan-versions.json          #   增量扫描版本基线
│   └── extractions/                #   原始提取数据
│       ├── scans/                  #     项目级扫描结果
│       ├── components/             #     全量组件列表
│       └── deep/                   #     深度提取详情
│
├── sources/                        # 源文件清单（按项目分）
├── screenshots/                    # 组件截图（不提交 git）
├── tests/                          # 单元测试
│   └── test_core.py                #   22 cases
├── docs/                           # 参考文档
│
├── AGENTS.md                       # AI Agent 指引
├── Makefile                        # 一键编排（11 命令）
├── .env.example                    # 环境变量模板
└── .gitignore
```

## 执行阶段

| # | 阶段 | 状态 | 说明 |
|---|------|------|------|
| 1 | 本地准备 | ✅ | 目录/分类/脚本 |
| 2 | 权限测试 | ✅ | Organization Full seat, 200次/天 |
| 3 | 工具审计 | ✅ | 17 个 MCP 工具全量测试 |
| 4 | 全量扫描 | ✅ | 544/555 文件, 4348 组件, 163 Token |
| 5 | 深度提取 | ✅ | 12 个高价值文件完整属性 |
| 6 | 组件去重 | ✅ | 17 组跨体系重复，全部以 DesignOps 为主版本 |
| 7 | 分类索引 | ✅ | 30 种 UI 类型，72.3% 重新归类 |
| 8 | 主版本选择 | ✅ | DesignOps 为核心，APB 数据已删除 |
| 9 | Token 导出 | ✅ | W3C 标准格式 |
| 10 | Variables 方案 | ✅ | 三层架构，94 变量 |
| 11 | 增量扫描 | ✅ | 版本基线，持续同步 |
| 12 | 截图本地化 | ✅ | 组件截图下载 |
| 13 | 工程评审 | ✅ | 12 人评审，6.8/10 |
| 14 | **统一组件库** | ✅ | 34 组件集 / 160 变体 / 6 页面 |
| 15 | 补充扫描 | ✅ | Flow Library + Online Integration 全量扫描 |
| 16 | Phase 5 数据准备 | ✅ | 页面模板 + 组件共现 + 参考索引 |
| 17 | **自动出图 (L1)** | 🔜 | 需求描述 → 线框图 |
