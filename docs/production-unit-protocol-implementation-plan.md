# OpenMontage Production Unit Protocol 與長課程支援 — Implementation Plan

> 狀態（2026-09-16）：第一個支援輪廓的 Lean M0～M5 functional slice 已合併至
> `team-main` 並同步至 `team-fork/team-main`；整合 commit 為
> `4d4c28c5cfed953d4cdd2cf5f0c5387b1daeeaa8`。PUP 目前仍是
> experimental、opt-in implementation；M6 qualification 與 rollout 尚未完成。
> 本文件是實作紀錄與 rollout 邊界，不構成 production qualification、provider
> 呼叫或部署授權。
>
> 實作快照：`team-main` @ `4d4c28c5cfed953d4cdd2cf5f0c5387b1daeeaa8`
>（2026-09-16；後續 M6 開始前必須重新凍結依賴、runtime 與 provider 輪廓）
>
> 第一個支援輪廓：單一 direct-child OM project、既有 pipeline DAG、40～60 分鐘課程、Production Unit opt-in
>
> 目前操作契約：`skills/meta/production-unit-protocol.md`、
> `skills/creative/course-form.md`、`schemas/artifacts/course_manifest.schema.json`
>
> 實驗證據：[30 分鐘 PUP vs off benchmark](production-unit-benchmark-30m.md)

### 目前 milestone 狀態

這裡的「完成」只表示第一個支援輪廓的 lean functional slice 已實作、測試、合併；
不表示原始 roadmap 中所有 aspirational gates 已滿足，也不等同 beta 或 production
qualification。

| Milestone | 狀態 | 已落地範圍／剩餘邊界 |
|---|---|---|
| M0 | 完成（lean） | 責任邊界、術語、Course Form 與 PUP 操作契約已收斂；未採用且狀態過時的大型 RFC 草稿未納入。 |
| M1 | 完成（lean） | Course/PUP contracts、path safety、`mode=off` 相容路徑及相應離線測試已落地。 |
| M2 | 完成（lean） | Script、CLP、scene plan 的 unit partition、context capsule、deterministic merge、coverage 與 boundary validation 已落地。 |
| M3 | 完成（lean） | Asset units 已接入 Batch V2 的 request／attempt／receipt 邊界，維持既有 publication authority。 |
| M4 | 完成（lean） | Edit merge、per-unit render contract、master assembly 與 resume／invalidation 邊界已落地。 |
| M5 | 完成（lean） | Course routing、Backlot observer-only projection、progress 與 delivery projection 已落地。 |
| M6 | 執行中（M6.0A follow-up review-ready） | Vocabulary 已分離為 approved policy mode 與 execution disposition；legacy helper seam 已明確降為 non-authoritative diagnostic；versioned qualification profile／capability matrix 最小契約、positive/invalid fixtures 與測試已建立。Live discovery/resolution、evidence/manifest trust binding、M6.0B～M6.3、跨 OS slow gate、真實 E2E、故障恢復、telemetry calibration 與 rollout 決策仍未完成。 |

目前可支持的陳述是：OM 已有可關閉、可回退的 bounded production-unit execution
與 deterministic merge 能力，而且凍結的 30 分鐘比較中 PUP 勝過該次 baseline。
目前仍不可宣稱所有 pipeline／runtime 都已支援 60 分鐘、180 秒是普遍最佳值，或
PUP 已經 production-qualified。M6 的資格門檻與證據要求仍以本文件第 10、11、15
節為準。

### 實作收斂說明

原 M0 規劃過的多份大型 RFC 草稿沒有納入目前候選；它們仍含
`definition only`／`not implemented` 等過時狀態，且會與已完成的 lean
implementation 互相矛盾。現階段以已測試的 schema、Python adapters、pipeline
directors、`course-form` skill 與 PUP meta skill 為準。若日後需要正式
qualification profile，應在 M6 以當時實際支援的 pipeline × runtime × provider
輪廓重新制定，而不是把舊草稿直接升格為規範。

## 1. 要交付的能力

本計畫的目的不是宣稱「OM 天生只能專注 180 秒」，而是增加一個可設定、可量測、可停用的 **Production Unit Protocol（PUP）**，使 Agent 在處理長課程時，每次只承擔一個有完整語意邊界的工作範圍，最後再以機械式驗證與合併產生既有 OM artifact。

完成本計畫後，目標能力如下：

1. 一門 40～60 分鐘課程仍是一個正常 OM project，沿用一套 pipeline manifest、stage order、checkpoint chain 與 Human Gates。
2. `script`、CLP、`scene_plan`、assets、edit、compose 可在 stage 內分 Production Units 執行；Agent 不需一次生成或審查整門課的高密度細節。
3. Unit 共享同一份已核准課程設計、術語、風格與 CLP；任何 context 變更都有 digest-based invalidation，不靠對話記憶同步。
4. Unit fragment 只是非 canonical staging；每一 stage 完成時仍發布現有完整 artifact，例如 `script`、`scene_plan`、`asset_manifest`、`edit_decisions`、`render_report`。
5. Backlot 只需讀取已驗證的課程描述、checkpoint 與 unit 進度投影，不成為新的 production state authority。
6. PUP 關閉時，既有短片及 long-form 工作流不產生 PUP sidecar、不改 tool routing、不改 gate，並通過 legacy parity tests。

這不是「所有 pipeline × 所有 renderer 已保證支援 60 分鐘」的承諾。能力與資格必須分開標示：

- **code-complete**：合約、離線 fixture、失敗恢復與 legacy parity 通過。
- **beta-qualified profile**：一個明確的 pipeline × render runtime 完成經授權的真實 60 分鐘 E2E。
- **production-qualified profile**：至少三個符合 versioned qualification profile 取樣矩陣的真實課程及故障注入通過，且全部 telemetry 達到該 profile 的量化門檻。

## 2. 不可破壞的架構不變量

以下條件是 hard gates，不是建議：

1. **Agent 仍是 control plane。** Agent 決定語意邊界、創意內容、provider 與 review，並依 manifest 的 binding gate policy 提交 Human Gate；是否需要 human approval 由 pipeline manifest 決定，不由 Agent 或 Python 重判。Python 只驗證並物化 Agent-authored partition，負責合約、路徑安全、digest、機械式切片／合併、持久化及 telemetry，不自行判斷課程語意。
2. **PUP 是 stage-internal execution layer，不是新 pipeline state machine。** 它不得自行推進 stage、核准 checkpoint 或繞過 pipeline manifest。
3. **單一 project identity。** MVP 不建立 `projects/<course>/chapters/<chapter>` 型子專案，也不修改 `resolve_project_dir()` 的 direct-child identity 契約。
4. **既有 stage canonical outputs 不被替換。** Unit fragments 不加入 `ARTIFACT_NAMES`，也不放入 checkpoint `artifacts`；正式 checkpoint 仍包含原本 schema-valid 的完整 artifact。Course support 只額外加入一份 optional、proposal-owned `course_manifest`，且不得承載 unit lifecycle。
5. **Checkpoint 與 Human Gate 不變。** Unit 完成不等於 stage 完成；只有所有 units 通過 merge gate 與 Agent review 後，才可依原 protocol 寫 `awaiting_human` 或 `completed`。
6. **CLP authority 不變。** 必須保留：

   ```text
   script
     -> clp_candidates
     -> clp_manifest
     -> scene_plan
     -> clp_shot_bindings
   ```

   不新增 `master_clp.json`，也不允許 unit 自己建立獨立 CLP authority。
7. **Backlot 是 observer。** Backlot 可顯示 PUP 狀態，但不得寫入、修復或裁決 unit／checkpoint 狀態。
8. **預設關閉。** 未出現已核准且 schema-valid 的 PUP policy 時，一律視為 `mode=off`。
9. **180 秒只是實驗預設。** 時長是 soft target；教學語意邊界、input/output complexity budget 與 renderer 能力優先。
10. **無隱性外部副作用。** 離線測試不得讀 credentials、呼叫 provider、部署、寫 GCS 或產生付費媒體。
11. **Digest 格式不偷換。** CLP 現有 `sha256:<64 hex>` 與 Batch V2 的 bare 64-hex 欄位各自維持既有格式；PUP schema 必須逐欄明定格式，不做隱性轉換，也不發明第三種可混用格式。

任何 milestone 若必須違反上述條件才可前進，應停止並回到 RFC，而不是在實作中臨時繞過。

## 3. 五個概念的責任分工

| 概念 | 負責什麼 | 不負責什麼 |
|---|---|---|
| `long-form.md` | 約 8～15 分鐘影片的留存、節奏、章節、影音創作方法 | OM 的系統容量、檔案分片、checkpoint 或 unit orchestration |
| `course-form.md` | 40～60 分鐘課程的學習目標、modules／lessons、先備知識、回顧與評量設計 | 執行切片、資料夾、重試、合併或渲染 |
| Production Unit Protocol | 將 stage 工作限制在有界 context，定義 unit input、result、merge、resume、telemetry | 課程教學法、pipeline stage order、Human Gate 決策 |
| Course Container V2 | 一個 project 內的課程描述、共享資源 ownership、交付與聚合語意 | 把 lesson 變成 nested OM project，或複製 CLP／狀態真理 |
| Backlot | 將 canonical checkpoint 與 PUP sidecar 投影為課程／unit UI | 成為 writer 或 recovery authority |

必須維持以下非等價關係：

```text
Course module / lesson ≠ Production Unit ≠ filesystem directory ≠ pipeline stage
```

一個 lesson 可對應多個 Production Units；一個 unit 在不同 stage 也可重新切分。不能因為教學章節是 8 分鐘，就強迫每個生成或 render unit 都是 8 分鐘。

## 4. 啟用與設定模型

### 4.1 三種 mode

| Mode | 行為 |
|---|---|
| `off` | 完全沿用 legacy stage director 行為；不建立 `.production-units/` |
| `auto` | Agent 依語意邊界與 complexity budget 建立 units；`target_seconds` 只是提示 |
| `fixed` | 使用者／已核准 proposal 指定 target 或限制；仍不得切斷不可分割的語意或媒體原子 |

第一輪建議值：

```json
{
  "mode": "auto",
  "target_seconds": 180,
  "boundary_priority": "semantic_first",
  "oversize_policy": "allow_with_reason"
}
```

不把 `180` 寫入 OM core invariant。每個 unit 除時長外，至少還要受以下 budget 約束：

- source sections／scenes 數量；
- input token estimate；
- expected output token estimate；
- asset count／預估 provider calls；
- renderer frame／resource estimate；
- 不可切割的 lesson、demonstration、argument 或 transition 邊界。

`fixed` 也不是以秒數在句中硬切：Agent／使用者先指定可接受的 section／scene boundary set，Python 只能以明定 tie-break 規則在該集合中選擇並驗證；若無合法 boundary，就產生 oversize unit 或 fail closed，而不是破壞語意原子。

### 4.2 Policy 的 canonical 位置

PUP policy 應作為 `proposal_packet.production_plan` 的**可選 typed 欄位**，由 proposal Human Gate 一起核准。不存在時等於 `off`。這讓 mode、目標與支援 stages 有明確 provenance，而不是藏在聊天內容、環境變數或 Backlot UI 中。

Pipeline manifest 的可選 `extensions.production_units` 只聲明該 pipeline 支援哪些 stages；它不代替專案層已核准的 policy，也不自動啟用 PUP。

```yaml
extensions:
  production_units:
    supported: true
    default_mode: off
    supported_stages: [script, clp, scene_plan, assets, edit, compose]
```

Manifest 沒有此 block、`supported=false`，或專案要求未列出的 stage/runtime 時，不得靜默假裝已 unitize；是否沿用 monolithic 或 fail closed 取決於已核准 proposal，規則如下。

更精確的判定如下：

- proposal 沒有 PUP policy：使用既有 monolithic path；
- proposal 明確核准 PUP，但 pipeline／stage／runtime 不支援：preflight 必須停止，不能 silent fallback；
- 若要從已核准 PUP 改走 monolithic：必須更新 proposal／decision evidence，並重新通過原 Human Gate；
- `execution_disposition: compare_only | publish_candidate` 是 unit plan 的執行意圖，不是第四種 mode。`compare_only` 永遠禁止 canonical publish；若涉及付費 call，仍需獨立授權。

另設一個只會**降低能力**的 audited emergency disable override。它不修改已核准 proposal，也不能把 `off` 變成 `auto`：

- stage 尚未開始：effective mode 變為 disabled；只有原 monolithic path 經重新核准後才可繼續；
- stage 執行中：停止新 dispatch，保留 attempts/receipts，不 merge、不 canonical publish；
- override 的來源、操作者、時間與原因要進 audit evidence／Backlot diagnostics；
- 解除 override 不得自動續跑 ambiguous 或 stale attempts。

Override／resume 必須形成 immutable、ordered control chain，而不是可覆寫的布林旗標。每筆 override 綁定 project/run/stage、proposal/policy/checkpoint/state digests、前一筆 control-chain digest、操作者 authority、reason 與遞增 event sequence。Active override 存在時，任何新 dispatch、merge 或 publish command 都必須 fail closed。

恢復 PUP 只能由另一份獨立的 Agent/user-authorized `production_unit_resume_authorization` 完成；它必須綁定最後一筆 override、當前 canonical checkpoint/state、必須重做的 units，以及每一個允許跨 epoch 重用的 exact result/context/provider-receipt digest，並開啟新的 `execution_epoch`。這是 operational resume authority，不得改變 proposal policy 或取代既有 Human Gate；涉及 ambiguous charged attempt、creative decision 或改走 monolithic 時，仍要遵守原有 approval/reapproval 規則。

Coordinator 必須在新 epoch 為每一組 reusable evidence 產生 immutable `production_unit_adoption_receipt`，重新驗證 predecessor checkpoint、policy、course、CLP、media profile、source/state digests 與 schema/protocol compatibility，並綁定 resume authorization 與 source/target epoch。Merge/publication 只能引用本 epoch 產生的 result，或由本 epoch exact adoption receipt 採認的 result；按 `unit_id`、latest attempt 或模糊範圍放行一律無效。

所有在新 epoch 產生的 dispatch/context/result、adoption、merge/publication command、receipt、stage state 與 checkpoint-transition provenance 都要綁定 `execution_epoch` 與當下 `control_chain_digest`。舊 epoch 的 sealed evidence 保留可讀，但不能直接重放成新工作或發布權限；每個 official checkpoint transition 都必須驗證完整 override/resume chain，而不是只相信最後一個 `disabled=false` 狀態。

`proposal_packet.production_plan` 另加 optional typed `content_form`（例如 `short_form | long_form | course_form`）。當值為 `course_form` 時，同一個 approved proposal checkpoint 必須包含 `course_manifest`；PUP preflight 與 checkpoint reader/writer 都要驗證這個條件。不要用 duration 猜測 content form。

## 5. Course Manifest V2

`course_manifest` 是課程的**靜態、宣告式** canonical artifact，第一個支援 profile 由 proposal stage 可選產生，並與 proposal 一起接受 Human Gate。

它應包含：

- `version`、`project_id`、課程標題、目標時長；
- audience、entry requirements、learning objectives；
- 有順序的 modules／lessons；
- 每個 lesson 的目標、先備依賴、預期成果、target duration、source refs；
- 共用 glossary／notation／style intent 的宣告或 canonical refs；
- 最終交付需求，例如 full master、lesson exports、chapter markers、captions。

它不得包含：

- mutable `status`；
- `render_output`；
- unit attempt／retry 狀態；
- 第二份 CLP；
- 可由 checkpoints、artifact、events 或 filesystem 推導的成本與進度。

課程的實際狀態仍來自 checkpoints；CLP 仍來自 `checkpoint_clp.json`；render 路徑仍來自 `render_report`。如此 Backlot 可輕鬆辨識課程，而不會出現兩套真理。

第一個 profile 需在 pipeline manifest 中引入 `optional_produces`，讓 proposal 可選產生 `course_manifest`，而一般影片不被迫產生它。這是 additive schema change；既有 manifests 與 artifacts 必須保持有效。

```yaml
- name: proposal
  produces: [proposal_packet, decision_log]
  optional_produces: [course_manifest]
```

Checkpoint validator 必須驗證 `course_manifest` 只能由宣告它的 stage 發布；後續 stage 只能消費該 approved predecessor，不可夾帶另一份不同內容的 course manifest。

## 6. PUP execution sidecar 合約

### 6.1 檔案位置

建議保留單一 project 的既有目錄，只新增被明確排除於 canonical artifact 與一般媒體掃描之外的 hidden subtree：

```text
projects/<project-id>/
├── project.json
├── artifacts/                       # 現有 canonical artifacts
├── assets/                          # 現有正式 assets
├── renders/                         # 現有正式 renders
├── checkpoint_<stage>.json          # 現有 checkpoint authority
└── .production-units/
    ├── control/
    │   ├── overrides/<override-id>.json
    │   └── resume-authorizations/<authorization-id>.json
    └── runs/<run-id>/
        ├── run.json
        ├── telemetry.jsonl
        └── stages/<stage>/
            ├── plan.json
            ├── state.json
            ├── adoptions/<adoption-id>.json
            ├── units/<unit-id>/
            │   ├── context.json
            │   └── attempts/<attempt-id>/
            │       ├── result.json
            │       ├── fragment.json
            │       └── receipts/
            ├── merge-command.json
            ├── merge-receipt.json
            ├── checkpoint-transitions/
            │   └── <sequence>-<transition-id>.json
            └── publication/                 # 僅 PUP-owned publication 使用
                ├── commands/<command-id>.json
                └── receipts/<receipt-id>.json
```

所有解析都必須 fail closed：resolve 後仍位於同一 direct-child project、不得經 symlink／junction 改變 identity、不得寫入 `artifacts/`、`assets/`、`renders/`、`history/` 或 `checkpoint_*.json`。

Override、resume authorization、adoption receipt 與 checkpoint-transition provenance 使用 contained、immutable、no-replace records，control records 與 checkpoint transitions 各以 previous digest + event sequence 形成可驗證 chain。`run.json`、plan、context、attempt result、Agent-authored command 與 receipt 一經封存亦 immutable；只有 stage `state.json` 可由單一 coordinator 以 temporary file + atomic replace 更新。任何一份 state 都不得被解讀成 pipeline approval。

### 6.2 `production_unit_plan`

至少包含：

- protocol／schema version；
- `run_id`、`project_id`、`pipeline_type`、`stage`、mode、起始 execution epoch／control-chain digest；
- 已核准 policy digest；
- authoritative predecessor checkpoint／artifact digests；
- course manifest digest（課程模式時）；
- ordered unit IDs；
- 每個 unit 的 source section／scene／lesson IDs、global time span、dependencies；
- 估算 budgets 與超過 soft target 的理由；
- plan 自身 digest。

Unit boundary 必須以穩定 artifact IDs 表示，不得只用 array index 或檔案位移。

### 6.3 `production_unit_context`

Context capsule 只攜帶該 unit 所需內容與全域 truth 的 digest-bound reference：

- course／proposal／script／CLP／style 的 authoritative digests；
- scoped source sections／scenes；
- glossary、locked terms、角色／場景／道具 refs；
- 前一 unit 的 exit state 與下一 unit 的必要預告；
- global timing offset 與 local `0..duration` mapping；
- 禁止事項、renderer／media profile lock；
- capsule digest。

Context capsule 不可複製並修改 CLP。需要的 CLP subset 只是 cache/view，必須能以 digest 與 ID 回溯到完整 `clp_manifest`。

### 6.4 `production_unit_result`

至少包含：

- unit、plan、context、attempt identity；
- 產生該 attempt 時的 execution epoch／control-chain digest；
- input/output digests；
- fragment type 與 contained path；
- schema／semantic validation outcome；
- warnings、repair count、terminal outcome；
- provider/tool receipts（若有）與成本摘要；
- 前後 boundary state；
- telemetry refs。

同一 unit 的多次嘗試不可覆寫。選用哪一次 result 是 Agent review 決策；Python 只驗證被選 result 的 identity 與完整性。

#### 6.4.1 Cross-epoch adoption

舊 epoch result 不可只靠相同 `unit_id` 被新 epoch 直接使用。Resume authorization 必須列出每個允許重用的 exact result、context、fragment、provider receipt 與 source-epoch digests；coordinator 再逐項重驗 predecessor checkpoint、policy、course、CLP、media profile、source/state、schema 與 protocol compatibility，產生本 epoch 的 immutable `production_unit_adoption_receipt`。

Adoption receipt 必須綁定 source/target epoch、resume authorization、完整 control chain、舊 evidence digests、重新驗證結果與採認 scope。任何 digest 不符、ambiguous provider outcome、跨越未核准 creative change 或 compatibility rule 不允許時都不得 adoption。後續 merge/publication command 只能選取本 epoch result，或同時引用 exact old result + 本 epoch adoption receipt；receipt 不可讓舊 command、舊 approval 或舊 publication capability 一併復活。

### 6.5 `production_unit_merge_command`

Agent review 後必須明示寫出 immutable merge command，至少綁定 plan／policy／context digests、execution epoch／control-chain digest、每個 unit 被選取的 exact result digest、必要的 adoption receipt、unit review evidence、任何 conflict resolution map，以及預期 artifact type。Python 不得自行挑「最新」或「成功」attempt。

每個 official checkpoint transition 的 `metadata.production_units.provenance` 必須是 schema-level discriminated union；同一 artifact 只能符合一種 publication authority，禁止混合兩套 command／receipt：

- `pup_json_merge`：script、CLP、scene plan、edit 等 JSON artifact 只引用 PUP merge command／merge receipt，最後仍由既有 checkpoint writer 發布；
- `batch_v2_assets`：assets 只引用既有 Batch V2 `PublicationCommand`／`PublicationState`（及其 receipts）作為唯一 publication authority。PUP result 綁定 exact BatchResult/work-item/publication digests，Batch publication records 也以 additive provenance 綁定 PUP plan、selected-result 與 control-chain digests；不得再產生 PUP publication command；
- `pup_render`：PUP-owned render/master 才使用 Agent-authored `production_unit_publication_command` 與 immutable `production_unit_publication_receipt`，綁定 selected results、targets、content digests、cost/approval evidence、execution epoch/control chain 與 no-replace/idempotency policy。

每次 official checkpoint state transition 都產生一筆 append-only、hash-chained `production_unit_checkpoint_transition_provenance`，綁定該 variant 的唯一 command/receipt/state refs、canonical artifact digest、目標 status、checkpoint identity 與前一筆 transition digest。`awaiting_human` 記錄綁定待審 checkpoint；`completed` 記錄必須綁定 exact preceding `awaiting_human` checkpoint/provenance、既有 Human Gate reply／decision evidence，以及該 variant 在第二次 transition 所需的 command/state（包括 Batch V2 既有的第二份 PublicationCommand）。不得覆寫第一筆 provenance，也不得另外發明 PUP approval。Merge、Batch publication 或 PUP publication command 都不等於 Human approval；checkpoint reader/writer 必須依 artifact/stage/status 驗證正確 variant 與 transition chain，拒絕 hybrid、缺欄位或錯誤 authority。

### 6.6 `production_unit_merge_receipt`

Merge receipt 應證明：

- 使用了哪些 ordered unit result digests；
- predecessor 與 policy digests 未改變；
- coverage、order、ID uniqueness、timeline、references 全部通過；
- 合併後 artifact 通過既有 JSON Schema 與 semantic validators；
- 合併後 canonical digest；
- merge tool／protocol version；
- execution epoch 與完整 control-chain digest。

若 checkpoint 的 `metadata.production_units` 宣稱 PUP provenance，checkpoint read 與 write 都必須載入其 exact contained checkpoint-transition provenance、前序 transition chain，以及 discriminated variant 所需的 merge receipt、Batch publication records 或 PUP publication receipt，驗證 project/stage/run/plan/policy/command/artifact、status、Human Gate evidence、execution epoch 與完整 control-chain digests。驗證失敗時 checkpoint 為 invalid；receipt 不能只是無人查驗的 advisory log。

Checkpoint `metadata.partial_progress.production_units` 只記錄 protocol version、`run_id`、stage、plan/policy/state digests、completed/failed unit IDs、counts 與 contained refs。它必須保留其他既有 partial-progress namespaces，不可內嵌未完成的巨大 artifact，也不可被 Backlot 當成 stage completion。

Merge candidate 必須先留在 `.production-units/`。通過 Agent review 後才交給既有 artifact validator 與 `write_checkpoint()`；不得先把未核准 loose artifact 寫到 `artifacts/`，讓 Backlot 在舊 checkpoint 旁讀到新內容。若 pipeline 同時維護 loose mirror，其內容必須與已發布 checkpoint artifact digest 完全一致，且 publication order／recovery 必須有測試。

### 6.7 Canonical publication 與 crash consistency

每次 PUP artifact publication 與 official checkpoint transition 都需要 single coordinator lock，並且只能使用第 6.5 節 variant 指定的唯一 authority command：`pup_json_merge` 使用 merge command、`batch_v2_assets` 使用既有 Batch V2 PublicationCommand、`pup_render` 使用 PUP publication command。建議順序為：驗證 variant-specific command/approval、adoption receipts 與當前 control chain → 將 selected bytes 以 content-addressed/no-replace 方式放入 canonical target → 重新驗證 bytes → 完成 variant-specific immutable receipt/state 與本次 checkpoint-transition provenance → 透過既有 official writer 寫該次 checkpoint（authority 最後可見）→ 修復 projection/state。由 `awaiting_human` 轉為 `completed` 時另寫下一筆 provenance，綁定原 Human Gate evidence；不得覆寫前一筆或增加 PUP gate。Loose mirror 在 checkpoint 前不得成為 Backlot authority。

M1 必須先對既有 `lib/checkpoint.py` 做 failure injection：candidate、canonical bytes、decision-log merge、checkpoint archive/temp/replace、receipt/state repair 的每一個 crash boundary，以及 disk-full、permission failure、兩個 coordinator 競爭。可接受結果只能是完整舊 authority或完整新 authority；不得出現 mixed provenance。若現有 writer 無法滿足，PUP capability 維持不可啟用，先提出一個 additive transaction/recovery slice，不能用文件假設掩蓋。

PUP-owned render publication 需要 PUP command、content digest、receipt、idempotent/no-replace target 與 checkpoint-last；Batch-owned assets 則沿用 Batch V2 command/state/receipt 的等價保證，不另建 PUP publisher。「master assembly 可重跑」本身不足以證明正式 `renders/` 與 `render_report` 的原子一致性。

## 7. 各 stage 的 unit 行為

### 7.1 Proposal／course design

- `course-form.md` 引導 Agent 產生課程架構與 `course_manifest`。
- proposal 鎖定 PUP policy、renderer family、render runtime、composition mode、media profile、成本與 provider 計畫。
- proposal Human Gate 核准前不得展開完整 scripts 或付費 assets。

### 7.2 Script

- 由已核准 `course_manifest` 的 lesson objectives 與 prerequisite graph 建立 script units。
- 每次只展開一個 bounded lesson／lesson slice，並提供相鄰 boundary context。
- 機械式 merge 檢查 section ID、順序、全域時間、word/time budget、來源引用與 objectives coverage。
- merge 後才形成完整現有 `script` artifact，並走原 script review／Human Gate。

### 7.3 CLP

- 可分 unit 抽取 `clp_candidates`，但只能在 merge 後形成一份 course-wide candidates 與一份 `clp_manifest`。
- 同 ID 的候選有衝突時，機械 merge 必須停止並輸出 digest-bound conflict set；Agent 產生 versioned resolution map／decision evidence。帶同一 resolution map 重播後，merge 必須 deterministic；程式不可自行猜測。
- 既有 zero-entity rule 與 non-empty CLP Human Gate 必須原封不動。

### 7.4 Scene plan

- 每個 unit 只接收 scoped script、course context 及 canonical CLP refs。
- Fragment 使用 global IDs／global timing 或明確 local-to-global mapping。
- merge 必須有 100% script section coverage、零重複／零遺漏／零非法 reference。
- `clp_shot_bindings` 必須在**完整 scene plan 合併後**對最終 `scene_plan` digest 重新產生或重新驗證；不可直接拼接舊 digest。
- Scoped CLP subset 只能是 prompt/context view，不得冒充既有 `clp_manifest` API input。Strict-reference provider call 仍由 root project 載入完整 digest-identical manifest/bindings，並綁定完整 bindings digest 與該 shot row digest。

### 7.5 Assets

- 每個 work item 綁定 exact scene、CLP binding、prompt、provider/model、input digests 與 output validation contract。
- 優先重用 Batch V2 已有的 immutable request、attempt、receipt、resume、single-writer publication 模式；不得假設 Batch V2 已完成真實 provider qualification。
- Unit workers／provider tools 不得直接發布 canonical `asset_manifest` 或 checkpoint。
- 全部 selected results 停止寫入後，先在 `.production-units/`／Batch staging 機械彙整非 canonical `asset_manifest` candidate；Agent 審查 exact BatchResults、candidate 與 coverage，並撰寫唯一的 Batch V2 PublicationCommand；之後才由 Batch V2 single publisher 發布 canonical `asset_manifest`／checkpoint。PUP adapter 不建立第二個 publication command 或 writer。

### 7.6 Edit

- Unit edit fragments 必須沿用 proposal 鎖定的 `renderer_family`、`render_runtime` 與 `composition_mode`。
- local timestamps 在 merge 時轉回 global absolute timestamps。
- transitions、music、narration、captions 等跨 unit 元素要由 boundary contract 明確指派 owner，防止重複或缺失。
- 完整 `edit_decisions` 必須通過 asset refs、timeline gaps/overlaps 與 duration validators。

### 7.7 Compose／render／assembly

- 只對已明確列為 supported 的 pipeline × runtime profile 啟用 per-unit render；已核准 PUP 遇到不支援的 atelier／runtime 必須 fail closed。只有 policy 原本就是 `off`，或 proposal/decision evidence 經原 Human Gate 重新核准，才可改走 monolithic compose。
- 每個 unit clip 使用同一 canonical media profile；不得在 unit 內自行改 fps、resolution、codec、audio codec、sample rate 或 loudness policy。
- `video_stitch` 先 ffprobe。完全相容才允許 stream copy；不相容則依已核准 profile 正規化／re-encode，不能假裝是無損拼接。
- 必須先解決目前 `video_stitch.py` 的 44.1 kHz 行為、舊提案的 48 kHz 假設，以及 `video-stitching.md` 對 narration/music 的 -16／-14 LUFS 差異，將規則移到一份 canonical media profile。
- Canonical profile 至少要 typed 定義 `fps`、resolution、video/audio codec、pixel format、`audio_sample_rate_hz`、channels、dialogue/music loudness 與 true peak；不得由第一支 clip 的偶然屬性決定課程母帶。
- 合併後 `render_report` 至少列出 full master；是否列出 lesson deliverables 由 course manifest 決定。

### 7.8 Publish

- Publish 不需要為了注意力而強制 unitize；它消費完整 `render_report` 與 `course_manifest`。
- 可機械式產生 chapter markers、lesson export index、captions 與 bundle manifest。
- 發布 Human Gate 與外部上傳權限維持既有規則。

## 8. Deterministic merge 與 invalidation 規則

每一種 fragment 都必須有明確、獨立測試的 merge adapter。禁止以通用 `dict.update()` 合併 creative artifacts。

共同 merge gates：

1. plan 與每個 result 的 project／stage／run identity 完全一致；
2. 所有 source、policy、course、CLP、media profile digests 仍有效；
3. unit order 完整，無遺漏、重複或多餘 result；
4. section／scene／asset／cut IDs 全域唯一；
5. source coverage 100%，順序保留；
6. timeline 無未宣告 gap／overlap，transition overlap 只出現一次；
7. 所有 cross references 可解析；
8. 完整 artifact 通過現有 schema 與 semantic validator；
9. Agent review 通過後才可 canonical publish。

Invalidation 規則：

- scoped source digest 改變：該 unit 及依賴它的下游 units stale；
- course glossary、style、CLP 或 renderer lock 改變：所有引用該 digest 的 units stale；
- unit boundary 改變：該 unit、相鄰 boundary owners 與下游 derived units stale；
- media profile 改變：所有 unit renders 與 master assembly stale；
- merge adapter／schema／protocol version 改變：舊 receipt 不可直接重用；
- 只有 exact identity + exact digest + validated output 才能 cache hit。

對已產生費用但回應不確定的 provider attempt，不自動重播；標示 ambiguous，交 Agent／使用者決定。

Unit-level checks／repairs 是 intra-stage evidence，不是正式 stage self-review。PUP policy 必須另設 bounded per-unit attempt/repair cap；所有 units 合併後仍執行一次既有正式 stage self-review，並遵守原本 reviewer/send-back 上限。不能用「unit review」重置或繞過正式 review 次數。

## 9. Telemetry 與 benchmark

Telemetry 為 append-only execution evidence，不是 canonical creative artifact。每個 event 至少記錄：

- project、run、stage、unit、attempt、protocol／schema／prompt template／model version；
- source duration、section/scene counts、input/output token estimate 或 provider 回報；
- latency、retry、repair、schema failures、terminal outcome；
- coverage、duplicate/missing refs、locked-term／CLP drift；
- boundary defect 類型；
- 粗粒度 `scene.type` 分布與連續 run；此項只能作 diagnostic，不得單獨作為
  視覺重複或品質退步的判定；
- tool/provider、成本、cache result；
- render wall time、peak memory／VRAM（能量測時）、output probe；
- resume／recovery outcome。

不得記錄 credentials。完整 prompts、使用者敏感原文與 provider payload 預設不寫入 telemetry；只保存 digest、計數與經明確允許的 redacted trace。

Concurrent workers 不得直接 append 同一個 JSONL。每個 attempt 先寫 immutable、schema-valid event records，coordinator 再以單一 writer deterministic aggregate 成 `telemetry.jsonl`。Recovery 必須能辨識 torn final line、保留已驗證 events 並拒絕偽造 sequence；啟動前另做 disk-space／retention preflight，避免一小時課程的 sidecars 無上限耗盡專案磁碟。

基準矩陣：

| Duration | 目的 |
|---:|---|
| 3 分鐘 | 確認 unit overhead 與 legacy 近似案例 |
| 8 分鐘 | 與常見單支影片比較 |
| 15 分鐘 | 與 `long-form.md` 使用範圍比較 |
| 30 分鐘 | 觀察中長內容的漂移與 aggregate cost |
| 60 分鐘 | 驗證課程能力、resume 與 render assembly |

第一輪至少比較 `off`、`auto@180s`、`auto@300s`、`auto@480s`，但不預設哪個必勝。評估指標：

- section／scene／learning-objective coverage；
- 遺漏、重複、提前揭露與跨 unit 重述；
- CLP／術語／style drift；
- schema failure、JSON truncation、repair count；
- 最大與總 input/output tokens；
- 每分鐘缺陷率與每個 boundary 缺陷率；
- render peak resource、失敗率、恢復時間與重算範圍。

Deterministic fixtures 只能證明 coverage、merge、schema、resume 與 media mechanics，不能單獨證明「Agent 注意力改善」。注意力假說另做 paired live-Agent benchmark：同一來源、凍結 prompt/model/protocol 版本、`off/180/300/480` 各至少三次 paired trials，以盲評 rubric／adjudication 報告變異。不得用一份 3600 秒 golden 來宣稱 180 秒是最佳預設。

目前已完成一個縮小範圍的 30 分鐘 `off` vs `auto@180s` paired benchmark。
它支持「在該課程、prompt、模型與 protocol 下，PUP 的資訊保留與盲評品質較佳」；
它不支持「180 秒是普遍最佳值」或「PUP 已 production-qualified」。詳細結果、
限制與 evidence digests 見
[30 分鐘 benchmark 摘要](production-unit-benchmark-30m.md)。

### 9.1 Versioned qualification profile

若日後要提出 beta／production qualification claim，M6 必須先新增一份依
實際支援輪廓校準的 versioned qualification profile，填滿量化門檻，不能留下
「可接受」「代表性」「嚴重」等未定義詞。舊的 definition-only 草稿不可直接
充當通過證據。該 profile 至少要定義：

- defect taxonomy 與 critical/major/minor 分級；critical boundary defects 容許值固定為 0；
- mechanical invariants：coverage、ID、order、timing、reference、CLP、schema 必須 100%／0 error；
- 每 unit 與整體允許的 repairs、retries、boundary drift、token growth；
- 目標 media profile 的 exact resolution、CFR/fps tolerance、codec、pixel format、stream count/disposition、sample rate、channels、`audio_required`、duration、loudness、true peak、A/V start/end sync、DTS/PTS monotonicity、full-decode 與 subtitle coverage tolerances；
- cost、wall time、peak RAM/VRAM、disk 與 retention ceilings；
- human-review rubric、paired-trial 統計與通過規則；
- PR quick gate、scheduled/manual slow gate 的 OS、最大時間／磁碟、cleanup 與 evidence retention。

Qualification report 必須綁定 Git commit、pipeline manifest digest、PUP/schema/merge-adapter versions、prompt/model/provider、renderer/FFmpeg/runtime、media-profile digest、OS 與 hardware。Schema、merge semantics、CLP rules、renderer major version、media profile、provider/model 或 prompt template 的實質變更，必須依 profile 規則做 partial 或 full requalification。

## 10. Milestones、預計修改位置與 gates

> 以下是原始最大範圍 roadmap，保留作為決策與風險紀錄，不是目前 lean
> branch 已逐項完成的聲明。實際納入 merge candidate 的能力以本文件開頭的
> 收斂說明、已追蹤程式碼、skills 與測試報告為準。

### M0 — RFC 與術語凍結（docs-only）

範圍：

- 新增 `docs/production-unit-protocol.md`；
- 重寫 `docs/course-container-architecture-v2.md`；
- 新增 `docs/course-form-rfc.md`，只凍結創作責任與輸出合約，暫不放進 skill routing；
- 新增 `docs/production-unit-qualification-profile-v1.md`，凍結缺陷分類、媒體／資源門檻、evidence binding 與 requalification 規則；
- 在原 `docs/course_container_architecture_proposal.md` 加上 superseded banner 與新文件連結，保留歷史，不原地改成另一份文件；
- 明列 `course lesson`、`long-form chapter`、`Production Unit` 的差異；
- 凍結第一個支援 profile 與 capability matrix。

Gate：

- Architecture review 確認本文件第 2 節所有 invariants；
- 無 runtime／schema／pipeline 行為改變；
- 原提案中「nested micro-project、master CLP、固定三分鐘、必然 OOM、100% 相容、3 秒拼接」等未證明主張不進入新 RFC。

Rollback：只 revert docs commit。

### M1 — Contracts、path safety 與 `mode=off`

預計新增／修改：

```text
schemas/execution/production_unit_plan.schema.json
schemas/execution/production_unit_run.schema.json
schemas/execution/production_unit_stage_state.schema.json
schemas/execution/production_unit_context.schema.json
schemas/execution/production_unit_result.schema.json
schemas/execution/production_unit_resolution.schema.json
schemas/execution/production_unit_execution_override.schema.json
schemas/execution/production_unit_resume_authorization.schema.json
schemas/execution/production_unit_adoption_receipt.schema.json
schemas/execution/production_unit_merge_command.schema.json
schemas/execution/production_unit_merge_receipt.schema.json
schemas/execution/production_unit_publication_command.schema.json
schemas/execution/production_unit_publication_receipt.schema.json
schemas/execution/production_unit_checkpoint_transition_provenance.schema.json
schemas/execution/production_unit_telemetry.schema.json
schemas/artifacts/course_manifest.schema.json
schemas/artifacts/proposal_packet.schema.json
schemas/artifacts/__init__.py
schemas/pipelines/pipeline_manifest.schema.json
lib/checkpoint.py
lib/pipeline_loader.py
lib/production_units/contracts.py
lib/production_units/identity.py
lib/production_units/workspace.py
lib/production_units/merge.py
backlot/server.py
tests/production_units/
tests/contracts/
tests/backlot/test_watch_captures.py
```

要求：

- 新欄位全部 optional/additive；舊 proposal、manifest、checkpoint 仍 valid；
- absent policy 等於 `off`；
- `off` 不建立 sidecar、不改 call graph；
- unit paths 通過 traversal、absolute path、symlink／junction、reserved canonical path 測試；
- PUP execution JSON 使用固定 UTF-8 canonical serialization 與 `sha256:<64 hex>`，有 golden vectors；不得沿用欄位名稱卻混入 Batch V2 bare digest；
- override／resume records 是 no-replace hash chain；所有新 epoch execution records、adoption receipts 與 checkpoint-transition provenance 綁定 exact `execution_epoch`／`control_chain_digest`，舊 epoch command 不可重放；
- execution sidecars 不加入 `ARTIFACT_NAMES`；`course_manifest` 才是 canonical artifact；
- checkpoint 對 `produces | optional_produces | existing supplementary-artifact rules` 做 stage ownership 驗證，並對 `content_form=course_form` 實施 typed conditional prerequisite；既有合法 supplementary checkpoints 必須有 N/N-1 regression fixture；
- M1 只讓 schemas/helpers 可被測試，不在任何 production manifest 宣告 `supported: true`，避免 stage directors 尚未具備語意時發生 silent no-op；
- `metadata.partial_progress.production_units` 使用獨立 namespace，保留其他 partial progress keys，並綁定 protocol、plan、policy、state digests；
- Backlot watcher 在 M2 前就忽略 `.production-units/` 的高頻 attempt/telemetry 寫入，只允許 checkpoint 或明確 aggregate-summary event 觸發更新；
- Python modules 不 import provider，也不做 stage／review／gate 決策。

Gate：

- 現有 full offline test suite 通過；
- deterministic legacy fixtures 的 artifact digests、stage order、gate outcomes 與 filesystem writes parity；
- 新 contracts 有 valid/invalid、unknown-field、digest tamper、duplicate ID、stale plan tests。
- immutable records 拒絕 identity reuse，mutable state 只有單一 writer 且以 atomic replace 顯示。
- active override 下 dispatch／merge／publish 全部 fail closed；只有 valid resume authorization 能建立下一個 epoch，缺鏈、分叉、重排、tamper 或 stale checkpoint/state 均拒絕。
- cross-epoch result 只有列入 resume authorization 且通過 exact adoption receipt 才能使用；只列 unit ID、缺少 dependent digest、ambiguous receipt 或 stale evidence 均拒絕。
- 每一筆 PUP checkpoint transition 的 receipt／artifact／prior-transition provenance 在 read 與 write 路徑都會驗證；手改 metadata、Human Gate evidence、receipt、transition chain 或 artifact 必須 fail closed。
- checkpoint-transition provenance 的 `pup_json_merge | batch_v2_assets | pup_render` union 必須互斥；錯 stage/artifact/status、hybrid authority、缺少 variant receipt/state 或多出另一種 publication command 都 fail closed。
- `awaiting_human → completed` fixture 證明兩筆 provenance append-only 且 hash-linked，completed 綁定原 Human Gate reply；不覆寫前一筆，也不新增 PUP approval。
- publication crash-boundary、disk-full／permission、concurrent coordinator tests 證明 canonical state 只可能是完整 old/new；否則不得在 M2 宣告 support。
- thousands-of-sidecar-writes watcher regression 不造成 thousands of SSE/refetch；普通 project watcher 行為保持 baseline。
- N/N-1 fixtures 證明新版讀取舊 checkpoints，emergency-disabled runtime 仍能安全讀取含新 optional course/PUP fields 的 checkpoints。

Stop condition：若無法在不改 existing required fields 或不繞過 checkpoint validation 下完成，停止並回 M0。

### M2 — Planning stages 的 compare-only／opt-in 路徑

現有 `script`／`scene_plan` JSON Schemas 主要驗證 shape；它們不完整保證 ID 唯一、`end > start`、排序、時間連續或 source coverage。因此 M2 必須加入 stage-specific semantic validators，不能把「schema-valid」誤當成「merge 正確」。同一原則在 M3/M4 適用於 `asset_manifest` 與 `edit_decisions`。

預計修改：

```text
skills/meta/production-unit-protocol.md
skills/pipelines/explainer/proposal-director.md
skills/pipelines/explainer/script-director.md
skills/pipelines/explainer/clp-director.md
skills/pipelines/explainer/scene-director.md
pipeline_defs/animated-explainer.yaml
lib/production_units/script_merge.py
lib/production_units/clp_merge.py
lib/production_units/scene_plan_merge.py
lib/production_units/semantic_validation.py
tests/production_units/test_script_merge.py
tests/production_units/test_clp_merge.py
tests/production_units/test_scene_plan_merge.py
tests/fixtures/production_units/
```

為了避免第一次 functional PR 同時改三個 creative stages，M2 再拆成兩個可獨立 review 的切片：

- **M2a：scene-plan vertical slice。** 只消費既有已核准的完整 script 與 canonical CLP，先證明 bounded-context plumbing、context capsule、merge、final bindings 與 checkpoint 相容；它本身不構成注意力改善證據。
- **M2b：segmented script + CLP candidates。** M2a 穩定後，再由已核准 course manifest 產生 script units、合併完整 script，並分段抽取 candidates、由 Agent 解決 course-wide CLP 衝突。

順序：

1. 先參考目前 root 中 `projects/attention-benchmark-pilot/REPORT.md` 的 433.83 秒 scene-plan pilot 重現 monolithic／segmented 比較；該 `projects/` evidence 不視為新 worktree 可取得的 source of truth，須建立經核准、可版本化且不含敏感內容的 fixture／report；
2. 增加完全 deterministic 的 3／8／15／30／60 分鐘 fixtures；
3. `execution_disposition=compare_only` 只產生 sidecars 與比較報告，不發布 canonical artifact；任何模型／付費呼叫仍需原本授權；
4. compare-only gates 通過後才允許 `publish_candidate` 的 opt-in merge 與正式 checkpoint；
5. 最終 CLP bindings 對合併後 scene plan digest 驗證；
6. M2a 通過且可獨立關閉後才開始 M2b。

只有在 M2a 同一個 reviewed change 中，meta skill、scene director、checkpoint PUP provenance 驗證與 merge tests 都存在後，`animated-explainer` manifest 才可把 `scene_plan` 標成 `supported: true`。Script／CLP capability 則等 M2b 才擴充；`course_manifest` 的 production routing 亦不可早於其 producer/consumer rules。

Gate：

- exact source coverage 100%；
- duplicate/missing IDs 與 unresolved refs 為 0；
- 最終 artifact schema failures 為 0；
- non-empty CLP fixture 的 locked reference coverage 100%；
- CLP conflict set + Agent-authored resolution map 的 permutation/retry/replay digest deterministic；
- Human Gates 與 checkpoint provenance tests 全部通過；
- unit repair 不會覆寫其他已通過 units。

Rollback：啟用 audited emergency disable，停止新 dispatch／publish；sidecars 保留供稽核。若要改走 monolithic，必須修訂 production decision 並重過原 Human Gate；已發布 canonical artifact 沿用 checkpoint history，不刪除歷史。

### M3 — Assets 與 Batch V2 接軌

範圍：

- 以 PUP unit plan 編譯 immutable asset work items；
- 重用 Batch V2 的 attempt、receipt、resume、cost reservation、single-writer publication 能力，避免再做第二套 batch engine；
- 先凍結 compatibility matrix。初始 `batch_v2_owned` route 由 Batch V2 **唯一**擁有 attempt/retry/cost/storage/publication；PUP result 只引用 exact BatchResult／work-item/publication digests，不建立第二套 asset attempt 或 publisher；
- 以向下相容的 optional provenance 讓每次 Batch PublicationCommand／PublicationState 綁定 PUP plan、selected-result、execution epoch 與 control-chain digests；PUP checkpoint-transition provenance 反向引用 exact Batch records，形成雙向可驗證 binding；
- publication 前先在非 canonical staging 彙整完整 `asset_manifest` candidate；Agent 審查 exact BatchResults/candidate 後才撰寫 Batch 唯一 PublicationCommand。`awaiting_human` 與 `completed` 的兩次 official transition 各沿用 Batch V2 對應的 command/state，後者綁定既有 Human Gate evidence；
- 加入 PUP-to-Batch adapter，而不是讓 PUP worker 直接寫正式 assets/checkpoint；不符合 matrix 的 provider/tool route 先標 unsupported；
- 先支援 fake/no-network adapters，再依 provider 逐項資格化。

預計位置：

```text
lib/production_units/assets.py
lib/batch_executor/                 # 僅在公開契約確有缺口時做 additive 修改
skills/pipelines/explainer/asset-director.md
tests/production_units/test_asset_integration.py
tests/batch_executor/
```

Gate：

- 100% required scene/asset coverage；
- 每個 asset 綁定 exact scene plan + CLP binding digests；
- dispatch authorization 必須包含既有 TTS/image/music/reference sample approval evidence；sample gate 未通過前不可擴張剩餘付費 units，PUP 不新增或替代 Human Gate；
- crash、429、5xx、malformed response、truncated JSON、corrupt media、ambiguous charged attempt 測試；
- resume 只重做 stale/failed units；
- canonical publication 單一 writer，且只在 execution 停止與 Agent review 後發生；`batch_v2_assets` checkpoint 不得存在 PUP publication command/receipt；
- tamper 任一側的 PUP↔Batch digest binding、使用錯誤 epoch 或混入 hybrid checkpoint-transition provenance 都必須 fail closed；
- 未取得外部測試授權時只可稱 offline code-complete，不得稱 production-qualified。

### M4 — Edit、per-unit render 與 master assembly

預計位置：

```text
lib/production_units/edit_merge.py
lib/production_units/render.py
skills/pipelines/explainer/edit-director.md
skills/pipelines/explainer/compose-director.md
tools/video/video_stitch.py
schemas/tools/video_stitch.schema.json
lib/media_profiles.py
schemas/artifacts/final_review.schema.json
tools/analysis/composition_validator.py
tools/video/video_compose.py
tools/video/hyperframes_compose.py
pipeline_defs/animated-explainer.yaml
tests/production_units/test_edit_merge.py
tests/production_units/test_render_resume.py
tests/qa/test_06_video_stitch.py
```

Gate：

- global timeline coverage 完整；
- 所有 cuts、overlays、narration、music、subtitles refs 有效；
- runtime／composition mode 不會 silent swap；
- 每個 unit clip 與 master 都通過 ffprobe、duration、fps、codec、audio sample rate、A/V sync 檢查；
- slow release gate 對每個 unit output 與 assembled master 做完整 decode-to-null scan；decode error、non-monotonic DTS/PTS、unexpected stream count/disposition 或 concat duration mismatch 一律 hard fail，不能只靠 metadata probe／稀疏抽幀；
- canonical profile 明定 `audio_required`／intentional silence；required audio 缺失、ffprobe 失敗、profile mismatch、duration 或 A/V sync 超過 qualification-profile tolerance 都是 hard failure，不可只記 warning 後仍回傳 `pass`；
- 每一 unit 內取樣、每一 boundary 兩側取樣、整體規律取樣，而不是全片只檢查 4 frames；
- PUP review 以 optional typed unit/boundary evidence 擴充 `final_review`，但一般影片仍可使用既有 schema；
- 不可直接相信目前 composition validator 已檢查 gap／overlap／order，必須先補 regression tests 與真正的 semantic validation；
- 既有 HyperFrames 約 1800 秒 fixed timeout、Remotion `max(600, scene_count*15)` 與 animated-explainer `orchestration.max_wall_time_minutes: 20` 必須改為 unit-aware、可恢復且可觀測的政策；不能用增加一個 60 分鐘總 timeout 取代切片；
- 斷點故障只重 render 必要 unit，master assembly 可重入；
- Agent-authored render publication command 綁定 master digest／target／review evidence；正式 `renders/`、`render_report` 與 terminal checkpoint 通過 no-replace、checkpoint-last、crash-recovery tests；
- render checkpoint transitions 只能使用 `pup_render` provenance 與其 publication receipt；不得引用 Batch asset publication state 充當 render authority；
- media profile 不符時明確 re-encode 並記錄，符合時才使用 stream copy。

### M5 — Course projection、Backlot 與 delivery

預計位置：

```text
backlot/state.py
backlot/server.py                 # 僅在現有 state endpoint 不足時
backlot/ui/                       # 先最小投影，完整 Studio UI 非本 milestone
skills/creative/course-form.md
skills/pipelines/explainer/publish-director.md
skills/INDEX.md
docs/ARCHITECTURE.md
tests/backlot/
tests/contracts/test_backlot_contract.py
```

此時才把已核准的 `course-form` RFC 發布為可路由 creative skill，並在 skill 中只描述課程設計；所有 attention、檔案與 resume 規則只引用 PUP，不複製一套協定。

Backlot 最小能力：

- 從已驗證 proposal checkpoint 的 `course_manifest` 判斷 `is_course`；
- 顯示 module／lesson outline、整體 stage、unit completed/failed/stale counts；
- 顯示目前 active unit 與 boundary defect／repair 摘要；
- canonical artifact 與 checkpoint invalid 時 fail closed／degraded，不以 sidecar 掩蓋；
- `course_manifest` 必須直接以 proposal checkpoint 為 authority；loose cache 不得覆蓋；
- 不遞迴掃描 nested projects，不寫 unit state。

Gate：

- 普通 project 卡片與 API response parity；
- malformed／stale／tampered course/PUP sidecar 不使 board crash，也不提升狀態；
- `.production-units/` 的每次 attempt/telemetry 寫入不得觸發全 board SSE/refetch；只有聚合後的 checkpoint progress 或明確 PUP summary event 可更新 UI；
- `board.js` 不再把所有 partial progress 假設成 `completed_scene_ids`；namespaced `production_units.completed_unit_ids/total_units` 有獨立、向下相容的 projection tests；
- course outline 與 checkpoint-derived progress 不互相覆寫；
- full master、lesson exports、chapters、captions 的 delivery manifest 可追溯到 render report。

### M6 — 60 分鐘 qualification 與 rollout

M6.0A 的 contract closure、consumer-review follow-up、測試快照、能力宣稱邊界與給
Backlot／GPT B 的 interface handoff 記錄於
`docs/production-unit-m6-qualification.md`。該狀態不等於 beta 或
production qualification。

離線 code-complete gate：

- 一個 3600 秒 deterministic golden course；
- 3／8／15／30／60 benchmark matrix；
- Windows 與 Linux CI；
- no-network／no-credential guard；
- fault injection 與 rollback rehearsal；
- `mode=off` full regression；
- 產出版本化 evidence report。

3600 秒 JSON／timeline golden 可進一般離線 gate；3600 秒實體媒體 assembly 應使用低複雜度 synthetic clips 並放在明確的 slow offline gate，避免讓每次 quick test 都渲染一小時影片。

- **PR quick gate**：contracts、property tests、3600 秒 JSON/timeline fixture、短 synthetic media、mode-off parity；
- **scheduled/manual slow release gate**：由多個有序 units 與 boundary transitions 組成的 3600 秒 synthetic media，不可只 loop 一支 clip；在 qualification profile 指定的 Windows/Linux runners 各通過一次完整 decode-to-null／DTS-PTS／stream integrity gate，遵守其 time/disk cap、成功與失敗 cleanup、evidence retention；
- profile tag／beta evidence 不得缺少 slow gate；日常 quick CI 則不必每次編碼一小時母帶。

經使用者另行核准的 beta gate：

- 一個明確 pipeline × runtime × provider profile 的真實 60 分鐘 E2E；
- 從 course design、script、CLP、scene plan、assets、edit、unit renders 到 master/publish artifact；
- paired live-Agent benchmark 依 qualification profile 通過，才可使用「注意力保持／改善」的產品或架構宣稱；未通過時仍只能稱 bounded execution/merge capability；
- 記錄實際 tokens、cost、repair、boundary defects、peak resources 與 resume evidence。

Production qualification gate：

- 至少三門覆蓋 qualification profile 所定內容／視覺／CLP 複雜度矩陣的真實 40～60 分鐘課程；
- 至少一次執行中 crash／resume 與一次 stale-unit 局部重建；
- 無 critical boundary defect、無 provenance bypass、無未解決 schema/reference failure；
- 使用者接受品質與成本報告。

M6 通過前，PUP 保持 opt-in；即使 code 已 merge，也不得在文件中寫成所有 OM pipeline 的普遍保證。

## 11. 測試分層

### Contract tests

- schema valid/invalid；
- version、unknown fields、identity、digest tamper；
- path containment 與 reserved paths；
- manifest optional fields 的向下相容；
- checkpoint artifact ownership／Human Gate／CLP provenance。
- approved `auto/fixed` → emergency-disabled 的 pre-stage、mid-stage、post-publication transitions；不得修改 proposal、不得自動 monolithic fallback、不得重送 ambiguous attempt。
- override/resume hash-chain 的 sequence、fork、tamper、stale-state、stale-epoch replay tests；resume authorization 只能增加 epoch，不能恢復被 policy 禁止的能力。
- exact cross-epoch adoption 的 valid/invalid cases；未列 digest、只列 unit ID、dependency drift、ambiguous receipt 或 adoption tamper 都 fail closed。
- checkpoint-transition provenance union 的三個 valid variants，以及 wrong-stage/status、hybrid、missing/extra authority record invalid cases。
- `awaiting_human → completed` 的 append-only transition chain、原 Human Gate evidence binding 與 Batch two-command fixture；不得產生第二套 PUP approval。

### Merge/property tests

- 隨機 section/scene partitions 後 merge 等於 canonical ordered model；
- 邊界第一／最後 unit、單一超大語意單元、零長度／重疊／缺口；
- duplicate IDs、out-of-order results、stale contexts；
- local/global timing round trip；
- deterministic digest 與 merge repeatability。

### Agent-instruction tests

- `course-form` 不宣稱 pipeline 限制；
- `long-form` 不被改寫成 PUP 規格；
- stage directors 在 `off` 時遵循原流程；
- Agent 仍執行 review／Human Gate，Python 不做創意裁決；
- unsupported pipeline/runtime fail closed。

### Backlot tests

- observer-only；
- canonical authority 優先；
- partial/stale/corrupt sidecar 降級顯示；
- 普通 project 無 course 欄位或有向下相容 default；
- 大型 artifacts 不使 library summary 必須全部反序列化。

### Media tests

- homogeneous stream-copy；
- heterogeneous normalize/re-encode；
- silent/audio clips；
- CFR、sample rate、channel layout、loudness、subtitle boundary；
- corrupt clip、missing clip、mid-assembly crash、re-entry；
- duration formula 含 transitions。

## 12. Branch、worktree、commit 與 merge 策略

### 決策

**要建立分支，而且要使用獨立 worktree。** 目前根 worktree 在 `team-main` 上已有使用者修改與多個 untracked projects/docs；直接 checkout 或 `git add .` 都有把無關內容帶入的風險。

本計畫核准後：

1. 先明定 integration authority。依目前 remote 配置建議使用 `team-fork/team-main`；若使用者選擇其他目標，必須先記錄。經授權後只 fetch 指定 remote，不在 dirty root 執行 pull；
2. 凍結 exact base SHA。若核准後 base 改變，先重做 compatibility review，不自動 rebase／merge；
3. 由單一機制建立獨立 worktree 與 branch，避免 Codex app 與 shell 同時建立。預期名稱為 `codex/pup-contracts`；若 app 指派不同名稱，記錄實際 branch/path/SHA；
4. 驗證新 worktree `HEAD == frozen_base_sha`、branch 正確且 status clean；
5. 精確匯入已核准的本 plan，第一個 commit 必須是 plan-only commit，記錄 commit SHA 與 file digest；之後才啟動新的 implementation task；
6. 第一個 implementation task 只執行 M0/M1；
7. 後續 milestones 各自從已合併基準建立短分支，例如：

   ```text
   codex/pup-planning-stages
   codex/pup-assets
   codex/pup-render-assembly
   codex/pup-course-backlot
   codex/pup-qualification
   ```

8. 每個 commit 與 PR 對齊一個可獨立驗收／revert 的邊界；
9. staging 只列明確檔案，merge 前檢查 staged paths，禁止 `git add .`；
10. 每一 PR 都維持 default-off 或尚未接上 legacy routing；
11. CI、獨立 review、rollback rehearsal 與使用者核准後才 merge；
12. 使用可辨識的 reviewed no-ff merge commit，以 `git revert -m 1 <merge-commit>` 保留整體回滾點，不使用 destructive reset。

目前 `docs/course_container_architecture_proposal.md` 與 `docs/studio_draft.md` 也是未追蹤的使用者檔案。新 worktree 不會自動包含它們；若 M0 要納入原提案，只能在使用者核准後精確複製／stage 指定文件，不得順手納入其他 dirty content。

Candidate merge 不得在目前 `D:\kj-openMontage` dirty root worktree 執行。優先使用 reviewed PR merge；若需本機整合驗證，另建 clean temporary integration worktree。Remote merge 後，dirty root 是否同步是另一個保存／整合決策，不自動 pull、checkout、merge 或 reset。

不建議把 M0～M6 放進一個長期 mega branch 再一次 merge。Contracts、planning stages、paid assets、render 及 Backlot 的風險不同，應分批縮小 blast radius。

## 13. 新 Codex task／Agent 執行策略

**建議在本 plan 核准後開新的 Codex task，但第一個 task 只負責 M0/M1。** 理由是取得乾淨 worktree、清楚的 scope／authority 與可稽核 handoff，不是依賴「換一個 Agent 就會自動更正確」。

Handoff 必須包含：

- repository-relative plan path、approved plan commit SHA 與 file digest；
- base commit、branch、worktree；
- 僅限當前 milestone 的 scope 與 non-goals；
- 第 2 節 invariants；
- 預計修改檔案與 acceptance commands；
- 禁止付費 provider、deployment、GCS mutation 與自行 merge；
- 完成條件是 **merge-ready review**，不是直接 merge。

新 task 在修改任何檔案前必須通過 startup gate：plan commit/digest 相符、exact base SHA、integration remote/target 已明定、worktree clean、branch 正確、allowed-path list 完整，以及禁止自行 merge／付費呼叫的 authority 已確認。任一條不符即停止，不憑記憶重建 plan。

執行 ownership：

- 一位 primary Agent 是唯一主要程式碼 writer；
- 子 Agents 可平行做 contracts、compatibility、security、tests 的 read-only review；
- 涉及同一核心檔案時不讓多位 Agent 同時修改；
- 每個 milestone 結束即停下，提交 evidence 給使用者決定是否進下一階段。

## 14. Rollback 與 coexistence

1. Audited emergency disable override 是已核准 PUP 專案的第一層 operational rollback；它停止新 dispatch／publish，但不竄改 proposal policy。原本就核准 `mode=off` 的專案維持 legacy path。Backlot／稽核工具可 read-only 顯示保留 evidence，但不得改變 normal project lifecycle／authority。
2. PUP sidecars 不刪除，保留 audit／resume evidence；它們不影響 legacy pipeline。
3. 每個 reviewed no-ff functional milestone merge 以 `git revert -m 1 <merge-commit>` 回復，不 rewrite shared history；已有相依 milestone 時必須由最新依賴開始逆序 revert。
4. Canonical publish 前失敗時，checkpoint 保持 `in_progress`／`failed` 並引用 run summary；不發布半成品。
5. Canonical publish 後若需重做，沿用 checkpoint history，不覆寫或偽造舊 approval。
6. PUP 是新增能力，沒有 legacy retirement 需求；在多個 profiles 真正 qualification 前，monolithic path 必須持續存在。
7. 一旦任何 project 已發布 `course_manifest`、PUP proposal fields 或 PUP checkpoint-transition provenance，M1 additive reader/schema/validator 就成為 compatibility floor，不能直接 revert 成無法讀取新 checkpoint 的版本。完全降級必須先有受測試的 migration；日常 rollback 只停用／逆序 revert M2+ 功能。
8. M1 必須保存 N/N-1 read/resume fixtures：新版可讀舊專案；停用後仍可讀含新 optional fields 的專案。任何 schema removal 或 required-field 變更都需另立 migration RFC。
9. 每新增一個 supported artifact boundary，都要驗證兩種 continuation：中途 disable → 保留 evidence → 經原 Human Gate 重新核准 monolithic → 不讀 sidecars 重跑本 stage；以及 PUP terminal checkpoint 已發布 → 重新核准 monolithic → legacy next-stage director 只消費 canonical artifact 正常前進。Scene plan、assets、edit、compose 至少各有 fixture，否則只能稱 safe stop，不能稱可回復 coexistence。

## 15. Definition of Done

### M0/M1 可合併

- [ ] RFC、course-form、Course Container V2 的責任沒有重疊。
- [ ] PUP contracts 與 path safety tests 完整。
- [ ] `mode=off` filesystem／artifact／gate parity 完整。
- [ ] Mandatory focused suites 全綠；full suite 與 CI 不得比 frozen baseline 新增 failure。若 baseline 原已有 failure，須逐項記錄而不可歸因於本變更。
- [ ] 無 provider call、無 deployment、無 Backlot authority 變更。

### PUP code-complete

- [ ] Script、CLP、scene plan、assets、edit、compose 的 supported profile 全部有 deterministic unit/merge adapters。
- [ ] 完整 canonical artifacts 與 checkpoints schema-valid。
- [ ] CLP chain、Human Gates、renderer lock 與 single-writer publication 未被繞過。
- [ ] 3600 秒 golden fixture、fault injection、resume、legacy parity 通過。
- [ ] Backlot 可讀 course／unit progress 且 observer-only。
- [ ] Migration／rollback rehearsal 與 evidence 文件完成。
- [ ] 每個 supported boundary 的 emergency-disable + reapproved monolithic continuation 通過。

### 一個 profile 可稱 beta-qualified

- [ ] 使用者明確核准外部 provider／成本／runtime。
- [ ] 真實 60 分鐘課程 E2E 完成。
- [ ] Paired live-Agent benchmark 達到綁定 qualification profile；否則不宣稱注意力改善。
- [ ] Coverage、CLP、boundary、media、cost、resource、resume telemetry 全部符合綁定版本的 qualification profile。
- [ ] 所有 critical defects 為 0。

### 一個 profile 可稱 production-qualified

- [ ] 三門覆蓋 qualification profile 取樣矩陣的真實課程完成。
- [ ] 故障恢復與局部重建實證完成。
- [ ] 品質／成本門檻與預設 unit size 有足夠資料支持。
- [ ] 使用者核准 rollout；PUP 仍可 per-project 關閉。

## 16. 本輪明確不做

- 不在目前 dirty `team-main` worktree 修改 OM core。
- 不建立 nested chapter projects，也不新增 `resolve_chapter_dir()`。
- 不建立 `master_clp.json`。
- 不把 180 秒定為 core invariant。
- 不全面改寫 `long-form.md`；最多在後續加上與 `course-form`／PUP 的責任說明。
- 不同時開發完整 Studio UI。
- 不在未授權下執行付費媒體生成、Cloud Run、GCS、deployment 或 merge。
- 不承諾 `<150 lines`、`1～2 days`、固定 `3 秒` 拼接或未經測試的 `100% compatibility`。

## 17. 建議的第一個執行切片

使用者核准本計畫後，只啟動以下工作：

1. 凍結 integration authority 與 exact base SHA；
2. 建立乾淨 worktree／branch，精確匯入核准 plan 並建立 plan-only commit；
3. 開新的 implementation task，先執行 startup gate；
4. 完成 M0 文件與術語凍結；
5. 完成 M1 execution schemas、course manifest、optional policy、path safety 與 `mode=off` parity；
6. 跑 mandatory focused suites、完整離線 regression 與獨立 review；
7. 停在 merge-ready 狀態，提交 diff、測試、風險與 rollback 摘要；
8. 由使用者決定是否 merge，再另開 M2 task。

這個切片刻意不進行模型生成、assets、render 或 Backlot UI 修改，先證明擴充點能在不破壞 OM 原設計的前提下存在。
