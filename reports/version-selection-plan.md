# 重复组件主版本选择方案

> 更新时间: 2026-04-16
> 基于 3,200 个组件（DesignOps 1,588 + Handover 1,612）
> APB 数据已全部删除（含 KP 品牌复制内容，不可学习）

---

## 历史说明

原方案分析了 17 组跨体系重复，其中 16 组为 APB vs DesignOps。
APB 被确认含有 KP 品牌复制内容后，其 1,148 个组件全部删除。
这 16 组重复不再存在——DesignOps 版本直接作为唯一主版本。

---

## 当前跨体系重复

仅 1 组跨 DesignOps 和 Handover：

### Top Up（6 变体）

| 来源 | 变体数 | 说明 |
|------|--------|------|
| DesignOps Web | 4 | Design library - web / Key Pages |
| Handover Mobile | 2 | Screen library - mobile / Content Icon |

**建议**: DesignOps Web 为主版本（变体更多，结构更规范）。

---

## 体系内重复（DesignOps 跨文件）

以下 9 组在 DesignOps 内部的多个文件中出现：

| 组件 | 变体数 | 出现文件 | 建议主文件 |
|------|--------|---------|-----------|
| icon | 72 | Mobile + Merchant Centre | Icon Library |
| Button | 69 | Mobile + Web + Merchant Centre | Web（24 变体，语义命名最规范） |
| Avatar | 52 | Mobile + Web | Mobile（48 变体） |
| page-header | 17 | Web + Merchant Centre | Web |
| Checkbox | 11 | Mobile + Web | Web（8 变体） |
| Search Box | 6 | Web + Merchant Centre | Web |
| loader | 6 | Mobile + Merchant Centre | 待确认 |
| Switch | 5 | Web + Merchant Centre | Web |
| home Indicator | 4 | Mobile + Web | Mobile |

---

## 统一组件库架构

全部以 DesignOps 为核心来源：

| 分类 | 主要组件 | 来源 |
|------|---------|------|
| Controls | Button/Checkbox/Radio/Switch/SearchBox/Pagination/loader-wheel | DesignOps Web |
| Data Display | Avatar/Transaction Status | DesignOps |
| Brand Assets | Atome-Logo/Bank Logo/Wallet Logo/Country Flag/Indonesian KTP | DesignOps Web |
| Navigation | 132 个组件 | DesignOps 独有 |
| Icons | 415 个 | DesignOps 独有（Icon Library） |
| Page Templates | voucher/modal/card/input 等 | 参考 Handover Screen Library |

### 品牌色

- **Atome 品牌色是黄色**（DesignOps `brand/primary: #f0ff5f`）
- 之前从 APB 提取的绿色 `#00D26A` 是 KP 品牌色，已废弃
