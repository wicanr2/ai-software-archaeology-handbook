"""三語流程圖：保留向量原稿，另輸出二倍 PNG 供 PDF 使用。"""
from html import escape
from pathlib import Path
import subprocess

LABELS = {
    "zh-Hant": {
        "titles": ["從證據到符合性", "規格閘門：何時可以實作", "差分驗證：缺失不等於通過"],
        "stages": [("證據", "原始觀測與來源"), ("假說", "可區分的候選解釋"), ("規格", "輸入、狀態與驗收"), ("行為基準", "固定條件的參考觀測"), ("實作", "僅限 READY 範圍"), ("差分驗證", "逐項比較與覆蓋"), ("符合性", "限定版本與聲明範圍")],
        "loop": "矛盾或證據缺口 → 重開受影響的證據與規格",
        "legend": "實線：工作推進　　虛線：帶著反例回查；不是自動升級信心",
        "gate": ["蒐證與隔離原型", "範圍內正式實作", "引用有範圍的結果"],
        "reviews": ["證據審查", "必要比較通過"],
        "note": "規格狀態 ≠ 主張信心；新證據或版本變更須重審受影響範圍。",
        "compare": ["參考觀測", "候選觀測", "固定版本、起始狀態與輸入", "對齊檢查點、時點與欄位", "依預先審查的契約比較", "精確相符／容許差異", "分開報告範圍與容差", "不相符", "保存第一個分歧", "缺失／不可比較／略過", "必要項不得計為通過"],
    },
    "en": {
        "titles": ["From evidence to conformance", "Specification gates: permission to implement", "Differential validation: missing is not passing"],
        "stages": [("Evidence", "Raw records + provenance"), ("Hypothesis", "Competing predictions"), ("Specification", "Inputs, state, acceptance"), ("Oracle", "Fixed reference capture"), ("Implementation", "READY scope only"), ("Differential validation", "Fields + coverage"), ("Conformance", "Version + bounded claim")],
        "loop": "Contradiction or evidence gap → reopen affected evidence and specification",
        "legend": "Solid: work advances. Dashed: investigate a counterexample, not a confidence promotion.",
        "gate": ["Evidence + isolated prototypes", "Implement within scope", "Cite the bounded result"],
        "reviews": ["Evidence review", "Required checks pass"],
        "note": "Specification state ≠ claim confidence. New evidence or versions require scoped review.",
        "compare": ["Reference capture", "Candidate capture", "Fixed version, initial state and inputs", "Align checkpoints, timing and fields", "Compare under the reviewed contract", "Exact / tolerated", "Report scope and tolerance", "Mismatch", "Keep the first divergence", "Missing / unknown / skipped", "Required items are not passed"],
    },
    "ja": {
        "titles": ["証拠から適合性へ", "仕様のゲート：実装を始める条件", "差分検証：欠測は合格ではない"],
        "stages": [("証拠", "生の観測と来歴"), ("仮説", "区別できる候補の予測"), ("仕様", "入力・状態・受入条件"), ("判定基準", "条件を固定した参照観測"), ("実装", "READY の範囲のみ"), ("差分検証", "項目別の比較と網羅範囲"), ("適合性", "版と声明の範囲を限定")],
        "loop": "矛盾や証拠の不足 → 影響する証拠と仕様を再調査",
        "legend": "実線：作業の進行　破線：反例をもとに再調査。確信度の自動昇格ではない。",
        "gate": ["証拠収集と隔離した試作", "範囲内の正式実装", "範囲を限定した結果の引用"],
        "reviews": ["証拠の審査", "必須の比較に合格"],
        "note": "仕様の状態 ≠ 主張の確信度。新しい証拠や版は影響範囲の再審査を要する。",
        "compare": ["参照の観測", "候補の観測", "版・初期状態・入力を固定", "検査点・時点・項目を整合", "審査済みの契約に従って比較", "厳密な一致／許容差", "範囲と許容差を別々に報告", "不一致", "最初の分岐を保存", "欠測／比較不能／スキップ", "必須項目は合格に数えない"],
    },
}


class Diagram:
    def __init__(self, title, height, lang):
        self.height = height
        font = "Noto Sans CJK JP" if lang == "ja" else "Noto Sans CJK TC"
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(title)} — {escape(LABELS[lang]["legend"])}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#397880" stroke-width="1.5"/></marker></defs><rect width="1000" height="{height}" fill="white"/><g font-family="{font},sans-serif">']
        self.text(28, 42, title, 29, "#142e4a", weight=700)
        self.parts.append('<path d="M28 61 H972" stroke="#0d9488" stroke-width="3"/>')

    def text(self, x, y, value, size=20, color="#344b60", weight=400, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>')

    def card(self, x, y, w, h, title, subtitle, number=None, dark=False):
        fill, ink = ("#142e4a", "#ffffff") if dark else ("#edf6f7", "#142e4a")
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#b6d7da"/>')
        if number:
            self.text(x+16, y+27, number, 16, "#86c9c4" if dark else "#217c77", 700)
        self.text(x+w/2, y+h/2+2, title, 17 if len(title)>20 else 23, ink, 700, "middle")
        self.text(x+w/2, y+h/2+34, subtitle, 16, ink, anchor="middle")

    def arrow(self, path, dashed=False):
        self.parts.append(f'<path d="{path}" fill="none" stroke="#397880" stroke-width="2.5" marker-end="url(#arrow)"'+(' stroke-dasharray="8 6"' if dashed else '')+'/>')

    def save(self, path):
        path.write_text("".join(self.parts)+"</g></svg>", encoding="utf-8")
        subprocess.run(["rsvg-convert", "-w", "2000", "-h", str(self.height*2), "-o", str(path.with_suffix(".png")), str(path)], check=True)


def generate(out: Path, lang: str):
    labels = LABELS[lang]
    out.mkdir(parents=True, exist_ok=True)
    d = Diagram(labels["titles"][0], 520, lang)
    coords = [(28,105),(273,105),(518,105),(763,105),(763,275),(518,275),(273,275)]
    for i, ((x,y), (title, sub)) in enumerate(zip(coords,labels["stages"])):
        d.card(x,y,209,125,title,sub,f"0{i+1}",i==6)
    for x in (237,482,727): d.arrow(f"M{x} 165 H{x+30}")
    d.arrow("M867 230 V266")
    d.arrow("M763 335 H736")
    d.arrow("M518 335 H491")
    d.arrow("M622 400 V425 H90 V242", True)
    d.text(125,459,labels["loop"],20)
    d.text(28,497,labels["legend"],17)
    d.save(out/f"lifecycle-{lang}.svg")
    d = Diagram(labels["titles"][1], 350, lang)
    for i,state in enumerate(("DRAFT","READY","CONFORMED")):
        d.card(28+i*345,125,254,120,state,labels["gate"][i],dark=i==2)
    for i in range(2):
        d.arrow(f"M{282+i*345} 180 H{365+i*345}")
        d.text(326+i*345,103,labels["reviews"][i],17,anchor="middle")
    d.text(28,305,labels["note"],19)
    d.save(out/f"gates-{lang}.svg")
    c=labels["compare"]
    d=Diagram(labels["titles"][2],465,lang)
    d.card(28,82,420,85,c[0],c[2]); d.card(552,82,420,85,c[1],c[2])
    d.arrow("M238 167 V187 H430 V206"); d.arrow("M762 167 V187 H570 V206")
    d.card(210,215,580,80,c[3],c[4])
    for i in range(3):
        x=28+i*330
        d.arrow(f"M500 295 V317 H{x+142} V336")
        d.card(x,345,284,90,c[5+i*2],c[6+i*2],dark=i==2)
    d.save(out/f"comparison-{lang}.svg")
