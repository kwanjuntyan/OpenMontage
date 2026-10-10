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
