# CLP Director - kj-cinematic Pipeline

## 何時使用

script 核准後、scene_plan 之前，或既有專案局部增修 CLP 資產時。建立與維護 Character／Location／Prop（CLP）參考圖與特徵描述，讓後續每個鏡頭的人物、場景、道具保持一致。
- **新專案建置**：依序執行功能 1 → 功能 2 → 功能 3。
- **既有專案局部增修**：可依需求單獨呼叫任一功能（例如放入新圖後，直接執行功能 3 看實圖更新 `clp_manifest.json`）。

產出：`clp_manifest`（`schemas/artifacts/clp_manifest.schema.json`）。圖檔放在 `projects/<project>/clp/`。

## 功能 1：從劇本萃取 CLP 清單（等使用者核准）

讀 `state.artifacts["script"]["script"]`，列出**重複出現或畫面關鍵**的角色、場景、道具，用表格給使用者：

| id | 類型 | 名稱 | 出現段落（section id） | 視覺描述 |
|---|---|---|---|---|

- `id` 用小寫英數與底線（`amy`、`london_boardroom`），之後 scene_plan 和 prompt 都用這個 id。
- 只出現一次、不需一致性的背景物件不要列。
- **使用者核准（可增刪改）之前，不要產生任何圖片。**

## 功能 2：取得基準參考圖（每個 entity 二選一）

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
使用者提供圖檔或資料夾時，複製到 `projects/<project>/clp/`，檔名統一用 `{id}.{ext}`（同一 entity 有多張角度圖時用 `{id}_2.{ext}` 等）。

## 功能 3：看實圖撰寫描述詞並更新 clp_manifest

- 生成（2A）與匯入（2B）的參考圖都先**直接看最終實圖**，將 `description`（外型、髮型、服裝、配色、材質、比例）整理成可獨立摘錄的簡短正向特徵句，以分號或句號分隔；描述一律以實圖為準，不能直接把生圖用的 `prompt_used` 或劇本裡與實圖矛盾的文字當成描述。若另有文字設定檔（如角色設定 `.md`）可一併合併，衝突時以實圖為準並告知使用者。
- 人物記穩定外觀、服裝與辨識特徵，道具記形狀／材質；動作、表情、視線及鏡位留給分鏡，不寫成共用設定。
- 場景記佈景結構、物件關係與材質，例如「窗邊座位」，不用依賴照片視角的「吧台在右側」；不確定的方位、遮蔽區域或材質不臆補。
- 多張參考圖需核對描述所指區域；不同視角未顯示某物件，不等於該物件不存在。實圖互相矛盾時回報，不拼湊成新格局。

```json
{"version": "1.0", "style_playbook": "kj-esg-pixar-hybrid",
 "entities": [{"id": "amy", "type": "character", "name": "Amy",
   "description": "...", "reference_images": ["clp/amy.png"],
   "source": "generated", "appears_in": ["s1", "s3"], "prompt_used": "..."}]}
```

`reference_images` 是相對於專案資料夾的路徑，第一張是主參考圖。完成後交給使用者核准（checkpoint 的 human approval）。
