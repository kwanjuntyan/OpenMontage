# OpenMontage CLP（Character, Location, Prop）影視工業級體系重構總體架構方案

> **文件版本**：v2.0（正式重構總綱）  
> **編制團隊**：OpenMontage 核心架構組 & Antigravity  
> **審查委託**：GPT-5.6 首席系統架構審查官  
> **狀態**：方案編制完成，等待人類審核（Pending User Review）

---

## 壹、 執行摘要與重構願景（Executive Summary & Vision）

### 1. 現狀瓶頸剖析
OpenMontage 原有的視覺一致性機制是由 2D 向量偶骨架（`character_design`）衍生改造而來。在面對現代影視大模型（如 ByteDance Seedance 2.0、Google Veo 3.1、Kling 1.5）時，面臨三大根本性瓶頸：
1. **實體模型混淆**：將「道具（Prop）」甚至「場景（Location）」視為「人物（Character）」的附屬配件，導致無法表達「無人空鏡頭」、「室內外場景更迭」以及「關鍵道具跨角色流轉」。
2. **上游升級污染（Upstream Pollution）**：直接在原作者專供 2D SVG Puppet 偶骨架的命名空間中疊加影視字段，將導致未來 `git pull / rebase upstream/main` 時面臨嚴重的代碼與 Schema 衝突。
3. **多模態槽位與劇本強耦合**：若在劇本中硬編碼 `@Amy` 等符號來控制是否鎖臉，既破壞了劇本純淨性（干擾 TTS 語音朗讀與字幕時間軸），又無法應對各大影片模型極度嚴苛的多模態參考圖槽位上限（Seedance 2.0 支援 9 圖、Veo 3.1 僅支援 2 圖、Runway 僅支援 1 圖）。

### 2. 重構終極目標
建立具備好萊塢影視工業標準的 **「CLP（Character, Location, Prop）三位一體資產管線」**：
* **實體平級解耦**：角色（人物/吉祥物/講師）、場景（環境/攝影棚）、道具（劇情道具/核心架構圖/產品模型）三大實體平級分立。
* **管線單向不可變**：劇本保持純自然語言，實體參照由 CLP 階段的「參照政策（Reference Policy）」獨立控制。
* **確定性與零摩擦**：確立「作法二（常態納入 + 零實體自動放行）」，影視管線嚴格卡關定裝，解說管線按需啟用、零實體秒速放行。
* **工業級全系統閉環**：深度貫穿 Contracts、Skills、Tools、Backlot 看板、Checkpoint 狀態機、GCS 雲端資產庫、預算記帳與下游模型槽位適配器。

---

## 貳、 核心架構設計原則（Architectural Principles）

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           核心架構四大基石                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. 上游衛生 (Upstream Hygiene)      │ 2. 單向不可變 (Pipeline Immutability) │
│    還原 2D 偶骨架，建立獨立 CLP 契約 │    劇本純自然語言，參照由 CLP 政策控制 │
├─────────────────────────────────────┼───────────────────────────────────────┤
│ 3. 確定性與零摩擦 (Approach 2)       │ 4. 多模態槽位智慧預算 (Slot Budgeting)│
│    管線常態納入，零實體 0.1 秒秒速放行│    動態降級裁切，語義編譯 <IMAGE_REF> │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 原則一：上游代碼衛生（Upstream Hygiene & Zero Merge Conflicts）
* **決策**：將原系統的 `character_design` 完全還原為原作者專屬的 2D 向量骨架語義（供 `character-animation` 管線使用）。
* **隔離**：建立全新的獨立合約 [`schemas/artifacts/clp_manifest.schema.json`](file:///d:/kj-openMontage/schemas/artifacts/clp_manifest.schema.json)（Version 2.0），所有影視、寫實、3D 生成全面遷移至 `clp_manifest` 命名空間。
* **效果**：未來無論官方上游如何重構 2D 動畫系統，本系統均能實現 **零代碼衝突、無痛 Rebase 升級**。

### 原則二：關注點分離與管線單向不可變（Pipeline Immutability & Decoupling）
* **劇本文字只讀（Script Read-Only）**：劇本審批通過後即凍結。劇本只負責「故事內容與對白」，不引入 `@Amy`、`#Lab` 等程式標記。
* **實體候選萃取（Candidate Extraction）**：`script-director` 產出劇本時，在 `script.json` 底部自動附加 `detected_entities` 候選清單。
* **政策解耦（Reference Policy）**：是否生成參考圖、是否鎖定畫面，完全由 CLP 階段的開關決定，**絕不反向修改劇本任何一個字**，保障 TTS 配音與字幕時間軸的絕對純淨。

### 原則三：確定性管線與零實體自動放行（Approach 2: Always in Pipeline + Zero-Entity Auto-Bypass）
* **靜態 DAG 編排**：管線 YAML 採用固定的單向有向無環圖（DAG），不引入複雜易錯的動態跳關邏輯。
* **自適應分流**：
  * **影視類管線（`cinematic`）**：預設啟用人類審查閘門（`human_approval_default: true`），定裝完成必須經人類在 Backlot 簽核。
  * **非純故事管線（`animated-explainer`）**：
    * 若需要固定架構圖、核心產品或吉祥物：停在看板等待審批。
    * 若檢測到實體數為 0（純文字動效）：系統寫入空清單，**0.1 秒自動標記 Completed 靜默放行**，零摩擦直接進入分鏡。

### 原則四：多模態槽位智慧預算（Multimodal Slot Budgeting）
* 針對 Seedance 2.0（9 圖）、Veo 3.1（2 圖）、Runway（1 圖）等模型的物理限制，模型適配層（Adapter）內建降級優先級演算法（主角 > 場景 > 道具）。超限實體自動平滑降級為純提示詞錨點（`prompt_anchor`），杜絕 API 報錯崩潰。

---

## 參、 系統實體模型與契約規格（Data Model & Contracts）

全新契約定義於 [`schemas/artifacts/clp_manifest.schema.json`](file:///d:/kj-openMontage/schemas/artifacts/clp_manifest.schema.json)，將三大實體平級分立：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "openmontage/artifacts/clp_manifest",
  "title": "CLP Manifest",
  "type": "object",
  "required": ["version", "project_id", "characters", "locations", "props"],
  "properties": {
    "version": { "type": "string", "const": "2.0" },
    "project_id": { "type": "string" },
    "decision_log_ref": { "type": "string" },

    "characters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "visual_traits", "policy"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z0-9_-]+$" },
          "name": { "type": "string" },
          "role": { "type": "string" },
          "age": { "type": ["integer", "null"] },
          "gender": { "type": "string" },
          "visual_traits": { "type": "string" },
          "costume": { "type": "string" },
          "voice_id": { "type": "string" },
          "image": { "type": "string" },
          "gcs_url": { "type": "string" },
          "prompt_anchor": { "type": "string" },
          "policy": { 
            "type": "string", 
            "enum": ["strict_reference", "text_anchor_only", "ignore"],
            "default": "strict_reference" 
          }
        }
      }
    },

    "locations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "environment_description", "policy"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z0-9_-]+$" },
          "name": { "type": "string" },
          "environment_description": { "type": "string" },
          "lighting": { "type": "string" },
          "palette": { "type": "array", "items": { "type": "string" } },
          "interior_exterior": { "type": "string", "enum": ["interior", "exterior", "abstract"] },
          "image": { "type": "string" },
          "gcs_url": { "type": "string" },
          "prompt_anchor": { "type": "string" },
          "policy": { 
            "type": "string", 
            "enum": ["strict_reference", "text_anchor_only", "ignore"],
            "default": "strict_reference" 
          }
        }
      }
    },

    "props": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "description", "policy"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z0-9_-]+$" },
          "name": { "type": "string" },
          "category": { "type": "string", "enum": ["hero_prop", "diagram_asset", "product_mockup", "set_dressing"] },
          "description": { "type": "string" },
          "material": { "type": "string" },
          "image": { "type": "string" },
          "gcs_url": { "type": "string" },
          "prompt_anchor": { "type": "string" },
          "policy": { 
            "type": "string", 
            "enum": ["strict_reference", "text_anchor_only", "ignore"],
            "default": "strict_reference" 
          }
        }
      }
    }
  }
}
```

---

## 肆、 跨子系統串聯架構（Subsystems Integration Matrix）

CLP 重構並非孤立的腳本，而是深度穿透 OpenMontage 的 8 大核心子系統：

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OpenMontage 8 大核心子系統串聯架構                        │
└─────────────────────────────────────────────────────────────────────────────┘
  ① Contracts      ➔ schemas/artifacts/clp_manifest.schema.json 契約註冊與校驗
  ② Skills         ➔ skills/pipelines/cinematic/clp-director.md 實體萃取與分配
  ③ Tools          ➔ tools/image/ (FLUX.1, Imagen 3, Recraft) 高清定裝圖生成
  ④ Backlot UI     ➔ backlot/ui/board.js 三大展示櫃、鎖定標籤與單卡局部重抽
  ⑤ State Machine  ➔ lib/checkpoint.py 檢查點閘門守護 (human_approval_default)
  ⑥ Storage & GCS  ➔ projects/<id>/assets/clp/ 規範目錄與跨專案共享庫 (shared_clp/)
  ⑦ Cost & Audit   ➔ tools/cost_tracker.py 計費記帳與 decision_log.json 審計
  ⑧ Model Adapters ➔ scene_plan 語義繫結與 Seedance/Veo 多模態槽位降級編譯
```

### 1. Contracts（合約層）
* 註冊於 `schemas/artifacts/__init__.py`，通過 `validate_artifact("clp_manifest", ...)` 校驗。
* 支援空清單（`characters: []`）邊界，相容無實體科普片。

### 2. Skills（導演知識庫層）
* 新增 [`skills/pipelines/cinematic/clp-director.md`](file:///d:/kj-openMontage/skills/pipelines/cinematic/clp-director.md)：
  * 指導 Agent 讀取 `script.json` 萃取實體候選；
  * 指導 Agent 呼叫生圖工具產出無背景或乾淨布景的定裝概念圖；
  * 評估各實體的劇情重要性，指派 `strict_reference` 或 `text_anchor_only`。

### 3. Tools（工具層）
* 透過 `image_selector` 調度底層生圖引擎（FLUX.1-dev、Google Imagen 3），根據美學指令產生高保真定裝照。

### 4. Backlot UI & Server（Web 互動看板層）
* **三展櫃佈局**：在看板首頁渲染 `Characters`、`Locations`、`Props` 三個獨立卡片區。
* **卡片互動資訊**：展示預覽圖、實體名稱、描述特徵、GCS 雲端狀態徽章。
* **政策徽章**：以 `STRICT LOCK`（金/青色標籤）與 `TEXT ONLY`（灰色標籤）直觀展示參照模式。
* **單卡局部重抽（Partial Card Regeneration）**：支援使用者單獨針對某個不滿意的場景點擊「重新生成」，不破壞已審核通過的角色卡。

### 5. Checkpoint & State Machine（狀態機與閘門層）
* 在 `lib/checkpoint.py` 註冊：
  * `ALL_KNOWN_STAGES` 納入 `"clp"`。
  * `CANONICAL_STAGE_ARTIFACTS["clp"] = "clp_manifest"`。
* 嚴格執行 `human_approval_default: true` 閘門守衛，未獲核准嚴禁推進至分鏡與算圖。

### 6. Storage & Shared Asset Registry（儲存與雲端資產庫）
* **標準本地目錄結構**：
  ```text
  projects/<project-id>/
  ├── artifacts/
  │   └── clp_manifest.json
  └── assets/
      └── clp/
          ├── characters/     # 角色正面肖像 (PNG/WebP)
          ├── locations/      # 場景概念空鏡 (PNG/WebP)
          └── props/          # 關鍵道具與架構圖 (PNG/WebP)
  ```
* **跨專案/跨集數資產共用（Shared CLP Registry）**：
  * 透過 `lib/gcs_storage.py` 與 `scripts/sync_clp_to_gcs.py`，將資產鏡像至雲端 `shared_clp/`。
  * 製作連續劇第二季或系列課程時，直接按實體 ID 引用上一季已確認之資產，無需重複花費算力生圖。

### 7. Cost Tracker & Decision Log（預算記帳與決策審計）
* 定裝圖生成成本精確計入 `projects/<id>/artifacts/cost_log.json`，受專案總預算限額約束。
* 美術風格、調色盤與模型選擇記錄於 `decision_log.json`，供後續分鏡導演與生片導演精準繼承。

### 8. Downstream Model Adapters（下游模型槽位降級編譯器）
* **分鏡語義繫結（`scene_plan.json`）**：
  ```json
  {
    "shot_id": "shot_03",
    "clp_bindings": {
      "location": "loc_boardroom",
      "characters": ["char_harrison", "char_amy"],
      "props": ["prop_audit_contract"]
    }
  }
  ```
* **多模態槽位預算分配演算法（Slot Allocation Algorithm）**：
  * 當前鏡頭實體數 > 模型可用槽位（如 Veo 僅 2 槽，而實體有 4 個）：
    1. **Slot 1**：分配給最核心主角（`char_harrison`）；
    2. **Slot 2**：分配給主場景（`loc_boardroom`）；
    3. **降級**：次要角色 `char_amy` 與道具 `prop_audit_contract` 自動降級為 Prompt 關鍵字錨點（`prompt_anchor`）。
* **Prompt 標籤自動編譯**：
  在 Seedance 2.0 中自動編譯為：
  ```markdown
  [reference_image: clp_harrison.jpg, clp_boardroom.jpg]
  [identity_lock] Mr. Harrison <IMAGE_REF_1>, age 55, bespoke navy suit.
  [location_lock] Executive Boardroom <IMAGE_REF_2>, overcast daylight, floor-to-ceiling glass.
  Amy (young female scientist) stands nearby, holding a black leather audit contract folder.
  ```

---

## 伍、 管線編排與流轉時序（Pipeline Sequencing）

### 1. 故事影視管線（`cinematic.yaml`）
```text
[Idea/Proposal] ──> [Script 劇本] ──> [CLP 定裝鎖定] ──(人機審批)──> [Scene Plan 分鏡] ──> [Assets 生片] ──> [Edit] ──> [Compose]
                                             │
                                   Backlot 看板展示 C/L/P
                                   使用者簽核通過才放行
```

### 2. 科普解說管線（`animated-explainer.yaml` - 作法二落地）
```text
[Idea/Proposal] ──> [Script 劇本] ──> [CLP 實體檢測] 
                                             │
                      ┌──────────────────────┴──────────────────────┐
                      ▼                                             ▼
             【檢測到實體數 > 0】                            【檢測到實體數 = 0】
         (例如: 固定架構圖/產品模型/吉祥物)                  (純快節奏文字、圖表與動效)
                      │                                             │
             產出圖片並於 Backlot 審批                     寫入空清單 {"props": []}
                      │                                    0.1 秒自動 Completed 秒速放行
                      ▼                                             ▼
               [Scene Plan 分鏡] <──────────────────────────────────┘
```

---

## 陸、 實施計畫藍圖（Roadmap & Milestones）

本計畫分為 4 個清晰階段，每階段均具備嚴格的測試交付指標：

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 階段一：契約與上游解耦 (Upstream Separation)                                 │
│  - [DONE] schemas/artifacts/clp_manifest.schema.json (V2.0 獨立合約)        │
│  - [DONE] schemas/artifacts/__init__.py 全域註冊                            │
│  - [DONE] lib/checkpoint.py ALL_KNOWN_STAGES 註冊                           │
│  - [DONE] 還原 2D 偶骨架 character_design 純潔性                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 階段二：管線編排與導演技能 (Pipelines & Director Skills)                    │
│  - [DONE] pipeline_defs/cinematic.yaml 注入 CLP (強制審批)                  │
│  - [DONE] pipeline_defs/animated-explainer.yaml 注入 CLP (作法二自適應)     │
│  - [DONE] skills/pipelines/cinematic/clp-director.md 實裝                   │
│  - [TODO] skills/pipelines/cinematic/scene-director.md 擴充實體繫結         │
│  - [TODO] skills/pipelines/cinematic/asset-director.md 實裝槽位降級編譯器    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 階段三：Backlot 看板三展櫃與互動 (UI & State Machine)                       │
│  - [TODO] backlot/state.py 實裝 _derive_clp() 解析三實體                    │
│  - [TODO] backlot/ui/board.js & board.css 實裝三展櫃與 STRICT LOCK 標籤     │
│  - [TODO] backlot/ui/board.js 支援單卡局部重抽 (Partial Card Regeneration)  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 階段四：雲端存儲與雙實機 E2E 驗證 (Cloud Sync & Verification)               │
│  - [TODO] lib/gcs_storage.py & scripts/sync_clp_to_gcs.py 支援跨專案資產庫  │
│  - [TODO] 自動化契約測試 (pytest tests/contracts/)                          │
│  - [TODO] 實機 E2E 驗證：影視片《ESG永續風暴》+ 科普片《鼴鼠的星空》雙驗證   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 柒、 驗證計畫（Verification Plan）

### 1. 自動化測試驗證（Automated Verification）
* `pytest tests/contracts/test_pipeline_catalog.py`：驗證所有管線 YAML 結構合法，且技能指標 100% 存在。
* `pytest tests/contracts/test_clp_manifest.py`：專門針對 `clp_manifest` 測試：
  1. 正向用例：三實體齊全、帶有完整欄位與 GCS URL；
  2. 邊界用例：空陣列相容測試（`characters: []`, `locations: []`, `props: []`）；
  3. 負向用例：缺少必要鍵值、非合法 Policy 列舉值時堅決拋出 `ValidationError`。

### 2. 實機端到端場景驗證（Manual E2E Scenarios）
* **測試場景 A（電影短片《ESG 永續風暴》- `cinematic`）**：
  * 驗證劇本萃取 2 角色（Harrison、Amy）、1 場景（倫敦會議室）、1 道具（ESG 稽核合約）。
  * 驗證 Backlot 看板正確顯示三個展示櫃，並成功卡在 `awaiting_human` 門禁。
  * 驗證人類審批通過後，`scene_plan` 與 Seedance 提示詞編譯器成功編譯 `<IMAGE_REF>`。
* **測試場景 B（科普解說《鼴鼠的星空》- `animated-explainer`）**：
  * 測試 1（零實體純動效）：驗證 CLP 階段 0.1 秒自動 Completed 綠燈放行，完全不彈窗打擾。
  * 測試 2（鎖定特定圖表）：在劇本中加入固定天文圖表，驗證系統精準捕捉並在 Props 展櫃等待審批。

---

## 捌、 GPT-5.6 審查委託與對齊（Review Bridge）

本方案已同步在 [`REVIEW_BRIDGE.md`](file:///d:/kj-openMontage/REVIEW_BRIDGE.md#L442) 之「模組六」開闢專用審查通道，提請 GPT-5.6 針對以下 6 個關鍵架構挑戰進行紅藍對抗：
1. **上游衛生與長期維護性**（零代碼衝突驗證）
2. **多模態槽位預算與降級裁切策略**（多實體超限時之優先級保護）
3. **作法二狀態機死鎖防範**（免審批特權與閘門鎖定的並發安全性）
4. **Backlot 局部重抽狀態一致性**（單卡重抽對 Manifest 哈希之影響）
5. **極端光影與視角適應**（避免強綁定引發之畫面撕裂）
6. **跨專案資產共用之快取一致性**（Immutable Versioning 防歷史重放被破壞）

*(本方案待人類使用者 Review 確認後，方才啟動後續實作)*


---

## 玖、 針對 GPT-5.6 審查意見與「Amy 多造型」之專項落地架構

### 1. 角色本體與造型變體分層架構（Identity vs. Look Variants）
徹底解決「角色換裝」與「雲端 CAS Hash 定址」的相容問題：
* **角色本體（Core Identity）**：鎖定人物不變項（五官、臉骨幾何、眼眸特徵、Voice ID），全劇唯一。
* **造型變體（Look Variants / Wardrobes）**：每一套服裝（實驗室白袍、晚宴禮服、運動服）作為獨立子物件，擁有專屬的二進位 `asset_sha256` 快照與提示詞錨點。
* **分鏡按鏡頭綁定（Shot Binding）**：`shot_01` 綁定 `char_amy@lab_coat`，`shot_15` 綁定 `char_amy@evening_gala`；未宣告則自動回退至 `default_look`。
* **專案鎖（Project Lock）**：`clp.lock.json` 鎖死本專案各鏡頭所引用的確切造型 Digest，杜絕歷史專案因第二季改版而破壞。

### 2. 四大 P0 阻斷點之防護機制清單
1. **P0-1（Fail-Closed 契約）**：廢除任何靜默 `continue`，manifest 宣告但未載入 schema 之 artifact 一律拋錯阻斷。
2. **P0-2（型別化免審條件，解決狀態機死鎖）**：狀態機引入 `gate_resolution: { mode: "policy_bypass", rule_id: "clp_literal_empty_v1", actor_type: "system" }`，僅三實體字面為空時合法放行，看板標註 `AUTO-PASSED · ZERO ENTITIES`，杜絕 Gate Violation 死鎖。
3. **P0-3（嚴禁暗降級）**：人類核准之 `strict_reference` 超出模型物理槽位上限時，系統一律回傳 `UNSATISFIED_REFERENCE_CONSTRAINTS` 阻斷，提示使用者拆鏡或換模型；僅 `soft` 實體允許動態降級。
4. **P0-4（CAS 內容定址）**：雲端資源全面以 `shared_clp/cas/sha256/<2hex>/<64hex>.png` 儲存，專案 `clp.lock.json` 釘死精確 generation 與 hash。

### 3. P1 影視與架構優化
1. **Sidecar 劇本保護**：劇本 100% 保持純自然語言，萃取實體由 `artifacts/clp_candidates.json` 承載並綁定 `source_script_sha256`。
2. **光影與幾何分離**：提示詞編譯器注入 `LIGHTING TRANSFORM`（明示參考圖僅供幾何五官，依世界光重新打光），極端角度前置生成「橋接幀（Bridge Keyframe）」。
3. **Backlot 冪等局部重抽**：重抽請求攜帶 `If-Match: <digest>` 與 `Idempotency-Key`，更新單一 leaf 並發布新 root digest，舊 leaf 與歷史版本安全保留。


---

## 拾、 最終共識定案：單集一套經典定裝（One Signature Look）架構

經架構紅藍對抗與用戶確認，本系統在第一階段正式確立極簡、可靠的工業級標準：
1. **單集一角色一套定裝**：1 個角色 = 1 張臉部與服裝合一的高清定裝照（Face + Outfit Composite Master），避開所有多造型嵌套死角。
2. **多模態槽位直連**：單一圖片直接填入 Seedance / Veo 參考槽位，大模型絕不發生人臉與服裝張冠李戴。
3. **CAS 內容定址**：圖片二進位 Hash 唯一，專案 `clp.lock.json` 鎖定歷史，永不崩塌。
4. **狀態機型別化免審**：非故事片零實體時 0.1 秒留下 typed evidence 放行，杜絕 Gate Violation。
5. **嚴禁暗降級**：人類核准的強鎖定超出模型槽位時堅決報警阻斷，禁止背著人類偷偷降級。
