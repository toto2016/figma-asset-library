#!/bin/bash
# Figma 项目文件发现脚本
# 用法: FIGMA_TOKEN=xxx bash scripts/discover-files.sh
#
# 获取 token 步骤:
#   1. 打开 https://www.figma.com/developers/api#access-tokens
#   2. 生成 Personal Access Token
#   3. 复制 token 后执行此脚本

set -e

if [ -z "$FIGMA_TOKEN" ]; then
  echo "❌ 请设置 FIGMA_TOKEN"
  echo "用法: FIGMA_TOKEN=figd_xxx bash scripts/discover-files.sh"
  exit 1
fi

TEAM_ID="1001793964266497780"
ORG_ID="1001709743790382367"

echo "🔍 正在获取 Atome UED 团队项目列表..."

PROJECTS_JSON=$(curl -sf -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/teams/$TEAM_ID/projects")

if [ $? -ne 0 ]; then
  echo "❌ API 调用失败，请检查 token 是否正确"
  exit 1
fi

echo "$PROJECTS_JSON" | python3 -c "
import json, sys, subprocess, os, re
from datetime import date

data = json.load(sys.stdin)
projects = data.get('projects', [])
print(f'✅ 发现 {len(projects)} 个项目')

name_map = {
    'Flow Library': 'flow-library',
    'DesignOps': 'designops',
    'UI Sandbox': 'ui-sandbox',
    'APS': 'aps',
    'Online Integration': 'online-integration',
    'Handover': 'handover',
    'Design QA': 'design-qa',
    'Atome Product 101': 'product-101',
    'Research': 'research',
    'UX Sandbox': 'ux-sandbox',
    'Misc': 'misc',
    'Atome AI Test': 'atome-ai-test'
}

total_files = 0
summary = []

for proj in projects:
    pid = str(proj['id'])
    pname = proj['name']

    # 匹配已知项目名
    safe_name = None
    for known, slug in name_map.items():
        if known.lower() in pname.lower():
            safe_name = slug
            break
    if not safe_name:
        safe_name = re.sub(r'[^a-z0-9]+', '-', pname.lower()).strip('-')

    print(f'  📁 {pname} (ID: {pid})')
    files_raw = subprocess.run(
        ['curl', '-sf', '-H', f'X-Figma-Token: {os.environ[\"FIGMA_TOKEN\"]}',
         f'https://api.figma.com/v1/projects/{pid}/files'],
        capture_output=True, text=True
    )

    if files_raw.returncode != 0:
        print(f'     ⚠️  获取文件失败，跳过')
        continue

    files_data = json.loads(files_raw.stdout)
    files = files_data.get('files', [])

    source_entry = {
        'project': safe_name,
        'projectName': pname,
        'projectId': pid,
        'projectUrl': f'https://www.figma.com/files/$ORG_ID/project/{pid}',
        'lastUpdated': str(date.today()),
        'files': []
    }

    for f in files:
        source_entry['files'].append({
            'name': f['name'],
            'fileKey': f['key'],
            'url': f'https://www.figma.com/design/{f[\"key\"]}',
            'lastModified': f.get('last_modified', ''),
            'status': 'pending'
        })

    out_path = f'sources/{safe_name}.json'
    with open(out_path, 'w') as out:
        json.dump(source_entry, out, ensure_ascii=False, indent=2)

    total_files += len(files)
    summary.append({'name': pname, 'slug': safe_name, 'count': len(files)})
    print(f'     -> {len(files)} 个文件 -> {out_path}')

print(f'\\n📊 总计: {len(projects)} 个项目, {total_files} 个文件')
print('\\n项目文件数:')
for s in sorted(summary, key=lambda x: -x['count']):
    print(f'  {s[\"name\"]}: {s[\"count\"]}')
" 2>&1

echo ""
echo "✅ 所有源文件清单已更新到 sources/ 目录"
