# 圖片生成歷史｜course-51-esg

2026-10-13：依 Asset Director 4.1 建立統一入口。後續所有 shot／模型的新生成紀錄追加於本檔；生成成功不等於確認採用。

## 既有紀錄與修復範圍

- 盤點 2.1.1～2.1.6 的 44 張現存分鏡圖片，另將兩張已記錄的 Banana v1 從 OM `.tmp/` 原樣複製至 `assets/images/`，合計 46 張。既有檔名、圖片內容與採用指向保留；場景包與 CLP 沿用其參考素材目錄。
- [短指令歷史](shot_prompts_2_1.md)及[Banana／GPT 比較歷史](shot_prompts_2_1_banana21.md)原文保留。下表逐版本連結原紀錄，並標示行號；原紀錄含完整 prompt、有序參考圖、檢視與費用說明。11 份被後續版本覆蓋的 prompt 與實際圖序已從原始請求補回本檔，不以目前章節開頭的 prompt 推定所有舊版本。
- 下表檔名包含 shot、生成來源與版本，完整專案相對路徑為 `assets/images/<檔名>`；無版本號的五張 JPG 曾是整理時的 manifest 指向，版本未知，不改名也不推定為 v1。所有生成版本的 id 可由檔名去掉副檔名識別；manifest 沿用既有 id。
- 下表「manifest 現行」為使用者於本次對話明確指定的六張採用圖片；五張舊 JPG 已由指定版本替換，其他圖片繼續保留。原檢視紀錄保留，採用不等於撤回其中記載的差異；選版依使用者指示，不以最大版本號推定。
- 五張 manifest JPG 的實際尺寸均為 `1376x768`，已修正原 `1792x1008`。未查到實際費用依據，移除五筆 `cost_usd=0.0` 與 `total_cost_usd=0.0`；費用未知，不代表免費。未改素材 id、path、prompt 或 source_tool。
- 本專案未找到 checkpoint／partial_progress，因此無既有路徑可同步；本次為資料修復，不代表 assets 階段完成。

## 工具與模型

| 下表代號 | 工具／供應商／模型 | 費用 |
|---|---|---|
| B | image_selector → google_imagen／Google Vertex AI／gemini-nano-banana-2.1；服務帳戶 JSON、global、edit、2K、16:9 | 實際費用未核帳；原紀錄所列金額均為估計 |
| G | 內建 image_gen／OpenAI；確切模型未提供 | 未提供 |
| L | manifest 原記錄 agent_native_image；供應商與確切模型未確認 | 未知；原零值已移除 |

## 版本索引

| shot | 圖片檔名 | 工具 | prompt／參考圖與生成紀錄 | 採用狀態 |
|---|---|---|---|---|
| 2.1.1 | [shot_2.1.1.jpg](../assets/images/shot_2.1.1.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.1 | [shot_2.1.1_banana21_v1.png](../assets/images/shot_2.1.1_banana21_v1.png) | B | [補回原請求](#shot_2.1.1_banana21_v1) | 保留版本 |
| 2.1.1 | [shot_2.1.1_banana21_v2.png](../assets/images/shot_2.1.1_banana21_v2.png) | B | [補回原請求](#shot_2.1.1_banana21_v2) | 保留版本 |
| 2.1.1 | [shot_2.1.1_banana21_v3.png](../assets/images/shot_2.1.1_banana21_v3.png) | B | [原紀錄第 28 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2.1.1_banana21_v4.png](../assets/images/shot_2.1.1_banana21_v4.png) | B | [原紀錄第 55 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2.1.1_banana21_v5.png](../assets/images/shot_2.1.1_banana21_v5.png) | B | [原紀錄第 84 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2.1.1_banana21_v6.png](../assets/images/shot_2.1.1_banana21_v6.png) | B | [原紀錄第 137 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2.1.1_gpt_template_v1.png](../assets/images/shot_2.1.1_gpt_template_v1.png) | G | [原紀錄第 30 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2.1.1_gpt_template_v2.png](../assets/images/shot_2.1.1_gpt_template_v2.png) | G | [原紀錄第 57 行](shot_prompts_2_1_banana21.md#211) | manifest 現行 |
| 2.1.1 | [shot_2.1.1_gpt_template_v3.png](../assets/images/shot_2.1.1_gpt_template_v3.png) | G | [原紀錄第 112 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2.1.1_short_v1.png](../assets/images/shot_2.1.1_short_v1.png) | G | [原紀錄第 24 行](shot_prompts_2_1.md#211amy-求救s02_medium_two_shot40mm) | 保留版本 |
| 2.1.2 | [shot_2.1.2.jpg](../assets/images/shot_2.1.2.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.2 | [shot_2.1.2_banana21_v1.png](../assets/images/shot_2.1.2_banana21_v1.png) | B | [補回原請求](#shot_2.1.2_banana21_v1) | 保留版本 |
| 2.1.2 | [shot_2.1.2_banana21_v2.png](../assets/images/shot_2.1.2_banana21_v2.png) | B | [原紀錄第 155 行](shot_prompts_2_1_banana21.md#212) | 保留版本 |
| 2.1.2 | [shot_2.1.2_banana21_v3.png](../assets/images/shot_2.1.2_banana21_v3.png) | B | [原紀錄第 185 行](shot_prompts_2_1_banana21.md#212) | 保留版本 |
| 2.1.2 | [shot_2.1.2_banana21_v4.png](../assets/images/shot_2.1.2_banana21_v4.png) | B | [原紀錄第 213 行](shot_prompts_2_1_banana21.md#212) | 保留版本 |
| 2.1.2 | [shot_2.1.2_gpt_template_v1.png](../assets/images/shot_2.1.2_gpt_template_v1.png) | G | [原紀錄第 157 行](shot_prompts_2_1_banana21.md#212) | manifest 現行 |
| 2.1.2 | [shot_2.1.2_short_v1.png](../assets/images/shot_2.1.2_short_v1.png) | G | [原紀錄第 37 行](shot_prompts_2_1.md#212amy-訴苦s06_amy_medium_close_up65mm) | 保留版本 |
| 2.1.3 | [shot_2.1.3.jpg](../assets/images/shot_2.1.3.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.3 | [shot_2.1.3_banana21_v1.png](../assets/images/shot_2.1.3_banana21_v1.png) | B | [補回原請求](#shot_2.1.3_banana21_v1) | 保留版本 |
| 2.1.3 | [shot_2.1.3_banana21_v2.png](../assets/images/shot_2.1.3_banana21_v2.png) | B | [補回原請求](#shot_2.1.3_banana21_v2) | 保留版本 |
| 2.1.3 | [shot_2.1.3_banana21_v3.png](../assets/images/shot_2.1.3_banana21_v3.png) | B | [補回原請求](#shot_2.1.3_banana21_v3) | 保留版本 |
| 2.1.3 | [shot_2.1.3_banana21_v4.png](../assets/images/shot_2.1.3_banana21_v4.png) | B | [原紀錄第 237 行](shot_prompts_2_1_banana21.md#213) | 保留版本 |
| 2.1.3 | [shot_2.1.3_banana21_v5.png](../assets/images/shot_2.1.3_banana21_v5.png) | B | [原紀錄第 270 行](shot_prompts_2_1_banana21.md#213) | 保留版本 |
| 2.1.3 | [shot_2.1.3_gpt_template_v1.png](../assets/images/shot_2.1.3_gpt_template_v1.png) | G | [原紀錄第 264 行](shot_prompts_2_1_banana21.md#213) | 保留版本 |
| 2.1.3 | [shot_2.1.3_short_v1.png](../assets/images/shot_2.1.3_short_v1.png) | G | [原紀錄第 51 行](shot_prompts_2_1.md#213george-解惑s03_ots_to_george60mm) | manifest 現行 |
| 2.1.4 | [shot_2.1.4.jpg](../assets/images/shot_2.1.4.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.4 | [shot_2.1.4_banana21_v1.png](../assets/images/shot_2.1.4_banana21_v1.png) | B | [補回原請求](#shot_2.1.4_banana21_v1) | 保留版本 |
| 2.1.4 | [shot_2.1.4_banana21_v2.png](../assets/images/shot_2.1.4_banana21_v2.png) | B | [補回原請求](#shot_2.1.4_banana21_v2) | 保留版本 |
| 2.1.4 | [shot_2.1.4_banana21_v4.png](../assets/images/shot_2.1.4_banana21_v4.png) | B | [原紀錄第 383 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2.1.4_gpt_template_v1.png](../assets/images/shot_2.1.4_gpt_template_v1.png) | G | [原紀錄第 318 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2.1.4_gpt_template_v2.png](../assets/images/shot_2.1.4_gpt_template_v2.png) | G | [原紀錄第 343 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2.1.4_gpt_template_v3.png](../assets/images/shot_2.1.4_gpt_template_v3.png) | G | [原紀錄第 378 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2.1.4_short_v1.png](../assets/images/shot_2.1.4_short_v1.png) | G | [原紀錄第 63 行](shot_prompts_2_1.md#214amy-反問s08_amy_close_up100mm) | 保留版本 |
| 2.1.4 | [shot_2.1.4_short_v2.png](../assets/images/shot_2.1.4_short_v2.png) | G | [原紀錄第 68 行](shot_prompts_2_1.md#214amy-反問s08_amy_close_up100mm) | manifest 現行 |
| 2.1.5 | [shot_2.1.5.jpg](../assets/images/shot_2.1.5.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.5 | [shot_2.1.5_banana21_v1.png](../assets/images/shot_2.1.5_banana21_v1.png) | B | [補回原請求](#shot_2.1.5_banana21_v1) | 保留版本 |
| 2.1.5 | [shot_2.1.5_banana21_v2.png](../assets/images/shot_2.1.5_banana21_v2.png) | B | [原紀錄第 412 行](shot_prompts_2_1_banana21.md#215) | 保留版本 |
| 2.1.5 | [shot_2.1.5_gpt_compare_v1.png](../assets/images/shot_2.1.5_gpt_compare_v1.png) | G | [原紀錄第 414 行](shot_prompts_2_1_banana21.md#215) | 保留版本 |
| 2.1.5 | [shot_2.1.5_gpt_template_v1.png](../assets/images/shot_2.1.5_gpt_template_v1.png) | G | [原紀錄第 440 行](shot_prompts_2_1_banana21.md#215) | 保留版本 |
| 2.1.5 | [shot_2.1.5_short_v1.png](../assets/images/shot_2.1.5_short_v1.png) | G | [原紀錄第 84 行](shot_prompts_2_1.md#215george-講解-epss07_george_close_up100mm) | manifest 現行 |
| 2.1.6 | [shot_2.1.6_banana21_v1.png](../assets/images/shot_2.1.6_banana21_v1.png) | B | [原紀錄第 478 行](shot_prompts_2_1_banana21.md#216) | 保留版本 |
| 2.1.6 | [shot_2.1.6_gpt_template_v1.png](../assets/images/shot_2.1.6_gpt_template_v1.png) | G | [補回原請求](#shot_2.1.6_gpt_template_v1) | 保留版本 |
| 2.1.6 | [shot_2.1.6_gpt_template_v2.png](../assets/images/shot_2.1.6_gpt_template_v2.png) | G | [補回原請求](#shot_2.1.6_gpt_template_v2) | 保留版本 |
| 2.1.6 | [shot_2.1.6_gpt_template_v3.png](../assets/images/shot_2.1.6_gpt_template_v3.png) | G | [原紀錄第 476 行](shot_prompts_2_1_banana21.md#216) | 保留版本 |
| 2.1.6 | [shot_2.1.6_short_v1.png](../assets/images/shot_2.1.6_short_v1.png) | G | [原紀錄第 98 行](shot_prompts_2_1.md#216esg-概念轉折s09_table_insert50mm) | manifest 現行 |
| 4.6.1 | `shot_4.6.1_gpt_template_v1.png`（本機未留存） | G | [生成紀錄](#shot_4.6.1_gpt_template_v1) | 未留存副本（僅存紀錄） |
| 4.6.1 | `shot_4.6.1_gpt_template_v2.png`（本機未留存） | G | [生成紀錄](#shot_4.6.1_gpt_template_v2) | 未留存副本（僅存紀錄） |
| 4.6.1 | [shot_4.6.1_gpt_template_v3.png](../assets/images/shot_4.6.1_gpt_template_v3.png) | G | [生成紀錄](#shot_4.6.1_gpt_template_v3) | 保留版本（待確認） |
| 4.6.1 | [shot_4.6.1_gpt_template_v4.png](../assets/images/shot_4.6.1_gpt_template_v4.png) | G | [生成紀錄](#shot_4.6.1_gpt_template_v4) | 保留版本（待確認） |
| 4.6.1 | [shot_4.6.1_gpt_template_v5.png](../assets/images/shot_4.6.1_gpt_template_v5.png) | G | [生成紀錄](#shot_4.6.1_gpt_template_v5) | 保留版本（待確認） |
| 4.6.2 | [shot_4.6.2_gpt_template_v1.png](../assets/images/shot_4.6.2_gpt_template_v1.png) | G | [生成紀錄](#shot_4.6.2_gpt_template_v1) | 保留版本（待確認） |
| 4.6.2 | [shot_4.6.2_gpt_template_v2.png](../assets/images/shot_4.6.2_gpt_template_v2.png) | G | [生成紀錄](#shot_4.6.2_gpt_template_v2) | 保留版本（待確認） |
| 4.6.2 | [shot_4.6.2_gpt_template_v3.png](../assets/images/shot_4.6.2_gpt_template_v3.png) | G | [生成紀錄](#shot_4.6.2_gpt_template_v3) | 保留版本（待確認） |
| 4.6.3 | [shot_4.6.3_gpt_template_v1.png](../assets/images/shot_4.6.3_gpt_template_v1.png) | G | [生成紀錄](#shot_4.6.3_gpt_template_v1) | 保留版本（待確認） |

## 缺件與歷史例外

- 2.1.4 Banana v3 有兩次失敗嘗試，原紀錄保留 OAuth 逾時及未取得正式圖片的錯誤；沒有可歸檔的 v3 圖片，版本跳號保留，不補造圖片。
- 2.1.4 GPT 身體修正的第一次未採用試圖，僅記錄原生路徑 `C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-14593896-6b08-49d4-ba29-51194578b02d.png`，本機不存在；其完整 prompt 與唯一底圖仍見[原紀錄第 347 行](shot_prompts_2_1_banana21.md#214-gpt-身體朝向修正-v32026-10-13)。不以已歸檔的第二次結果冒充。
- 2.1.2 GPT template v1 實際附件為場景、blocks、George、Amy、杯碟／糖罐拼接圖，共五個檔案；prompt 內的圖 5／6 共用最後一張。`D:/kj-openMontage/.tmp/shot_2.1.2_props_5_6.png` 本機缺件，保留[原紀錄第 157 行](shot_prompts_2_1_banana21.md#212)的圖序與來源說明，不改記成 Banana 的六張獨立參考圖。
- 五張舊 JPG 的完整 prompt 與其他資料已保存在本檔「選版前的 manifest 快照」；工具原記錄與圖片尺寸可核對，但參考圖有序檔名、確切模型、實際費用缺乏可核實紀錄，明列未知，不用現行場景圖回填。
- 既有 `_short_`、`_gpt_template_`、`_gpt_compare_` 等檔名依 4.1 保留。後續同一 shot 使用穩定來源簡稱並接續該來源既有最大版本號；失敗且已有紀錄的版本號也保留，不重用。
- 舊紀錄中的 `.tmp/` 是當時請求／輸出位置。兩張已歸檔 Banana v1 的現行圖片位置以上表為準；原始請求不改寫，避免竄改當時實際輸入。

## 從原始請求補回的完整紀錄

以下均為既有生成，不是本次重生。圖片均連結至上方版本索引；參考圖依實際傳入順序列出，路徑轉為專案相對連結，prompt 原文保留。

### shot_2.1.1_banana21_v1

來源：OM `.tmp/banana21_six_short_1_result.json`；工具代號 B；實際費用未知。
原始用量：{"prompt_token_count": 5811, "candidates_token_count": 1680}；生成耗時 32.73 秒。

有序參考圖：

1. [references/scenes/coffee_shop/renders/blocks_blender_s02_medium_two_shot.png](../references/scenes/coffee_shop/renders/blocks_blender_s02_medium_two_shot.png)
2. [references/scenes/coffee_shop/cameras/empty_banana_s02_medium_two_shot.png](../references/scenes/coffee_shop/cameras/empty_banana_s02_medium_two_shot.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 prompt：

```text
圖 1 是人物定位 blocks；圖 2 是本鏡空景。圖 3 提供George 外觀與服裝。圖 4 提供Amy 外觀與服裝。圖 5 提供白色咖啡杯碟外觀。
背景與光影沿用圖 2；依圖 1 的人物位置、整體大小、朝向與遮擋置入角色，藍色為 George、紅色為 Amy。人物外觀及自身頭身比例依人物參考圖，不照搬展示姿態；表演依下段。人物坐入既有椅子。維持既有 3D 動畫風格、取景與暖色日光，輸出一張 16:9 彩色分鏡圖；不呈現方塊、參考圖展示排版或新增字幕。
Amy 愁眉微皺，一手握小匙、匙端仍在拿鐵中，抬眼望向 George 求助；George 沉著聆聽。保留雙人中景與桌面互動。
```

### shot_2.1.1_banana21_v2

來源：OM `.tmp/banana21_first_v2_result.json`；工具代號 B；實際費用未知。原紀錄估 US$0.059262，未核帳。
原始用量：{"prompt_token_count": 5908, "candidates_token_count": 1680}；生成耗時 35.11 秒。

有序參考圖：

1. [references/scenes/coffee_shop/renders/blocks_blender_s02_medium_two_shot.png](../references/scenes/coffee_shop/renders/blocks_blender_s02_medium_two_shot.png)
2. [references/scenes/coffee_shop/cameras/empty_banana_s02_medium_two_shot.png](../references/scenes/coffee_shop/cameras/empty_banana_s02_medium_two_shot.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 prompt：

```text
圖 1 是人物定位 blocks；圖 2 是本鏡空景，也是唯一的背景編輯底圖。圖 3 提供 George 外觀與服裝；圖 4 提供 Amy 外觀與服裝；圖 5 提供白色咖啡杯碟外觀。
直接在圖 2 中置入人物，保留其原取景、透視、家具位置、牆面掛畫、自然藤葉形狀與分布、材質及光影；不要重建背景。圖 1 只提供藍色 George、紅色 Amy 的人物佔位、整體大小、對坐朝向與遮擋，不採用圖 1 的背景、葉片或方塊材質。兩人坐入圖 2 既有椅子，人物頭頂高度、頭肩所在範圍與入座位置對齊圖 1；在這個佔位內依人物參考圖還原自然頭身比例，不放大人物或頭部、不改變鏡位與裁切。
Amy 愁眉微皺，一手握小匙、匙端仍在拿鐵中，抬眼望向 George 求助；George 沉著聆聽。肩膀與軀幹保持原本對坐朝向。只為這個表演調整表情、視線、手臂與原杯中飲品。維持雙人中景、既有 3D 動畫風格，輸出一張 16:9 彩色分鏡圖；不呈現方塊、展示排版或字幕。
```

### shot_2.1.2_banana21_v1

來源：OM `.tmp/banana21_six_short_2_result.json`；工具代號 B；實際費用未知。
原始用量：{"prompt_token_count": 4699, "candidates_token_count": 1680}；生成耗時 31.68 秒。

有序參考圖：

1. [references/scenes/coffee_shop/renders/blocks_blender_s06_amy_medium_close_up.png](../references/scenes/coffee_shop/renders/blocks_blender_s06_amy_medium_close_up.png)
2. [references/scenes/coffee_shop/cameras/empty_banana_s06_amy_medium_close_up.png](../references/scenes/coffee_shop/cameras/empty_banana_s06_amy_medium_close_up.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)

完整 prompt：

```text
圖 1 是人物定位 blocks；圖 2 是本鏡空景。圖 3 提供George 外觀與服裝。圖 4 提供Amy 外觀與服裝。
背景與光影沿用圖 2；依圖 1 的人物位置、整體大小、朝向與遮擋置入角色，藍色為 George、紅色為 Amy。人物外觀及自身頭身比例依人物參考圖，不照搬展示姿態；表演依下段。人物坐入既有椅子。維持既有 3D 動畫風格、取景與暖色日光，輸出一張 16:9 彩色分鏡圖；不呈現方塊、參考圖展示排版或新增字幕。
Amy 已停止攪拌，眉心皺起、嘴角下垂、頭微偏，望向 George 訴說 KPI 要 GG 的無奈；小幅攤手僅在原取景容納處呈現。George 只保留 圖 1 所示局部前景，不補出臉。
```

### shot_2.1.3_banana21_v1

來源：OM `.tmp/banana21_six_short_3_result.json`；工具代號 B；實際費用未知。
原始用量：{"prompt_token_count": 5823, "candidates_token_count": 1680, "thoughts_token_count": 1505}；生成耗時 38.87 秒。

有序參考圖：

1. [references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png](../references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png)
2. [references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png](../references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 prompt：

```text
圖 1 是人物定位 blocks；圖 2 是本鏡空景。圖 3 提供George 外觀與服裝。圖 4 提供Amy 外觀與服裝。圖 5 提供白色咖啡杯碟外觀。
背景與光影沿用圖 2；依圖 1 的人物位置、整體大小、朝向與遮擋置入角色，藍色為 George、紅色為 Amy。人物外觀及自身頭身比例依人物參考圖，不照搬展示姿態；表演依下段。人物坐入既有椅子。維持既有 3D 動畫風格、取景與暖色日光，輸出一張 16:9 彩色分鏡圖；不呈現方塊、參考圖展示排版或新增字幕。
George 溫和微笑看向 Amy，一手握咖啡杯柄，準備放回原杯碟；杯底尚未接觸碟面，保留清楚空隙。Amy 以頭肩背影聆聽。握起原有杯子，碟上不留重複杯。
```

### shot_2.1.3_banana21_v2

來源：OM `.tmp/banana21_third_v2_result.json`；工具代號 B；實際費用未知。原紀錄估 US$0.0675855，未核帳。
原始用量：{"prompt_token_count": 5732, "candidates_token_count": 1680, "thoughts_token_count": 1145}；生成耗時 40.14 秒。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png](../references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png)
2. [references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png](../references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 prompt：

```text
圖 1 是場景，物件與光影的絕對參考來源；圖 2 僅提供人物位置、比例、朝向與遮擋；圖 3、圖 4 分別提供 George、Amy 的外觀與服裝；圖 5 提供咖啡杯碟外觀。

George 溫和微笑看向 Amy，一手握住原有咖啡杯的杯柄，準備放回杯碟；杯底尚未接觸碟面，保留清楚空隙，碟上不留重複杯。Amy 安靜聆聽。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_2.1.3_banana21_v3

來源：OM `.tmp/banana21_third_v3_result.json`；工具代號 B；實際費用未知。原紀錄估 US$0.063372，未核帳。
原始用量：{"prompt_token_count": 5738, "candidates_token_count": 1714, "thoughts_token_count": 548}；生成耗時 33.8 秒。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png](../references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png)
2. [references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png](../references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 prompt：

```text
圖 1 是場景，物件，風格，氣氛，與光影的絕對參考來源；圖 2 僅提供人物位置、比例、朝向與遮擋；圖 3、圖 4 分別提供 George、Amy 的外觀與服裝；圖 5 提供咖啡杯碟外觀。

George 溫和微笑看向 Amy，一手握住原有咖啡杯的杯柄，準備放回杯碟；杯底尚未接觸碟面，保留清楚空隙，碟上不留重複杯。Amy 安靜聆聽。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_2.1.4_banana21_v1

來源：OM `.tmp/banana21_six_short_4_result.json`；工具代號 B；實際費用未知。
原始用量：{"prompt_token_count": 3599, "candidates_token_count": 1680, "thoughts_token_count": 554}；生成耗時 31.96 秒。

有序參考圖：

1. [references/scenes/coffee_shop/renders/blocks_blender_s08_amy_close_up.png](../references/scenes/coffee_shop/renders/blocks_blender_s08_amy_close_up.png)
2. [references/scenes/coffee_shop/cameras/empty_banana_s08_amy_close_up.png](../references/scenes/coffee_shop/cameras/empty_banana_s08_amy_close_up.png)
3. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)

完整 prompt：

```text
圖 1 是人物定位 blocks；圖 2 是本鏡空景。圖 3 提供Amy 外觀與服裝。
背景與光影沿用圖 2；依圖 1 的人物位置、整體大小、朝向與遮擋置入角色，藍色為 George、紅色為 Amy。人物外觀及自身頭身比例依人物參考圖，不照搬展示姿態；表演依下段。人物坐入既有椅子。維持既有 3D 動畫風格、取景與暖色日光，輸出一張 16:9 彩色分鏡圖；不呈現方塊、參考圖展示排版或新增字幕。
Amy 聽見「企業健康指標」而睜大眼睛、微抬眉、輕輕歪頭，嘴唇微張，望向畫外 George 驚奇反問。維持單人頭肩特寫。身體維持 圖 1 中朝向對坐的 George，肩膀與軀幹不轉動，只輕輕歪頭；頭與胸口朝向同一位對坐者，不做側身回頭姿勢。
```

### shot_2.1.4_banana21_v2

來源：OM `.tmp/banana21_fourth_v2_result.json`；工具代號 B；實際費用未知。原紀錄估 US$0.0556035，未核帳。
原始用量：{"prompt_token_count": 3469, "candidates_token_count": 1680}；生成耗時 35.87 秒。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/empty_banana_s08_amy_close_up.png](../references/scenes/coffee_shop/cameras/empty_banana_s08_amy_close_up.png)
2. [references/scenes/coffee_shop/renders/blocks_blender_s08_amy_close_up.png](../references/scenes/coffee_shop/renders/blocks_blender_s08_amy_close_up.png)
3. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)

完整 prompt：

```text
圖 1 是場景，物件，風格，與光影的絕對參考來源；圖 2 僅提供人物位置、人物朝向、人物比例與遮擋；圖 3 提供 Amy 的外觀與服裝。

Amy 睜大眼睛、微抬眉，輕輕歪頭，嘴唇微張。歪頭只調整頭部，肩膀與軀幹朝向沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_2.1.5_banana21_v1

來源：OM `.tmp/banana21_fifth_v1_result.json`；工具代號 B；實際費用未知。原紀錄估 US$0.0558105，未核帳。
原始用量：{"prompt_token_count": 3607, "candidates_token_count": 1680}；生成耗時 31.17 秒。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/empty_banana_s07_george_close_up.png](../references/scenes/coffee_shop/cameras/empty_banana_s07_george_close_up.png)
2. [references/scenes/coffee_shop/renders/blocks_blender_s07_george_close_up.png](../references/scenes/coffee_shop/renders/blocks_blender_s07_george_close_up.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)

完整 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s07_george_close_up.png] 是場景參考圖，是整體場景，物件，風格，與光影的絕對參考來源；
圖 2 [blocks_blender_s07_george_close_up.png] 是人物定位圖，是人物在場景中的位置、朝向、顯示比例，遮擋的絕對參考來源；
圖 3 [char_esg_george.png] 是人物參考圖，提供 George 的外觀與服裝。

生圖指引：
將圖 2 的藍色人物原位替換為圖 3 人物，維持人物在畫面中的佔位、裁切、與顯示部位，嚴禁縮小人物以展示更多身體。

畫面人物動作描述：
George 下巴略收，帶著肯定的神情與溫和微笑，嘴唇自然微張。只調整頭部姿態與表情，肩膀與軀幹朝向沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_2.1.6_gpt_template_v1

來源：OM `.tmp/gpt_sixth_template_v1_result.json`；工具代號 G；實際費用未知。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/empty_banana_s09_table_insert.png](../references/scenes/coffee_shop/cameras/empty_banana_s09_table_insert.png)
2. [references/scenes/coffee_shop/renders/blocks_blender_s09_table_insert.png](../references/scenes/coffee_shop/renders/blocks_blender_s09_table_insert.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s09_table_insert.png]：場景參考圖。
圖 2 [blocks_blender_s09_table_insert.png]：人物定位圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_set.png]：咖啡杯碟參考圖。

生圖指引：
場景、物件、材質、風格與光影以圖 1 為準。
最終構圖以圖 2 為準，包括取景、人物位置、朝向、畫面佔比，以及人物與場景物件的遮擋關係。
將圖 2 的藍色、紅色定位人物原位替換為 George、Amy；人物外觀與服裝分別採用圖 3、圖 4，不採用其展示姿態與取景。
杯碟外觀採用圖 5，不採用其展示排列或其他配件。
參考圖之間有差異時，依上述分工處理。

畫面人物動作描述：
George 已將咖啡杯放回杯碟。兩人的手自然停在桌邊，兩只咖啡杯均放在各自杯碟上，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_2.1.6_gpt_template_v2

來源：OM `.tmp/gpt_sixth_template_v2_result.json`；工具代號 G；實際費用未知。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/empty_banana_s09_table_insert.png](../references/scenes/coffee_shop/cameras/empty_banana_s09_table_insert.png)
2. [references/scenes/coffee_shop/renders/blocks_blender_s09_table_insert.png](../references/scenes/coffee_shop/renders/blocks_blender_s09_table_insert.png)
3. [clp/char_esg_george.png](../clp/char_esg_george.png)
4. [clp/char_esg_amy.jpeg](../clp/char_esg_amy.jpeg)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s09_table_insert.png]：場景外觀參考圖。
圖 2 [blocks_blender_s09_table_insert.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應紅色人物。
圖 5 [prop_coffee_set.png]：杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只替換圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3、圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。杯碟外觀採用圖 5；圖 5 的其他物件不參與生成。

畫面人物動作描述：
George 已將咖啡杯放回杯碟。兩人的手自然停在桌邊，兩只咖啡杯均放在各自杯碟上，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

## 2026-10-13 選版前的 manifest 快照

以下保留被替換的五張舊 JPG 記錄；完整 prompt 隨原 JSON 保存，歷史參考圖檔名／模型／費用仍未知。

```json
{
  "version": "1.0",
  "assets": [
    {
      "id": "img_shot_2.1.1",
      "type": "image",
      "path": "assets/images/shot_2.1.1.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2.1.1",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the entire 3D spatial geometry, camera perspective, room depth, and vanishing lines for the FULL scene. All foreground, midground, and background cafe elements must align with Image 1's perspective.\n- Image 2: Character identity and attire for Amy.\n- Image 3: Character identity and attire for George.\n- Image 4 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy Image 4's camera angle or frontal layout.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.1 in a single unified 3D perspective strictly matching Image 1:\nThe camera looks over George's (Image 3) right shoulder in the foreground. The coffee table and the entire cafe background (walls, windows, lighting) must rotate coherently with the camera's line of sight, creating realistic 3D parallax depth behind Amy (Image 2).\nAmy leans forward with both hands on the table, face full of panic and anxious pleading. George sits calmly listening.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_amy, char_george, loc_coffee_shop | Agent Native R2I: George右肩過肩中景看Amy慌張求救（全景透視主從對齊）"
    },
    {
      "id": "img_shot_2.1.2",
      "type": "image",
      "path": "assets/images/shot_2.1.2.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2.1.2",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the 3D camera angle (15-degree right turn), close-up framing, and background spatial perspective. Background room vanishing lines must align with this camera view.\n- Image 2: Character identity and attire for Amy.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or frontal layout.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.2 in a single unified 3D perspective strictly matching Image 1:\nAmy (Image 2) sits at the cafe table, clutching the sides of her head with both hands in dramatic, comical panic and frustration, face squished into an exaggerated overwhelmed pout. The background cafe elements rotate coherently with the 15-degree camera angle, smoothly blurred with shallow depth of field.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_amy, loc_coffee_shop | Agent Native R2I: Amy抱頭苦瓜臉特寫抓狂KPI要GG（15度背景透視消逝對齊）"
    },
    {
      "id": "img_shot_2.1.3",
      "type": "image",
      "path": "assets/images/shot_2.1.3.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2.1.3",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the 3D camera angle (15-degree left turn), framing, and room depth. Background cafe depth and vanishing perspective must strictly align with Image 1.\n- Image 2: Character identity and attire for George.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or flat backdrop.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.3 in a single unified 3D perspective strictly matching Image 1:\nGeorge (Image 2) sits at the table, placing a white coffee cup onto a saucer, looking across with a warm reassuring smile. The cafe background rotates coherently with the 15-degree camera orientation, creating realistic 3D depth and soft bokeh.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_george, prop_coffee_cup, loc_coffee_shop | Agent Native R2I: George放下咖啡杯溫和微笑中景（15度左偏室內縱深對齊）"
    },
    {
      "id": "img_shot_2.1.4",
      "type": "image",
      "path": "assets/images/shot_2.1.4.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2.1.4",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the 3D camera angle (45-degree right turn), close-up framing, and background spatial perspective. Background room vanishing lines must align with this diagonal view.\n- Image 2: Character identity and attire for Amy.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or frontal layout.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.4 in a single unified 3D perspective strictly matching Image 1:\nAmy (Image 2) is shown in close-up with head tilted slightly, wide curious eyes and raised eyebrows in surprise and questioning reaction. The cafe background rotates coherently to match the 45-degree camera orientation, smoothly throwing background cafe lights and textures into soft bokeh.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_amy, loc_coffee_shop | Agent Native R2I: Amy歪頭大眼好奇驚訝特寫（45度對角線吧台中島透視對齊）"
    },
    {
      "id": "img_shot_2.1.5",
      "type": "image",
      "path": "assets/images/shot_2.1.5.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2.1.5",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the front eye-level 3D camera angle, close-up framing, and centered room depth. Background cafe depth and vanishing perspective must strictly align with Image 1.\n- Image 2: Character identity and attire for George.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or flat backdrop.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.5 in a single unified 3D perspective strictly matching Image 1:\nGeorge (Image 2) sits at the table, raising his right hand with the index finger extended upward in a clear, confident instructional gesture, speaking warmly. The cafe interior background extends directly behind him with balanced, centered symmetrical perspective matching Image 1's depth.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_george, loc_coffee_shop | Agent Native R2I: George正面食指開導手勢特寫（正向軸線對稱縱深對齊）"
    }
  ]
}
```

## 2026-10-13 使用者確認採用

依使用者本次逐檔指定更新 manifest：前五鏡沿用既有 id，第六鏡新增 `img_shot_2.1.6`。六張均為內建 image_gen／OpenAI，確切模型與費用未提供，相關選填欄位省略。prompt 沿用各版歷史；short 版本按原紀錄的圖片角色說明＋共用短指令＋該鏡完整短指令拼接，未改寫。實際尺寸皆為 1672×941 PNG。

| shot | 採用圖片 |
|---|---|
| 2.1.1 | [shot_2.1.1_gpt_template_v2.png](../assets/images/shot_2.1.1_gpt_template_v2.png) |
| 2.1.2 | [shot_2.1.2_gpt_template_v1.png](../assets/images/shot_2.1.2_gpt_template_v1.png) |
| 2.1.3 | [shot_2.1.3_short_v1.png](../assets/images/shot_2.1.3_short_v1.png) |
| 2.1.4 | [shot_2.1.4_short_v2.png](../assets/images/shot_2.1.4_short_v2.png) |
| 2.1.5 | [shot_2.1.5_short_v1.png](../assets/images/shot_2.1.5_short_v1.png) |
| 2.1.6 | [shot_2.1.6_short_v1.png](../assets/images/shot_2.1.6_short_v1.png) |

舊圖片與既有生成紀錄保留；專案沒有既有 checkpoint／partial_progress 可同步。本次只確認六張 shot image，不代表整個 assets 階段完成。

## 2026-10-16 場景 4.6（行銷部）W2I 生成紀錄

### shot_4.6.1_gpt_template_v1

**原標題**：4.6.1 GPT 非自拍模板樣圖 v1

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；以使用者最新「不要自拍」與確認的 prompt 為準。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：一次、生成一張；transparent_background=false；prompt 原文送出，未追加創意條件。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s06_amy_medium_close_up.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s06_amy_medium_close_up.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 輸出：../assets/images/shot_4.6.1_gpt_template_v1.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-0b9d39b0-7077-4abf-b9fd-8054a2c6b2f2.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：非自拍、無手機、無字幕、Amy 開朗說話表情與暖色場景成立；灰色白模軀幹、手臂及手部仍殘留，Amy 部分上身出現在白模軀幹後方，人物替換未完成，未通過驗收。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未驗證後續影片效果。
- 狀態：保留本次未通過樣圖，未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准；script.json／scene_plan 仍保留舊自拍規劃，後續以使用者最新指示為準。

#### 實際送出 prompt

```text
參考圖說明：
圖 1 empty_gpt_s06_amy_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s06_amy_medium_close_up.png：構圖底圖。
圖 3 char_esg_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。
將定位人物替換為 Amy，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張正面、接近平視的胸部以上中近景，由人物前方的攝影機拍攝。Amy 位於畫面中央，頭部、肩膀與胸部入鏡，手臂及畫面右下角露出的局部手部沿用圖 2 的可見範圍與裁切。
定格在 Amy 來到行銷部、開口介紹最後一站的瞬間。她帶著開朗且期待的笑容，眼睛看向鏡頭，嘴巴微張，流露即將探索創意寶藏的興奮。身體朝向與手部位置沿用圖 2，呈現自然說話的姿態，不持手機、不做伸臂自拍動作。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_4.6.1_gpt_template_v2

**原標題**：4.6.1 GPT 非自拍模板樣圖 v2

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；以使用者最新「不要自拍」與確認的 prompt 為準。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：依使用者明確要求重新生成一次、一張；使用與 v1 完全相同的 prompt、三張參考圖及順序，transparent_background=false，未追加修正條件。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s06_amy_medium_close_up.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s06_amy_medium_close_up.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 輸出：../assets/images/shot_4.6.1_gpt_template_v2.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-fdfe952c-94bd-483a-9142-91aac53ac034.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：非自拍、無手機、無字幕、Amy 開朗說話表情與暖色場景成立；灰色白模軀幹、手臂及手部仍殘留，Amy 部分上身出現在白模軀幹後方，人物替換未完成，未通過驗收。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未驗證後續影片效果。
- 狀態：保留 v1 與本次未通過的 v2 樣圖，未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准；script.json／scene_plan 仍保留舊自拍規劃，後續以使用者最新指示為準。

#### 實際送出 prompt

```text
參考圖說明：
圖 1 empty_gpt_s06_amy_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s06_amy_medium_close_up.png：構圖底圖。
圖 3 char_esg_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。
將定位人物替換為 Amy，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張正面、接近平視的胸部以上中近景，由人物前方的攝影機拍攝。Amy 位於畫面中央，頭部、肩膀與胸部入鏡，手臂及畫面右下角露出的局部手部沿用圖 2 的可見範圍與裁切。
定格在 Amy 來到行銷部、開口介紹最後一站的瞬間。她帶著開朗且期待的笑容，眼睛看向鏡頭，嘴巴微張，流露即將探索創意寶藏的興奮。身體朝向與手部位置沿用圖 2，呈現自然說話的姿態，不持手機、不做伸臂自拍動作。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_4.6.1_gpt_template_v3

**原標題**：4.6.1 GPT 完整人物替換樣圖 v3

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；以使用者最新「不要自拍」與核准的完整人物替換 prompt 為準。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：一次、一張；使用本輪核准 prompt 原文與原三張參考圖，transparent_background=false；未改用 v1／v2 成果作底圖。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s06_amy_medium_close_up.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s06_amy_medium_close_up.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 輸出：../assets/images/shot_4.6.1_gpt_template_v3.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-21d907ac-f69b-4a48-804b-dbb1905977ce.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：灰色人物白模軀幹、手臂及手部不再殘留；Amy 的自然上身、服裝、手臂與開朗說話表情成立，無自拍／手機／字幕。但 blocks 右下角原可見手部被裁掉，頭頂留白減少，背景白板左邊界向右偏移，仍未完全符合原構圖與可見範圍，未宣稱整鏡驗收通過。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未驗證後續影片效果。
- 狀態：保留 v1／v2／v3，不追加生成、未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准；script.json／scene_plan 仍保留舊自拍規劃，後續以使用者最新指示為準。

#### 實際送出 prompt

```text
參考圖說明：
圖 1 empty_gpt_s06_amy_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s06_amy_medium_close_up.png：構圖底圖，其中的積木狀人物是待完整替換的定位人物。
圖 3 char_esg_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、場景物件配置、人物佔位、顯示範圍與遮擋關係。

將圖 2 中整個定位人物在原位置完整替換為 Amy，包含頭部、頸部、肩膀、軀幹、雙臂及所有可見手部，不可只替換頭臉或部分上身。

人物中央的大灰色長方體是軀幹，兩側灰色長條是手臂，畫面右下角的灰色手部也屬於同一個定位人物；這些都不是桌子、擋板或其他前景物件，必須一起替換。不可保留這些方塊，再把 Amy 放在它們後方。

替換後，軀幹與手臂呈現 Amy 的西裝與衣袖，可見手部呈現 Amy 的自然手掌與手指；人物各部位自然連接，不保留任何白模、積木狀外殼或未替換的定位人物部件。

保留定位人物的站位、朝向、姿勢、畫面尺度與裁切，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張正面、接近平視的胸部以上中近景，由人物前方的攝影機拍攝。Amy 位於畫面中央，頭部、肩膀與胸部入鏡，手臂及畫面右下角露出的局部手部沿用圖 2 的可見範圍與裁切。
定格在 Amy 來到行銷部、開口介紹最後一站的瞬間。她帶著開朗且期待的笑容，眼睛看向鏡頭，嘴巴微張，流露即將探索創意寶藏的興奮。身體朝向與手部位置沿用圖 2，呈現自然說話的姿態，不持手機、不做伸臂自拍動作。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_4.6.1_gpt_template_v4

**原標題**：4.6.1 GPT SH01 雙人全景與白板內容樣圖 v4

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；以使用者最新 SH01 雙人全景、非自拍及白板圖文參考為準。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：一次、一張；使用本輪核准 prompt 原文與五張獨立參考圖，transparent_background=false；未以舊成果作底圖。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s01_wide_two_shot.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s01_wide_two_shot.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 圖 4：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_li.jpeg
- 圖 5：D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png
- 輸出：../assets/images/shot_4.6.1_gpt_template_v4.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-1d31015b-a69f-423b-adc4-83b08b7d6256.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：Amy 左／小李右且全身入鏡，定位人物完整替換、無白模，Amy 開口介紹與小李閉嘴看向 Amy、垂放雙手、非自拍／無手機／無字幕成立。既有白板已帶入十張彩色便條紙及圖文，未新增第二塊白板；但人物較 blocks 高、頭頂及腳下留白減少，小李偏右，部分便條紙位置／間距有調整，未完全保留構圖。白板文字已目視檢視，未宣稱逐字或逐像素一致。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未驗證後續影片效果。
- 狀態：保留 v1～v4，不追加生成、未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准；script.json／scene_plan 仍保留舊自拍規劃，後續以使用者最新指示為準，4.6.2 不變。

#### 實際送出 prompt

```text
參考圖說明：
圖 1 empty_gpt_s01_wide_two_shot.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s01_wide_two_shot.png：構圖底圖，其中的兩個積木狀人物是待完整替換的定位人物。
圖 3 char_esg_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的灰色衣服人物。
圖 4 char_esg_li.jpeg：小李人物參考圖，對應圖 2 右側的藍綠色衣服人物。
圖 5 prop_whiteboard_incorrect.png：白板上的圖文內容參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、場景物件配置、人物佔位、顯示範圍與遮擋關係。

將兩個定位人物在原位置完整替換為 Amy 與小李，包含頭部、頸部、肩膀、軀幹、雙臂、手部、雙腿與雙腳，不可只替換頭臉或部分身體。
灰色與藍綠色的軀幹方塊、長條手臂、方塊手掌、腿部與腳部都屬於定位人物，必須一起替換。不可保留這些方塊，再把角色放在它們前方或後方。
替換後，各部位呈現對應角色的自然身體、服裝、手掌、手指與鞋子，彼此自然連接，不保留任何白模、積木狀外殼或未替換的定位人物部件。

保留人物的站位、朝向、姿勢、畫面尺度與裁切，只呈現圖 2 中可見的部位，不補出畫外身體。Amy 的外觀與服裝採用圖 3，小李的外觀與服裝採用圖 4，不採用人物參考圖的展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 5 中白板書寫面內的彩色便條紙、文字內容及版面排列，依圖 2 的白板透視貼合到既有白板上，保留各張便條紙的顏色、相對位置與比例，不自行改寫或修正文字。
圖 5 只提供白板內的畫面內容，不採用其板框、拍攝角度或其他物件。白板的位置、大小、板框、筆槽、腳架及遮擋關係沿用圖 2，不新增另一塊白板，也不為了露出文字而移動人物。

畫面描述：
這是一張正面略俯視的雙人全景。Amy 位於畫面左側，小李位於右側，兩人從頭到腳完整入鏡，白板位於兩人後方中央。人物大小、間距、頭頂留白、腳下地面範圍與周圍空間沿用圖 2，不拉近鏡頭或將人物向中央靠攏。

定格在 Amy 來到行銷部、開口介紹最後一站的瞬間。她帶著開朗且期待的笑容，眼睛看向鏡頭，嘴巴微張，流露即將探索創意寶藏的興奮；身體與手部姿勢沿用圖 2。小李自然站在右側，嘴巴閉合，視線看向 Amy，聆聽她介紹，雙臂與雙手沿用圖 2 的垂放姿勢。兩人不持手機、不做自拍動作。
後方白板呈現圖 5 的彩色便條紙與圖文內容，人物自然遮住的部分維持遮擋。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_4.6.1_gpt_template_v5

**原標題**：4.6.1 GPT SH01 雙人中景與白板內容樣圖 v5

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；以使用者本輪貼上的雙人中景 prompt 為準。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：一次、一張；使用使用者 prompt 原文與五張獨立參考圖，transparent_background=false；未改用 SH01 wide、舊 SH02 或舊成果作底圖。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s01_medium_two_shot.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s01_medium_two_shot.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 圖 4：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_li.jpeg
- 圖 5：D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png
- 輸出：../assets/images/shot_4.6.1_gpt_template_v5.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-ba4eb610-7f7b-46ec-8421-24339f8ef51d.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：Amy 左／小李右的雙人中景、頭部至部分大腿入鏡、完整人物替換與無白模成立。Amy 開口看向鏡頭介紹、小李閉嘴看向 Amy 並垂放雙手，無手機／自拍／字幕。白板已呈現十張彩色便條紙及圖文，未新增白板。兩人頭頂較 blocks 上移、留白減少，Amy 抬手位置較高，構圖與姿勢未完全對齊；白板圖文已目視檢視，未宣稱逐字或逐像素一致。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未驗證後續影片效果。
- 狀態：保留 v1～v5，不追加生成、未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准；分鏡與角色設定未改，後續以使用者最新指示為準，4.6.2 不變。

#### 實際送出 prompt

```text
參考圖說明：
圖 1 empty_gpt_s01_medium_two_shot.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s01_medium_two_shot.png：構圖底圖，其中的兩個積木狀人物是待完整替換的定位人物。
圖 3 char_esg_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的灰色衣服人物。
圖 4 char_esg_li.jpeg：小李人物參考圖，對應圖 2 右側的藍綠色衣服人物。
圖 5 prop_whiteboard_incorrect.png：白板上的圖文內容參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、場景物件配置、人物佔位、顯示範圍與遮擋關係。

將兩個定位人物在原位置完整替換為 Amy 與小李，包含頭部、頸部、肩膀、軀幹、雙臂、手部、雙腿與雙腳，不可只替換頭臉或部分身體。
灰色與藍綠色的軀幹方塊、長條手臂、方塊手掌、腿部與腳部都屬於定位人物，必須一起替換。不可保留這些方塊，再把角色放在它們前方或後方。
替換後，各部位呈現對應角色的自然身體、服裝、手掌、手指與鞋子，彼此自然連接，不保留任何白模、積木狀外殼或未替換的定位人物部件。

保留人物的站位、朝向、姿勢、畫面尺度與裁切，只呈現圖 2 中可見的部位，不補出畫外身體。Amy 的外觀與服裝採用圖 3，小李的外觀與服裝採用圖 4，不採用其展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 5 中白板書寫面內的彩色便條紙、文字內容及版面排列，依圖 2 的白板透視貼合到既有白板上，保留各張便條紙的顏色、相對位置與比例，不自行改寫或修正文字。
圖 5 只提供白板內的畫面內容，不採用其板框、拍攝角度或其他物件。白板的位置、大小、板框、筆槽、腳架及遮擋關係沿用圖 2，不新增另一塊白板，也不為了露出文字而移動人物。

畫面描述：
這是一張正面雙人中景。Amy 位於畫面左側，小李位於右側，兩人從頭到大腿一半，完整入鏡，白板位於兩人後方中央。人物大小、間距、頭頂留白、腳下地面範圍與周圍空間沿用圖 2，不拉近鏡頭或將人物向中央靠攏。

定格在 Amy 來到行銷部、開口介紹最後一站的瞬間。她帶著開朗且期待的笑容，眼睛看向鏡頭，嘴巴微張，流露即將探索創意寶藏的興奮；身體與手部姿勢沿用圖 2。小李自然站在右側，嘴巴閉合，視線看向 Amy，聆聽她介紹，雙臂與雙手沿用圖 2 的垂放姿勢。兩人不持手機、不做自拍動作。
後方白板呈現圖 5 的彩色便條紙與圖文內容，人物自然遮住的部分維持遮擋。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_4.6.2_gpt_template_v1

**原標題**：4.6.2 GPT 雙人海報模板樣圖 v1

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：一次、一張；使用本輪核准的 4.6.2 prompt 原文與四張參考圖，transparent_background=false，未追加修正條件。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s02_medium_two_shot.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s02_medium_two_shot.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 圖 4：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_li.jpeg
- 輸出：../assets/images/shot_4.6.2_gpt_template_v1.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-bd8816b5-1e7d-4e5f-9f5d-93011cc189dd.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：兩個定位人物已完整替換，無殘留白模；Amy 灰西裝、小李花襯衫與無眼鏡符合實圖，小李雙手舉彩色海報、興奮說話與看向 Amy，Amy 看海報／閉嘴聆聽、海報空白標語區及無字幕成立。人物較 blocks 靠近中央，兩人間距縮小、頭頂留白減少；Amy 改成托下巴與橫臂，未沿用 blocks 手勢。構圖與姿勢未完全通過。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未製作海報文字後製或驗證後續影片效果。
- 狀態：保留本次樣圖，不追加生成、未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准。

#### 實際送出 prompt

```text
參考圖說明：
圖 1 empty_gpt_s02_medium_two_shot.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s02_medium_two_shot.png：構圖底圖，其中的兩個積木狀人物是待完整替換的定位人物。
圖 3 char_esg_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的灰色衣服人物。
圖 4 char_esg_li.jpeg：小李人物參考圖，對應圖 2 右側的藍綠色衣服人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、場景物件配置、人物佔位、顯示範圍與遮擋關係；小李舉海報及兩人的表情、視線依下方畫面描述調整。

將兩個定位人物在原位置完整替換為 Amy 與小李，包含頭部、頸部、肩膀、軀幹、雙臂、所有可見手部及腿部，不可只替換頭臉或部分上身。
灰色與藍綠色的長方體軀幹、長條手臂、方塊手掌與腿部都屬於定位人物，不是桌子、擋板或其他場景物件，必須一起替換。不可保留這些方塊，再把角色放在它們前方或後方。
替換後，各部位呈現對應角色的自然身體、服裝、手掌與手指，彼此自然連接，不保留任何白模、積木狀外殼或未替換的定位人物部件。背景白板與場景家具仍須保留。

只呈現圖 2 中可見的身體範圍，不補出畫外身體。Amy 的外觀與服裝採用圖 3，小李的外觀與服裝採用圖 4，不採用人物參考圖的展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張近眼高、固定鏡頭的雙人中景。Amy 位於畫面左側，小李位於右側，空白白板在兩人後方中央。兩人的頭部、軀幹、手臂及部分大腿入鏡，人物大小、間距、頭頂留白與下緣裁切沿用圖 2。

定格在小李興奮展示剛印出的炫彩新海報、期待 Amy 回應的瞬間。小李將原本垂下的雙手改為舉起一張海報，手指自然握住紙張邊緣，海報位於兩人之間的胸腹高度，正面略斜向 Amy，同時讓觀眾看得到紙面，不遮擋兩人的臉。海報採鮮明彩色設計，保留空白標語區，不生成海報文字。
小李帶著興奮、自信又期待認同的表情，嘴巴張開說話，視線看向 Amy。Amy 的視線落在海報上，神情專注，嘴巴自然閉合，安靜聆聽；手部姿勢沿用圖 2。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_4.6.2_gpt_template_v2

**原標題**：shot_4.6.2 GPT 模板生成 v2

- 日期：2026-10-16
- 使用者指示：使用上一輪已展示的 prompt，在 GPT 生圖。
- 工具／供應商：內建 image_gen／OpenAI；介面未提供確切模型及費用。
- 本輪生成次數：1；未追加生成。
- 輸出：`../assets/images/shot_4.6.2_gpt_template_v2.png`
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-e05dd814-6afe-4225-942d-0860d188ba8f.png`
- 參考圖依下列 prompt 圖號順序傳入；prompt 原文未改寫。
- 圖 1：`../references/scenes/marketing_department/cameras/empty_gpt_s02_li_medium_close_up.png`
- 圖 2：`../references/scenes/marketing_department/renders/blocks_blender_s02_li_medium_close_up.png`
- 圖 3：`../clp/char_esg_li.jpeg`
- 圖 4：`../clp/prop_whiteboard_incorrect.png`

#### Prompt 原文

```text
參考圖說明：
圖 1 empty_gpt_s02_li_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s02_li_medium_close_up.png：構圖底圖，其中藍綠色衣服的積木狀人物是待完整替換的定位人物。
圖 3 char_esg_li.jpeg：小李人物參考圖，對應圖 2 的藍綠色衣服人物。
圖 4 prop_whiteboard_incorrect.png：白板上的圖文內容參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、場景物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物在原位置完整替換為小李，包含畫面中可見的頭部、頸部、肩膀、軀幹與手臂，不可只替換頭臉或部分身體。
藍綠色的軀幹方塊與長條手臂都屬於定位人物，必須一起替換。不可保留這些方塊，再把小李放在它們前方或後方。
替換後，各部位呈現小李的自然身體與服裝，彼此自然連接，不保留任何白模、積木狀外殼或未替換的定位人物部件。

保留人物的站位、身體朝向、姿勢、畫面尺度與裁切，只呈現圖 2 中可見的部位，不補出畫外身體、手掌或手指。
小李的外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 4 中白板書寫面內的彩色便條紙、文字內容及版面排列，依圖 2 的白板透視貼合到既有白板上，保留各張便條紙的顏色、相對位置與比例，不自行改寫或修正文字。
圖 4 只提供白板內的畫面內容，不採用其板框、拍攝角度或其他物件。白板的位置、大小、板框、筆槽、裁切及遮擋關係沿用圖 2，不新增另一塊白板，也不為了露出文字而移動人物。
以整塊白板書寫面對應圖 4 的完整版面，再依圖 2 的取景自然裁切。位於畫外或被小李遮住的內容維持不可見，不將全部便條紙縮小或重新排列到可見區域。

畫面描述：
這是一張小李單人中近景。小李位於畫面中央偏右，呈現頭部、頸部、肩膀、胸口與部分上臂，下方軀幹及手臂依圖 2 的畫面邊界裁切，雙手不入鏡。白板佔據畫面左側及小李後方，右側保留圖 2 可見的窗戶與背景。人物大小、位置、頭頂留白、白板可見範圍與周圍空間沿用圖 2，不拉近或拉遠鏡頭，不將小李移到畫面正中央。

定格在小李興奮介紹新產品標語、期待 Amy 反應的瞬間。他帶著自豪且熱切的笑容，眉毛微微揚起，嘴巴張開正在說話，視線看向畫面左側、位於畫外的 Amy；身體與可見手臂的姿勢沿用圖 2。
Amy、雙手與原本展示的海報皆留在本鏡的畫外範圍，不為了呈現展示動作而新增入鏡的手部或海報。
後方白板呈現圖 4 的彩色便條紙與圖文內容，人物自然遮住及畫面裁切掉的部分維持不可見。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

#### 結果檢視

- 1672×941 RGB PNG，接近 16:9；完整解碼成功，專案副本與原始輸出 SHA256 相同。
- 小李單人中近景、花襯衫、完整人物替換與興奮說話表情成立；視線朝左，Amy、手部及海報未入鏡，未見殘留白模或字幕。
- 小李相對 blocks 略向右移；白板十張便條紙集中在可見區，未維持整塊白板版面映射後應有的裁切與遮擋，構圖要求尚未完全通過。
- 白板內容外觀已套用，但未確認所有文字逐字一致；不將本版標示為已核准。
- 保留舊版，未替換正式素材，未改分鏡／manifest，未推進 assets 核准。

### shot_4.6.2_gpt_template_v3

**原標題**：shot_4.6.2 GPT 模板生成 v3

- 日期：2026-10-16
- 使用者指示：使用本輪提供的完整 prompt 重新生成，新增只顯示白板可見區域之部分便條紙內容的括號說明。
- 工具／供應商：內建 image_gen／OpenAI；介面未提供確切模型及費用。
- 本輪生成次數：1；未追加生成。
- 輸出：`../assets/images/shot_4.6.2_gpt_template_v3.png`
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-1f7e72ad-57ad-490f-846a-eaabcf856e75.png`
- 參考圖依下列 prompt 圖號順序傳入；prompt 原文未改寫。
- 圖 1：`../references/scenes/marketing_department/cameras/empty_gpt_s02_li_medium_close_up.png`
- 圖 2：`../references/scenes/marketing_department/renders/blocks_blender_s02_li_medium_close_up.png`
- 圖 3：`../clp/char_esg_li.jpeg`
- 圖 4：`../clp/prop_whiteboard_incorrect.png`

#### Prompt 原文

```text
參考圖說明：
圖 1 empty_gpt_s02_li_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s02_li_medium_close_up.png：構圖底圖，其中藍綠色衣服的積木狀人物是待完整替換的定位人物。
圖 3 char_esg_li.jpeg：小李人物參考圖，對應圖 2 的藍綠色衣服人物。
圖 4 prop_whiteboard_incorrect.png：白板上的圖文內容參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、場景物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物在原位置完整替換為小李，包含畫面中可見的頭部、頸部、肩膀、軀幹與手臂，不可只替換頭臉或部分身體。
藍綠色的軀幹方塊與長條手臂都屬於定位人物，必須一起替換。不可保留這些方塊，再把小李放在它們前方或後方。
替換後，各部位呈現小李的自然身體與服裝，彼此自然連接，不保留任何白模、積木狀外殼或未替換的定位人物部件。

保留人物的站位、身體朝向、姿勢、畫面尺度與裁切，只呈現圖 2 中可見的部位，不補出畫外身體、手掌或手指。
小李的外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 4 中白板書寫面內的彩色便條紙、文字內容及版面排列，依圖 2 的白板透視貼合到既有白板上，保留各張便條紙的顏色、相對位置與比例，不自行改寫或修正文字。(僅需針對所顯示的白板區域，來顯示部分的便條紙內容)
圖 4 只提供白板內的畫面內容，不採用其板框、拍攝角度或其他物件。白板的位置、大小、板框、筆槽、裁切及遮擋關係沿用圖 2，不新增另一塊白板，也不為了露出文字而移動人物。
以整塊白板書寫面對應圖 4 的完整版面，再依圖 2 的取景自然裁切。位於畫外或被小李遮住的內容維持不可見，不將全部便條紙縮小或重新排列到可見區域。

畫面描述：
這是一張小李單人中近景。小李位於畫面中央偏右，呈現頭部、頸部、肩膀、胸口與部分上臂，下方軀幹及手臂依圖 2 的畫面邊界裁切，雙手不入鏡。白板佔據畫面左側及小李後方，右側保留圖 2 可見的窗戶與背景。人物大小、位置、頭頂留白、白板可見範圍與周圍空間沿用圖 2，不拉近或拉遠鏡頭，不將小李移到畫面正中央。

定格在小李興奮介紹新產品標語、期待 Amy 反應的瞬間。他帶著自豪且熱切的笑容，眉毛微微揚起，嘴巴張開正在說話，視線看向畫面左側、位於畫外的 Amy；身體與可見手臂的姿勢沿用圖 2。
Amy、雙手與原本展示的海報皆留在本鏡的畫外範圍，不為了呈現展示動作而新增入鏡的手部或海報。
後方白板呈現圖 4 的彩色便條紙與圖文內容，人物自然遮住及畫面裁切掉的部分維持不可見。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

#### 結果檢視

- 1672×941 RGB PNG，接近 16:9；完整解碼成功，專案副本與原始輸出 SHA256 相同。
- 小李單人中近景、花襯衫、完整人物替換與興奮說話表情成立；視線朝左，Amy、雙手及海報未入鏡，未見殘留白模或字幕。
- 相較 v2，白板只露出部分便條紙，其餘被小李遮擋；不再將十張便條紙全部明顯呈現於可見區。
- 小李頭頂留白與頭部位置較接近 blocks；肩線及軀幹輪廓仍有變動，便條紙位置及比例未確認精確對齊整板映射。
- 未確認白板所有文字逐字一致；不將本版標示為已核准。
- 保留舊版，未替換正式素材，未改分鏡／manifest，未推進 assets 核准。

### shot_4.6.3_gpt_template_v1

**原標題**：shot_4.6.3 GPT 模板生成 v1

- 日期：2026-10-16
- 使用者指示：使用上一輪完整 prompt，在 GPT 生圖。
- 工具／供應商：內建 image_gen／OpenAI；介面未提供確切模型及費用。
- 本輪生成次數：1；未追加生成。
- 輸出：`../assets/images/shot_4.6.3_gpt_template_v1.png`
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-35cd7a18-4fc4-4f20-a925-82488d52dae9.png`
- 參考圖依下列 prompt 圖號順序傳入；prompt 原文未改寫。
- 圖 1：`../references/scenes/marketing_department/cameras/empty_gpt_s03_amy_medium_close_up.png`
- 圖 2：`../references/scenes/marketing_department/renders/blocks_blender_s03_amy_medium_close_up.png`
- 圖 3：`../clp/char_esg_amy.jpeg`
- 圖 4：`../clp/prop_whiteboard_incorrect.png`
- 圖 5：`../clp/prop_smartphone.png`

#### Prompt 原文

```text
參考圖說明：
圖 1 empty_gpt_s03_amy_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s03_amy_medium_close_up.png：構圖底圖，其中灰色衣服的積木狀人物是待完整替換的定位人物。
圖 3 char_esg_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服人物。
圖 4 prop_whiteboard_incorrect.png：白板上的圖文內容參考圖。
圖 5 prop_smartphone.png：Amy 手中手機的實體外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、場景物件配置、人物佔位、顯示範圍與遮擋關係。

將整個灰色定位人物在原位置完整替換為 Amy，包含畫面中可見的頭部、頸部、肩膀、軀幹、雙臂、手掌與手指，不可只替換頭臉或部分身體。
灰色軀幹方塊、長條手臂、方塊手掌與手指都屬於定位人物，必須一起替換。不可保留這些方塊，再把 Amy 放在它們前方或後方。
替換後，各部位呈現 Amy 的自然身體、服裝、手掌與手指，彼此自然連接，不保留任何白模、積木狀外殼或未替換的定位人物部件。

保留人物的站位、身體朝向、畫面尺度與裁切，只呈現圖 2 中可見的部位，不補出畫外身體。雙臂與雙手的位置沿用圖 2，僅允許持手機的手掌與手指因握持需要而調整。
Amy 的外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或構圖。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 4 中白板書寫面內的彩色便條紙、文字內容及版面排列，依圖 2 的白板透視貼合到既有白板上，保留各張便條紙的顏色、相對位置與比例，不自行改寫或修正文字。僅針對圖 2 所顯示的白板區域，呈現部分便條紙內容。
圖 4 只提供白板內的畫面內容，不採用其板框、拍攝角度或其他物件。白板的位置、大小、板框、筆槽、裁切及遮擋關係沿用圖 2，不新增另一塊白板，也不為了露出文字而移動人物。
以整塊白板書寫面對應圖 4 的完整版面，再依圖 2 的取景自然裁切。位於畫外或被 Amy、手臂及手機遮住的內容維持不可見，不將全部便條紙縮小或重新排列到可見區域。

在 Amy 位於畫面右側、原本抬起的手中放入一支手機，手機的機身顏色、邊框、厚度、背蓋及鏡頭模組採用圖 5。
手機直向握持，螢幕朝向 Amy，鏡頭主要看見手機背面與側邊；尺寸與她的手掌相稱，手指自然握住機身，不穿透手機，不遮住臉部。
圖 5 只提供同一支手機的實體外觀，不採用其多視圖排列、展示角度、背景或「主管來電」介面，畫面中只出現一支手機。手機用於查證資訊，不呈現自拍、錄影或接聽電話的動作，也不新增面向觀眾的法規頁面或文字介面。

畫面描述：
這是一張 Amy 單人中近景。Amy 位於畫面中央偏左，呈現頭部、頸部、肩膀、上半身及圖 2 中可見的雙臂與手部。畫面右側的前臂彎曲抬起，手中握著手機；另一隻手位於畫面下緣，沿用圖 2 的部分裁切，不補出被裁掉的手部或下半身。
白板位於畫面右側與 Amy 後方，左側保留圖 2 可見的辦公桌、隔板、螢幕、窗戶及其他既有物件。人物大小、位置、頭頂留白、白板可見範圍與周圍空間沿用圖 2，不拉近或拉遠鏡頭，不將 Amy 移到畫面正中央。

定格在 Amy 剛用手機查證資訊、抬眼嚴肅提醒小李文案可能涉及漂綠的瞬間。她眉頭微皺，神情專注且帶著擔憂，嘴巴微張正在說話，視線看向畫面右側、位於畫外的小李；身體與手臂姿勢沿用圖 2，手機仍握在抬起的手中，螢幕朝向自己。
小李與海報均在畫外，不新增入鏡人物或海報。後方白板呈現圖 4 的部分便條紙與圖文內容，人物、手臂與手機自然遮住及畫面裁切掉的部分維持不可見。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

#### 結果檢視

- 1672×941 RGB PNG，接近 16:9；完整解碼成功，專案副本與原始輸出 SHA256 相同。
- Amy 單人、灰色西裝、完整替換白模及皺眉嚴肅說話表情成立；視線朝右，一支黑色手機呈現背面與側邊，未出現來電介面、字幕、小李或海報。
- 相較 blocks，Amy 頭頂留白減少；持手機手明顯抬高並向身體內收，前臂角度改變，另一手的可見部分減少，構圖／姿勢尚未完全符合。
- 白板呈現部分便條紙及遮擋；版面位置、比例未確認精確符合整塊白板的映射，文字未確認逐字一致。
- 不將本版標示為已核准；未替換正式素材，未改分鏡／manifest，未推進 assets 核准。
