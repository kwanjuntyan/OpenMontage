# CLP Director - kj-cinematic Pipeline

## 何時使用

script 核准後、scene_plan 之前。建立 Character／Location／Prop（CLP）參考圖，讓後續每個鏡頭的人物、場景、道具保持一致。
產出：`clp_manifest`（`schemas/artifacts/clp_manifest.schema.json`）。檔案放在 `projects/<project>/clp/`。

## 步驟 1：從劇本建議清單 → 等使用者核准

讀 `state.artifacts["script"]["script"]`，列出**重複出現或畫面關鍵**的角色、場景、道具，用表格給使用者：

| id | 類型 | 名稱 | 出現段落（section id） | 視覺描述 |
|---|---|---|---|---|

- `id` 用小寫英數與底線（`amy`、`london_boardroom`），之後 scene_plan 和 prompt 都用這個 id。
- 只出現一次、不需一致性的背景物件不要列。
- **使用者核准（可增刪改）之前，不要產生任何圖片。**

## 步驟 2：取得參考圖（每個 entity 二選一）

### A. 產生新圖（`source: "generated"`）
用 `image_selector` 產生，prompt 由三層組成：

```
{style 的 image_prompt_prefix} + {類型模版} + {entity 描述}
negative: {style 的 image_negative_prompt}
```

| 類型 | 模版 |
|---|---|
| character | character reference sheet, front / three-quarter / side / back views, full body, neutral pose, plain light-grey background, consistent outfit |
| location | wide establishing shot, empty of people, clear layout, natural lighting matching the mood |
| prop | single object, three-quarter view, plain neutral background, soft studio light |

- style 用 proposal 選定的 playbook（例如 `kj-esg-pixar-hybrid`），用 `styles/playbook_loader.load_playbook()` 讀取。
- 把完整 prompt 存進 `prompt_used`，之後可以重產。
- 每個 entity 給使用者看圖，不滿意就改描述重產。

### B. 匯入現成圖（`source: "imported"`）
使用者提供圖檔或資料夾時：
1. 複製到 `projects/<project>/clp/`，檔名用 `{id}.{ext}`（多張用 `{id}_2` 等）。
2. **直接看圖**，改寫 `description`：外型、髮型、服裝、配色、材質、比例。描述要以圖為準，不要沿用劇本裡互相矛盾的文字。
3. 使用者若另有文字設定檔（例如角色設定 .md），與圖片描述合併；衝突時以圖片為準，並告知使用者。

## 步驟 3：寫出 clp_manifest

```json
{"version": "1.0", "style_playbook": "kj-esg-pixar-hybrid",
 "entities": [{"id": "amy", "type": "character", "name": "Amy",
   "description": "...", "reference_images": ["clp/amy.png"],
   "source": "generated", "appears_in": ["s1", "s3"], "prompt_used": "..."}]}
```

`reference_images` 是相對於專案資料夾的路徑，第一張是主參考圖。完成後交給使用者核准（checkpoint 的 human approval）。
