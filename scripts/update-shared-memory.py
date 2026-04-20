#!/usr/bin/env python3
"""
更新共享记忆系统 — 从 operation-log 和项目数据中同步到 ~/.shared-memory/

用法:
  python3 scripts/update-shared-memory.py              # 更新 timeline（当天）
  python3 scripts/update-shared-memory.py --core        # 同时更新 CORE.md
  python3 scripts/update-shared-memory.py --full        # 全量更新所有文件
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

MEMORY_DIR = Path.home() / '.shared-memory' / 'figma-asset-library'
TIMELINE_DIR = MEMORY_DIR / 'timeline'
PROJECT_ROOT = Path(__file__).parent.parent
OP_LOG = PROJECT_ROOT / 'reports' / 'operation-log.md'
TODAY = datetime.now().strftime('%Y-%m-%d')


def ensure_dirs():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    TIMELINE_DIR.mkdir(parents=True, exist_ok=True)


def extract_today_stages():
    """从 operation-log.md 中提取今天的 Stage 条目"""
    if not OP_LOG.exists():
        return []

    content = OP_LOG.read_text(encoding='utf-8')
    stages = []
    current_stage = None
    current_date = None

    for line in content.split('\n'):
        stage_match = re.match(r'^## (Stage \d+:.+)', line)
        if stage_match:
            current_stage = stage_match.group(1)
            current_date = None
            continue

        date_match = re.match(r'\*\*日期\*\*:\s*(\d{4}-\d{2}-\d{2})', line)
        if date_match and current_stage:
            current_date = date_match.group(1)
            if current_date == TODAY:
                stages.append(current_stage)

    return stages


def update_timeline():
    """生成/更新当天的 timeline 文件"""
    stages = extract_today_stages()
    timeline_file = TIMELINE_DIR / f'{TODAY}.md'

    if not stages and not timeline_file.exists():
        print(f'  今天暂无 Stage 记录，跳过 timeline')
        return

    if stages:
        content = f'# {TODAY}\n\n## 完成\n'
        for s in stages:
            content += f'- {s}\n'
        content += '\n## 备注\n- 由 update-shared-memory.py 自动生成\n'
        timeline_file.write_text(content, encoding='utf-8')
        print(f'  ✅ timeline/{TODAY}.md 已更新（{len(stages)} 个 Stage）')
    else:
        print(f'  ℹ️  timeline/{TODAY}.md 已存在，无新 Stage')


def compact_old_timelines():
    """将超过 14 天的 timeline 压缩为月度摘要"""
    cutoff = datetime.now() - timedelta(days=14)
    monthly = {}

    for f in sorted(TIMELINE_DIR.glob('????-??-??.md')):
        try:
            file_date = datetime.strptime(f.stem, '%Y-%m-%d')
        except ValueError:
            continue

        if file_date >= cutoff:
            continue

        month_key = file_date.strftime('%Y-%m')
        if month_key not in monthly:
            monthly[month_key] = []

        content = f.read_text(encoding='utf-8')
        completed = []
        in_completed = False
        for line in content.split('\n'):
            if line.startswith('## 完成'):
                in_completed = True
                continue
            if line.startswith('## ') and in_completed:
                in_completed = False
            if in_completed and line.startswith('- '):
                completed.append(line)

        if completed:
            monthly[month_key].append({
                'date': f.stem,
                'items': completed
            })

    for month, entries in monthly.items():
        summary_file = TIMELINE_DIR / f'{month}-summary.md'
        content = f'# {month} 月度摘要\n\n'
        for entry in entries:
            content += f'## {entry["date"]}\n'
            for item in entry['items']:
                content += f'{item}\n'
            content += '\n'

        summary_file.write_text(content, encoding='utf-8')
        # 删除已压缩的日志
        for entry in entries:
            old_file = TIMELINE_DIR / f'{entry["date"]}.md'
            old_file.unlink(missing_ok=True)

        print(f'  📦 {month} 压缩了 {len(entries)} 天到月度摘要')


def update_core():
    """更新 CORE.md 热摘要"""
    core_file = MEMORY_DIR / 'CORE.md'
    if not core_file.exists():
        print('  ⚠️  CORE.md 不存在，跳过')
        return

    # 读取最近 3 天 timeline 获取最新动态
    recent_decisions = []
    for i in range(3):
        d = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        tf = TIMELINE_DIR / f'{d}.md'
        if tf.exists():
            content = tf.read_text(encoding='utf-8')
            in_decisions = False
            for line in content.split('\n'):
                if line.startswith('## 决策'):
                    in_decisions = True
                    continue
                if line.startswith('## ') and in_decisions:
                    in_decisions = False
                if in_decisions and line.startswith('- '):
                    recent_decisions.append(f'{d}: {line[2:]}')

    if recent_decisions:
        core = core_file.read_text(encoding='utf-8')
        # 更新"最近关键决策"部分
        new_decisions = '\n'.join(f'- {d}' for d in recent_decisions[:5])
        core = re.sub(
            r'(## 最近关键决策\n\n)(.*?)(\n\n## )',
            f'\\1{new_decisions}\n\\3',
            core,
            flags=re.DOTALL
        )
        core_file.write_text(core, encoding='utf-8')
        print(f'  ✅ CORE.md 已更新（{len(recent_decisions)} 条最近决策）')
    else:
        print(f'  ℹ️  无新决策，CORE.md 未变')


def main():
    ensure_dirs()
    args = set(sys.argv[1:])

    print(f'🧠 共享记忆更新 — {TODAY}')
    print(f'   目录: {MEMORY_DIR}')
    print()

    # 始终更新 timeline
    update_timeline()
    compact_old_timelines()

    if '--core' in args or '--full' in args:
        update_core()

    if '--full' in args:
        print('\n  ℹ️  FACTS.md / PREFS.md / OPS.md 需手动更新（内容需人工判断）')

    print('\n✅ 完成')


if __name__ == '__main__':
    main()
