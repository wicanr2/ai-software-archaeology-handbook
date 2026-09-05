"""唯讀檢查手冊結構、來源引用及三語演練；不是相容性測試或翻譯認證。"""

from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "docs" / "handbook"
LANGUAGES = {"繁體中文": BOOK, "英文": BOOK / "en", "日文": BOOK / "ja"}
CHAPTERS = [
    "00-principles.md", "01-evidence.md", "02-hypotheses.md",
    "03-specification-gates.md", "04-oracles.md", "05-differential-testing.md",
    "06-conformance.md", "07-agent-workflows.md", "08-failure-patterns.md",
]
PAGES = CHAPTERS + ["README.md", "worked-example.md"]
ERRORS = []


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def prose(text):
    """只移除 fenced code，避免把程式示例當成本機連結或標題。"""
    return re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)


def heading_ids(text):
    """本書所用簡單 ATX 標題的 GitHub 錨點；不宣稱通用 Markdown 解析器。"""
    ids, counts = set(), {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", prose(text), re.M):
        title = title.replace("`", "").lower()
        slug = "".join(
            c if c in "_-" or unicodedata.category(c)[0] in "LNM" else
            "-" if c.isspace() else "" for c in title
        )
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        ids.add(slug + (f"-{count}" if count else ""))
    return ids


def source_ids(text):
    return set(re.findall(r"(?<![A-Za-z0-9])([MSFWOTP][1-9][0-9]*)(?![A-Za-z0-9])", text))


def table_widths(text, label):
    width = None
    for number, line in enumerate(prose(text).splitlines(), 1):
        if line.startswith("|") and line.endswith("|"):
            current = len(re.split(r"(?<!\\)\|", line)) - 2
            if width is None:
                width = current
            require(current == width, f"表格欄數不一致：{label}，處理後第 {number} 行")
        else:
            width = None


def example_rows(text):
    return re.findall(
        r"^\| ([AB]\d+) \| `([0-9A-F ]+)` \| (\d+) \| (\d+) \| `([a-z_]+)` \|",
        text, re.M,
    )


def check_example(text, label):
    rows = example_rows(text)
    require([row[0] for row in rows] == ["A01"] + [f"B{i:02d}" for i in range(1, 9)],
            f"演練檢查點不完整：{label}")
    previous = 250
    for point, request, before, after, result in rows:
        before, after = int(before), int(after)
        raw = bytes.fromhex(request)
        require(before == (10 if point == "A01" else previous), f"狀態不連續：{label}/{point}")
        if len(raw) != 2:
            expected, code = before, "invalid_length"
        elif raw[0] == 1:
            expected, code = min(255, before + raw[1]), "ok"
        elif raw[0] == 2 and raw[1] == 0:
            expected, code = 0, "ok"
        elif raw[0] == 2:
            expected, code = before, "invalid_operand"
        else:
            expected, code = before, "unknown_operation"
        require((after, result) == (expected, code), f"演練推導錯誤：{label}/{point}")
        if point.startswith("B"):
            previous = after
    return rows


def main():
    plan = (ROOT / "PLAN.md").read_text()
    planned = set(re.findall(r"docs/handbook/([0-9]{2}-[^`\s]+\.md)", plan))
    require(planned == set(CHAPTERS), "章節清單與 PLAN 不一致")
    inventory = (ROOT / "docs" / "inventory.md").read_text()
    registry = set(re.findall(r"^\| ([MSFWOTP]\d+) \|", inventory, re.M))
    require(len(registry) == 20, "固定來源索引不是二十筆")
    book_texts = {}
    for language, directory in LANGUAGES.items():
        require({p.name for p in directory.glob("*.md")} == set(PAGES), f"頁面清單不完整：{language}")
        for name in PAGES:
            path = directory / name
            if not path.exists():
                continue
            text = path.read_text()
            book_texts[(language, name)] = text
            require(len(re.findall(r"^# ", text, re.M)) == 1, f"主標題數量：{path}")
            require(text.count("```") % 2 == 0, f"程式圍欄未閉合：{path}")
            require(not re.search(r"\b(?:TODO|TBD|FIXME|lorem ipsum)\b", text, re.I), f"仍有佔位內容：{path}")
            require(source_ids(text) <= registry, f"未登錄來源 ID：{path}: {source_ids(text) - registry}")
            table_widths(text, f"{language}/{name}")

    # 檢查儲存庫文件的實際目的檔與本書使用的簡單標題錨點，不請求遠端網站。
    docs = list((ROOT / "docs").rglob("*.md")) + [ROOT / p for p in ("README.md", "AGENTS.md", "PLAN.md", "WORKLOG.md")]
    links = 0
    for path in docs:
        text = path.read_text()
        for target in re.findall(r"\]\(([^)\s]+)\)", prose(text)):
            if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            destination, _, fragment = unquote(target).partition("#")
            resolved = (path.parent / destination).resolve() if destination else path
            require(resolved.exists(), f"連結不存在：{path.relative_to(ROOT)} → {target}")
            if resolved.is_file() and fragment and resolved.suffix == ".md":
                require(fragment in heading_ids(resolved.read_text()), f"錨點不存在：{path.relative_to(ROOT)} → {target}")
            links += 1

    for name in CHAPTERS + ["worked-example.md"]:
        original = book_texts.get(("繁體中文", name), "")
        tokens = set(re.findall(r"\b(?:CONFIRMED|STRONG_INFERENCE|HYPOTHESIS|UNKNOWN|DRAFT|READY|CONFORMED)\b", original))
        for language in ("英文", "日文"):
            translated = book_texts.get((language, name), "")
            require(source_ids(original) == source_ids(translated), f"三語來源 ID 不一致：{language}/{name}")
            found = set(re.findall(r"\b(?:CONFIRMED|STRONG_INFERENCE|HYPOTHESIS|UNKNOWN|DRAFT|READY|CONFORMED)\b", translated))
            require(tokens == found, f"三語狀態詞不一致：{language}/{name}")

    examples = {language: check_example(book_texts.get((language, "worked-example.md"), ""), language)
                for language in LANGUAGES}
    require(examples["繁體中文"] == examples["英文"] == examples["日文"], "三語演練資料不一致")
    for error in ERRORS:
        print(f"錯誤：{error}")
    print(f"手冊頁面 {len(book_texts)}/33；本機連結 {links}；來源 ID {len(registry)}；三語演練各 9 個檢查點；錯誤 {len(ERRORS)}")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
