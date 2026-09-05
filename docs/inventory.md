# 案例盤點與證據索引

## 目前狀態

| 日期 | 授權階段 | 現有程式 | 本輪驗證範圍 | 交付與下一閘門 |
|---|---|---|---|---|
| 2026-09-05 | 第 0、1 階段及 PDF 已交付；後續確認宣傳網站與儲存庫公開 | 無 `osa` 工具實作；文件工具與靜態宣傳網站 | 三語文件／PDF 驗收；網站四種寬度、導覽及無 JavaScript 閱讀；未重跑原版 | [宣傳網站](https://wicanr2.github.io/ai-software-archaeology-handbook/)、[三語手冊](handbook/README.md)、[PDF](pdf-release.md)；儲存庫已公開，第 2–7 階段不在本次交付範圍 |

這張表是專案的唯一目前狀態表。一般作業歷程另見 [WORKLOG.md](../WORKLOG.md)。
手冊先完成並審讀繁體中文，再擴充英文與日文；以下案例盤點保留第 0 階段的取證邊界。

## 方法與信心邊界

七個案例均在本機找到，以唯讀掛載檢查 Git 遠端、提交及受追蹤檔案狀態；
盤點時七者的受追蹤檔案均無修改。本輪引用以 `git show <完整提交>:<路徑>`
的內容為準，不引用未提交檔案，也不把歷史工作清單當成新的授權。

最終核對時 Parhelion 的 HEAD 已前進至
`ced79d239bd13c3ab3ac2dc03f49b3c60f0897a3`。本輪仍引用下列最初固定的
`106313a99f93bd97dc25a4b49b47b487445968bc`，二十筆雜湊均已直接對 Git 物件驗證，
不把工作期間的新版本混進同一批案例。

工具為 Docker 中的 Git 2.49.1（`alpine/git:2.49.1`），文件雜湊由同一容器的
`sha256sum` 計算。來源表的雜湊識別的是文件／程式碼，不是原版 EXE 或 ROM。
可用下列命令在同樣唯讀掛載的容器內回查；`CASE` 是容器內的案例目錄：

```sh
git -C "$CASE" show "$COMMIT:$FILE"
git -C "$CASE" show "$COMMIT:$FILE" | sha256sum
```

信心必須限定主詞：

- `CONFIRMED`：本輪直接核對的提交、文件內容、程式分支，以及「來源確有記錄某次勘誤」。
- `STRONG_INFERENCE`：由多個已核對來源萃取的可重用工程規則；不是已證實普遍有效。
- `HYPOTHESIS`：尚待後續實作或獨立研究驗證的方法建議。
- `UNKNOWN`：本輪未重新驗證的原版行為、執行結果與未抽樣的能力。

下列案例摘要中的歷史結果均為來源作者的報告，沒有升格成本輪動態驗證。
這次不是反組譯證據匯出，不轉錄原版指令、原版資產或跨工具位址表。
要把案例中的遊戲語意升格為本專案的 `CONFIRMED`，仍須另核對原版輸入雜湊、
工具版本、位址空間及原始觀測；文件雜湊不能取代這些資料。

## 七個案例

### MM2

- 儲存庫：`wicanr2/mm2_cht`；本機 `/home/anr2/cht/mm2`。
- 提交：`d887651741b6f236973b48f756157a24c3bbcad5`。
- 目的：以 DOS 原版為基準的《魔法門 II》重製與繁體中文化。
- 原始證據與保存：格式筆記、原版按鍵時間線、截圖／記憶體傾印入口、現況文件中的勘誤表（M1–M3）。
- 流程與假說：資料解碼、讀寫端追查、原版動態觀察互相訂正；保留推翻原因。
- 行為基準（oracle）：DOSBox 中的原版與固定起始狀態；跨平台資料另外處理。
- 驗證：離屏測試、封包啟動與實際畫面是不同層。M1 記錄文字在最後顯示轉接處被清掉，內部測試未涵蓋。
- 機器可讀觀測：M3 指向記憶體傾印與固定輸入序列；本輪未重新擷取。
- 可重用實踐：驗證最後一段使用者路徑；負向格式檢查；新鮮起始狀態。
- 專案限定：DOS、MSX 等平台素材及地圖語意不能相互套用。
- 限制：M2 §4 仍寫舊的文字位移／單字字典解釋，M1「已被推翻的斷言」已撤回；該段不得當現行規格。

### 春之石

- 儲存庫：`wicanr2/shard_of_spring_cht`；本機 `/home/anr2/cht/shard_of_spring`。
- 提交：`0e00fea38d370aa4223fc21421442a6ceef64bed`。
- 目的：DOS《Shard of Spring》的規則重建與繁體中文重製。
- 原始證據與保存：依問題編號的逆向筆記、指令片段、資料欄位與存取統計、CONTEXT 勘誤索引（S1–S3）。
- 流程與假說：從資料分布提出候選，再追查實際讀寫及傷害／死亡路徑；新證據可撤回「已確認」。
- 行為基準：DOSBox 原版觀察與原版程式資料流；兩者覆蓋不同問題。
- 驗證：搜尋過濾器需要正對照；判別測試必須能分開競爭假說。
- 機器可讀觀測：S2 記錄修正掃描腳本及呼叫計數；本輪只讀歷史輸出與程式片段。
- 失敗：助憶碼過濾漏計呼叫；用單調遞增把錯誤欄位認成生命值。
- 可重用實踐：撤回也要證據；確定一個欄位不等於順便確定其他欄位。
- 專案限定與限制：BASIC 執行期中斷形式是此工具鏈線索；S3 的經驗值解釋當時仍缺結算端，不能改標已證實。

### 炎龍騎士團 2

- 儲存庫：`wicanr2/fd2_re`；本機 `/home/anr2/cht/fd2`。
- 提交：`420daf9a81d563a5eb2bc49adcdafba3ca9f3a7f`。
- 目的：DOS 原版資料、演出、戰鬥與玩家流程重建。
- 原始證據與保存：F1 將問題路由到 IDA 資料、覆蓋矩陣、介面證據與歷史反思；F2 保存連拍方法及勘誤。
- 流程與假說：分開靜態資產、原版演出與現行實作；歷史交接不覆蓋現況。
- 行為基準：DOSBox 實跑畫面及原版 handler 證據；攻略與影片需標出能裁決的範圍。
- 驗證：靜態主選單圖不能證明整段開場；擷取是否從真正起點開始需要獨立核對。
- 機器可讀觀測：F1 指向 `docs/data/ida/` 及 `docs/data/fd2_*`；F2 指向編號畫格。本輪未逐份驗證那些資料。
- 失敗：以局部靜態合成否定 logo 縮放；擷取起點曾被誤認；無音訊路徑時無法裁決音樂同步。
- 可重用實踐：以問題路由減少過期結論；連續事件用完整時間線查證。
- 專案限定與限制：F1 的 E0／E2 等證據分層不可直接等同本手冊四級信心；未全面稽核遊戲完成度。

### WinCV

- 儲存庫：`wicanr2/wincv-remake`；本機 `/home/anr2/cht/wincv`。
- 提交：`b2d8b43f4f4f8e6eca1bf6099a2fafbf108da31a`。
- 目的：WinCV 0.52 檔案瀏覽工具的跨平台重寫，包含明示的新增功能。
- 原始證據與保存：Forth image／符號入口、字模量測、格點比對、外部解碼器對照及勘誤表（W1–W2）。
- 流程與假說：先辨認安裝檔、核心與應用 image 的角色，再追查實際功能。
- 行為基準：Wine 中原版用於介面；格式解碼另用獨立實作；新增功能不能宣稱 WinCV 原版相容性。
- 驗證：格點、像素、解壓內容雜湊、封包格式與實際啟動分開。
- 機器可讀觀測：W1 記錄格點差異工具、W2 記錄逐成員 SHA-256 比對；未在本輪執行。
- 失敗：截圖工具像素寬度錯誤；檔案時間無法識別舊建置；APK 格式驗過仍在 Layout 崩潰。
- 可重用實踐：觀測工具也要驗證；修好工具後重查受污染的推論。
- 專案限定與限制：原版外觀與新增功能使用不同基準；來源的素材與授權處置不移植至本專案。

### OnePCE AI Pacifista

- 儲存庫：`wicanr2/onepce-ai-pacifista`；本機 `/home/anr2/cht/onepce-ai-pacifista`。
- 提交：`d424d1ca5ba3e74d3df829e63d86e183e8cb9551`。
- 目的：供代理觀察、重播與對拍的 PC Engine 模擬器。
- 原始證據與保存：畫面規格、同幀記憶體傾印、輸入計畫、擷取腳本與 metadata 雜湊（O1–O3）。
- 流程與假說：先對記憶體，再對顯示視窗；偏移搜尋只診斷，不取代預先指定的驗收位置。
- 行為基準：Mesen2 的固定輸入與畫格輸出；不是原始主機實測。
- 驗證：O1 報告三個畫格各比對 76,480 像素；最後一列 320 像素在參考畫面外。
- 機器可讀觀測：畫面二進位檔、VRAM／SAT／色盤傾印及 metadata；O2 的 `TestFramebufferMatchesMesen2Picture` 可直接回查。
- 失敗：全速跳幀導致畫面取到舊幀，O3 明確關閉該功能。
- 可重用實踐：決定性必須涵蓋擷取；報告比較分母、裁切與未知區域。
- 限制：O2 缺必要環境變數會略過整個測試；`readWords` 遇不存在的記憶體檔回空值，呼叫端會略過該區。測試存在不代表每次都完成規格要求的記憶體核對。

### Atari Talos AI Toolkit

- 儲存庫：`wicanr2/atari-talos-ai-toolkit`；本機 `/home/anr2/cht/atari-talos-ai-toolkit`。
- 提交：`ea0c7ae6e8fbee2b6a9f29c61d0a1071a6e70e53`。
- 目的：讓代理以機器可讀介面觀察 Atari ST／STF；T1 明示仍未能完整開機玩遊戲。
- 原始證據與保存：固定外部 CPU 語料、Hatari 觀察、輸入及工具雜湊、版本化規格（T1–T4）。
- 流程與假說：控制介面、核心指令、整機與收據契約分開設閘門。
- 行為基準：外部 CPU 語料與程序外 Hatari；語料有缺陷時明示勘誤。
- 驗證：T4 報告 TAS 狀態與時序的不同驗收來源，並排除腳位波形等範圍。
- 機器可讀觀測：T2 是 `talos-jsonl/1` 控制契約；T3 的完整外部收據載體仍為 `DRAFT`。
- 失敗：外部 TAS 語料不能獨自裁決全部時序；不能把大批 CPU 通過數當完整遊戲驗收。
- 可重用實踐：未知／未實作明確回錯；基準缺陷與修正理由保留。
- 專案限定與限制：68000 指令樣本及 ST 時序不外推其他平台；本手冊不開啟硬體時序深挖。

### Parhelion PME86

- 儲存庫：`wicanr2/Parhelion-PME86`；本機 `/home/anr2/cht/Parhelion-PME86`。
- 提交：`106313a99f93bd97dc25a4b49b47b487445968bc`。
- 目的：重建 DOS 版 UCSD p-System 的 p-machine；不是 SunDog 的 68000 直譯器。
- 原始證據與保存：直譯器與檔案格式筆記、spec 閘門、原版軌跡及差分實作（P1–P3）。
- 流程與假說：原版證據、推論、刻意差異與新增功能分開記錄。
- 行為基準：dosgolem 中運行的原版 PME；從同一 dispatch 邊界擷取狀態。
- 驗證：P3 逐步比較 `IPC`、`SP`、`TOS`，回報第一個分歧；未實作與不相符分開。
- 機器可讀觀測：`Capture`、`Divergence`、`ParityResult` 型別；`Err` 與 `Diverge` 都必須解讀。
- 限制：P1 報告一致走過 306 條後停在未實作指令；不是整套 p-System 相容性證明。本輪未重跑。
- 可重用實踐：比較前先定義觀測邊界；無分歧但提早停止不是完整通過。
- 專案限定：擷取原版狀態適合指令差分，不等於正常玩家路徑證據。

## 固定來源索引

下表的識別碼供其餘三份文件引用。連結固定完整提交；章節或符號為本輪實際使用的定位。
部分來源可能需要存取權，本輪以本機 Git 物件為證，未驗證所有遠端連結可公開讀取。

| ID | 固定提交來源與定位 | 文件／程式碼 SHA-256 |
|---|---|---|
| M1 | [MM2 CONTEXT](https://github.com/wicanr2/mm2_cht/blob/d887651741b6f236973b48f756157a24c3bbcad5/CONTEXT.md)，§5 已被推翻的斷言 | `dbac7522704d9dd3b80d58e805fa238f70900c02df33009a87832322813e42a8` |
| M2 | [MM2 LZW](https://github.com/wicanr2/mm2_cht/blob/d887651741b6f236973b48f756157a24c3bbcad5/docs/formats/03-lzw-compression.md)，§1、§4 | `2a37598d384077406c50e1d963f24afc50a7a6a0056d5e575205951aea48e8ae` |
| M3 | [MM2 原版時間線](https://github.com/wicanr2/mm2_cht/blob/d887651741b6f236973b48f756157a24c3bbcad5/docs/playtest/01-oracle-timeline.md)，§3、§6 重測 | `ac3e818bd3b2219df98ccf330758562055d23f84643aa2d4bbfb0741c4eafcb9` |
| S1 | [春之石 CONTEXT](https://github.com/wicanr2/shard_of_spring_cht/blob/0e00fea38d370aa4223fc21421442a6ceef64bed/CONTEXT.md)，§6 已被推翻的斷言 | `111f2ee9e2e142b7444c055b2e793c49cfdabf3138bbcd35b1a37f6b45343019` |
| S2 | [春之石筆記 44](https://github.com/wicanr2/shard_of_spring_cht/blob/0e00fea38d370aa4223fc21421442a6ceef64bed/docs/re/44-int3d-is-used-after-all.md)，§1、§4 | `a13c8c66342dbc309c9769a560c611b58820cbaa2fef593b3b9ed2ab0fcac583` |
| S3 | [春之石筆記 83](https://github.com/wicanr2/shard_of_spring_cht/blob/0e00fea38d370aa4223fc21421442a6ceef64bed/docs/re/83-hp-is-attribute-3.md)，§1–4 | `0edf848eddf4a8ede13d01db179c47a9474a157f2450d78b364971ac9b04aaad` |
| F1 | [FD2 問題路由](https://github.com/wicanr2/fd2_re/blob/420daf9a81d563a5eb2bc49adcdafba3ca9f3a7f/docs/knowledge-base/00-index.md)，檔首與現況文件表 | `7cbd8ea56f82116044cb276696522a7442e43bf0996dc02a10a5dd4a252c4c63` |
| F2 | [FD2 開場流程](https://github.com/wicanr2/fd2_re/blob/420daf9a81d563a5eb2bc49adcdafba3ca9f3a7f/docs/knowledge-base/23-boot-title-and-scenario-flow.md)，§2.3–2.4 | `d34079c7a9ef56a65ff26c24778931055ae7037fa20497db8cd2a8c65a2a59ec` |
| W1 | [WinCV CONTEXT](https://github.com/wicanr2/wincv-remake/blob/b2d8b43f4f4f8e6eca1bf6099a2fafbf108da31a/CONTEXT.md)，已被推翻的斷言、決策紀錄 | `c57595958edbeaaf01c6af503496f5de720afacd3d674166f7ea1b9f660ad1fd` |
| W2 | [WinCV README](https://github.com/wicanr2/wincv-remake/blob/b2d8b43f4f4f8e6eca1bf6099a2fafbf108da31a/README.md)，專案介紹與來源聲明 | `817db75334fcb690579de52f5d8e2c5751849d37aca8b213f74c0ca246da1a40` |
| O1 | [OnePCE 畫面規格](https://github.com/wicanr2/onepce-ai-pacifista/blob/d424d1ca5ba3e74d3df829e63d86e183e8cb9551/docs/spec/framebuffer-parity.md)，§4–7 | `0f4f6192ad5103e0d91a97d3eaa24ee2e65be19be17c79909f807b9cfd9d345f` |
| O2 | [OnePCE 畫面測試](https://github.com/wicanr2/onepce-ai-pacifista/blob/d424d1ca5ba3e74d3df829e63d86e183e8cb9551/screen_oracle_test.go)，TestFramebufferMatchesMesen2Picture、readWords | `448d111af6677573b733cdf4bb5b48ba458f3de0559f728ab42cb600a4729ecf` |
| O3 | [OnePCE 擷取腳本](https://github.com/wicanr2/onepce-ai-pacifista/blob/d424d1ca5ba3e74d3df829e63d86e183e8cb9551/tools/oracle/mesen2_headless.sh)，跳幀開關、metadata 與雜湊 | `514c33e89ed56539f91d05bbf7298b39bae3d5b1162594c68d2b7fc48a4b8c66` |
| T1 | [Talos README](https://github.com/wicanr2/atari-talos-ai-toolkit/blob/ea0c7ae6e8fbee2b6a9f29c61d0a1071a6e70e53/README.md)，現況與里程碑 | `cd89ffbedb1b6c27b337ac78275b47b93edfa68294db172e03097bb3af0ac88b` |
| T2 | [Talos 控制契約](https://github.com/wicanr2/atari-talos-ai-toolkit/blob/ea0c7ae6e8fbee2b6a9f29c61d0a1071a6e70e53/docs/spec/002-jsonl-control.md)，傳輸與錯誤 | `12f3e3cbd0d149358629b40575086b3c1e9ba0608251d3ef84f6fd9fa4e2f756` |
| T3 | [Talos 收據草案](https://github.com/wicanr2/atari-talos-ai-toolkit/blob/ea0c7ae6e8fbee2b6a9f29c61d0a1071a6e70e53/docs/spec/023-hatari-oracle-receipt.md)，DRAFT、待定根決策 | `f6a3d4bb49c98c22bdc6945d4a0ef310bbe2c673f88a85c651f75bc30aca6c5a` |
| T4 | [Talos TAS 規格](https://github.com/wicanr2/atari-talos-ai-toolkit/blob/ea0c7ae6e8fbee2b6a9f29c61d0a1071a6e70e53/docs/spec/048-m68000-tas.md)，範圍、語料限制與驗收 | `811bc8b9025ad96b15033496061a5d96a881a526db0df48f739dcbce8947fde5` |
| P1 | [Parhelion README](https://github.com/wicanr2/Parhelion-PME86/blob/106313a99f93bd97dc25a4b49b47b487445968bc/README.md)，重做與 306 條對拍紀錄 | `400452950302d78844f1b42ef6638217f8ae838610d633364f00d3bcf72d0fb6` |
| P2 | [Parhelion 規格閘門](https://github.com/wicanr2/Parhelion-PME86/blob/106313a99f93bd97dc25a4b49b47b487445968bc/docs/30-remake/spec-workflow.md)，三個狀態與同狀態驗證 | `9e4601dc5efcd595e4ba403cc81e592f81503f734546060dfe53857e125a8744` |
| P3 | [Parhelion 差分實作](https://github.com/wicanr2/Parhelion-PME86/blob/106313a99f93bd97dc25a4b49b47b487445968bc/oracle/parity.go)，Capture、ParityResult、Parity | `88b2af82b440adb66faacfa4159a75e14c65c8fac08f7e6371f7bb1d5d75fdf2` |

## 缺失證據與第 0 階段審查

七個儲存庫均可讀；缺的是本輪獨立動態重跑，不是來源不可用。
未檢查所有原版輸入、畫面及軌跡是否仍完整存在，也未驗證各案例全部成果。
來源目前的公開／私人狀態未逐個查詢，不依歷史文件宣稱其現行可見性。

| 第 0 階段條件 | 本輪材料 | 自查結果 |
|---|---|---|
| 至少三個有來源的重複模式 | 模式矩陣 R1–R7，各列至少兩個專案 | 滿足送審條件 |
| 至少三個有來源的失敗模式 | 失敗模式 F01–F08 | 滿足送審條件 |
| 不把專案特例普遍化 | 矩陣的差異表與各案例限制 | 已明列 |
| 可追溯來源 | 七個完整提交、二十筆來源雜湊與章節／符號 | 二十筆均與固定提交 Git 物件吻合 |
| 不確定性明示 | 文件觀察、歷史結果、方法推論分開 | 已明列 |

上表保存首次盤點的送審條件，不冒稱專案負責人逐項審查過來源。
後續依「完成手冊」的明確指示繼續第 1 階段；來源及條件的編輯審查見
[手冊驗收紀錄](handbook-review.md)。本次未建立 schema、CLI 或原版介接器。
