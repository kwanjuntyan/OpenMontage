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
| 2.1.1 | [shot_2_1_1.jpg](../assets/images/shot_2_1_1.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.1 | [shot_2_1_1_banana21_v1.png](../assets/images/shot_2_1_1_banana21_v1.png) | B | [補回原請求](#shot_2_1_1_banana21_v1) | 保留版本 |
| 2.1.1 | [shot_2_1_1_banana21_v2.png](../assets/images/shot_2_1_1_banana21_v2.png) | B | [補回原請求](#shot_2_1_1_banana21_v2) | 保留版本 |
| 2.1.1 | [shot_2_1_1_banana21_v3.png](../assets/images/shot_2_1_1_banana21_v3.png) | B | [原紀錄第 28 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2_1_1_banana21_v4.png](../assets/images/shot_2_1_1_banana21_v4.png) | B | [原紀錄第 55 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2_1_1_banana21_v5.png](../assets/images/shot_2_1_1_banana21_v5.png) | B | [原紀錄第 84 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2_1_1_banana21_v6.png](../assets/images/shot_2_1_1_banana21_v6.png) | B | [原紀錄第 137 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2_1_1_gpt_template_v1.png](../assets/images/shot_2_1_1_gpt_template_v1.png) | G | [原紀錄第 30 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2_1_1_gpt_template_v2.png](../assets/images/shot_2_1_1_gpt_template_v2.png) | G | [原紀錄第 57 行](shot_prompts_2_1_banana21.md#211) | manifest 現行 |
| 2.1.1 | [shot_2_1_1_gpt_template_v3.png](../assets/images/shot_2_1_1_gpt_template_v3.png) | G | [原紀錄第 112 行](shot_prompts_2_1_banana21.md#211) | 保留版本 |
| 2.1.1 | [shot_2_1_1_short_v1.png](../assets/images/shot_2_1_1_short_v1.png) | G | [原紀錄第 24 行](shot_prompts_2_1.md#211amy-求救s02_medium_two_shot40mm) | 保留版本 |
| 2.1.2 | [shot_2_1_2.jpg](../assets/images/shot_2_1_2.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.2 | [shot_2_1_2_banana21_v1.png](../assets/images/shot_2_1_2_banana21_v1.png) | B | [補回原請求](#shot_2_1_2_banana21_v1) | 保留版本 |
| 2.1.2 | [shot_2_1_2_banana21_v2.png](../assets/images/shot_2_1_2_banana21_v2.png) | B | [原紀錄第 155 行](shot_prompts_2_1_banana21.md#212) | 保留版本 |
| 2.1.2 | [shot_2_1_2_banana21_v3.png](../assets/images/shot_2_1_2_banana21_v3.png) | B | [原紀錄第 185 行](shot_prompts_2_1_banana21.md#212) | 保留版本 |
| 2.1.2 | [shot_2_1_2_banana21_v4.png](../assets/images/shot_2_1_2_banana21_v4.png) | B | [原紀錄第 213 行](shot_prompts_2_1_banana21.md#212) | 保留版本 |
| 2.1.2 | [shot_2_1_2_gpt_template_v1.png](../assets/images/shot_2_1_2_gpt_template_v1.png) | G | [原紀錄第 157 行](shot_prompts_2_1_banana21.md#212) | manifest 現行 |
| 2.1.2 | [shot_2_1_2_short_v1.png](../assets/images/shot_2_1_2_short_v1.png) | G | [原紀錄第 37 行](shot_prompts_2_1.md#212amy-訴苦s06_amy_medium_close_up65mm) | 保留版本 |
| 2.1.3 | [shot_2_1_3.jpg](../assets/images/shot_2_1_3.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.3 | [shot_2_1_3_banana21_v1.png](../assets/images/shot_2_1_3_banana21_v1.png) | B | [補回原請求](#shot_2_1_3_banana21_v1) | 保留版本 |
| 2.1.3 | [shot_2_1_3_banana21_v2.png](../assets/images/shot_2_1_3_banana21_v2.png) | B | [補回原請求](#shot_2_1_3_banana21_v2) | 保留版本 |
| 2.1.3 | [shot_2_1_3_banana21_v3.png](../assets/images/shot_2_1_3_banana21_v3.png) | B | [補回原請求](#shot_2_1_3_banana21_v3) | 保留版本 |
| 2.1.3 | [shot_2_1_3_banana21_v4.png](../assets/images/shot_2_1_3_banana21_v4.png) | B | [原紀錄第 237 行](shot_prompts_2_1_banana21.md#213) | 保留版本 |
| 2.1.3 | [shot_2_1_3_banana21_v5.png](../assets/images/shot_2_1_3_banana21_v5.png) | B | [原紀錄第 270 行](shot_prompts_2_1_banana21.md#213) | 保留版本 |
| 2.1.3 | [shot_2_1_3_gpt_template_v1.png](../assets/images/shot_2_1_3_gpt_template_v1.png) | G | [原紀錄第 264 行](shot_prompts_2_1_banana21.md#213) | 保留版本 |
| 2.1.3 | [shot_2_1_3_short_v1.png](../assets/images/shot_2_1_3_short_v1.png) | G | [原紀錄第 51 行](shot_prompts_2_1.md#213george-解惑s03_ots_to_george60mm) | manifest 現行 |
| 2.1.4 | [shot_2_1_4.jpg](../assets/images/shot_2_1_4.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.4 | [shot_2_1_4_banana21_v1.png](../assets/images/shot_2_1_4_banana21_v1.png) | B | [補回原請求](#shot_2_1_4_banana21_v1) | 保留版本 |
| 2.1.4 | [shot_2_1_4_banana21_v2.png](../assets/images/shot_2_1_4_banana21_v2.png) | B | [補回原請求](#shot_2_1_4_banana21_v2) | 保留版本 |
| 2.1.4 | [shot_2_1_4_banana21_v4.png](../assets/images/shot_2_1_4_banana21_v4.png) | B | [原紀錄第 383 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2_1_4_gpt_template_v1.png](../assets/images/shot_2_1_4_gpt_template_v1.png) | G | [原紀錄第 318 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2_1_4_gpt_template_v2.png](../assets/images/shot_2_1_4_gpt_template_v2.png) | G | [原紀錄第 343 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2_1_4_gpt_template_v3.png](../assets/images/shot_2_1_4_gpt_template_v3.png) | G | [原紀錄第 378 行](shot_prompts_2_1_banana21.md#214) | 保留版本 |
| 2.1.4 | [shot_2_1_4_short_v1.png](../assets/images/shot_2_1_4_short_v1.png) | G | [原紀錄第 63 行](shot_prompts_2_1.md#214amy-反問s08_amy_close_up100mm) | 保留版本 |
| 2.1.4 | [shot_2_1_4_short_v2.png](../assets/images/shot_2_1_4_short_v2.png) | G | [原紀錄第 68 行](shot_prompts_2_1.md#214amy-反問s08_amy_close_up100mm) | manifest 現行 |
| 2.1.5 | [shot_2_1_5.jpg](../assets/images/shot_2_1_5.jpg) | L | [原 manifest 快照](#2026-10-13-選版前的-manifest-快照)；有序參考圖檔名未留存 | 舊版（已替換） |
| 2.1.5 | [shot_2_1_5_banana21_v1.png](../assets/images/shot_2_1_5_banana21_v1.png) | B | [補回原請求](#shot_2_1_5_banana21_v1) | 保留版本 |
| 2.1.5 | [shot_2_1_5_banana21_v2.png](../assets/images/shot_2_1_5_banana21_v2.png) | B | [原紀錄第 412 行](shot_prompts_2_1_banana21.md#215) | 保留版本 |
| 2.1.5 | [shot_2_1_5_gpt_compare_v1.png](../assets/images/shot_2_1_5_gpt_compare_v1.png) | G | [原紀錄第 414 行](shot_prompts_2_1_banana21.md#215) | 保留版本 |
| 2.1.5 | [shot_2_1_5_gpt_template_v1.png](../assets/images/shot_2_1_5_gpt_template_v1.png) | G | [原紀錄第 440 行](shot_prompts_2_1_banana21.md#215) | 保留版本 |
| 2.1.5 | [shot_2_1_5_short_v1.png](../assets/images/shot_2_1_5_short_v1.png) | G | [原紀錄第 84 行](shot_prompts_2_1.md#215george-講解-epss07_george_close_up100mm) | manifest 現行 |
| 2.1.6 | [shot_2_1_6_banana21_v1.png](../assets/images/shot_2_1_6_banana21_v1.png) | B | [原紀錄第 478 行](shot_prompts_2_1_banana21.md#216) | 保留版本 |
| 2.1.6 | [shot_2_1_6_gpt_template_v1.png](../assets/images/shot_2_1_6_gpt_template_v1.png) | G | [補回原請求](#shot_2_1_6_gpt_template_v1) | 保留版本 |
| 2.1.6 | [shot_2_1_6_gpt_template_v2.png](../assets/images/shot_2_1_6_gpt_template_v2.png) | G | [補回原請求](#shot_2_1_6_gpt_template_v2) | 保留版本 |
| 2.1.6 | [shot_2_1_6_gpt_template_v3.png](../assets/images/shot_2_1_6_gpt_template_v3.png) | G | [原紀錄第 476 行](shot_prompts_2_1_banana21.md#216) | 保留版本 |
| 2.1.6 | [shot_2_1_6_short_v1.png](../assets/images/shot_2_1_6_short_v1.png) | G | [原紀錄第 98 行](shot_prompts_2_1.md#216esg-概念轉折s09_table_insert50mm) | manifest 現行 |

## 缺件與歷史例外

- 2.1.4 Banana v3 有兩次失敗嘗試，原紀錄保留 OAuth 逾時及未取得正式圖片的錯誤；沒有可歸檔的 v3 圖片，版本跳號保留，不補造圖片。
- 2.1.4 GPT 身體修正的第一次未採用試圖，僅記錄原生路徑 `C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-14593896-6b08-49d4-ba29-51194578b02d.png`，本機不存在；其完整 prompt 與唯一底圖仍見[原紀錄第 347 行](shot_prompts_2_1_banana21.md#214-gpt-身體朝向修正-v32026-10-13)。不以已歸檔的第二次結果冒充。
- 2.1.2 GPT template v1 實際附件為場景、blocks、George、Amy、杯碟／糖罐拼接圖，共五個檔案；prompt 內的圖 5／6 共用最後一張。`D:/kj-openMontage/.tmp/shot_2_1_2_props_5_6.png` 本機缺件，保留[原紀錄第 157 行](shot_prompts_2_1_banana21.md#212)的圖序與來源說明，不改記成 Banana 的六張獨立參考圖。
- 五張舊 JPG 的完整 prompt 與其他資料已保存在本檔「選版前的 manifest 快照」；工具原記錄與圖片尺寸可核對，但參考圖有序檔名、確切模型、實際費用缺乏可核實紀錄，明列未知，不用現行場景圖回填。
- 既有 `_short_`、`_gpt_template_`、`_gpt_compare_` 等檔名依 4.1 保留。後續同一 shot 使用穩定來源簡稱並接續該來源既有最大版本號；失敗且已有紀錄的版本號也保留，不重用。
- 舊紀錄中的 `.tmp/` 是當時請求／輸出位置。兩張已歸檔 Banana v1 的現行圖片位置以上表為準；原始請求不改寫，避免竄改當時實際輸入。

## 從原始請求補回的完整紀錄

以下均為既有生成，不是本次重生。圖片均連結至上方版本索引；參考圖依實際傳入順序列出，路徑轉為專案相對連結，prompt 原文保留。

### shot_2_1_1_banana21_v1

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

### shot_2_1_1_banana21_v2

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

### shot_2_1_2_banana21_v1

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

### shot_2_1_3_banana21_v1

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

### shot_2_1_3_banana21_v2

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

### shot_2_1_3_banana21_v3

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

### shot_2_1_4_banana21_v1

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

### shot_2_1_4_banana21_v2

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

### shot_2_1_5_banana21_v1

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

### shot_2_1_6_gpt_template_v1

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

### shot_2_1_6_gpt_template_v2

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
      "id": "img_shot_2_1_1",
      "type": "image",
      "path": "assets/images/shot_2_1_1.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2_1_1",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the entire 3D spatial geometry, camera perspective, room depth, and vanishing lines for the FULL scene. All foreground, midground, and background cafe elements must align with Image 1's perspective.\n- Image 2: Character identity and attire for Amy.\n- Image 3: Character identity and attire for George.\n- Image 4 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy Image 4's camera angle or frontal layout.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.1 in a single unified 3D perspective strictly matching Image 1:\nThe camera looks over George's (Image 3) right shoulder in the foreground. The coffee table and the entire cafe background (walls, windows, lighting) must rotate coherently with the camera's line of sight, creating realistic 3D parallax depth behind Amy (Image 2).\nAmy leans forward with both hands on the table, face full of panic and anxious pleading. George sits calmly listening.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_amy, char_george, loc_coffee_shop | Agent Native R2I: George右肩過肩中景看Amy慌張求救（全景透視主從對齊）"
    },
    {
      "id": "img_shot_2_1_2",
      "type": "image",
      "path": "assets/images/shot_2_1_2.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2_1_2",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the 3D camera angle (15-degree right turn), close-up framing, and background spatial perspective. Background room vanishing lines must align with this camera view.\n- Image 2: Character identity and attire for Amy.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or frontal layout.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.2 in a single unified 3D perspective strictly matching Image 1:\nAmy (Image 2) sits at the cafe table, clutching the sides of her head with both hands in dramatic, comical panic and frustration, face squished into an exaggerated overwhelmed pout. The background cafe elements rotate coherently with the 15-degree camera angle, smoothly blurred with shallow depth of field.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_amy, loc_coffee_shop | Agent Native R2I: Amy抱頭苦瓜臉特寫抓狂KPI要GG（15度背景透視消逝對齊）"
    },
    {
      "id": "img_shot_2_1_3",
      "type": "image",
      "path": "assets/images/shot_2_1_3.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2_1_3",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the 3D camera angle (15-degree left turn), framing, and room depth. Background cafe depth and vanishing perspective must strictly align with Image 1.\n- Image 2: Character identity and attire for George.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or flat backdrop.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.3 in a single unified 3D perspective strictly matching Image 1:\nGeorge (Image 2) sits at the table, placing a white coffee cup onto a saucer, looking across with a warm reassuring smile. The cafe background rotates coherently with the 15-degree camera orientation, creating realistic 3D depth and soft bokeh.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_george, prop_coffee_cup, loc_coffee_shop | Agent Native R2I: George放下咖啡杯溫和微笑中景（15度左偏室內縱深對齊）"
    },
    {
      "id": "img_shot_2_1_4",
      "type": "image",
      "path": "assets/images/shot_2_1_4.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2_1_4",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the 3D camera angle (45-degree right turn), close-up framing, and background spatial perspective. Background room vanishing lines must align with this diagonal view.\n- Image 2: Character identity and attire for Amy.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or frontal layout.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.4 in a single unified 3D perspective strictly matching Image 1:\nAmy (Image 2) is shown in close-up with head tilted slightly, wide curious eyes and raised eyebrows in surprise and questioning reaction. The cafe background rotates coherently to match the 45-degree camera orientation, smoothly throwing background cafe lights and textures into soft bokeh.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_amy, loc_coffee_shop | Agent Native R2I: Amy歪頭大眼好奇驚訝特寫（45度對角線吧台中島透視對齊）"
    },
    {
      "id": "img_shot_2_1_5",
      "type": "image",
      "path": "assets/images/shot_2_1_5.jpg",
      "source_tool": "agent_native_image",
      "scene_id": "shot_2_1_5",
      "prompt": "3D Pixar animation style, warm studio rim lighting, 8k render.\n\n[Reference Roles & Spatial Hierarchy]:\n- Image 1 (PRIMARY 3D ANCHOR): Strictly governs the front eye-level 3D camera angle, close-up framing, and centered room depth. Background cafe depth and vanishing perspective must strictly align with Image 1.\n- Image 2: Character identity and attire for George.\n- Image 3 (STYLE & MATERIAL ONLY): Reference for cafe materials, color palette, and lighting style only. DO NOT copy its camera angle or flat backdrop.\n\n[Shot Synthesis & 3D Parallax]:\nRender shot 2.1.5 in a single unified 3D perspective strictly matching Image 1:\nGeorge (Image 2) sits at the table, raising his right hand with the index finger extended upward in a clear, confident instructional gesture, speaking warmly. The cafe interior background extends directly behind him with balanced, centered symmetrical perspective matching Image 1's depth.",
      "resolution": "1376x768",
      "format": "jpg",
      "generation_summary": "clp: char_george, loc_coffee_shop | Agent Native R2I: George正面食指開導手勢特寫（正向軸線對稱縱深對齊）"
    }
  ]
}
```

## 2026-10-13 使用者確認採用

依使用者本次逐檔指定更新 manifest：前五鏡沿用既有 id，第六鏡新增 `img_shot_2_1_6`。六張均為內建 image_gen／OpenAI，確切模型與費用未提供，相關選填欄位省略。prompt 沿用各版歷史；short 版本按原紀錄的圖片角色說明＋共用短指令＋該鏡完整短指令拼接，未改寫。實際尺寸皆為 1672×941 PNG。

| shot | 採用圖片 |
|---|---|
| 2.1.1 | [shot_2_1_1_gpt_template_v2.png](../assets/images/shot_2_1_1_gpt_template_v2.png) |
| 2.1.2 | [shot_2_1_2_gpt_template_v1.png](../assets/images/shot_2_1_2_gpt_template_v1.png) |
| 2.1.3 | [shot_2_1_3_short_v1.png](../assets/images/shot_2_1_3_short_v1.png) |
| 2.1.4 | [shot_2_1_4_short_v2.png](../assets/images/shot_2_1_4_short_v2.png) |
| 2.1.5 | [shot_2_1_5_short_v1.png](../assets/images/shot_2_1_5_short_v1.png) |
| 2.1.6 | [shot_2_1_6_short_v1.png](../assets/images/shot_2_1_6_short_v1.png) |

舊圖片與既有生成紀錄保留；專案沒有既有 checkpoint／partial_progress 可同步。本次只確認六張 shot image，不代表整個 assets 階段完成。
