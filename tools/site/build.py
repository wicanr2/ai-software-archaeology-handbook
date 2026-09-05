"""以既有 Pandoc 工具鏈產生完整靜態閱讀網站；不改寫 Markdown 來源。"""
from pathlib import Path
import os, re, json, subprocess, hashlib, unicodedata
from html import escape as e
from urllib.parse import urlsplit, unquote

ROOT = Path('/work')
OUT = Path('/site')
BASE = 'https://wicanr2.github.io/ai-software-archaeology-handbook/'
REPO = 'https://github.com/wicanr2/ai-software-archaeology-handbook/'
sources = sorted(list((ROOT/'docs').rglob('*.md')) + list(ROOT.glob('*.md')))
mapping = {p: (p.relative_to(ROOT/'docs').with_suffix('.html') if p.is_relative_to(ROOT/'docs') else Path('project')/p.with_suffix('.html').name) for p in sources}
titles = {p: re.search(r'^# (.+)$', p.read_text(), re.M)[1].replace('`','') for p in sources}

def href(current, target):
    return os.path.relpath(target, current.parent)

def link(current, target, label):
    return f'<a href="{e(href(current,target),quote=True)}">{e(label)}</a>'

def shell(path, title, body, nav='', lang='zh-Hant'):
    home = link(path,Path('index.html'),'王俊又 wicanr2')
    library = link(path,Path('library.html'),'全部文件 · All pages · 全ページ')
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}｜AI 軟體考古</title><link rel="canonical" href="{BASE}{path.as_posix()}"><link rel="stylesheet" href="{href(path,Path('assets/reader.css'))}"><link rel="icon" href="{href(path,Path('assets/favicon.svg'))}"></head><body><a class="skip" href="#content">{'Skip to content' if lang=='en' else '本文へ' if lang=='ja' else '跳至內文'}</a><header>{home}<nav>{library}</nav></header><div class="layout">{nav}<main id="content">{body}</main></div><footer>{home} · AI 輔助軟體考古手冊 · {library}<p>證據先行，保留未知。 Evidence first. Keep uncertainty visible.</p></footer></body></html>'''

def write(path, text):
    dest = OUT/path
    parent = dest.parent
    while not parent.exists(): parent=parent.parent
    assert parent.stat().st_uid == os.getuid(), parent
    if dest.exists(): assert dest.stat().st_uid == os.getuid(), dest
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(text)
    assert dest.stat().st_uid == os.getuid()

records=[]
for source,path in mapping.items():
    raw=source.read_text()
    ast=json.loads(subprocess.check_output(['pandoc','-f','gfm','-t','json'],input=raw.encode()))
    counts={}; headings=[]
    raw_titles=iter(re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$',re.sub(r'^```[^\n]*\n.*?^```\s*$','',raw,flags=re.M|re.S),re.M))
    lang='ja' if '/handbook/ja/' in str(source) else 'en' if '/handbook/en/' in str(source) else 'zh-Hant'
    def walk(node):
        if isinstance(node,list):
            for x in node: walk(x)
        elif isinstance(node,dict):
            t=node.get('t'); c=node.get('c')
            if t=='Header':
                title=next(raw_titles).replace('`','')
                slug=''.join(ch if ch in '_-' or unicodedata.category(ch)[0] in 'LNM' else '-' if ch.isspace() else '' for ch in title.lower())
                n=counts.get(slug,0);counts[slug]=n+1
                slug+=f'-{n}' if n else ''
                c[1][0]=slug
                if c[0] in (2,3): headings.append((slug,title,c[0]))
            elif t in ('Link','Image'):
                url=c[2][0]; parsed=urlsplit(url); target=None
                if not parsed.scheme and parsed.path:
                    target=(source.parent/unquote(parsed.path)).resolve()
                elif url.startswith(REPO+'blob/'):
                    pieces=unquote(parsed.path).split('/',5)
                    if len(pieces)==6: target=(ROOT/pieces[5]).resolve()
                if target in mapping:
                    c[2][0]=href(path,mapping[target])+('?' + parsed.query if parsed.query else '')+('#'+parsed.fragment if parsed.fragment else '')
                elif target and not parsed.scheme:
                    if target.is_relative_to(ROOT/'docs') and target.exists(): c[2][0]=href(path,target.relative_to(ROOT/'docs'))+('#'+parsed.fragment if parsed.fragment else '')
                    else: c[2][0]=REPO+'blob/main/'+str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else url
            walk(c)
    walk(ast['blocks'])
    body=subprocess.check_output(['pandoc','-f','json','-t','html5','--wrap=none'],input=json.dumps(ast).encode()).decode()
    body=body.replace('<table>','<div class="table-scroll" tabindex="0"><table>').replace('</table>','</table></div>')
    # 原始流程定義保留於可展開區；圖片是同一套已驗收的三語向量圖。
    body=re.sub(r'(<pre class="mermaid">.*?</pre>)',lambda m:f'<figure><img src="{href(path,Path("assets/diagrams")/f"lifecycle-{lang}.svg")}" alt="{e(titles[source])} — Evidence → Hypothesis → Specification → Oracle → Implementation → Differential Validation → Conformance"></figure><details><summary>Mermaid · 原始流程定義</summary>{m[1]}</details>',body,flags=re.S)
    book=ROOT/'docs/handbook'/({'en':'en','ja':'ja'}.get(lang,''))
    chapters=sorted(book.glob('*.md'),key=lambda p: ('0' if p.name=='README.md' else '1')+p.name)
    navigation=''.join('<li'+(' class="current"' if p==source else '')+'>'+link(path,mapping[p],titles[p])+'</li>' for p in chapters)
    extra=''.join('<li>'+link(path,mapping[p],titles[p])+'</li>' for p in sources if 'handbook' not in p.parts)
    nav=f'<aside><details open><summary>{"Chapters" if lang=="en" else "章一覧" if lang=="ja" else "章節導覽"}</summary><nav><ul>{navigation}</ul></nav></details><details><summary>研究與專案文件</summary><nav><ul>{extra}</ul></nav></details></aside>'
    switches=[]
    if 'handbook' in source.parts:
        for code,label in [('zh-Hant','繁體中文'),('en','English'),('ja','日本語')]:
            other=ROOT/'docs/handbook'/({'en':'en','ja':'ja'}.get(code,''))/source.name
            switches.append(link(path,mapping[other],label))
    toc='<details class="toc"><summary>'+('On this page' if lang=='en' else 'このページの内容' if lang=='ja' else '本頁目錄')+'</summary><ul>'+''.join(f'<li class="depth-{level}"><a href="#{e(slug)}">{e(title)}</a></li>' for slug,title,level in headings)+'</ul></details>'
    write(path,shell(path,titles[source],'<div class="languages">'+' · '.join(switches)+'</div>'+toc+'<article>'+body+'</article>',nav,lang))
    records.append({'source':str(source.relative_to(ROOT)),'page':str(path),'sha256':hashlib.sha256(raw.encode()).hexdigest()})

path=Path('library.html')
body='<h1>全部文件</h1><p>三語手冊、完整演練、來源證據與專案說明，都在同一網站內閱讀。</p>'
for directory,label in [('docs/handbook','繁體中文'),('docs/handbook/en','English'),('docs/handbook/ja','日本語'),('docs','研究、來源與發行'),('.','專案說明與工作歷程'),('docs/releases','發行紀錄')]:
    body+='<section><h2>'+label+'</h2><ul>'+''.join('<li>'+link(path,mapping[p],titles[p])+'</li>' for p in sources if p.parent==ROOT/directory)+'</ul></section>'
write(path,shell(path,'全部文件',body))
# 宣傳首頁仍由人工維護；只機械轉換指向本儲存庫文件的連結。
landing=(OUT/'index.html').read_text()
for source,path in mapping.items():
    landing=landing.replace(REPO+'blob/main/'+str(source.relative_to(ROOT)),path.as_posix())
if 'href="library.html"' not in landing:
    landing=landing.replace('</footer>','<p><a href="library.html">全部文件：手冊、研究與專案說明</a></p></footer>')
write(Path('index.html'),landing)
write(Path('site-manifest.json'),json.dumps({'pages':records},ensure_ascii=False,indent=2)+'\n')
write(Path('sitemap.xml'),'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in ['','library.html']+[r['page'] for r in records])+'</urlset>\n')
print(f'已產生 {len(records)} 份完整文件內頁與文件總覽。')
