"""將既有三語手冊排版成 PDF；不修改正文、不執行任何案例軟體。"""
import argparse
import hashlib
import html
import json
import logging
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

from weasyprint import HTML
from diagrams import generate, LABELS

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "docs/handbook"
FILES = ["README.md", "00-principles.md", "01-evidence.md", "02-hypotheses.md", "03-specification-gates.md", "04-oracles.md", "05-differential-testing.md", "06-conformance.md", "07-agent-workflows.md", "08-failure-patterns.md", "worked-example.md"]
TEXT = {
    "zh-Hant": ["AI 輔助<br>軟體考古手冊", "以證據約束推論，以比較驗證實作。", "繁體中文版", "目錄", "閱讀指南", "固定來源索引", "九章方法 · 七個案例 · 一個完整演練", "歷史結果為原專案紀錄，非本書重新執行。合成案例不代表歷史軟體；本書不包含已實作的 osa 工具。", "來源文件與程式碼的固定版本；雜湊不代表原版 EXE 或 ROM。來源可能需要存取權限。", "路徑", "提交", "圖"],
    "en": ["AI-Assisted<br>Software Archaeology<br>Handbook", "Ground claims in evidence.<br>Validate implementations by comparison.", "English edition", "Contents", "Reading guide", "Fixed source registry", "Nine chapters · Seven cases · One worked example", "Historical results are reports by the source projects, not new runs for this book. The synthetic example is not historical software. The planned osa toolkit is not implemented here.", "Pinned source documents and code; hashes do not identify original executables or ROMs. Source access may require permission.", "Path", "Commit", "Figure"],
    "ja": ["AI 支援<br>ソフトウェア考古学<br>ハンドブック", "証拠で推論を支え、比較で実装を検証する。", "日本語版", "目次", "読書ガイド", "固定出典一覧", "九つの章 · 七つの事例 · 一つの演習", "過去の結果は元プロジェクトの記録であり、本書のための再実行ではありません。合成例は歴史的ソフトウェアではなく、osa ツールの実装も含みません。", "出典文書とコードの固定版です。ハッシュは原版 EXE や ROM のものではありません。出典の閲覧には権限が必要な場合があります。", "パス", "コミット", "図"],
}


def run(args, data=None):
    return subprocess.run(args, input=data, text=True, capture_output=True, check=True).stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(node):
    if isinstance(node, list): return "".join(plain(n) for n in node)
    if not isinstance(node, dict): return ""
    if node["t"] in ("Str", "Code"): return node["c"] if node["t"]=="Str" else node["c"][1]
    if node["t"] in ("Space", "SoftBreak", "LineBreak"): return " "
    return plain(node.get("c", []))


def walk(node, callback):
    if isinstance(node, dict):
        callback(node)
        for value in list(node.values()): walk(value, callback)
    elif isinstance(node,list):
        for value in node: walk(value,callback)


def figure(out, lang, kind, number):
    idx = {"lifecycle":0,"gates":1,"comparison":2}[kind]
    title = LABELS[lang]["titles"][idx]
    return {"t":"RawBlock", "c":["html",f'<figure><img src="{(out/"promo"/f"{kind}-{lang}.png").as_uri()}" alt="{html.escape(title)}"><figcaption>{TEXT[lang][11]} {number} · {html.escape(title)}</figcaption></figure>']}


def assemble(out, lang, version):
    t=TEXT[lang]
    folder = BOOK / ({"zh-Hant":"", "en":"en", "ja":"ja"}[lang])
    trees={name:json.loads(run(["pandoc","-f","gfm","-t","json",str(folder/name)])) for name in FILES}
    anchors={}
    titles={}
    for name, tree in trees.items():
        prefix = "guide" if name=="README.md" else "example" if name=="worked-example.md" else "c"+name[:2]
        def headers(node):
            if node.get("t")=="Header":
                level,attr,inlines=node["c"]
                old=attr[0]
                new=prefix if level==1 else prefix+"-"+old
                anchors[(name,old)]=new
                attr[0]=new
                if level==1:
                    anchors[(name,"")]=new
                    if name=="README.md": node["c"][2]=[{"t":"Str","c":t[4]}]
                    titles[name]=plain(node["c"][2])
        walk(tree,headers)
    sections=[]
    for name, tree in trees.items():
        blocks=tree["blocks"]
        # 每章第一段是網頁導覽；紙本以統一目錄及頁碼取代。
        assert blocks[0]["t"]=="Header" and blocks[1]["t"]=="Para", name
        del blocks[1]
        if name=="README.md":
            first_table=next(i for i,b in enumerate(blocks) if b["t"]=="Table")
            assert blocks[first_table-1]["t"]=="Header"
            del blocks[first_table-1:first_table+1]
        replaced=[]
        inserted=False
        for block in blocks:
            if block["t"]=="CodeBlock" and "mermaid" in block["c"][0][1]:
                replaced.append(figure(out,lang,"lifecycle",1)); continue
            replaced.append(block)
            if block["t"]=="Table" and not inserted and name[:2] in ("03","05"):
                replaced.append(figure(out,lang,"gates" if name[:2]=="03" else "comparison",2 if name[:2]=="03" else 3))
                inserted=True
        tree["blocks"]=replaced
        # 各章末尾固定的來源與範圍註記採緊湊、不可拆散的編輯註樣式。
        if name!="README.md":
            last_heading=max(i for i,b in enumerate(tree["blocks"]) if b["t"]=="Header")
            tree["blocks"].insert(last_heading,{"t":"RawBlock","c":["html",'<aside class="sources-note">']})
            tree["blocks"].append({"t":"RawBlock","c":["html","</aside>"]})
        def links(node):
            if node.get("t")!="Link": return
            target=node["c"][2][0]
            if re.match(r"^[a-zA-Z]+:",target): return
            path,_,fragment=target.partition("#")
            resolved=(folder/(unquote(path) or name)).resolve()
            if resolved.parent==folder.resolve() and resolved.name in trees:
                key=(resolved.name,unquote(fragment))
                if key not in anchors: raise ValueError(f"未知 PDF 錨點：{name}: {target}")
                node["c"][2][0]="#"+anchors[key]
            elif resolved==ROOT/"docs/inventory.md": node["c"][2][0]="#sources"
            else:
                relative=resolved.relative_to(ROOT).as_posix()
                node["c"][2][0]=f"https://github.com/wicanr2/ai-software-archaeology-handbook/blob/{version}/{relative}"+("#"+fragment if fragment else "")
        walk(tree,links)
        body=run(["pandoc","-f","json","-t","html5","--wrap=none"],json.dumps(tree))
        sections.append(f'<section class="chapter chapter-{anchors[(name, "")]}">{body}</section>')
    source_rows=re.findall(r"\| ([MSFWOTP]\d) \| \[([^]]+)\]\((https://github.com/[^)]+)\)(.*?) \| `([a-f0-9]{64})` \|",(ROOT/"docs/inventory.md").read_text())
    assert len(source_rows)==20
    cards=[]
    for sid,label,url,locator,sha in source_rows:
        repo,commit,path=re.match(r"https://github.com/(.+?)/blob/([a-f0-9]{40})/(.+)",url).groups()
        cards.append(f'<div class="source" id="source-{sid}"><h2>{sid} · <a href="{url}">{html.escape(repo)}</a></h2><p>{t[9]}: <code>{html.escape(path)}</code></p><p>{t[10]}: <code>{commit}</code><br>SHA-256: <code>{sha}</code></p><p>{html.escape(label+locator)}</p></div>')
    toc="".join(f'<a href="#{anchors[(n,"")]}">{html.escape(titles[n])}</a>' for n in FILES)+f'<a href="#sources">{t[5]}</a>'
    cover=f'<div class="cover"><div class="eyebrow">ORACLE-DRIVEN SOFTWARE ARCHAEOLOGY</div><h1>{t[0]}</h1><div class="subtitle">{t[1]}</div><div class="accent"></div><p>{t[6]}</p><div class="meta"><p class="edition">{version}</p><p>{t[2]} · 2026-09-05</p><p>wicanr2 / ai-software-archaeology-handbook</p></div></div>'
    css=(ROOT/"tools/pdf/book.css").read_text().replace("RELEASE_VERSION",version)
    document=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{html.escape(t[0].replace("<br>"," "))}</title><meta name="author" content="wicanr2"><meta name="dcterms.created" content="2026-09-05T00:00:00Z"><style>{css}</style></head><body>{cover}<section class="toc"><h1>{t[3]}</h1>{toc}<p class="scope">{t[7]}</p></section>{"".join(sections)}<section class="chapter"><h1 id="sources">{t[5]}</h1><p>{t[8]}</p>{"".join(cards)}</section></body></html>'
    html_path=out/"render"/f"handbook-{lang}.html"
    html_path.write_text(document)
    pdf=out/"release"/f"osa-handbook-{lang}-{version}.pdf"
    HTML(string=document,base_url=str(ROOT)).write_pdf(pdf,pdf_identifier=hashlib.sha256(document.encode()).digest())
    return pdf


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--version",required=True)
    p.add_argument("--source-commit",required=True)
    p.add_argument("--image-id",required=True)
    args=p.parse_args()
    if not re.fullmatch(r"v\.\d+\.\d+\.\d+-\d{8}",args.version): p.error("版號必須使用 v.主.次.修訂-YYYYMMDD")
    if not re.fullmatch(r"[a-f0-9]{40}",args.source_commit): p.error("必須提供完整來源提交")
    out=args.out.resolve()
    if not out.is_dir() or out.stat().st_uid!=os.getuid(): p.error("輸出目錄不存在或擁有權不符")
    for item in out.rglob("*"):
        if item.stat().st_uid!=os.getuid(): p.error(f"擁有權不符：{item}")
        if item.name!=".keep": p.error("請使用乾淨的明確輸出目錄")
    for folder in ("release","promo","render"): (out/folder).mkdir()
    logging.basicConfig(level=logging.WARNING)
    for lang in TEXT:
        generate(out/"promo",lang)
        pdf=assemble(out,lang,args.version)
        print(f"完成 {pdf.name}",flush=True)
    inputs=sorted(set(BOOK.rglob("*.md"))|set((ROOT/"tools/pdf").glob("*"))|{ROOT/"docs/inventory.md"})
    manifest={"version":args.version,"source_commit":args.source_commit,"image_id":args.image_id,"visibility":"private","scope":"手冊排版與流程圖；未重跑原版，未實作 osa 工具。","inputs":{str(p.relative_to(ROOT)):digest(p) for p in inputs if p.is_file()},"tools":{"pandoc":run(["pandoc","--version"]).splitlines()[0],"python_packages":Path("/opt/python-packages.txt").read_text(),"debian_packages":Path("/opt/debian-packages.txt").read_text()},"outputs":{str(p.relative_to(out)):digest(p) for p in sorted(out.rglob("*")) if p.is_file() and p.suffix in (".pdf",".svg",".png")}}
    (out/"release"/f"manifest-{args.version}.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")


if __name__=="__main__": main()
