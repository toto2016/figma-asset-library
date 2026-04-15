# 源文件清单

每个项目一个 JSON 文件，记录该项目下所有 Figma 文件的 fileKey 和名称。

## 如何填充

1. 在 Figma 中打开对应项目
2. 逐个文件右键 -> Copy link
3. 从 URL 中提取 fileKey（`figma.com/design/:fileKey/:fileName` 中的 `:fileKey` 部分）
4. 填入对应的 JSON 文件

## 文件格式

```json
{
  "project": "flow-library",
  "projectUrl": "https://www.figma.com/files/...",
  "files": [
    {
      "name": "文件名称",
      "fileKey": "abc123def456",
      "url": "https://www.figma.com/design/abc123def456/文件名称",
      "tags": ["ID", "kyc"],
      "status": "pending"
    }
  ]
}
```

status 取值: pending(待提取) | scanned(已快速扫描) | extracted(已深度提取) | skipped(跳过)
