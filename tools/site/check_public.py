"""以無認證 HTTP 驗證正式網站及八個公開 Release 附件。"""
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from PIL import Image

ROOT = Path('/work')
OUT = Path('/out')
BASE = 'https://wicanr2.github.io/ai-software-archaeology-handbook/'
RELEASE = 'https://github.com/wicanr2/ai-software-archaeology-handbook/releases/download/v.1.0.0-20260905/'


def fetch(url, status=200):
    request = urllib.request.Request(url, headers={'User-Agent': 'osa-handbook-public-verification'})
    try:
        with urllib.request.urlopen(request, timeout=40) as response:
            actual, data = response.status, response.read()
    except urllib.error.HTTPError as error:
        actual, data = error.code, error.read()
    assert actual == status, (url, actual, status)
    return data


def sha(data):
    return hashlib.sha256(data).hexdigest()


assert OUT.is_dir() and OUT.stat().st_uid == os.getuid()
results = []
for relative in ['index.html', 'library.html', 'assets/reader.css', 'assets/site.css', 'assets/site.js', 'assets/favicon.svg', 'assets/social.png', 'robots.txt', 'sitemap.xml'] + [r['page'] for r in json.loads((ROOT/'docs/site-manifest.json').read_text())['pages']]:
    url = BASE + ('' if relative == 'index.html' else relative)
    data = fetch(url)
    assert data == (ROOT / 'docs' / relative).read_bytes(), ('網站與本機不符', relative)
    if relative == 'assets/social.png':
        assert Image.open(io.BytesIO(data)).size == (1200, 630)
    results.append({'url': url, 'bytes': len(data), 'sha256': sha(data)})
    print('匿名網站讀取通過：' + relative, flush=True)
missing = fetch(BASE + 'nonexistent-osa-verification-page', status=404)
assert '回到證據的起點' in missing.decode('utf-8')
local_release = ROOT / 'dist-all/v.1.0.0-20260905/release'
files = sorted(local_release.iterdir())
assert len(files) == 8
for path in files:
    data = fetch(RELEASE + path.name)
    assert sha(data) == sha(path.read_bytes()), ('附件雜湊不符', path.name)
    results.append({'url': RELEASE + path.name, 'bytes': len(data), 'sha256': sha(data)})
    print('匿名附件下載通過：' + path.name, flush=True)
(OUT / 'public-downloads.json').write_text(json.dumps({'authenticated': False, 'custom_404': True, 'results': results}, ensure_ascii=False, indent=2) + '\n')
