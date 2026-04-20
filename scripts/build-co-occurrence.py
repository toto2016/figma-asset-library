#!/usr/bin/env python3
"""从分类数据构建组件共现矩阵 — 分析哪些 UI 类型经常一起出现在同一流程中"""
import json
import os
from collections import defaultdict, Counter
from itertools import combinations

BY_TYPE_DIR = 'catalog/classified/by-type'
OUTPUT = 'catalog/component-co-occurrence.json'


def load_classified_components():
    """加载所有按类型分类的组件"""
    by_type = {}
    for tf in sorted(os.listdir(BY_TYPE_DIR)):
        if not tf.endswith('.json'):
            continue
        with open(os.path.join(BY_TYPE_DIR, tf)) as f:
            td = json.load(f)
        ui_type = tf.replace('.json', '')
        by_type[ui_type] = td.get('items', [])
    return by_type


def build_file_type_matrix(by_type):
    """构建 file → ui_types 矩阵，找出每个文件包含哪些类型的组件"""
    file_types = defaultdict(set)
    type_files = defaultdict(set)

    for ui_type, items in by_type.items():
        for item in items:
            file_name = item.get('file', '')
            system = item.get('system', '')
            file_key = f"{system}/{file_name}"
            file_types[file_key].add(ui_type)
            type_files[ui_type].add(file_key)

    return file_types, type_files


def compute_co_occurrence(file_types):
    """计算 UI 类型之间的共现频率"""
    pair_count = Counter()
    for file_key, types in file_types.items():
        type_list = sorted(types)
        for a, b in combinations(type_list, 2):
            pair_count[(a, b)] += 1
    return pair_count


def build_adjacency(pair_count, type_files):
    """构建邻接表形式的共现关系"""
    adjacency = defaultdict(list)
    for (a, b), count in pair_count.most_common():
        if count < 2:
            break
        adjacency[a].append({'type': b, 'coOccurrence': count})
        adjacency[b].append({'type': a, 'coOccurrence': count})

    for ui_type in adjacency:
        adjacency[ui_type].sort(key=lambda x: -x['coOccurrence'])

    return dict(adjacency)


def main():
    by_type = load_classified_components()
    total_comps = sum(len(v) for v in by_type.values())
    print(f'加载 {len(by_type)} 种 UI 类型，{total_comps} 个组件')

    file_types, type_files = build_file_type_matrix(by_type)
    print(f'涉及 {len(file_types)} 个文件')

    pair_count = compute_co_occurrence(file_types)
    adjacency = build_adjacency(pair_count, type_files)

    # 组件类型统计
    type_stats = {}
    for ui_type, items in by_type.items():
        systems = Counter(i.get('system', '?') for i in items)
        type_stats[ui_type] = {
            'total': len(items),
            'systems': dict(systems),
            'fileCount': len(type_files.get(ui_type, set())),
            'topCoOccurrences': adjacency.get(ui_type, [])[:5]
        }

    result = {
        'generatedAt': __import__('datetime').datetime.now().isoformat(),
        'totalTypes': len(by_type),
        'totalComponents': total_comps,
        'totalFiles': len(file_types),
        'typeStats': dict(sorted(type_stats.items(),
                                  key=lambda x: -x[1]['total'])),
        'topPairs': [
            {'types': list(pair), 'coOccurrence': count}
            for pair, count in pair_count.most_common(30)
        ]
    }

    with open(OUTPUT, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f'\n✅ 共现矩阵已生成: {OUTPUT}')
    print(f'\n=== Top 15 共现对 ===')
    for pair, count in pair_count.most_common(15):
        print(f'  {pair[0]} ↔ {pair[1]}: {count}')


if __name__ == '__main__':
    main()
