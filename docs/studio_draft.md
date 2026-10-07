# OpenMontage Studio（導演控制台與虛擬製片工作台）介面設計規劃草案

> **版本**：v0.5.0 (Restructured Architecture & Industrial Production Draft)  
> **日期**：2026-09-15  
> **狀態**：規劃審議中 (Under Review)  
> **關聯文件**：[`AGENT_GUIDE.md`](../AGENT_GUIDE.md)、[`backlot/README.md`](../backlot/README.md)、[`schemas/artifacts/`](../schemas/artifacts/)

---

## 1. 系統定位與核心哲學

### 1.1 什麼是 OpenMontage Studio？
OpenMontage Studio 是建立在 Backlot Headless API 之上的**「互動式虛擬製片工作台（Interactive Production Studio）」**。

它將作為**生產進程中的「分階段專用作業台」**：隨影視製作標準管線（劇本 ➔ 風格 ➔ CLP 角色 ➔ 鏡頭生成 ➔ 專案管理 ➔ 預算管理）提供各階段所產出之資訊及媒體，並提供相關功能，如直觀的九宮格選圖、單鏡頭重繪、色票微調、管線狀態監控與審批按鈕。

### 1.2 核心設計原則
- **Backlot同源架構（In-tree Backlot Extension）**：作為 Backlot 原生擴充頁面，由現有的 FastAPI 統一管理派送，享用現成的 SSE 檔案變更即時推播，零額外 npm 依賴。
- **架構邊界嚴格解耦（Agent as Brain, Studio as Observer & Gateway）**：Studio 保持輕量與高響應，嚴格遵守 OM「Agent 才是編排大腦，Python 為工具與持久化」的最高原則，絕不將 Studio 伺服器膨脹為不可控的自主後台排程器。
- **富上下文互動（Context-Aware Human-in-the-Loop）**：UI 不僅是展示看板，更是帶有精確上下文的「導演對講機」，使用者在特定卡片點擊按鈕，直接向後台 Agent 傳遞結構化導演修改指令。

---

## 2. 專案架構模式：單片短專案 vs. 長劇本/系列課程父子管線

OpenMontage Studio 支援兩種標準專案架構模式，依製片規模自適應調度：

### 2.1 單片獨立專案模式 (Standalone Project Mode)
適用於 30 秒至 3 分鐘的短影音、廣告預告片、單支概念解說片。依循單一專案目錄（`projects/<project-id>/`）跑完整流水線。

### 2.2 支援各種長度及類型的劇本 (依循 OM 現行標準規範)
參考 short-form_script.md, long-form_script.md, course-form_script.md 的結構。

#### 2.2.1 遵循 OM 既有標準資產（零重複造輪子）
OpenMontage 系統內已沉澱完整的長篇影音與拼接標準，Studio 介面應直接遵循並複用以下既有體系：
- **編劇與章節架構標準**：[`skills/creative/long-form.md`](../skills/creative/long-form.md)
  - 嚴格規範長篇敘事節奏：單一章節長度為 **2~4 分鐘**，10~15 分鐘影片上限為 **5~6 個 Chapters**。
  - 實施留存曲線管理（Retention Curve）：0:30 前完成 Hook 跨越「30秒懸崖」、2:00~3:00 安排留存低谷（Retention Valley）破局點、每 45~90 秒插入模式中斷（Pattern Interrupt）、旁白維持 **150~160 WPM** 教育黃金語速。
  - 長篇音訊標準：全片襯樂連續鋪墊（Narration 下壓 18~20 dB）、跨章節音量偏差必須 **< 2 LUFS**（目標 -14 LUFS integrated）。
- **影像串接與拼接規範**：[`skills/creative/video-stitching.md`](../skills/creative/video-stitching.md)
  - 規範循序拼接（Sequential Stitching）與 `stitch_plan` 結構。
  - 防止長音訊漂移（Audio Drift）關鍵機制：強制輸入必須為 **CFR 恆定影格率 (`-vsync cfr`)**。
  - 調用 `tools/video/video_trimmer.py`（concat 操作，首選 `codec: copy` Stream Copy，異常時自動回退至 CRF 18 近無損重編碼）與 `tools/video/video_stitch.py`。
- **章節發布與時間戳標準**：[`tools/publishers/export_bundle.py`](../tools/publishers/export_bundle.py) 與 [`schemas/artifacts/publish_log.schema.json`](../schemas/artifacts/publish_log.schema.json)
  - 原生支援自 `script.json` 區段自動生成 YouTube / 企業 LMS 相容之 `metadata/chapters.txt` 與帶時間戳之 `metadata/description.txt`。
- **封裝式課程容器架構 (Course Container Architecture)**：
  - 詳見專用提案規範：[`docs/course_container_architecture_proposal.md`](course_container_architecture_proposal.md)。
  - 確立「一門課程即一個資料夾 (`projects/<course-id>/`)」的單一容器封裝標準，所有章節收納於內部 `chapters/`，徹底杜絕根目錄污染與資產同步困難。

#### 2.2.2 課程前置處理與交付流程
### 2.3 檔案結構與工具分工定位



## 3. 總覽架構：簡潔頂部導覽列 + 六大專用工作區

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Backlot Studio]                                                                                      │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  [ 📝 劇本 ]  |  [ 🎨 視覺風格 ]  |  [ 👤 角色定裝 ]  |  [ 🎬 鏡頭挑片 ]  |  [ 📁 專案管理 ]  |  [ 💰 預算管理 ]  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **頂部簡潔導覽列（Top Navigation Bar）**：
  為保持各製作階段的專注與最大化可視創作空間，頂部僅保留 Studio 品牌標識與**六大專用分頁標籤**：
  - 完美呼應影視前期製作流程，隨專案當前卡點（Checkpoint）自動預設跳轉，亦支援使用者隨意手動切換。
  - **架構優化（權責嚴格劃分）**：原「頂部常駐抬頭列（Always-on HUD）」功能全面解構為獨立專用分頁呈現，不再常駐頂部佔用空間——專案/課程切換、管線狀態燈號、原生故事板快速跳轉與階段導覽歸入**「第五區：專案管理」**；總花費、預算進度條、供應商佔比與鏡頭花費排行則歸入**「第六區：預算與成本管理區」**集中深度治理。

---

## 4. 六大工作區詳細規格

### 第一區：劇本審閱與修訂區 (Script)

* **任務**：檢視與核定全片劇本內容、段落結構與台詞長度，支援「原始輸入文稿」與「改編結構化劇本」的雙重視圖比對與知識點溯源，向 Agent 提出修改意見並執行階段審批。
* **使用對象與場景**：講師、領域專家（SME）、編劇、企劃人員在專案前期的 `script` 階段使用。
* **具體功能**：
  1. **雙重視圖切換 (Dual-View Switcher)**：
     - **視圖 A：結構化分段劇本 (Production Script)**：依序展示場景標題（Slugline）、動作指示（Action）、角色名稱、對白台詞（標準好萊塢寬版劇本排版），並標註預估朗讀秒數與語氣情緒指導（Delivery Cues）。
     - **視圖 B：原始輸入文稿 (Raw Source Document)**：完整呈現使用者最早丟入的講義、課程大綱或 Word 原稿文字，供講師確認專業術語與核心概念。
     - **視圖 C：左右並列對照 (Split-Screen Comparison)**：左側為原始文稿，右側為改編後的分段台詞。
  2. **點擊高亮溯源 (Source Reference Tracing)**：
     - 點擊右側任一 Section 台詞，左側原始文稿中對應的來源段落自動高亮（Highlight），方便講師瞬間核對「AI 有沒有改歪我的專業概念？有沒有漏掉重要知識點？」。
     - *實施路徑*：初期在前端以字串模糊比對（Fuzzy String Matching）迅速對齊；長期於 `script-director.md` 引導 LLM 產出 `source_ref` / `source_section_id` 欄位並擴充 `schemas/artifacts/script.schema.json`。
  3. **精準時長與字數統計**：統計並顯示各場景及全片的預估旁白朗讀秒數（基於 WPM/CPM 語言學公式）與總字數。
  4. **修改意見輸入框**：讓使用者輸入反饋文字（例如「第 2 段碳稅定義請保留原稿原話，語氣改嚴肅」）並發送給 Agent 重新編劇。
  5. **核准劇本按鈕 (Human Approval Gate)**：確認核准後通知管線推進至下一個製作階段。
* **取用 OM 的資料**：
  - `artifacts.script.title`（劇本標題）
  - `artifacts.script.total_duration_seconds`（全片預估總時長）
  - `artifacts.script.sections[]`（段落陣列，包含 `id`, `heading`, `narration`, `dialogue`, `action`, `estimated_duration`, `source_ref`）
  - 專案原始輸入文件（如 `artifacts/raw_script.md` 或 `brief.source_material`）
  - `stages[]`（檢查 script 階段目前是否處於 `awaiting_human` 狀態）
* **如何取得**：
  發送 HTTP GET 請求至 `http://127.0.0.1:4750/api/project/{project_id}/state`，讀取回傳 JSON 中的 `artifacts.script` 物件及原始文稿欄位。

---

### 第二區：視覺風格與美學調度區 (Style & Aesthetics)

* **任務**：定義、檢視與微調全片的宏觀美術風格、視覺色票、光影調性、鏡頭語言與負向提示詞，支援全域風格庫的挑選、繼承與沉澱，作為全片所有分鏡生圖的「審美總綱領」。
* **使用對象與場景**：導演、藝術總監（Art Director）在開拍前期（`proposal` / `clp` 階段）定調視覺語言時使用。
* **具體功能**：
  1. **下拉挑選既有風格庫（Preset & Custom Selector）**：建立新課或微調時，可直接從下拉選單快速挑選、切換套用既有風格（如系統預設的 `clean-professional`、`anime-ghibli`，或既有客製的 `esg-pixar-hybrid`）。
  2. **另存為新風格（Fork & Save As）**：支援以既有風格為基底，在 UI 上微調色票、光影或 Prompt 前綴後，輸入新名稱點擊「另存為新風格」（例如存為 `styles/custom/finance-gold.yaml`），自動沉澱入庫，供未來該客戶或該系列的所有影片長期共用。
  3. **視覺化色票面板（Color Swatches）**：直觀顯示本片的主色調、輔助色、環境光色盤（可直接點擊複製 Hex 代碼）。
  4. **風格語彙與基調展示**：顯示當前套用的 Playbook 核心光影（如體積光、冷暖對比）、鏡頭焦段（35mm/85mm）與材質渲染規則（SSS 皮膚、織物細節）。
  5. **全局 Prompt 前綴／後綴展示與編輯**：檢視與微調自動注入每個鏡頭的通用風格詞庫。
  6. **全片負向提示詞（Negative Prompts）管理**：設定並檢查全片禁忌規則（如嚴禁低畫質、變形肢體、文字浮水印）。
* **取用 OM 的資料**：
  - `state.style_playbook`（當前選定的風格手冊路徑）
  - 全域可用風格清單（透過調用 `lib.playbook_generator.list_playbooks()` 取得所有 `styles/` 與 `styles/custom/` 清單）
  - 對應的 `styles/*.yaml` 內容（包含 `palette`、`visual_rules`、`prompt_templates`、`negative_prompt`、`audio_rules`）
* **如何取得與操作**：
  - **讀取資料**：發送 HTTP GET 至 `/api/project/{project_id}/state` 取得當前風格；後端提供 `GET /api/styles` 端點獲取可用清單（封裝 `lib.playbook_generator.list_playbooks()`）。
  - **另存新風格**：前端點擊「另存為新風格」後，發送 HTTP POST 至後端端點 `/api/styles/save_as`，由後端調用 `lib.playbook_generator.save_playbook()` 將新設定寫入 `styles/custom/<new_name>.yaml` 並更新專案關聯。

---

### 第三區：角色與實體定裝區 (CLP & Entities)

* **任務**：檢視與鎖定登場角色、場景空間及關鍵道具的視覺特徵，建立全片外觀一致性的基準。
* **使用對象與場景**：美術指導、角色設計師在 `clp` 階段使用。
* **具體功能**：
  1. 以寬版卡片清單列出全片角色（Characters）、場景（Locations）與道具（Props）。
  2. 顯示角色的基準定裝肖像大圖、年齡、職務描述。
  3. 顯示角色的「外觀特徵鎖定詞庫（`visual_locks`）」，供使用者檢查細節（如髮型、服裝、五官特徵）。
  4. 標記各實體的鎖定狀態標籤（`Locked 🔒` / `Draft ⚠️`）。
  5. 支援候選圖盲測比較（A/B Comparison），點擊特定肖像即可鎖定為標準臉。
  6. 點擊肖像圖可彈出大圖燈箱（Lightbox）放大檢視。
* **取用 OM 的資料**：
  - `clp.characters[]`（角色陣列，包含 `id`, `name`, `role`, `age`, `description`, `visual_locks`, `portrait`）
  - `clp.locations[]`（場景陣列）
  - `clp.props[]`（道具陣列）
  - 圖片二進位路由：`/thumb/{project_id}/{portrait}` 或 `/media/{project_id}/{portrait}`
* **如何取得**：
  發送 HTTP GET 請求至 `http://127.0.0.1:4750/api/project/{project_id}/state`，讀取回傳 JSON 中的 `clp` 物件。

---

### 第四區：鏡頭分鏡與資產調度區 (Shots & Assets)

* **核心哲學**：**「以 Scene（場景）為空間與機位覆蓋容器，以 Shot（鏡頭）為語意與動態錨點」**。在劇本與影視製作中，Scene 是時空、光影與機位連貫的實體容器（亦為**【九宮格場景機位覆蓋矩陣】**的宿主層級），而 Shot 是鏡頭調度、審查與資產替換的最小語意單位。
* **任務**：多模態呈現全片資產（**Image、Video、Audio 三位一體**），自適應相容「全場景多鏡頭長片（Seedance / Omni）」與「單鏡頭原子短片（Veo / Kling / 圖像）」兩種生成範式，並提供導演級的 **Scene 九宮格機位覆蓋矩陣**、分鏡縮圖自動擷取、無損切片與單鏡頭局部抽換（Shot Patching）工具。
* **使用對象與場景**：現場導演、分鏡師、剪輯師在 `assets`（素材生成與挑片）與 `edit`（剪輯決策）階段使用。

* **具體功能與介面架構**：

  #### 1. 多模態資產三位一體呈現 (Image + Video + Audio Co-existence)
  每個鏡頭卡片或場景容器均支援三種模態的聯動展示，不再孤立切割：
  - **Image（圖像卡片）**：顯示高清靜態分鏡圖、3x3 九宮格候選圖、或自影片擷取之代表影格（Keyframe Thumbnail），支援點擊彈出全螢幕大圖燈箱（Lightbox）放大檢視細節。
  - **Video（影片播放槽）**：支援就地播放（In-place Player）、懸浮預覽、雙速播放，卡片上直觀標記解析度、FPS、時長與生成模型徽章（例如 `[Seedance 2.5]` 或 `[Veo 2]`）。
  - **Audio（音訊波形軌道）**：獨立呈現該鏡頭/場景綁定的 TTS 旁白語音檔（`.wav`/`.mp3`）、環境音效（SFX）或配樂（BGM），自帶即時波形條（Audio Waveform）與試聽按鈕。

  #### 2. 場景容器與雙態自適應渲染 (Scene Container & Dual-State Rendering)
  - **外層容器：場景折疊膠卷 (Scene Filmstrip Container)**
    - 以 Scene（如 `Scene 01: 董事會危機爆發 (00:00 - 00:18)`）為可折疊的橫向或縱向膠卷容器。
    - 顯示場景級概況：場景時長、對應劇本段落對白、總覽標籤。
  - **內層雙態自適應**：
    - **模式 A：Shot-as-Asset（單鏡頭原子模式，適用 Google Veo 2 / Kling / 靜態圖像）**
      - 每個 Shot（Shot 1.1, 1.2, 1.3）對應獨立實體檔案（`shot_1_1.mp4`, `shot_1_2.mp4`）。
      - 各鏡頭卡片並列，具備各自獨立的播放器、Prompt、Seed 與重算按鈕。
    - **模式 B：Scene-as-Asset（全場景母帶模式，適用 ByteDance Seedance 2.0/2.5 / Gemini Omni Flash）**
      - 場景頂部設有 **「場景全段母帶播放器（Scene Master Player）」**，可一鍵連續播放 15~30 秒帶原生剪輯與同步音畫之完整母帶。
      - 下方依據 `tools/analysis/scene_detect.py` 檢測出的剪輯點，列出 **虛擬鏡頭切片卡（Virtual Shot Cards）**，標註時間戳（如 `00:05 - 00:11`）與截取的分鏡縮圖。
      - **互動跳轉**：點擊任一 Shot 卡片，上方母帶播放器自動跳轉（Seek）至該鏡頭起點循環試聽。

  #### 3. 剪輯、裁切、抽圖與局部抽換工具 (Slicing, Cropping & Patching)
  - **★ 九宮格場景機位覆蓋矩陣 (Scene Coverage 9-Grid) —— Scene 層級空間一致性核心工具**：
    - **層級專屬性 (Scene-Level Tool)**：本工具嚴格定錨於 **`Scene`（場景）層級**。因 Scene 代表「同一時空與實體環境（如董事長辦公室）」，天生需要多機位覆蓋（Coverage：大全景、中景、特寫、過肩 OTS、反打 Reverse、俯瞰、仰角、道具特寫、空鏡）。
    - **空間自注意力機制 (Global Self-Attention)**：調用生圖模型（如 FLUX）在單一畫布上一次性生成 3x3 九宮格母圖。在單次前向傳播中，神經網絡的全局自注意力強行定錨全場景的幾何坐標、同軸光影（Key Light）與 180 度攝影機軸線（Eyeline），徹底杜絕跳軸與空間漂移。
    - **0.1 秒無損幾何切片與資產派發**：後端調用 Python Pillow (PIL) 幾何切片端點（`POST /api/project/{id}/shot/{shot_id}/crop_tile`），瞬時切出 9 張獨立的高清 Shot 圖片（`shot_01.png` ~ `shot_09.png`），自動指派為該 Scene 內各 Shot 的 First-Frame 靜態定錨圖。
    - **黃金備選庫 (Safety Takes & B-roll)**：即便該 Scene 只需 3~4 個鏡頭，其餘格子自動沉澱為「備用視角」與「氛圍空鏡」，供導演在卡片上一鍵點擊切換替換！
  - **自動分鏡影格擷取 (Scene-Guided Keyframe Sampling)**：後端調用 `tools/analysis/frame_sampler.py`，根據剪輯點自動在每段鏡頭起點或中點截取代表圖，確保即便生成的是連續長片，看板上也能有清晰的分鏡縮圖。
  - **無損物理切片 (Lossless Trimming)**：若需要將場景母帶物理拆解為獨立檔案，調用 `tools/video/video_trimmer.py`（FFmpeg `-c copy`），毫秒級切出個別鏡頭獨立短片。
  - **👑 導演救生圈：單鏡頭獨立覆蓋抽換 (Shot Override / Patching - 跨階段生命週期)**：
    - *觸發點 (Assets Stage)*：當 Seedance/Omni 母帶整體優秀，但其中某個 Shot（如 Shot 1.2）穿幫或不合意時，在該 Shot 卡片點擊「⚡ 獨立抽換此鏡頭」。可調用 Veo 2 / Kling 單獨重算該短片（`shot_1_2_patch.mp4`），或改用靜態高精圖像（FLUX）+ Remotion 運鏡。
    - *決策寫入 (Edit Stage)*：在剪輯決策檔 `edit_decisions.json` 記錄開窗抽換區間（如 `replace: scene_1 [00:05-00:11] with shot_1_2_patch.mp4`）。
    - *合成執行 (Compose Stage)*：於最終 `video_compose` 階段自動執行「三明治開窗接合」，保留前後好鏡頭，只替換瑕疵鏡頭，並以 `tools/audio/audio_mixer.py` 交叉淡化（Crossfade）平滑處理音訊接縫。
  - **單鏡頭重新生成按鈕**：支援在卡片上微調 Prompt，發送給後端重算，卡片即時顯示掃光微光動畫（`◉ GENERATING`）。
  - **歷史版本切換 (Takes Carousel)**：支援即時切換該鏡頭過往生成過的所有歷史版本（`Take 1`, `Take 2`...），隨時一鍵 Rollback。

* **取用 OM 的資料**：
  - `storyboard.scenes[]`（每個鏡頭包含 `id`, `description`, `start_seconds`, `end_seconds`, `duration_seconds`, `visual`, `takes[]`, `audio[]`）
  - `artifacts.asset_manifest.assets[]`（包含各資產的 `type` (image/video/audio/narration), `prompt`, `model`, `seed`, `cost_usd`, `duration_seconds`）
  - 分析工具結果：`scene_detect.py` 產出之剪輯點清單、`frame_sampler.py` 產出之縮圖
  - 媒體檔案串流路徑：`/media/{project_id}/{path}` 與 `/thumb/{project_id}/{path}`
* **如何取得與操作**：
  - 讀取資料：呼叫 `GET /api/project/{project_id}/state`。
  - 動作操作：
    - 九宮格裁切：發送 `POST /api/project/{id}/shot/{shot_id}/crop_tile`（帶 `tile_index: 1~9`）。
    - 鏡頭重繪：發送 `POST /api/project/{id}/shot/{shot_id}/regenerate`。
    - 鏡頭抽換：發送 `POST /api/project/{id}/shot/{shot_id}/override`（指定替換模型與 prompt）。

---

### 第五區：專案管理 (Project Management)

* **任務**：統籌管理整體專案生命週期、跨專案/課程章節切換調度、管線 DAG 與階段卡點（Checkpoint）即時監控，以及全站導航跳轉。**本區專注於「專案進程、狀態調度與指令審批」，完全不介入財務成本細節**。
* **使用對象與場景**：導演、製片人、專案經理在需要切換不同專案/微課程、排查管線卡點瓶頸、審核管線推進階段、或快速穿梭各工作區與原生故事板時切入此分頁使用。
* **具體功能**（由原頂部常駐 HUD 移入分頁內集中管理，取代「頂部常駐」，在分頁內專用呈現）：
  1. **專案/課程切換選單（Project Selector Dropdown）**：呼叫 `GET /api/projects` 取得所有歷史與正在進行的課程專案清單，讓導演隨時切換檢驗不同專案，無須重整網址；清楚標註各專案狀態、最後修改時間與章節所屬。
  2. **當前管線狀態燈號與階段推進監控（Pipeline Status & Stage Indicator）**：即時顯示目前專案所處的製作階段與卡點狀態（如 `awaiting_human: assets`、`in_progress: compose` 或 `completed`），並視覺化呈現各階段的進退狀態與 DAG 流程。
  3. **審核卡點與指令歷程紀錄（Approval Gates & Directives Log）**：即時顯示當前待審核項目（Human Approval Gate）、審查歷程，以及使用者發布之最新修改指令（`directives.json`），精確掌握後台 Agent 的編排執行狀態。
  4. **原生故事板快速切換鈕（Native Storyboard Switcher）**：一鍵返回 Backlot 原生 Storyboard (`/p/{project_id}`)，方便在 Studio 深度工作台與輕量動態故事板之間無縫穿梭。
  5. **六大專用工作區導覽與跳轉（Stage Quick Jump & Workflow Navigation）**：完美呼應影視前期製作流程，彙整各階段（劇本、風格、角色、鏡頭、預算）的當前進度卡片，隨專案當前卡點（Checkpoint）自動提示推薦跳轉，亦支援使用者在此隨意手動點擊切換。
* **取用 OM 的資料**：
  - `GET /api/projects`（全域專案清單與元資料）
  - `stages[]` 與 `checkpoint`（當前階段卡點狀態，如 `awaiting_human`、`current_stage`）
  - `directives.json`（非同步修改指令佇列與歷史）
  - `project_id`、`title`、`pipeline_type`（專案標識）
* **如何取得與操作**：
  - 發送 HTTP GET 請求至 `/api/projects` 取得所有專案清單以供切換。
  - 發送 HTTP GET 請求至 `/api/project/{project_id}/state`，於分頁內直觀渲染當前專案之管線狀態燈號、階段卡點、指令佇列與各階段導覽按鈕。

---

### 第六區：預算與成本管理區 (Budget & Cost)

* **任務**：專門負責全專案資金消耗審計、API 服務商花費分析、高成本鏡頭重繪監控，並實施專案預算防超支治理機制。（原頂部 HUD 之總花費與預算進度條全面收斂至本區進行深度視覺化展現）。
* **使用對象與場景**：製片人、財務管理者、專案經理在整個製作生命週期隨時監看資金消耗、排查高額開銷、設定預算警報時使用。
* **具體功能**：
  1. **總花費儀表與預算進度條（Total Spent & Budget Progress Gauge）**：整合原頂部 HUD 之預算進度條，直觀呈現消耗百分比（基於 `cost.total_spent_usd` 與設定預算上限），以動態色彩（綠 ➔ 黃 ➔ 紅）清晰警示預算消耗程度與剩餘額度（`cost.budget_remaining_usd`）。
  2. **供應商服務支出佔比分析（Provider Cost Breakdown）**：依 API 供應商分類支出佔比（Google Imagen/Veo 算圖、OpenAI LLM、ElevenLabs 配音、Fal.ai Seedance、本機免費渲染等），以環形圖或長條圖呈現各服務商費用分佈。
  3. **高成本鏡頭花費排行表（Top Expensive Shots Ranking）**：自動撈取 `artifacts.asset_manifest.assets[]`，分析統計因反覆重繪（Multiple Takes）或調用頂級模型而花費最高的鏡頭排行榜，標示各鏡頭耗費金額、重繪次數與每次花費明細。
  4. **預算上限防超支控制與安全閥（Budget Cap & Safety Thresholds）**：提供「預算上限設定輸入框」，當專案花費達到安全門檻（例如 80%、100%）時發出視覺警告並暫停昂貴 API 生成，防止非預期的費用暴增。
* **取用 OM 的資料**：
  - `cost.total_spent_usd`（專案總累計支出）
  - `cost.budget_usd` / `cost.budget_remaining_usd`（專案預算上限與剩餘額度）
  - `artifacts.asset_manifest.total_cost_usd`（資產總成本）
  - `artifacts.asset_manifest.assets[].cost_usd`（單一資產成本）
  - `artifacts.asset_manifest.assets[].provider`（服務商名稱）
  - `artifacts.asset_manifest.assets[].model`（生成模型）
* **如何取得**：
  發送 HTTP GET 請求至 `http://127.0.0.1:4750/api/project/{project_id}/state`，讀取其中的 `cost` 物件及 `asset_manifest.assets` 清單中的費用與模型明細。

---

## 5. 互動式動作與 Agent-Native 雙軌協同機制

為恪守 OpenMontage **「Agent 才是大腦，Python 為工具與持久化，Backlot 永遠是輕量觀察者」** 的核心哲學，互動按鈕採取嚴謹的雙軌架構，兼顧「0.1 秒極速回饋」與「LLM 深度編排智能」：

```
                    ┌────────────────────────┐
                    │  Studio UI 使用者點擊   │
                    └───────────┬────────────┘
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
   【軌道 1：機械性工具操作】                  【軌道 2：創意性編排與階段核准】
  (無須 LLM 創意介入，極速執行)               (需劇本上下文理解或推進 Pipeline)
          │                                           │
          ├─ 九宮格裁切 (Pillow)                       ├─ 途徑 A (輕量 Prompt 算圖)：
          ├─ 無損切片 (FFmpeg)                         │   FastAPI 背景任務直接調用
          └─ 風格手冊另存 (PlaybookGen)                │   BaseTool 算圖並更新 Manifest
          │                                           │
          ▼                                           ├─ 途徑 B (重大改動/階段核准)：
  FastAPI 端點直接同步/異步執行                         │   寫入 directives.json 與 Checkpoint
          │                                           │   由主環境 Agent 讀取並正式編排
          ▼                                           ▼
   寫入磁碟資產 / 更新 Manifest ────────────────> watchfiles 捕獲變更 ➔ SSE 推播 ➔ 前端 0.1s 刷新
```

### 5.1 軌道 1：機械性操作（Direct Tool Execution）
* **代表功能**：九宮格點選第 5 格裁切採用、風格手冊 YAML 另存、無損影音切片。
* **執行流**：前端發送 `POST` 請求 ➔ FastAPI 端點調用相應工具（如 Python Pillow / `lib.playbook_generator.save_playbook`）執行 ➔ 寫入磁碟目標檔案 ➔ `watchfiles` 自動捕捉檔案變更 ➔ SSE 推播事件 ➔ 前端畫面 0.1 秒無感更新。

### 5.2 軌道 2：創意性操作與階段核准（Agent-Native Collaboration）
* **代表功能**：單鏡頭修改重新生成（例如「表情改焦慮」）、劇本核准推進階段。
* **執行雙途徑**：
  - **途徑 A（輕量即時重繪 - Headless Tool Direct Call）**：若僅是單一鏡頭 Prompt 微調，後端 FastAPI 背景任務直接實例化 BaseTool（如 `ImageSelector` 或 `SeedanceVideo`）重新生成 Take，寫入 `asset_manifest.json`，免去拉起龐大 Agent 的開銷。
  - **途徑 B（非同步指令佇列 - Directive Queue）**：若為涉及劇本脈絡理解、多鏡頭連鎖改動或階段審批（`human_approved: true`）：
    1. UI 將指令打包寫入 `projects/<id>/directives.json`，並更新 Checkpoint 狀態。
    2. 開發者在 Antigravity / Claude 終端對話中觸發繼續，Agent 即刻讀取 `directives.json` 上下文執行正式管線編排。
    3. 產出新檔案寫入磁碟，SSE 廣播喚醒前端，新畫面伴隨微光動畫浮現。
    *此機制確保 Backlot 伺服器永遠不會膨脹為失控的自主後台排程器，百分之百捍衛 OM 的架構純粹性。*

---

## 6. 前後端檔案佈局

在現有 `backlot/` 目錄中擴充，不破壞原先任何功能：

```text
backlot/
├── server.py              # 現有 FastAPI 伺服器（新增 /p/{id}/studio 路由與動作端點）
├── state.py               # 現有狀態機引擎（資料完全沿用，無需改動）
└── ui/
    ├── board.html         # 現有：電影級故事板（原封不動）
    ├── board.js
    ├── studio.html        # ★ 新增：六區工作台主頁面
    ├── studio.js          # ★ 新增：六區切換、專案管理、Lightbox 與通訊邏輯
    ├── studio.css         # ★ 新增：專用版面樣式（繼承 board.css 暗室電影級變數）
    ├── board.css          # 共用顏色與字體變數系統
    └── lib.js             # 共用 DOM 構建與 SSE 訂閱函式庫
```

---

## 7. 分階段實施路線圖 (Implementation Roadmap)

為確保工程穩健推進，杜絕 UI 開發時因底層資料結構變動而重工，採取「先核心資料契約、後視覺工作台」之嚴謹推進路線：

### 先決里程碑：Phase 0 - 長課程容器與後端資料契約凍結 (Headless POC)
*詳見專用架構提案：[`docs/course_container_architecture_proposal.md`](course_container_architecture_proposal.md)*
- [ ] 建立 `schemas/artifacts/course_manifest.schema.json`（定義 `course.json` 契約）。
- [ ] 在 `lib/identity.py` 新增 `resolve_chapter_dir` 支援二級安全路徑解析。
- [ ] 在 `backlot/state.py` 加入對 `course.json` 的自動識別與子章節進度聚合。
- [ ] 撰寫 `skills/pipelines/course-orchestrator.md` 編排指引。
- [ ] 重構 `skills/creative/long-form.md`，將內部段落模板由 Chapter 改寫為 Sequence。
- [ ] 完成端到端無頭（Headless）Smoke Test：2 個微章節管線生成 ➔ FFmpeg Stream Copy 零損縫合為母帶 ➔ 產出 `chapters.txt`。

---

### 第一階段：Studio 靜態六區框架與資料綁定 (視覺快速交付)
- [ ] 建立 `studio.html`、`studio.js` 與 `studio.css`。
- [ ] 在 `server.py` 新增 `/p/{project_id}/studio` 頁面路由。
- [ ] 完成頂部簡潔導覽列與六大分頁標籤切換。
- [ ] 綁定現有 `GET /api/projects` 與 `GET /api/project/{id}/state`，將劇本、風格色票、CLP、分鏡膠卷、專案管理控制台與成本排行完整渲染。
- [ ] 完成圖片/肖像點擊彈出全螢幕大圖燈箱（Lightbox）。

### 第二階段（機械性動作與輕量互動 - 工具閉環）
- [ ] 在 `server.py` 加入九宮格裁切端點（Pillow 幾何切片）與風格手冊另存端點（`save_playbook`）。
- [ ] 實作單鏡頭輕量重繪端點（途徑 A：調用 BaseTool 生成新 Take）。
- [ ] 於鏡頭卡片加裝互動按鈕、Takes Carousel 歷史版本切換與微光加載動畫。
- [ ] 驗證 SSE 0.1 秒極速刷新體驗。

### 第三階段（高級編排與長課程閉環 - 旗艦功能）
- [ ] 完善 `directives.json` 非同步指令佇列與 Checkpoint 審批狀態雙向同步。
- [ ] 實作單鏡頭局部抽換（Shot Patching）之剪輯決策記錄與 `video_compose` 三明治開窗合成接縫平滑處理。
- [ ] 驗證長課程微單元管線（Course Manifest ➔ Micro-pipeline ➔ Master Stitching 一鍵縫合）完整全流程。
