# OpenMontage 團隊協作環境建置手冊 (Lean 分支)

> 給新加入或更換電腦的協作成員。依照以下 4 個步驟即可完成配置並與正式專案同步。

---

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
專案所有影片、圖片、Blender 模型與算圖成果均存於 Dropbox。請在 **命令提示字元 (CMD)** 執行目錄聯結：
```cmd
mklink /J "projects" "你的Dropbox路徑\kj-om-projects"
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
