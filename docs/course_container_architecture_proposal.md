# OpenMontage 長影片五層次架構與課程容器 (Course Container) 改造提案

**文檔狀態**：提案徵詢稿 (RFC - Request for Comments)  
**目標版本**：OpenMontage v0.6.0  
**提案日期**：2026-09-15  
**關聯文件**：
- [`docs/studio_draft.md`](studio_draft.md)
- [`skills/creative/long-form.md`](../skills/creative/long-form.md)
- [`skills/creative/video-stitching.md`](../skills/creative/video-stitching.md)
- [`lib/identity.py`](../lib/identity.py)
- [`backlot/state.py`](../backlot/state.py)

---

## 摘要 (Executive Summary)

本提案旨在解決 OpenMontage (以下簡稱 OM) 在跨入 **30~60 分鐘專業長課程（如企業培訓、線上學程）** 製作時所遭遇的核心架構瓶頸：

> **現狀矛盾**：OM 官方雖然在 [`skills/creative/long-form.md`](../skills/creative/long-form.md) 中規劃了優秀的長影片編劇與留存曲線規範（單章 2~4 分鐘），但其**有效容量被硬性限制在 8~15 分鐘（上限 5~6 個 Chapters）**。當面對 40~60 分鐘的巨型長課程時，既有規範無法直接線性擴展。

其根本癥結在於：現行 `long-form.md` 本質上仍是**「單一專案單體結構 (Monolithic Single-Project)」**——所有章節皆被塞入同一個 `script.json`、同一份 `scene_plan.json` 並由單一瀏覽器進程渲染。若要將容量擴大 4 倍（達到 40~60 分鐘），就**必須在架構上實體化「增加一個階層」**！

為此，本提案正式確立 **「五層次敘事與封裝式課程容器（5-Tier Course Container Architecture）」**：
- **概念與實體階層升格**：將單體專案升級為五階層體系：`Project (課程容器) ➔ Chapter (微管線單元) ➔ Sequence (敘事段落) ➔ Scene (場景空間) ➔ Shot (單一分鏡)`。
- **檔案物理結構封裝**：在 `projects/` 根目錄下實施「單一課程資料夾封裝」，內部收納 `course.json`、全域 `master_clp.json`、共用資產及 `chapters/` 微型管線，徹底避免目錄污染。
- **實施策略**：將本改造作為 **Phase 1 獨立核心驗證專案**，以極低代碼量（預計 < 150 行）完成後端資料契約與無損縫合測試，待 API 契約凍結後，再開展 Phase 2 的 Studio UI 開發。

---

## 一、專案目的 (Purpose & Objectives)

### 1.1 解鎖 long-form.md 的 15 分鐘極限，透過「增設階層」擴大系統容量
現行 OM 的 `long-form.md` 雖然提出了「章節切分（Chaptering）」概念，但該 Chapter 僅是單一 JSON 內的文字標籤。本專案的目的在於**在實體架構上正式增設 Chapter 階層**，打破「長片必須塞在單一 JSON 與單一渲染進程」的單體瓶頸，將 OM 的製作容量由 15 分鐘一舉釋放至 40~60 分鐘，同時完整保留 OM 原生在 2~3 分鐘微單元內「極致專注、高密度 Prompt、嚴格審查」的最高畫質優勢。

### 1.2 建立清晰優雅的五層次概念體系
將影視工業結構與教育學習科學標準化為五個階層：
$$\text{Project (全劇課程)} \longrightarrow \text{Chapter (微單元)} \longrightarrow \text{Sequence (敘事段落)} \longrightarrow \text{Scene (場景空間)} \longrightarrow \text{Shot (單一分鏡)}$$
明確各層級的責任邊界，並支援**向下相容的動態摺疊**（短影片省略 Chapter，長影片完整展開）。

### 1.3 終結檔案管理混亂，落實單一容器封裝 (Encapsulation)
讓「一門課程即一個資料夾」，母層維護全劇真理（大綱、風格、角色定裝），子層微型管線獨立運作，產出無損縫合母帶，兼顧本地磁碟整潔、極速備份歸檔與 UI 視覺清爽。

### 1.4 先地基後裝潢：凍結 API 契約以護航 Studio UI
將資料結構改造從龐大的 Studio 介面專案中抽離，作為獨立前置 POC。在無前端（Headless）環境下驗證路徑安全、狀態聚合與 Stream Copy 縫合，產出穩定可信的後端 API，避免未來 UI 專案陷入頻繁重工。

---

## 二、面臨挑戰與技術痛點 (Challenges & Root Cause Analysis)

### 2.1 現行 long-form.md 的天花板：為什麼現有架構無法直接擴展到 40 分鐘？
OM 現行的 [`skills/creative/long-form.md`](../skills/creative/long-form.md) 已經具備極佳的專業影視規範：
- 明訂最佳單一章節時長為 **2~4 分鐘**。
- 規範了留存曲線（Retention Curve）、30秒 Hook、150~160 WPM 教育語速與 -14 LUFS 音訊標準。
- 但其規格表第一行明確寫道：`DURATION: 8-15 min (sweet spot for most topics)`，章節上限為 **5~6 個 Chapters**。

**為什麼 OM 無法在現有架構下「直接把章節數增加到 15 個」以支援 40 分鐘？**
因為在現有架構中，`long-form.md` 的 Chapters 只是 `artifacts/script.json` 裡的 `sections[]` 陣列元素，它在物理上**並沒有獨立的專案生命週期**！
如果單純增加章節數而不增加實體階層，整支 40 分鐘的內容仍必須被打包進同一份 `scene_plan.json`、同一個 `asset_manifest.json`，並由單一 Remotion 進程渲染，這必然立即撞上以下三大物理鐵壁：

### 2.2 數據體積爆炸與大模型注意力崩塌 (The Prompt Explosion Dilemma)
* **長劇本階段**：一份 40 分鐘的劇本文稿約 8,000~10,000 字（約 6K~8K tokens），現代 LLM 具備百萬級 Context Window，在處理長劇本的情緒弧線與結構時毫無壓力。
* **分鏡生圖階段的雪崩式擴展**：
  - 40 分鐘影片包含約 400~480 個分鏡鏡頭。
  - 每個鏡頭在 OM 的嚴格標準下，需包含：鏡頭景別（Lens mm）、攝影運動、光影色溫、主體描述、角色特徵鎖定詞（Visual Locks）、背景細節、情緒意圖等，平均每個鏡頭 Prompt 需 250~300 tokens。
  - **總輸出需求**：$480 \times 250 = 120,000\text{ tokens}$。
  - **物理鐵壁**：當前所有頂級大模型（Claude 3.5 Sonnet、GPT-4o 等）的**單次最大輸出長度（Max Output Tokens）皆限制在 4K ~ 8K tokens 之間**。
  - **後果**：若試圖一次性生成全劇分鏡，模型必然會偷工減料、簡化描述、遺忘角色特徵，最終導致畫面風格劇烈漂移。

### 2.3 瀏覽器渲染進程的記憶體極限 (Chromium Render OOM)
* 40 分鐘 @ 30fps = **72,000 幀畫面**。
* 不管是 Remotion 還是 HyperFrames，底層皆調用無頭瀏覽器（Headless Chromium）逐幀渲染。
* 在單一渲染進程中連續繪製 72,000 幀的高解析度畫布與複雜 DOM 動畫，Chromium 的 V8 記憶體必定發生洩漏或膨脹，超過 4GB 上限即觸發 `Out of Memory (OOM)` 崩潰中斷。

### 2.4 檔案扁平化散落的維護災難 (Directory Namespace Pollution)
若在沒有頂層容器的情況下，單純將章節拆成多個獨立 Project：
```text
projects/
├── esg-course-ch01/
├── esg-course-ch02/
...
└── esg-course-ch15/
```
* **目錄混亂**：3 門課程就會產生近 50 個目錄，難以識別歸屬。
* **資產孤島**：講師定裝圖（CLP）、品牌 Logo、風格手冊被拷貝成 15 份；一旦講師換髮型，必須手動同步 15 次。
* **UI 崩潰**：Backlot 專案看板首頁會被 15 張子卡片淹沒，失去宏觀管理能力。
* **微調代價高**：修復第 2 章一句口誤，如果沒有容器統籌，必須手動重新串接各片段。

### 2.5 OM 現行架構的嚴格路徑約束 (Strict Single-Child Path Constraint)
OM 的 [`lib/identity.py`](../lib/identity.py) 實施了極為嚴格的路徑安全契約：
```python
def resolve_project_dir(root: str | Path, project_id: object) -> Path:
    # 強制 project_dir.parent == resolved_root，禁止任何深層子路徑
    if project_dir.parent != resolved_root or project_dir.name != safe_project_id:
        raise InvalidProjectIdError(...)
```
這意味著現行系統不允許 `projects/course_id/chapters/ch01` 這類二級路徑直接作為 `project_id` 傳入，必須有安全、優雅的適配機制。

---

## 三、架構對策 (Strategic Architecture & Solutions)

### 3.1 概念對策：五層次彈性架構與動態摺疊

#### 階層定義標準
| 階層名稱 | 英文標識 | 作用範圍 | 典型時長 / 規模 | 核心職責與產出 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 專案 / 課程** | `Project` | 全局頂層 | 15 ~ 60 分鐘 | 統籌長劇本大綱、情緒弧線、Master CLP、風格手冊、最終母帶串接。 |
| **2. 章節 / 微單元** | `Chapter` | 單元獨立管線 | 2 ~ 4 分鐘 | 獨立執行 micro-pipeline，承載最高 Prompt 注意力與完整自審機制。 |
| **3. 敘事序列** | `Sequence` | 章節內段落 | 45 ~ 90 秒 | 對應教學結構（破題 Hook、核心概念、案例解析、小結）。 |
| **4. 場景空間** | `Scene` | 空間或主題塊 | 10 ~ 30 秒 | 鏡頭群組，維持同一場景背景空間與主體對象。 |
| **5. 單一分鏡** | `Shot` | 物理鏡頭 | 2 ~ 6 秒 | 最底層原子單位，具備精確的景別、光影、Prompt、秒數與生成素材。 |

#### 3.1.2 命名空間對齊：消除 `long-form.md` 歷史包袱（Chapter ➔ Sequence 歸位）
* **歷史衝突成因**：OM 現行 `skills/creative/long-form.md` 借用了 YouTube 產品術語（YouTube 官方將播放器進度條時間戳稱為 "YouTube Chapters"），因此在其內容模板中隨手將 45~90 秒的小段落寫為 `[CHAPTER 1]`, `[CHAPTER 2]`。
* **致命威脅**：若維持原樣，當 Agent 被指派處理 Tier 2 的 Chapter 時，再讀到 `long-form.md` 說「一部影片包含 5~6 個 Chapters」，大模型極易觸發**無限套娃幻覺 (Nesting Hallucination)**，在單章內又生出子 Chapter，或輸出錯誤的 JSON 欄位導致校驗崩潰。
* **解決對策**：**全面修改 `skills/creative/long-form.md`**，將其內部的段落名詞精準歸位為 Tier 3 的 **`Sequence`（敘事段落）**：
  - `[CHAPTER 1] Foundation` ➔ `[SEQUENCE 1: 基礎構建]` (0:30 - 2:00)
  - `[CHAPTER 2] Complication` ➔ `[SEQUENCE 2: 機制深化]` (2:00 - 3:30)
  - `[CHAPTER 3] Key Insight` ➔ `[SEQUENCE 3: 總結交付]` (3:30 - 4:00)
* **Chapter 名詞之純化**：在全系統中，`Chapter` 專指 **Tier 2 的獨立微單元與資料夾 (`chapters/ch01`)**；而 YouTube 的時間戳則純化為發布階段的平台標籤（`metadata/chapters.txt`）。

---

### 3.2 物理對策：封裝式課程容器 (Course Container Pattern)

在檔案系統中，強制實施**「單一課程目錄封裝」**：

```text
projects/
└── esg-training-course/                   # ★ 頂層唯一的課程容器目錄
    ├── project.json                       # OM 標準專案識別標記
    ├── course.json                        # [New] 課程總排程 (Course Manifest)
    ├── master_clp.json                    # 全課程角色定裝標準 (Single Source of Truth)
    ├── style_playbook.yaml                # 全課程統一視覺風格規範
    │
    ├── shared_assets/                     # 全課程共用資產庫 (唯讀繼承)
    │   ├── instructor_portrait.png        # 講師標準肖像圖
    │   ├── brand_logo.svg                 # 品牌標誌
    │   └── theme_bgm.mp3                  # 全劇統一母帶襯樂
    │
    ├── chapters/                          # ★ 內部封裝的章節微型專案 (Micro-Projects)
    │   ├── ch01-climate-crisis/           # 獨立微型管線 1 (2~4分鐘)
    │   │   ├── artifacts/                 # 獨立的 script.json, scene_plan.json, asset_manifest.json
    │   │   ├── assets/                    # 獨立生成的影音素材片段
    │   │   └── renders/                   # 產出單章微單元 ch01.mp4 (相容 LMS)
    │   ├── ch02-carbon-tax-mechanisms/    # 獨立微型管線 2
    │   │   ├── artifacts/
    │   │   ├── assets/
    │   │   └── renders/                   # 產出 ch02.mp4
    │   └── ch03-corporate-action/         # 獨立微型管線 3
    │       └── ...
    │
    └── renders/                           # ★ 全課程最終成果交付區
        ├── chapters.txt                   # LMS / YouTube 相容之章節時間戳清單
        ├── course_full_master.mp4         # FFmpeg Stream Copy 無損縫合的 40 分鐘完整大片
        └── export_bundle.zip              # 全課程一鍵匯出包
```

---

### 3.3 技術實現方案：4 項極輕量修改 (總計 < 150 行代碼)

本提案堅持「不重複造輪子、不侵入核心工具、向下 100% 相容」三大原則：

#### 項目 1：新增資料契約 [`schemas/artifacts/course_manifest.schema.json`](../schemas/artifacts) (約 40 行 JSON)
定義 `course.json` 的 JSON Schema，強制約束：
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Course Manifest",
  "type": "object",
  "required": ["course_id", "title", "chapters", "master_clp", "style_playbook"],
  "properties": {
    "course_id": { "type": "string" },
    "title": { "type": "string" },
    "total_target_duration_seconds": { "type": "number" },
    "master_clp": { "type": "string" },
    "style_playbook": { "type": "string" },
    "chapters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "sequence_number", "title", "dir_name", "pipeline_type", "status"],
        "properties": {
          "id": { "type": "string" },
          "sequence_number": { "type": "integer" },
          "title": { "type": "string" },
          "dir_name": { "type": "string" },
          "pipeline_type": { "type": "string" },
          "target_duration_seconds": { "type": "number" },
          "status": { "type": "string", "enum": ["pending", "in_progress", "completed", "failed"] },
          "render_output": { "type": "string" }
        }
      }
    },
    "stitch_plan": {
      "type": "object",
      "properties": {
        "output_path": { "type": "string" },
        "export_chapters_txt": { "type": "boolean" },
        "audio_normalization": { "type": "string", "default": "-14 LUFS" }
      }
    }
  }
}
```

#### 項目 2：路徑安全層微調 [`lib/identity.py`](../lib/identity.py) (約 15 行 Python)
保留原有 `resolve_project_dir` 的嚴格檢查，新增支援二級章節安全解析的專用函式：
```python
def resolve_chapter_dir(root: str | Path, course_id: object, chapter_id: object) -> Path:
    """Resolve a secure contained chapter directory beneath a course container."""
    course_dir = resolve_project_dir(root, course_id)
    safe_chapter_id = validate_project_id(chapter_id)
    chapters_root = (course_dir / "chapters").resolve()
    chapter_dir = (chapters_root / safe_chapter_id).resolve()
    
    if chapter_dir.parent != chapters_root or chapter_dir.name != safe_chapter_id:
        raise InvalidProjectIdError(f"Chapter path escapes chapters root: {chapter_dir}")
    return chapter_dir
```

#### 項目 3：狀態彙整與辨識 [`backlot/state.py`](../backlot/state.py) (約 45 行 Python)
在掃描 `projects/` 目錄時：
* 若目錄內含有 `course.json`，判定為 `is_course = True`。
* 聚合所有子章節的秒數、完成狀態、花費與活動時間，組裝成「單一課程摘要物件（Course Summary）」，在 Backlot 首頁呈現單一卡片，並提供子章節清單端點。

#### 項目 4：新增編排技能指引 [`skills/pipelines/course-orchestrator.md`](../skills/pipelines) (Markdown 文檔)
引導 Agent 如何依照標準生命週期工作：
1. 長劇本分析 ➔ 切分章節大綱 ➔ 產出 `course.json`。
2. 鎖定全域 `master_clp.json` 與視覺風格。
3. 依序或並行調用現有管線（如 `animated-explainer`）在各 `chapters/` 內跑完生成。
4. 調用現成工具 `tools/video/video_stitch.py`，依照 `course.json` 的章節順序在 3~5 秒內以 Stream Copy (`-c copy`) 縫合為 `course_full_master.mp4`。

#### 項目 5：重構 [`skills/creative/long-form.md`](../skills/creative/long-form.md) 命名空間 (純 Markdown 文本微調)
* 消除歷史包袱：將檔案內部所有 `[CHAPTER 1]`, `[CHAPTER 2]` 與 `Chapter Length Rules` 改寫歸位為 **`[SEQUENCE 1]`** 與 **`Sequence Length Rules`**。
* 保留所有留存曲線、模式中斷、語速與音訊核心原則。
* 純化 `Chapter` 名詞專指 Tier 2 微單元目錄，徹底根絕大模型的「套娃嵌套幻覺」。

---

## 四、風險分析與防範對策 (Risk Analysis & Mitigations)

| 風險項目 | 風險等級 | 潛在後果 | 防範對策與緩解措施 |
| :--- | :---: | :--- | :--- |
| **命名空間二義性 (Namespace Ambiguity)** | 高 | 大模型混淆 Tier 2 Chapter (微課) 與 Tier 3 Sequence (段落)，觸發套娃嵌套幻覺或輸出錯誤 JSON 欄位導致驗證崩潰。 | 執行項目 5：徹底將 `long-form.md` 內部的 Chapter 名詞改寫歸位為 `Sequence`，在系統全流程 Prompt 中維持嚴格的術語唯一性。 |
| **音畫漂移 (Audio Drift)** | 中 | 拼接後的母帶在播放到第 35 分鐘時，出現字幕與語音不同步現象。 | 強制執行 [`video-stitching.md`](../skills/creative/video-stitching.md) 規範：所有章節輸出必須鎖定恆定影格率（CFR，`-vsync cfr`），統一音訊採樣率為 48,000Hz。 |
| **章節間角色長相走樣** | 中 | 第 1 章講師為黑髮西裝，第 4 章講師突然變成捲髮休閒服。 | 強制實施 `master_clp.json` 頂層繼承：各章節管線在 `clp` 階段**禁止自創角色**，一律引用母層的 `master_clp.json` 作為 Visual Locks。 |
| **路徑穿越安全隱患** | 低 | 惡意構造的章節名稱導致讀寫跳出 `projects/` 根目錄。 | 使用 Python `pathlib.Path.resolve()` 與 `relative_to` 雙重防禦檢查，任何符號連結（Symlink）或 `..` 語法直接中斷報錯。 |
| **短片向後相容退化** | 低 | 既有短片專案在改版後無法正常運行或報錯。 | 嚴格維持短片專案無 `course.json` 的原狀，所有核心工具（Tools）接口簽名保持 100% 不變，測試套件納入短片迴歸測試。 |
| **專案範圍蔓延 (Scope Creep)** | 高 | 在底層資料結構尚未驗證前，過早跳入寫 UI，導致前端頻繁崩潰重構。 | **嚴格落實二階段分期**：Phase 1 僅限無頭 CLI 驗證，禁止任何 UI 代碼進入；Phase 1 驗收通關後才允許啟動 Phase 2。 |

---

## 五、預期效益與投資回報 (Expected Benefits & ROI)

```
┌────────────────────────────────────────────────────────────────────────┐
│                          專案效益矩陣                                    │
│                                                                        │
│   商業與產品價值                            工程與系統價值               │
│  ┌───────────────────────────────┐        ┌───────────────────────────┐│
│  │ 1. 突破 15 分鐘上限，直取     │        │ 1. 核心工具零翻修，        ││
│  │    40~60 分鐘專業高價企業課。 │        │    向下 100% 完美相容。    ││
│  │ 2. 雙交付形態：微單元微課     │        │ 2. 增量渲染 (Dirty Render)││
│  │    (LMS) + 40分完整大片 (YT)。 │        │    改一處只需重算 2 分鐘。 ││
│  │ 3. 專案封裝完整，一鍵備份     │        │ 3. 凍結 API 契約，為      ││
│  │    遷移，零遺漏風險。         │        │    Studio UI 打造堅實地基。││
│  └───────────────────────────────┘        └───────────────────────────┘│
└────────────────────────────────────────────────────────────────────────┘
```

1. **產品競爭力大幅躍升**：
   使 OpenMontage 從「短影音生成玩具」正式升級為「具備製作系統化專業學程能力的長篇影視引擎」。
2. **極致的渲染效率與低維護成本 (Dirty Re-render)**：
   過去 40 分鐘單體影片改動一個錯字，需重繪 72,000 幀（耗時數小時且冒 OOM 當機風險）；現在改動第 2 章台詞，**只需重新生成第 2 章（3分鐘）**，父層利用 FFmpeg Stream Copy 於 **3 秒內**完成無損拼接更新！
3. **目錄整潔度提升 90%**：
   磁碟目錄結構井井有條，一門課一個資料夾，使用者與檔案管理系統再無迷航困擾。
4. **開發風險大幅降低**：
   以百餘行代碼的微型投資（Phase 1），提前消除長片生成崩潰的架構隱患，並為後續 Studio UI 奠定完全確定的資料接口。

---

## 六、實施步驟與驗收標準 (Implementation Plan & Acceptance Criteria)

### 6.1 實施步驟 (兩階段劃分)

#### 【Phase 1：長課程容器核心 POC 驗證】（本提案聚焦範圍，預計 1~2 天）
1. **Schema 落地**：建立 `schemas/artifacts/course_manifest.schema.json`。
2. **路徑適配**：在 `lib/identity.py` 加入 `resolve_chapter_dir` 安全解析。
3. **狀態聚合**：在 `backlot/state.py` 加入對 `course.json` 的辨識與資料聚合。
4. **命名空間歸位**：重構 `skills/creative/long-form.md`，將內部段落模板由 Chapter 改寫為 Sequence。
5. **編排技能**：編寫 `skills/pipelines/course-orchestrator.md`。
6. **端到端無頭驗證**：建立一個包含 2 個極短章節（各 10 秒）的測試課程容器，執行管線生成並透過 `video_stitch` 成功輸出完整母帶。

#### 【Phase 2：Studio UI 專案開展】（待 Phase 1 驗收後啟動）
1. 依據凍結的 `course_manifest` 接口，實作 Studio 導航列的「課程/章節下拉選單 (Chapter Drawer)」。
2. 在工作區一提供「課程大綱與章節劇本切換面板」。
3. 在工作區三落實「全域 Master CLP 與子章節定裝繼承」。
4. 串接 HUD 顯示全課程總進度條與各章節微進度。

### 6.2 Phase 1 驗收標準 (Definition of Done)
1. **目錄封裝性**：執行完測試後，`projects/` 根目錄僅新增一個 `test-course/` 資料夾，子章節皆被約束在 `chapters/` 內。
2. **路徑安全性**：單元測試驗證 `resolve_chapter_dir` 能有效攔截非法路徑逃逸。
3. **向下相容性**：既有單元測試（特別是 `tests/contracts/test_identity_contract.py`）全數 100% 通過。
4. **無損縫合產出**：成功產出 `course_full_master.mp4` 與 LMS 相容的 `chapters.txt`，播放無卡頓、音畫無漂移。

---

## 結論與建議

本提案不追求大規模重寫系統，而是以極度收斂、精準的「外層封裝模式」，同時化解了大模型注意力上限、瀏覽器記憶體瓶頸與本地檔案管理的痛點。

**強烈建議優先核准並執行 Phase 1 核心驗證專案**，確認資料契約與無損縫合完全可行後，再全力展開 Studio UI 的視覺開發。
