#!/bin/bash
# 通过 REST API 下载组件缩略图到本地
# 用法: FIGMA_TOKEN=xxx bash scripts/download-screenshots.sh
# 从每个高价值文件获取组件缩略图 URL，然后下载到 screenshots/
set -e

if [ -z "$FIGMA_TOKEN" ]; then
  echo "❌ 请设置 FIGMA_TOKEN"
  exit 1
fi

python3 - << 'PYEOF'
import json, subprocess, os, sys, time, re
from datetime import datetime

token = os.environ["FIGMA_TOKEN"]
COMP_DIR = "reports/extractions/components"
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# 每个文件取 Top N 组件集截图
MAX_PER_FILE = 10


def fetch_json(url):
    result = subprocess.run(
        ["curl", "-s", "--max-time", "30",
         "-H", f"X-Figma-Token: {token}", url],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


def download_image(url, filepath):
    subprocess.run(
        ["curl", "-s", "-L", "--max-time", "15", "-o", filepath, url],
        capture_output=True
    )
    return os.path.exists(filepath) and os.path.getsize(filepath) > 100


def safe_filename(name):
    return re.sub(r'[^\w\-.]', '_', name)[:60]


total_downloaded = 0
total_failed = 0

for filename in sorted(os.listdir(COMP_DIR)):
    if not filename.endswith('.json'):
        continue
    with open(os.path.join(COMP_DIR, filename)) as f:
        data = json.load(f)

    file_key = data["fileKey"]
    file_name = data["fileName"]
    system = data["system"]
    components = data["components"]

    if not components:
        continue

    # 按 ComponentSet 去重，只取唯一组件集
    seen_sets = {}
    for comp in components:
        cs = (comp.get("containing_frame", {}) or {}).get(
            "containingComponentSet", {})
        cs_name = (cs or {}).get("name", "")
        key = cs_name or comp["name"]
        if key not in seen_sets:
            seen_sets[key] = comp["node_id"]

    # 取前 N 个
    node_ids = list(seen_sets.values())[:MAX_PER_FILE]
    node_names = list(seen_sets.keys())[:MAX_PER_FILE]

    if not node_ids:
        continue

    # 批量获取缩略图
    ids_param = ",".join(node_ids)
    url = (f"https://api.figma.com/v1/images/{file_key}"
           f"?ids={ids_param}&format=png&scale=2")

    print(f"\n📸 {system}/{file_name} ({len(node_ids)} 个组件)...")
    try:
        result = fetch_json(url)
    except Exception as e:
        print(f"   ❌ API 错误: {e}")
        continue

    images = result.get("images", {})
    if not images:
        print(f"   ⚠️ 无图片返回")
        continue

    file_dir = os.path.join(SCREENSHOT_DIR, safe_filename(f"{system}_{file_name}"))
    os.makedirs(file_dir, exist_ok=True)

    for node_id, name in zip(node_ids, node_names):
        img_url = images.get(node_id)
        if not img_url:
            continue
        safe_name = safe_filename(name)
        filepath = os.path.join(file_dir, f"{safe_name}.png")
        if download_image(img_url, filepath):
            total_downloaded += 1
            print(f"   ✅ {name}")
        else:
            total_failed += 1
            print(f"   ❌ {name}: 下载失败")

    time.sleep(1)

print(f"\n📊 截图下载完成:")
print(f"   成功: {total_downloaded}")
print(f"   失败: {total_failed}")
print(f"   保存目录: {SCREENSHOT_DIR}/")
PYEOF
