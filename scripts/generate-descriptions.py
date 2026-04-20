#!/usr/bin/env python3
"""为 ComponentSet 生成自然语言语义描述，供 RAG 检索使用"""
import json, os, re
from collections import defaultdict
from datetime import datetime

COMP_DIR = 'reports/extractions/components'
OUTPUT = 'catalog/component-descriptions.json'

CATEGORY_DESCRIPTIONS = {
    'button': '可点击的交互按钮，触发操作或导航',
    'icon': '图标元素，用于辅助文字说明或独立表意',
    'input': '文本输入框，用户在其中输入信息',
    'card': '卡片容器，承载一组相关内容',
    'navigation': '导航组件，帮助用户在页面间移动',
    'modal': '弹窗/浮层，覆盖在页面上方展示内容',
    'list': '列表/表格，展示多条同类数据',
    'badge': '标签/徽章，标记状态或分类',
    'avatar': '头像组件，展示用户或品牌标识',
    'toggle': '开关/选择控件，用于切换状态',
    'toast': '提示消息，临时展示操作反馈',
    'loading': '加载状态，表示内容正在获取中',
    'typography': '文字排版组件',
    'image': '图片/插图展示区域',
    'flag': '国家/地区旗帜标识',
    'voucher': '优惠券/促销卡片',
    'form': '表单控件，如下拉框、日期选择器',
    'progress': '进度指示器，展示流程进度',
    'divider': '分割线，分隔内容区域',
    'tooltip': '气泡提示，悬浮展示额外信息',
    'logo': '品牌标识/Logo',
    'gesture': '手势图标/插图，说明触屏操作',
    'screen': '完整页面/屏幕截图组件',
    'chart': '图表/数据可视化组件',
    'error-state': '错误/空状态展示',
    'payment-flow': '支付流程中的业务组件',
    'kyc-flow': '身份验证流程中的业务组件',
    'account': '账户/个人设置相关组件',
    'security': '安全/密码相关组件',
    'onboarding': '新手引导/注册流程组件',
    'empty-content': '空内容/占位组件',
}

CLASSIFY_RULES = [
    ('button', ['button', 'btn', 'cta', 'fab']),
    ('icon', ['icon', 'ic-', 'ic_', 'ic ']),
    ('input', ['input', 'text field', 'textfield', 'search bar',
                'textarea', 'otp']),
    ('card', ['card']),
    ('navigation', ['tab', 'nav', 'menu', 'sidebar', 'breadcrumb',
                     'pagination', 'header', 'footer', 'appbar',
                     'bottom bar', 'toolbar']),
    ('modal', ['modal', 'dialog', 'popup', 'bottom sheet', 'bottomsheet',
               'overlay', 'drawer', 'action sheet']),
    ('list', ['list', 'table', 'row', 'cell', 'grid']),
    ('badge', ['badge', 'tag', 'chip', 'label', 'status', 'pill']),
    ('avatar', ['avatar', 'profile pic']),
    ('toggle', ['toggle', 'switch', 'checkbox', 'radio', 'check box']),
    ('toast', ['toast', 'snackbar', 'notification', 'alert', 'banner',
               'notice']),
    ('loading', ['loading', 'spinner', 'skeleton', 'shimmer', 'loader']),
    ('logo', ['logo', 'brand', 'atome-logo']),
    ('kyc-flow', ['kyc', 'verification', 'selfie', 'liveness', 'ktp',
                   'nric', 'facial', 'biometric']),
    ('payment-flow', ['payment', 'pay', 'amount', 'checkout', 'receipt',
                       'withdrawal', 'withdraw', 'cash', 'top up',
                       'bank account', 'transfer', 'bills', 'biller']),
    ('gesture', ['hand', 'finger', 'gesture', 'swipe']),
    ('chart', ['chart', 'graph', 'pie', 'donut', 'analytics']),
    ('error-state', ['error', 'empty state', 'no result', 'failed',
                      'rejected']),
    ('screen', ['screen', '/sub.', '/sub ', 'scroll']),
    ('voucher', ['voucher', 'coupon', 'deal', 'promo', 'cashback']),
    ('form', ['form', 'dropdown', 'select', 'picker', 'filter']),
    ('image', ['image', 'photo', 'thumbnail', 'illustration']),
    ('typography', ['heading', 'title', 'text', 'paragraph', 'caption']),
]


def classify(name):
    n = name.lower()
    for cat, kws in CLASSIFY_RULES:
        if any(kw in n for kw in kws):
            return cat
    return 'uncategorized'


def describe_variant(variant_name):
    """从变体名提取属性描述"""
    parts = []
    for segment in variant_name.split(','):
        segment = segment.strip()
        if '=' in segment:
            key, val = segment.split('=', 1)
            key = key.strip().replace('Property ', 'P')
            parts.append(f'{key}={val.strip()}')
    return ', '.join(parts) if parts else variant_name


def generate_description(cs_name, category, variants, system, file_name,
                          platform):
    """为单个 ComponentSet 生成语义描述"""
    cat_desc = CATEGORY_DESCRIPTIONS.get(category, '设计组件')
    variant_props = set()
    for v in variants[:20]:
        for seg in v.split(','):
            seg = seg.strip()
            if '=' in seg:
                key = seg.split('=')[0].strip()
                if not key.startswith('Property'):
                    variant_props.add(key)

    props_str = '、'.join(sorted(variant_props)[:5]) if variant_props else '无'
    plat = {'mobile': '移动端', 'web': '网页端',
            'shared': '跨平台', 'unknown': ''}.get(platform, '')

    desc = (f'{cs_name} 是{plat}{cat_desc}，'
            f'来自 {system} 体系的 {file_name}。'
            f'共有 {len(variants)} 个变体')
    if variant_props:
        desc += f'，可配置属性包括 {props_str}'
    desc += '。'
    return desc


def main():
    comp_sets = defaultdict(lambda: {
        'name': '', 'variants': [], 'system': '', 'file': '',
        'platform': '', 'category': ''
    })

    for filename in sorted(os.listdir(COMP_DIR)):
        if not filename.endswith('.json'):
            continue
        with open(os.path.join(COMP_DIR, filename)) as f:
            data = json.load(f)

        system = data['system']
        file_name = data['fileName']
        fn = file_name.lower()
        platform = ('mobile' if 'mobile' in fn or 'app' in fn
                     else 'web' if 'web' in fn
                     else 'shared' if 'icon' in fn or 'illust' in fn
                     else 'unknown')

        for comp in data['components']:
            frame = comp.get('containing_frame', {}) or {}
            cs = (frame.get('containingComponentSet') or {})
            cs_name = cs.get('name', '')
            if not cs_name:
                continue
            key = f'{data["fileKey"]}::{cs.get("nodeId", "")}'
            entry = comp_sets[key]
            entry['name'] = cs_name
            entry['system'] = system
            entry['file'] = file_name
            entry['platform'] = platform
            entry['category'] = classify(cs_name)
            entry['variants'].append(comp['name'])

    descriptions = []
    for key, cs in sorted(comp_sets.items(), key=lambda x: x[1]['name']):
        desc = generate_description(
            cs['name'], cs['category'], cs['variants'],
            cs['system'], cs['file'], cs['platform'])
        descriptions.append({
            'componentSet': cs['name'],
            'category': cs['category'],
            'system': cs['system'],
            'file': cs['file'],
            'platform': cs['platform'],
            'variantCount': len(cs['variants']),
            'description': desc,
            'sampleVariants': cs['variants'][:5],
        })

    output = {
        'generatedAt': datetime.now().isoformat(),
        'totalComponentSets': len(descriptions),
        'descriptions': descriptions,
    }

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f'✅ 组件语义描述生成完成')
    print(f'   ComponentSet 数量: {len(descriptions)}')
    print(f'   输出: {OUTPUT}')
    for d in descriptions[:5]:
        print(f'\n   📝 {d["componentSet"]}:')
        print(f'      {d["description"]}')


if __name__ == '__main__':
    main()
