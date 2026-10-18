# kj lean 分支：現況與交接
> 給接手的 agent（Claude / GPT / Gemini）。開始前先讀完；做完一段工作後更新本檔（保持 100 行內）。歷次逐鏡生圖與 Blender 精修流水帳已完整歸檔於 [`docs/kj-lean-history.md`](kj-lean-history.md)。

## 分支、環境與專案結構
- **Remote 與分支**：`origin` = upstream `calesthio/OpenMontage`；`team-fork` = `kwanjuntyan/OpenMontage`。日常開發在 `lean`，push 到 `team-fork lean`。舊複雜版在 `team-main`（tag `archive/complex-v1`）。同步 upstream：`git switch main; git merge --ff-only origin/main; git switch lean; git merge main`。
- **開發與協作規則**：見 [`AGENTS.md`](../AGENTS.md)（`CLAUDE.md`、`CODEX.md` 等均指向它）。含「既有專案的局部修改與續作」六點，以及「少碰原始檔、單點插入、一題一 Commit」原則。
- **執行環境**：統一使用 `.venv/Scripts/python.exe`（已裝 `google-genai 2.25.0`、`google-auth 2.61.0`，`pip check` 通過）；不遷就未使用的 `google-cloud-aiplatform`／`langchain-google-genai`。
- **`projects/` 資產庫**：透過 Windows Junction 指向 `D:\Dropbox\kj-om-projects`，根目錄保留五大專案：`course-51-esg`、`course-31-pdca`（收納 8 章節與批次腳本）、`client-01-foxconn-core-values`、`fairytale-01-frog-and-scorpion`、`fairytale-02-mole-stargazer`。`.gitignore` 已設白名單將各專案的 `artifacts/`、`project.json` 與 `checkpoint_*.json` 納入 Git 版控（大型影音留 Dropbox）；團隊建置步驟見 [`docs/team-setup.md`](team-setup.md)。

## 核心 Pipeline 與已接通工具
- **`kj-cinematic` pipeline**：[`pipeline_defs/kj-cinematic.yaml`](../pipeline_defs/kj-cinematic.yaml)（在 `script` 與 `scene_plan` 間加入 `clp` 階段，產出 `clp_manifest`）。
  - Schema：`schemas/artifacts/clp_manifest.schema.json`；`schemas/artifacts/scene_plan.schema.json` 擴充 `render_stages`（枚舉 `T2I/I2I/R2I/W2I/T2V/I2V/R2V/W2V`）。
  - Checkpoint／Backlot：`lib/checkpoint.py` 與 `backlot/state.py` 已註冊 `clp` 階段與 `clp_manifest.json`、支援中途切入專案並由 `artifacts/` 自動推導看板階段完成狀態；`backlot/ui/board.js` 支援小數點分鏡號 `shot_2.1.1` 顯示；新增毛片預覽器 `backlot/ui/player.html`＋`player.js`（由看板右下角 `🎬 Scene Player` 開啟，支援專案／幕／場篩選、對白音檔 vs 影片原音、圖像 vs 影片、分鏡圖 vs Camera 視角圖／並排對照及評鑑資訊面板；2026-10-16 A1～A5、B1～B5 全數完成）。
  - Skills：`skills/pipelines/kj-cinematic/clp-director.md`、`scene-director.md`（含對白逐字忠於原稿、動作括號拆離對白、`shot_2.1.1` 編號規範，以及 `cam_<主體>_<景別縮寫>_<角度>[_<6種型式末綴>]` 鏡頭命名與無模型／有模型選鏡規則）、`asset-director.md`（音訊先行統一存 `assets/audio/` 並登記於 `asset_manifest.json`、預錄採 `shot_<編號>.<格式>`／TTS 採 `shot_<編號>_<來源>_v<版本號>.<格式>`＋4.1 圖片版本與採用規範＋同機位 `_empty_*`／`_block_*` 配對規則）與 `prompt-recipes.md`（由 `scripts/read_prompt_recipe.py <模態>` 按章節讀取；`T2V/I2V/R2V/W2V` 強制於 Prompt 正文明寫 `影片長度 [N] 秒`）。
  - 自訂風格：`styles/custom/kj-esg-pixar-hybrid.yaml`、`kj-pixar-fairytale.yaml`、`kj-vox-paper-collage.yaml`。
- **Google 模型（固定預設 Vertex AI＋`GOOGLE_APPLICATION_CREDENTIALS` 服務帳戶 JSON，不 fallback API key）**：
  - **圖片（`google_imagen`）**：`gemini-3*` 與 `gemini-nano-banana-2.1` 自動走 `global`；支援 `generation_mode="edit"`、`1K/2K/4K`、`thinking_level`（`MINIMAL/MEDIUM/HIGH`）、15 種 `aspect_ratio`、最多 14 張 `image_paths` 及 `media_paths`（本機或 `gs://` 影片／PDF，已接通 `image_selector`／`provider_routing` 過濾）與 `video_metadata`。
  - **影片（`gemini_omni_video`）**：預設 `gemini-omni-1.1-flash-preview`（`global` Interactions REST），支援整數 3–10 秒、360p/720p/1080p/4k、`reference_image_path(s)`、`last_image_path`、`reference_video_paths`、`input_video_path`、`edit_video`/`extend_video` 與 `previous_interaction_id`。`veo_video` 預設直接走 Google Vertex。
  - **語音（`gemini_tts`）**：預設 `gemini-3.8-flash-tts`（`global` `generateContent`），支援單人／雙人與逐句 style，限定輸出 `.wav`（24kHz/16-bit/單聲道）。舊 `google_tts` 同樣使用 JSON 憑證。
- **MiniMax 語音（`minimax_tts`）**：連接國際版 `https://api.minimax.io/v1/`，預設 `speech-2.6-hd`（讀 `MINIMAX_API_KEY`），輸出 32kHz 單聲道 WAV／MP3。`config/minimax_voice_baselines.json` 保存 7 角色人工校準 baseline（`wang/chen/linda/li/george/amy/biao`），呼叫 `tts_selector` 帶 `voice_baseline="amy"` 即自動路由並帶入 Voice ID 與語速。

## 專案製作進度摘要（詳見 [`docs/kj-lean-history.md`](kj-lean-history.md)）
- **`course-51-esg`**：
  - 全五幕劇本（220 分鏡／1,631.62 秒真實錄音校準，台詞已逐字對齊 `master_script.md` 並拆離動作括號）、`artifacts/clp_manifest.json`（34 件角色／場景／道具，含 `char_analyst2`）、分鏡／圖檔編號已全面統一為小數點格式（如 `shot_2.1.1`），且 218 個預錄對白音檔已統一移入 `assets/audio/shot_X.Y.Z.mp3` 並全數登記於 `artifacts/asset_manifest.json`（全數通過 schema 驗證）。
  - 已建置 8 組 Blender 場景包（`references/scenes/` 下的 `coffee_shop`、`investment_office`、`admin_office`、`marketing_department`、`factory_affairs`、`it_department`、`procurement_department`、`rd_department`），並將 8 場之人物白模全面統一至最新標準（單一集合 `07_PEOPLE_BLOCKS`、物件命名 `CHAR_<ID> | <部位>`、圓頭＋圓鼻朝向＋髮蓋／安全帽＋長方體四肢＋三代表色：對談角色藍 `#1F5CE6`、主角紅 `#DE131B`、第三人灰 `#7A8086`＋膚色 `#D9A17C`）；`rd_department` 亦已改裝為「紡織材料供應商研發室（rPET 再生聚酯高分子／機能纖維實驗室）」（配置灰綠環保毛毯卷、機能布試片疊、回收寶特瓶、rPET 酯粒／瓶片／母粒透明樣品罐、精密電子天平、桌上型熔融／含水率分析儀、加熱磁力攪拌器、原絲捲與 3 層儲料架），將 `CHAR_AMY`／`CHAR_CHEN` 移至中島實驗桌前對談；全 8 場共 89 顆鏡頭（`investment_office` 12 鏡、`coffee_shop` 9 鏡、`factory_affairs` 10 鏡、`marketing_department` 18 鏡、`admin_office` 11 鏡、`it_department` 8 鏡、`procurement_department` 9 鏡、`rd_department` 12 鏡）之正式 `cameras/*_block_blender.png` 與 `_empty_blender.png` 已重算完成。
  - `artifacts/scene_plan.json` 已完成全五幕（220 劇本段落／222 分鏡條目，含 `shot_4.3.4a/b/c`）完整更新與驗證，全面對應 8 個場景之 `cameras/` 機位（有人物鏡選 `_block_blender.png`、無人物特寫／環境鏡選 `_empty_blender.png`）與 34 件 `clp_manifest.json` 實體；場景 2.1（咖啡館六鏡 `shot_2.1.1`～`2.1.6`）已完成多輪 GPT／Nano Banana 2.1 生成，採用版本登記於 `artifacts/asset_manifest.json`，全部 46 張試圖索引於 `artifacts/image_generation_history.md`。
- **`fairytale-01-frog-and-scorpion`**：以 `kj-cinematic` 完成 Gemini 3.8 TTS 旁白（`assets/audio/shot_1.1.1_gemini_v1.wav`～`1.1.4`）、CLP 3 實體（`artifacts/clp_manifest.json`）、4 張皮克斯分鏡圖（`assets/images/shot_1.1.1_native_v1.jpg`～`1.1.4`），全數對齊統一編號／命名規則並通過 6 項 artifact schema 驗證，完成 FFmpeg 平滑版與 HyperFrames 成品版（`renders/frog_and_scorpion_hyperframes.mp4`，1080p/30fps/40.1s，含右側常駐階梯式磨砂字幕欄）。
- **`fairytale-02-mole-stargazer`**：自 `archive/complex-v1` 還原並升級 8 項 `artifacts/*.json`（`shot_1.1.1`～`1.1.5` 共 5 鏡），對齊統一命名（`shot_1.1.X_edgetts_v1.mp3`、`shot_1.1.X_banana_v1.png`、`shot_1.1.X_ffmpeg_v1.mp4`），支援 Scene Player 圖像與影片雙模式預覽。
- **`course-31-pdca`**：自 `archive/complex-v1` 合併還原第 2～6 幕共 7 章節、**143 鏡**（`shot_2.1.1`～`shot_6.3.4`）至根目錄 `artifacts/`，並將 143 組音檔、縮圖、Vox 剪紙影片對齊至 `assets/{audio,images,videos}/shot_X.Y.Z_<source>_v1.<ext>`（共 429 件媒體資產），支援 Scene Player 跨幕／跨場篩選及圖像／影片預覽。
- **`client-01-foxconn-core-values`**：自 `archive/complex-v1` 還原 5 項 `artifacts/*.json`（含 `script.json` 20 段劇本與 `clp_manifest.json` 16 件 CLP 資產，尚未進入 `scene_plan` 分鏡階段）。

## 踩過的坑（核心結論）
- **Blender 場景與白模**：原檔多為 Workbench，切 Cycles 才顯示材質；本機 RTX 3050 Laptop GPU 搭配 Blender 5.2.2 LTS 時，Cycles GPU 須指定 `CUDA`（`OPTIX` 會因 `optix.ptx.copysign.f32` 編譯失敗報錯）；開啟子集合人物（如 `12 v008...`）須同時確認母集合 `07 People` 未設 `hide_render`；若 `LayerCollection` 設為 `exclude=True` 或 `hide_viewport=True`，Blender 不會計算其子物件的 `matrix_world`（回傳單位矩陣 `Identity(4)`），解開父子關係或讀世界座標前務必先將該 `LayerCollection` 取消隱藏並呼叫 `view_layer.update()`。全景檢查需暫時解除 timeline camera marker 綁定。多影格關鍵影格綁定不同姿勢時，須先 `scene.frame_set(f)` 再設定物件姿態與 `keyframe_insert`，否則 `frame_set` 會先依既有 F-Curve 插值覆寫剛擺好的姿態；局部旋轉若物件帶 `rz=180°` 會翻轉局部 X 軸，後仰／轉頭一律以世界座標軸（`rotate_world_axis`）計算。修改道具／鋼架尺度須以模型公尺實測並重貼掛板、檢查前後排深度與覆蓋率。
- **W2I／R2I 生圖與構圖控制**：
  - W2I 唯一模板採「參考圖說明 → 生圖指引 → 單段畫面描述 → 輸出」，圖片固定按「場景 → blocks → 人物 → 道具」排序；以 blocks 為編輯底圖鎖定取景與佔位，場景圖僅供材質與光影，指定表演合併進畫面描述，不寫與 blocks 矛盾的指令。
  - **視角劫持（View Hijacking）**：特寫／過肩鏡只傳與本鏡朝向一致的場景參考圖，勿傳反向全局圖以免整間店旋轉 90 度。
  - **空椅入座（Occupy vs Spawn）**：I2I／W2I 置入人物寫「直接坐入既有木椅（入座佔用，不額外加椅）」，避免寫「保留所有桌椅」導致雙胞椅。
  - **驗收紀律**：AI 生成圖常有頭部放大、頭頂留白減少或局部配件增減，須逐張看圖驗收，不能僅因文字規則齊全或檔案存在就判定通過。
- **Schema 與 Manifest 規範**：`scene_plan` 與 `asset_manifest` 的項目皆為 `additionalProperties: false`；CLP 標註放 `required_assets[].clp_id` 與 `character_actions[].character_id`，manifest 記於 `generation_summary` 開頭（`clp: ... | ...`）。選填 `lens_mm` 若枚舉無實值則省略並記於描述。未知模型／費用省略不填 0。
- **Google／MiniMax API 細節**：
  - Nano Banana Pro／2.1 不支援 `negative_prompt`（改寫 `Avoid: ...`）；2K 回應含 `thought=true` 的 1376×768 草圖，adapter 已自動略過並取正式圖；費用保持 `unquoted`。
  - Omni 1.1 遇 HTTP 400 時須看回應本文區分參數錯誤與 `prohibited_content`（知名人物過濾，動畫圖亦可能觸發）。
  - MiniMax `emotion` 僅接受 9 種列舉值（無 `Neutral`），`<#0.4#>` 停頓原樣傳送；`output_format="hex"` 為傳輸編碼，WAV／MP3 設於 `audio_setting.format`。
- **Windows 與合成環境**：
  - PowerShell 勿用 `python -c` 塞複雜引號，改寫入 `.tmp/*.py` 並先設 `$env:PYTHONPATH=(pwd).Path; $env:PYTHONIOENCODING="utf-8"`。獨立腳本讀 `.env` 需先 `load_dotenv()`。
  - Windows 登錄檔易將 `.js` 誤設為 `text/plain` 致 Backlot 黑畫面，已在 `backlot/server.py` 強制設定 MIME。
  - FFmpeg 單圖 Ken Burns 禁止在 `zoompan` 前加 `-loop 1`，須先升 4K（3840×2160）超採樣再縮回 1080p/30fps 消除抖動。

## 下一步候選（使用者決定順序）
1. `projects/kj-om-openMontage修改意見.md` 與評估報告之 A1～A5、B1～B5（含 Scene Player 毛片預覽器）已於 2026-10-16 全數完成。
2. 評估是否推進 `course-51-esg` 場景 4.5／4.6 或投資辦公室（Act 01）之分鏡生圖／生影片。
3. 從 `team-main` 搬回 `pixar-course` pipeline（在 `gemini/pixar-course-pipeline` 分支）。
