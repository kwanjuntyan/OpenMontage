# OpenMontage 跨 AI 協作審查橋接文件 (Review Bridge: Antigravity ↔ GPT)

> **本文件目的**：作為 **Antigravity (Google DeepMind)** 與 **GPT (OpenAI)** 兩位 AI 架構師之間的雙向異步 Code Review 與改進紀錄板。
> 雙方透過本文件往返討論、提出邊界漏洞、修復代碼並驗證，直到系統防護達到最高標準！

---

## 📌 模組一：系統架構與今日更新背景（Antigravity 撰寫）

### 1. 核心設計原則
* **Git 純淨化**：Git 倉庫僅允許保存**系統程式碼**（`lib/`, `tools/`, `scripts/`, `backlot/`）與**純文字課程配方**（`projects/*/artifacts/*.json`, `checkpoint_*.json`, `project.json`）。
* **多媒體雲端託管**：所有生成的多媒體檔案（`.mp4`, `.mp3`, `.png`, `.jpg`）一律被 `.gitignore` 排除，並由 `lib/gcs_storage.py` 自動背景非阻塞同步至 Google Cloud Storage (GCS)。
* **防呆與強制分類**：透過 `.githooks/commit-msg` 守門員強制區分：
  * **類別 A (系統代碼)**: `feat(...)`, `fix(...)`, `docs:`, `test(...)` 等
  * **類別 B (課程配方)**: `content(<course-id>): ...`, `data(<course-id>): ...`
  * **嚴禁混雜**：禁止同一次 commit 混雜系統代碼與 `projects/` 配方。
  * **二進位防護盾**：即使訊息符合規則，只要暫存區有媒體檔立即強制阻斷。
  * **名實不符阻斷**：改代碼卻掛 `content()` 或改課程卻掛 `feat()` 一律攔截。
* **零手動設定開機自啟**：`lib/git_bootstrap.py` 於 `tools/base_tool.py` 與 `backlot/server.py` 啟動時自動靜默安裝 Hook。
* **一鍵智慧助手**：`scripts/om_commit.py` 自動識別暫存狀態，分批打包並自動產生合規 commit。

### 2. 今日相關 Commit 歷程 (`team-main` 分支)
```text
48a99ba feat(git): add content-aware verification (binary, mixed, and semantic shields) to commit guard
3681f5c feat(git): add automated commit guard and smart commit assistant
8ab99f1 feat(projects): track project JSON recipes, checkpoints, and GCS manifests
5723386 feat(cloud): add non-blocking automated GCS sync for media generation
8d63bcc feat(showcase): add cloud stream URLs and 15-shot pdca-master card
b970dab feat(gcs): add ADC fallback to support separate storage credentials
9cab185 feat(cloud): unify GCS storage pipeline across CLP, shot video, audio, image, and master renders
d84dd88 feat(clp): support GCS remote storage and automatic 302 fallback for CLP character assets
```

### 3. 待審核的核心檔案清單
1. `.githooks/commit-msg`（守門員核心三道防護盾）
2. `lib/git_bootstrap.py`（開機自動引導與安裝）
3. `scripts/om_commit.py`（智慧分類打包與提交工具）
4. `tests/lib/test_git_commit_guard.py`（守門員單元測試套件）
5. `lib/gcs_storage.py`（GCS 雲端儲存與非阻塞自動同步核心）

---

## 🎯 模組二：Antigravity 給 GPT 的審查挑戰題（請 GPT 重點檢驗）

請 GPT 仔細閱讀上述檔案及倉庫狀態，並挑戰以下問題：

1. **【Hook 繞過與邊界漏洞】**：
   * 在 `.githooks/commit-msg` 中，對於路徑字串比對（如 `f.startswith("projects/")`）以及正規表示式比對，是否存在任何作業系統特殊字元（如 Windows 反斜線 `\`、大小寫敏感度、空格、符號連結 Symlink、空 commit `--allow-empty`、或合併衝突 commit）能避開檢查的漏洞？
2. **【智慧助手 `scripts/om_commit.py` 的穩定性】**：
   * 在解析 `git status --porcelain` 時，狀態碼如 `??`, `A `, ` M`, `MM`, `R `, `D ` 是否處理完善？若檔名包含空格或中文字元，執行 `git add` 時是否會失效？
3. **【GCS 非同步安全】**：
   * `lib/gcs_storage.py` 的背景非同步上傳 (`sync_file_in_background`)，若 Python 主行程意外結束、或短時間大量高頻觸發，執行緒池與佇列是否會發生記憶體洩漏或檔案丟失？
4. **【Git 倉庫二進位污染清查】**：
   * 請執行 `git ls-files` 進行全局審計，確認當前倉庫中是否仍有任何 `.mp4`, `.mp3`, `.png`, `.jpg`, `.onnx` 等大檔案被意外納入 Git 追蹤？

---

## 💬 模組三：GPT 審查意見與回饋區（請 GPT 填寫於下方）

*(請 GPT 在此區塊填寫您的審查發現。請依「嚴重度」、「問題描述」、「可能導致的後果」及「建議修復方式」結構化列出)*

### 範例格式：
```markdown
### 發現 1：[標題]
* **嚴重度**：[Critical / Major / Minor / Suggestion]
* **相關檔案**：[檔名與行號]
* **問題說明**：
* **潛在風險**：
* **修復建議**：
```

<!-- GPT 回饋請從此行下方開始撰寫 -->




---

## 🛠️ 模組四：Antigravity 修正與回應記錄（Antigravity 填寫）

*(當 GPT 填寫意見後，Antigravity 將在此區塊記錄修復動作、對應 Commit 與單元測試驗證結果)*

| 問題編號 | 提出方 | 審查意見摘要 | 處理狀態 | 修復 Commit / 說明 |
| :--- | :--- | :--- | :--- | :--- |
| *待新增* | GPT | - | 待審核 | - |

---

## 🔄 模組五：協作工作流指引（供使用者操作）
1. **第一步**：請將本檔案 `REVIEW_BRIDGE.md` 提供給 GPT，或告知 GPT：「請讀取 `d:\kj-openMontage\REVIEW_BRIDGE.md`，並依照裡面的指示進行審查，將你的意見寫在『模組三』中並存檔。」
2. **第二步**：GPT 存檔後，告訴 Antigravity：「GPT 已經填寫好審查意見了，請讀取並改進。」
3. **第三步**：Antigravity 讀取意見、評估並執行代碼改進、通過單元測試、填寫『模組四』的修復紀錄，並提交 commit。
4. **第四步**：再次交由 GPT 複核，直到雙方達成「零缺失（All Passed）」共識！
