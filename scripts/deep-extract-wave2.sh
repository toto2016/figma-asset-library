#!/bin/bash
# Wave 2 深度提取: APB + Handover 高价值文件
# 用法: FIGMA_TOKEN=xxx bash scripts/deep-extract-wave2.sh

set -e

if [ -z "$FIGMA_TOKEN" ]; then
  echo "❌ 请设置 FIGMA_TOKEN"
  exit 1
fi

OUTPUT_DIR="reports/extractions/deep"
mkdir -p "$OUTPUT_DIR"

python3 - "$OUTPUT_DIR" << 'PYEOF'
import json, subprocess, os, sys, time

token = os.environ["FIGMA_TOKEN"]
output_dir = sys.argv[1]

HIGH_VALUE_FILES = [
    {"fileKey": "g9F3TwBLLNWTYpF7oVMhHR", "name": "[Design System] Web", "project": "apb"},
    {"fileKey": "YNeBaTLNxbog6ZbmBAkykE", "name": "[Content] Mobile", "project": "apb"},
    {"fileKey": "FpqdumoL6hcQo3podguhe9", "name": "[Content] Web", "project": "apb"},
    {"fileKey": "3FiNujs9BBmaEL5yZA1ih3", "name": "[Design System] Mobile 2.0", "project": "apb"},
    {"fileKey": "D4UDNtlDzjN09lG1iy7ELj", "name": "[Asset] Illustration", "project": "apb"},
    {"fileKey": "SxKYbrp6JbItrSM4jyDyW6", "name": "Screen library - mobile app", "project": "handover"},
    {"fileKey": "jqprInB4CDozEXXw0lmlsb", "name": "Screen library - web", "project": "handover"},
]

def fetch_json(url):
    r = subprocess.run(
        ["curl", "-sf", "-H", f"X-Figma-Token: {token}", url],
        capture_output=True, text=True, timeout=60
    )
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)

def summarize_children(children, depth=0):
    if depth > 1 or not children:
        return []
    summaries = []
    for c in children[:30]:
        s = {"name": c.get("name", "?"), "type": c.get("type", "")}
        if c.get("characters"):
            s["text"] = c["characters"]
        if c.get("style"):
            s["textStyle"] = {
                "fontFamily": c["style"].get("fontFamily"),
                "fontSize": c["style"].get("fontSize"),
                "fontWeight": c["style"].get("fontWeight"),
            }
        if c.get("fills"):
            s["fills"] = c["fills"]
        if c.get("cornerRadius"):
            s["cornerRadius"] = c["cornerRadius"]
        if c.get("layoutMode"):
            s["layoutMode"] = c["layoutMode"]
        sub = c.get("children", [])
        if sub:
            s["children"] = summarize_children(sub, depth + 1)
        summaries.append(s)
    return summaries

def extract_file(finfo):
    fkey = finfo["fileKey"]
    fname = finfo["name"]
    print(f"\n{'='*60}")
    print(f"🔬 深度提取: {fname}")
    print(f"   fileKey: {fkey}")

    result = {"fileKey": fkey, "fileName": fname, "project": finfo["project"]}

    print("  [1/4] 文件结构 (depth=3)...")
    file_data = fetch_json(f"https://api.figma.com/v1/files/{fkey}?depth=3")
    if not file_data:
        print("  ❌ 文件结构获取失败")
        return None

    result["lastModified"] = file_data.get("lastModified", "")
    result["version"] = file_data.get("version", "")
    pages = file_data.get("document", {}).get("children", [])
    result["pageCount"] = len(pages)
    result["pages"] = []
    for p in pages:
        children = p.get("children", [])
        page_info = {
            "name": p["name"], "id": p["id"],
            "childCount": len(children),
            "children": [
                {"name": c.get("name", "?"), "id": c.get("id", ""), "type": c.get("type", ""),
                 "childCount": len(c.get("children", [])),
                 "childNames": [sc.get("name", "?") for sc in c.get("children", [])[:20]]}
                for c in children
            ]
        }
        result["pages"].append(page_info)
    time.sleep(0.5)

    print("  [2/4] 已发布组件...")
    comp_data = fetch_json(f"https://api.figma.com/v1/files/{fkey}/components")
    components = comp_data.get("meta", {}).get("components", []) if comp_data else []
    result["publishedComponents"] = len(components)

    comp_node_ids = [c.get("node_id", "") for c in components[:50] if c.get("node_id")]
    if comp_node_ids:
        print(f"  [2b/4] 组件节点属性 ({len(comp_node_ids)} 个)...")
        result["componentDetails"] = []
        batch_size = 10
        for bs in range(0, len(comp_node_ids), batch_size):
            batch = comp_node_ids[bs:bs + batch_size]
            ids_param = ",".join(batch)
            nodes_data = fetch_json(f"https://api.figma.com/v1/files/{fkey}/nodes?ids={ids_param}")
            if nodes_data and "nodes" in nodes_data:
                for nid, ndata in nodes_data["nodes"].items():
                    doc = ndata.get("document", {})
                    result["componentDetails"].append({
                        "nodeId": nid, "name": doc.get("name", "?"), "type": doc.get("type", ""),
                        "absoluteBoundingBox": doc.get("absoluteBoundingBox"),
                        "fills": doc.get("fills", []), "strokes": doc.get("strokes", []),
                        "effects": doc.get("effects", []),
                        "cornerRadius": doc.get("cornerRadius"),
                        "layoutMode": doc.get("layoutMode"),
                        "paddingLeft": doc.get("paddingLeft"), "paddingRight": doc.get("paddingRight"),
                        "paddingTop": doc.get("paddingTop"), "paddingBottom": doc.get("paddingBottom"),
                        "itemSpacing": doc.get("itemSpacing"),
                        "componentProperties": doc.get("componentProperties"),
                        "children": summarize_children(doc.get("children", []))
                    })
            time.sleep(0.5)
    else:
        result["componentDetails"] = []

    result["componentIndex"] = [
        {"name": c["name"], "key": c["key"], "nodeId": c.get("node_id", ""),
         "description": c.get("description", ""),
         "containingFrame": c.get("containing_frame", {}).get("name", "")}
        for c in components
    ]
    time.sleep(0.5)

    print("  [3/4] 已发布样式...")
    style_data = fetch_json(f"https://api.figma.com/v1/files/{fkey}/styles")
    styles = style_data.get("meta", {}).get("styles", []) if style_data else []
    result["publishedStyles"] = len(styles)

    style_node_ids = [s.get("node_id", "") for s in styles if s.get("node_id")]
    if style_node_ids:
        print(f"  [3b/4] 样式节点属性 ({len(style_node_ids)} 个)...")
        ids_param = ",".join(style_node_ids)
        style_nodes = fetch_json(f"https://api.figma.com/v1/files/{fkey}/nodes?ids={ids_param}")
        result["styleDetails"] = []
        if style_nodes and "nodes" in style_nodes:
            for nid, ndata in style_nodes["nodes"].items():
                doc = ndata.get("document", {})
                detail = {"nodeId": nid, "name": doc.get("name", "?"), "type": doc.get("type", "")}
                if doc.get("fills"): detail["fills"] = doc["fills"]
                if doc.get("style"): detail["textStyle"] = doc["style"]
                if doc.get("effects"): detail["effects"] = doc["effects"]
                result["styleDetails"].append(detail)
    else:
        result["styleDetails"] = []
    time.sleep(0.5)

    print("  [4/4] 变量...")
    var_data = fetch_json(f"https://api.figma.com/v1/files/{fkey}/variables/local")
    if var_data and "meta" in var_data:
        meta = var_data["meta"]
        collections = meta.get("variableCollections", {})
        variables = meta.get("variables", {})
        result["variableCollections"] = len(collections)
        result["variables"] = len(variables)
        result["variableDetails"] = {
            "collections": [
                {"id": cid, "name": c.get("name", "?"),
                 "modes": [{"modeId": m["modeId"], "name": m["name"]} for m in c.get("modes", [])],
                 "variableIds": c.get("variableIds", [])}
                for cid, c in collections.items()
            ],
            "variables": [
                {"id": vid, "name": v.get("name", "?"), "resolvedType": v.get("resolvedType", ""),
                 "valuesByMode": v.get("valuesByMode", {}), "scopes": v.get("scopes", [])}
                for vid, v in list(variables.items())[:200]
            ]
        }
    else:
        result["variableCollections"] = 0
        result["variables"] = 0
        result["variableDetails"] = None

    result["extractedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return result

print("🔬 Wave 2 深度提取")
print(f"   目标: {len(HIGH_VALUE_FILES)} 个文件")
print(f"   输出: {output_dir}/\n")

all_results = []
for finfo in HIGH_VALUE_FILES:
    result = extract_file(finfo)
    if result:
        out_path = f"{output_dir}/{finfo['fileKey']}.json"
        with open(out_path, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        all_results.append(result)
        print(f"  💾 已保存 → {out_path}")
        print(f"     组件: {result.get('publishedComponents',0)} (详情: {len(result.get('componentDetails',[]))}), 样式: {result.get('publishedStyles',0)}, 变量: {result.get('variables',0)}")

print(f"\n{'='*60}")
print(f"✅ 深度提取完成: {len(all_results)}/{len(HIGH_VALUE_FILES)} 成功")
total_c = sum(r.get("publishedComponents", 0) for r in all_results)
total_s = sum(r.get("publishedStyles", 0) for r in all_results)
total_v = sum(r.get("variables", 0) for r in all_results)
total_d = sum(len(r.get("componentDetails", [])) for r in all_results)
print(f"   组件: {total_c} ({total_d} 个有详细属性)")
print(f"   样式: {total_s}")
print(f"   变量: {total_v}")
PYEOF
