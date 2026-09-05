# 宣傳網站與公開交付

## 已確認的方向

專案負責人指定以「王俊又 wicanr2 進入 AI 時代的貢獻」建立 GitHub Pages，並明確授權
網站完成後把本儲存庫轉為公開。經兩份可撤回的首屏預覽，使用者回答 `yes`，確認：

- 採用「三語手冊＋七個案例」呈現可追溯的貢獻，使用深色、橘色重點與大字版面。
- 不擴充為完整個人作品集，不補造個人生涯、外部影響力、使用人數或原版相容性紀錄。
- 署名為王俊又（wicanr2）；透過人與 AI 協作完成案例整理、手冊、翻譯與交付。
- 網站完成驗收後公開本儲存庫；不變更另外七個案例儲存庫的設定。

正式網址：[王俊又 wicanr2｜讓 AI 的實作經得起驗證](https://wicanr2.github.io/ai-software-archaeology-handbook/)。
網站為繁體中文宣傳入口，連結既有三語手冊與 PDF；不將入口的單一語言誤稱為全站三語翻譯。

## 設計參考與權利

參考使用者指定的 `open-kimi-ppt-skill`，本機版本固定於
[`28040e1f57dbb4002f79afb597c4640f18b828c2`](https://github.com/Binaryify/open-kimi-ppt-skill/tree/28040e1f57dbb4002f79afb597c4640f18b828c2)。
閱讀其技能、通用視覺與品牌展示指引，並比較兩張範例截圖；沿用「清楚的讀者任務、
大字階層、留白、逐頁視覺複核」的工作方式，重新撰寫本網站的 HTML、CSS 與圖形。

上游專案自述為非官方 Kimi Slides 工具，採 MIT 授權。本網站沒有複製其編輯器程式、
範例品牌圖片、產品素材或字型，也未將手冊傳送到 Kimi 編輯器。不存在官方合作或背書聲明。
本次輸出是使用者指定的網站，不執行上游的 PPTD／PPTX 匯出流程。

網站使用系統字型、專案自行製作的 SVG／PNG；無第三方字型下載、追蹤碼或外部前端套件。
公開閱讀不等於另行授予第三方素材的使用權；本次沒有替專案新增軟體或內容授權條款。

## 部署與重建

GitHub Pages 使用 `main` 分支的 `/docs` 目錄；`docs/.nojekyll` 指示直接發佈靜態檔案。
主要檔案為 `docs/index.html`、`docs/assets/site.css`、`docs/assets/site.js`；
另有分享圖、網站圖示、404 頁、搜尋引擎網站地圖及爬蟲入口。
採用 GitHub 的[分支發佈方式](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)，不新增 Node 建置或套件安裝流程。

分享圖原稿為 `docs/assets/social.svg`，以既有 `osa-handbook-pdf:20260905` 容器內的
`rsvg-convert -w 1200 -h 630` 生成 `social.png`。來源圖與文字可直接編輯，PNG 供社群平台使用。

瀏覽器驗收沿用 `ghcr.io/puppeteer/puppeteer:23.11.1`，映像 ID 為
`sha256:6a74444753c00dd2420b241d13d653fff9762b31033d6f7f3eb94fc059fb55ca`。
此映像在目前 UID 下須明確指定原有快取 `PUPPETEER_CACHE_DIR=/home/pptruser/.cache/puppeteer`；
不掛入主機 runtime，也不另建重複瀏覽器映像。

建立目前 UID/GID 擁有的明確輸出目錄後，在專案根目錄執行（替換實際輸出路徑）：

```sh
timeout 120s docker run --rm --label project=osa-pages \
  --network none --memory 2g --cpus 2 --pids-limit 192 \
  -u "$(id -u):$(id -g)" \
  -e PUPPETEER_CACHE_DIR=/home/pptruser/.cache/puppeteer \
  -v "$PWD:/work:ro" -v /明確驗收目錄:/out \
  ghcr.io/puppeteer/puppeteer:23.11.1 node /work/tools/site/check.cjs
```

正式站重驗使用相同命令，僅將網路改為 `--network bridge` 並加上
`-e SITE_URL=https://wicanr2.github.io/ai-software-archaeology-handbook/`。
原始碼仍唯讀；輸出僅限指定目錄。每批工作後以 `docker ps -a --filter label=project=osa-pages`
檢查是否有殘留容器。

## 公開前檢查與證據界線

前輪已檢查全部七個可達提交的物件類型及常見憑證格式，未發現命中；歷史內容均為文件或文字腳本，
沒有原版遊戲二進位檔。這是有界的檢查，不宣稱通用機密偵測器已證明不存在任何敏感資料。
轉公開會一併公開既有 Git 作者信箱、本機路徑、研究文件與工作歷程；已向使用者說明，沒有重寫歷史。

2026-09-05 以 GitHub API 回讀七個案例儲存庫，當時全部為公開；這不保證未來可見性永遠不變。
主張仍連到手冊中的固定提交與二十筆來源，不因來源目前可見而提升證據等級。

既有 `v.1.0.0-20260905` 的 tag 與附件保持不變。PDF 發行說明與 manifest 中的私人狀態
記錄的是首次產生／發布時的事實；儲存庫之後公開，不回寫附件或移動 tag。
目前可見性、Pages 部署與驗收回讀另追加到 [WORKLOG.md](../WORKLOG.md)。

## 全站文件閱讀

使用者進一步要求所有頁面都留在網站內閱讀。`tools/site/build.py` 使用既有
`osa-handbook-pdf:20260905` 中的 Pandoc，將根目錄與 `docs/` 的全部 45 份 Markdown
完整轉成 HTML，不只製作摘要。三語章節共 33 頁，另含研究、來源、發行與專案文件。
網站提供章節導覽、本頁目錄、對應語言切換與 `library.html` 全部文件入口。
本儲存庫 Markdown 連結改為站內 HTML；外部案例與附件仍保留原始來源。

重建時掛載專案為 `/work:ro`、`docs/` 為 `/site`，在上述容器內執行
`python /work/tools/site/build.py`；沿用相同 UID/GID、資源限制與無網路設定。
向量流程圖沿用 `tools/pdf/diagrams.py` 的三語輸出，保留原始 Mermaid 定義供查核。
`tools/site/check_pages.py` 核對來源雜湊、全部文件覆蓋、檔案連結、重複 ID 與跨頁錨點；
瀏覽器驗收另逐頁檢查手機寬度。發布前先更新文件、重建、檢查，再一併提交產生的 HTML。
這是出版工具，不代表第 2 階段 `osa` 參考工具已實作。
