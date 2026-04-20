#!/usr/bin/env python3
"""将 design-tokens.json 转换为 W3C Design Token Community Group 标准格式"""
import json, os, re
from datetime import datetime

INPUT = 'catalog/tokens/design-tokens.json'
OUTPUT = 'catalog/tokens/w3c-design-tokens.json'


def hex_to_srgb(hex_val, opacity=1.0):
    """将 #RRGGBB 转为 W3C sRGB 格式"""
    h = hex_val.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'#{h.lower()}{int(opacity * 255):02x}' if opacity < 1 else f'#{h.lower()}'


def normalize_name(name):
    """将 Style 名转为 Token 路径: 'greyscale/dark 1 #141C30' → 'greyscale.dark-1'"""
    name = re.sub(r'#[0-9a-fA-F]{6}', '', name).strip()
    name = re.sub(r'\s+', '-', name)
    name = name.replace('/', '.').lower()
    return re.sub(r'-+', '-', name).strip('-')


def convert_colors(colors):
    """转换颜色 Token 到 W3C 格式"""
    groups = {}
    for name, data in colors.items():
        token_path = normalize_name(name)
        parts = token_path.split('.')
        current = groups
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = {
            '$type': 'color',
            '$value': hex_to_srgb(data['value'], data.get('opacity', 1.0)),
            '$description': f'Source: {data.get("source", "unknown")}',
        }
    return groups


def convert_typography(typography):
    """转换字体 Token 到 W3C 格式"""
    groups = {}
    for name, data in typography.items():
        token_path = normalize_name(name)
        parts = token_path.split('.')
        current = groups
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = {
            '$type': 'typography',
            '$value': {
                'fontFamily': data.get('fontFamily', 'sans-serif'),
                'fontSize': f'{data.get("fontSize", 14)}px',
                'fontWeight': data.get('fontWeight', 400),
                'lineHeight': f'{data.get("lineHeight", 1.5)}',
                'letterSpacing': f'{data.get("letterSpacing", 0)}px',
            },
            '$description': f'Source: {data.get("source", "unknown")}',
        }
    return groups


def convert_effects(effects):
    """转换效果 Token 到 W3C 格式"""
    result = {}
    for name, data in effects.items():
        token_name = normalize_name(name)
        result[token_name] = {
            '$type': 'shadow',
            '$value': {
                'color': data.get('color', 'rgba(0,0,0,0.1)'),
                'offsetX': f'{data.get("offset", {}).get("x", 0)}px',
                'offsetY': f'{data.get("offset", {}).get("y", 4)}px',
                'blur': f'{data.get("radius", 8)}px',
                'spread': f'{data.get("spread", 0)}px',
            },
            '$description': f'Source: {data.get("source", "unknown")}',
        }
    return result


def main():
    with open(INPUT) as f:
        data = json.load(f)

    w3c_tokens = {
        '$schema': 'https://design-tokens.github.io/community-group/format/',
        '$metadata': {
            'name': 'Atome Design Tokens',
            'generatedAt': datetime.now().isoformat(),
            'source': 'Figma Asset Library',
            'totalColors': len(data.get('colors', {})),
            'totalTypography': len(data.get('typography', {})),
            'totalEffects': len(data.get('effects', {})),
        },
        'color': convert_colors(data.get('colors', {})),
        'typography': convert_typography(data.get('typography', {})),
        'shadow': convert_effects(data.get('effects', {})),
    }

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        json.dump(w3c_tokens, f, indent=2, ensure_ascii=False)

    c = len(data.get('colors', {}))
    t = len(data.get('typography', {}))
    e = len(data.get('effects', {}))
    print(f'✅ W3C Design Token 格式导出完成')
    print(f'   颜色: {c} | 字体: {t} | 效果: {e}')
    print(f'   输出: {OUTPUT}')


if __name__ == '__main__':
    main()
