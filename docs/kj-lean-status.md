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
- `tools/graphics/google_imagen.py`：`gemini-3*` 與 `gemini-nano-banana-*` 模型自動走 Vertex `global` 區域。
- **2026-10-08 Google 更新**：共用 SDK、Imagen、Cloud TTS 改用服務帳戶 JSON；Google 模型預設直接工具，Veo 不自動改走 fal。
- Omni 預設 `gemini-omni-1.1-flash-preview`：整數 3–10 秒、首尾幀、圖片／影片參考、360p/720p/1080p/4k、編輯／延長、interaction state；預設 inline MP4，可指定 GCS 輸出。
- Gemini TTS 改接 Vertex `global` 的 `generateContent`：3.8 Flash／Flash-Lite、單人／雙人、逐句風格、聲音清單、WAV/PCM/μ-law/A-law。共用 selector 已接通。
- **執行環境**：使用 `.venv/Scripts/python.exe`；已安裝 `google-genai 2.25.0`、`google-auth 2.61.0`，專案 `pip check` 通過。
- **使用者決定**：OM 不需遷就共用環境的 `google-cloud-aiplatform`／`langchain-google-genai`；目前程式與依賴清單未使用它們，專案 `.venv` 亦未安裝。OM 只維護專案環境，升級依 OM 需求，不維持這兩個舊套件的相容性。
- **離線驗證通過**：`.tmp/google_upgrade_smoke.py` 使用真實 SDK 序列化＋模擬 HTTP，驗證 JSON 認證、TTS／圖片、Omni 參數及 selector；WAV／MP4 可讀。付費實測結果見下。
- **Gemini 3.8 TTS 實測通過**：Vertex JSON＋`tts_selector` 成功列出聲音、生成單人中文 6.52 秒及雙人中文 5.20 秒 WAV；24 kHz／16-bit／單聲道，FFmpeg 完整解碼與非靜音檢查通過。輸出 `.tmp/vertex-tts-single.wav`、`.tmp/vertex-tts-duo.wav`；尚未人工聽審。
- **Omni 1.1 實測通過**：使用者改選 Amy 後，`video_selector`＋Vertex JSON＋人物／會議室參考圖成功產出 `.tmp/vertex-omni-amy.mp4`；影片 5.000 秒、1280×720、24 fps，含 AAC 音訊（容器 5.035 秒），完整解碼及首／中／尾抽幀通過。這是唯一生成的影片，首尾幀輸入／編輯／延長仍僅離線驗證。
- **Nano Banana 2.1 已加入**：指定 `model="gemini-nano-banana-2.1"`，由 `image_selector` 直接路由 `google_imagen`，使用 Vertex JSON／global；支援既有生圖、參考圖編輯及 1K/2K/4K 參數。預設模型不變，沿用 genai 2.25.0，未另裝套件。
- **Nano 實測**：兩次相同純文字請求成功，已檢視草圖的繁體中文 ESG 字卡文字正確；第二次保存全部回應，修正草圖誤取後離線重播得到原始正式圖 `.tmp/nano-banana-21-final.png`（2752×1536，2K 級，非本機放大）。兩次各回報輸入 127、圖片輸出 1680 tokens，依官方單價合計估 US$0.101181，未核對帳單；本輪上限 US$0.20。參考圖編輯僅離線驗證，未實測 1K/4K 或角色一致性。
- **Nano 進階參數已接入（尚未付費實測）**：`video_paths`／`pdf_paths` 接受本機檔案陣列，`video_uris`／`pdf_uris` 接受 GCS URI 陣列，可混合原有圖片參考；仍使用 Vertex JSON／global、genai 2.25.0，輸出圖片。
- 指定 `model="gemini-nano-banana-2.1"`、有參考素材時用 `generation_mode="edit"`；例如 `video_paths=[".tmp/vertex-omni-amy.mp4"]`、`video_metadata={"start_offset":"0s","end_offset":"3s","fps":2}`。時間及取樣率套用本次所有影片，未指定就沿用 Google 預設；影片合計最多 10 支，長度／檔案容量仍受 Google 限制。
- `thinking_level` 可選 `MINIMAL`／`MEDIUM`／`HIGH`（省略沿用模型預設 MEDIUM）；`aspect_ratio` 開放官方全部 15 種，含 `21:9`、`9:21`、`8:1`、`1:8`，由 width/height 推算時亦使用完整比例。新選項須明確指定 Nano，其他模型不會默默忽略；原有預設模型不變。
- **進階離線 smoke 通過**：`.tmp/nano_banana_media_smoke.py` 使用真實 SDK＋模擬 HTTP，確認本機／GCS 影片與 PDF、混合圖片、起訖／FPS、三種推理等級、15 種比例與路由；產出可讀 PNG。6 次模擬請求、0 次真實請求，本次費用 US$0；搜尋與多輪編輯未加入。
- **MiniMax／海螺 TTS 已接入**：使用者指定國際版，`minimax_tts` 固定連接 `https://api.minimax.io/v1/`，目前僅開放 `speech-2.6-hd`，也是預設模型；使用 `MINIMAX_API_KEY`，沿用現有 requests，未安裝新套件。Google 仍使用 Vertex JSON。
- `tts_selector` 可指定 `preferred_tool="minimax_tts"`，或用 `model_id="speech-2.6-hd"` 路由；支援既有 Voice ID、`speed`（0.5–2）、`volume`（大於 0 至 10）、`pitch`（整數 -12 至 12）、`emotion`、`language_boost`、`output_format="wav"/"mp3"`。輸出固定 32 kHz／單聲道，`output_path` 副檔名須一致。
- **MiniMax 人工校準 baseline 已保存**：`config/minimax_voice_baselines.json` 匯入 Excel 的 7 個角色；綁定供應商 `minimax`、模型 `speech-2.6-hd` 及各自 Voice ID。別名：`wang/chen/linda/li/george/amy/biao`，語速依序為 `1.2/1/1/1/1.05/1.2/1`。來源：`D:/Dropbox/_AI動畫製作_ESG/A2_聲音庫/ESG_人物語音參數表.xlsx`，未複製金鑰。
- 呼叫 `tts_selector.execute({"voice_baseline":"amy", "text":"台詞", "output_path":".tmp/amy.wav"})`，自動路由 MiniMax 並帶入模型、Voice ID、語速；可加 `speed=1.1` 單次覆寫，不改 JSON。明確換成其他 Voice ID 時不沿用原 baseline 語速；省略 speed 即用工具預設 1.0。跨供應商或未支援模型不套用，直接報錯。
- `operation="list_voices"` 可搭配 `voice_type="all"/"system"/"voice_cloning"/"voice_generation"`；生成費用保持 `unquoted`，不冒稱免費。模型價格／首次使用聲音的費用，須於真實合成前確認。
- **MiniMax 離線 smoke 通過**：`.tmp/minimax_tts_smoke.py` 驗證 registry 自動發現、selector 路由、官方請求規格、列出聲音、Amy 參數／停頓、WAV／MP3 寫入及 FFmpeg 解碼；參數／HTTP／API 錯誤直接拋出，沒有重試或切換供應商。6 次模擬 HTTP、0 次真實呼叫、US$0；輸出為本機測試音，非生成語音。
- **MiniMax baseline 離線 smoke 通過**：`.tmp/minimax_baseline_smoke.py` 確認 7 個角色的路由、模型／Voice ID／語速對應、覆寫不改檔、換聲音不沿用語速，以及 Google 等其他供應商不接受此 baseline；9 次模擬請求、0 次真實生成。
- **MiniMax Amy 實測通過**：使用者已在 `.env` 設定 `MINIMAX_API_KEY`，國際版 `get_voice` 成功找到 Amy 的既有 clone；授權本輪測試並同意 4 個檔案。`tts_selector`＋`voice_baseline="amy"` 自動帶入 1.2 倍語速，唯一一次生成 `.tmp/minimax-amy-baseline.wav`：7.4705 秒、32 kHz／16-bit／單聲道，FFmpeg 完整解碼、非靜音通過（平均 -19.3 dB、峰值 -3.9 dB）；使用者已確認試音成功並核准 commit。
- 本次 Amy 試音事前估低於 US$0.01；API 回報 `usage_characters=79`，按 [官方 speech-2.6-hd 價格](https://platform.minimax.io/docs/pricing/overview) US$100／百萬字元估 US$0.0079，未核對帳單。請求／結果記錄在 `.tmp/minimax-amy-result.json`；其他 6 個聲音尚未逐一連線試音，未 clone／重試／安裝套件。

## 驗證過的流程（測試專案 `projects/esg-act1-kj/`，未 commit）

- CLP 匯入現成圖並看圖改寫描述：6 張 ✅
- CLP 自行寫 prompt 生圖（Nano Banana Pro）：2 張 ✅
- **2026-10-08 分鏡已核准**：主管通話採辦公室（測試沿用 `amy_office`），s01 倫敦外景不列 CLP。
- 使用者要求僅生成 **1 段影片，其餘用圖片**；已生成唯一一段 Amy 技術測試片，保存在 `.tmp/`，未冒充 Harrison 的 s04；專案 assets 仍為 `in_progress`。
- 已準備 s04 Harrison 提問的約 5 秒樣片；其餘預計重用 6 張情境圖。腳本 `.tmp/esg_smoke.py`。
- **2026-10-08 實測授權**：使用者授權 Omni／3.8 TTS 驗證合計 US$3，明確允許人物／會議室參考圖與提示詞送至 Google Vertex AI，後續明確指定改用 `clp/amy.jpeg` 取代 Harrison；沙箱網路需升權。
- **Harrison 參考圖未通過**：Omni HTTP 400 `prohibited_content`，Google 判定輸入涉及知名人物。未產出影片；使用者改選 Amy 後，同模型／參考圖模式成功，不代表 Harrison 素材問題已解除。
- `.tmp/google_live_smoke.py` 保存請求／結果；兩次 400 留存 `.tmp/vertex-omni-error-01.json`、`-02.json`。Amy API 用量為輸入 2386、影片輸出 28960、推理 524 tokens，按官方單價估 US$0.515095。TTS 未回報用量，整輪費用估低於 US$0.60，實際帳單未核對；失敗結果的 `cost_usd=0` 不是帳單證明。
- 輔助腳本在 `.tmp/`：`seed_esg_act1_kj.py`、`gen_clp.py`、`write_clp.py`、`write_scene_plan.py`、`approve_clp.py`。

## 踩過的坑

- **MiniMax 情緒與音訊格式**：`speech-2.6-hd` 支援 `happy/sad/angry/fearful/disgusted/surprised/calm/fluent/whisper`；用 `emotion` 指定整次合成，省略則由模型決定。Excel 的 `(happy)` 等標記不自動解析，`Neutral` 不是 API 列舉值；多種情緒請分句呼叫，`<#0.4#>` 停頓原樣傳送。API 的 `output_format="hex"` 是傳輸編碼，WAV／MP3 則放在 `audio_setting.format`，回傳用十六進位解碼。
- **PowerShell**：不要用 `python -c` 塞複雜引號，改寫成 `.tmp/*.py` 再跑。
  - 跑之前設 `$env:PYTHONPATH=(pwd).Path; $env:PYTHONIOENCODING="utf-8"`。
  - 主控台中文顯示亂碼不代表檔案壞了。
- **Nano Banana Pro**：`google_imagen` + `model="gemini-3-pro-image"`。
  - 參考圖用 `image_paths`（本機路徑，最多 14 張），搭配 `generation_mode="edit"`。
  - 不支援 `negative_prompt`，把要避免的寫進 prompt（`Avoid: ...`）。
  - `estimate_cost` 會丟 `PriceQuoteRequired`，報價用估計值：2K 約 US$0.13／張，4K 約 US$0.24／張。
- **Vertex 憑證**在 `.env`；獨立腳本要先 `load_dotenv()`。共用 client 明確載入 JSON；不再因環境裡有 API key 就改走 AI Studio。
- **Nano 2K 草圖誤取已修**：真實 SDK 請求已送 `imageSize=2K`，回應依序含 `thought=true` 的 1376×768 草圖與 2752×1536 正式圖；舊碼遇第一張即停止，現在略過 thought 圖。`.tmp/nano_banana_smoke.py offline` 可重現修前失敗／修後通過，`.tmp/nano_banana_replay.py` 用保存的真實圖驗證，不再付費。新模型 ID 沒有 `image` 字樣，selector 路由亦已補上；費用按 tokens，保持 `unquoted`，不套舊固定單張價。
- **SDK 離線測試注意**：2.25.0 的巢狀媒體／思考欄位保留 snake_case，二進位使用 URL-safe Base64；測試原先誤設 lowerCamelCase／一般 Base64，已依實際序列化及 ProtoJSON 規格修正，未修改 SDK 或另加轉換層。新功能的 Google 端接受度與生成品質仍待實測。
- **Omni 根因已修**：upstream 10/4 台北版仍是舊模型、只讀 API key、duration 僅估價；新版改用 Vertex REST 與 `response_format.duration`（如 `5s`）。費用估算隨解析度計算影片輸出，輸入／推理 token 另計。
- **Omni HTTP 錯誤明細**：`raise_for_status()` 原本只留下 400 狀態碼，已補回 Google 回應本文，才能區分參數錯誤與內容過濾；實測動畫參考圖也可能觸發知名人物過濾，不繞過。
- **SDK 依賴歷史**：2.25.0 要求 google-auth ≥2.56；先前為共用環境的 aiplatform／LangChain 限制，曾恢復共用套件至 1.65.0／2.48.0，新版裝在專案 `.venv`。使用者後續決定不再遷就這兩個舊套件；共用環境原有 gtts/click 衝突未動。
- **Vertex 媒體**：不使用 AI Studio Files API；本機圖片／影片送 inline data，GCS 使用 URI。URI 輸出要提供 `gcs_uri`，否則使用 inline。
- **`write_checkpoint`** 要求前面的 stage 都是 completed 且已核准；寫入時會用 schema 驗證 artifact。
- **scene_plan** 的 scene 物件 `additionalProperties: false`：CLP 標註放在 `required_assets` 項目（可加 `clp_id`）和 `character_actions[].character_id`。
- **asset_manifest** 的 asset 物件也不能加欄位：CLP 記在 `generation_summary` 開頭，格式 `clp: amy, ... | ...`。
- 已知失敗、與我們無關：`tests/contracts/test_phase3_contracts.py::TestVeoVideo::test_backend_auto_detect`（因為 `.env` 有 Vertex 憑證；乾淨的 upstream 也會失敗）。
- 舊專案 `projects/esg-act1-crisis/` 是複雜版格式，不要還原或混用。

## 下一步候選（使用者決定順序）

1. 從 `team-main` 搬回 `pixar-course` pipeline（在 `gemini/pixar-course-pipeline` 分支）。
2. Omni／3.8 TTS 呼叫實測已通過，樣片／樣音待使用者觀看與聽審。繼續 `esg-act1-kj` 前，決定如何使用 Amy 測試片；原 Harrison s04 尚無影片，不再自動加生第二段。
3. 專案設定（`foxconn-core-values-course` 等）、3 個 skill（`ai-video-asset-designer`、`ai-video-storyboard-converter`、`google-flow-scripting`）、`vox-explainer` 風格。
4. 尚未回答的問題：影片製作流程的 checkpoint／人工核准關卡要不要也精簡（目前照 `AGENT_GUIDE.md`）。
