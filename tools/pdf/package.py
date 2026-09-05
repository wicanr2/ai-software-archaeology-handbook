"""將已驗收的 PDF 與推廣圖打包，產生附件清單及 SHA-256。"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import fitz


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main(out,version):
    release=out/"release"
    report=json.loads((out/"qa/report.json").read_text())
    if len(report)!=3 or any(r["errors"] for r in report): raise ValueError("PDF 未通過驗收")
    for r in report:
        if sha(release/r["file"])!=r["sha256"]: raise ValueError("驗收後 PDF 已改變")
        lang=r["file"].split("handbook-",1)[1].split("-v.",1)[0]
        with fitz.open(release/r["file"]) as doc:
            doc[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(out/"promo"/f"cover-{lang}.png")
    (release/f"validation-{version}.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    notices=[]
    for package in ("fonts-noto-cjk","fonts-dejavu-core"):
        notices.append(package+"\n\n"+(Path("/usr/share/doc")/package/"copyright").read_text())
    (release/f"font-notices-{version}.txt").write_text("\n\n".join(notices))
    (out/"promo"/"README.txt").write_text("三語推廣圖／流程圖\n\ncover：封面 PNG。lifecycle、gates、comparison：三組流程圖，各有繁體中文、英文、日文的 SVG 原稿與 2000 像素 PNG。\nSVG 字型為 Noto Sans CJK TC／JP；PNG 不需另外安裝字型。\n用途是說明本手冊的方法，不代表原版軟體驗證結果。\n來源：https://github.com/wicanr2/ai-software-archaeology-handbook\n儲存庫維持私人；此附件不新增公開授權或來源專案素材的散布權。\n版本："+version+"\n")
    archive=release/f"osa-handbook-promo-{version}.zip"
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in sorted((out/"promo").iterdir()):
            info=zipfile.ZipInfo(path.name,date_time=(2026,9,5,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,path.read_bytes())
    manifest_path=release/f"manifest-{version}.json"
    manifest=json.loads(manifest_path.read_text())
    manifest["outputs"]={str(p.relative_to(out)):sha(p) for folder in (release,out/"promo") for p in sorted(folder.iterdir()) if p.is_file() and p!=manifest_path and not p.name.startswith("SHA256SUMS")}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    checksum=release/f"SHA256SUMS-{version}.txt"
    checksum.write_text("".join(f"{sha(p)}  {p.name}\n" for p in sorted(release.iterdir()) if p.is_file() and p!=checksum))
    print("附件：",*[p.name for p in sorted(release.iterdir())],sep="\n")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--version",required=True)
    args=p.parse_args()
    main(args.out,args.version)
