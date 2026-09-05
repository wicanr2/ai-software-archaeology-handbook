"""逐頁檢查完整 Markdown 覆蓋、站內檔案與跨頁錨點。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib
ROOT=Path('/work'); DOCS=ROOT/'docs'
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.ids=[];self.links=[];self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag in ('a','img','link','script'):
            value=a.get('href',a.get('src'))
            if value:self.links.append(value)
pages={p:Page(p) for p in DOCS.rglob('*.html')}
manifest=json.loads((DOCS/'site-manifest.json').read_text())['pages']
assert {r['source'] for r in manifest}=={str(p.relative_to(ROOT)) for p in list(DOCS.rglob('*.md'))+list(ROOT.glob('*.md'))}
for record in manifest:
    assert hashlib.sha256((ROOT/record['source']).read_bytes()).hexdigest()==record['sha256']
    assert DOCS/record['page'] in pages
errors=[];count=0
for path,page in pages.items():
    if len(page.ids)!=len(set(page.ids)):errors.append((str(path),'duplicate IDs'))
    for link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:
            if '/wicanr2/ai-software-archaeology-handbook/blob/' in link and u.path.endswith('.md'):errors.append((str(path),link))
            continue
        target=(DOCS/u.path.removeprefix('/ai-software-archaeology-handbook/')) if u.path.startswith('/') else (path.parent/unquote(u.path)).resolve() if u.path else path
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append((str(path),link,'missing file'))
        elif target.suffix=='.md':errors.append((str(path),link,'raw Markdown'))
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append((str(path),link,'missing anchor'))
        count+=1
assert not errors,json.dumps(errors,ensure_ascii=False,indent=2)
print(f'{len(manifest)} 份 Markdown 全覆蓋；{len(pages)} 個 HTML、{count} 個站內連結與錨點通過。')
