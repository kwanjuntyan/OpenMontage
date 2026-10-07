# OpenMontage Backlot Director Workspace — Track B Architecture and Implementation Plan

> **版本**：v0.3 current planning baseline
> **日期**：2026-09-16
> **狀態**：現行 Track B 主文件；B0～B2 specification draft，尚未授權產品程式實作
> **維護**：GPT B（Track B3 與跨軌協調）
> **目前程式基線**：`team-main @ df0f8ca`；PUP M0～M5 整合點為 `4d4c28c`
> **Track A dependency snapshot**：固定於 `df0f8ca`；這不是 live milestone status。PUP 仍為 `experimental`／`opt-in`，最新進度只查 Track A implementation plan
> **實作授權**：本文件定義架構與 rollout；本輪只撰寫文件，不授權修改 Backlot、PUP 或 canonical production data

## 0. 如何閱讀這份文件

這份文件是 Backlot／Director Workspace 的現行 Track B 架構與分期實施基線。它吸收 `studio_draft.md`、早期 Backlot 分析與 B0～B6 討論稿中仍有效的內容，避免長對話、跨 Agent 協作或上下文壓縮造成設計理由流失。

本文件已凍結三項方向：第一個可發布版本為 B0＋B1＋B2；Workspace 使用獨立且 feature-flagged 的路由；Production Unit 詳細檢視依賴獨立的 A→B inspection contract，而不擴大 M6.0B。仍標記為 `OPEN` 的項目不得由實作者自行代答。

本文使用下列標記，避免把「程式事實」與「產品決策」混為一談：

- **FACT**：由目前 code、schema、test 或正式文件直接證明；來源改變時必須重新查證。
- **CONSTRAINT**：現有 architecture／authority 的 hard boundary；若要改變必須另立 RFC，而不是由 UI 實作順手改掉。
- **DECIDED**：使用者已做的產品或策略決定；應在 decision log 保存決定者與依據。
- **WORKING AGREEMENT**：目前 Agent 分工或協作方式；可因交接與執行狀況調整，不是產品 runtime contract。
- **PROVISIONAL**：GPT B 的建議方向，必須逐項討論後才能升格。
- **OPEN**：尚未決定，不能被實作自行代答。
- **BLOCKED**：依賴 Track A 契約、M6 qualification 或另一份正式 RFC 才能前進。

討論過程應更新相關段落與末尾 decision log。B0～B2 開始實作前，仍須把本文件中的 logical contract 落成 schemas、fixtures 與可驗收的 API contract；不得把尚未決定的欄位 shape 留給 UI 猜測。

## 1. 文件角色與來源優先序

### 1.1 本文件負責什麼

**DECIDED**：本文件是 Backlot／Director Workspace 的 Track B 規劃與協調來源，負責：

- 保存產品定位、資訊架構、authority boundary 與 rollout 設計；
- 區分現有能力、暫定方向與未決問題；
- 記錄 Track A／Track B 的 consumer-producer 介面；
- 維護 Backlot 設計決策與 supersession history。

### 1.2 本文件不取代什麼

| 來源 | 權責 | 與本文件的關係 |
|---|---|---|
| `AGENT_GUIDE.md`、pipeline manifests、schemas、director skills、`lib/checkpoint.py` | 現行 OM control plane、artifact、gate 與 checkpoint 契約 | 優先於本文件 |
| `skills/creative/course-form.md` | 課程教學設計與 `course_manifest` 語意 | 本文件只能投影，不可重定義 |
| `skills/meta/production-unit-protocol.md` | PUP 現行操作邊界 | 本文件只能消費，不可擴權 |
| `docs/production-unit-protocol-implementation-plan.md` | Track A／M6 狀態與 qualification 邊界 | Track A 的單一 M6 狀態來源 |
| 本文件 | Track B Backlot／Director Workspace 規劃 | 不成為 runtime authority |
| `docs/studio_draft.md` | 原始產品願景與功能構想 | vision input；不是現行資料或 authority contract |
| `docs/course_container_architecture_proposal.md` | 舊 Course Container 構想 | historical input；與現行契約衝突處不得採用 |

若文字描述與已驗證 schema／程式行為衝突，以現行 typed contract 與 fail-closed 行為為準，並回頭修正文檔。

## 2. 已確認的協作邊界

### 2.1 Agent 分工

**WORKING AGREEMENT**：

- GPT A 負責 Track A：M6 各階段的 contract closure、qualification、測試、evidence 與 rollout 建議。
- GPT B 負責 Track B3 與跨軌協調，並維護這份 Backlot 規劃基線。
- GPT A 的 M6 狀態只更新 `docs/production-unit-protocol-implementation-plan.md`；Backlot 設計不與它共用同一份狀態文件。

### 2.2 避免互相踩檔的操作護欄

**WORKING AGREEMENT**：

- GPT A 不修改 `backlot/`、`backlot/ui/`、`tests/backlot/`。
- 若 Backlot 將來需要 Track A 的新資料，GPT A 只交付 producer-side contract、fixture 與介面說明。
- PUP／execution／qualification producer schemas、PUP directors、`lib/production_units/`，以及 PUP authority 相關的 `lib/checkpoint.py` 由 GPT A 單寫；未來 Backlot projection／intent／candidate schemas 不因此自動歸入 Track A。
- GPT B 在 GPT A 產生 review-ready commit／versioned fixture 前，不依賴未定稿欄位，也不在 UI 端猜測其 shape。
- 任何跨軌 interface change 先形成明確 handoff，再由各自 owner 在自己的範圍實作。

目前 Track B 的規劃基線為 `df0f8ca`。是否已 push 不改變上述產品架構，但所有未來 handoff 都必須記錄 exact base SHA，不能只以「最新版本」描述。

## 3. 現況基線

### 3.1 PUP 與 Course Form

**FACT**：

- 本文件的 consumer dependency 固定於 `team-main @ df0f8ca`；該 snapshot 已包含 M0～M5 與 M6.0A consumer contracts。最新 M6 milestone 狀態不在本文件重複維護。
- B0～B2 不依賴任何 M6.0B recovery/coordinator contract；B3 也不得直接讀取 private coordinator state，而是等待獨立 A→B inspection contract。
- PUP 仍是 `experimental`、`opt-in`，預設為 `off`。
- 30 分鐘 frozen benchmark 是一筆正面證據：該 profile 的 12 個 matched spans 中 PUP 全勝，且沒有 critical boundary defect；它不是 60 分鐘、跨平台、media、recovery 或 production qualification。
- `180` 秒只是實驗預設，不能成為產品不變量或 UI 推薦值。
- Course Form 由可觀察的學習成果、先備關係、練習與評量決定；不能由片長、資料夾或檔名推測。
- 一門課仍是一個 direct-child OM project；module、lesson、Production Unit、filesystem directory 與 pipeline stage 互不等價。

### 3.2 Backlot 現有能力

**FACT**：目前 Backlot 已具備：

- project library 與 project board；
- 依 pipeline manifest 生成的 stage rail；
- checkpoint／artifact-derived board state；
- SSE change feed、media serving、thumbnail 與現有 GCS 同步入口；
- script、CLP、approval review、decision log、activity、storyboard、media 與 render 檢視；
- 由核准 proposal checkpoint 衍生的最小 course card；
- namespaced PUP aggregate progress 與 delivery trace。

一般 artifact 的顯示來源目前尚未完全 provenance-normalized：多數 `artifacts/*.json` 維持 historical loose-file precedence，checkpoint-embedded artifact 只在 loose file 缺席時 backfill；CLP 與有正式 Batch V2 publication claim 的 asset manifest 才有較嚴格的 checkpoint authority。因而目前不能替所有 artifact 一律標示「checkpoint-authoritative」或「canonical digest」。

Course projection 目前只承認同時符合以下條件的 authority：

1. proposal checkpoint 有效；
2. status 為 `completed`；
3. `human_approved=true`；
4. checkpoint 同時包含 `proposal_packet` 與 `course_manifest`；
5. proposal 的 `production_plan.content_form="course_form"`。

Loose `artifacts/course_manifest.json` 只能用來做一致性診斷，不能建立或覆蓋 course authority。

PUP progress 只從 checkpoint 的 `metadata.partial_progress.production_units` 投影。Backlot 目前顯示：

- total／completed／failed／stale unit counts；
- active unit；
- boundary defect 與 repair counts。

Delivery projection 只追蹤有效 completed compose／publish checkpoints，並要求 exact `render_report` digest 與安全、相符的 project-relative path。這是 checkpoint evidence trace，不等於 Backlot 已重新確認實體檔案存在、可播放或內容正確。

### 3.3 已有的 fail-closed 防線

**FACT／CONSTRAINT**：以下行為不可在改版中退化：

- 普通 project 保持既有 API shape，不被強加 `course` 欄位。
- Invalid checkpoint 不可提升 stage、approval 或 delivery 狀態。
- 某一 stage 的 PUP progress 壞掉時，course 可降級顯示，但壞 progress 不可冒充有效狀態。
- Course truth 永遠來自 approved proposal checkpoint；後續 stage 不另造可變 course truth。
- PUP progress 保持獨立 namespace，不能覆寫 legacy `completed_scene_ids` 等 partial progress。
- `.production-units/` 被 media scan 與 watcher hot path 排除。
- Sidecar attempts／media 不可冒充 canonical asset 或 render。
- Backlot 不裁決 unit、checkpoint、Human Gate 或 publication 狀態。

### 3.4 尚未存在的能力

**FACT**：以下項目目前都還不是 Backlot 能力：

- Studio 固定六分頁或完整 Director Workspace；
- UI 直接核准 checkpoint、修改 canonical artifact 或推進 stage；
- directive／intent queue；
- UI 直接呼叫 provider／BaseTool 進行 regenerate；
- 持久化的 take selection、candidate lineage、A/B comparison；
- crop、style save、UI-side budget-cap editing／runtime safety control／reapproval flow，以及 PUP override／repair／resume 控制；
- module／lesson-scoped artifact API；
- provenance-grade raw-source locator／source-map；
- PUP attempt、execution epoch、receipt、policy digest 的詳細 inspector；
- pagination、delta state、ETag、artifact lazy loading、storyboard virtualization。

現有 UI 所稱 active visual／take 主要是 manifest order heuristic，不是人類核准或持久化 selection，不能在產品文案中誤稱為已選定 take。

另有一個重要的 proposal review 盲區：`course_manifest` 是 proposal stage 的 optional output，但目前 stage metadata 與 approval review 只投影 `produces`，沒有 `optional_produces`；course projection 又必須等 proposal `completed + human_approved` 後才成立。因此使用者目前無法在同一個結構化 Course workspace 中完整審閱「尚待核准的 course candidate」。未核准 candidate 不能建立 `state.course.is_course=true`，但未來必須有清楚分離的 review presentation。

### 3.5 40～60 分鐘 workspace 的現有規模風險

**FACT**：現行 board 適合做改版起點，但不能未經量測就當成長課程 workspace 的最終資料契約：

- `/api/project/{id}/state` 會重新讀取 checkpoints、收集完整 artifacts、join storyboard、掃描 media；
- library summary 目前仍會經過完整 `load_board_state()`；
- event reader 會先讀取持續增長的 `events.jsonl` 再截尾端；
- scene-to-script 與 snapshot fallback 含線性／重複掃描路徑；
- SSE change 後前端重新抓取 full state，並清空重建整頁；
- storyboard 一次建立所有 scenes、takes 與 media elements。

**DECIDED response**：採 compact/versioned summary-detail projections、on-demand loading、bounded pagination、ETag/cache 與 single-flight refresh；DOM virtualization 是否必要由 B0 大型 fixture 決定。具體效能門檻仍是 **OPEN**，必須先量測再核准，不能沿用 `studio_draft.md` 的「0.1 秒」宣稱。

### 3.6 現有 evidence／test 缺口

**FACT**：目前的 course projection tests 已保護核心 M5 invariants，但還不足以替 Director Workspace 或長課程規模背書：

- proposal authority 尚缺 unapproved／awaiting／invalid proposal 與多次 rerun 的完整矩陣；
- progress 尚缺 zero-total + active、active 同時 terminal、completed checkpoint 仍 active、policy off 卻出現 progress 等 edge cases；
- course projector 會拒絕壞 progress，但 stage rail 仍可能顯示 raw partial progress，尚無 UI consistency test；
- delivery 尚缺 missing files、更多 unsafe／wrong-prefix paths、duplicate targets、optional requirements 與 invalid compose／publish 組合；
- server performance fixture 沒有大量 scenes／takes／events／artifact history 的單一大型 project；
- Playwright 只確認 visual take 標記存在，沒有 selection semantics、持久化、keyboard／accessibility 或大量 DOM 測試。

這些是 B0 evidence backlog，不表示現在的 M5 tests 失敗。

## 4. 對 `studio_draft.md` 的修正基線

`studio_draft.md` 最值得保留的產品目標是：讓導演在同一處看懂進度、審閱完整上下文、比較媒體並精確提出修改要求。以下資料與 authority 假設則已過時或尚無契約支撐。

| 原構想 | 現行修正 | 狀態 |
|---|---|---|
| 依短片／長片片長選擇 project mode | 依 approved proposal 的 `content_form`；片長不是 Course Form 判準 | FACT／CONSTRAINT |
| `projects/<course>/chapters/<chapter>` nested projects | 一門課是一個 direct-child project；PUP 是 stage-internal execution | FACT／CONSTRAINT |
| `course.json` 同時保存設計、進度與 render state | proposal-owned immutable `course_manifest` 只保存 static learning design | FACT／CONSTRAINT |
| 每章一份 CLP／`master_clp.json` | 全課程維持一份 canonical `clp_manifest` 與既有 provenance chain | FACT／CONSTRAINT |
| 固定 Script／Style／CLP／Shots／Projects／Budget 六分頁 | primary navigation 依 pipeline manifest stage rail；跨階段資訊作 persistent lenses | DECIDED |
| Scene → Shot → Take 為現有資料模型 | 現行 `scene_plan.scenes[]` 與 `asset_manifest.assets[]` 是 flat、以 `scene_id` 關聯 | FACT |
| 前端用 fuzzy match 建立 raw-source trace | 先顯示 verified refs；逐段 highlight 必須等待正式 source-map contract | PROVISIONAL／BLOCKED |
| FastAPI 直接呼叫 BaseTool 並改 manifest | UI 只建立 structured Agent intent；Agent 走既有 director／review／gate／checkpoint 流程 | DECIDED／CONSTRAINT |
| UI 寫 checkpoint 完成 approval | Approval 必須綁定 exact pending checkpoint，且由既有 authority 完成 transition | CONSTRAINT |
| UI 直接開啟或調整 PUP | PUP policy 在 proposal Human Gate 核准；目前 Backlot 只能可靠顯示 approved policy 與 aggregate progress。未來 runtime effective disposition 必須等待正式 contract | CONSTRAINT／BLOCKED |
| 0.1 秒刷新與 `state.py` 無需修改 | 先量測長課程資料量，再設計 compact projection 與增量載入 | PROVISIONAL |

在本文件完成 v1 前，不直接重寫 `studio_draft.md`；它保留為 vision history。最終可選擇將它標註 superseded，或重寫成只描述使用者體驗的 vision document。

## 5. 產品北極星

### 5.1 核心命題

**DECIDED**：

> Backlot 演進為 manifest-driven、provenance-first 的 Director Workspace；Studio 是 Backlot 的深度工作模式，而不是第二套資料模型、第二個 orchestrator 或第二個 production control plane。

這代表改版是 additive evolution：保留現有 Board Overview，再增加針對 stage、artifact、lesson、scene 與交付的深度工作空間。第一個可發布版本不以「控制整條管線」為目標，而是先讓導演能可靠地找到課程、讀懂劇本與創作基準、檢視 prompts，並判斷 image／audio／video 品質。

### 5.2 三層產品結構

**DECIDED**：

1. **Library**：跨 project 搜尋、摘要、健康狀態與進入點。
2. **Board Overview**：現有 living storyboard；快速掌握 stage、gate、course、cost、media 與 delivery。
3. **Director Workspace／Studio mode**：對選中的 stage、artifact、lesson、scene 或 issue 做深度檢視；B4 之後才透過 structured intent 提出修改。

**DECIDED**：第一版使用獨立的 `/p/{project_id}/workspace` 路由並受 server-side feature flag 控制；現有 `/p/{project_id}` Board 與 `/api/project/{id}/state` 保持不變。是否日後改名為 Studio，不影響 projection contract。

### 5.3 Manifest-driven navigation

**DECIDED**：主導覽由實際 pipeline stages 生成，不把所有 pipeline 強塞進六個固定分頁。跨階段的 course outline、decisions、cost、diagnostics、history 與 delivery 作 persistent rail／drawer／lens，而不是取代 stage rail。

第一個 release 的四個前期 inspector 依 owner stage 掛載，而不是重建固定頁籤：

- proposal：Course design 與 Style；
- script：完整 Script；
- clp：Characters／Locations／Props；
- assets：Scene Assets 與 generation instructions。

Course outline 可在各 inspector 保持為穩定側欄；Style 在 B1，CLP 與其 media／binding primitives 在 B2；兩者都是第一個 B0＋B1＋B2 release 的必要功能，不延後到 B3 或進階 Lens。

### 5.4 第一個可發布版本的使用者成果

**DECIDED**：第一個可發布版本為 **B0＋B1＋B2**，必須同時完成：

1. 從 project／course selector 搜尋並切換指定課程；
2. 閱讀 approved 或清楚標示為 candidate／legacy 的完整課程設計與劇本；
3. 檢視本片採用的 Style：course style intent、selected visual approach、playbook、taste profile、palette、typography、motion、audio 與 prompt rules；
4. 檢視 CLP：characters、locations、props、reference images、prompt anchors 與 consistency policy；
5. 依 scene／media type／provider／model 瀏覽 image、audio、video；
6. 查看有證據的 generation instructions／prompts、seed、provider、model、成本、解析度與時長；
7. 點選圖片進入原尺寸 lightbox 並 zoom／pan，播放 audio／video，且保持 deep link；
8. 明確辨識 canonical、candidate、execution evidence、legacy display source、invalid 與 unavailable。

B0～B2 全部是 read-only。修改劇本、Style、CLP、prompt、重製 asset 或生成九宮格，分別由 B4／B5 的 Agent Intent 與 Candidate Set 承接。

## 6. Authority architecture

### 6.1 四個平面

**DECIDED**：以四個平面描述系統，避免「可看見」被誤認為「可寫入」：

| 平面 | 內容 | Authority |
|---|---|---|
| Truth plane | Canonical checkpoints、artifacts、decision log、approved proposal | 既有 schema／director／checkpoint／Human Gate |
| Projection plane | BoardState、course projection、diagnostics、validated summaries | Backlot read model；可 degraded，不可升格 truth |
| Intent plane | 使用者提出 approval、revision、fork、new take、patch、budget change、repair／resume request | 未來 versioned protocol；request 不是完成狀態 |
| Execution plane | Agent 依 pipeline、director、reviewer、tools 與 gates 執行 | Agent control plane；Backlot 不接管 |

建議資料流：

```text
canonical checkpoints / artifacts
              |
              v
     validated projections ------> Backlot / Director Workspace
                                          |
                                          v
                                  structured user intent
                                          |
                                          v
                                       Agent
                                          |
                         existing pipeline / review / Human Gate
                                          |
                                          v
                              new canonical checkpoint
```

UI 的 optimistic state 必須明確標成 draft／queued／accepted-for-work；只有新 canonical checkpoint 出現後，才能顯示為 applied／approved／published。

這裡的 observer-only 是指「Backlot 不裁決或寫入 canonical production state」，不等於 server 絕對零副作用。現有 `sync_gcs` 是 operational utility；它未取得 artifact/checkpoint authority。B0～B2 不把它納入 Workspace；若日後保留，須在 B4 security／intent RFC 決定改走 intent 或移到 admin／operations surface。

### 6.2 初步 authority map 與 normalization gap

| UI domain | Current source／behavior | Proposed target | Gap／owner | Status |
|---|---|---|---|---|
| Project identity | `project.json` 與 direct-child identity | 唯讀投影；不另造 child project | 現有 identity contract | FACT／CONSTRAINT |
| Pipeline／stage rail／gates | manifest + validated checkpoints | 動態顯示；invalid 時 fail closed | 現有 Backlot | FACT／CONSTRAINT |
| Approved course design | approved proposal checkpoint 內的 `course_manifest` | 維持唯一 course truth | 現有 M5 projection | FACT／CONSTRAINT |
| Course candidate under review | artifact 可存在於 awaiting proposal checkpoint，但 `optional_produces` 未進 stage meta／approval review | 與 approved course truth 分離的完整 candidate inspector | Track B read model；不可把 candidate 設成 `state.course` | B1 prerequisite |
| PUP policy | approved `proposal_packet.production_plan` 存在；目前無完整 runtime-effective projection | 顯示 approved policy；不在 UI 啟用。Runtime disposition 等 Track A contract | Track A producer + Track B projection | FACT／BLOCKED in part |
| PUP aggregate progress | checkpoint `metadata.partial_progress.production_units` | 驗證後投影；壞資料降級 | 現有 M5 projection | FACT |
| CLP artifacts | owning checkpoint 有較嚴格 authority；loose file 只是 cache | 可顯示已驗證 authority 與 digest | 現有 CLP validator | FACT |
| Batch V2 asset publication | 只有 explicit publication claim 走專用 validator | 可顯示已驗證 publication authority | 現有 Batch V2 contract | FACT |
| 其他 script／scene／asset／edit／render／publish artifacts | 多數 loose `artifacts/*.json` 具有 historical precedence；checkpoint 只 backfill | B0 建立 authority-preserving resolver；legacy-only 明示 `display_only/unverified` | Track B B0；不可由 UI 假定 | B0 REQUIRED |
| Decisions | Board 可讀 loose artifact／root file；操作契約要求 append-only `(category, subject)` history | 來源與 checkpoint/provenance 關係需正規化後再給 canonical badge | Core/Track B coordination | OPEN |
| Course delivery | digest-bound compose／publish evidence | 顯示 evidence status，不自行宣稱檔案有效 | 現有 M5 projection | FACT |
| User requested change | 尚無 intent artifact／event | 未來與 canonical state 分欄顯示 | Track B intent RFC + Agent integration | BLOCKED |

完整的「UI field → current source → target authority → validator → degradation behavior → owner」矩陣是 B0 必交付物；上表只是起點。B1/B2 只能對已驗證為 authoritative 的資料顯示 canonical badge，其餘來源必須誠實標示。

### 6.3 Course 與 PUP 的雙軌視圖

**DECIDED**：同一 workspace 平行顯示，而不是混成一棵假階層：

- **Curriculum lane**：promise → objectives → modules → lessons → assessments → delivery requirements。
- **Production lane**：pipeline stages → Production Units → completed／failed／stale／active → defects／repairs → 由既有 director／checkpoint writer 發布的 validated merge outcome／delivery。

只有 producer 提供 exact、validated ownership mapping 時，才顯示 lesson／objective／scene 與 unit 的 cross-link。不能依時間重疊、名稱相似或資料夾位置自行推論。

### 6.4 共同窄腰層

前期的 Course／Script／Style／CLP／Asset inspectors，與後期的 Production Unit、Agent Intent、九宮格及 Lenses，都必須建立在同一組邏輯契約上：

```text
Canonical checkpoints / artifacts / manifests / evidence
                              |
                    validators + adapters
                              v
                 Versioned Workspace Projections
              +---------------+----------------+
              v               v                v
       Stage inspectors   Unit inspector     Lenses
              +---------------+----------------+
                              |
                       exact ResourceRef
                              |
                    Structured Agent Intent
                              |
                              v
                Agent + pipeline + review + gates
                              |
                              v
                   New canonical checkpoint
```

#### ResourceRef — 穩定的邏輯識別

`ResourceRef` 用來導覽及 cross-link，不以 path、URL 或檔名作 identity。B0 schema 至少必須表達：

| 欄位 | 語意 |
|---|---|
| `project_id` | direct-child OM project identity |
| `kind` | `project|stage|course|module|lesson|script_section|clp_entity|scene|asset|generation_instruction|production_unit|candidate_set|candidate` |
| `stage` | owner stage；`production_unit` 必填，其他 resource 依需要填寫 |
| `local_id` | producer 提供的 exact ID；不得由標題、時間或檔名猜測 |
| `parent_refs` | 只保存 producer 明確提供且已驗證的 ownership 關係 |

Production Unit identity 至少是 `project_id + stage + local_id`；單獨的 `unit_id` 不具全域意義。lesson／section／scene／asset／unit 的關聯沒有 exact mapping 時，UI 必須顯示 unavailable，而不是 fuzzy join。

#### RevisionRef — 精確版本識別

導覽只需要 `ResourceRef`；任何未來 mutation intent 還必須綁定適用的 revision evidence：

- checkpoint canonical digest；
- artifact name + canonical digest；
- asset content digest；
- projection/source snapshot digest；
- execution epoch（僅在 Track A 提供正式 contract 時使用）。

舊畫面或 stale browser state 不得修改已更新的 production state。缺少必要 digest 時，B4 action capability 必須為 disabled。

#### AuthorityDescriptor — 來源與可信度

每一份 projection 及必要的 field group 都要表明：

- `authority_state`：`canonical|candidate|execution_evidence|display_only|unavailable`；
- `validation_state`：`validated|invalid|unverified`；
- `source_kind`：例如 `approved_checkpoint_artifact`、`awaiting_checkpoint_artifact`、`batch_v2_publication`、`project_marker`、`style_catalog_current`、`legacy_loose_file`、`legacy_scan`；
- `evidence_scope`：例如 `manifest_only`、`provider_request`、`provider_receipt`、`binary_observed`、`human_reviewed`；它描述證據深度，不改變 authority state；
- source stage、checkpoint status、source refs／digests；
- `degraded_reasons[]`。

PUP policy mode、execution disposition、manifest support、qualification status、checkpoint status 與 Human Gate status 是不同軸；不得濃縮成單一「綠燈」或 `effective_mode`。

#### WorkspaceProjection — versioned read model

所有新 endpoint 回傳共同 envelope；B0 需落成 schema，而不是只依賴 TypeScript／JavaScript 慣例：

```json
{
  "projection_version": "backlot.workspace.v1",
  "projection_kind": "script",
  "resource_ref": {},
  "source_snapshot": {
    "sources": [
      {"source_kind": "checkpoint_artifact", "resource_ref": {}, "sha256": "sha256:..."}
    ],
    "composite_sha256": "sha256:..."
  },
  "authority": {},
  "capabilities": {
    "inspect": {"available": true},
    "request_revision": {"available": false, "reason": "intent_protocol_unavailable"}
  },
  "diagnostics": [],
  "data": {}
}
```

`sources[]` 依 deterministic key 排序；`composite_sha256` 綁定完整 source set，作為 projection token／ETag 基礎。單一 artifact inspector 也使用同一結構，多來源 Style projection 因此能同時綁定 proposal、course、marker/checkpoint、current catalog 與 downstream observation，而不遺漏其中一項。

同一 logical resource 可能同時存在已核准版本與待審候選。B0 schema 必須提供 `revision_set` projection kind；其 `data.current_canonical`、`data.pending_candidates[]` 與 `data.historical_revisions[]` 都是完整的 `ProjectedRevision`，各自帶 ResourceRef、RevisionRef、source snapshot、authority、capabilities、diagnostics 與 data。不得用 awaiting candidate 覆蓋 producer仍承認的 current canonical，也不得要求 endpoint 二選一後讓另一版本消失。Archived checkpoint只能標為 historical；除非 core contract明確指認，Backlot不得自行把「最近一次 completed history」提升為 current canonical。

`capabilities` 由 server 根據已驗證 contract 明確產生。前端不得因為某個欄位、button label 或媒體檔剛好存在，就自行推論可修改、核准、重製或採用。

#### GenerationInstruction — prompt 的長期顯示模型

UI 不綁定單一 `prompt: string`。B2 將不同 producer 資料正規化為 `generation_instructions[]`。每筆至少包含：

- projection-stable `instruction_id`，由 parent ResourceRef + exact source field/work-item identity 建立，不由文字內容猜測；
- `resource_ref.kind=generation_instruction` 與 exact parent ResourceRef；
- `instruction_digest`／RevisionRef；
- instruction kind、display-safe content、source locator、AuthorityDescriptor、evidence scope 與 unavailable reason。

支援的 instruction kind 包含：

- `creative_specification`；
- `provider_input`；
- `negative_prompt`；
- `narration_text`／`delivery_contract`；
- `music_intent`／`sfx_intent`；
- `search_query`。

現有 `asset_manifest.assets[].prompt` 先投影為 `creative_specification`；其 authority state 跟隨 owning manifest，另以 `evidence_scope=manifest_only` 表示沒有 provider request/receipt 證據。`manifest_only` 不是 AuthorityDescriptor 的第六種 authority state。不能把 scene description、CLP prompt anchor 或 playbook prefix 猜成實際 provider input。未記錄就是 `unavailable`。

#### AgentIntent — 唯一 mutation 邊界

B0～B3 不建立 mutation endpoint。B4 之後 Backlot 只能提出 versioned、append-only、idempotent、digest-bound request；不得直接呼叫 provider、修改 canonical artifact、寫 checkpoint、裁決 Human Gate，或選擇「最新成功 attempt」作為正式結果。只有 Agent 產生新 canonical checkpoint 並回綁 `intent_id` 後，UI 才可顯示 `applied`。

## 7. Scope guardrails

### 7.1 全階段不可破壞的護欄

**CONSTRAINT**：

- 不建立第二個 pipeline state machine、background orchestrator 或 publisher。
- 不讓 Backlot 直接呼叫生成 provider、決定 fallback、重試 ambiguous charge 或記帳。
- 不由 UI 直接修改 canonical artifact、checkpoint、Human Gate 或 decision history。
- 不建立 nested chapter projects、`resolve_chapter_dir()` 或 `master_clp.json`。
- 不由前端發明 Scene／Shot／Take、source-map、repair receipt 或 PUP epoch schema。
- 不由片長自動選 Course Form 或開啟 PUP。
- 不把 PUP 標示為 default、recommended 或 production-ready。
- 不移除普通 project 的相容行為，也不要求每個 pipeline 都有 course／CLP／script。

**PROVISIONAL engineering preference**：不為了建立 Workspace 預先更換整套前端框架。若代表 fixture 顯示現有 vanilla DOM 無法達到已決定的 performance、accessibility、virtualization 或 state-isolation 門檻，且有低風險、可量測的 migration plan，則可推翻此偏好。

### 7.2 可以與 M6 平行推進的範圍

**DECIDED**：以下工作不需要等待 M6 完成：

- 現況與 vocabulary audit；
- authority／field mapping；
- read-only information architecture；
- 使用既有 validated fields，或清楚標示 display source／authority 限制的 inspectors；
- long-course state／DOM performance benchmark；
- compact projection、lazy loading、pagination 與 virtualization 的 contract design；
- UI 對 `experimental / opt-in / unqualified` 的誠實標示；
- 使用已整合的 M6.0A schemas／fixtures 設計 policy、support 與 qualification 的 observer-side presentation；live resolution 仍只相信正式 trusted loader／evidence contract。

任何依賴 execution epoch、resume authorization、adoption receipt、qualified profile 或 operational repair 的介面，必須等待 Track A 提供 versioned producer contract。

## 8. B0～B6 分期實施

分期的目的不是建立七套產品，而是讓每一期都交付獨立價值，同時沿用第 6.4 節的共同窄腰層。任何後期功能都不得繞過早期 projection contracts 直接讀 private files 或另造 identity。

| Phase | 使用者取得的能力 | 同時建立的長期基礎 | Track A 依賴 |
|---|---|---|---|
| B0 | 主要為內部準備 | versioned projections、ResourceRef、authority、capabilities、效能與相容基線 | 無 |
| B1 | 選課程；看 Course、Script、Style | catalog、deep links、planning inspectors | 無 |
| B2 | 看 CLP、prompts 與 image／audio／video 品質 | CLP/asset projection、media viewer、generation instructions | 無 |
| B3 | 按 Production Unit 看輸入、prompt、結果 | sanitized inspection contract、exact crosswalk | 需要獨立 A→B handoff |
| B4 | 提出修改／重製要求 | digest-bound Agent Intent、acknowledgement | PUP-specific intent 另依 Track A |
| B5 | 比較候選、九宮格與 first-frame selection | Candidate Set、selection 與 lineage | 無直接 M6 依賴 |
| B6 | Quality／Cost／Provenance／History lenses | 組合既有 projections，不新增 truth | 視 lens 而定 |

### B0 — Foundation freeze

#### Deliverables

- 保留現有 Board、`/api/project/{id}/state`、CLI 與 ordinary project 行為。
- 新增獨立、feature-flagged `/p/{project_id}/workspace` shell；flag 關閉時 route 與新 API 不可使用，舊 Board 不受影響。
- 將 `ResourceRef`、`RevisionRef`、`AuthorityDescriptor`、`WorkspaceProjection`、capability entry 與 diagnostic 落成 versioned schemas／typed contracts。
- 建立 compact project catalog，避免 library summary 再呼叫完整 `load_board_state()`。
- 定義 summary/detail 分離的 read-only endpoints、pagination、ETag／projection digest 與 SSE invalidation semantics。
- 建立通用 artifact-source resolver：能同時描述 owning checkpoint artifact、awaiting candidate、loose cache、legacy display source 與 mismatch，不改變舊 Board precedence。
- 讓 manifest 的 `produces` 與 `optional_produces` 都能進入 Workspace stage metadata；awaiting proposal 裡的 `course_manifest` 可供 candidate review，但不可建立 approved course truth。
- 建立代表性 40～60 分鐘 synthetic course fixture，量測 state derivation、catalog latency、payload、SSE refetch 與 DOM 規模。
- 所有 B0～B2 endpoint 均為 GET／HEAD；不得加入 canonical write、provider call 或 approval transition。

#### Required compatibility fixtures

- ordinary non-course project；
- approved course + PUP off；
- approved course + PUP opt-in／experimental；
- awaiting-human course candidate；
- missing／invalid／mismatched script、style、CLP 或 asset source；
- zero-entity CLP；
- validated Batch V2 publication 與 legacy asset manifest；
- failed／stale progress；
- completed delivery；
- 大量 sections、scenes、assets、events 與 history。

#### Exit gate

- 每個 UI field 都能追到 current source、validator、authority、degraded behavior 與 owner。
- 關閉 feature flag 後，舊 Board API／UI tests 維持 parity。
- projection 不暴露任意 filesystem path，也不把 invalid／loose data 升格。
- performance baseline 與第一版 budgets 已記錄；不沿用未實測的「0.1 秒」承諾。

### B1 — Course／Script／Style Context

B1 完成課程規劃、劇本與專案級視覺方向的前期審閱。Style 不是後期附加 Lens；它在看生成成果以前就必須可見。

#### Workspace shell 與 Course selector

- 可搜尋、篩選及切換 project／course；預設可聚焦 course，但 ordinary project 仍能進入 Workspace。
- catalog 清楚區分 `approved_course`、`awaiting_course_candidate`、`ordinary`、`legacy` 與 invalid/degraded。
- persistent context 顯示 project、pipeline、current stage/gate、approved PUP policy、qualification（若可驗證）、cost summary 與 authority health；各軸分開呈現。
- pipeline manifest 產生 primary stage rail；URL 保存 stage、module、lesson、section、CLP entity 等 selection context。
- Course outline 作穩定側欄，顯示 promise、audience、entry requirements、objectives、modules、lessons、prerequisites、teaching beats、assessments、sources、glossary、notation、style intent 與 delivery requirements。

#### Script inspector

- 顯示完整 title、duration、voice-performance contract 與所有 ordered sections。
- 每段顯示 timing、text、speaker directions、delivery cues、enhancement cues、pronunciation guide 與原樣記錄的 `source_ref`。`source_ref` 目前是 free-form string，不因此取得 typed／verified cross-link authority。
- 支援全文搜尋、section deep link、course lesson cross-link；只有 producer 提供 exact mapping 時才顯示 lesson ownership。
- raw-source split view 不以 fuzzy match 實作；缺少 canonical source locator 時只顯示已存在的 source reference 或 unavailable。
- owning checkpoint、awaiting candidate 與 legacy loose script 使用不同 authority badge；stage completed 不會讓另一份 loose script 自動變成 approved。現有 script 主要是 JSON-schema validation，UI 不得額外宣稱 section timing continuity、ID uniqueness 或 duration sum 已通過 semantic validation，除非 producer 日後提供該 evidence。

#### Style inspector

Style 是多來源 projection，不建立新的 `style.json`：

- approved／candidate proposal：selected concept `visual_approach`、`production_plan.playbook`、`taste_profile`、`art_direction`、`renderer_family`、`render_runtime`、`composition_mode`；concept 的 `suggested_playbook` 只能標成 recommendation，不能冒充 selection；
- approved course：`course_manifest.style_intent`；
- project/checkpoint：validated `style_playbook` identity；
- current style catalog：經 `styles.playbook_loader` 驗證的 playbook content，包括 identity、palette、typography、motion、audio、asset-generation prompt prefix／negative prompt、consistency anchors、quality rules 與 optional taste profile；不得用較寬鬆的 generator-side loader 代替 read-time validation。

Project-specific approved proposal `taste_profile` 優先於 playbook-level default；缺少時可以分欄顯示 catalog default，但不可合成未記錄的 dials。若 catalog playbook 沒有被 checkpoint digest 綁定，UI 必須標示 `style_catalog_current` 與 `historically_frozen=false`，不可宣稱它就是歷史 execution 使用的 exact bytes。

所有**目前存在且具 authority 的** proposal、marker、checkpoint 與 downstream scene-plan style claims 一致時，才可顯示 resolved style。早期尚未產生 scene plan 只表示 `not_yet_corroborated`，不會讓 B1 Style 消失；真正的名稱衝突、missing／invalid catalog entry 或 proposal/marker drift 才將 resolved style 設為 unavailable。前端不得自行選勝者、相似名稱或 fallback playbook。

B1 只讀：不提供切換 playbook、另存 Style、修改 palette／prompt prefix 或直接更新 project marker。這些在 B4 以 `request_style_revision`／`fork_style_playbook` intent 設計，且 global style library 的權限另行審議。

#### B1 exit gate

- 使用者能從 catalog 選到指定課程，重新整理 deep link 後仍停在同一 inspector／resource。
- approved course 與 awaiting candidate 不混淆；ordinary project 不被誤判為 course。
- 完整 script 與 Style 均有 authority、source snapshot、capabilities 與 degraded reason。
- missing optional artifact 只讓該 inspector unavailable，不使 Workspace crash。

### B2 — CLP／Scene／Asset／Prompt Review

B2 完成 CLP continuity context 與第一個 release 的媒體品質審閱。CLP 與 Scene Assets 共用 reference image、thumbnail、lightbox、media ref 與 exact binding primitives；兩者同批完成可避免建立臨時圖片模型。在 B3 前仍誠實稱為 **Scene Assets**，不把現有 manifest rows 冒稱為完整 Production Unit results。

#### CLP inspector

- 以 Characters／Locations／Props 分組顯示 `clp_manifest`。
- 顯示 name、role/category、visual/environment description、costume/material、lighting/palette、prompt anchor、policy、voice ID、asset digest 與 reference image。
- reference image 使用 thumbnail；點擊後可在 lightbox 查看原圖並 zoom／pan。
- valid owning `checkpoint_clp` artifact 依 lifecycle 分為 completed canonical、awaiting candidate、working/failed display snapshot 或 invalid/unavailable；loose CLP file 只是 cache。合法 zero-entity auto-pass仍是 canonical，但另以 `verification_mode=zero_entity_auto_pass` 說明，不發明新的 authority state。
- `policy=strict_reference|text_anchor_only|ignore` 描述 consistency policy，不等於 Approved／Locked。只有 canonical strict-reference entity 且 image digest evidence 已驗證，才可使用「reference locked」文案。
- `clp_shot_bindings` 由 valid owning scene-plan checkpoint提供 entity-to-shot usage、coverage 與 digest evidence；沒有 lesson mapping 時不推測。
- legacy character/design/image scan 可以保留相容顯示，但 authority 必須是 `display_only + unverified`；filename match 不得合成 strict-reference authority。
- empty validated CLP 顯示「本專案明確沒有 recurring entities」，與 missing／invalid CLP 分開。
- `clp_candidates` 是 script extraction evidence，不是圖片 Candidate Set；A/B reference selection、重製 image 與變更 policy 延後到 B4／B5。

#### User-facing capabilities

- 依 scene、media type、provider、model、source tool、status 與 authority 篩選。
- 圖片 gallery、原尺寸 lightbox、zoom／pan、前後切換與 metadata panel。
- 影片 poster／metadata／完整 player；音訊 player、duration 與基本 metadata。
- asset detail 顯示 ID、scene binding、path/reference、type、prompt records、provider、model、source tool、seed、cost、quality score、resolution、duration、format、license、source URL、voice-performance evidence、authority 與 digest（存在時）。每個 quality score 必須標示為 producer-declared、tool-observed 或 human-reviewed evidence，不能只顯示無來源分數。
- scene detail 並列 script excerpt、scene description、CLP bindings、required assets 與實際 asset rows；缺少 exact relation 時不猜測。
- 多個成果可並排瀏覽，但 asset manifest order 或「最後一個 renderable asset」不得標成 selected take。
- Prompt 缺少時顯示「未記錄」，不能從 scene description、CLP anchor 或 style prefix還原成實際 provider prompt。

#### Projection foundation

- `generation_instructions[]` 統一 image／video／audio／narration／music／SFX 的顯示模型。
- Batch V2 asset publication 使用其正式 validator；其他 asset manifest 依 owning checkpoint／legacy source 誠實標示。
- Media list 與 detail 分開載入；列表只含 thumbnail／summary，原始媒體不內嵌 response。
- 長清單使用 cursor pagination 或經量測核准的等價 bounded strategy；filter/sort 在 server-side projection 上執行。
- `/media`／`/thumb` 保持 project containment；missing bytes 與 valid metadata 分開顯示。

#### First-release gate（B0＋B1＋B2）

- 使用者可在不返回 Library 的情況下切換課程，完成 Course、Script、Style、CLP 與多媒體檢視。
- image、audio、video 均有至少一個 valid、missing、invalid/degraded fixture。
- 圖片 detail 可放大；audio／video 可播放；keyboard、focus、screen-reader label 與 reduced-motion 基本檢查通過。
- image／audio／video 的 acceptance fixtures 覆蓋 generation instruction present/unavailable、provider/model/seed、declared dimensions/duration、observed metadata（若有）、quality evidence kind 與 authority labels。
- 一次 SSE change 不再無條件重抓及重建所有 Workspace projections。
- no-write test 證明使用所有 B0～B2 API 不會改變 project tree、checkpoint、artifact、style catalog 或媒體檔。
- 舊 Board、ordinary project、PUP off 與 feature-flag rollback tests 全綠。

### B3 — Production Unit Inspector

B3 才正式完成「按 Production Unit 查看輸入、prompt、work items、結果與 assets」。它依賴 Track A 另行提供 versioned、sanitized、digest-bound inspection contract；不讀 `.production-units/`、`.batch-v2/`、coordinator `state.json` 或其他 private sidecar。

Inspector 至少需要：

- run／stage／execution epoch／stage-local unit identity；
- exact lesson／section／scene ownership crosswalk；
- input context／work-item identity；
- display-safe prompt records或 unavailable reason；
- selected result、asset refs 與 selection authority；
- source checkpoint／artifact digests；
- `candidate|canonical|failed|stale|unsupported|unknown|invalid` 狀態；
- valid、missing、stale、tampered、cross-epoch fixtures。

Batch V2 影片可以顯示正式 request／receipt／digest evidence。image／audio 若只有 canonical manifest 資料，仍顯示為 manifest-level evidence，不補造 attempt provenance。M6.0B 的 candidate handoff metadata 本身不提供上述 unit-inspection 資料。

### B4 — Structured Agent Intent

先開放一般 revision，不立即開放 PUP recovery control。第一批 intent：

- `request_script_revision`；
- `request_style_revision`；
- `request_clp_revision`；
- `revise_generation_instruction`；
- `regenerate_asset`（single replacement candidate；多候選輸出必須等待 B5 Candidate Set contract）。

每筆 intent 至少包含 version、intent ID、idempotency key、actor、ResourceRef、RevisionRef、修改要求、保留／變更 provider-model 偏好、sample／batch 與成本含意、stale-target policy。初版可先產生或複製正式 intent packet；接 durable queue 時沿用同一 envelope。

Agent 必須 acknowledgement 並依既有 director、review、cost disclosure、Human Gate 與 checkpoint 流程執行。PUP repair／resume／cross-epoch adoption 等控制另待 Track A durable contract 與適用 qualification。

### B5 — Candidate Set／Take／九宮格

九宮格是通用 Candidate Set 的一種 presentation，不是 Backlot 直接裁切並發布 canonical asset 的捷徑。

```text
first-frame candidate set
  +-- candidate 1
  +-- candidate 2
  +-- ...
  +-- candidate 9
```

Candidate Set 可容納九張獨立圖片，或一張 3×3 parent grid 加九個有明確座標的 derived regions。選定一格至少保存 parent digest、tile ID／crop parameters、derived digest、generation lineage、selection intent 與下游 video request binding。

B5 在 Candidate Set schema、storage、lineage 與 adoption rules 通過 gate 後，才新增 `generate_first_frame_candidates` intent；B4 不得先產出沒有 canonical identity／lifecycle 的九張 loose images。

選格不能只存在 browser local state，也不直接成為 canonical asset。Agent 必須正式採用 selection，並經 review／gate／checkpoint 發布。不得宣稱單張 3×3 生成必然維持幾何、光影、180 度軸線一致；裁切是否無損、解析度是否足夠與候選是否可當 first frame 都要由實際 media evidence 判定。

### B6 — Lenses／History／Diff

等 inspectors 經過實際使用後，再把同一批 projections 組合成：

- Prompt Review Lens；
- Style／CLP Consistency Lens；
- Quality／Failure Lens；
- Cost Lens；
- Provenance Lens；
- Course Coverage Lens；
- Delivery Lens；
- History／Diff Lens。

Lens 只保存 filter、query、layout preference 與 user display state；不擁有 artifact、不改 checkpoint、不建立第二套狀態模型。B1 的 Script／Style inspectors，以及 B2 的 CLP／Asset inspectors，會直接成為 Lens 元件，而不是被後期功能淘汰。

### 8.1 兩軌並行順序

```text
Track B: B0 -> B1 -> B2 --------> B4 -> B5 -> B6
                    |
                    +-----------> B3（inspection contract ready 後）

Track A: M6.0B closure -> separate A-to-B inspection contract -> PUP-specific intents
```

B0～B2 不等待 M6.0B。B3 也不應反過來把 private recovery/coordinator state 變成 Backlot API；Track A 只提供 consumer-safe inspection projection、validator 與 fixtures。

## 9. Track A → Track B interface

### 9.1 Current boundary

Track A 的 milestone 狀態只由 `docs/production-unit-protocol-implementation-plan.md` 維護；本文件只記錄 Backlot 可以或不可以依賴的 consumer boundary。

在 pinned dependency snapshot `df0f8ca` 可使用的 consumer boundary：

- M6.0A 已整合，提供 policy／execution vocabulary、qualification profile／capability matrix shape 與 fail-closed validators；
- `manifest_supported`、qualification status、approved policy、execution disposition 與 checkpoint status 必須分開呈現；
- 缺少 trusted profile／matrix resolution 時，Backlot 顯示 `unknown`，不得自行 follow opaque `profile_ref`；
- Track B 不對 M6.0B 的 live completion 狀態作假設；即使 recovery/candidate handoff contract存在，它也不自動成為 unit list、prompt、asset、aggregate progress或 recovery control API；
- B0～B2 完全不等待 M6.0B。

### 9.2 Separate inspection-contract slice for B3

**DECIDED**：Production Unit 詳細 inspector 需要一個緊接 M6.0B closure、但與 recovery coordinator 分離的 A→B inspection-contract slice。它應提供：

- versioned JSON schema 與 validator；
- sanitized、display-safe projection，不暴露 provider secrets、private chain-of-thought 或 mutable coordinator internals；
- exact run／stage／epoch／unit／work-item identity；
- exact lesson／section／scene／asset crosswalk；
- prompt record或 unavailable reason；
- selected result與其 authority；
- source checkpoint／artifact digests；
- valid、missing、stale、tampered、cross-epoch fixtures；
- backward-compatible absence semantics。

Track A 可以選擇 checkpoint-embedded artifact、validated evidence reference 或其他 bounded public surface，但 Track B 不讀 private sidecars、receipt directories 或 `state.json`，也不把 producer internal file layout固定成產品 API。

### 9.3 Handoff gate

1. GPT A 提供 review-ready commit、contract version、valid/invalid fixtures 與介面說明。
2. GPT B 只做 consumer review：authority、degraded behavior、backward compatibility、payload／privacy 與 Backlot usability。
3. 缺口以 interface note 回傳；雙方不直接修改對方 ownership 的檔案。
4. Contract 凍結後，Track B 才加入 B3 projection、API 與 tests。
5. Read-only inspection 不授權 PUP repair／resume／adoption；operational controls 必須另有 intent policy 與 qualification gate。

## 10. Workspace v1 read contract

### 10.1 Route and feature flag

- UI route：`/p/{project_id}/workspace`。
- API prefix：`/api/workspace/v1`。
- server-side flag：`BACKLOT_WORKSPACE_ENABLED`，process startup 時讀取，預設 `false`。
- flag off：新 UI/API 回 404；舊 `/p/{id}`、`/api/projects`、`/api/project/{id}/state`、SSE、media routes 與 response shape 不變。
- `/p/{project_id}/workspace` 必須在現有 `/p/{project_path:path}` catch-all 之前註冊，避免被舊 Board route 吞掉。
- 新 UI 使用獨立的 workspace HTML／JS／CSS modules；可重用 design tokens 與安全的 DOM/media helpers，不把 `board.js` 當 state store。

### 10.2 Endpoint split

候選 v1 endpoints：

| Endpoint | Phase | Responsibility |
|---|---|---|
| `GET /api/workspace/v1/catalog` | B0/B1 | compact project/course catalog；query、kind、cursor、limit |
| `GET /api/workspace/v1/projects/{id}/shell` | B0 | identity、manifest stage rail、gate、course outline summary、capabilities |
| `GET /api/workspace/v1/projects/{id}/course` | B1 | course revision set：current canonical與 pending candidates可同時存在 |
| `GET /api/workspace/v1/projects/{id}/script` | B1 | script summary／sections；query、cursor、limit、section key |
| `GET /api/workspace/v1/projects/{id}/style` | B1 | proposal／course／checkpoint／catalog style sources |
| `GET /api/workspace/v1/projects/{id}/clp` | B2 | CLP entity list／detail；kind、cursor、limit、resource key |
| `GET /api/workspace/v1/projects/{id}/scenes` | B2 | scene summary／exact bindings；filters、cursor、limit |
| `GET /api/workspace/v1/projects/{id}/assets` | B2 | asset list；scene、media type、provider、model、cursor、limit |
| `GET /api/workspace/v1/projects/{id}/assets/{resource_key}` | B2 | one asset detail + generation instructions + safe media refs |
| `GET /api/workspace/v1/projects/{id}/units` | B3 | only after A→B inspection contract |

Schema 中的 `section.id`、`asset.id` 等一般只是 string，不保證 URL-safe。Projection 必須提供 opaque、URL-safe `resource_key` 給 detail route；它應穩定代表 logical ResourceRef，revision 改變時由 RevisionRef／ETag處理。原始 logical ID 留在 `ResourceRef`，不能直接插進 URL path。

Known project 中缺少 optional artifact 時，回傳 `authority_state=unavailable` 的 envelope 與 reason；unknown project、非法／未知 `resource_key` 才使用 404。Invalid source fail closed，不回退成看似 canonical 的資料。

### 10.3 Snapshot, cache and SSE semantics

- `source_snapshot.composite_sha256` 是 digest-based projection token，並作為 ETag。
- detail response 綁定生成它的 source snapshot；pagination cursor 也必須綁定同一 snapshot，避免翻頁期間混入新版資料。
- browser 使用 `If-None-Match`；SSE 只作 coarse invalidation signal，不把完整 projection 塞進 event。
- change event 後只重新取得 shell 與目前可見的 detail；同一時間一個 in-flight refresh，期間變更最多排一個 trailing refresh。
- 不清空重建整頁；保留 scroll、focus、expanded state、lightbox selection 與 media playback position，除非其 ResourceRef 已失效。
- list endpoint 必須 bounded；媒體 bytes 永不內嵌 JSON。

### 10.4 Authority-preserving source resolution

Workspace 不直接 serialise `load_board_state()`。新的 resolver 只重用既有的安全 primitives：project containment、manifest loader、checkpoint validation、artifact validation、canonical digest 與正式 producer validator。

每一個 artifact family 依序判定：

1. 找出 manifest-declared owner stage 及 valid checkpoint；
2. 依 checkpoint lifecycle 分成 completed canonical、awaiting candidate、in-progress／failed display snapshot，或 invalid／missing unavailable；display snapshot永遠不取得 approval/publication authority；
3. 驗證 artifact schema／semantic contract並計算 digest；
4. 若存在 loose cache，只做 digest comparison／diagnostic，不自動取得 authority；
5. 只有沒有 modern authority、且該 family 明確允許 legacy fallback 時，才投影為 `display_only + unverified`；
6. invalid authoritative claim 不得悄悄回退到 loose file。

Resolver 不以「挑一份最新資料」抹除其他 lifecycle。若 current canonical 與 awaiting candidate 同時存在，兩者分別形成 `ProjectedRevision`；legacy cache則只作 comparison diagnostic，不成為第三份競爭 truth。

CLP、Batch V2 assets 與 course 已有較強 authority rules，必須保留。Generic script／scene／asset 等不能沿用現有 loose-first flattening而失去 provenance。Checkpoint status 與 Human Gate 必須顯示；單純「checkpoint 可解析」不足以把 awaiting／in-progress artifact標成 canonical approved。

### 10.5 Style and CLP source rules

Style projection 保持 field groups 分離，不把下列來源合成一個不可追溯 object：

- proposal creative direction；
- course `style_intent`；
- project/checkpoint playbook identity；
- current validated playbook content；
- scene-plan style observation／drift diagnostic。

Marker／checkpoint／proposal 只保存 playbook name，沒有歷史 YAML snapshot/digest；即使計算 current catalog digest，也只能代表目前解析內容。Source names 不一致時 `resolved_style=null`，由 diagnostic 解釋衝突。

CLP entity identity與 canonical image ref只取依 checkpoint lifecycle 分類後的 valid `clp_manifest`。依 ID／name 掃描到的圖片、legacy `character_design` 或資料夾影像只能作 display suggestion，不能取得 strict-reference／locked authority。`policy=strict_reference` 也不等於使用者已選定某個 take；必須同時顯示 canonical checkpoint authority 與已驗證 image digest evidence。

### 10.6 Media and declared-versus-observed metadata

- Projection 產生 contained `/media`／`/thumb` URLs；filesystem path不是 identity。
- Remote/GCS fallback 必須使用與 asset／CLP projection 相同的 authoritative source；不得另讀 loose manifest 後提供另一個 URL。
- `resolution`、`duration_seconds`、`format`、`quality_score` 等 manifest 值標為 `producer_declared`。若 probe 實體 bytes，結果標為 `tool_observed` 並有自己的 timestamp／digest；human review score另標 `human_reviewed` 並綁定 review evidence。各類 evidence並列，不得靜默覆寫。
- `seed`、provider、model、source tool、cost、quality 與 voice-performance fields 應直接由 schema-valid manifest 投影，避免舊 storyboard normalization 丟欄位。
- Script `source_ref` 是 free-form source metadata，可能是 research ID 或 URL；除非另有 typed mapping，不得把它變成 lesson／objective／asset cross-link。

### 10.7 Workspace information architecture

```text
Project/Course selector
  +-- persistent context bar: pipeline, stage/gate, authority health, PUP axes, cost
  +-- manifest-driven stage rail
  +-- course outline rail (when applicable)
  +-- active inspector
  |     +-- list/navigation pane
  |     +-- primary content
  |     +-- detail/provenance drawer
  +-- diagnostics drawer
```

URL query／fragment 保存 stage 與 ResourceRef selection；重新整理、browser back/forward 與貼上 deep link 都必須可還原。Lenses 到 B6 才加入，但 B1/B2 inspector components 必須能在不改變 projection contract 的前提下被 Lens 重用。

## 11. Verification, compatibility, security and rollback

### 11.1 Contract and projection tests

B0～B2 至少需要：

- schema positive／negative tests：projection envelope、ResourceRef、RevisionRef、AuthorityDescriptor、capabilities、diagnostics、pagination cursor；
- source precedence matrix：approved／awaiting／in-progress／failed／invalid checkpoint，matching／mismatched／missing loose cache；
- course candidate versus approved truth；
- style source matrix：missing／invalid playbook、proposal-marker-checkpoint drift、current catalog without historical digest；
- CLP zero-entity、non-empty approved、awaiting candidate、invalid owner checkpoint、mismatched cache、legacy scan；
- asset source matrix：ordinary checkpoint、legacy loose manifest、valid／invalid Batch V2 publication、missing prompt／seed／file；
- path containment、opaque resource key、unsafe media ref、remote URL authority；
- no `.production-units/`／`.batch-v2/` private scan；
- ordinary non-course、different pipeline shape、PUP off／opt-in／missing profile；
- feature flag off/on 與 old API shape parity。

Existing tests in `tests/backlot/` remain regression gates。Workspace tests should be separate enough that disabling the feature leaves old Board behavior untouched。

### 11.2 UI and accessibility tests

- project/course search and switch；
- deep-link restore、browser back/forward、refresh；
- script search／section navigation；
- Style palette／typography／rules rendering and invalid/degraded states；
- CLP keyboard navigation、entity detail、exact versus legacy image badge；
- image lightbox zoom/pan/close、video controls、audio controls；
- lazy loading、pagination、filter stability and empty states；
- keyboard-only flow、focus management、screen-reader labels、contrast and reduced motion；
- SSE refresh retains selection、scroll and media playback。

### 11.3 Performance gate

B0 先量測再凍結具體 budgets。測量至少包含：

- cold／warm catalog latency；
- shell、script、CLP、scene、asset list/detail latency；
- JSON compressed/uncompressed payload size；
- checkpoint/artifact parse count and cache hit rate；
- one SSE burst caused的 request count；
- initial／expanded DOM node count、main-thread render time and memory；
- image thumbnail versus original-byte loading；
- large `events.jsonl` and history behavior。

代表 fixture 必須接近 40～60 分鐘課程的 sections／scenes／assets 規模，不能用目前單 scene performance fixture 代替。若 vanilla DOM 無法達到經核准 budgets，再以量測證據提出 framework／virtualization migration，不預先更換整套前端。

### 11.4 Security and deployment boundary

- B0～B2 的正式支援面維持目前 loopback／local-user 模式；LAN/shared deployment 必須另有 authentication、authorization、session／CSRF、audit retention 與 media exposure RFC。
- project ID、resource key、cursor、media path與所有 source refs 均視為 untrusted input；resolve 後仍須 containment／schema validation。
- server 不 follow opaque `profile_ref`、任意 local path或未核准 remote URL，不把 secrets／provider credentials 投影給 browser。
- GET projection 不取得 approval、provider、publication、budget 或 filesystem write authority。
- thumbnail／projection cache 必須是可刪除的 server-owned cache；不得與 canonical project artifacts 混淆。
- 現有 GCS sync 是 operations utility，不因 Workspace 出現而成為 production authority；是否保留於 UI 延後決定。

### 11.5 Compatibility and rollback

- 新 code additive；不改動舊 `/state` response shape，不搬移 project files，不 migration canonical artifacts。
- flag 預設 off。Rollback 是關閉 flag並停止註冊新 routes；canonical project state無需回復。
- 新 projection version 只能向後相容新增 optional fields，或另開 version；不得在同一 version 靜默改變 authority 語意。
- server-owned cache 可丟棄重建，不成為 rollback prerequisite。
- B0～B2 的自動化 no-authority-escalation test 應比較操作前後的 checkpoints、artifacts、decision log、style catalog 與 project marker；允許明確列出的 thumbnail／projection cache變動。

### 11.6 Later-phase gates

#### B3 Unit Inspector

- [ ] A→B versioned inspection contract、validator與 fixtures 已 review-ready／integrated。
- [ ] Missing contract只讓 unit details unavailable，不影響 B0～B2。
- [ ] No private sidecar reads，no inferred crosswalk，no recovery authority。

#### B4 Agent Intent

- [ ] Actor／authorization、idempotency、digest binding、stale target、cost disclosure、cancellation與 result binding 有 versioned contract。
- [ ] Request 與 canonical state在 storage、API與 UI 清楚分離。
- [ ] Agent unavailable、stale revision或 unsupported action皆 fail closed。

#### B5 Candidate Set

- [ ] Candidate／selection／lineage schema、migration、history、invalidation與 cost／approval rules 完整。
- [ ] UI local selection不能冒充 adopted/canonical。

#### PUP operational controls

- [ ] Track A 提供適用 contract／evidence與 consumer fixtures。
- [ ] 對應 profile達到該 action 所需 qualification；read-only顯示不自動授權 repair／resume。
- [ ] PUP experimental／opt-in／qualification 文案與實際 evidence 一致。

## 12. Assumptions register

每個暫定方向都要有可推翻條件，避免 `PROVISIONAL` 在討論中悄悄固化。

| ID | Assumption | 需要的證據 | 何種結果會推翻 | Owner／最晚決定點 |
|---|---|---|---|---|
| B-A004 | 現有 vanilla DOM 可作首版基礎 | B0 large-course performance/accessibility fixture | 無法達到核准門檻，且 migration 有較低總風險 | Track B／B0 exit |
| B-A005 | Compact + lazy + paginated read model 足以支撐首版；virtualization按量測加入 | B0 fixture benchmark | 即使 bounded API，實際 DOM／memory仍超標 | Track B／B0 exit |
| B-A006 | 結構化 intent 是互動的正確邊界 | B4 threat model、Agent acknowledgement與 workflow prototype | 無法可靠綁定 actor／target／result，或另有不擴權且更簡單的 mechanism | User + Track A/B／B4 RFC |
| B-A008 | Loopback/local-user deployment可滿足 B0～B2 | 實際使用情境與部署需求 | 首版必須多人／LAN協作 | User／B0 kickoff |
| B-A009 | `/p/{id}/workspace` 是最清楚的 deep-mode route | prototype navigation與 route-conflict tests | 使用者需要跨 project persistent workspace，或 route hierarchy造成不可接受限制 | User + Track B／B1 UI review |

## 13. Decision log

這裡記錄設計過程本身的決策。若決定改變，新增一列並指向被取代項目，不靜默改寫歷史。

| ID | 日期 | 類型／狀態 | 決定 | Decided by／evidence | Supersedes | 理由／影響 |
|---|---|---|---|---|---|---|
| B-D001 | 2026-09-16 | working agreement | GPT A 負責 Track A；GPT B 負責 Track B3 與協調 | User；本對話中的明確分工 | — | 分離 M6 producer contract 與 Backlot consumer/product design |
| B-D002 | 2026-09-16 | working agreement | Track A M6 狀態與 Track B Backlot 規劃使用不同文件 | GPT A 提案、User 接受後繼續；本對話 | — | 避免雙方同改一份狀態來源 |
| B-D003 | 2026-09-16 | decided | 先建立可推翻的 v0 基線，逐題討論，最後整體重寫 v1 | User：「同意，執行吧」 | — | 同時降低記憶流失與過早定案風險 |
| B-D004 | 2026-09-16 | provisional | Backlot 平台 + Board Overview + Director Workspace deep mode | GPT B recommendation；待 D1／D3 | — | 避免平行 UI／state model，但尚待 user-job 驗證 |
| B-D005 | 2026-09-16 | provisional under constraint | Backlot 作 projection／intent gateway，Agent 保持 execution control plane | GPT B recommendation；受 `AGENT_GUIDE.md` 與 PUP hard boundary 約束 | — | Intent transport 未定，但不得弱化既有 authority boundary |
| B-D006 | 2026-09-16 | working interface handoff | `6478309` 可供 fixture-driven observer shape／UX design，但在 merge 前不是已整合契約，且尚不足以支援 live effective qualification | GPT A handoff + GPT B diff／focused-test／consumer-authority review | — | 解鎖 vocabulary/UI 討論；discovery、trust、selection 與 legacy authority finding 仍須收斂 |
| B-D007 | 2026-09-16 | decided | Backlot + Board Overview + Director Workspace deep mode 是同一產品的三層體驗 | User 同意 B0～B6 基線並要求開始撰寫 | B-D004 | 不建立第二套資料模型或 control plane |
| B-D008 | 2026-09-16 | decided under constraint | Backlot 是 versioned projection／intent gateway；Agent保持唯一 execution control plane | User 同意開始正式化；`AGENT_GUIDE.md` hard boundary | B-D005 | B0～B3 read-only；B4 也只提交 request |
| B-D009 | 2026-09-16 | integrated status | M6.0A 已隨 `df0f8ca` 整合；live trust/resolution仍不得由 Backlot 猜測 | `team-main @ df0f8ca` | B-D006 | Candidate vocabulary已成基線，但不擴張其 authority claim |
| B-D010 | 2026-09-16 | decided | 第一個 release 為 B0＋B1＋B2 | User 同意前述方案並要求開始撰寫 | — | 優先交付課程、劇本、Style、CLP、prompt與媒體檢視 |
| B-D011 | 2026-09-16 | decided | Workspace 使用獨立、default-off feature-flagged route；舊 Board保持不動 | User 接受建議後要求開始撰寫 | — | 隔離 rollout／rollback與 API evolution |
| B-D012 | 2026-09-16 | decided | B3 的 A→B inspection contract另立 slice，不擴大 M6.0B recovery scope | Track A/B 協調討論 | — | B0～B2 可立即進行；Backlot不讀 private sidecar |
| B-D013 | 2026-09-16 | decided | Style在 B1；CLP與 media primitives在 B2；兩者都是首版必交付 | User明確補充需求 + current source audit | — | Style需先於媒體理解；CLP images/bindings重用 B2 viewer基礎 |
| B-D014 | 2026-09-16 | decided | B0～B6 取代舊 Phase 0～4 rollout；Lenses不擁有 truth | User接受討論版 v0.1並要求正式撰寫 | — | 前後期功能共用 ResourceRef／Projection／Intent窄腰層 |
| B-D015 | 2026-09-16 | decided | `docs/backlot-director-workspace-plan.md` 作 Track B 現行主文件；`studio_draft.md`保留為 vision history | 現有 working plan + 避免產生重複主文件 | — | 文件名可日後另做純 rename，但不得同時維護競爭版本 |

## 14. Revision protocol

- 每完成一個 phase contract或產品決策，更新相關段落與 decision log。
- 暫定建議升格時改為 `DECIDED`；被推翻時保留 supersession 紀錄並更新 assumptions register。
- 牽涉 Track A producer contract 的結論，先形成 handoff note，不直接改 Track A 檔案。
- Track A milestone細節不複製進本文件；只更新 consumer boundary與 dependency status。
- B0 schema/API RFC完成後，以它們取代本文件中的示意 JSON與候選 endpoint；不得讓示意 shape永久成為未驗證實作。
- 達到對應 readiness gate 後才開始該 phase；不必等待 B3～B6 全部定案。
