"""Figma REST API 通用模块 — 统一重试、缓存、限流管理"""
import json, os, subprocess, time, hashlib
from pathlib import Path

CACHE_DIR = Path('reports/.api-cache')
MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 8]


def get_token():
    """从环境变量或 .env 文件加载 Token"""
    token = os.environ.get('FIGMA_TOKEN')
    if token:
        return token
    env_file = Path('.env')
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith('FIGMA_TOKEN='):
                return line.split('=', 1)[1].strip()
    raise RuntimeError('FIGMA_TOKEN 未设置，请配置 .env 或环境变量')


def _cache_key(url):
    """生成缓存文件名"""
    return CACHE_DIR / f'{hashlib.md5(url.encode()).hexdigest()}.json'


def fetch_json(url, use_cache=False, cache_ttl=3600):
    """
    调用 Figma REST API，支持重试和缓存。
    use_cache: 启用缓存
    cache_ttl: 缓存有效期（秒）
    """
    if use_cache:
        cache_file = _cache_key(url)
        if cache_file.exists():
            age = time.time() - cache_file.stat().st_mtime
            if age < cache_ttl:
                return json.loads(cache_file.read_text())

    token = get_token()
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            result = subprocess.run(
                ['curl', '-s', '--max-time', '30',
                 '-H', f'X-Figma-Token: {token}', url],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f'curl 失败: {result.stderr}')

            data = json.loads(result.stdout)

            if data.get('status') == 429:
                wait = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
                print(f'  ⏳ 限流，等待 {wait}s...')
                time.sleep(wait)
                continue

            if data.get('err'):
                raise RuntimeError(f'API 错误: {data["err"]}')

            if use_cache:
                CACHE_DIR.mkdir(parents=True, exist_ok=True)
                _cache_key(url).write_text(json.dumps(data))

            return data

        except (json.JSONDecodeError, RuntimeError) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_DELAYS[attempt]
                print(f'  ⚠️ 重试 {attempt + 1}/{MAX_RETRIES} '
                      f'(等待 {wait}s): {e}')
                time.sleep(wait)

    raise RuntimeError(
        f'API 调用失败（已重试 {MAX_RETRIES} 次）: {last_error}'
    )


def fetch_file_meta(file_key):
    """获取文件元数据（带缓存，1小时有效）"""
    url = f'https://api.figma.com/v1/files/{file_key}?depth=1'
    return fetch_json(url, use_cache=True, cache_ttl=3600)


def fetch_components(file_key):
    """获取文件的全量已发布组件"""
    url = f'https://api.figma.com/v1/files/{file_key}/components'
    return fetch_json(url, use_cache=True, cache_ttl=3600)


def fetch_styles(file_key):
    """获取文件的全量已发布样式"""
    url = f'https://api.figma.com/v1/files/{file_key}/styles'
    return fetch_json(url, use_cache=True, cache_ttl=3600)


def fetch_images(file_key, node_ids, fmt='png', scale=2):
    """批量获取节点截图 URL（不缓存）"""
    ids_param = ','.join(node_ids)
    url = (f'https://api.figma.com/v1/images/{file_key}'
           f'?ids={ids_param}&format={fmt}&scale={scale}')
    return fetch_json(url, use_cache=False)
