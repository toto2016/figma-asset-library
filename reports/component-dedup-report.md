# 组件去重分析报告

> 生成时间: 2026-04-16（APB 数据已于 2026-04-16 全部清除）
> 总组件数: 3200（DesignOps: 1588 + Handover: 1612）
> 组件集(ComponentSet): 226

---

## 一、各体系概览

| 体系 | 组件集 | 变体总数 | 独立组件 | 合计 | 文件数 |
|------|--------|---------|---------|------|--------|
| DesignOps | 207 | 1273 | 315 | 1588 | 4 |
| Handover | 19 | 41 | 1571 | 1612 | 3 |

> APB（1148 组件）已全部删除，原因：APB 中 PJP 设计师复制了 KP（另一品牌）的内容，
> 品牌色和风格与 Atome 不符，数据不可学习。

---

## 二、跨体系重复组件

APB 移除后，原 17 组跨体系重复中仅保留 DesignOps 与 Handover 之间的重复：

### 1. `Top Up` (other) — 6 变体

跨越: DesignOps, Handover

| 体系 | 文件 | 页面 | 变体数 | 示例 |
|------|------|------|--------|------|
| DesignOps | Design library - web | Key Pages | 2 | Section=No, Section=Yes |
| DesignOps | Design library - web | Key Pages | 2 | Section=No, Section=Yes |
| Handover | Screen library - mobile | Content Icon | 2 | Active=Yes, Active=No |

> 其余 16 组原为 APB vs DesignOps 的重复，APB 删除后不再存在重复问题，
> DesignOps 版本直接作为唯一主版本。

---

## 三、体系内跨文件重复

- **icon** (DesignOps) — 72 变体, 出现在: Design library - Mobile, Merchant Centre Library
- **Button** (DesignOps) — 69 变体, 出现在: Design library - Mobile, Design library - web, Merchant Centre Library
- **Avatar** (DesignOps) — 52 变体, 出现在: Design library - Mobile, Design library - web
- **page-header** (DesignOps) — 17 变体, 出现在: Design library - web, Merchant Centre Library
- **Checkbox** (DesignOps) — 11 变体, 出现在: Design library - Mobile, Design library - web
- **Search Box** (DesignOps) — 6 变体, 出现在: Design library - web, Merchant Centre Library
- **loader** (DesignOps) — 6 变体, 出现在: Design library - Mobile, Merchant Centre Library
- **Switch** (DesignOps) — 5 变体, 出现在: Design library - web, Merchant Centre Library
- **home Indicator** (DesignOps) — 4 变体, 出现在: Design library - Mobile, Design library - web

---

## 四、分类分布矩阵

| 分类 | 总计 | DesignOps | Handover |
|------|------|-----------|----------|
| other | 1636 | 497 | 1139 |
| icon | 422 | 415 | 7 |
| navigation | 151 | 132 | 19 |
| input | 145 | 97 | 48 |
| voucher | 118 | 2 | 116 |
| button | 92 | 73 | 19 |
| image | 77 | 75 | 2 |
| card | 69 | 5 | 64 |
| modal | 69 | 3 | 66 |
| list | 67 | 35 | 32 |
| form | 67 | 49 | 18 |
| toggle | 45 | 43 | 2 |
| loading | 39 | 1 | 38 |
| avatar | 52 | 52 | 0 |
| badge | 35 | 31 | 4 |
| toast | 36 | 19 | 17 |
| divider | 26 | 15 | 11 |
| tooltip | 9 | 3 | 6 |
| flag | 3 | 2 | 1 |
| progress | 3 | 1 | 2 |

---

## 五、去重建议

1. **跨体系重复已大幅减少**——APB 删除后仅 1 组（Top Up）
2. **体系内重复**通常是 Mobile/Web 两端的同名组件，需确认是否为同一设计意图的不同平台实现
3. **Handover 项目**中 1,139 个 "other" 类为页面级设计稿/插图；但剩余 473 个组件
   覆盖 voucher(116)、modal(66)、card(64)、input(48) 等明确 UI 类型，
   代表**实际交付开发的设计规范**，应纳入参考
4. 统一库以 **DesignOps 为核心** + Handover 的 Screen Library 验证实际落地模式
