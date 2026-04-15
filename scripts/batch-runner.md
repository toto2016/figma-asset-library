# 批量执行指南

## 执行流程

### 阶段 A: 快速筛选（每文件 1 次 get_metadata 调用）

对每个文件调用 `get_metadata`，获取结构概览：

```
CallMcpTool: plugin-figma-figma / get_metadata
{
  "nodeId": "0:1",
  "fileKey": "FILE_KEY_HERE"
}
```

根据返回的 XML 判断文件是否有价值：
- 有 COMPONENT / COMPONENT_SET 节点 -> 值得深度提取
- 只有 FRAME 但数量多 -> 可能是设计稿，值得截图
- 节点数为 0 或全是 TEXT -> 可跳过

### 阶段 B: 深度提取（每文件 1 次 use_figma 调用）

对筛选出的文件执行深度提取：

```
CallMcpTool: plugin-figma-figma / use_figma
{
  "fileKey": "FILE_KEY_HERE",
  "code": "<extract-all-metadata.js 的内容>",
  "description": "Extract all metadata from FILE_NAME",
  "skillNames": "figma-use"
}
```

### 阶段 C: 关键截图（每节点 1 次 get_screenshot 调用）

对重要的组件和页面截图：

```
CallMcpTool: plugin-figma-figma / get_screenshot
{
  "nodeId": "NODE_ID_HERE",
  "fileKey": "FILE_KEY_HERE"
}
```

## 每日执行规范

1. 开始前检查当天已用调用数（心算或记录）
2. 每天最多使用 50 次调用（预留 150 次给其他需求）
3. 每次调用结果立即保存到本地 JSON
4. 更新 sources/*.json 中文件的 status 字段
5. 遇到失败立即停止，分析原因后再继续

## 结果保存格式

每个文件的提取结果保存为：
```
reports/extractions/
  {fileKey}.json          # 深度提取结果
  {fileKey}.lite.json     # 轻量扫描结果
```

## 进度跟踪

更新 `reports/extraction-log.json`：
```json
{
  "date": "2026-04-16",
  "project": "flow-library",
  "filesProcessed": 5,
  "callsUsed": 5,
  "results": [
    { "fileKey": "abc", "status": "success", "components": 12 },
    { "fileKey": "def", "status": "skipped", "reason": "empty file" }
  ]
}
```
