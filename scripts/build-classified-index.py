#!/usr/bin/env python3
"""多维度分类索引 — 按 UI类型/平台/体系/模块 对全量组件建立索引"""
import json, os, re
from collections import defaultdict
from datetime import datetime

COMP_DIR = 'reports/extractions/components'
OUTPUT_DIR = 'catalog/classified'
OUTPUT_INDEX = 'catalog/classified-index.json'


def normalize(name):
    """标准化名称"""
    return re.sub(r'[_\-\.\s]+', ' ', name.lower()).strip()


def detect_platform(file_name):
    """根据文件名推断平台"""
    n = file_name.lower()
    if 'mobile' in n or 'app' in n:
        return 'mobile'
    if 'web' in n:
        return 'web'
    if 'icon' in n or 'illustration' in n:
        return 'shared'
    return 'unknown'


def classify_component(name):
    """按 UI 类型分类（与 dedup 脚本一致）"""
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
        ('progress', ['progress', 'step indicator']),
        ('divider', ['divider', 'separator', 'line']),
        ('tooltip', ['tooltip', 'popover', 'hint']),
        ('logo', ['logo', 'brand', 'atome-logo']),
    ]
    for category, keywords in rules:
        if any(kw in n for kw in keywords):
            return category
    return 'other'


def detect_business_module(name, page_name, frame_name):
    """识别业务模块"""
    combined = f'{name} {page_name} {frame_name}'.lower()
    modules = {
        'payment': ['payment', 'pay', 'checkout', 'transaction', 'trx',
                     'wallet', 'top up', 'topup', 'bank'],
        'kyc': ['kyc', 'verification', 'identity', 'id card', 'selfie',
                 'liveness', 'ktp', 'nric', 'cmnd'],
        'onboarding': ['onboarding', 'sign up', 'signup', 'register',
                        'welcome', 'intro'],
        'merchant': ['merchant', 'store', 'shop', 'partner', 'deal'],
        'home': ['home', 'dashboard', 'main page'],
        'profile': ['profile', 'account', 'setting', 'my page'],
        'voucher': ['voucher', 'coupon', 'promo', 'reward', 'cashback'],
        'notification': ['notification', 'inbox', 'message'],
        'loan': ['loan', 'instalment', 'installment', 'bnpl', 'credit'],
    }
    for module, keywords in modules.items():
        if any(kw in combined for kw in keywords):
            return module
    return 'general'


def load_all():
    """加载全量组件并增加多维度标签"""
    components = []
    for filename in sorted(os.listdir(COMP_DIR)):
        if not filename.endswith('.json'):
            continue
        with open(os.path.join(COMP_DIR, filename)) as f:
            data = json.load(f)

        system = data['system']
        file_name = data['fileName']
        file_key = data['fileKey']
        platform = detect_platform(file_name)

        for comp in data['components']:
            frame = comp.get('containing_frame', {}) or {}
            cs = (frame.get('containingComponentSet') or {})
            cs_name = cs.get('name', '')
            page_name = frame.get('pageName', '')
            frame_name = frame.get('name', '')
            display_name = cs_name or comp['name']

            components.append({
                'name': comp['name'],
                'displayName': display_name,
                'key': comp.get('key', ''),
                'nodeId': comp.get('node_id', ''),
                'description': comp.get('description', ''),
                'system': system,
                'file': file_name,
                'fileKey': file_key,
                'platform': platform,
                'page': page_name,
                'frame': frame_name,
                'componentSet': cs_name,
                'uiType': classify_component(display_name),
                'businessModule': detect_business_module(
                    display_name, page_name, frame_name
                ),
            })
    return components


def build_indices(components):
    """构建多维度索引"""
    by_type = defaultdict(list)
    by_platform = defaultdict(list)
    by_system = defaultdict(list)
    by_module = defaultdict(list)
    by_type_platform = defaultdict(list)

    for comp in components:
        ref = {
            'name': comp['displayName'],
            'key': comp['key'],
            'system': comp['system'],
            'file': comp['file'],
            'platform': comp['platform'],
            'uiType': comp['uiType'],
            'module': comp['businessModule'],
        }
        by_type[comp['uiType']].append(ref)
        by_platform[comp['platform']].append(ref)
        by_system[comp['system']].append(ref)
        by_module[comp['businessModule']].append(ref)
        combo = f"{comp['uiType']}_{comp['platform']}"
        by_type_platform[combo].append(ref)

    return by_type, by_platform, by_system, by_module, by_type_platform


def save_dimension(name, data, output_dir):
    """保存单个维度的索引文件"""
    dim_dir = os.path.join(output_dir, name)
    os.makedirs(dim_dir, exist_ok=True)
    summary = {}
    for key, items in data.items():
        summary[key] = len(items)
        filepath = os.path.join(dim_dir, f'{key}.json')
        with open(filepath, 'w') as f:
            json.dump({'dimension': name, 'value': key,
                        'count': len(items), 'items': items},
                       f, indent=2, ensure_ascii=False)
    return summary


def main():
    components = load_all()
    by_type, by_platform, by_system, by_module, by_tp = build_indices(
        components)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    type_summary = save_dimension('by-type', by_type, OUTPUT_DIR)
    platform_summary = save_dimension('by-platform', by_platform, OUTPUT_DIR)
    system_summary = save_dimension('by-system', by_system, OUTPUT_DIR)
    module_summary = save_dimension('by-module', by_module, OUTPUT_DIR)
    tp_summary = save_dimension('by-type-platform', by_tp, OUTPUT_DIR)

    index = {
        'generatedAt': datetime.now().isoformat(),
        'totalComponents': len(components),
        'dimensions': {
            'uiType': {
                'description': 'UI 组件类型（button, icon, input...）',
                'values': dict(sorted(type_summary.items(),
                                       key=lambda x: x[1], reverse=True)),
            },
            'platform': {
                'description': '目标平台（mobile, web, shared）',
                'values': platform_summary,
            },
            'system': {
                'description': '设计体系来源（DesignOps, APB, Handover）',
                'values': system_summary,
            },
            'businessModule': {
                'description': '业务模块（payment, kyc, merchant...）',
                'values': dict(sorted(module_summary.items(),
                                       key=lambda x: x[1], reverse=True)),
            },
            'typePlatform': {
                'description': '类型 × 平台交叉索引',
                'values': dict(sorted(tp_summary.items(),
                                       key=lambda x: x[1], reverse=True)),
            },
        }
    }

    with open(OUTPUT_INDEX, 'w') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f'✅ 多维度分类索引构建完成')
    print(f'   总组件: {len(components)}')
    print(f'   UI 类型: {len(type_summary)} 种')
    print(f'   平台: {len(platform_summary)} 种')
    print(f'   体系: {len(system_summary)} 种')
    print(f'   业务模块: {len(module_summary)} 种')
    print(f'   类型×平台: {len(tp_summary)} 种组合')
    print(f'\n   按 UI 类型 Top 10:')
    for cat, count in sorted(type_summary.items(),
                               key=lambda x: x[1], reverse=True)[:10]:
        print(f'     {cat}: {count}')
    print(f'\n   按业务模块:')
    for mod, count in sorted(module_summary.items(),
                               key=lambda x: x[1], reverse=True):
        print(f'     {mod}: {count}')


if __name__ == '__main__':
    main()
