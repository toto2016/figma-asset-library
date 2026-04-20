#!/bin/bash
# 通过 REST API 获取高价值文件的全量组件列表
# 用法: FIGMA_TOKEN=xxx bash scripts/fetch-components.sh
set -e

if [ -z "$FIGMA_TOKEN" ]; then
  echo "❌ 请设置 FIGMA_TOKEN"
  exit 1
fi

OUTPUT_DIR="reports/extractions/components"
mkdir -p "$OUTPUT_DIR"

python3 - "$OUTPUT_DIR" << 'PYEOF'
import json, subprocess, os, sys, time

token = os.environ["FIGMA_TOKEN"]
output_dir = sys.argv[1]

# 所有有已发布组件的高价值文件
HIGH_VALUE_FILES = [
    {"fileKey": "OMp0bfNpPE8oHvRGAIrpvU", "system": "DesignOps", "name": "Design library - Mobile"},
    {"fileKey": "jIrRokAq33eq1ifxOtRFKS", "system": "DesignOps", "name": "Merchant Centre Library"},
    {"fileKey": "3FiNujs9BBmaEL5yZA1ih3", "system": "DesignOps", "name": "Design library - web"},
    {"fileKey": "fvIH2yRyQuqVMRKcmcwXYt", "system": "DesignOps", "name": "Icon Library"},
    {"fileKey": "g9F3TwBLLNWTYpF7oVMhHR", "system": "APB", "name": "[Design System] Web"},
    {"fileKey": "YNeBaTLNxbog6ZbmBAkykE", "system": "APB", "name": "[Content] Mobile"},
    {"fileKey": "FpqdumoL6hcQo3podguhe9", "system": "APB", "name": "[Content] Web"},
    {"fileKey": "jqprInB4CDozEXXw0lmlsb", "system": "APB", "name": "[Style Guide] Mobile"},
    {"fileKey": "Q8bFuMuXHKLX6X9S4IcVYU", "system": "APB", "name": "Gesture Icons"},
    {"fileKey": "SxKYbrp6JbItrSM4jyDyW6", "system": "Handover", "name": "Screen library - web"},
    {"fileKey": "D4UDNtlDzjN09lG1iy7ELj", "system": "Handover", "name": "Screen library - mobile"},
    {"fileKey": "vUCA0RnhjKYt6XvJat6tdP", "system": "Handover", "name": "Flow Library"},
]


def fetch_json(url):
    """调用 Figma REST API"""
    result = subprocess.run(
        ["curl", "-s", "--max-time", "30",
         "-H", f"X-Figma-Token: {token}", url],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


total_components = 0
for file_info in HIGH_VALUE_FILES:
    key = file_info["fileKey"]
    name = file_info["name"]
    system = file_info["system"]
    print(f"📦 {system}/{name} ({key})...")

    url = f"https://api.figma.com/v1/files/{key}/components"
    data = fetch_json(url)

    if data.get("error"):
        print(f"   ⚠️ 错误: {data['error']}")
        continue

    components = data.get("meta", {}).get("components", [])
    count = len(components)
    total_components += count
    print(f"   ✅ {count} 个组件")

    output = {
        "fileKey": key,
        "fileName": name,
        "system": system,
        "componentCount": count,
        "components": [{
            "key": c.get("key", ""),
            "name": c.get("name", ""),
            "description": c.get("description", ""),
            "node_id": c.get("node_id", ""),
            "containing_frame": c.get("containing_frame", {}),
        } for c in components]
    }

    out_path = os.path.join(output_dir, f"{key}.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    time.sleep(0.5)

print(f"\n✅ 全量组件列表获取完成，共 {total_components} 个组件")
PYEOF
