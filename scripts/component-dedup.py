#!/usr/bin/env python3
"""组件去重分析 — 基于全量 REST API 数据对比三个设计体系"""
import json, os, re
from collections import defaultdict
from datetime import datetime

COMP_DIR = 'reports/extractions/components'
OUTPUT_JSON = 'reports/component-dedup-report.json'
OUTPUT_MD = 'reports/component-dedup-report.md'


def normalize(name):
    """标准化名称用于匹配"""
    n = name.lower().strip()
    n = re.sub(r'[_\-\.\s]+', ' ', n)
    n = re.sub(r'\s+', ' ', n)
    return n.strip()


def classify_component(name):
    """按 UI 类型自动分类"""
    n = name.lower()
    rules = [
        ('button', ['button', 'btn', 'cta', 'fab']),
        ('icon', ['icon', 'ic-', 'ic_', 'ic ']),
        ('input', ['input', 'text field', 'textfield', 'search bar',
                    'textarea', 'otp']),
        ('card', ['card']),
        ('navigation', ['tab', 'nav', 'menu', 'sidebar', 'breadcrumb',
                         'pagination', 'header', 'footer', 'appbar',
                         'bottom bar', 'toolbar']),
        ('modal', ['modal', 'dialog', 'popup', 'bottom sheet', 'bottomsheet',
                    'overlay', 'drawer']),
        ('list', ['list', 'table', 'row', 'cell', 'grid']),
        ('badge', ['badge', 'tag', 'chip', 'label', 'status', 'pill']),
        ('avatar', ['avatar', 'profile pic']),
        ('toggle', ['toggle', 'switch', 'checkbox', 'radio', 'check box']),
        ('toast', ['toast', 'snackbar', 'notification', 'alert', 'banner']),
        ('loading', ['loading', 'spinner', 'skeleton', 'shimmer']),
        ('typography', ['heading', 'title', 'text', 'paragraph', 'caption',
                         'font', 'typography']),
        ('image', ['image', 'photo', 'thumbnail', 'illustration']),
        ('flag', ['flag', 'country']),
        ('voucher', ['voucher', 'coupon', 'deal', 'promo']),
        ('form', ['form', 'dropdown', 'select', 'picker', 'date picker',
                   'slider', 'stepper']),
        ('progress', ['progress', 'step indicator', 'stepper']),
        ('divider', ['divider', 'separator', 'line']),
        ('tooltip', ['tooltip', 'popover', 'hint']),
    ]
    for category, keywords in rules:
        if any(kw in n for kw in keywords):
            return category
    return 'other'


def load_all():
    """加载全量组件数据，按 ComponentSet 聚合"""
    component_sets = defaultdict(lambda: {
        'variants': [], 'system': '', 'file': '', 'fileKey': '',
        'pageName': '', 'frameName': '',
    })
    standalone = []

    for filename in sorted(os.listdir(COMP_DIR)):
        if not filename.endswith('.json'):
            continue
        with open(os.path.join(COMP_DIR, filename)) as f:
            data = json.load(f)

        system = data['system']
        file_name = data['fileName']
        file_key = data['fileKey']

        for comp in data['components']:
            frame = comp.get('containing_frame', {})
            cs = frame.get('containingComponentSet') or {}
            cs_name = cs.get('name', '')
            cs_node = cs.get('nodeId', '')
            page = frame.get('pageName', '')
            frame_name = frame.get('name', '')

            if cs_name:
                key = f"{file_key}::{cs_node}"
                entry = component_sets[key]
                entry['name'] = cs_name
                entry['system'] = system
                entry['file'] = file_name
                entry['fileKey'] = file_key
                entry['pageName'] = page
                entry['frameName'] = frame_name
                entry['variants'].append(comp['name'])
            else:
                standalone.append({
                    'name': comp['name'],
                    'system': system,
                    'file': file_name,
                    'fileKey': file_key,
                    'pageName': page,
                    'frameName': frame_name,
                    'category': classify_component(comp['name']),
                })

    return dict(component_sets), standalone


def find_cross_system_duplicates(component_sets):
    """按标准化名称查找跨体系重复的组件集"""
    by_normalized = defaultdict(list)
    for key, cs in component_sets.items():
        norm = normalize(cs['name'])
        by_normalized[norm].append({**cs, 'csKey': key})

    duplicates = []
    for norm_name, entries in by_normalized.items():
        systems = set(e['system'] for e in entries)
        if len(systems) >= 2:
            total_variants = sum(len(e['variants']) for e in entries)
            duplicates.append({
                'normalizedName': norm_name,
                'displayName': entries[0]['name'],
                'category': classify_component(norm_name),
                'systemCount': len(systems),
                'systems': sorted(systems),
                'totalVariants': total_variants,
                'instances': [{
                    'system': e['system'],
                    'file': e['file'],
                    'page': e['pageName'],
                    'componentSetName': e['name'],
                    'variantCount': len(e['variants']),
                    'sampleVariants': e['variants'][:5],
                } for e in entries]
            })
    duplicates.sort(key=lambda x: x['totalVariants'], reverse=True)
    return duplicates


def find_intra_system_duplicates(component_sets):
    """查找同体系内跨文件的重复组件"""
    by_system = defaultdict(lambda: defaultdict(list))
    for key, cs in component_sets.items():
        norm = normalize(cs['name'])
        by_system[cs['system']][norm].append(cs)

    intra_dupes = []
    for system, name_groups in by_system.items():
        for norm_name, entries in name_groups.items():
            files = set(e['file'] for e in entries)
            if len(files) >= 2:
                intra_dupes.append({
                    'normalizedName': norm_name,
                    'displayName': entries[0]['name'],
                    'system': system,
                    'fileCount': len(files),
                    'files': sorted(files),
                    'totalVariants': sum(len(e['variants']) for e in entries),
                })
    intra_dupes.sort(key=lambda x: x['totalVariants'], reverse=True)
    return intra_dupes


def build_category_matrix(component_sets, standalone):
    """构建分类 × 体系矩阵"""
    matrix = defaultdict(lambda: defaultdict(int))
    for cs in component_sets.values():
        cat = classify_component(cs['name'])
        matrix[cat][cs['system']] += len(cs['variants'])
    for comp in standalone:
        matrix[comp['category']][comp['system']] += 1

    rows = []
    for cat in sorted(matrix.keys()):
        row = {'category': cat, 'total': sum(matrix[cat].values())}
        for sys in ['DesignOps', 'APB', 'Handover']:
            row[sys] = matrix[cat].get(sys, 0)
        rows.append(row)
    rows.sort(key=lambda x: x['total'], reverse=True)
    return rows


def build_system_summary(component_sets, standalone):
    """按体系汇总"""
    stats = defaultdict(lambda: {
        'componentSets': 0, 'totalVariants': 0,
        'standaloneComponents': 0, 'files': set()
    })
    for cs in component_sets.values():
        s = stats[cs['system']]
        s['componentSets'] += 1
        s['totalVariants'] += len(cs['variants'])
        s['files'].add(cs['file'])
    for comp in standalone:
        s = stats[comp['system']]
        s['standaloneComponents'] += 1
        s['files'].add(comp['file'])

    return {sys: {
        'componentSets': info['componentSets'],
        'totalVariants': info['totalVariants'],
        'standaloneComponents': info['standaloneComponents'],
        'totalAll': info['totalVariants'] + info['standaloneComponents'],
        'fileCount': len(info['files']),
        'files': sorted(info['files']),
    } for sys, info in sorted(stats.items())}


def generate_markdown(report):
    """生成可读的 Markdown 报告"""
    lines = [
        '# 组件去重分析报告',
        f'\n> 生成时间: {report["generatedAt"]}',
        f'> 总组件数: {report["totalComponents"]}',
        f'> 组件集(ComponentSet): {report["totalComponentSets"]}',
        '\n---\n',
        '## 一、各体系概览\n',
        '| 体系 | 组件集 | 变体总数 | 独立组件 | 合计 | 文件数 |',
        '|------|--------|---------|---------|------|--------|',
    ]
    for sys, info in report['systemSummary'].items():
        lines.append(
            f'| {sys} | {info["componentSets"]} | '
            f'{info["totalVariants"]} | {info["standaloneComponents"]} | '
            f'{info["totalAll"]} | {info["fileCount"]} |'
        )

    lines.extend([
        '\n---\n',
        '## 二、跨体系重复组件\n',
        f'共发现 **{report["crossSystemDuplicates"]["totalGroups"]}** '
        f'组同名组件跨越多个设计体系，'
        f'涉及 **{report["crossSystemDuplicates"]["totalVariants"]}** 个变体。\n',
    ])

    for i, dup in enumerate(report['crossSystemDuplicates']['groups'][:30]):
        lines.append(
            f'### {i+1}. `{dup["displayName"]}` '
            f'({dup["category"]}) — {dup["totalVariants"]} 变体\n'
        )
        lines.append(f'跨越: {", ".join(dup["systems"])}\n')
        lines.append('| 体系 | 文件 | 页面 | 变体数 | 示例 |')
        lines.append('|------|------|------|--------|------|')
        for inst in dup['instances']:
            samples = ', '.join(inst['sampleVariants'][:3])
            lines.append(
                f'| {inst["system"]} | {inst["file"]} | '
                f'{inst["page"]} | {inst["variantCount"]} | '
                f'{samples} |'
            )
        lines.append('')

    lines.extend([
        '\n---\n',
        '## 三、体系内跨文件重复\n',
    ])
    for dup in report['intraSystemDuplicates'][:20]:
        files = ', '.join(dup['files'])
        lines.append(
            f'- **{dup["displayName"]}** ({dup["system"]}) — '
            f'{dup["totalVariants"]} 变体, 出现在: {files}'
        )

    lines.extend([
        '\n---\n',
        '## 四、分类分布矩阵\n',
        '| 分类 | 总计 | DesignOps | APB | Handover |',
        '|------|------|-----------|-----|----------|',
    ])
    for row in report['categoryDistribution']:
        lines.append(
            f'| {row["category"]} | {row["total"]} | '
            f'{row.get("DesignOps", 0)} | {row.get("APB", 0)} | '
            f'{row.get("Handover", 0)} |'
        )

    lines.extend([
        '\n---\n',
        '## 五、去重建议\n',
        '1. **跨体系重复组件**应选择一个"主版本"，其余标记为弃用',
        '2. **体系内重复**通常是 Mobile/Web 两端的同名组件，'
        '需确认是否为同一设计意图的不同平台实现',
        '3. **Handover 项目**的组件大多是页面级截图而非原子组件，'
        '不应纳入统一组件库',
        '4. 建议统一组件库以 DesignOps 为基础，'
        '补充 APB 中独有的现代化组件（如 Design System Web 体系）',
    ])

    return '\n'.join(lines)


def main():
    component_sets, standalone = load_all()
    cross_dupes = find_cross_system_duplicates(component_sets)
    intra_dupes = find_intra_system_duplicates(component_sets)
    category_matrix = build_category_matrix(component_sets, standalone)
    system_summary = build_system_summary(component_sets, standalone)

    report = {
        'generatedAt': datetime.now().isoformat(),
        'totalComponents': sum(
            s['totalAll'] for s in system_summary.values()
        ),
        'totalComponentSets': len(component_sets),
        'systemSummary': system_summary,
        'crossSystemDuplicates': {
            'totalGroups': len(cross_dupes),
            'totalVariants': sum(d['totalVariants'] for d in cross_dupes),
            'groups': cross_dupes
        },
        'intraSystemDuplicates': intra_dupes,
        'categoryDistribution': category_matrix,
    }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    md = generate_markdown(report)
    with open(OUTPUT_MD, 'w') as f:
        f.write(md)

    print(f'✅ 去重分析完成')
    print(f'   总组件: {report["totalComponents"]}')
    print(f'   组件集: {len(component_sets)}')
    print(f'   独立组件: {len(standalone)}')
    print(f'   跨体系重复组: {len(cross_dupes)}'
          f' ({sum(d["totalVariants"] for d in cross_dupes)} 变体)')
    print(f'   体系内重复组: {len(intra_dupes)}')
    for sys, info in system_summary.items():
        print(f'   {sys}: {info["totalAll"]} 组件 '
              f'({info["componentSets"]} 集 + '
              f'{info["standaloneComponents"]} 独立)')
    print(f'   JSON: {OUTPUT_JSON}')
    print(f'   报告: {OUTPUT_MD}')


if __name__ == '__main__':
    main()
