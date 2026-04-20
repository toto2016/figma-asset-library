#!/bin/bash
# 增量扫描 — 仅重新扫描有变更的 Figma 文件
# 用法: FIGMA_TOKEN=xxx bash scripts/incremental-scan.sh
# 比较每个文件的 version，仅在版本变更时重新提取
set -e

if [ -z "$FIGMA_TOKEN" ]; then
  echo "❌ 请设置 FIGMA_TOKEN"
  exit 1
fi

python3 - << 'PYEOF'
import json, subprocess, os, sys, time
from datetime import datetime

token = os.environ["FIGMA_TOKEN"]
COMP_DIR = "reports/extractions/components"
DEEP_DIR = "reports/extractions/deep"
VERSION_FILE = "reports/scan-versions.json"

TRACKED_FILES = [
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
    result = subprocess.run(
        ["curl", "-s", "--max-time", "15",
         "-H", f"X-Figma-Token: {token}", url],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


def load_versions():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE) as f:
            return json.load(f)
    return {}


def save_versions(versions):
    with open(VERSION_FILE, "w") as f:
        json.dump(versions, f, indent=2)


def rescan_components(file_info):
    """重新获取组件列表"""
    key = file_info["fileKey"]
    url = f"https://api.figma.com/v1/files/{key}/components"
    data = fetch_json(url)
    components = data.get("meta", {}).get("components", [])
    output = {
        "fileKey": key,
        "fileName": file_info["name"],
        "system": file_info["system"],
        "componentCount": len(components),
        "components": [{
            "key": c.get("key", ""),
            "name": c.get("name", ""),
            "description": c.get("description", ""),
            "node_id": c.get("node_id", ""),
            "containing_frame": c.get("containing_frame", {}),
        } for c in components]
    }
    os.makedirs(COMP_DIR, exist_ok=True)
    with open(os.path.join(COMP_DIR, f"{key}.json"), "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    return len(components)


versions = load_versions()
updated = 0
skipped = 0
errors = 0

print(f"🔍 增量扫描开始 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
print(f"   追踪文件: {len(TRACKED_FILES)}")
print()

for file_info in TRACKED_FILES:
    key = file_info["fileKey"]
    name = file_info["name"]

    # 获取当前版本
    url = f"https://api.figma.com/v1/files/{key}?depth=1"
    try:
        meta = fetch_json(url)
        current_version = meta.get("version", "")
        last_modified = meta.get("lastModified", "")
    except Exception as e:
        print(f"  ❌ {name}: 获取元数据失败 ({e})")
        errors += 1
        continue

    prev_version = versions.get(key, {}).get("version", "")

    if current_version == prev_version:
        print(f"  ⏭️  {name}: 无变更 (v={current_version[:12]}...)")
        skipped += 1
        continue

    print(f"  🔄 {name}: 版本变更! 重新扫描...")
    count = rescan_components(file_info)
    print(f"     ✅ {count} 个组件已更新")

    versions[key] = {
        "version": current_version,
        "lastModified": last_modified,
        "lastScanned": datetime.now().isoformat(),
        "componentCount": count,
    }
    updated += 1
    time.sleep(0.5)

save_versions(versions)

print(f"\n📊 扫描结果:")
print(f"   更新: {updated} | 跳过: {skipped} | 错误: {errors}")
print(f"   版本记录已保存: {VERSION_FILE}")
PYEOF
