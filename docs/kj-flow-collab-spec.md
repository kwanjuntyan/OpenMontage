# KJ Flow Collaboration — 持續維護規格

- **狀態：** v3 — 包含設計歷史的現行產品規格；尚未批准實作
- **最後更新：** 2026-09-21
- **建議基準：** 待定。`08e2151` 是目前的建議，但尚未正式批准。
- **規格權威：** 第 1–9 節及第 11 節中狀態為「已確認」的項目構成現行規格。第 0 節記錄設計理由與演進過程，但不得推翻現行規格，也不得自行解決待確認問題。若對話歷史或 repository 技術證據與本文件衝突，以現行規格為準。新討論只有在明確確認並更新本文件後，才會改變規格。

## 0. 起源、技術證據與設計演進

本節保存 KJ Flow Collaboration 出現的原因，以及現行設計的形成過程。本節屬於歷史與解釋性資料；若早期方案與第 1–9 節衝突，以現行章節及決策紀錄為準。

### 0.1 原始問題與成功條件

專案一開始以全自動 script-to-video 為目標。對處於原型階段的兩人團隊而言，這個方向逐漸累積了超出新工作流程需求的 Provider 自動化、復原機制、治理及生產控制系統。

因此產品方向改為：

- OM 繼續負責 script、CLP／reference 狀態、scene plan、Prompt Pack、回收素材准入、edit、audio、subtitle、compose 與 final render。
- 人工操作 Google Flow 及外部圖像生成工具。
- 個別 Unit 也可以改用既有 OM pipeline、外部同事、其他工具或人工準備的媒體。
- 所有可用成果都透過統一 delivery boundary 回到父層 OM 專案。
- 相較於企業級安全、IAM、自動 Provider 調度、完整可稽核性或生產規模 orchestration，優先追求快速可用與程式簡潔。

原始問題與對策的對照如下：

| 原始問題或限制 | 產品對策 |
|---|---|
| 兩人原型團隊沒有理由承擔大型生產控制系統。 | 使用薄層、選擇性啟用的協作 adapter，以及簡單的 Unit 工作清單。 |
| Google Flow 由人工操作，不是 OM Provider。 | 將人視為正式橋接者；匯出 Prompt Pack，再匯入人工選定的成果。 |
| 不同 Unit 可能由不同路徑製作。 | 每個 Unit 宣告 `production_method`，並共用同一套回收契約。 |
| 不同製作者之間的共用視覺與交付規則可能逐漸偏離。 | 中央化 CLP、風格、輸出規格、音訊／字幕政策、命名及連續性指示。 |
| OM 已具備可重用的 script 與後期製作能力。 | 直接重用既有 script、scene planning、asset manifest、edit、audio、subtitle、compose 與 render 行為。 |
| Phase F 研究有價值，但其操作與治理對本原型過重。 | 將它保存為唯讀證據，只吸收研究結論，不移植治理機制。 |
| Optional providers 不得改變一般 OM 行為。 | KJ Flow Collaboration 必須明確選用；沒有 CLP context 時維持既有預設行為。 |

設計從一開始就有明確上限：不新增 scheduler、queue、worker、orchestration engine 或為未來需求預先建設的基礎設施；主要新增模組不得超過五個、新 artifact 類型不得超過三種、正式人工確認點不得超過三個。

### 0.2 Phase F 封存與證據邊界

Phase F worktree 是封存的生產等級研究與證據來源。不得 reset、clean、刪除、覆寫、繼續開發，也不得把它當成實作工作分支。

初次唯讀稽核時，Git 登記的實際路徑是：

`D:\kj-openMontage\.pytest-tmp\pixar-course-pipeline`

當時它位於 `19b5bce`，包含 20 個 tracked 變更與 107 個 untracked 項目。這些數字只描述當時的稽核快照，不代表要求重新檢查或修改該 worktree。

Repository 內容與 Phase F 可以提供技術證據、範例及經驗，但不能推翻本文件已確認的產品方向。

KJ Flow Collaboration 從 Phase F 保留的研究結論只有：

- 人類是 OM 與 Flow 之間的正式橋接者；
- Prompt Pack 應區分共用規則與每 Unit 工作單；
- Flow rough cut 只是 review proxy，不是 canonical edit；
- importer 只做機械檢查，創意判斷保留給人；
- 父專案保留 canonical edit、compose 與最終發布權限。

Phase F 的 digest chain、promotion receipt、復原機制、Gate enforcement、Provider staging 及相關治理實作不納入本產品。

### 0.3 原始 Git 基準分析

最初以唯讀方式檢查三個候選 commit，目標只回答一個問題：哪個基準最適合保留一般 OM，同時只新增精簡 Flow 協作與 Unit 工作清單？

| 候選基準 | 當時的稽核證據 | 初始判斷 | 目前狀態 |
|---|---|---|---|
| `08e2151` | 原始上游 OM；稽核時有 2,115 個 tracked files、13 條 pipeline、167 個 tools。具備所需的 script、scene plan、edit、audio、subtitle 與 compose 能力，且未耦合 GCS、Batch V2、完整 PUP、正式 CLP 或 Workspace。 | 最符合需求，依賴面最小。它沒有正式 CLP，但可新增薄層、選擇性啟用的 CLP 能力。 | 建議採用，但尚未批准。參見 KJFC-019。 |
| `9d5e22a` | 相較 `08e2151` 多 14 個檔案，約 +1,770/-55 行；未實質改善本需求相關的 checkpoint、pipeline loader、compose、audio、subtitle、script 或 scene contract。 | 次選。個別修正有價值，但也加入 batch helper、Backlot CLP heuristic、Provider 探測，且沒有相應測試變更。 | 未選定；若日後實際需要，可再個別評估特定修正。 |
| `c693b0e` | 相較 `9d5e22a` 多約 375 個檔案及 +87,034/-530 行，包含大量 Batch V2、PUP、CLP、GCS 與 Workspace 程式；並改動核心 checkpoint、selector、manifest、scene plan 與 compose 介面。 | 對原型過於龐大，也難以保證一般 OM 的預設行為不變。 | 僅作研究來源，不建議作為精簡版基準。 |

初始分析建議 `08e2151`。這項建議有技術證據支持，但從未升格為正式批准的基準，因此 KJFC-019 仍是待確認問題。

稽核也發現 `08e2151` 以外可能有價值的個別變更，例如 Windows MIME 修正及 Vox style。這些內容被明確視為未來可選擇性評估的候選，而不是採用整個較重基準的理由。

### 0.4 最初提出的對策

第一輪方案將 `kj-flow-collab` 定位為 adapter／router，而不是新的生成引擎。它負責派送、回收及重新接上既有 OM 後期製作能力。

最初提出的 stage 順序是：

```text
script -> scene_plan -> dispatch -> collect -> edit -> compose
```

當時提出：

- 一份共用 plan，包含 CLP-lite、風格、delivery profile、命名、音訊／字幕政策及 Unit index；
- 一種可重複使用的 Unit work-order contract，人類可讀的 Flow Prompt Pack 只是其 projection；
- Flow、OM child pipeline、外部同事及 manual media 共用一套 delivery contract；
- project-local inbox，支援 dry-run 檢查及 no-overwrite 匯入；
- 讓核准的素材進入既有 `asset_manifest`；
- 直接重用既有 edit、audio、subtitle、compose 與 render 行為；
- 不建立 Flow、Omni 或 Veo 的自動 Provider 路徑。

最初提出的五個主要新增模組如下：

| 模組 | 第一輪歷史提案 |
|---|---|
| Pipeline declaration | 只新增 `pipeline_defs/kj-flow-collab.yaml`，不修改既有 manifest。 |
| Stage instructions | 新增一份可依 stage 運作的 collaboration director，引用既有 OM 方法而不複製整套能力。 |
| Contracts | 新增三份小型 schema，分別描述 plan、work order 與 delivery。 |
| Local adapter tool | 只提供 export、inbox inspection、delivery import 與 status。 |
| Tests | 新增 contract 與 adapter 測試，不建立生產等級治理框架。 |

以上只是規劃提案，不是實作授權。由於後續 CLP 討論證明「在 scene planning 之後才第一次建立 CLP」不可行，這些確切模組路徑與 artifact 組合目前都尚未批准。

最初的最小驗收案例是一段 45–60 秒、含三個 Unit 的課程片段：

- `u01`：`flow_manual`，回傳一支 hero video clip；
- `u02`：`om_pipeline: animation`，回傳一支圖解動畫；
- `u03`：`manual_media`，回傳同事提供的 B-roll。

預計驗證的內容是：一次 export 能驅動三種 production route；inbox inspection 可在不寫入 canonical assets 的前提下發現錯誤；通過確認的 scene-level media 能以 no-overwrite 方式進入既有 asset manifest；既有 edit／audio／subtitle／compose 能在不呼叫自動 Flow、Omni 或 Veo Provider 的情況下產生 final render。

原始風險及可刪減內容包括：

- 不使用 digest binding 時，dispatch 後若 scene ID 改變，所有受影響的 work order 必須重新 export；
- 不同製作者可能交付不同色彩、frame rate、resolution 或 audio 規格，應由既有 edit／compose conform，而不是另建第二套處理引擎；
- 父層 asset manifest 可能變大，原型階段可以接受；
- 不新增 concurrency lock；兩人團隊透過 Unit ownership 避免衝突寫入；
- Unit status 可以從檔案存在狀態推導，不一定持久化；
- 第一版可以只輸出 JSON，並只支援常見的 MP4、MOV、PNG 與 JPG；
- 不需要 Unit 專用的 Backlot UI。

### 0.5 討論如何修正最初方案

原始方案解決了 routing 與 delivery，但 CLP 的時序不符合預期創作流程。討論依下列順序演進：

| 步驟 | 問題或發現 | 形成的修正 |
|---|---|---|
| 1 | `08e2151` 是否已具備 CLP？ | 它沒有後期的正式 CLP 系統，但這不代表它不適合；可以加入小型、選擇性啟用的 CLP 能力，而不必移植重型實作。基準仍未批准。 |
| 2 | 是否應由 Flow 負責 CLP？ | 不應。OM 設計 Character、Location、Prop 的意圖及 Provider-oriented prompts；人工在外部生成圖片；OM 登記選定圖片與 canonical tags。 |
| 3 | 是否能在選定 CLP 圖片回到 OM 之前完成 scene planning？ | 對本工作流程而言不能。OM 必須先完成 CLP 登記，再定稿 scene plan 與 scene prompts。KJFC-003、KJFC-016 及 KJFC-018 記錄了這項修正。 |
| 4 | CLP 是否能只存在於 scene planning 之後才建立的 `kj_flow_plan`？ | 不能。原本的三-artifact 組合因此失效。替代 artifact 與 schema 仍在 KJFC-021、KJFC-022 中保持待確認。 |
| 5 | Scene 應如何使用 CLP？ | Scene planning 必須以結構化方式引用 CLP。`scene_plan.clp_refs` 這項概念已確認，但 exact schema 仍由 KJFC-023 保持待定。 |
| 6 | 誰擁有 tags 與 reference truth？ | OM 擁有 canonical identity、tags、選定 references 及 mapping。Provider 與 Flow 可以產生或消費候選內容，但不擁有 canonical CLP。此邊界由 KJFC-004 與 KJFC-024 規範。 |
| 7 | 既有 OM child pipelines 如何參與？ | 它們隨 Unit work order 收到由父專案產生的唯讀 CLP context，不得修改父專案 CLP，並透過統一 delivery contract 回傳成果。此結論成為 KJFC-035。 |
| 8 | 同意上述修正是否也代表所有 schema 都已定案？ | 不代表。外部等待的表示方式、CLP 與 `clp_refs` 的 exact shape、Flow work-order exact schema，以及 Git 基準仍是待確認問題。 |

因此，修正後的相對流程為：

```text
[既有 script 輸入或 script stage：待定]
  -> OM 設計 CLP
  -> 人工操作外部工具生成並選擇圖片
  -> OM 登記 CLP
  -> scene_plan 以結構化方式引用 CLP
  -> dispatch
  -> 外部或 child-pipeline 製作
  -> collect
  -> 既有 edit / audio / subtitle / compose
```

### 0.6 下一個 Agent 的閱讀與實作規則

後續 Agent 應依下列順序使用本文件：

1. 閱讀第 0 節，理解原始問題、技術證據及早期方案改變的原因。
2. 將第 1–9 節及決策紀錄中「已確認」的項目視為實作權威。
3. 將第 10 節及所有「已確認（細節待定）」項目視為未解決；不得自行發明 schema 或決定基準。
4. 使用第 12 節避免重新引入已被取代的 CLP 時序、權責或 artifact 假設。
5. 將第 0 節的初始模組清單、artifact 名稱及驗收案例視為設計歷史與限制，而不是實作許可。

本文件本身不構成實作、新分支或新 worktree 的授權。封存的 Phase F worktree 仍不在實作範圍內。

## 1. 目標與範圍

KJ Flow Collaboration 將目標從全自動 script-to-video，改為適合小型團隊的人類／AI 協作工作流程。

OpenMontage（OM）負責規劃及 canonical project state：script、CLP 定義與 references、scene planning、work orders、回收素材准入、asset manifest、edit、audio、subtitles、composition 與 final render。人類操作外部圖像生成器及 Google Flow、挑選可用成果，再將成果送回 OM。

`kj-flow-collab` 是一條必須明確選用的薄層 pipeline，負責 CLP 協作、Unit routing、work-order export、delivery collection，以及重新接上既有 OM 能力。它不是新的影片生成引擎，也不會自動操作外部 Provider。

長課程可以拆分成多個 Unit。Unit 只使用簡單工作清單，不建立 scheduling、queueing、worker 或 Production Unit Protocol 系統。

## 2. 現行端到端流程

```text
[既有 script 輸入或 script stage：待定]
  -> OM 設計 Character / Location / Prop 描述、tags、
     continuity rules 與 Provider-oriented image prompts
  -> 人工使用外部工具生成 CLP candidate images
  -> 將選定圖片送回 OM
  -> OM 登記 canonical CLP references 與 tags
  -> OM 使用結構化 CLP references 設計 scene_plan
  -> OM 匯出 shared instructions、Unit work orders 與 Flow Prompt Packs
  -> 人工確認點 1：Prompt Pack / 工作清單
  -> 每個 Unit 交由 Flow、既有 OM child pipeline、
     外部同事或 manual media 路徑製作
  -> 將選定圖片、clips、metadata 及 optional rough cuts 送回 OM
  -> OM 檢查 delivery
  -> 人工確認點 2：回收素材
  -> 核准的媒體進入既有 asset_manifest
  -> OM 重用既有 edit、audio、subtitle 與 compose 能力
  -> 人工確認點 3：final preview
  -> final render
```

Flow 可以產生 storyboard images、選定 clips 及 optional rough cut。Flow rough cut 只用於傳達剪輯意圖；永遠不會取代 OM 的 canonical edit timeline。

## 3. Pipeline 階段

已確認的相對順序為：

```text
[script 輸入或 script stage：待定]
  -> CLP 設計 / 外部生成 / OM 登記
  -> scene_plan
  -> dispatch
  -> collect
  -> edit
  -> compose
```

| Stage 或活動 | 責任 | 確認方式 |
|---|---|---|
| Script input／stage | 提供 canonical content basis。`kj-flow-collab` 是建立還是接收 script，仍待確認。 | 本規格尚未定義 |
| CLP | OM 設計 C／L／P prompts；人工在外部生成圖片；OM 登記選定 references 與 canonical tags。 | 尚未確認為獨立 Gate |
| Scene plan | OM 使用結構化 CLP references 規劃 scenes。 | 納入 Prompt Pack 確認 |
| Dispatch | 匯出 shared context、Unit work orders、Flow instructions、prompts 與 reference mappings。 | 確認點 1 |
| External production | 由人工操作 Flow、OM child pipeline、外部同事或 manual media 路徑製作。 | 不建立 OM execution engine |
| Collect | 在進入 canonical import 前，檢查回收媒體、scene mapping 與 delivery information。 | 確認點 2 |
| Edit | 重用既有 OM editing 與 timeline 行為。 | 不新增 Gate |
| Compose | 重用既有 audio、subtitle 與 composition 行為。 | 確認點 3 |

等待外部 CLP 生成期間的確切表示方式仍待確認。可能是一個維持 `in_progress` 的 `clp` stage、拆成多個 stages，或其他簡單表示方式；目前尚未定案。

## 4. CLP 生命週期

### 4.1 OM 設計

OM 設計 canonical Character、Location 與 Prop 意圖，包括：

- identity 與 visual description；
- continuity constraints；
- `must_preserve` 與 `must_avoid` 指引；
- draft tags；
- Provider-oriented prompts，例如提供給 Midjourney 或 Nano Banana 的 prompts；
- 後續 scenes 所需的 reference views 或 image roles。

OM 只需要建立 prompt 文字，不必呼叫外部 CLP Provider、不必替其處理認證，也不必自動調度。

### 4.2 外部生成與人工選擇

人類使用外部圖像生成工具、檢視候選結果，再將選定圖片送回 OM。外部工具負責產生 candidates，但不擁有 CLP truth。

### 4.3 OM 登記

OM 將選定圖片登記到 canonical C／L／P identity，並建立 canonical reference mapping。OM 也負責建立及維護 canonical CLP tags。人類或外部工具可以提供初步描述、candidate tags 或修正建議，但 scene planning 與 exported work orders 只能使用 OM 已登記的值。

確切 tag vocabulary 與 CLP schema 仍待確認。

### 4.4 Scene 與 Prompt Pack 的使用方式

Scene plan 必須以結構化方式引用 CLP。目前此產品概念稱為 `scene_plan.clp_refs`，但 exact JSON shape 尚未定案。

Prompt Pack exporter 會把各 scene 的 CLP references 解析成 Flow 或其他製作者需要的圖片、tags、continuity rules 與使用指示。

### 4.5 權責邊界

Flow 與 OM child pipelines 以唯讀方式消費 CLP context。它們可以使用 CLP 設計 prompts 與媒體，但不得重新定義或修改父專案的 canonical CLP。任何希望升格為新 CLP reference 的外部生成圖片，都必須先送回 OM 並完成登記。

## 5. Unit 路由與 `production_method`

每個 Unit 都必須宣告 `production_method`。已確認的最低支援集合為：

- `flow_manual`
- `om_pipeline: animation`
- `om_pipeline: cinematic`
- `om_pipeline: animated-explainer`
- `manual_media`

Unit 可以獨立完成，也可以交給其他同事。所有路徑都必須透過相同 delivery boundary 回傳，不得直接寫入父專案的 canonical assets。

### 既有 OM child pipelines 如何消費 CLP

既有 OM child pipelines 會隨 Unit work order 收到由父專案產生的唯讀 CLP context。它們在設計 prompts 與產生媒體時，可以使用 canonical CLP definitions、已核准 reference images、tags、continuity constraints 及 scene bindings。

Child pipelines 不得重新定義或修改父專案 CLP。其輸出必須透過 Flow 與外部同事共用的 delivery contract 回傳。未提供 CLP context 時，既有 child pipeline manifest 與預設行為維持不變。

## 6. 正式產物（Canonical Artifacts）

實作最多可以新增三種 artifact 類型。確切組合與 schema 仍待確認。

已確認的需求如下：

- CLP information 必須在 scene planning 前存在，而且可以被多個 Unit 與製作者重用。
- Scene plan 必須以結構化方式引用 CLP。
- Unit work orders 必須攜帶或能解析 shared production context。
- 回收媒體必須透過統一 delivery contract 進入。
- 核准的媒體必須進入既有 OM `asset_manifest`，不得建立替代 asset system。
- 應盡可能重用既有 `script`、`scene_plan`、`asset_manifest`、`edit_decisions`、`render_report`、audio、subtitle 與 composition contracts。

原本的 artifact 組合 `kj_flow_plan` + `kj_flow_work_order` + `kj_flow_delivery` 已不是現行方案，因為它把 CLP 放在 scene planning 之後。像 `clp_lite`、`kj_flow_work_order`、`kj_flow_delivery` 這類候選名稱仍只是提案，不是已批准的 schema。

## 7. 交接與交付契約

### 7.1 共用資訊

共用資訊必須中央化，不得由各 Unit 各自重新發明。內容包括：

- CLP definitions、已登記 references 與 tags；
- visual style；
- resolution、aspect ratio 及相關輸出設定；
- audio 與 subtitle policy；
- naming rules；
- common instructions 與 continuity constraints。

### 7.2 工作單語意

Flow 或 Unit work order 至少必須表達：

- Unit 與 scene identity；
- 相關 CLP entities 與 references；
- 每個 reference 的使用方式；
- scene prompt；
- continuity、preserve 與 avoid instructions；
- aspect ratio；
- target duration；
- requested variations；
- expected deliverables；
- acceptance criteria。

Exact schema、field names、required-field set、Flow aliases、model fields、credit fields 與 version fields 仍待確認。

### 7.3 交付語意

Flow、OM child pipelines、外部同事及 manual-media 路徑，必須透過統一 delivery boundary 回傳檔案。Delivery 必須保留足以把回傳檔案對應到父專案、Unit 及目標 scenes 的 identity。

最低必要 provenance、每個檔案是否必須只對應單一 scene，以及能否接受涵蓋多個 scenes 的 Unit master，都仍待確認。

Importer 可以執行本機機械檢查，並準備既有 `asset_manifest` entries。角色相似度、continuity、acting、composition 及教學品質等創意判斷，仍由人類／OM review 負責。

## 8. 人工確認點

正式人工確認點最多三個：

1. **Prompt Pack／工作清單** — 檢查已登記的 CLP context、scene plan、Unit routes、shared instructions 與 exported prompts。
2. **回收素材** — 在 canonical import 前檢查 Flow、child pipeline、外部同事與 manual-media 輸出。
3. **Final preview** — 檢查已組裝的 edit、audio、subtitles 與 final composition。

尚未批准為 CLP 圖片選擇新增第四個 Gate。CLP 選擇與登記如何納入三個確認點的限制，仍是待確認問題。

## 9. 不做項目

本專案不新增或啟用：

- Batch Executor V2；
- 完整 Production Unit Protocol；
- GCS Provider staging；
- Omni 或 Veo 自動生成路徑；
- IAM 或 credential management；
- CAS digests；
- request fingerprints；
- operation recovery 或 resume coordinator；
- candidate promotion；
- 多層 receipts；
- enterprise audit 或 governance systems；
- scheduler、queue 或 worker infrastructure；
- automatic Provider 或 model dispatch；
- Flow browser automation；
- automatic Flow credit approval；
- 第二套 canonical timeline 或 publication authority；
- 在既有 OM pipelines 強制啟用 CLP；
- 為未來需求預先建設的基礎設施。

若設計需要超過五個主要新增模組、三種新 artifact 或三個新 Gate，必須停止並回到更簡單的方案。

## 10. 待確認問題

| ID | 待確認問題 | 目前邊界 |
|---|---|---|
| KJFC-019 | 應採用哪個 Git 基準？ | 建議 `08e2151`，但尚未批准。 |
| KJFC-020 | 外部 CLP 等待期間應如何表示？ | 相對 stage 順序已確認；exact stages 與 checkpoint state 仍待定。 |
| KJFC-021 | 確切的三種新 artifact 是哪些？ | 原本的組合已被取代；尚未批准替代組合。 |
| KJFC-022 | CLP artifact 的確切名稱與邊界為何？ | 它必須在 scene planning 前可用；exact schema 仍待定。 |
| KJFC-023 | `scene_plan.clp_refs` 的 exact schema 為何？ | 結構化 scene-to-CLP reference 已確認。 |
| KJFC-024 | Canonical tag vocabulary 與 schema 為何？ | OM 擁有 canonical tags 的權責已確認。 |
| KJFC-025 | 回傳的 CLP 圖片應如何登記？ | 共用 delivery form 或直接 CLP inbox registration 都仍有可能。 |
| KJFC-026 | CLP 選擇如何納入三個確認點？ | 未批准新增 Gate。 |
| KJFC-027 | Character、Location、Prop 各自最低需要哪些 reference views？ | 尚未批准 mandatory view set。 |
| KJFC-028 | 哪些 Provider prompt dialects 屬於 first-class？ | Midjourney 與 Nano Banana 只是例子；固定或可擴充支援仍待確認。 |
| KJFC-029 | Flow work-order 的 exact schema 為何？ | 必要語意內容已確認；exact fields 仍待定。 |
| KJFC-030 | Flow delivery 必須提供哪些 provenance？ | Model、prompt、Flow media／version IDs 與 selection notes 尚未區分必要或選填。 |
| KJFC-031 | `kj-flow-collab` 是建立還是接收 script？ | Pipeline 入口仍待確認。 |
| KJFC-032 | Unit 的最低輸出粒度為何？ | Single-scene files 或 multi-scene Unit master 仍待確認。 |
| KJFC-033 | Unit status vocabulary 與 directory rules 為何？ | Persisted status 或由檔案推導 status 仍待確認。 |

## 11. 決策紀錄

| ID | 主題 | 目前決定 | 取代內容 | 狀態 | 日期 |
|---|---|---|---|---|---|
| KJFC-001 | 產品目標 | 使用人類／AI 協作工作流程；OM 負責規劃與組裝，人類操作外部工具與 Flow。 | 以全自動為主要目標 | 已確認 | 2026-09-21 |
| KJFC-002 | Pipeline 角色 | 新增薄層 `kj-flow-collab`，負責 routing、dispatch 與 collection，不是生成引擎。 | — | 已確認 | 2026-09-21 |
| KJFC-003 | CLP 生命週期 | OM 設計 prompts；人工在外部生成；OM 在 scene planning 前登記選定圖片；Flow 消費這些資料。 | 在 scene planning 後才於 dispatch 建立 CLP | 已確認 | 2026-09-21 |
| KJFC-004 | CLP 權責 | OM 擁有 canonical CLP definitions、tags 與 reference mapping；Flow 與 Providers 不擁有。 | 任何暗示 Flow 擁有或更新 CLP 的方案 | 已確認 | 2026-09-21 |
| KJFC-005 | Unit 規劃 | 將長課程拆成 Units，使用簡單工作清單。 | 完整 PUP planning | 已確認 | 2026-09-21 |
| KJFC-006 | Production methods | 支援 Flow manual、三種既有 OM pipeline routes 及 manual media。 | — | 已確認 | 2026-09-21 |
| KJFC-007 | Shared context | 中央化 CLP、style、output profile、audio／subtitles、naming 與 common instructions。 | 每個 Unit 各自決定規則 | 已確認 | 2026-09-21 |
| KJFC-008 | 回收邊界 | Flow、OM children、外部同事及 manual media 共用 work-order 與 delivery boundary。 | 各 route 自建回收系統 | 已確認 | 2026-09-21 |
| KJFC-009 | Flow rough cut | Flow rough cut 是 review proxy，不是 canonical edit timeline。 | — | 已確認 | 2026-09-21 |
| KJFC-010 | 重用 OM | 重用既有 asset manifest、edit、audio、subtitle、compose 與 render 能力。 | 新建替代後期製作引擎 | 已確認 | 2026-09-21 |
| KJFC-011 | 人工確認 | 只保留 Prompt Pack／工作清單、回收素材及 final preview 三個確認點。 | 額外的重型 Gates | 已確認 | 2026-09-21 |
| KJFC-012 | 相容性 | 協作功能必須選擇性啟用；沒有 CLP context 或 Optional providers 時，既有 pipeline 行為維持不變。 | 全域啟用 | 已確認 | 2026-09-21 |
| KJFC-013 | 排除系統 | 排除 Batch V2、完整 PUP、GCS staging、自動 Providers、IAM、recovery、promotion、receipts、queues 與 Flow automation。 | — | 已確認 | 2026-09-21 |
| KJFC-014 | 複雜度上限 | 超過五個主要模組、三種新 artifact 或三個 Gate 時必須停止並簡化。 | — | 已確認 | 2026-09-21 |
| KJFC-015 | 規格權威 | 現行規格優先於對話及 repository evidence，直到本文件經明確確認後更新。 | — | 已確認 | 2026-09-21 |
| KJFC-016 | CLP 位置 | CLP 不能只存在於 scene planning 後建立的 plan；替代 artifact 仍待定。 | 只把 `clp_lite` 放在 scene planning 後的 `kj_flow_plan` | 已取代 | 2026-09-21 |
| KJFC-017 | Artifact 組合 | 原本的 `kj_flow_plan` + work order + delivery 組合無效；替代組合仍待定。 | 原始三-artifact 提案 | 已取代 | 2026-09-21 |
| KJFC-018 | Stage 順序 | 沒有在 scene planning 前處理 CLP 的 stage 順序無效；確切 CLP stages 仍待定。 | `script -> scene_plan -> dispatch -> collect -> edit -> compose` | 已取代 | 2026-09-21 |
| KJFC-019 | Git 基準 | 尚未批准任何基準；`08e2151` 仍是目前建議。 | — | 待確認 | 2026-09-21 |
| KJFC-020 | Stage 結構 | CLP 必須先於 scene planning，dispatch 必須在其後；exact script entry 與 external-wait representation 仍待定。 | — | 已確認（細節待定） | 2026-09-21 |
| KJFC-021 | Artifact 組合 | 尚未批准確切的替代三-artifact 組合。 | — | 待確認 | 2026-09-21 |
| KJFC-022 | CLP artifact | CLP 必須在 scene planning 前可用；exact name 與 schema 仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-023 | Scene CLP references | Scene planning 必須使用結構化 `clp_refs`；exact schema 仍待定。 | 只使用 free-text CLP references | 已確認（細節待定） | 2026-09-21 |
| KJFC-024 | CLP tags | OM 擁有並維護 canonical CLP tags；vocabulary 與 schema 仍待定。 | 未指定 tag authority | 已確認（細節待定） | 2026-09-21 |
| KJFC-025 | CLP registration | 回傳 CLP 圖片的 registration mechanism 仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-026 | CLP 確認 | CLP 選擇必須納入三個確認點；確切作法仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-027 | Reference views | 尚未批准 mandatory C／L／P reference-view set。 | — | 待確認 | 2026-09-21 |
| KJFC-028 | Prompt dialects | 固定或可擴充的外部 Provider prompt 支援仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-029 | Work-order 內容 | 最低必要語意已確認；Flow work-order exact schema 仍待定。 | 未定義的 work-order 內容 | 已確認（細節待定） | 2026-09-21 |
| KJFC-030 | Delivery provenance | Flow provenance 的必要與選填欄位仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-031 | Pipeline 入口 | Pipeline 是建立還是接收 script，仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-032 | 輸出粒度 | Single-scene 或 multi-scene Unit delivery 仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-033 | Unit state | Status vocabulary 與 directory rules 仍待定。 | — | 待確認 | 2026-09-21 |
| KJFC-035 | Child pipeline 消費 CLP | 既有 OM child pipelines 消費父專案產生的唯讀 CLP context，不得修改父專案 CLP，並透過統一 delivery contract 回傳。 | Child-owned 或全域強制 CLP 行為 | 已確認 | 2026-09-21 |

## 12. 已取代決策

### KJFC-003 — 在 scene planning 後才建立 CLP

原本的順序 `script -> scene_plan -> dispatch`，以及到 dispatch 才第一次組成 CLP 的方案，已被取代。Scene planning 與 prompts 必須以 OM 已登記的選定圖片及 canonical tags 為基礎。

### KJFC-004 — 由 Flow 擔任 CLP 權威

任何可能暗示 Flow 建立、擁有或更新 canonical CLP 的早期文字均已被取代。Flow 只接收唯讀 exported context。

### KJFC-016 — CLP 只存放於 `kj_flow_plan`

將 `clp_lite` 只放在 scene planning 後才建立的 plan 中，此方案已被取代。替代 artifact 的名稱與 schema 仍待定。

### KJFC-017 — 原始三-artifact 組合

原本提出的 `kj_flow_plan`、`kj_flow_work_order` 及 `kj_flow_delivery` 組合已被取代，因為它沒有在 scene planning 前提供 CLP artifact。尚未批准替代組合。

### KJFC-018 — 沒有 pre-scene-plan CLP activity 的 pipeline

原本的 `script -> scene_plan -> dispatch -> collect -> edit -> compose` 已被取代。CLP 設計、外部生成、回傳及 OM 登記必須發生在 scene planning 之前；確切 stage boundaries 仍待定。

## 13. 變更紀錄

### 2026-09-21 — v3

- 將整份規格改為繁體中文。
- 保留 `KJFC-*` IDs、Git commits、路徑、artifact 名稱、schema 欄位及其他程式識別字，避免改變契約語意。
- 本次只調整語言及用詞，沒有改變產品決策、狀態或待確認邊界。

### 2026-09-21 — v2

- 新增原始問題、團隊與原型限制，以及問題與對策的設計理由。
- 記錄 Phase F 的封存證據邊界，以及從中保留的有限研究結論。
- 新增 `08e2151`、`9d5e22a` 與 `c693b0e` 的唯讀比較，同時維持基準尚未批准的狀態。
- 將最初的薄層 adapter 提案、五模組範圍、三-Unit 驗收案例、風險及刪減選項保存為歷史脈絡，而不是實作權威。
- 記錄討論如何修正 CLP 時序、權責、scene references、artifact 假設及 child-pipeline 消費方式。
- 新增明確閱讀規則，讓後續 Agent 能區分現行規格、待確認問題及已取代歷史。

### 2026-09-21 — v1

- 將暫訂結論重新整理成持續維護規格的結構。
- 確認由 OM 擁有、外部人工生成的 CLP 生命週期。
- 確認 CLP 必須先於 scene planning。
- 確認選擇性啟用及維持既有預設行為的相容性要求。
- 確認結構化 scene-to-CLP references，同時維持 exact schema 待定。
- 確認 OM 擁有 canonical CLP tags，同時維持 tag schema 待定。
- 確認 Flow work-order 的必要語意，同時維持 exact schema 待定。
- 新增 KJFC-035，規範既有 OM child pipelines 以唯讀方式消費 CLP。
- 移除 KJFC-034，因為它屬於對話 metadata，不是產品決策。該 ID 已停用，未來不得重用。

### 2026-09-21 — v0

- 記錄最初已確認結論、已取代提案及未解決問題，供各側邊對話交叉核對。
