# GPT B Closure Re-review Handoff — Production Unit Protocol M6.0B

> 用途：供 GPT B 對 Track A 的 M6.0B producer-side consumer-boundary
> follow-up 進行封閉式 re-review。
>
> 本文件是 review handoff，不是資格宣告，也不是 merge／push 核准。M6.0B candidate 仍維持 review-ready、未 merge、未 push。

## 1. 請 GPT B 執行的任務

請以 consumer／Backlot 整合者視角，review 下列 bounded M6.0B follow-up：

- exact base：`df0f8ca616fceac056c8762a9b59193a2e822873`
- initial candidate：`77d286c9615b6997c6d9447ca1baf4fbb7fa8d71`
- follow-up candidate：本文件所在的 `HEAD`；exact SHA 由 GPT A 的交付訊息提供
- branch：`codex/pup-m6-handoff`
- isolated worktree：`D:\kj-openMontage\.pytest-tmp\pup-m6b`

建議先執行：

```powershell
git -C D:\kj-openMontage\.pytest-tmp\pup-m6b status --short --branch
git -C D:\kj-openMontage\.pytest-tmp\pup-m6b show --stat --oneline HEAD
git -C D:\kj-openMontage\.pytest-tmp\pup-m6b diff 77d286c..HEAD
git -C D:\kj-openMontage\.pytest-tmp\pup-m6b diff df0f8ca..HEAD
```

請判斷：

1. 是否存在 blocking finding。
2. 下列三項原 blocking findings 是否已完整封閉：stage artifact authority、Human Gate provenance、同 project/stage 寫入原子性。
3. Backlot consumer 可以安全依賴的介面是否明確，且沒有把 producer assertion 誤認為已驗證事實。
4. 如有問題，請依 blocking／P1／P2 分級，附檔案、行號、失敗情境及最小修正建議。
5. 最後提供明確 verdict：可合併、需 follow-up 後合併，或不可合併。

Review 階段請不要 merge、push、開始 M6.0C，或修改 Backlot-owned 檔案。

### 此次 consumer review findings 的處理

1. Stage authority：candidate artifacts 現在必須落在該 manifest stage 的
   `produces | optional_produces` allowlist；foreign-stage artifact 在 sidecar
   persistence 前即拒絕，durable chain 讀取時也會重新驗證。
2. Human Gate：`completed/human_approved=true` 必須從相符、已持久化的
   `awaiting_human` checkpoint 與 receipt 轉換；artifacts 與
   `candidate_handoff` 必須完全保留，混入 Batch V2／render authority 會拒絕。
3. Concurrency：既有 checkpoint writer 對每個 project/stage 使用同一 OS lock；
   PUP 在 revalidate source/target 到 checkpoint write/receipt 的整段期間，依固定
   順序持有所有 frozen predecessor 與 target stage locks。這不是 CAS 或新的
   multi-writer coordinator。

## 2. M6.0B 範圍與非目標

本 commit 只建立最小、canonical 的 JSON candidate handoff 與 recovery seam，適用於：

- `script`
- `clp`
- `scene_plan`
- `edit`

本 commit 明確沒有：

- 將 PUP 改為預設啟用、beta 或 production-qualified；
- 呼叫 provider、網路或付費服務；
- 執行真實媒體或 60 分鐘 E2E；
- 建立第二套 Human approval、publisher 或 pipeline state machine；
- 修改 Backlot、Batch V2 publisher 或既有 required checkpoint fields；
- 實作 M6.0C、M6.1、M6.2 或 M6.3。

PUP 仍是 experimental／opt-in。

## 3. Canonical handoff 路徑

```text
director candidate（non-canonical sidecar）
  → immutable plan / candidate records
  → explicit stage review receipt（不是 Human approval）
  → registered canonical artifact validators
  → immutable checkpoint intent
  → existing lib.checkpoint.write_checkpoint
  → original Human Gate
```

核心不變量：

1. candidate 在既有 checkpoint writer 接受以前始終是 non-canonical。
2. 只有 `lib.checkpoint.write_checkpoint` 能建立正式 checkpoint。
3. stage review receipt 不等於 Human Gate approval。
4. gated stage 首次寫入只能是 `awaiting_human`、`human_approved=false`。
5. 只有既有 Human Gate transition 能將其轉成 `completed`、`human_approved=true`。

## 4. Durable coordinator／receipt 模型

每個 handoff 的 producer-side records 位於：

```text
.production-units/handoffs/<handoff_id>/
  plan.json
  candidate.json
  review.json
  validation.json
  checkpoint-intent.json
  checkpoint-receipt.json
  state.json
  <lock file>
```

設計原則：

- `plan.json` 到 `checkpoint-receipt.json` 是以 atomic no-replace 方式建立的 immutable records。
- `state.json` 是可修復、非權威的 digest projection；它不是新的 approval 或 pipeline state machine。
- OS-level lock 保證同一 handoff 同一時間只有一個 coordinator。
- Canonical commit 另以 project/stage lock set 序列化 frozen source/target
  revalidation、既有 checkpoint writer 與 receipt；不同 handoff IDs 不能同時
  通過同一 target 的 stale check。
- restart 以 immutable records、正式 checkpoint 與 digest binding 判定下一步，不相信單獨的 `state.json`。

## 5. Identity、epoch 與 control-chain binding

Handoff 明確綁定：

- project、run、pipeline、stage；
- validated approved proposal checkpoint；
- approved PUP policy digest；
- plan、candidate、review、validation、intent、receipt digests；
- 當下所有已完成的 predecessor checkpoints；
- 寫入前的 target checkpoint 狀態；
- execution epoch；
- caller 提供的 control-chain identity 與 digest。

Approved policy mode 的唯一可信來源仍是 validated、completed、human-approved proposal checkpoint：

```text
proposal_packet.production_plan.production_unit_policy.mode
```

Policy 缺席或 `off` 時，canonical API 在建立 `.production-units` 前即回傳 no-op。Deprecated legacy alias 不得啟用 canonical handoff。

目前只驗證 control-chain identity／digest 與 frozen plan 完全一致；完整 control-chain trust verifier 尚未在 M6.0B 建立。

## 6. Authority 分離

### 6.1 JSON artifacts

本階段只有 `pup_json_merge` 可處理上述四個 JSON stages。正式 authority 仍由既有 checkpoint writer 與 stage artifact validator 決定。每個 candidate 只能帶入 owning manifest stage 的 `produces | optional_produces`；例如 `script` 不得攜帶 `asset_manifest`。

### 6.2 Assets／Batch V2

`assets` 會以 `BATCH_V2_AUTHORITY_REQUIRED` fail closed。Batch V2 繼續是 `PublicationCommand`／`PublicationState` 的唯一 publication authority；PUP 不建立平行 publisher。

### 6.3 Render／compose

`compose` 會以 `RENDER_AUTHORITY_NOT_QUALIFIED` fail closed。Physical render publication 與 media recovery 明確 deferred 至 M6.0C。

### 6.4 Hybrid provenance

Checkpoint metadata 若同時混用 `production_units`、`batch_v2_publication` 或 `pup_render_publication` authority，會被拒絕，避免 JSON 與 physical media 形成 hybrid provenance。

## 7. Checkpoint provenance contract

新增 optional metadata：

```text
metadata.production_units.candidate_handoff
```

其 schema 為：

```text
schemas/execution/production_unit_checkpoint_provenance.schema.json
```

最小欄位包括：

- `version`
- `authority`
- `handoff_id`
- `run_id`
- `execution_epoch`
- `control_chain`
- `policy_checkpoint_sha256`
- `policy_sha256`
- `plan_record_sha256`
- `candidate_record_sha256`
- `candidate_sha256`
- `review_record_sha256`
- `validation_record_sha256`
- `checkpoint_intent_sha256`

`lib.checkpoint.validate_checkpoint` 會在正式 write 與後續 read 時驗證這個 optional provenance。舊 checkpoint 沒有此 metadata 時，沿用原路徑，不增加 required field。

Consumer 必須區分：

- provenance metadata 證明「這個正式 checkpoint 綁定哪一組 candidate handoff records」；
- checkpoint 本身的 `status` 與 `human_approved` 才是 canonical stage／Human Gate 狀態；
- approved PUP policy 仍只能從 proposal checkpoint 取得；
- qualification status 仍須由後續 trusted profile／resolver 決定。

Consumer 不應直接讀取 sidecar records 或 `state.json` 來推斷 approval、publication 或 qualification。

Human Gate transition 另有 write-time guard：必須先讀回相符的 durable
`awaiting_human` checkpoint／receipt，然後原樣保留 candidate artifacts 與
provenance。只有 intent、移除 provenance、替換 artifacts 或增加另一種
publication authority 都不能形成合法 completed checkpoint。

## 8. Crash、restart 與 idempotency

### 8.1 Writer 前 crash

若已存在 frozen checkpoint intent、但正式 writer 尚未成功，restart 只能驗證並重用同一份 intent；任何 policy、plan、candidate、review、validation、epoch 或 target checkpoint drift 都會 fail closed。

### 8.2 Writer 後、receipt 前 crash

Restart 先讀取並驗證正式 checkpoint：若其內容與 frozen intent 完全相符，補寫缺少的 receipt／state，不重寫 checkpoint。

### 8.3 Retry 與 concurrency

- 相同輸入的 retry 是 idempotent。
- concurrent coordinator 由 handoff lock 拒絕。
- 合法但落後的 `state.json` 可由 immutable records 修復。
- tampered 或超前的 `state.json` 會 fail closed。

### 8.4 Charged attempt

若 caller 表示存在 ambiguous charged attempt，handoff 在任何 candidate record 持久化或 provider dispatch 前即拒絕；M6.0B 不會自動重送或採用結果。

## 9. Fail-closed 行為

測試涵蓋下列拒絕情境：

- stale／tampered policy；
- stale plan 或 predecessor／target checkpoint；
- tampered candidate、review receipt、validation、intent 或 receipt；
- authority mismatch；
- execution epoch mismatch／cross-epoch replay；
- control-chain mismatch；
- 非法 adoption fields；
- ambiguous charged attempt；
- concurrent coordinator；
- Human Gate bypass；
- JSON／media hybrid provenance。

M6.0B 沒有合法的 cross-epoch adoption path；restart 必須使用原 execution epoch。需要跨 epoch 接管時必須等待後續 milestone 定義明確授權契約。

## 10. Backlot consumer interface handoff

GPT B／Backlot 現在可以安全依賴：

1. 經 `lib.checkpoint` 正式 reader 驗證通過的 optional `metadata.production_units.candidate_handoff` shape。
2. `authority="pup_json_merge"` 只代表 producer-side JSON candidate handoff authority。
3. checkpoint `status`／`human_approved` 保持原有語意，沒有被 stage review receipt 取代。
4. provenance 中的 identity／digest 用來顯示或關聯 handoff；不能用來自行提升 approval 或 qualification。
5. 沒有 PUP metadata 的 ordinary／legacy checkpoint 繼續按原規則處理。

GPT B／Backlot 目前仍不可依賴：

- 直接讀取 `.production-units/handoffs/**`；
- 把 `state.json` 當 canonical coordinator 或 pipeline state；
- 由 sidecar 判定 Human approval、publication 或 stage completion；
- assets／render 的 PUP publication；
- cross-epoch adoption 或 recovery authorization；
- control-chain digest 已具備外部信任根；
- live profile／matrix discovery 或 effective qualification；
- producer-authored qualification assertion 等同於已驗證證據；
- Backlot aggregate progress 已完成整合。

若 Backlot 要投影 PUP handoff，應只從經正式 checkpoint reader 驗證後的 optional provenance 讀取，且 absence 必須是正常、向下相容的狀態。

## 11. Follow-up 修改檔案

相對 initial candidate `77d286c`，follow-up 修改／新增：

```text
docs/production-unit-protocol-implementation-plan.md
docs/production-unit-m6-qualification.md
docs/production-unit-m6-0b-gpt-b-review-handoff.md
lib/checkpoint.py
lib/production_units/handoff.py
skills/meta/production-unit-protocol.md
tests/production_units/test_handoff.py
```

沒有修改：

```text
backlot/
backlot/ui/
tests/backlot/
```

## 12. 已完成測試

### 12.1 Focused handoff tests

```powershell
python -m pytest tests/production_units/test_handoff.py -q --basetemp D:\kj-openMontage\.pytest-tmp\m6b-followup-focused-final
```

結果：`37 passed in 52.08s`

### 12.2 Full Production Unit suite

```powershell
python -m pytest tests/production_units -q --basetemp D:\kj-openMontage\.pytest-tmp\m6b-followup-pu
```

結果：`147 passed in 64.76s`

### 12.3 Batch V2 publication／release regressions

```powershell
python -m pytest tests/batch_executor/test_m2_publication.py tests/batch_executor/test_m4_release_gate.py -q --basetemp D:\kj-openMontage\.pytest-tmp\m6b-followup-batch
```

結果：`81 passed, 2 skipped in 24.07s`

### 12.4 Checkpoint、course-routing 與 Backlot projection regressions

```powershell
python -m pytest tests/contracts/test_checkpoint_read_gate.py tests/lib/test_checkpoint_prerequisites.py tests/lib/test_checkpoint_noncanonical_stage.py tests/production_units/test_course_routing.py tests/backlot/test_course_projection.py tests/contracts/test_pipeline_catalog.py tests/contracts/test_backlot_contract.py -q --basetemp D:\kj-openMontage\.pytest-tmp\m6b-followup-reg
```

結果：`103 passed in 4.97s`

### 12.5 Backlot Human Gate regression

```powershell
python -m pytest tests/backlot/test_gate_scenarios.py -q --basetemp D:\kj-openMontage\.pytest-tmp\m6b-followup-gates
```

結果：`4 passed in 1.44s`

### 12.6 Static checks

```powershell
python -m ruff check lib/checkpoint.py lib/production_units/__init__.py lib/production_units/handoff.py tests/production_units/test_handoff.py
python -m py_compile lib/checkpoint.py lib/production_units/__init__.py lib/production_units/handoff.py tests/production_units/test_handoff.py
git diff --check 77d286c9615b6997c6d9447ca1baf4fbb7fa8d71..HEAD
```

結果：Ruff、`py_compile` 與 `git diff --check` 全部通過。

## 13. Backward compatibility

- 沒有新增 required checkpoint fields。
- 沒有改變既有 Human Gate transition 語意。
- Human Gate writer 現在只接受 exact PUP `awaiting_human` → `completed`
  transition；ordinary／legacy checkpoints 沒有 PUP provenance 時仍走原路徑。
- 沒有改變 Batch V2 publication authority。
- ordinary project、policy `off` 與舊 checkpoint 不建立 handoff sidecar，沿用原行為。
- 新 checkpoint provenance 是 optional 且只在存在時驗證。
- 沒有修改 Backlot-owned code 或 tests。

## 14. 明確 deferred 項目

| 項目 | Owner／milestone | M6.0B 的 capability claim |
|---|---|---|
| Physical render publication、media receipt 與 recovery | Track A／M6.0C | 不支援；`compose` fail closed |
| Cross-epoch adoption／resume authorization | 後續 recovery milestone | 不支援；cross-epoch replay 一律拒絕 |
| 完整 control-chain trust verifier／trust root | 後續 security／qualification milestone | 只做 caller-supplied identity／digest exact binding |
| Live profile／matrix discovery、resolver 與 trust root | Track A／M6.1 | 不宣稱 effective qualification |
| Backlot aggregate progress／UI integration | Track B，待 producer contract review 後另案 | 本 commit 僅提供 optional checkpoint provenance |
| Provider-backed 60 分鐘 E2E | Track A／M6.2 | 未執行，不得聲稱 production-qualified |
| Rollout／default enablement | Track A／M6.3 | PUP 維持 experimental／opt-in |

## 15. 剩餘風險

1. control-chain digest 已被精確綁定，但尚未建立外部 trust chain；caller 若本身不可信，digest 不能自行提供信任。
2. M6.0B 刻意不提供 cross-epoch adoption；長時間中斷後若必須換 epoch，目前只能 fail closed。
3. 尚未驗證 physical media、真實 provider 或 60 分鐘 E2E。
4. producer-side restart 需要 durable handoff records；consumer 不應自行依賴這些 sidecars。
5. Optional checkpoint provenance 可證明正式 checkpoint 與 handoff records 的綁定，但不等於 qualification evidence authenticity。
6. Project/stage locks 是本機 OS lock；本 slice 不宣稱跨主機、網路檔案系統或分散式 multi-writer safety。

## 16. 建議 GPT B 的 focused review checklist

- [ ] Policy activation 是否只能來自 approved proposal checkpoint。
- [ ] Candidate 是否在 existing writer 接受前保持 non-canonical。
- [ ] `state.json` 是否確實只是可修復 projection，而非第二套 state machine。
- [ ] Original Human Gate 是否完全不能被 stage review receipt 繞過。
- [ ] Batch V2 publication authority 是否保持唯一且未被 PUP metadata 混淆。
- [ ] Crash-after-write-before-receipt 是否只補 receipt，而不重寫 checkpoint。
- [ ] Stale、tampered、cross-epoch、ambiguous evidence 是否全部 fail closed。
- [ ] Optional provenance 的 read-time validation 是否不影響舊 checkpoint。
- [ ] Backlot 是否能只靠正式 checkpoint reader 取得安全、有限的 projection input。
- [ ] 文件 capability claims 是否與實作一致，沒有提前宣稱 M6.0C／M6.1／M6.2 已完成。

## 17. 預期 review 輸出格式

請 GPT B 回覆：

```text
Verdict:
- blocking finding: yes / no
- recommendation: merge / follow-up then merge / reject

Findings:
- [severity] file:line — issue, impact, minimal fix

Consumer interface:
- safe to rely on:
- still forbidden / deferred:

Regression assessment:
- checkpoint / Human Gate:
- Batch V2 authority:
- Backlot compatibility:

Remaining risks:
- ...
```

Review 完成後請停止，將 verdict 交回 GPT A／使用者；除非另有明確核准，不要 merge 或 push。
