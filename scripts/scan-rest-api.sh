#!/bin/bash
# Figma REST API 批量文件扫描
# 用法: FIGMA_TOKEN=xxx bash scripts/scan-rest-api.sh sources/flow-library.json
#
# 为每个文件提取：文件结构 + 已发布组件 + 已发布样式
# 输出保存到 reports/extractions/scans/

set -e

if [ -z "$FIGMA_TOKEN" ]; then
  echo "❌ 请设置 FIGMA_TOKEN"
  exit 1
fi

SOURCE_FILE="${1:?用法: bash scripts/scan-rest-api.sh sources/<project>.json}"
OUTPUT_DIR="reports/extractions/scans"
mkdir -p "$OUTPUT_DIR"

python3 - "$SOURCE_FILE" "$OUTPUT_DIR" << 'PYEOF'
import json, subprocess, os, sys, time

token = os.environ["FIGMA_TOKEN"]
source_file = sys.argv[1]
output_dir = sys.argv[2]

with open(source_file) as f:
    source = json.load(f)

project_name = source["projectName"]
files = source["files"]
print(f"🔍 扫描项目: {project_name} ({len(files)} 个文件)")
print(f"   输出目录: {output_dir}/")
print()

results = []
errors = []

for i, file_info in enumerate(files):
    fkey = file_info["fileKey"]
    fname = file_info["name"]
    print(f"  [{i+1}/{len(files)}] {fname} ({fkey})")

    try:
        # 获取文件结构（depth=2 足够看到页面下的顶层节点）
        r = subprocess.run(
            ["curl", "-sf", "-H", f"X-Figma-Token: {token}",
             f"https://api.figma.com/v1/files/{fkey}?depth=2"],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode != 0:
            print(f"    ⚠️  文件结构获取失败")
            errors.append({"file": fname, "key": fkey, "error": "structure_fetch_failed"})
            time.sleep(1)
            continue

        file_data = json.loads(r.stdout)
        doc = file_data.get("document", {})
        pages = doc.get("children", [])

        # 获取已发布组件
        r2 = subprocess.run(
            ["curl", "-sf", "-H", f"X-Figma-Token: {token}",
             f"https://api.figma.com/v1/files/{fkey}/components"],
            capture_output=True, text=True, timeout=30
        )
        comp_data = json.loads(r2.stdout) if r2.returncode == 0 else {}
        components = comp_data.get("meta", {}).get("components", [])

        # 获取已发布样式
        r3 = subprocess.run(
            ["curl", "-sf", "-H", f"X-Figma-Token: {token}",
             f"https://api.figma.com/v1/files/{fkey}/styles"],
            capture_output=True, text=True, timeout=30
        )
        style_data = json.loads(r3.stdout) if r3.returncode == 0 else {}
        styles = style_data.get("meta", {}).get("styles", [])

        # 汇总页面信息
        page_summaries = []
        total_nodes = 0
        for p in pages:
            children = p.get("children", [])
            total_nodes += len(children)
            page_summaries.append({
                "name": p["name"],
                "id": p["id"],
                "childCount": len(children),
                "topLevelNames": [c.get("name", "?") for c in children[:15]]
            })

        # 组件按 containing_frame 分组
        comp_by_group = {}
        for c in components:
            group = c.get("containing_frame", {}).get("name", "ungrouped")
            if group not in comp_by_group:
                comp_by_group[group] = []
            comp_by_group[group].append({
                "name": c["name"],
                "key": c["key"],
                "nodeId": c.get("node_id", ""),
                "description": c.get("description", "")
            })

        # 样式按类型分组
        style_by_type = {}
        for s in styles:
            st = s.get("style_type", "OTHER")
            if st not in style_by_type:
                style_by_type[st] = []
            style_by_type[st].append({
                "name": s["name"],
                "key": s["key"],
                "nodeId": s.get("node_id", ""),
                "description": s.get("description", "")
            })

        result = {
            "fileKey": fkey,
            "fileName": fname,
            "projectName": project_name,
            "lastModified": file_data.get("lastModified", ""),
            "version": file_data.get("version", ""),
            "extractedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "summary": {
                "pageCount": len(pages),
                "totalTopLevelNodes": total_nodes,
                "publishedComponents": len(components),
                "publishedStyles": len(styles),
                "styleBreakdown": {t: len(v) for t, v in style_by_type.items()},
                "worthDeepExtract": len(components) > 0 or len(styles) > 0
            },
            "pages": page_summaries,
            "componentGroups": comp_by_group,
            "styleGroups": style_by_type
        }

        results.append(result)
        print(f"    ✅ {len(pages)} 页, {len(components)} 组件, {len(styles)} 样式")

    except Exception as e:
        print(f"    ❌ 错误: {e}")
        errors.append({"file": fname, "key": fkey, "error": str(e)})

    time.sleep(0.5)

# 保存结果
safe_name = source.get("project", "unknown")
output_file = f"{output_dir}/{safe_name}-scan.json"
with open(output_file, "w") as f:
    json.dump({
        "project": safe_name,
        "projectName": project_name,
        "scannedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totalFiles": len(files),
        "successCount": len(results),
        "errorCount": len(errors),
        "files": results,
        "errors": errors
    }, f, ensure_ascii=False, indent=2)

print(f"\n📊 扫描完成: {len(results)}/{len(files)} 成功, {len(errors)} 失败")
print(f"📁 结果: {output_file}")

# 打印汇总
total_comps = sum(r["summary"]["publishedComponents"] for r in results)
total_styles = sum(r["summary"]["publishedStyles"] for r in results)
high_value = [r for r in results if r["summary"]["worthDeepExtract"]]
print(f"\n合计: {total_comps} 组件, {total_styles} 样式")
print(f"高价值文件（有组件/样式）: {len(high_value)} / {len(results)}")
PYEOF
