# kj lean 分支：現況與交接

> 給接手的 agent（Claude / GPT / Gemini）。開始前先讀完；做完一段工作後更新本檔。

## 分支與 remote

- `origin` = upstream `calesthio/OpenMontage`；`team-fork` = `kwanjuntyan/OpenMontage`。
- 日常開發在 **`lean`**，push 到 `team-fork lean`。
- 舊的複雜版在 `team-main`，tag `archive/complex-v1`（`489638b`）。只拿來參考或撈檔案（`git show team-main:<path>`），不要合併回來。
- 同步 upstream：`git fetch origin; git switch main; git merge --ff-only origin/main; git switch lean; git merge main`。

## 已完成
- **2026-10-09 咖啡館 `/360view` 概念測試**：使用者改選 ChatGPT 內建生圖；Dropbox 正面圖先縮至 `.tmp/cafe_360view_reference.jpg`（原始大圖遇 base64 傳輸錯誤），一次成功生成八視角拼圖，保存於 `C:/Users/user/.codex/generated_images/01a120c4-9227-75c2-8031-ff2c5c320dcf/exec-3bee21ef-e1a9-4232-8887-92030a54c5a7.png`；完整提示詞在 `.tmp/cafe_360view_prompt.txt`。目視風格延續，但門／層架／黑板為推測，桌椅朝向有漂移且315度格近正面；僅概念預覽，未驗證Blender幾何，未替換CLP資產；使用帳號額度，工具未回報美元費用。
- **2026-10-09 ESG 2.1.3～2.1.5 R2I 提示詞與實測（部分通過）**：`.tmp/run_r2i_2_1_perspective.py` 保存結構化提示詞，Vertex JSON／global、`gemini-nano-banana-2.1`、2K／16:9；幾何取白模、角色取人物圖、場景圖提供材質。2.1.5 的 `scene_plan.json` 已改成與 2.1.3 共用左偏15度中景白模。
- **本輪圖像結果**：`.tmp/shot_2_1_3_banana_perspective.png` 人物位置、牆腳斜線及掛畫縮短改善（未證明精確15度）；`shot_2_1_4_banana_perspective_v2.png` 歪頭改善但臉仍偏正面，45度側臉未過；`shot_2_1_5_banana_perspective.png` 食指手勢正確，但白模綠牆及跨鏡背景漂移仍未解。四張成功圖均2752×1536，原圖、首版與各次 `.request.json`／`.result.json` 均保留，未升為正式核准資產。
- **費用與中斷**：四張成功圖按回報用量及官方單價估US$0.248283，未核對帳單。2.1.5 全木質補測（`--suffix perspective_v2`）兩次在 OAuth 認證連線逾時，未送到生圖端點；TLS檢查曾成功，根因未確認，停止重送。將新生2.1.3當第五張連戲參考的方案被自動核准審查拒絕，未上傳；現行腳本只用使用者原本指定的參考圖。
- **2026-10-09 ESG 完整課程五幕劇本與 32 件 CLP 資產清單就位**：在 `projects/esg-whole-course/` 完成全套劇本（222 分鏡／1,631.62 秒真實錄音校準）。正式產出 `artifacts/clp_manifest.json`，完整登記 10 位角色、8 大場景、14 件關鍵道具，綁定 5.5K 實體圖檔並完成出場分鏡自動標註，100% 通過 `clp_manifest.schema.json` 驗證；花費 US$0。
- **2026-10-09 童話 HyperFrames 側欄階梯排版**：右側半透明磨砂欄加寬 20%（288px）並全程常駐；段落標題階梯式依序累積出現不消失、新段落出現時前段自動降低亮度；完成 1080p／30fps／40.1 秒渲染 (`renders/frog_and_scorpion_hyperframes.mp4`)，關鍵幀抽樣檢查通過；無額外費用。

- `AGENTS.md`：開發原則與協作方式；`CLAUDE.md`、`CODEX.md` 等都指向它。
- **2026-10-08 開發規則精修**：使用者同意將高推理用於找根因與縮小修改範圍；區分開發／影片製作，按修改內容做最小驗證，驗收通過即停止。既有大檔允許局部修改，已授權範圍不重複詢問；上游影片製作關卡、花費與 commit／push 規則保留。
- 自訂風格：`styles/custom/kj-esg-pixar-hybrid.yaml`、`kj-vox-paper-collage.yaml`。prompt 前綴在 `asset_generation.image_prompt_prefix`，用 `styles.playbook_loader.load_playbook()` 讀。
- **kj-cinematic pipeline**：`pipeline_defs/kj-cinematic.yaml`（= upstream cinematic + `clp` stage，在 script 與 scene_plan 之間）。
  - `schemas/artifacts/clp_manifest.schema.json`（寬鬆）。
  - skills：`skills/pipelines/kj-cinematic/clp-director.md`、`scene-director.md`、`asset-director.md`（後兩者是 cinematic 版的薄包裝）。
- `tools/graphics/google_imagen.py`：`gemini-3*` 與 `gemini-nano-banana-*` 模型自動走 Vertex `global` 區域。
- **2026-10-08 Google 更新**：共用 SDK、Imagen、Cloud TTS 改用服務帳戶 JSON；Google 模型預設直接工具，Veo 不自動改走 fal。
- Omni 預設 `gemini-omni-1.1-flash-preview`：整數 3–10 秒、首尾幀、圖片／影片參考、360p/720p/1080p/4k、編輯／延長、interaction state；預設 inline MP4，可指定 GCS 輸出。
- **Omni 介面精簡**：素材只用 `reference_image_path(s)`、`last_image_path`、`reference_video_paths`、`input_video_path`，同欄位接受本機或 `gs://`；續接用 `previous_interaction_id`。刪 URL 欄位及其他素材別名，冪等欄位同步縮減；Omni 只用 `edit_video`，共用 selector 保留其他供應商的 `video_edit`。
- Gemini TTS 使用 Vertex `global` 的 `generateContent`：3.8 Flash／Flash-Lite、單人／雙人、逐句風格；僅 Gemini 限定 WAV，共用 selector 保留供應商格式與 Azure 轉換。`list_voices` 直接呼叫 `voices.list()`，不提供 search/page_size/page_token/voice_types。
- **執行環境**：使用 `.venv/Scripts/python.exe`；已安裝 `google-genai 2.25.0`、`google-auth 2.61.0`，專案 `pip check` 通過。
- **使用者決定**：OM 不需遷就共用環境的 `google-cloud-aiplatform`／`langchain-google-genai`；目前程式與依賴清單未使用它們，專案 `.venv` 亦未安裝。OM 只維護專案環境，升級依 OM 需求，不維持這兩個舊套件的相容性。
- **離線驗證通過**：`.tmp/google_upgrade_smoke.py` 使用真實 SDK 序列化＋模擬 HTTP，驗證 JSON 認證、TTS／圖片、Omni 參數及 selector；WAV／MP4 可讀。付費實測結果見下。
- **Gemini 3.8 TTS 實測通過**：Vertex JSON＋`tts_selector` 成功列出聲音、生成單人中文 6.52 秒及雙人中文 5.20 秒 WAV；24 kHz／16-bit／單聲道，FFmpeg 完整解碼與非靜音檢查通過。輸出 `.tmp/vertex-tts-single.wav`、`.tmp/vertex-tts-duo.wav`；尚未人工聽審。
- **Omni 1.1 實測通過**：使用者改選 Amy 後，`video_selector`＋Vertex JSON＋人物／會議室參考圖成功產出 `.tmp/vertex-omni-amy.mp4`；影片 5.000 秒、1280×720、24 fps，含 AAC 音訊（容器 5.035 秒），完整解碼及首／中／尾抽幀通過。這是唯一生成的影片，首尾幀輸入／編輯／延長仍僅離線驗證。
- **Nano Banana 2.1 已加入**：指定 `model="gemini-nano-banana-2.1"`，由 `image_selector` 直接路由 `google_imagen`，使用 Vertex JSON／global；支援既有生圖、參考圖編輯及 1K/2K/4K 參數。預設模型不變，沿用 genai 2.25.0，未另裝套件。
- **Nano 實測**：兩次相同純文字請求成功，已檢視草圖的繁體中文 ESG 字卡文字正確；第二次保存全部回應，修正草圖誤取後離線重播得到原始正式圖 `.tmp/nano-banana-21-final.png`（2752×1536，2K 級，非本機放大）。兩次各回報輸入 127、圖片輸出 1680 tokens，依官方單價合計估 US$0.101181，未核對帳單；本輪上限 US$0.20。參考圖編輯僅離線驗證，未實測 1K/4K 或角色一致性。
- **圖片參考媒體介面已精簡（尚未付費實測）**：原 video_paths/video_uris/pdf_paths/pdf_uris 合併成 `media_paths` 陣列，本機讀檔、`gs://` 用 `from_uri`，MIME 依副檔名判斷；可混合原有圖片參考，沿用 Vertex JSON／global、genai 2.25.0。
- 有參考素材時用 `generation_mode="edit"`；例如 `model="gemini-nano-banana-2.1", media_paths=[".tmp/vertex-omni-amy.mp4", "gs://bucket/reference.pdf"]`、`video_metadata={"start_offset":"0s","end_offset":"3s","fps":2}`。metadata 只附加於影片，未提供影片時不附加；長度與容量限制由供應商處理。
- `thinking_level` 可選 `MINIMAL`／`MEDIUM`／`HIGH`；Nano 的 `aspect_ratio` 支援 15 種，依 width/height 推算時亦使用完整比例。已刪「非 Nano 不可用」與「video_metadata 需要影片」檢查；其他模型是否支援須由 API 回應確認，移除本機限制不代表已實測相容。
- **進階離線 smoke 通過**：`.tmp/nano_banana_media_smoke.py` 使用真實 SDK＋模擬 HTTP，確認 media_paths 的本機／GCS 影片與 PDF、混合圖片、起訖／FPS、推理等級、15 種比例及移除限制後的請求；產出可讀 PNG。8 次模擬請求、0 次真實請求；搜尋與多輪編輯未加入。
- **MiniMax／海螺 TTS 已接入**：使用者指定國際版，`minimax_tts` 固定連接 `https://api.minimax.io/v1/`，目前僅開放 `speech-2.6-hd`，也是預設模型；使用 `MINIMAX_API_KEY`，沿用現有 requests，未安裝新套件。Google 仍使用 Vertex JSON。
- `tts_selector` 可指定 `preferred_tool="minimax_tts"`，或用 `model_id="speech-2.6-hd"` 路由；支援既有 Voice ID、`speed`（0.5–2）、`volume`（大於 0 至 10）、`pitch`（整數 -12 至 12）、`emotion`、`language_boost`。經 selector 或直接呼叫均可選 WAV／MP3；輸出固定 32 kHz／單聲道，`output_path` 副檔名須一致。
- **MiniMax 人工校準 baseline 已保存**：`config/minimax_voice_baselines.json` 匯入 Excel 的 7 個角色；綁定供應商 `minimax`、模型 `speech-2.6-hd` 及各自 Voice ID。別名：`wang/chen/linda/li/george/amy/biao`，語速依序為 `1.2/1/1/1/1.05/1.2/1`。來源：`D:/Dropbox/_AI動畫製作_ESG/A2_聲音庫/ESG_人物語音參數表.xlsx`，未複製金鑰。
- 呼叫 `tts_selector.execute({"voice_baseline":"amy", "text":"台詞", "output_path":".tmp/amy.wav"})`，自動路由 MiniMax 並帶入模型、Voice ID、語速；可加 `speed=1.1` 單次覆寫，不改 JSON。明確換成其他 Voice ID 時不沿用原 baseline 語速；省略 speed 即用工具預設 1.0。baseline 只由 MiniMax 工具讀取；已移除設定檔 provider 檢查與 selector 的跨供應商報錯。
- `operation="list_voices"` 可搭配 `voice_type="all"/"system"/"voice_cloning"/"voice_generation"`；生成費用保持 `unquoted`，不冒稱免費。模型價格／首次使用聲音的費用，須於真實合成前確認。
- **MiniMax 離線 smoke 通過**：`.tmp/minimax_tts_smoke.py` 驗證 registry 自動發現、selector 路由、官方請求規格、列出聲音、Amy 參數／停頓、WAV／MP3 寫入及 FFmpeg 解碼；參數／HTTP／API 錯誤直接拋出，沒有重試或切換供應商。6 次模擬 HTTP、0 次真實呼叫、US$0；輸出為本機測試音，非生成語音。
- **MiniMax baseline 歷史驗證**：7 個角色的路由、模型／Voice ID／語速對應、覆寫不改檔、換聲音不沿用語速曾通過。本輪 `.tmp/minimax_tts_smoke.py` 的 WAV／MP3 均經 selector，WAV 使用 Amy baseline；舊 `.tmp/minimax_baseline_smoke.py` 含已刪除的跨供應商報錯斷言，本輪未跑。
- **MiniMax Amy 實測通過**：使用者已在 `.env` 設定 `MINIMAX_API_KEY`，國際版 `get_voice` 成功找到 Amy 的既有 clone；授權本輪測試並同意 4 個檔案。`tts_selector`＋`voice_baseline="amy"` 自動帶入 1.2 倍語速，唯一一次生成 `.tmp/minimax-amy-baseline.wav`：7.4705 秒、32 kHz／16-bit／單聲道，FFmpeg 完整解碼、非靜音通過（平均 -19.3 dB、峰值 -3.9 dB）；使用者已確認試音成功並核准 commit。
- 本次 Amy 試音事前估低於 US$0.01；API 回報 `usage_characters=79`，按 [官方 speech-2.6-hd 價格](https://platform.minimax.io/docs/pricing/overview) US$100／百萬字元估 US$0.0079，未核對帳單。請求／結果記錄在 `.tmp/minimax-amy-result.json`；其他 6 個聲音尚未逐一連線試音，未 clone／重試／安裝套件。
- **童話專案實測通過（`projects/frog-and-scorpion/`）**：`kj-cinematic` pipeline；Google TTS `gemini-3.8-flash-tts`（Kore）4 段旁白 WAV（40 秒）；CLP 3 實體通過；Agent Native 生成 4 張 16:9 皮克斯畫面；成功完成 FFmpeg 平滑版與 HyperFrames 成品版（Chrome + GSAP 30fps，皮克斯金色動態標題 + 磨砂篇章字幕卡 + GPU 浮點運鏡）渲染出片 (`renders/frog_and_scorpion_hyperframes.mp4`)。

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
- **R2I 幾何與材質仍可能互相污染**：只寫「依白模視角」不足；指定牆腳、畫框上下邊、木條間距朝同一消失方向收斂可改善背景，但本輪仍出現白模綠牆被當成材質、Amy被生為正臉。現行2.1.5新增全牆／柱包覆原木的正向描述，受認證逾時影響尚未驗證；未宣稱全鏡一致性通過。
- **人物文字也要服從實圖**：目前George實體設定圖是棕色背心、奶油白襯衫、領帶及深色方框眼鏡；本輪提示詞直接引用人物圖，未沿用交接文字的深灰針織背心／圓框描述，未改動角色圖與CLP清單。

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
- **共用 selector 不套用單一工具限制**：先前誤刪通用 `video_edit` 並把所有 TTS 限為 WAV；已恢復影片操作、通用格式與 Azure 轉換。已刪除失效的 Veo `test_backend_auto_detect`；只跑指定 3 支離線 smoke。
- 舊專案 `projects/esg-act1-crisis/` 是複雜版格式，不要還原或混用。
- **Windows Backlot MIME 陷阱**：Windows 登錄檔易將 `.js` 誤註冊為 `text/plain` 導致 ES Module 被拒呈黑畫面；已在 `backlot/server.py` 加入 `mimetypes.add_type` 並更新檔案 mtime 破除 304 快取。
- **FFmpeg 單圖 Ken Burns 抖動陷阱**：禁止在 zoompan 前加 `-loop 1`（會引發影格衝突重算），且須先升至 4K（3840×2160）超採樣再縮回 1080p，搭配 30fps 徹底消除子像素截斷抖動。
- **CLP Manifest 文字污染陷阱**：CLP 描述文字不可套用通用模板或臆造（如咖啡廳紅磚牆與鐵框窗、咖啡杯紅陶底）；文字與參考圖脫節會導致模型受文字干擾發明背景。實體圖片為唯一真理（Source of Truth），描述必須嚴格對齊圖片特徵。

## 下一步候選（使用者決定順序）
- 本輪R2I待續：先處理Vertex OAuth連線，再執行 `.tmp/run_r2i_2_1_perspective.py 5 --suffix perspective_v2 --live` 驗證全木質背景；Amy45度側臉及3／5跨鏡佈景仍待解，下一次付費前重新報價。所有測試沿用專案`.venv`，不需重跑整套影片。

1. 從 `team-main` 搬回 `pixar-course` pipeline（在 `gemini/pixar-course-pipeline` 分支）。
2. Omni／3.8 TTS 呼叫實測已通過，樣片／樣音待使用者觀看與聽審。繼續 `esg-act1-kj` 前，決定如何使用 Amy 測試片；原 Harrison s04 尚無影片，不再自動加生第二段。
3. 專案設定（`foxconn-core-values-course` 等）、3 個 skill（`ai-video-asset-designer`、`ai-video-storyboard-converter`、`google-flow-scripting`）、`vox-explainer` 風格。
4. 尚未回答的問題：影片製作流程的 checkpoint／人工核准關卡要不要也精簡（目前照 `AGENT_GUIDE.md`）。
