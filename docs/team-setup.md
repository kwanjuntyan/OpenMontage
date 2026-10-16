# OpenMontage 團隊協作環境建置與更新手冊 (Lean 分支)

> 本手冊分為兩部分：
> - **一、既有環境：日常更新與啟動 Scene Player（常用）**
> - **二、新電腦／首次建置：4 步驟完成配置**

---

## 一、既有環境：日常更新與啟動 Scene Player

### 1. 確認 Dropbox 同步完成
五大專案的媒體檔（`assets/audio/`、`assets/images/`、`assets/videos/`）均由 Dropbox 自動同步，更新前請先確認電腦右下角 **Dropbox 已完成同步**。

### 2. 更新 Git 程式碼與專案食譜
打開 PowerShell 進入專案根目錄（例如 `cd D:\kj-openMontage`），執行：

```powershell
# 若當初依下方「第一步」直接 clone kwanjuntyan/OpenMontage，遠端名稱為 origin：
git fetch origin lean
git reset --hard origin/lean

# （若你的遠端名稱設為 team-fork，請改跑：git fetch team-fork lean; git reset --hard team-fork/lean）
```
*(註：因 `projects/*/artifacts/` 已納入 Git 版控，使用 `fetch + reset --hard` 可避免與 Dropbox 已同步之相同檔案發生未追蹤衝突。)*

### 3. 啟動 Backlot 看板與 Scene Player（毛片預覽器）
在專案根目錄執行：

```powershell
$env:PYTHONPATH="."; .venv\Scripts\python.exe -m backlot serve --port 4750
```

啟動後，用瀏覽器開啟：
- **🎬 Scene Player（毛片預覽器）**：`http://127.0.0.1:4750/ui/player.html`
  - 支援切換專案、幕／場篩選、對白音檔 vs 影片原音、分鏡圖 vs 影片、Camera 視角圖／並排對照，以及檢視／複製生成 Prompt。
- **📋 專案看板（Backlot）**：`http://127.0.0.1:4750/p/course-51-esg`（右下角亦可點擊 `🎬 Scene Player` 進入）

---

## 二、新電腦／首次建置：4 步驟完成配置

### 第一步：指定下載 `lean` 正式分支
請在終端機（PowerShell 或 CMD）執行（務必加上 `-b lean` 參數，避開其他歷史分支）：
```bash
git clone -b lean https://github.com/kwanjuntyan/OpenMontage.git kj-openMontage
cd kj-openMontage
```
確認目前分支：
```bash
git branch
# 終端機應顯示：* lean
```

---

### 第二步：建立 Python 虛擬環境並安裝依賴
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

### 第三步：連結 Dropbox 專案資料庫 (Windows Junction)
專案所有影片、圖片、音檔與 Blender 模型均存於 Dropbox（GitHub 僅版控各專案輕量的 `artifacts/`、`project.json` 與 `checkpoint_*.json`）。請在 **命令提示字元 (CMD)** 依序執行：
```cmd
rmdir /s /q projects
mklink /J "projects" "你的Dropbox路徑\kj-om-projects"
git checkout -- projects
```
*範例（若 Dropbox 位於 D 槽）：*
`mklink /J "projects" "D:\Dropbox\kj-om-projects"`

---

### 第四步：配置 API 金鑰與環境變數 (.env)
向團隊索取現成的 `.env` 與 Google Vertex AI 服務帳戶 JSON 憑證檔：
1. 將憑證 JSON 檔存放於本機目錄（例如 `C:\keys\vertex-service-account.json`）。
2. 在 `kj-openMontage/` 專案根目錄放置 `.env`，設定對應路徑與金鑰：
```env
GOOGLE_APPLICATION_CREDENTIALS=C:\keys\vertex-service-account.json
MINIMAX_API_KEY=your_minimax_key_here
```

完成後即可正常執行生成與合成腳本，成果將自動同步至 Dropbox。
