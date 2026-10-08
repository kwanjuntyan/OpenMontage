# Asset Director - kj-cinematic Pipeline

**先完整閱讀並遵循 `skills/pipelines/cinematic/asset-director.md`**，再套用以下 CLP 規則。

## CLP 規則

輸入多了 `state.artifacts["clp"]["clp_manifest"]`。對每個 scene，從 `required_assets` 裡 `type: "clp"` 的項目取得 `clp_id`，查出該 entity 的 `reference_images`（路徑相對於專案資料夾）。

1. **生圖**（`image_selector`）：把參考圖放進 `image_urls`，並選支援參考圖的 provider（例如 `openai_image`、`atlas_image`、`kling_official_image`）。`google_imagen` 不支援參考圖，有 CLP 的鏡頭不要用它。
2. **生影片**（`video_selector`）：把參考圖放進 `reference_image_paths`，並選支援參考圖的 provider（例如 `kling_official_video`、`gemini_omni_video`、`atlas_video`、`grok_video`）。若該鏡頭已先產生首幀圖，改用首幀圖做 image-to-video。
3. **Prompt 寫法**：
   - 開頭用 style 的 `image_prompt_prefix`。
   - 用名稱指稱 CLP 並對應參考圖，例如 `Amy (see reference image 1) in the boardroom (reference image 2)`。
   - **不要重新描述外觀**，只寫動作、表情、構圖、鏡頭運動、光線。
4. **一個鏡頭最多帶 3 張參考圖**（角色優先，其次場景，再來道具），避免模型混淆。
5. 在 `asset_manifest` 每個資產的 `generation_summary` 開頭記錄用到的 CLP，格式 `clp: amy, london_boardroom | ...`，方便之後重產。（asset 項目不允許自訂欄位，不要加 `clp_ids`。）
