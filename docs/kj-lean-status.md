# kj lean 分支：現況與交接

> 給接手的 agent（Claude / GPT / Gemini）。開始前先讀完；做完一段工作後更新本檔。
## 分支與 remote

- `origin` = upstream `calesthio/OpenMontage`；`team-fork` = `kwanjuntyan/OpenMontage`。
- 日常開發在 **`lean`**，push 到 `team-fork lean`。
- 舊的複雜版在 `team-main`，tag `archive/complex-v1`（`489638b`）。只拿來參考或撈檔案（`git show team-main:<path>`），不要合併回來。
- 同步 upstream：`git fetch origin; git switch main; git merge --ff-only origin/main; git switch lean; git merge main`。

## 已完成
- **2026-10-10 Shot 2.1.5 W2I 雙場景實測**：依 Asset Director 與 W2I 配方（白模→front+left_far雙場景→George→杯碟共五圖），使用 Vertex JSON／global／Nano Banana 2.1／2K／16:9 生成 `.tmp/shot_2_1_5_w2i.png`（2752×1536）；輸入 6768（圖片 5600、文字 1168）、圖片輸出 1680 tokens，估約 US$0.0607。George 右手食指引導手勢精確成立，左側大窗、中央綠柱植物畫與右側第二扇窗幾何完美對齊白模，桌面純白杯碟糖罐保留。
- **2026-10-10 Shot 2.1.4 W2I 實測（v1 單場景與 v2 雙場景 front+right）**：依 Asset Director 與 W2I 配方（白模→front+right雙場景→Amy共四圖），Vertex JSON／global／Nano Banana 2.1／2K／16:9 生成 `.tmp/shot_2_1_4_w2i_v2.png`（2752×1536）；輸入 5532（文字 1052、圖片 4480）、圖片輸出 1680 tokens，估約 US$0.0588。相較 v1，v2 前方桌椅退出，特寫取景與人物佔位更忠實對齊白模；右側木牆完美融入植物畫與垂藤，左身後吧台、磨豆機與黑板菜單細節完整，Amy 綠眼、雀斑與驚奇反問神態生動。
- **2026-10-10 咖啡館 CLP 視角資產擴充與替換**：使用者核准導入 3 張 5.5K CLP 新圖；新增右側吧台全景 `clp/loc_esg_coffee_shop_right_far.jpg`、新增左側單窗中景 `clp/loc_esg_coffee_shop_left.jpg`（由 left_v2 改名），並以 `left_v1` 覆蓋替換原 `clp/loc_esg_coffee_shop_left_far.jpg`（補齊中央綠柱植物標本畫）。`artifacts/clp_manifest.json` 已同步登記 6 張視角圖，通過 schema 驗證；花費 US$0。
- **2026-10-10 kj-cinematic assets 自足化**：移除上游 Asset Director 繼承，補音訊先行、八類 `prompt-recipes.md`、CLP 佈景／白模取景分工、W2I→W2V 交接；接通 TTS／本機音樂庫。離線 loader、既有／兩步 scene 格式及 Shot 2.1.3 selector→Google adapter 的四圖順序／global／2K 通過；報告 `.tmp/kj_asset_director_offline_report.json`。1 次模擬 SDK 回應、0 次真實 API，未驗證生成品質；schema 與 adapter 未改。
- **2026-10-10 CLP 共用描述／配方分流整理及 W2I 實測**：George 與咖啡館 description 已依實圖修正，既有 schema 驗證通過。Director 管共通來源、音訊、工具、交接與驗收；Recipes 管八類配方。W2I 恢復原五段，十項分鏡欄位供設計選填，白模提供姿勢／互動基準，明確修改優先；素材按白模→場景→人物→道具連號，W2V 保留原五段。`scripts/read_prompt_recipe.py` 八類 CLI 讀取通過；原例文字裝配及報告保留在 `.tmp/w2i_original_example_*`，僅離線。使用者另授權 Shot 2.1.3：核對四張實圖後以新版五段、`image_selector→google_imagen`／Vertex JSON／global／Nano Banana 2.1／2K／16:9 成功生成一張 `.tmp/shot_2_1_3_w2i_v3.png`（2752×1536）；同 stem 的 `_prompt.txt`、`.request.json`、`.result.json` 保存請求及用量。輸入6308、圖片輸出1680 tokens，按 Google 官方單價估 US$0.059862，未核對帳單。人物外觀及部分窗戶保留，但右後方新增椅子／牆面、窗區改變，取景與杯底空隙仍有偏差，未列正式核准素材；八類未全面實測，Agent 自動遵循與上下文隔離未驗證。 本輪 W2I 裝配指引要求 Agent 理解元素關係、對應白模；第三段範本加入必須送給生圖引擎的場景理解與保留規則，區分鏡位投影、出框／遮擋、白模省略特徵與明確修改。已依新規則重產 `.tmp/shot_2_1_3_w2i_v4_prompt.txt` 與同 stem 的 `.request.json`，第三段保留通用引擎規則並填入本鏡元素對應；四圖順序、五段與十項欄位離線核對通過，未送出生成，v3 紀錄保留。 本輪再將欄位選單移出送出範本，Agent 按最新指示／核准分鏡取捨與合併，CLP 只摘必要短句；新增 `.tmp/shot_2_1_3_w2i_v5_prompt.txt` 供檢閱（3903→1698字元），保留五段與場景空間規則。使用者核准後，以相同四圖、模型與參數成功生成 `.tmp/shot_2_1_3_w2i_v5.png`（2752×1536）；請求／結果／用量／目視比較合存 `.result.json`，未改 Prompt。輸入5518（文字1038、圖片4480）、圖片輸出1680 tokens，按官方單價估 US$0.058677，未核對帳單；與 v3 比較，右後方多餘梳背椅消失、杯底離碟空隙清楚，頭部尺度／留白略改善，但改成左手持杯、最右木牆／掛畫仍進入取景，未列正式核准素材。每版僅一張，空間規則與篇幅同時改動，不能單獨歸因於精簡。
- **2026-10-09 咖啡館 `/360view` 概念測試**：使用者改選 ChatGPT 內建生圖；Dropbox 正面圖先縮至 `.tmp/cafe_360view_reference.jpg`（原始大圖遇 base64 傳輸錯誤），一次成功生成八視角拼圖，保存於 `C:/Users/user/.codex/generated_images/01a120c4-9227-75c2-8031-ff2c5c320dcf/exec-3bee21ef-e1a9-4232-8887-92030a54c5a7.png`；完整提示詞在 `.tmp/cafe_360view_prompt.txt`。目視風格延續，但門／層架／黑板為推測，桌椅朝向有漂移且315度格近正面；僅概念預覽，未驗證Blender幾何，未替換CLP資產；使用帳號額度，工具未回報美元費用。
- **2026-10-09 ESG 2.1.3～2.1.5 R2I 提示詞與實測（部分通過）**：`.tmp/run_r2i_2_1_perspective.py` 保存結構化提示詞，Vertex JSON／global、`gemini-nano-banana-2.1`、2K／16:9；幾何取白模、角色取人物圖、場景圖提供材質。2.1.5 的 `scene_plan.json` 已改成與 2.1.3 共用左偏15度中景白模。
- **本輪圖像結果**：`.tmp/shot_2_1_3_banana_perspective.png` 人物位置、牆腳斜線及掛畫縮短改善（未證明精確15度）；`shot_2_1_4_banana_perspective_v2.png` 歪頭改善但臉仍偏正面，45度側臉未過；`shot_2_1_5_banana_perspective.png` 食指手勢正確，但白模綠牆及跨鏡背景漂移仍未解。四張成功圖均2752×1536，原圖、首版與各次 `.request.json`／`.result.json` 均保留，未升為正式核准資產。
- **費用與中斷**：四張成功圖按回報用量及官方單價估US$0.248283，未核對帳單。2.1.5 全木質補測（`--suffix perspective_v2`）兩次在 OAuth 認證連線逾時，未送到生圖端點；TLS檢查曾成功，根因未確認，停止重送。將新生2.1.3當第五張連戲參考的方案被自動核准審查拒絕，未上傳；現行腳本只用使用者原本指定的參考圖。
- **2026-10-10 scene_plan.schema.json 擴充 render_stages**：在 `scenes.items.properties` 局部新增 `render_stages`（枚舉限定八大模態：T2I/I2I/R2I/W2I/T2V/I2V/R2V/W2V），已通過離線 schema 驗證與非破壞相容性測試。
- **2026-10-09 ESG 完整課程五幕劇本與 32 件 CLP 資產清單就位**：在 `projects/esg-whole-course/` 完成全套劇本（222 分鏡／1,631.62 秒真實錄音校準）。正式產出 `artifacts/clp_manifest.json`，完整登記 10 位角色、8 大場景、14 件關鍵道具，綁定 5.5K 實體圖檔並完成出場分鏡自動標註，100% 通過 `clp_manifest.schema.json` 驗證；花費 US$0。
- **2026-10-09 童話 HyperFrames 側欄階梯排版**：右側半透明磨砂欄加寬 20%（288px）並全程常駐；段落標題階梯式依序累積出現不消失、新段落出現時前段自動降低亮度；完成 1080p／30fps／40.1 秒渲染 (`renders/frog_and_scorpion_hyperframes.mp4`)，關鍵幀抽樣檢查通過；無額外費用。
- `AGENTS.md`：開發原則與協作方式；`CLAUDE.md`、`CODEX.md` 等都指向它。
- **2026-10-08 開發規則精修**：使用者同意將高推理用於找根因與縮小修改範圍；區分開發／影片製作，按修改內容做最小驗證，驗收通過即停止。既有大檔允許局部修改，已授權範圍不重複詢問；上游影片製作關卡、花費與 commit／push 規則保留。
- 自訂風格：`styles/custom/kj-esg-pixar-hybrid.yaml`、`kj-vox-paper-collage.yaml`。prompt 前綴在 `asset_generation.image_prompt_prefix`，用 `styles.playbook_loader.load_playbook()` 讀。
- **kj-cinematic pipeline**：`pipeline_defs/kj-cinematic.yaml`（= upstream cinematic + `clp` stage，在 script 與 scene_plan 之間）。
  - `schemas/artifacts/clp_manifest.schema.json`（寬鬆）。
  - skills：`skills/pipelines/kj-cinematic/clp-director.md`、`scene-director.md`、`asset-director.md`；scene 仍繼承 cinematic，assets 自足並搭配 `prompt-recipes.md`，共用既有工具與製作 checkpoint。
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
- **W2I 圖文職責衝突**：Shot 2.1.3 曾出現窗區木板化與杯子提前落碟。2026-10-10 v3 實測保留人物外觀、部分玻璃窗／綠意及右手持杯，但右後方新增梳背椅與牆面、窗區改變，頭部比白模大、頭頂留白減少，杯底離碟空隙偏小，首幀未完全通過。驗收曾漏掉佈景偏差；新版 W2I 從場景元素關係與鏡位轉換編寫通用保留要求，不逐項把案例禁令加入 skill，v5 實測局部改善佈景與杯底空隙，但原文指定右手仍生為左手，最右木牆／掛畫仍帶入，不能因文字規則齊全就判定驗收通過。v6 直接辨識／保留指令及左右手消歧後，右手正確、杯底空隙保留，但右窗區變成木牆、窗格及白模取景仍未過；每版一張且場景規則與手部文字同時調整，不能單獨歸因。首輪被 sandbox 網路限制擋在 OAuth（WinError 10013），未送生圖；取得網路權限後同一請求成功，錯誤另存 `.tmp/shot_2_1_3_w2i_v3.oauth-error.json`，未換認證／模型。George manifest 已依實圖修正棕色背心、奶油色襯衫、深棕領帶／長褲、方框眼鏡、銀灰髮／白色短鬍鬚，移除固定表情與性格；schema 驗證通過，實體與參考圖未改。
- **assets 指引載入與維護落差**：上游未提供完整 Audio-First，已移除 YAML 的上游 required_skill 並接通 TTS；四圖需求不能沿用舊三圖上限。Director／Recipe 曾重複維護細則，且「只交代職責」與 CLP 摘錄衝突、R 類混入白模條款、W2I 一律當首幀；現已按工序／配方分工，改為省略多餘空間定位、R 類依分鏡、獨立 W2I 呈現指定瞬間。2026-10-10 再修正「刪除與素材不符指令」的歧義：依素材職責判斷，本鏡指定表演與白模／CLP 展示姿態不同不算衝突。八類索引後直接接共用五段式，容易讓 T／I／R 也套 W 模板；現已分節並提供各自範本，以章節讀取工具輸出當前配方，避免先讀八類全文；它不清除已讀上下文。場景通則曾混入窗牆等具體設定，現已改為依經核對的 CLP 保留，I2I 的明確修改另按本次要求。後半部只詳述 W2I→W2V 交接，其他多步組合與交付適用範圍不夠清楚；現已補共通交接、W2V 特例及圖片／影片驗收差異，未新增核准關卡。本輪另修正 W2I 將原五段縮成工序摘要、白模職責過度縮窄的問題：恢復原 Prompt 結構、分鏡欄位、完整風格與輸出要求，以使用者原例文字裝配核對。上述僅離線驗證，未生成。 W2I 曾把十項設計選項全數當作送出欄位、抄入過長 CLP 摘錄；已分開設計選單與引擎範本，要求 Agent 取捨、省略及合併，未以精簡篇幅宣稱品質提升。本輪將 W2I 素材核對與引擎規則分開：Agent 不需轉寫整個場景，僅具體歧義補短句；第三段直接要求引擎辨識並保留構件造型、分割、連接與相對位置，沿用白模鏡位，僅離線核對。
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
- **W2I Shot 2.1.3 本輪已結案（使用者接受 v13）**：使用者決策為增加場景參考圖、採用 v8／v13 的 Prompt 寫法；暫不追加生成。已將 v8／v13 寫法同步至既有 W2I 唯一範本：第一段只說圖片內容，第三段採簡潔素材分工與保留正文；單張／多張場景共用一份範本，多張只加經核對的互補範圍。Agent 保留標題與通用正文，依素材填引用、本鏡設定及核准風格／比例；人物表演依最新指示／核准分鏡，案例不作通用預設。Director 與章節讀取工具接線保留；既有 W2I CLI 讀取與 v8 單場景／v13 多場景規則裝配離線核對通過；本輪未重新送出生成。其餘模態與本輪觀察保留。以下為測試歷程：W2I v3 已生成一張，已確認佈景、人物取景及杯底空隙偏差；W2I v4 Prompt／請求保留，v5 精簡 Prompt 已實測並與 v3 比較，局部改善但仍有左右手及窗牆取景偏差，待使用者檢閱，不自動補生成。最新 W2I 範本已套入 `.tmp/shot_2_1_3_w2i_v6_prompt.txt`（36行／1569字元），使用者授權同四圖／Vertex JSON／global／Nano Banana 2.1／2K／16:9 生成一張 `.tmp/shot_2_1_3_w2i_v6.png`（2752×1536）；請求、用量及與 v5 比較合存 `.result.json`，Prompt 未改。輸入5418（文字938／圖片4480）、圖片輸出1680 tokens，按官方單價估 US$0.058527，未核對帳單；右手修正但右窗區改成木牆、左窗分格與取景仍偏離，未核准，不補生成，舊版紀錄保留。另依使用者指定四條素材分工建立 `.tmp/shot_2_1_3_w2i_v7_prompt.txt`（34行／1273字元），僅第三段重寫、第一段移除重複權責並保留圖片識別與必要 CLP 短句；第二／四／五段及右手持杯設定未變，skill 未改。四圖與修改範圍離線核對通過，未送生圖，尚不能確認根因或品質改善。後續依使用者將第一段改為「參考圖內容」、第三段集中素材使用與符合參考圖的要求，建立 `.tmp/shot_2_1_3_w2i_v8_prompt.txt`（37行／1444字元）；保留 v7 四條分工，人物表演及必要道具互動依第二段，白模鏡位造成的透視／裁切／遮擋不算改造佈景。其他三段、四圖順序與舊版／skill 未變；使用者授權同參數生成一張 v8（2752×1536），請求／用量／與 v6 比較合存 `.tmp/shot_2_1_3_w2i_v8.result.json`。輸入5307（文字827／圖片4480）、圖片輸出1680、推理1941 tokens，按官方單價估 US$0.072918，未核對帳單。右窗恢復、右手與杯底空隙正確，但窗格仍缺橫向分割、人物偏左不符白模佔位、綠牆掛畫空白；未完全通過，不補生成，單張結果不能確認根因。本輪依使用者原文，v9 僅替換第三段 IMAGE 2 句子為裝潢／窗戶／掛畫／桌椅，完整 Prompt（37行／1448字元）、請求、用量及與 v8 比較合存 `.tmp/shot_2_1_3_w2i_v9.result.json`，未另建 Prompt 檔。沿用同四圖與參數生成一張 v9（2752×1536）；輸入5312（文字832／圖片4480）、圖片輸出1680、文字輸出374、推理1284 tokens，按官方單價估 US$0.070803，未核對帳單。橫向窗格與木牆植物掛畫出現，但木牆／吊燈／桌椅區重新進入取景、杯底空隙縮小；人物較 v8 接近中央仍未符合白模鏡位與尺度，未完整通過，不補生成，v8／skill 保留。本輪測方法2：v10 僅套入使用者核准的精簡第三段，指定 IMAGE 1 的鏡位／VIEW／人物佔位與尺度／透視為唯一依據，IMAGE 2 不沿用拍攝角度或構圖；完整 Prompt（38行／1448字元）合存 `.tmp/shot_2_1_3_w2i_v10.result.json`，其他四段與同四圖／參數未變。成功生成一張 v10（2752×1536）；輸入5314（文字834／圖片4480）、圖片輸出1680 tokens，API 未回報推理用量，按回報用量及官方單價估 US$0.058371，未核對帳單。右手與杯底空隙正確、橫向窗格可見，但取景擴大帶入更多桌椅／木牆／吊燈／風管／糕點展示櫃，人物仍偏左、綠牆小畫框空白，未固定白模 VIEW；單張未達方法2目的，未完整通過，不補生成，舊成果／skill 保留；Flow 編修由使用者同事處理。本輪測裁切參考圖：原場景純裁切 (1200,200)-(3250,2050)，保留兩組窗戶／中央綠牆／窗邊吧台與座椅及周邊餘量，新增 `.tmp/loc_esg_coffee_shop_left_far_crop.jpg`（2050×1850，未縮放／改透視）。v11 保留 v8 Prompt 原文與其他三張參考／工具參數，只替換 Image 2，成功生成一張 `.tmp/shot_2_1_3_w2i_v11.png`（2752×1536）；完整請求／裁切座標／用量／與 v8 比較合存 `.result.json`。輸入5307（文字827／圖片4480）、圖片輸出1680 tokens，API 未回報推理用量，按回報用量及官方單價估 US$0.058361，未核對帳單。橫向窗格出現，但左窗組被綠牆分開、George 轉為偏右／朝左，白模 VIEW 與場景相鄰關係仍未通過；單張未解漂移，未確認根因，不補生成，原圖／Prompt／skill 保留。重新看圖確認原場景中央小框本來近乎空白，不以缺植物畫判失敗。使用者要求改為16:9後，另由原場景裁切 (1100,450)-(3404,1746)，新增 `.tmp/loc_esg_coffee_shop_left_far_crop_16x9.jpg`（原生2304×1296，精確16:9），保留兩組窗／中央綠牆／窗邊吧台與座椅及周邊餘量；尺寸足夠，未插值放大／拉伸／改透視。已目視及尺寸核對，僅交付裁切圖供檢閱，未送生成；舊裁切及v11保留。使用者核准16:9裁切圖後，v12 以其替換 Image 2、v8 Prompt 逐字不變，其他三圖／工具參數沿用，成功生成一張 `.tmp/shot_2_1_3_w2i_v12.png`（2752×1536）；完整請求／裁切座標／用量／與v8及v11比較合存 `.result.json`。輸入5307（文字827／圖片4480）、圖片輸出1680 tokens，API 未回報推理用量，依回報用量與官方單價估 US$0.058361，未核對帳單。兩組窗格與中央綠牆較v11接近場景圖，右手／杯底空隙保留；但取景與透視較接近場景圖，George仍偏右／朝左、層架與垂藤／木牆邊緣入鏡，未固定白模VIEW，未通過、不補生成。v11到v12同時改裁切範圍及比例，各一張，不能單獨歸因於16:9；舊版／Prompt／skill保留。依使用者指定加入front與最新左側近景，以v8改寫 `.tmp/shot_2_1_3_w2i_v13_prompt.txt`；五圖順序為白模→`loc_esg_coffee_shop_front.jpg`→16:9左側裁切→George→杯碟，第一段只說圖像內容，第三段由兩場景共同提供佈景／元素關係、左側圖對應本鏡窗牆細節，鏡位及VIEW仍依白模。第二／四／五段及風格前綴未變；五圖引用與修改範圍離線核對通過，僅供檢閱、未送生成，skill及舊版保留。使用者核准後，以 v13 五圖透過 image_selector→google_imagen／Vertex JSON／global／Nano Banana 2.1／2K／16:9 送出一次，實際收到 2752×1536 PNG；核對原樣 Prompt 與五圖有序位元組，輸入6571／圖片輸出1680 tokens，按 API 回報及官方單價估約 US$0.060256（未核對帳單，推理用量未回報）。v13 的右手持杯與離碟空隙正確，窗格保留，George 朝右較 v12 接近白模；左層架、吊燈／垂藤及右前木椅仍進入白模未指定的 VIEW，頭頂留白偏少，未通過完整取景驗收。請求、用量及比較合存 `.tmp/shot_2_1_3_w2i_v13.result.json`，成果為同名 PNG；單張結果不能證明雙場景圖已解決飄移，未追加生成或修改 skill。依使用者要求測 front＋原始 left_far，v14 只替換 v13 的 Image 3 並同步該圖名稱／檔名，其餘 Prompt、五圖順序及工具參數保留；同模型送出一次，成功生成 `.tmp/shot_2_1_3_w2i_v14.png`（2752×1536），完整 Prompt／請求／用量／與v13比較合存同名 `.result.json`。實際核對五圖原始位元組及順序，輸入6564／圖片輸出1680／推理2356 tokens，按官方單價估 US$0.077916，未核對帳單。層架、吊燈及右前木椅退出，人物朝右且近中央，桌面右側罐子與第二杯恢復，VIEW較v13接近白模；但左窗缺橫向窗格、右窗多分格，綠牆小框改成植物畫並增加垂藤，杯底空隙較不明顯，未通過完整場景一致性。front木牆／服務區未呈現，不能驗證全場景多視角一致；各一張、未固定種子，未確認穩定性，不補生成、不改skill，舊版保留。舊 v2 Prompt／請求未重產、舊 R2I 腳本不作為新版實測證明。2.1.3 規劃12.42秒且缺白模影片，W2V 尚不可實測；Amy45度側臉及3／5連戲仍待解，下次付費前重新報價，沿用專案`.venv`。
1. 從 `team-main` 搬回 `pixar-course` pipeline（在 `gemini/pixar-course-pipeline` 分支）。
2. Omni／3.8 TTS 呼叫實測已通過，樣片／樣音待使用者觀看與聽審。繼續 `esg-act1-kj` 前，決定如何使用 Amy 測試片；原 Harrison s04 尚無影片，不再自動加生第二段。
3. 專案設定（`foxconn-core-values-course` 等）、3 個 skill（`ai-video-asset-designer`、`ai-video-storyboard-converter`、`google-flow-scripting`）、`vox-explainer` 風格。
4. 尚未回答的問題：影片製作流程的 checkpoint／人工核准關卡要不要也精簡（目前照 `AGENT_GUIDE.md`）。
