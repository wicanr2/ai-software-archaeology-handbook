# PDF 排版與發行

本入口說明三語手冊的 PDF 交付、重建方法與驗收邊界；不啟動 PLAN 的 `osa` 工具階段。

## 正式入口與附件

[v.1.0.0-20260905](https://github.com/wicanr2/ai-software-archaeology-handbook/releases/tag/v.1.0.0-20260905)
提供繁體中文、英文、日文三份獨立 PDF，以及推廣圖壓縮包、來源／工具版本清單、
自動驗收紀錄、字型授權告知及 SHA-256。儲存庫與 Release 維持私人；下載者需要相應存取權。
本次沒有改成公開儲存庫，也沒有替來源專案或本書新增公開散布授權。

PDF 使用 A4 白底、深藍標題與青綠重點色，含可點選目錄、章節書籤、頁碼及二十筆固定來源。
圖一呈現證據到符合性的循環與反例回路；圖二呈現規格閘門；圖三區分差分結果，避免將缺失當通過。
三圖各有三語 SVG 原稿與二倍 PNG；封面另存 PNG，方便製作介紹材料。
正文仍以三語 Markdown 為準；排版只移除網頁導覽與重複目錄，不變更技術結論。

本機交付根目錄為 `dist-all/<版本>/`：`release/` 是發行附件，`promo/` 是推廣素材；
`render/` 與 `qa/` 保存可重建 HTML、逐頁縮圖與目視抽查圖。這些產物不加入 Git。
手冊不是遊戲重製封包，不含原版 EXE、ROM、商業素材或案例儲存庫的完整快照。

## 隔離工具鏈

既有 `report-docx:20260901` 只具 DOCX 能力；既有 Pandoc、LibreOffice 與其他文件映像
未同時具備此工作所需的固定排版器、三語字型及 PDF 結構驗收。因此新增專案專用
`osa-handbook-pdf:20260905`，不取代其他專案的映像。

- 基底：Dockerfile 固定 Python 3.12 slim 的映像摘要。
- 系統套件：Debian `20260901T000000Z` 快照，含 Pandoc、Noto CJK、Pango、librsvg、Poppler。
- Python 套件：`tools/pdf/requirements.txt` 完整鎖版；WeasyPrint 66.0 排版，PyMuPDF 1.26.4 驗收。
- 來源與輸出逐檔 SHA-256、實際套件版本及映像 ID 記錄在附件 manifest；不只依賴映像標籤。
- Python 僅用於 PDF 工具鏈與既有文件驗收，不是改變 PLAN 中 Go 工具的語言決策。

必要的建置網路只在建立映像時使用；文件排版、驗收與封裝一律離線。

```sh
timeout 600s docker build --memory 2g --cpu-quota 200000 \
  -t osa-handbook-pdf:20260905 -f tools/pdf/Dockerfile .
```

正式重建先 checkout 該 tag，確認 `git status --porcelain` 為空，並以 `git rev-parse HEAD`
取得來源提交、`docker image inspect` 取得實際映像 ID。建立一個目前 UID/GID 擁有的全新輸出目錄；
不要刪除或覆寫已發布附件。以下將 `/明確的新輸出目錄` 及兩個識別碼替換成實際值：

```sh
timeout 300s docker run --rm --name osa-pdf-build --label project=osa-handbook-pdf \
  --network none --memory 3g --cpus 2 --pids-limit 128 \
  -u "$(id -u):$(id -g)" \
  -v "$PWD:/work:ro" -v /明確的新輸出目錄:/out \
  osa-handbook-pdf:20260905 sh -c '
    python tools/check_handbook.py &&
    python tools/pdf/build.py --out /out --version v.1.0.0-20260905 \
      --source-commit 完整提交 --image-id sha256:實際映像識別碼 &&
    python tools/pdf/verify.py --out /out &&
    python tools/pdf/package.py --out /out --version v.1.0.0-20260905
  '
```

建置器在寫入前檢查輸出目錄及既有檔案擁有權，拒絕非空目錄（僅容許 `.keep`）。
來源唯讀；完成後再次抽查產物 UID/GID，以 `docker ps -a --filter label=project=osa-handbook-pdf`
確認沒有殘留容器。保留現行映像，不清理其他專案的容器或懸空映像。

## 驗收與限制

自動檢查包含三份 PDF、非空頁、文字邊界、必要術語、正文與表格區塊抽取、
章節書籤、具名目的地、十二個目錄目的頁及印刷頁碼；全部逐頁產生縮圖。
逐段文字核對涵蓋原始段落、表格、標題與程式區塊，不以檔案存在代替完成。
流程圖文字位於圖片，另目視核對三語原稿及 PDF 內的實際呈現。
PDF 的三組圖為高解析 PNG，向量 SVG 保留在推廣包；正文仍可搜尋、選取及複製。

歷史執行結果仍是來源專案的報告，不是這次 PDF 工作重新驗證；工具鏈與文件驗收
不構成原版相容性證明。尚未由真人讀者跨所有 PDF 閱讀器試讀，亦未實體印刷驗色。
固定來源可能位於私人儲存庫，PDF 內保存版本與雜湊不等於替讀者取得其存取權。

細部執行歷程與實際發行回讀追加至 [WORKLOG.md](../WORKLOG.md)。
