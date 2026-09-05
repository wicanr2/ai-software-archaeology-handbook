"""檢查 PDF 結構、可抽取文字、來源與頁面邊界，並產生逐頁縮圖供目視複核。"""
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
import fitz
from PIL import Image, ImageDraw
import tinyhtml5


def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC",s)).replace("\u00ad", "")


def verify(out):
    reports=[]
    qa=out/"qa"
    qa.mkdir(exist_ok=True)
    for pdf in sorted((out/"release").glob("*.pdf")):
        lang=re.search(r"handbook-(.+)-v\.",pdf.name)[1]
        doc=fitz.open(pdf)
        errors=[]
        font_xrefs={font[0] for page in doc for font in page.get_fonts()}
        for xref in font_xrefs:
            if not doc.extract_font(xref)[3]: errors.append(f"字型未嵌入：{xref}")
        text=[]
        thumbnails=[]
        for i,page in enumerate(doc):
            body=page.get_text(clip=fitz.Rect(0,45,page.rect.width,790))
            text.append(body)
            if len(body.strip())<25: errors.append(f"第 {i+1} 頁疑似空白")
            if "\ufffd" in body or "\x00" in body: errors.append(f"第 {i+1} 頁含無效文字")
            for block in page.get_text("dict")["blocks"]:
                if block["type"]!=0: continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        x0,y0,x1,y1=span["bbox"]
                        if x0<35 or x1>page.rect.width-35 or y0<15 or y1>page.rect.height-15:
                            errors.append(f"第 {i+1} 頁文字越界：{span['text'][:60]}")
            for link in page.get_links():
                if link["kind"] in (fitz.LINK_GOTO,fitz.LINK_NAMED) and not (0<=link.get("page",-1)<len(doc)):
                    errors.append(f"第 {i+1} 頁內部連結無效")
            pix=page.get_pixmap(matrix=fitz.Matrix(0.45,0.45),alpha=False)
            thumb=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
            tile=Image.new("RGB",(290,410),"#dde5ec")
            tile.paste(thumb,((290-thumb.width)//2,8))
            ImageDraw.Draw(tile).text((12,390),f"{lang} | {i+1} / {len(doc)}",fill="#142e4a")
            thumbnails.append(tile)
        combined=norm("\n".join(text))
        for required in ("SPEC-ACC-v1","CONFIRMED","STRONG_INFERENCE","HYPOTHESIS","UNKNOWN","invalid_length","B08"):
            if norm(required) not in combined: errors.append(f"必要文字缺失：{required}")
        htmlpath=out/"render"/f"handbook-{lang}.html"
        root=tinyhtml5.parse(htmlpath.read_text())
        ns="{http://www.w3.org/1999/xhtml}"
        candidates=[]
        for elem in root.iter():
            if elem.tag in {ns+x for x in ("p","td","th","h2","h3","pre")}:
                value=norm("".join(elem.itertext()))
                if len(value)>4: candidates.append(value)
        missing=[value for value in candidates if value not in combined]
        # 跨頁段落可能被重複表頭或頁首切開；另外保存所有未逐段命中的內容供複核。
        (qa/f"text-review-{lang}.json").write_text(json.dumps(missing,ensure_ascii=False,indent=2))
        toc=[x for x in doc.get_toc() if x[0]==1]
        if len(toc)!=13: errors.append(f"一級書籤應有 13 個（含目錄），實際 {len(toc)}")
        toc_links={x.get("nameddest",str(x.get("page"))):x for x in doc[1].get_links() if x["kind"] in (fitz.LINK_GOTO,fitz.LINK_NAMED)}
        if len(toc_links)!=12: errors.append(f"目錄應有 12 個章節連結，實際 {len(toc_links)}")
        for destination,link in toc_links.items():
            actual=link["page"]+1
            if actual not in [entry[2] for entry in toc[1:]]:
                errors.append(f"目錄目的地與章節書籤不符：{destination}")
            rect=link["from"]
            printed=re.findall(r"\d+",doc[1].get_text(clip=fitz.Rect(490,rect.y0,550,rect.y1)))
            if [str(actual)]!=printed: errors.append(f"目錄印刷頁碼不符：{destination}：{printed!r} / {actual}")
        if missing: errors.append(f"{len(missing)} 個文字區塊需要複核")
        for i in range(0,len(thumbnails),12):
            sheet=Image.new("RGB",(1160,1230),"white")
            for j,tile in enumerate(thumbnails[i:i+12]): sheet.paste(tile,((j%4)*290,(j//4)*410))
            sheet.save(qa/f"contact-{lang}-{i//12+1:02}.png")
        # 封面、流程圖所在頁、密集表格與附錄都可由下列全頁圖覆核。
        samples={0,1,2,len(doc)-1}
        samples.update(i for i,page in enumerate(doc) if page.get_images())
        for i in sorted(samples): doc[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(qa/f"page-{lang}-{i+1:03}.png")
        report={"file":pdf.name,"sha256":hashlib.sha256(pdf.read_bytes()).hexdigest(),"pages":len(doc),"bookmarks":len(doc.get_toc()),"top_level_bookmarks":toc,"toc_links":len(toc_links),"internal_links":sum(x["kind"] in (fitz.LINK_GOTO,fitz.LINK_NAMED) for p in doc for x in p.get_links()),"text_blocks_checked":len(candidates),"text_blocks_needing_review":len(missing),"errors":errors}
        reports.append(report)
        print(json.dumps(report,ensure_ascii=False),flush=True)
    if len(reports)!=3: raise ValueError("應有三語 PDF")
    (qa/"report.json").write_text(json.dumps(reports,ensure_ascii=False,indent=2)+"\n")
    if any(r["errors"] for r in reports): raise SystemExit(1)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    verify(p.parse_args().out)
