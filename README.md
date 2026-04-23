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

## 在线文档

| 文档 | 说明 |
|------|------|
| [设计词汇表 v1.0（飞书）](https://advancegroup.sg.larksuite.com/wiki/C3KhwG7JYiHWaHkVVpFlKV4xg8f) | 仓库内 16 份语义层文档的在线镜像，含 Token 体系 + 10 个业务场景映射，供设计师集中验收 |

> 飞书文档为仓库 `docs/` 目录的镜像，真源以仓库为准。

## 项目结构

```
figma-asset-library/
├── catalog/                        # 素材索引（产出数据）
│   ├── assets.json                 #   全量统一索引（3,200 组件）
│   ├── vocabulary-data.json        #   机器层词汇数据（488KB）
│   ├── classified/                 #   多维分类索引
│   │   ├── by-type/                #     30 种 UI 类型
│   │   ├── by-module/              #     10 种业务模块
│   │   ├── by-platform/            #     4 种平台
│   │   ├── by-system/              #     设计体系归属
│   │   └── by-type-platform/       #     类型×平台交叉
│   ├── component-descriptions.json #   248 个组件自然语言描述
│   ├── component-co-occurrence.json#   组件共现关系
│   ├── page-templates.json         #   页面模板索引
│   ├── taxonomy.json               #   分类规则定义
│   ├── schema.json                 #   数据 Schema
│   └── tokens/                     #   Design Token
│       ├── design-tokens.json      #     原始格式
│       └── w3c-design-tokens.json  #     W3C 标准格式
│
├── docs/                           # 设计词汇表 + 参考文档
│   ├── design-vocabulary.md        #   词汇表总入口（三层架构导航）
│   └── vocabulary/                 #   语义层子文档（57 份）
│       ├── tokens/                 #     colors / typography / shadows / conventions
│       ├── scenarios/              #     10 个业务场景（含 Merchant Checkout L2 实装）
│       ├── by-type/                #     按 UI 类型（22 种）
│       ├── by-module/              #     按业务模块（10 个）
│       └── icons/                  #     图标字典（按字母分页）
│
├── scripts/                        # 自动化脚本
│   ├── lib/figma_api.py            #   API 通用模块（重试/缓存）
│   ├── vocab/                      #   词汇表生成器
│   ├── build-index.js              #   统一索引构建
│   ├── build-classified-index.py   #   多维分类索引
│   ├── build-vocabulary.js         #   词汇表双层构建
│   ├── component-dedup.py          #   组件去重分析
│   ├── refine-classification.py    #   分类细化
│   ├── export-w3c-tokens.py        #   W3C Token 导出
│   ├── generate-descriptions.py    #   组件描述生成
│   ├── scan-rest-api.sh            #   REST API 批量扫描
│   ├── incremental-scan.sh         #   增量扫描
│   └── download-screenshots.sh     #   截图下载
│
├── reports/                        # 分析报告 + 提取数据
│   ├── operation-log.md            #   完整操作记录（核心文档，2000+ 行）
│   ├── extractions/                #   原始提取数据（scans / components / deep）
│   └── *.md / *.json               #   去重、评审、可行性、迁移方案等
│
├── sources/                        # Figma 源文件清单（按项目分）
├── screenshots/                    # 组件截图（.gitignore，通过 make screenshots 下载）
├── tests/                          # 单元测试（22 cases）
│
├── AGENTS.md                       # AI Agent 指引
├── Makefile                        # 一键编排（make all / scan / test）
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
