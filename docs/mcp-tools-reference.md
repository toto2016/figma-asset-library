# Figma MCP 工具速查手册

MCP Server: `plugin-figma-figma`

---

## 读取类工具

### get_design_context

获取节点的设计上下文（代码 + 截图 + 元数据），首选工具。

```
参数:
  nodeId: "123:456"     # 节点 ID
  fileKey: "abc123"     # 文件 key
```

### get_metadata

获取节点结构概览（XML 格式），仅包含 ID、类型、名称、位置、尺寸。

```
参数:
  nodeId: "0:1"         # 页面 ID 通常是 "0:1"
  fileKey: "abc123"
```

### get_screenshot

获取节点截图。

```
参数:
  nodeId: "123:456"
  fileKey: "abc123"
```

### search_design_system

搜索已发布的设计系统资产（组件、变量、样式）。

```
参数:
  query: "button"              # 搜索关键词
  fileKey: "abc123"            # 文件 key（提供上下文）
  includeComponents: true
  includeVariables: true
  includeStyles: true
```

---

## 写入类工具

### use_figma

通过 Plugin API 执行 JavaScript，最强大的工具。

```
参数:
  fileKey: "abc123"
  code: "...JS 代码..."
  description: "操作描述"
  skillNames: "figma-use"      # 日志用途
```

关键规则：
- 用 `return` 返回数据
- 颜色 0-1 范围
- FILL/HUG 在 appendChild 之后设置
- 字体先 loadFontAsync
- 页面切换用 `await figma.setCurrentPageAsync(page)`

### generate_figma_design

将网页截图导入 Figma（免计费）。

```
参数:
  captureId: "..."             # 轮询用
  outputMode: "existingFile"   # newFile | existingFile | clipboard
  fileKey: "abc123"            # existingFile 模式需要
```

### create_new_file

创建新的 Figma 文件。

```
参数:
  fileName: "文件名"
  planKey: "team::xxx"         # 从 whoami 获取
  editorType: "design"         # design | figjam
```

---

## 辅助工具

### whoami

验证身份和权限（免计费）。无参数。

### generate_diagram

在 FigJam 中生成图表。

---

## 计费规则

| 工具 | 是否计费 |
|------|---------|
| whoami | 免费 |
| generate_figma_design | 免费 |
| add_code_connect_map | 免费 |
| 其余所有工具 | 计费 |

| 计划 | 席位 | 额度 |
|------|------|------|
| Starter | 任意 | 6 次/月 |
| Professional | Full/Dev | 200 次/天 |
| Organization | Full/Dev | 200 次/天 |
| Enterprise | Full/Dev | 600 次/天 |

失败的调用也会消耗额度。
