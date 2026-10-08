# kj lean 分支：現況與交接

> 給接手的 agent（Claude / GPT / Gemini）。開始前先讀完；做完一段工作後更新本檔。

## 分支與 remote

- `origin` = upstream `calesthio/OpenMontage`；`team-fork` = `kwanjuntyan/OpenMontage`。
- 日常開發在 **`lean`**，push 到 `team-fork lean`。
- 舊的複雜版在 `team-main`，tag `archive/complex-v1`（`489638b`）。只拿來參考或撈檔案（`git show team-main:<path>`），不要合併回來。
- 同步 upstream：`git fetch origin; git switch main; git merge --ff-only origin/main; git switch lean; git merge main`。

## 已完成

- `AGENTS.md`：開發原則與協作方式；`CLAUDE.md`、`CODEX.md` 等都指向它。
- 自訂風格：`styles/custom/kj-esg-pixar-hybrid.yaml`、`kj-vox-paper-collage.yaml`。prompt 前綴在 `asset_generation.image_prompt_prefix`，用 `styles.playbook_loader.load_playbook()` 讀。
- **kj-cinematic pipeline**：`pipeline_defs/kj-cinematic.yaml`（= upstream cinematic + `clp` stage，在 script 與 scene_plan 之間）。
  - `schemas/artifacts/clp_manifest.schema.json`（寬鬆）。
  - skills：`skills/pipelines/kj-cinematic/clp-director.md`、`scene-director.md`、`asset-director.md`（後兩者是 cinematic 版的薄包裝）。
- `tools/graphics/google_imagen.py`：`gemini-3*` 模型自動走 Vertex `global` 區域。

## 驗證過的流程（測試專案 `projects/esg-act1-kj/`，未 commit）

- CLP 匯入現成圖並看圖改寫描述：6 張 ✅
- CLP 自行寫 prompt 生圖（Nano Banana Pro）：2 張 ✅
- scene_plan 標註 CLP：21 鏡草稿，checkpoint 為 `awaiting_human`。
- **停在 scene_plan**。使用者說有正式需求再跑到 mp4。繼續時，先問使用者三個待決問題：
  1. 主管通話時所在場景（建議新增 CLP `supervisor_office`）。
  2. s01 倫敦外景不列 CLP，可否？
  3. 分鏡是否核准？
- 輔助腳本在 `.tmp/`：`seed_esg_act1_kj.py`、`gen_clp.py`、`write_clp.py`、`write_scene_plan.py`、`approve_clp.py`。

## 踩過的坑

- **PowerShell**：不要用 `python -c` 塞複雜引號，改寫成 `.tmp/*.py` 再跑。
  - 跑之前設 `$env:PYTHONPATH=(pwd).Path; $env:PYTHONIOENCODING="utf-8"`。
  - 主控台中文顯示亂碼不代表檔案壞了。
- **Nano Banana Pro**：`google_imagen` + `model="gemini-3-pro-image"`。
  - 參考圖用 `image_paths`（本機路徑，最多 14 張），搭配 `generation_mode="edit"`。
  - 不支援 `negative_prompt`，把要避免的寫進 prompt（`Avoid: ...`）。
  - `estimate_cost` 會丟 `PriceQuoteRequired`，報價用估計值：2K 約 US$0.13／張，4K 約 US$0.24／張。
- **Vertex 憑證**在 `.env`（`GOOGLE_APPLICATION_CREDENTIALS` 等）。獨立腳本若只 import `tools.google_credentials`，要先 `load_dotenv()`，否則會誤走 API key 路徑而回 429。
- **`write_checkpoint`** 要求前面的 stage 都是 completed 且已核准；寫入時會用 schema 驗證 artifact。
- **scene_plan** 的 scene 物件 `additionalProperties: false`：CLP 標註放在 `required_assets` 項目（可加 `clp_id`）和 `character_actions[].character_id`。
- **asset_manifest** 的 asset 物件也不能加欄位：CLP 記在 `generation_summary` 開頭，格式 `clp: amy, ... | ...`。
- 已知失敗、與我們無關：`tests/contracts/test_phase3_contracts.py::TestVeoVideo::test_backend_auto_detect`（因為 `.env` 有 Vertex 憑證；乾淨的 upstream 也會失敗）。
- 舊專案 `projects/esg-act1-crisis/` 是複雜版格式，不要還原或混用。

## 下一步候選（使用者決定順序）

1. 從 `team-main` 搬回 `pixar-course` pipeline（在 `gemini/pixar-course-pipeline` 分支）。
2. 工具改良：`gemini_omni_video`、`google_tts`、`google_imagen`。先和 upstream 10/3 版做 diff，只搬確實需要的部分。
3. 專案設定（`foxconn-core-values-course` 等）、3 個 skill（`ai-video-asset-designer`、`ai-video-storyboard-converter`、`google-flow-scripting`）、`vox-explainer` 風格。
4. 尚未回答的問題：影片製作流程的 checkpoint／人工核准關卡要不要也精簡（目前照 `AGENT_GUIDE.md`）。
