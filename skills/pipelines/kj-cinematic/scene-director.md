# Scene Director - kj-cinematic Pipeline

**先完整閱讀並遵循 `skills/pipelines/cinematic/scene-director.md`**，再套用以下 CLP 規則。

## CLP 規則

輸入多了 `state.artifacts["clp"]["clp_manifest"]`。

1. **每個鏡頭標註用到的 CLP。** 在 scene 的 `required_assets` 加入（scene_plan schema 允許這個欄位帶額外屬性）：
   ```json
   {"type": "clp", "description": "amy", "source": "provided", "clp_id": "amy"}
   ```
   角色有表演時，`character_actions[].character_id` 也用同一個 CLP id。
2. **`description` 不重寫 CLP 的外觀。** 寫動作、表情、構圖、鏡頭、光線、情緒；Asset Director 看圖後可補精簡的可見特徵，不能臆造外觀。
   - ✅ `amy 在 london_boardroom 起身，握緊報告，鏡頭由中景推近到特寫`
   - ❌ `一位穿深藍色西裝、棕色短髮的女性在玻璃會議室起身…`
3. **劇本出現但 clp_manifest 沒有的重要角色或場景**：停下來告訴使用者，建議回到 clp stage 補上，不要自行描述外觀。

## 視覺工序規劃

- 需生成的鏡頭使用既有 `render_stages` 表達順序，如 `["R2I"]` 或 `["W2I", "W2V"]`；八類定義見 `skills/pipelines/kj-cinematic/prompt-recipes.md`。沿用現成素材時不必補生成階段。
- `description` 補人物所在位置、拍攝朝向與可見背景，將場景 CLP 的佈景對應到白模取景；位置不明先釐清，不杜撰「窗邊」或新格局。
- 白模圖沿用 `required_assets` 的 `type: "camera_ref"`、`role: "first_frame_ref"`，影片用 `type: "camera_video_ref"`、`role: "motion_ref"`；每項保留 `description`、`source` 與實際 `path`。
- 尚待製作的白模標明 `source: "generate"` 與需求，不虛填已存在路徑。W2V 需可用預演影片；必要素材未就緒時 Asset Director 回報缺件。
- 鏡外對話者可出現在表演的視線目標，但不因此要求人物進入畫面或附其 CLP 圖。單人鏡頭需明寫可見人數。
- scene_plan 只保留製作意圖與素材需求；不預填生成結果、核准紀錄或續作狀態。缺少／空的 `render_stages` 不使舊分鏡失效。

## 鏡頭命名與選用規則

1. **鏡頭基底名稱語法（彈性數量、固定槽位）**：
   - 格式：**`cam_<主體>_<景別縮寫>_<角度或修飾>`**（不綁 `s01` 流水號，各場景依實際需求彈性配置鏡頭數量）。
   - `<主體>`：多人用 `twoshot`／`threeshot`；單人用角色短名（如 `amy`、`george`、`li`、`biao`）；物件或環境用區域／道具名（如 `table`、`whiteboard`、`poster`、`window_bar`）。
   - `<景別縮寫>`：`wide`（全景 24–35mm）、`mws`（全身／中全景 38–42mm）、`ms`（中景／腰上含手勢 45–55mm）、`mcu`（中特寫／胸上 60–75mm）、`cu`（臉部特寫 85–100mm）、`ots`（過肩 50–80mm，**被拍主體放第 2 欄 `<主體>`、前景肩膀角色放第 4 欄**，如 `cam_george_ots_amy`；若同組過肩有不同景別可加尾綴如 `cam_amy_ots_li_ms`／`cam_amy_ots_li_cu`）、`insert`（細節插鏡 50–65mm）、`ambience`（環境空鏡 28–35mm）。
   - `<角度或修飾>`：水平 `front`／`15deg`／`45deg`／`profile`；垂直或構圖 `level`／`low_angle`／`high_bird`／`top`／`iso`；特殊 `selfie`／`emotion`；或 `ots` 的前景角色名。
2. **無參考模型 vs 有參考模型的選鏡規則**：
   - **未指明參考 3D 模型**：必須從標準對話基礎鏡位組合選用（`cam_twoshot_wide_level`、`cam_twoshot_ms_level`、`cam_twoshot_ms_profile`、`cam_twoshot_wide_high_bird`、`cam_<a>_ots_<b>`、`cam_<a>_ms_15deg`、`cam_<a>_mcu_15deg`、`cam_<a>_mcu_45deg`、`cam_<a>_cu_emotion`、`cam_<a>_ms_low_angle`、`cam_<prop>_insert_top`、`cam_<prop>_insert_iso`、`cam_<zone>_ambience_front`），將 `<a/b>` 代換為該場角色短名寫入 `scene_plan`。
   - **有指明參考 3D 模型**：設計前先盤點 `references/scenes/<location>/cameras/` 現有角度圖，**必須採用該模型附屬的既有角度圖機位**；若缺必要機位，標明 `source: "generate"` 並回報補圖，不虛填不存在的路徑。
3. **角度圖 6 種型式末綴與存放位置**：
   - 各模型的所有角度圖統一存放於 `references/scenes/<location>/cameras/`，檔名為 **`cam_<主體>_<景別縮寫>_<角度或修飾>_<型式末綴>.png`**；`references/scenes/<location>/renders/` 僅留給場景全景測試、材質驗證或過程歸檔（`renders/archive/`），禁止放置分鏡機位圖。
   - 6 種型式末綴：`empty_blender`、`empty_gpt`、`empty_banana`（無人物空景圖）；`block_blender`、`block_gpt`、`block_banana`（附人物定位圖）。
   - `scene_plan.json` 的 `camera_ref.path` 統一指向 `references/scenes/<location>/cameras/<鏡頭基底名稱>_block_blender.png`。

## 對白與動作分離規則

1. **台詞不可加油添醋。** `character_actions[].dialogue`（及上游 `script.json` 的台詞 `sections[].text`）必須逐字忠於核准劇本原詞，嚴禁自行改寫、擴寫或潤飾詞句。
2. **括號動作歸入畫面描述，不放對白。** 劇本括號內的舞台指示、動作、表情或道具標記（如 `（放下手中的咖啡杯，溫和地微笑。）`、`（@Coffee_Cup）`）必須拆入 `description`（畫面提示詞）、`character_actions[].action_sequence` 或 `speaker_directions`，`dialogue` 與台詞 `text` 只保留角色實際開口說出的台詞。
3. **分鏡編號格式。** 多層次分鏡 ID 統一以小數點分隔（如 `shot_2.1.1`），不以底線分隔數字。
