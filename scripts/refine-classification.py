#!/usr/bin/env python3
"""细化 'other' 分类 — 将 2,150 个未分类组件重新归类"""
import json, os, re
from collections import defaultdict
from datetime import datetime

COMP_DIR = 'reports/extractions/components'
OUTPUT = 'catalog/classified-index.json'
CLASSIFIED_DIR = 'catalog/classified'

REFINED_RULES = [
    ('button', ['button', 'btn', 'cta', 'fab']),
    ('icon', ['icon', 'ic-', 'ic_', 'ic ']),
    ('input', ['input', 'text field', 'textfield', 'search bar',
                'textarea', 'otp', 'pin input']),
    ('card', ['card']),
    ('navigation', ['tab', 'nav', 'menu', 'sidebar', 'breadcrumb',
                     'pagination', 'header', 'footer', 'appbar',
                     'bottom bar', 'toolbar', 'top bar', 'back button']),
    ('modal', ['modal', 'dialog', 'popup', 'bottom sheet', 'bottomsheet',
               'overlay', 'drawer', 'action sheet']),
    ('list', ['list', 'table', 'row', 'cell', 'grid']),
    ('badge', ['badge', 'tag', 'chip', 'label', 'status', 'pill']),
    ('avatar', ['avatar', 'profile pic']),
    ('toggle', ['toggle', 'switch', 'checkbox', 'radio', 'check box']),
    ('toast', ['toast', 'snackbar', 'notification', 'alert', 'banner',
               'notice']),
    ('loading', ['loading', 'spinner', 'skeleton', 'shimmer',
                  'loader', 'progress bar']),
    ('typography', ['heading', 'title', 'text block', 'paragraph',
                     'caption', 'font', 'typography']),
    ('image', ['image', 'photo', 'thumbnail', 'illustration']),
    ('flag', ['flag', 'country flag']),
    ('voucher', ['voucher', 'coupon', 'deal', 'promo', 'cashback']),
    ('form', ['form', 'dropdown', 'select', 'picker', 'date picker',
               'slider', 'stepper', 'filter']),
    ('progress', ['progress', 'step indicator']),
    ('divider', ['divider', 'separator']),
    ('tooltip', ['tooltip', 'popover', 'hint']),
    ('logo', ['logo', 'brand', 'atome-logo']),
    # —— 以下是新增的细分类（业务流程优先于通用 screen）——
    ('kyc-flow', ['kyc', 'verification', 'identity', 'selfie', 'liveness',
                   'ktp', 'nric', 'facial', 'biometric', 'document scan']),
    ('payment-flow', ['payment', 'pay', 'amount', 'checkout', 'receipt',
                       'withdrawal', 'withdraw', 'cash', 'top up', 'topup',
                       'bank account', 'transfer', 'send money', 'bills',
                       'biller', 'atomepay']),
    ('gesture', ['hand', 'finger', 'onefinger', 'twofinger', 'threefinger',
                  'fourfinger', 'fivefinger', 'gesture', 'swipe', 'pinch',
                  'tap', 'drag']),
    ('chart', ['chart', 'graph', 'pie', 'bar chart', 'line chart',
                'donut', 'analytics', 'statistics']),
    ('error-state', ['error', 'empty state', 'no result', 'no data',
                      'failed', 'something went wrong', 'can\'t connect',
                      'rejected']),
    ('onboarding', ['onboarding', 'welcome', 'intro', 'get started',
                     'sign up', 'register', 'a new way']),
    ('screen', ['screen', 'page', 'scroll', '/sub.', '/sub ',
                 'transaction/sub', 'access/sub']),
    ('account', ['account', 'profile', 'setting', 'my page', 'personal',
                  'edit profile']),
    ('security', ['pin', 'password', 'otp', 'lock', 'unlock',
                   'authenticate', 'secure']),
    ('empty-content', ['empty', 'placeholder', 'no content',
                        'coming soon']),
]


def classify_v2(name, page_name='', frame_name=''):
    """增强版分类：先精确匹配，再模糊匹配"""
    combined = f'{name} {page_name}'.lower()
    for category, keywords in REFINED_RULES:
        if any(kw in combined for kw in keywords):
            return category
    return 'uncategorized'


def load_and_reclassify():
    """重新加载全量组件并用增强规则分类"""
    components = []
    for filename in sorted(os.listdir(COMP_DIR)):
        if not filename.endswith('.json'):
            continue
        with open(os.path.join(COMP_DIR, filename)) as f:
            data = json.load(f)

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
                'system': data['system'],
                'file': data['fileName'],
                'platform': detect_platform(data['fileName']),
                'page': page_name,
                'frame': frame_name,
                'uiType': classify_v2(display_name, page_name, frame_name),
            })
    return components


def detect_platform(file_name):
    """平台检测"""
    n = file_name.lower()
    if 'mobile' in n or 'app' in n:
        return 'mobile'
    if 'web' in n:
        return 'web'
    if 'icon' in n or 'illustration' in n:
        return 'shared'
    return 'unknown'


def save_index(components):
    """保存分类索引"""
    by_type = defaultdict(int)
    for comp in components:
        by_type[comp['uiType']] += 1

    os.makedirs(CLASSIFIED_DIR, exist_ok=True)
    by_type_items = defaultdict(list)
    for comp in components:
        by_type_items[comp['uiType']].append({
            'name': comp['displayName'],
            'system': comp['system'],
            'file': comp['file'],
            'platform': comp['platform'],
        })

    for ui_type, items in by_type_items.items():
        type_dir = os.path.join(CLASSIFIED_DIR, 'by-type')
        os.makedirs(type_dir, exist_ok=True)
        with open(os.path.join(type_dir, f'{ui_type}.json'), 'w') as f:
            json.dump({'dimension': 'uiType', 'value': ui_type,
                        'count': len(items), 'items': items},
                       f, indent=2, ensure_ascii=False)

    index = {
        'generatedAt': datetime.now().isoformat(),
        'version': 'v2-refined',
        'totalComponents': len(components),
        'uiTypeDistribution': dict(sorted(by_type.items(),
                                            key=lambda x: x[1], reverse=True)),
        'improvements': {}
    }
    with open(OUTPUT, 'w') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    return by_type


def main():
    components = load_and_reclassify()
    by_type = save_index(components)

    v1_other = 2150
    v2_uncategorized = by_type.get('uncategorized', 0)
    reclassified = v1_other - v2_uncategorized

    print(f'✅ 分类细化完成 (v2)')
    print(f'   总组件: {len(components)}')
    print(f'   v1 "other": {v1_other}')
    print(f'   v2 "uncategorized": {v2_uncategorized}')
    print(f'   成功重新归类: {reclassified} '
          f'({reclassified * 100 / v1_other:.1f}%)')
    print(f'\n   分类分布:')
    for cat, count in sorted(by_type.items(),
                               key=lambda x: x[1], reverse=True):
        marker = ' ← NEW' if cat in (
            'gesture', 'screen', 'chart', 'error-state',
            'payment-flow', 'kyc-flow', 'account', 'security',
            'onboarding', 'empty-content'
        ) else ''
        print(f'     {cat}: {count}{marker}')


if __name__ == '__main__':
    main()
