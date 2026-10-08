# Scene Director - kj-cinematic Pipeline

**先完整閱讀並遵循 `skills/pipelines/cinematic/scene-director.md`**，再套用以下 CLP 規則。

## CLP 規則

輸入多了 `state.artifacts["clp"]["clp_manifest"]`。

1. **每個鏡頭標註用到的 CLP。** 在 scene 的 `required_assets` 加入（scene_plan schema 允許這個欄位帶額外屬性）：
   ```json
   {"type": "clp", "description": "amy", "source": "provided", "clp_id": "amy"}
   ```
   角色有表演時，`character_actions[].character_id` 也用同一個 CLP id。
2. **`description` 不再描述 CLP 的外觀。** 只寫動作、表情、構圖、鏡頭、光線、情緒。外觀由參考圖鎖定；文字和圖不一致時，模型會混淆。
   - ✅ `amy 在 london_boardroom 起身，握緊報告，鏡頭由中景推近到特寫`
   - ❌ `一位穿深藍色西裝、棕色短髮的女性在玻璃會議室起身…`
3. **劇本出現但 clp_manifest 沒有的重要角色或場景**：停下來告訴使用者，建議回到 clp stage 補上，不要自行描述外觀。
