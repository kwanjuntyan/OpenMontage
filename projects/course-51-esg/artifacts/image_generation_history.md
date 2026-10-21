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
| 2.1.7 | [shot_2.1.7_gpt_v1.png](../assets/images/shot_2.1.7_gpt_v1.png) | G | [生成紀錄](#2026-10-19-shot_217-gpt-v1) | manifest 現行 |
| 4.6.1 | `shot_4.6.1_gpt_template_v1.png`（本機未留存） | G | [生成紀錄](#shot_4.6.1_gpt_template_v1) | 未留存副本（僅存紀錄） |
| 4.6.1 | `shot_4.6.1_gpt_template_v2.png`（本機未留存） | G | [生成紀錄](#shot_4.6.1_gpt_template_v2) | 未留存副本（僅存紀錄） |
| 4.6.1 | [shot_4.6.1_gpt_template_v3.png](../assets/images/shot_4.6.1_gpt_template_v3.png) | G | [生成紀錄](#shot_4.6.1_gpt_template_v3) | 保留版本 |
| 4.6.1 | [shot_4.6.1_gpt_template_v4.png](../assets/images/shot_4.6.1_gpt_template_v4.png) | G | [生成紀錄](#shot_4.6.1_gpt_template_v4) | 保留版本 |
| 4.6.1 | [shot_4.6.1_gpt_template_v5.png](../assets/images/shot_4.6.1_gpt_template_v5.png) | G | [生成紀錄](#shot_4.6.1_gpt_template_v5) | manifest 現行 |
| 4.6.1 | [shot_4.6.1_gpt_v6.png](../assets/images/shot_4.6.1_gpt_v6.png) | G | [生成紀錄](#2026-10-19-shot_461-gpt-v6--雙人中景) | 待採用確認 |
| 4.6.2 | [shot_4.6.2_gpt_template_v1.png](../assets/images/shot_4.6.2_gpt_template_v1.png) | G | [生成紀錄](#shot_4.6.2_gpt_template_v1) | 保留版本 |
| 4.6.2 | [shot_4.6.2_gpt_template_v2.png](../assets/images/shot_4.6.2_gpt_template_v2.png) | G | [生成紀錄](#shot_4.6.2_gpt_template_v2) | 保留版本 |
| 4.6.2 | [shot_4.6.2_gpt_template_v3.png](../assets/images/shot_4.6.2_gpt_template_v3.png) | G | [生成紀錄](#shot_4.6.2_gpt_template_v3) | manifest 現行 |
| 4.6.2 | [shot_4.6.2_gpt_v4.png](../assets/images/shot_4.6.2_gpt_v4.png) | G | [生成紀錄](#2026-10-19-shot_462-gpt-v4--小李單人中近景) | 待採用確認 |
| 4.6.3 | [shot_4.6.3_gpt_template_v1.png](../assets/images/shot_4.6.3_gpt_template_v1.png) | G | [生成紀錄](#shot_4.6.3_gpt_template_v1) | manifest 現行 |
| 4.6.3 | [shot_4.6.3_gpt_v2.png](../assets/images/shot_4.6.3_gpt_v2.png) | G | [生成紀錄](#2026-10-19-shot_463-gpt-v2--amy-持手機提醒) | 保留結果；額外白板／版面偏差，未採用 |
| 4.6.3 | [shot_4.6.3_gpt_v3.png](../assets/images/shot_4.6.3_gpt_v3.png) | G | [生成紀錄](#2026-10-19-shot_463-gpt-v3--移除額外白板) | 移除額外白板；便條比例仍有偏差，待確認 |
| 4.6.3 | [shot_4.6.3_gpt_v4.png](../assets/images/shot_4.6.3_gpt_v4.png) | G | [生成紀錄](#2026-10-19-shot_463-gpt-v4--依白模恢復朝向與便條構圖) | 便條構圖改善；軀幹仍偏正面，待確認 |
| 4.6.3 | [shot_4.6.3_gpt_v11.png](../assets/images/shot_4.6.3_gpt_v11.png) | G | [生成紀錄](#2026-10-19-shot_463-gpt-v11--使用者原文五圖重生) | 四張便條裁切大致成立；軀幹右轉不明確、頭部偏大，待確認 |
| 4.6.3 | [shot_4.6.3_gpt_v12.png](../assets/images/shot_4.6.3_gpt_v12.png) | G | [生成紀錄](#2026-10-19-shot_463-gpt-v12--gpt-空景與自身左轉原文) | GPT 空景外觀成立；軀幹偏正面、中藍紙縮窄，待確認 |
| 4.6.3 | [shot_4.6.3_gpt_v13.png](../assets/images/shot_4.6.3_gpt_v13.png) | G | [生成紀錄](#2026-10-19-shot_463-gpt-v13--頭頸肩胸整體朝右) | 頭頸肩胸朝右已改善；沿用 v12 背景，待確認採用 |
| 4.6.4 | [shot_4.6.4_gpt_v1.png](../assets/images/shot_4.6.4_gpt_v1.png) | G | [生成紀錄](#2026-10-19-shot_464-gpt-v1--小李困惑抓頭) | 待採用確認 |
| 4.6.4 | [shot_4.6.4_gpt_v2.png](../assets/images/shot_4.6.4_gpt_v2.png) | G | [生成紀錄](#2026-10-19-shot_464-gpt-v2--人物比例校正未通過) | 比例校正未通過，未採用 |
| 4.6.6 | [shot_4.6.6_gpt_v1.png](../assets/images/shot_4.6.6_gpt_v1.png) | G | [生成紀錄](#2026-10-19-shot_466-gpt-v1--小李委屈特寫) | 構圖仍有差異，待採用確認 |
| 4.6.7 | [shot_4.6.7_gpt_v1.png](../assets/images/shot_4.6.7_gpt_v1.png) | G | [生成紀錄](#2026-10-19-shot_467-gpt-v1--amy-過肩回應) | 身體朝向與構圖仍有差異，待確認 |
| 4.6.7 | [shot_4.6.7_gpt_v2.png](../assets/images/shot_4.6.7_gpt_v2.png) | G | [生成紀錄](#2026-10-19-shot_467-gpt-v2--巨大前景與上半身朝右要求) | 上半身轉向與遮擋仍有差異，待確認 |
| 4.6.8 | [shot_4.6.8_gpt_v1.png](../assets/images/shot_4.6.8_gpt_v1.png) | G | [生成紀錄](#2026-10-19-shot_468-gpt-v1--粉紅便條首幀) | 使用者要求修正 Amy 視線，保留版本 |
| 4.6.8 | [shot_4.6.8_gpt_v2.png](../assets/images/shot_4.6.8_gpt_v2.png) | G | [生成紀錄](#2026-10-19-shot_468-gpt-v2--amy-看向小李) | Amy 視線已修正，待採用確認 |
| 4.6.9 | [shot_4.6.9_gpt_v1.png](../assets/images/shot_4.6.9_gpt_v1.png) | G | [生成紀錄](#2026-10-19-shot_469-gpt-v1--amy-情緒特寫) | 肩胸裁切與白板仍有差異，待確認 |
| 4.6.10 | [shot_4.6.10_gpt_v1.png](../assets/images/shot_4.6.10_gpt_v1.png) | G | [生成紀錄](#2026-10-19-shot_4610-gpt-v1--雙人中景對鏡收尾) | 頭身比例、人物位置及部分白板配置仍有差異，待確認 |
| 4.6.10 | [shot_4.6.10_gpt_v2.png](../assets/images/shot_4.6.10_gpt_v2.png) | G | [生成紀錄](#2026-10-19-shot_4610-gpt-v2--correct-白板參考重生) | 標語落在黃紙、粉紅紙殘留示意線及人物比例有差異，未通過 |
| 4.6.10 | [shot_4.6.10_gpt_v3.png](../assets/images/shot_4.6.10_gpt_v3.png) | G | [生成紀錄](#2026-10-19-shot_4610-gpt-v3--十張便條與相對身高要求) | 十張便條替換改善；小李仍偏高／頭大，人物比例未通過 |

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

1. [references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png](../references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png)
2. [references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_banana.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
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

1. [references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png](../references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png)
2. [references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_banana.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
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

1. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)

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

1. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png)
2. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
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

1. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
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

1. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
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

1. [references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_banana.png)
3. [clp/char_amy.jpeg](../clp/char_amy.jpeg)

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

1. [references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png)
3. [clp/char_amy.jpeg](../clp/char_amy.jpeg)

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

1. [references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png](../references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)

完整 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s07_george_close_up.png] 是場景參考圖，是整體場景，物件，風格，與光影的絕對參考來源；
圖 2 [blocks_blender_s07_george_close_up.png] 是人物定位圖，是人物在場景中的位置、朝向、顯示比例，遮擋的絕對參考來源；
圖 3 [char_george.png] 是人物參考圖，提供 George 的外觀與服裝。

生圖指引：
將圖 2 的藍色人物原位替換為圖 3 人物，維持人物在畫面中的佔位、裁切、與顯示部位，嚴禁縮小人物以展示更多身體。

畫面人物動作描述：
George 下巴略收，帶著肯定的神情與溫和微笑，嘴唇自然微張。只調整頭部姿態與表情，肩膀與軀幹朝向沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

### shot_2.1.6_gpt_template_v1

來源：OM `.tmp/gpt_sixth_template_v1_result.json`；工具代號 G；實際費用未知。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_table_insert_top_block_blender.png](../references/scenes/coffee_shop/cameras/cam_table_insert_top_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s09_table_insert.png]：場景參考圖。
圖 2 [blocks_blender_s09_table_insert.png]：人物定位圖。
圖 3 [char_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
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

1. [references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_table_insert_top_block_blender.png](../references/scenes/coffee_shop/cameras/cam_table_insert_top_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s09_table_insert.png]：場景外觀參考圖。
圖 2 [blocks_blender_s09_table_insert.png]：構圖底圖。
圖 3 [char_george.png]：George 人物參考圖，對應藍色人物。
圖 4 [char_amy.jpeg]：Amy 人物參考圖，對應紅色人物。
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
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/cameras_新增資料夾/empty_gpt_s06_amy_medium_close_up.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/renders_v1/blocks_blender_s06_amy_medium_close_up.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
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
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服人物。

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
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/cameras_新增資料夾/empty_gpt_s06_amy_medium_close_up.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/renders_v1/blocks_blender_s06_amy_medium_close_up.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
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
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服人物。

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
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/cameras_新增資料夾/empty_gpt_s06_amy_medium_close_up.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/renders_v1/blocks_blender_s06_amy_medium_close_up.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
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
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服定位人物。

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
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/cameras_新增資料夾/empty_gpt_s01_wide_two_shot.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/renders_v1/blocks_blender_s01_wide_two_shot.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 圖 4：D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg
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
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的灰色衣服人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側的藍綠色衣服人物。
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
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_empty_gpt.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/b1723_blocks_blender_s01_medium_two_shot.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 圖 4：D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg
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
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的灰色衣服人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側的藍綠色衣服人物。
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
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/cameras_新增資料夾/empty_gpt_s02_medium_two_shot.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/renders/archive/renders_v1/blocks_blender_s02_medium_two_shot.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 圖 4：D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg
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
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的灰色衣服人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側的藍綠色衣服人物。

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
- 圖 1：`../references/scenes/marketing_office/cameras/cam_li_mcu_15deg_empty_gpt.png`
- 圖 2：`../references/scenes/marketing_office/renders/archive/b1723_blocks_blender_s02_li_medium_close_up.png`
- 圖 3：`../clp/char_li.jpeg`
- 圖 4：`../clp/prop_whiteboard_incorrect.png`

#### Prompt 原文

```text
參考圖說明：
圖 1 empty_gpt_s02_li_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s02_li_medium_close_up.png：構圖底圖，其中藍綠色衣服的積木狀人物是待完整替換的定位人物。
圖 3 char_li.jpeg：小李人物參考圖，對應圖 2 的藍綠色衣服人物。
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
- 圖 1：`../references/scenes/marketing_office/cameras/cam_li_mcu_15deg_empty_gpt.png`
- 圖 2：`../references/scenes/marketing_office/renders/archive/b1723_blocks_blender_s02_li_medium_close_up.png`
- 圖 3：`../clp/char_li.jpeg`
- 圖 4：`../clp/prop_whiteboard_incorrect.png`

#### Prompt 原文

```text
參考圖說明：
圖 1 empty_gpt_s02_li_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s02_li_medium_close_up.png：構圖底圖，其中藍綠色衣服的積木狀人物是待完整替換的定位人物。
圖 3 char_li.jpeg：小李人物參考圖，對應圖 2 的藍綠色衣服人物。
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
- 圖 1：`../references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_gpt.png`
- 圖 2：`../references/scenes/marketing_office/renders/archive/b1723_blocks_blender_s03_amy_medium_close_up.png`
- 圖 3：`../clp/char_amy.jpeg`
- 圖 4：`../clp/prop_whiteboard_incorrect.png`
- 圖 5：`../clp/prop_smartphone.png`

#### Prompt 原文

```text
參考圖說明：
圖 1 empty_gpt_s03_amy_medium_close_up.png：行銷部場景外觀參考圖。
圖 2 blocks_blender_s03_amy_medium_close_up.png：構圖底圖，其中灰色衣服的積木狀人物是待完整替換的定位人物。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的灰色衣服人物。
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

## 2026-10-18 shot_2.1.1 GPT 生圖

### shot_2.1.1_gpt_template_v4

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 使用者要求：使用本輪已提供的 Prompt 在 GPT 生圖；Prompt 原文與五張獨立參考圖依序送出，僅生成一張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法可靠報價。
- 輸出：[shot_2.1.1_gpt_template_v4.png](../assets/images/shot_2.1.1_gpt_template_v4.png)
- 原生來源：C:/Users/user/.codex/generated_images/01a14f82-04fd-7e80-9bb9-de04e4c7cd62/exec-797d942b-6469-4cf2-a379-f23f2e1ed60c.png
- transparent_background=false；工具耗時 91.1 秒。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png](../references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 Prompt：

```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_banana.png：場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 prop_coffee_cup.png：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。兩人直接坐入圖 2 的既有木椅，不額外增加椅子。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。

畫面描述：
這是一張以 40mm 鏡頭、接近坐姿眼高並略微俯拍的雙人中景。George 位於畫面左側，Amy 位於右側，兩人隔著木桌相向而坐。畫面呈現兩人的完整頭部、上半身、伸向桌面的前臂與手部；腿部只呈現圖 2 中露出的範圍，沿用桌面的遮擋與畫面下緣的裁切。Amy 愁眉微皺，一手握著小匙，匙端仍在面前杯中的拿鐵裡，呈現攪拌時抬眼望向 George 求助的瞬間；George 神情沉著，注視 Amy 聆聽。依上述表演調整 Amy 的握匙手勢與兩人的表情、視線，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不呈現定位方塊或參考圖展示排版，不加入字幕。
```

結果檢視：

- 1672×941 RGB PNG，接近但非精確 16:9；Pillow 完整解碼成功，專案副本與原始輸出 SHA256 相同。
- George 左、Amy 右，兩人坐入木椅隔桌相向；角色外觀、Amy 皺眉抬眼求助與握匙入杯、George 聆聽成立，未見定位方塊或新增字幕。
- 相較 blocks，人物頭頂上移、留白減少，身體佔比與姿勢有變動；George 的手改成扶杯，未完全沿用 blocks。
- 本版為待確認候選；未替換 asset_manifest.json 中已採用的 shot_2.1.1_gpt_template_v2.png，未修改分鏡、未追加生成或推進整體 assets 核准。


## 2026-10-18 shot_2.1.2 GPT 生圖

### shot_2.1.2_gpt_template_v2

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 使用者要求：使用本輪兩份 Prompt 在 GPT 各生成一張；本鏡 Prompt 原文與五張獨立參考圖依序送出，僅生成一張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法可靠估算。
- 輸出：[shot_2.1.2_gpt_template_v2.png](../assets/images/shot_2.1.2_gpt_template_v2.png)
- 原生來源：C:/Users/user/.codex/generated_images/01a14f82-04fd-7e80-9bb9-de04e4c7cd62/exec-f255bde0-4a3f-4d14-b5a4-62d2c1a4bc87.png
- transparent_background=false。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_banana.png：場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左下角的藍色人物局部。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 prop_coffee_cup.png：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。Amy 直接坐入既有木椅，不額外增加椅子。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。左下方糖罐的白色罐身與金色金屬蓋沿用圖 1。

畫面描述：
這是一張以 65mm 鏡頭、接近坐姿眼高微側拍攝的 Amy 中特寫。Amy 位於畫面中右側，完整頭部、頸部、肩膀與胸部可見；手臂及手部只呈現圖 2 下緣可見的部分，下半身在畫外。George 只保留左下角極少量局部前景，頭部與臉部不入鏡，Amy 是畫面中唯一可辨識的面孔。前景杯碟與糖罐沿用圖 2 的位置、遮擋及下緣裁切。Amy 已停止攪拌，眉心皺起、嘴角下垂，嘴唇微張、頭部微偏，望向畫面左側的 George，呈現為工作績效焦慮、無奈訴苦的瞬間；小幅攤手只在原取景容納的範圍內呈現，不為展示手勢擴大取景。依上述表演調整表情、視線、頭部輕微姿態與可見手勢，肩膀及軀幹維持圖 2 的朝向，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不呈現定位方塊或參考圖展示排版，不加入字幕。
```

結果檢視：

- 1672×941 RGB PNG，接近但非精確 16:9；Pillow 完整解碼成功，專案副本與原始輸出 SHA256 相同。
- Amy 是唯一可辨識面孔，皺眉微張嘴、向左看與下方攤手成立；白色杯碟、白色金蓋糖罐及咖啡機背景保留，未見定位方塊或新增字幕。
- 相較 blocks，Amy 頭頂留白減少、主體向右且比例偏大；George 左下角局部前景明顯擴大，杯碟與糖罐位置亦有偏移，未完全遵守原取景與配置。
- 本版為待確認候選；未替換 asset_manifest.json 中已採用的 shot_2.1.2_gpt_template_v1.png，未修改分鏡、未追加生成或推進整體 assets 核准。


## 2026-10-18 shot_2.1.3 GPT 生圖

### shot_2.1.3_gpt_template_v2

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 使用者要求：使用本輪兩份 Prompt 在 GPT 各生成一張；本鏡 Prompt 原文與五張獨立參考圖依序送出，僅生成一張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法可靠估算。
- 輸出：[shot_2.1.3_gpt_template_v2.png](../assets/images/shot_2.1.3_gpt_template_v2.png)
- 原生來源：C:/Users/user/.codex/generated_images/01a14f82-04fd-7e80-9bb9-de04e4c7cd62/exec-a34faa16-d4ad-45ba-afe6-367d1fc66878.png
- transparent_background=false。

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png](../references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_cup.png](../clp/prop_coffee_cup.png)

完整 Prompt：

```text
參考圖說明：
圖 1 cam_george_ots_amy_empty_banana.png：場景外觀參考圖。
圖 2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 prop_coffee_cup.png：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。兩人直接坐入既有木椅，不額外增加椅子。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。

畫面描述：
這是一張以 60mm 鏡頭、接近坐姿眼高並略微俯拍，從 Amy 肩後看向 George 的過肩中景。George 位於畫面左側中景，完整頭部、上半身與圖 2 中可見的前臂、手部入鏡；Amy 的後腦、頸部與肩背位於右側近景，沿用圖 2 的大小、裁切及遮擋關係，不轉頭露出正臉。George 面前的杯碟完整入鏡，焦點落在 George 與持杯的手。George 帶著溫和安撫的微笑，注視 Amy，嘴唇自然微張，一手握著原有咖啡杯的杯柄，準備將杯子放回面前的原杯碟；杯底尚未接觸碟面，保留清楚空隙，杯碟上不留第二只重複的杯子。Amy 以頭肩背影安靜聆聽。依上述表演調整 George 的持杯手勢、原杯子的位置及表情、視線，肩膀與軀幹維持圖 2 的朝向，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不呈現定位方塊或參考圖展示排版，不加入字幕。
```

結果檢視：

- 1672×941 RGB PNG，接近但非精確 16:9；Pillow 完整解碼成功，專案副本與原始輸出 SHA256 相同。
- George 左中景、Amy 右前景背影的過肩關係成立，George 溫和微笑、握杯柄且杯底與空杯碟保留清楚空隙，未重複新增杯子；未見定位方塊或新增字幕。
- 相較 blocks，George 頭部與上身變大、略偏左，頭頂留白減少；Amy 頭肩的佔位與裁切亦有差異，未完全對齊原構圖。
- 本版為待確認候選；未替換 asset_manifest.json 中已採用的 shot_2.1.3_short_v1.png，未修改分鏡、未追加生成或推進整體 assets 核准。


## 2026-10-18 shot_2.1.2 GPT 圖 5 咖啡組參考 v3

### shot_2.1.2_gpt_template_v3

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 補記上一輪已生成並保存的 v3；該輪在寫入歷史前中斷，本次未重生此圖。圖 5 改為 prop_coffee_set.png，說明仍為「咖啡杯碟外觀參考圖」。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法可靠估算。每次一張，transparent_background=false。
- 輸出：[shot_2.1.2_gpt_template_v3.png](../assets/images/shot_2.1.2_gpt_template_v3.png)
- 原生來源：C:/Users/user/.codex/generated_images/01a14f82-04fd-7e80-9bb9-de04e4c7cd62/exec-ba40fdb4-cad9-4d93-99ef-8a70d433781b.png

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_banana.png：場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左下角的藍色人物局部。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 prop_coffee_set.png：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。Amy 直接坐入既有木椅，不額外增加椅子。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。左下方糖罐的白色罐身與金色金屬蓋沿用圖 1。

畫面描述：
這是一張以 65mm 鏡頭、接近坐姿眼高微側拍攝的 Amy 中特寫。Amy 位於畫面中右側，完整頭部、頸部、肩膀與胸部可見；手臂及手部只呈現圖 2 下緣可見的部分，下半身在畫外。George 只保留左下角極少量局部前景，頭部與臉部不入鏡，Amy 是畫面中唯一可辨識的面孔。前景杯碟與糖罐沿用圖 2 的位置、遮擋及下緣裁切。Amy 已停止攪拌，眉心皺起、嘴角下垂，嘴唇微張、頭部微偏，望向畫面左側的 George，呈現為工作績效焦慮、無奈訴苦的瞬間；小幅攤手只在原取景容納的範圍內呈現，不為展示手勢擴大取景。依上述表演調整表情、視線、頭部輕微姿態與可見手勢，肩膀及軀幹維持圖 2 的朝向，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不呈現定位方塊或參考圖展示排版，不加入字幕。
```

結果檢視：

- 1672×941 RGB PNG，接近但非精確 16:9；Pillow 完整解碼成功，專案副本與原始輸出 SHA256 相同。
- Amy 的焦慮訴苦與單手攤開成立，白色糖罐仍為金色金屬蓋；George 左側局部前景明顯擴大，Amy 頭頂留白減少，人物比例、手勢與杯罐配置未完全沿用 blocks。
- 未見新增字幕或參考圖展示排版；本版為待確認候選，未替換 asset_manifest.json 中已採用的 shot_2.1.2_gpt_template_v1.png，未修改分鏡、未追加生成或推進整體 assets 核准。


## 2026-10-18 shot_2.1.2 GPT 圖 5 咖啡組參考 v4

### shot_2.1.2_gpt_template_v4

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 使用本次使用者貼上的 Prompt 原文；圖 5 說明改為「咖啡杯碟和糖罐的外觀參考圖」，正文仍保留糖罐白色罐身與金色金屬蓋沿用圖 1 的指令，未自行改寫。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法可靠估算。每次一張，transparent_background=false。
- 輸出：[shot_2.1.2_gpt_template_v4.png](../assets/images/shot_2.1.2_gpt_template_v4.png)
- 原生來源：C:/Users/user/.codex/generated_images/01a14f82-04fd-7e80-9bb9-de04e4c7cd62/exec-ac14d281-87eb-4262-8090-234f0a1cd38c.png

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_banana.png：場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左下角的藍色人物局部。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 prop_coffee_set.png：咖啡杯碟和糖罐的外觀參考圖。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。
將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。Amy 直接坐入既有木椅，不額外增加椅子。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。左下方糖罐的白色罐身與金色金屬蓋沿用圖 1。
畫面描述：
這是一張以 65mm 鏡頭、接近坐姿眼高微側拍攝的 Amy 中特寫。Amy 位於畫面中右側，完整頭部、頸部、肩膀與胸部可見；手臂及手部只呈現圖 2 下緣可見的部分，下半身在畫外。George 只保留左下角極少量局部前景，頭部與臉部不入鏡，Amy 是畫面中唯一可辨識的面孔。前景杯碟與糖罐沿用圖 2 的位置、遮擋及下緣裁切。Amy 已停止攪拌，眉心皺起、嘴角下垂，嘴唇微張、頭部微偏，望向畫面左側的 George，呈現為工作績效焦慮、無奈訴苦的瞬間；小幅攤手只在原取景容納的範圍內呈現，不為展示手勢擴大取景。依上述表演調整表情、視線、頭部輕微姿態與可見手勢，肩膀及軀幹維持圖 2 的朝向，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不呈現定位方塊或參考圖展示排版，不加入字幕。
```

結果檢視：

- 1672×941 RGB PNG，接近但非精確 16:9；Pillow 完整解碼成功，專案副本與原始輸出 SHA256 相同。
- Amy 是唯一可辨識面孔，皺眉微張嘴、向左看及下方攤手成立；糖罐仍為白色罐身與金色金屬蓋，未帶入圖 5 的木蓋。相較 blocks，George 左側前景擴大、Amy 頭頂留白減少，人物比例與雙手可見範圍、杯罐位置仍有偏移，未完全遵守原構圖。
- 未見新增字幕或參考圖展示排版；本版為待確認候選，未替換 asset_manifest.json 中已採用的 shot_2.1.2_gpt_template_v1.png，未修改分鏡、未追加生成或推進整體 assets 核准。


## 2026-10-18 shot_2.1.2 GPT 木頭蓋糖罐 v5

### shot_2.1.2_gpt_template_v5

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 使用者要求：本次 Prompt 原文與五張獨立參考圖依序送出；糖罐改為「白色罐身與木頭蓋沿用圖5」，未自行改寫其餘文字，僅生成一張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法可靠估算。transparent_background=false。
- 輸出：[shot_2.1.2_gpt_template_v5.png](../assets/images/shot_2.1.2_gpt_template_v5.png)
- 原生來源：C:/Users/user/.codex/generated_images/01a14f82-04fd-7e80-9bb9-de04e4c7cd62/exec-195916c3-bda7-4525-96e0-b3e976f743ca.png

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png)
3. [clp/char_george.png](../clp/char_george.png)
4. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_banana.png：場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左下角的藍色人物局部。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 prop_coffee_set.png：咖啡杯碟和糖罐的外觀參考圖。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。
將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。Amy 直接坐入既有木椅，不額外增加椅子。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。左下方糖罐的白色罐身與木頭蓋沿用圖5。
畫面描述：
這是一張以 65mm 鏡頭、接近坐姿眼高微側拍攝的 Amy 中特寫。Amy 位於畫面中右側，完整頭部、頸部、肩膀與胸部可見；手臂及手部只呈現圖 2 下緣可見的部分，下半身在畫外。George 只保留左下角極少量局部前景，頭部與臉部不入鏡，Amy 是畫面中唯一可辨識的面孔。前景杯碟與糖罐沿用圖 2 的位置、遮擋及下緣裁切。Amy 已停止攪拌，眉心皺起、嘴角下垂，嘴唇微張、頭部微偏，望向畫面左側的 George，呈現為工作績效焦慮、無奈訴苦的瞬間；小幅攤手只在原取景容納的範圍內呈現，不為展示手勢擴大取景。依上述表演調整表情、視線、頭部輕微姿態與可見手勢，肩膀及軀幹維持圖 2 的朝向，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不呈現定位方塊或參考圖展示排版，不加入字幕。
```

結果檢視：

- 1672×941 RGB PNG，接近但非精確 16:9；Pillow 完整解碼成功，專案副本與原始輸出 SHA256 相同。
- 糖罐已呈現白色罐身與帶圓鈕的木頭蓋，符合本次指定變更；Amy 的焦慮表情、微張嘴、向左看與攤手成立。
- 相較 blocks，George 左側前景明顯擴大，左上邊緣露出少量白髮；Amy 頭頂留白減少，人物比例、手勢及杯罐位置／裁切仍有差異，未完全遵守原構圖。
- 未見新增字幕或參考圖展示排版；本版為待確認候選，未替換 asset_manifest.json 中已採用的 shot_2.1.2_gpt_template_v1.png，未修改分鏡、未追加生成或推進整體 assets 核准。



## 2026-10-19 shot_2.1.7 GPT v1

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成，預備後續 I2V 首幀。
- 使用者確認前一則回覆的完整 prompt，原文與下列五張參考圖依序送出，僅生成一張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法取得報價；transparent_background=false。
- 輸出：[shot_2.1.7_gpt_v1.png](../assets/images/shot_2.1.7_gpt_v1.png)
- 原生來源：C:/Users/servi/.codex/generated_images/01a151db-f372-7411-9451-41b4a31ab9a3/exec-dbee10e3-6008-4385-bce8-07769a635b47.png

有序參考圖：

1. [references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_banana.png](../references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_banana.png)
2. [references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png](../references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png)
3. [clp/char_amy.jpeg](../clp/char_amy.jpeg)
4. [clp/char_george.png](../clp/char_george.png)
5. [clp/prop_coffee_set.png](../clp/prop_coffee_set.png)

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_ots_george_empty_banana.png：場景外觀參考圖。
圖 2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 4 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐的外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3、圖 4，不採用其展示姿態或構圖。兩人直接坐入既有木椅，不額外增加椅子。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。桌面咖啡杯碟與木蓋糖罐的外觀採用圖 5，數量、位置與遮擋沿用圖 2，不為展示道具而移動人物或補出被遮住的物件。

畫面描述：
這是一張坐姿近眼高、60mm 視角的過肩中景，從 George 身後越過他的肩膀看向 Amy。畫面中有兩人：George 的後腦、肩背與局部手臂佔據左前景，呈柔焦；Amy 位於右中景，完整頭部、上半身及桌邊可見手部依圖 2 呈現，下半身維持原有遮擋與裁切。Amy 保持圖 2 的坐姿，上半身尚未前傾，眉心微蹙，眼神帶著畏難與遲疑，望向對坐的 George，嘴唇輕合，呈現準備開口探問的瞬間。George 維持面向 Amy 的坐姿與原有遮擋。雙方手臂及手部姿態沿用圖 2。背景維持原木服務牆與義式咖啡機，保留日間溫暖光線，淺景深聚焦 Amy 的眼睛與擔憂神情。除上述表情、視線與景深調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

結果檢視：

- 1672×940 RGB PNG，接近但非精確 16:9；Pillow 完整解碼成功，專案副本與原始輸出 SHA256 相同。
- George 左前景過肩、Amy 右中景成立；Amy 閉嘴、皺眉、望向 George 的遲疑擔憂神情成立，角色外觀與暖色咖啡館延續參考圖，未見字幕或參考圖展示排版。
- 相較 blocks，Amy 頭部放大、頭頂留白減少且位置右移；George 頭頂被上緣裁切；Amy 可見手部姿態改變，原本被 George 遮住的糖罐與前景杯子露出，構圖與遮擋未完全符合指令。
- 2026-10-19 使用者已重新製作並更新 `assets/images/shot_2.1.7_gpt_v1.png`，確認登記至 `artifacts/asset_manifest.json`（`img_shot_2.1.7`）供 Scene Player 預覽；尚未製作 I2V，也未推進整體 assets 核准。

## 2026-10-19 shot_4.4.1 GPT v1 — Amy 腿部修正

- 使用者要求：修正左側 Amy 出現三條腿的錯誤；本次在既有 kj-cinematic assets 階段做 I2I 局部編修。
- 輸出：`assets/images/shot_4.4.1_gpt_v1.png`；原圖 `assets/images/shot_4.4.1.png` 保留，採用版本待確認，未更新 manifest。
- 工具／供應商：內建 `image_gen`／OpenAI；確切模型、用量及費用未提供，事前已告知無法可靠估價；單張，`transparent_background=false`。
- 有序輸入：圖 1（唯一編輯底圖）`D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.4.1.png`。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a15234-02e5-7383-8cdc-4870c76251b8/exec-24ddddcf-46f9-4936-b9f5-9b1852ae1d2b.png`。
- 檢視：Amy 多出的下方灰色褲管已移除，現為兩條腿；人物、雙人構圖與場景整體保留。生成式編修仍有螢幕小字及衣料細節變動，未宣稱局部之外像素完全相同。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG。沒有既有 checkpoint／partial_progress 可同步；未進行 I2V 或整體 assets 核准。

完整 Prompt：

```text
Use case: precise-object-edit.
Input image 1 is the edit target: shot_4.4.1.png.
以原圖為基礎，只修正畫面左側灰色套裝短棕髮女性 Amy 的腿部解剖錯誤。她目前看起來有三條腿；請移除大腿下方、靠近椅面與畫面底部中央偏左的多餘灰色褲管／第三條腿，局部重建被它遮住的椅面或背景。Amy 必須只有兩條腿：骨盆連接兩條大腿、兩個膝蓋及兩條小腿，雙膝自然靠攏、兩條小腿自然向下延伸至原圖底部裁切外，坐姿清楚合理。保留她原有的灰色西裝褲材質、紋理、衣褶與光影，保留原本放在腿上的手及其位置。編修只限 Amy 腰部以下有問題的褲子與緊鄰的必要修補區，盡量減少變動。
嚴格保留所有其他內容：Amy 的臉、髮型、笑容、頭部與身體比例、白襯衫、灰西裝外套、雙手與上身姿勢；右側 Linda 的全身與坐姿；兩張椅子、桌子、電腦螢幕上的原有文字與圖表、鍵盤、滑鼠、伺服器、玻璃、便利貼、書架、盆栽、窗戶；原有 3D 動畫風格、色彩、光線、相機角度及畫面取景。保持原圖的橫向畫布與尺寸比例，不縮放、不裁切、不改動任何其他人物或物件，不新增文字或水印。只輸出一張完成的修正版。
```

## 2026-10-19 shot_4.6.1 GPT v6 — 雙人中景

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；使用者確認沿用雙人中景、雙手垂放方向，並明確要求使用上一輪完整 Prompt 在 GPT 生圖、存入 assets/images。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，生成前已告知無法報價。
- 呼叫：一次、一張；transparent_background=false；以下 Prompt 原文送出，五張參考圖按列示順序使用，未追加條件。
- 輸出：[shot_4.6.1_gpt_v6.png](../assets/images/shot_4.6.1_gpt_v6.png)；GPT 來源接續既有 template v1～v5，檔名採穩定來源簡稱 gpt。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-126e2386-f6ed-4bca-88ad-5bd2e26229ce.png`。
- 檢視：Amy 左、小李右，雙人中景；角色外觀、空手垂放、Amy 微張嘴看鏡頭與小李閉嘴看向 Amy 成立，無殘留白模、手機、海報或字幕。兩人頭部較 blocks 放大、頭頂留白減少，白板部分文字／字形有變動，未完全對齊底圖與參考圖。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG（接近但非精確 16:9）；來源／目的地 SHA256 相同：`7e2c98433d3569d3bd60a2c5f116481eb3024c9f3a3c5515ffc49c02c68ab9de`。未裁切或放大。
- 狀態：待使用者採用確認；保留舊版本與現行 asset_manifest，無既有 checkpoint／partial_progress 可同步，未生成影片或推進整體 assets 核准。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：行銷部場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的紅色定位人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側的藍色定位人物。
圖 5 prop_whiteboard_incorrect.png：既有白板上的便條紙與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、身體朝向、畫面尺度、顯示範圍與遮擋關係。

將兩個定位人物完整替換為 Amy 與小李，包含畫面中所有可見的身體、服裝及手部，不殘留方塊軀幹、長條四肢或定位人物外殼。只呈現圖 2 中可見的部位，不補出畫外身體。Amy 的外觀與服裝採用圖 3；小李的外觀與服裝採用圖 4，保留花襯衫、白色內搭與棕色長褲，不加眼鏡。不採用人物參考圖的展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 5 白板書寫面內的十張彩色便條紙及圖文，依圖 2 的白板透視貼合到既有白板上，保留顏色、相對位置、比例與原有文字，不自行改寫。圖 5 只提供白板內容；板框、筆槽、腳架及遮擋沿用圖 2。被人物遮住或位於畫外的內容維持不可見，不縮排便條紙，也不移動人物來露出文字。

畫面描述：
這是一張接近眼高、略俯視的正面雙人中景。Amy 位於左側，小李位於右側，兩人從頭部至部分大腿入鏡，下緣裁切依圖 2；白板位於兩人後方中央，左右保留既有窗戶與辦公區。定格在 Amy 開口介紹「最後一站，我們要來挖掘行銷部的寶藏」的瞬間：她帶著開朗、期待的笑容，眼睛看向鏡頭，嘴巴微張，雙臂自然垂放。小李嘴巴閉合，帶著期待的微笑，頭部與視線略朝向 Amy，安靜聆聽，雙手自然垂放於身側。兩人空手，不持海報或手機。保持原有的人物間距、頭頂留白、身體比例與白板遮擋，不推近鏡頭、不放大頭部。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```


## 2026-10-19 shot_4.6.2 GPT v4 — 小李單人中近景

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；使用者明確要求使用上一輪完整 Prompt 在 GPT 生圖，存入 assets/images。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，生成前已告知無法報價。
- 呼叫：一次、一張；transparent_background=false；以下 Prompt 原文送出，四張參考圖按列示順序使用，未追加條件。
- 輸出：[shot_4.6.2_gpt_v4.png](../assets/images/shot_4.6.2_gpt_v4.png)；GPT 來源接續既有 template v1～v3，檔名採穩定來源簡稱 gpt。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-bf575116-ddcb-4098-ac96-17021125a6aa.png`。
- 檢視：小李單人中近景、花襯衫與白色內搭、開口微笑及朝左視線成立；Amy、雙手、海報、眼鏡、字幕與殘留白模均未出現。相較 blocks，頭頂留白減少、肩線與胸口可見範圍改變，白板頂框露出且便條紙位置／尺度變動，未保持完整的底圖構圖與整板映射；白板文字亦未逐字一致。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG（接近但非精確 16:9）；來源／目的地 SHA256 相同：`96b1923cdd5fcdcc1b889ec00930a3a3d5cfc7eaf3fc3823e26327f136991d02`。未裁切或放大。
- 狀態：待使用者採用確認；asset_manifest 仍指向缺件的 template v3，本次未替換或補造該版本；無既有 checkpoint／partial_progress 可同步，未生成影片或推進整體 assets 核准。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_mcu_15deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_mcu_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_li_mcu_15deg_empty_gpt.png：行銷部場景外觀參考圖。
圖 2 cam_li_mcu_15deg_block_blender.png：構圖底圖。
圖 3 char_li.jpeg：小李人物參考圖，對應圖 2 的藍色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板上的便條紙與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、身體朝向、畫面尺度、顯示範圍與遮擋關係。

將藍色定位人物完整替換為小李，包含畫面中可見的頭部、頸部、肩膀、胸口與上臂，不殘留方塊軀幹、長條手臂或定位人物外殼。只呈現圖 2 中可見的部位，不補出畫外身體、手掌或手指。小李的外觀與服裝採用圖 3，保留棕色上梳短髮、花襯衫及白色內搭，不加眼鏡；不採用人物參考圖的展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 4 白板書寫面內的彩色便條紙與圖文，依圖 2 的白板透視貼合到既有白板上。以整塊白板對應圖 4 的完整版面，再依本鏡取景自然裁切，只呈現可見區域的部分內容。保留各張便條紙的顏色、相對位置、比例與原有文字，不自行改寫。位於畫外或被小李遮住的部分維持不可見，不將全部便條紙縮小、移位或重新排列到可見區域。

圖 4 只提供白板內容；白板位置、大小、板框與遮擋沿用圖 2，不新增白板，也不移動人物來露出文字。

畫面描述：
這是一張略帶側角的小李單人中近景。小李位於畫面中央偏右，呈現完整頭部、頸部、肩膀、胸口與部分上臂，下方軀幹及手臂依圖 2 的畫面邊界裁切，雙手不入鏡。白板位於畫面左側與人物後方，右側保留既有窗戶。定格在小李興奮開口介紹新產品標語的瞬間：他帶著自豪、熱切的笑容，眉毛微揚，嘴巴張開正在說話，視線看向畫面左側、位於畫外的 Amy；肩膀、軀幹及可見手臂維持圖 2 的姿態。畫面只出現小李一人，Amy、雙手與海報均在畫外。保持原有頭部尺度、頭頂留白、人物位置與白板遮擋，不推近鏡頭、不將人物移到正中央。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```


## 2026-10-19 shot_4.6.3 GPT v2 — Amy 持手機提醒

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；使用者明確要求使用上一輪完整 Prompt 在 GPT 生圖，存入 assets/images。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，生成前已告知無法報價。
- 呼叫：一次、一張；transparent_background=false；以下 Prompt 原文送出，五張參考圖按列示順序使用，未追加條件。
- 輸出：[shot_4.6.3_gpt_v2.png](../assets/images/shot_4.6.3_gpt_v2.png)；GPT 來源接續既有 template v1，檔名採穩定來源簡稱 gpt。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-027d1b0a-d625-4ccd-b44a-cb1147a82c39.png`。
- 檢視：Amy 單人、皺眉微張嘴、朝右看畫外小李、畫面右側抬手直向持手機成立；手機螢幕朝角色，背面三鏡頭朝觀眾，無來電介面、字幕、小李或海報。但模型額外生成一塊帶框白板，原背景上方的線條便條仍存在，新增板內便條紙重新排列且文字有變動；背景配置未通過。人物頭身／肩線與底圖有差異，手機上緣高於下巴，亦未完全遵循要求。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG（接近但非精確 16:9）；來源／目的地 SHA256 相同：`fe3427518e849e096fb27a0476ae98f4ae5a6177b99e4ab030a03881d8729212`。未裁切或放大。
- 狀態：保留結果並回報背景缺陷，未追加生成或標為品質通過；asset_manifest 仍指向缺件的 template v1，本次未替換或補造該版本；無既有 checkpoint／partial_progress 可同步，未生成影片或推進整體 assets 核准。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_gpt.png：行銷部場景外觀參考圖。
圖 2 cam_amy_mcu_15deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板上的便條紙與圖文內容參考。
圖 5 prop_smartphone.png：Amy 手中手機的實體外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、身體朝向、畫面尺度與裁切。持手機所需的前臂及手部調整依下方畫面描述，其餘沿用圖 2。

將紅色定位人物完整替換為 Amy，包含畫面中可見的頭部、頸部、肩膀、軀幹與手臂，不殘留方塊軀幹、長條四肢或定位人物外殼。Amy 的外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或構圖，不補出畫外下半身。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

將圖 4 白板書寫面內的彩色便條紙與圖文，依圖 2 的白板透視貼合到既有白板上。以整塊白板對應圖 4 的完整版面，再依本鏡取景自然裁切，只呈現可見區域的部分內容。保留便條紙的顏色、相對位置、比例與原有文字，不自行改寫。位於畫外或被 Amy、手臂及手機遮住的內容維持不可見，不將全部便條紙縮小、移位或重新排列到可見區域。圖 4 只提供白板內容，不改變既有板框與配置。

手機的機身顏色、邊框、厚度、背蓋及鏡頭模組採用圖 5，尺寸與 Amy 的手掌相稱。圖 5 只提供同一支手機的實體外觀，不採用其多視圖排列、背景或「主管來電」介面。畫面只出現一支手機，螢幕朝向 Amy，鏡頭主要看見背面與側邊，不新增面向觀眾的搜尋頁面或文字介面。

畫面描述：
這是一張略帶側角的 Amy 單人中近景。Amy 位於畫面中央偏左，呈現完整頭部、頸部、肩膀與上半身，下緣裁切沿用圖 2；白板位於右側與人物後方，左側保留既有辦公桌、隔板、螢幕與窗戶。定格在 Amy 已用手機查證、正開口提醒小李的瞬間：她眉頭微皺，神情專注且帶著擔憂，嘴巴微張，視線看向畫面右側、位於畫外的小李。將畫面右側的前臂彎曲抬起，手掌自然握住直向手機，置於胸前偏右、低於下巴的位置，螢幕朝向自己，不遮住臉部；手指自然環握機身，不穿透手機。另一側手臂沿用底圖的垂放方向，手掌維持在畫外。畫面只出現 Amy 一人，小李與海報均在畫外。保持原有頭部尺度、頭頂留白、人物位置與背景裁切，不推近鏡頭、不將 Amy 移到正中央。除上述持手機姿態、表情及視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、警告字卡或額外疊字。
```


## 2026-10-19 shot_4.6.3 GPT v3 — 移除額外白板

- Pipeline／階段：course-51-esg／kj-cinematic／assets；使用者指出 v2 圖片不對並要求重新生成，本輪以 I2I 局部修正多出的白板背景，沿用角色與手機表演。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，執行前已告知；一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v3.png](../assets/images/shot_4.6.3_gpt_v3.png)，保留 v2 與所有既有紀錄。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-999a26fe-9160-475e-a284-8de5632e794d.png`。
- 原因與調整：v2 將整板內容參考生成為第二塊帶框白板；本輪明確指定移除新增板框，以同機位空景恢復原白板，內容圖只提供四張可見便條的文字。
- 檢視：新增的銀色矩形白板框與重複便條已移除；原圖 Amy 的臉、擔憂表情、向右視線、服裝及持手機姿勢整體保留。四張綠／藍便條仍有位置與比例偏差，中間淺藍便條較小且移右，右下綠色便條沒有依空景被右邊界裁切；文字亦有變動，未宣稱完整背景或像素對齊。手機高度沿用 v2。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG；來源／目的地 SHA256 相同：`702ba79e189b3db2be384074f86ecf6075479cdb3a51833f4298f61844edc1b7`。未裁切或放大。
- 狀態：待使用者確認，未更新 asset_manifest／scene_plan，未追加生成，未推進影片或整體 assets 核准。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.3_gpt_v2.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_gpt.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖用途：
圖 1 shot_4.6.3_gpt_v2.png：本次需要修正的原圖。保留 Amy 與手機，只修正錯誤的白板背景。
圖 2 cam_amy_mcu_15deg_empty_gpt.png：同一機位的正確背景，決定唯一既有白板的位置、大小、透視、裁切及彩色便條紙的精確配置。
圖 3 prop_whiteboard_incorrect.png：只提供便條紙內的文字內容，絕對不要把這張照片的整塊白板或板框放進場景。

以圖 1 為基礎，重建 Amy 後方及右側的白板區域，使它恢復圖 2 的背景配置。圖 1 新增的、從手機上方延伸到畫面右下方的銀色矩形板框，以及框內重新縮排的小便條紙，全部移除。這裡始終只有圖 2 原本的一塊大白板，其上下及右側邊界在本鏡畫外，不要在畫面內新增頂框、底框、右框、第二塊板或板中板。

將圖 2 的白板表面與既有便條紙按相同取景直接恢復到圖 1 背景：畫面頂緣是被上邊界裁切的綠色、淺藍色便條紙；中間偏右是原有的一張大淺藍色便條紙；右下方是被畫面右邊界裁切的綠色便條紙。這些紙張的位置、尺度、裁切與空白間隔完全依圖 2，人物及手機前景自然遮擋它們。原本畫外的黃色、粉紅色便條紙不要搬進本鏡，也不要為了顯示全部文案而縮小紙張。

只將每張既有紙張內的深色橫線替換為圖 3 對應便條紙的文字：頂緣綠色對應「100% 地球救星！」便條、頂緣淺藍色對應「純天然無毒擁抱」便條、中間淺藍色對應「綠色神話」便條、右下綠色對應「天然之魂」便條。以整塊白板的完整版面對應，再自然裁切文字；被畫面裁掉或被人物遮住的文字不要補到其他空白處。圖 3 的板框、紙張以外物件及拍攝構圖完全忽略。最後不留下原本的裝飾橫線，也不再添加另一套重複便條。

嚴格保留圖 1 的 Amy：同一張臉、髮型、綠色眼睛、微皺眉、擔憂且微張嘴的表情、向畫面右側的視線、灰色西裝與白襯衫、人物大小及位置、身體姿勢、手臂與握手機的手指。保留同一支深灰三鏡頭手機，螢幕朝 Amy，背面朝觀眾，不新增介面。保留圖 1 左側窗戶、辦公桌、隔板、電腦與暖色日光。只修正白板區域，不改人物、不改相機、不裁切、不新增人物或海報。

輸出一張 16:9 彩色修正版，不加入字幕、對話框、警告字卡或水印。
```


## 2026-10-19 shot_4.6.3 GPT v4 — 依白模恢復朝向與便條構圖

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部重生；使用者要求 Amy 身體及臉均朝右、白板版面依原圖 2 再貼原圖 4 便條，並確認視線看向畫外右側小李。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，生成前已告知無法估價；一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v4.png](../assets/images/shot_4.6.3_gpt_v4.png)，保留舊版本。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-3c490642-0db5-4ca9-a5f5-ee6823fd45b1.png`。
- 調整：回到原五張參考圖，不使用 v3 作底圖；逐張指定圖 2 四張便條的輪廓、尺寸、裁切及圖 4 內容對應；明寫肩膀、胸口、軀幹和臉均朝畫面偏右。
- 檢視：Amy 臉與視線朝畫外右側，微皺眉、張嘴提醒，手機上緣低於下巴，單人與手機外觀成立；軀幹僅微朝右，正面可見範圍仍多，不能宣稱已完全符合使用者要求的身體轉向。四張綠／藍便條的位置、尺寸及右緣裁切較 v3 接近 blocks，未新增板框或其他顏色便條；中間藍紙左緣仍略偏右、上排文字可見範圍與原裁切有差異，字形與換行亦重新生成，未達精確貼圖。肩線高度及人物對便條的遮擋與 blocks 仍有差別。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG；來源／目的地 SHA256 相同：`28141a699054f2c34407b83813ebece2f811bebbaa4fd9867e13ab952fb421fe`。未裁切、放大或程式合成。
- 狀態：待使用者檢視，未更新 asset_manifest／scene_plan，未追加生成或推進影片階段。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_gpt.png：行銷辦公室的材質、風格與光影參考。
圖 2 cam_amy_mcu_15deg_block_blender.png：本次唯一構圖底圖，決定人物身體與臉部朝向、鏡位、尺度，以及白板與每張便條紙的位置、尺寸、透視、裁切和遮擋。
圖 3 char_amy.jpeg：Amy 的人物外觀與服裝參考，對應圖 2 紅色定位人物。
圖 4 prop_whiteboard_incorrect.png：只提供既有便條紙的顏色、紙張質感及各張紙上的圖文，不提供本鏡構圖。
圖 5 prop_smartphone.png：Amy 手中手機的實體外觀參考。

生圖指引：
直接以圖 2 為編輯底圖製作這張分鏡。保留圖 2 的取景、透視、背景配置、人物佔位、頭部尺度、頭頂留白、肩線、軀幹朝向與下緣裁切。將場景材質、風格與光影更新為圖 1 的外觀，空間構圖仍依圖 2。

將紅色定位人物完整替換為圖 3 的 Amy：棕色微捲短髮、綠色眼睛、灰色西裝外套與白色襯衫。移除所有白模方塊、簡化頭部與長條四肢。圖 3 只提供外觀，不使用其正面展示姿態。Amy 的肩膀、胸口、軀幹和臉部都要依圖 2 朝畫面偏右，呈自然的斜側面；不能把胸口與兩肩攤平成正對鏡頭，再只將眼睛或頭部轉右。上半身轉向與臉朝向必須一致，保持圖 2 的人物位置與相對角度。

白板直接保留圖 2 原有的那一塊板。先鎖定圖 2 四張可見便條紙的外輪廓，再在這些相同輪廓內貼合圖 4 對應便條的圖文，替換原本的黑色示意橫線。不要把圖 4 的整板照片、板框或其他便條紙置入畫面。四張紙的位置與裁切如下，百分比只用於辨認圖 2 的既有輪廓：
- 頂緣偏中間的綠色紙：位於畫面寬約 47%～73%，只見頂部被畫面上緣裁掉的下半部分，下緣約在畫面高 15%。貼入圖 4 左上「100% 地球救星！」那張紙的對應內容，文字也隨原紙裁切。
- 頂緣右側的淺藍色紙：左緣約在畫面寬 77%，延伸到右邊界外，上部被頂緣裁切，下緣約在畫面高 15%。貼入圖 4 上排「純天然無毒擁抱」那張紙的對應內容。
- 中間偏右的大淺藍色紙：輪廓約在畫面寬 47%～74%、高 50%～82%；左下區域自然被 Amy 遮住。貼入圖 4 左下「綠色神話」那張紙的內容。維持原尺寸與位置，不往右移來露出完整文字。
- 右下綠色紙：左緣約在畫面寬 78%，上緣約在高 68%，下緣約在高 96%，右側延伸出畫面。貼入圖 4「天然之魂」那張紙的內容，保留右邊界裁切。

各張紙上的原有文字以圖 4 為準，不改寫、不重排，不為讀完文案而縮小紙張或文字；文字與紙張共同接受圖 2 的透視、人物遮擋及畫面邊緣裁切。畫外的黃色與粉紅色便條維持畫外。白板上下及右側板框維持畫外，不新增第二塊白板或內框，不保留重複的黑色示意橫線。

手機的深灰色機身、厚度、背蓋與三鏡頭模組依圖 5，尺寸與手掌相稱。只生成一支手機，不採用圖 5 的多視圖排版、背景或「主管來電」介面。

畫面描述：
這是一張略帶側角的 Amy 單人中近景，Amy 位於中央偏左，完整頭部、頸部、雙肩與上半身入鏡，人物尺度與胸前下緣裁切沿用圖 2，左側保留原有辦公桌、隔板、螢幕與窗戶，右側是原有大白板的局部。定格在 Amy 已用手機查證、正開口提醒畫外小李的瞬間：她的身體與臉都朝畫面偏右，眉頭微皺，神情專注而擔憂，嘴巴微張，雙眼明確看向畫外右側、與她交談的小李，不看鏡頭也不低頭看手機。只將畫面右側的前臂彎曲抬起，自然握住直向手機，放在胸前偏右，手機上緣低於下巴，螢幕朝向 Amy，鏡頭看見背面與側邊，手指自然環握機身；另一側手臂保持圖 2 的垂放方向，手掌在畫外。白板便條紙自然被人物及手機遮擋。畫面只出現 Amy 一人，小李與海報均在畫外。除持手機所需的前臂與手部、表情及視線外，其餘姿態、身體朝向及構圖沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、警告字卡、水印或額外疊字。
```


## 2026-10-19 shot_4.6.4 GPT v1 — 小李困惑抓頭

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；使用者明確要求使用上一輪完整 Prompt 在 GPT 生圖並存入 assets/images。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，生成前已告知無法估價；一次、一張，transparent_background=false。
- 呼叫：以下 Prompt 原文送出，四張參考圖依列示順序使用，未追加條件。
- 輸出：[shot_4.6.4_gpt_v1.png](../assets/images/shot_4.6.4_gpt_v1.png)。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-1d4db774-e6d5-4673-8512-96664f1889e0.png`。
- 檢視：小李單人、花襯衫／白色內搭、畫面右側抬手抓頭、困惑眉形與微張嘴、朝畫外左側的視線成立；Amy、海報、眼鏡、問號與殘留白模均未出現。相較 blocks，頭部較大、頭頂留白減少，臉略傾斜且視線偏左上；白板部分便條紙的尺寸、位置、裁切與文字換行仍有變動，未達構圖或圖文精確轉貼。未額外生成第二塊白板。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG（接近但非精確 16:9）；來源／目的地 SHA256 相同：`7e50e558feab9e75e8ad3f665f7630428ba729faa73d4fe23572a4c43905aa03`。未裁切、放大或程式合成。
- 狀態：待使用者採用確認，未更新 asset_manifest／scene_plan；無既有 checkpoint／partial_progress 可同步，未生成影片或推進整體 assets 核准。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_ms_15deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_ms_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_li_ms_15deg_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_li_ms_15deg_block_blender.png：構圖底圖，決定人物朝向、佔位、尺度，以及白板與便條紙的位置、大小、透視、裁切和遮擋。
圖 3 char_li.jpeg：小李人物參考圖，對應圖 2 的藍色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板上各張便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭頂留白、身體朝向、顯示範圍與遮擋關係。抓頭所需的手臂與手部調整依下方畫面描述，其餘沿用圖 2。

將藍色定位人物完整替換為小李，包含畫面中可見的頭部、頸部、肩膀、軀幹與手臂，不殘留方塊軀幹、長條四肢或定位人物外殼。外觀與服裝採用圖 3，保留棕色上梳短髮、藍底彩色花襯衫及白色內搭，不加眼鏡；不採用人物參考圖的展示姿態或構圖。肩膀、胸口與臉部都沿用圖 2 朝畫面偏左的角度，不改成正面面向鏡頭。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置；保留既有白板、下方筆槽與右側窗戶的位置和可見範圍。

白板便條紙的構圖完全依圖 2。保留每張既有紙張的外輪廓、位置、大小、傾斜角度與間距，只把紙張內的黑色示意橫線替換為圖 4 對應便條的圖文：
上排由左至右，可見局部淺藍紙對應「純天然無毒擁抱」、粉紅紙對應「零碳奇蹟」、黃紙對應「環保魔法」。
中排左側黃紙對應「地球救星毯」，人物後方粉紅紙對應「絕對循環」。
下排由左至右，局部綠紙對應「天然之魂」、黃紙對應「永續至尊」、被人物遮擋的粉紅紙對應「環保教主」。

各張紙內的完整文字及字樣以圖 4 為準，貼合圖 2 原有紙張的透視，並自然接受畫面邊緣裁切與人物遮擋。不要為了讀完整段文案而縮小、移動或重新排列便條紙；原本畫外或被人物擋住的內容維持不可見。圖 4 的整板構圖、板框、腳架及其他物件不參與生成，不新增第二塊白板，不保留重複的示意橫線。

畫面描述：
這是一張近眼高、略帶側角的小李單人中景。小李位於畫面中央偏右，呈現完整頭部、頸部、肩膀與上半身，下緣裁切沿用圖 2；白板在左側與人物後方，右側保留原有窗戶及窗外樹景。定格在小李因聽見「漂綠」而愣住、抓著頭側發問的瞬間：他的身體和臉朝畫面偏左，視線看向畫外左側的 Amy，眉毛一高一低、眉心微皺，眼睛略睜大，嘴巴微張，流露不理解而非興奮的神情。畫面右側的手臂屈肘抬起，指尖自然接觸同側耳朵上方的髮際，呈現困惑抓頭的姿勢，不遮住眼睛與臉；另一側手臂沿用垂放方向，手掌與原海報維持在畫外下方，不補進畫面。畫面只出現小李一人，Amy 在畫外。保持原人物位置、頭部尺度、肩線、頭頂留白及背景裁切，不推近鏡頭，不把小李移到正中央。除上述抓頭姿勢、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、問號符號、對話框、水印或額外疊字。
```


## 2026-10-19 shot_4.6.4 GPT v2 — 人物比例校正未通過

- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 修正；使用者指出人物變矮，要求重新校對。
- 校對原因：v1 相較 blocks 有頭部放大、歪頭及可見頸部縮短，造成矮壯感；以同畫幅比例目視比對，不能用未入鏡的全身量測宣稱實際身高改變。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，生成前已告知；一次、一張，transparent_background=false。
- 調整：沿用原四張參考圖，在原 Prompt 加入 blocks 頭頂約高 15%、下巴約高 51%、頭部中心約寬 57%、頭寬約 18%、肩頸交界約高 60% 的定位，要求頭頸直立、成人比例並保持抓頭。
- 輸出：[shot_4.6.4_gpt_v2.png](../assets/images/shot_4.6.4_gpt_v2.png)，保留 v1。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-04aef566-c333-4a8b-ac33-6208f8df7a0a.png`。
- 檢視：抓頭、花襯衫、困惑表情保留；頭部大小與 v1 仍接近，頭頂目視約高 8%、下巴約高 56%，未恢復 blocks 的定位，人物比例校正未通過。便條紙內容與間距也有重繪，未宣稱背景完全不變。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG；來源／目的地 SHA256 相同：`29911dcb73be3c1982f3136c98b65dd3645ef31850538286e290a77ed8a858f3`。未拉伸、裁切或程式合成。
- 狀態：未通過本次人物比例要求，未採用；asset_manifest／scene_plan 未改。下一修正方案為以此圖局部 I2I 校正頭頸與相連手臂，尚未執行。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_ms_15deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_ms_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_li_ms_15deg_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_li_ms_15deg_block_blender.png：構圖底圖，決定人物朝向、佔位、尺度，以及白板與便條紙的位置、大小、透視、裁切和遮擋。
圖 3 char_li.jpeg：小李人物參考圖，對應圖 2 的藍色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板上各張便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭頂留白、身體朝向、顯示範圍與遮擋關係。抓頭所需的手臂與手部調整依下方畫面描述，其餘沿用圖 2。本次優先校正人物頭身比例：先按圖 2 的位置建立直立的頸部、肩膀與軀幹，再放入同尺度的角色頭部，不能把人物畫成大頭、短頸、矮壯的比例。

將藍色定位人物完整替換為小李，包含畫面中可見的頭部、頸部、肩膀、軀幹與手臂，不殘留方塊軀幹、長條四肢或定位人物外殼。外觀與服裝採用圖 3，保留棕色上梳短髮、藍底彩色花襯衫及白色內搭，不加眼鏡；不採用人物參考圖的展示姿態或構圖。肩膀、胸口與臉部都沿用圖 2 朝畫面偏左的角度，不改成正面面向鏡頭。

人物尺度以圖 2 為準，以下均為整張畫面的相對座標：包含髮型的頭頂約在畫面高度 15%，下巴約在高度 51%，頭部中心約在畫面寬度 57%，頭部連頭髮的寬度約佔畫面 18%；髮型也必須容納於這個範圍，不因蓬鬆頭髮而額外放大頭部。頸部自然直立並清楚可見，從下巴銜接到約在畫面高度 60% 的肩頸交界，雙肩高度及透視沿用圖 2；軀幹保持挺直，自肩膀自然向畫面下緣延伸並被裁切，不壓縮胸腹，不縮肩、彎腰或蹲低。保留圖 3 成年男性的自然頭身關係與五官，不畫成幼童或 Q 版。不要靠放大整個人物、改鏡頭遠近或上下拉伸畫面來校正比例。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置；保留既有白板、下方筆槽與右側窗戶的位置和可見範圍。

白板便條紙的構圖完全依圖 2。保留每張既有紙張的外輪廓、位置、大小、傾斜角度與間距，只把紙張內的黑色示意橫線替換為圖 4 對應便條的圖文：
上排由左至右，可見局部淺藍紙對應「純天然無毒擁抱」、粉紅紙對應「零碳奇蹟」、黃紙對應「環保魔法」。
中排左側黃紙對應「地球救星毯」，人物後方粉紅紙對應「絕對循環」。
下排由左至右，局部綠紙對應「天然之魂」、黃紙對應「永續至尊」、被人物遮擋的粉紅紙對應「環保教主」。

各張紙內的完整文字及字樣以圖 4 為準，貼合圖 2 原有紙張的透視，並自然接受畫面邊緣裁切與人物遮擋。不要為了讀完整段文案而縮小、移動或重新排列便條紙；原本畫外或被人物擋住的內容維持不可見。圖 4 的整板構圖、板框、腳架及其他物件不參與生成，不新增第二塊白板，不保留重複的示意橫線。

畫面描述：
這是一張近眼高、略帶側角的小李單人中景。小李位於畫面中央偏右，呈現完整頭部、頸部、肩膀與上半身，下緣裁切沿用圖 2；白板在左側與人物後方，右側保留原有窗戶及窗外樹景。定格在小李因聽見「漂綠」而愣住、抓著頭側發問的瞬間：他的身體和臉朝畫面偏左，頭部保持圖 2 的直立狀態，不向肩膀歪頭、低頭或仰頭；視線平視畫外左側的 Amy，眉毛一高一低、眉心微皺，眼睛略睜大，嘴巴微張，流露不理解而非興奮的神情。畫面右側的手臂屈肘抬起，指尖自然接觸同側耳朵上方的髮際，呈現困惑抓頭的姿勢，不遮住眼睛與臉；另一側手臂沿用垂放方向，手掌與原海報維持在畫外下方，不補進畫面。畫面只出現小李一人，Amy 在畫外。保持原人物位置、頭部尺度、肩線、頭頂留白及背景裁切，不推近鏡頭，不把小李移到正中央。除上述抓頭姿勢、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、問號符號、對話框、水印或額外疊字。
```


## 2026-10-19 shot_4.6.6 GPT v1 — 小李委屈特寫

- 使用者授權：使用修改後的 shot 4.6.6 prompt 在 GPT 生圖；本次僅生成 1 張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、預估費用與實際費用均未由工具提供，不記為零。
- 模態／參數：四圖 W2I；referenced_image_paths 依下列順序，transparent_background=false。原樣使用 `artifacts/shot_4.6.6_image_prompt.md` 的修改後 CU prompt，未追加條件。
- 輸出：`assets/images/shot_4.6.6_gpt_v1.png`；1672×941、RGB PNG、2143270 bytes，保留工具原生尺寸，未裁切或縮放。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-b37f864b-3c3c-4ca2-af72-f80b4117cbd9.png`。
- 驗證：已看生成結果並對照指定 Blender 構圖、完整解碼圖片，原始檔與專案副本 SHA-256 相同：`2fcc68d892d30937bc8ae8b5c61dd937414ef3fffe8c579e60bc7ff4a13445ed`。
- 視覺檢視：小李單人、花襯衫／白內搭、無眼鏡、委屈張嘴辯解與朝左視線成立，Amy／雙手／海報未入鏡。頭頂留白明顯減少（目視約 7%，blocks 約 24%），頭部偏大且歪頭仰視，肩部／衣領露出多於 blocks；便條的位置、尺度、裁切與部分圖文仍有差異，尤其底部粉紅紙露出較多。未完全符合指定構圖，不記為構圖校正通過。
- 採用狀態：待使用者檢視；未改 asset_manifest、scene_plan 或 prompt，未自動追加生成，原始輸出保留。

### 實際送入的參考圖（順序固定）

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_cu_emotion_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_li_cu_emotion_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

### 實際送入的完整 prompt

```text
參考圖說明：
圖 1 cam_li_cu_emotion_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_li_cu_emotion_block_blender.png：本鏡情緒特寫的構圖底圖，決定頭部與頸部的位置、大小、朝向、裁切，以及白板便條紙的透視與遮擋。
圖 3 char_li.jpeg：小李人物參考圖，對應圖 2 的藍色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板上各張便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部尺度、頭頂上方留白、下緣裁切與遮擋關係。本鏡以頭部和頸部為主，下緣只露少量肩線；不要拉遠補出胸口、上臂或雙手，也不要再推近、放大頭部或把人物往上移。

將定位人物完整替換為小李，只替換圖 2 可見的頭部、頸部與畫面下緣少量肩部，不殘留簡化頭部、方塊頸部或藍色白模。外觀採用圖 3，保留棕色上梳短髮與五官特徵；可見衣領及肩部延續藍底彩色花襯衫與白色內搭，不加眼鏡。不採用人物參考圖的展示姿態或構圖。頭部、頸部與僅露出的肩線沿用圖 2 朝畫面偏左的方向，不改成正面直視鏡頭。

保持圖 2 的頭部尺度、頭頂與下巴位置、可見頸部長度，不因委屈表情而縮頸、彎腰或降低人物位置。肩膀微收只作用於下緣原本可見的少量肩線，不為了呈現肩膀動作而擴大取景。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置；白板局部位於左側與人物後方，右側保留既有窗戶及窗外樹景。

白板便條紙的構圖完全依圖 2。保留每張紙的外輪廓、位置、大小、間距與裁切，只將黑色示意橫線替換為圖 4 的對應圖文：
左上被畫面裁切的粉紅紙對應「零碳奇蹟」，上方黃紙對應「環保魔法」。
左側只露部分的黃紙對應「地球救星毯」，人物頭部後方的粉紅紙對應「絕對循環」。
畫面最下緣僅露出的黃紙與粉紅紙邊，分別對應「永續至尊」與「環保教主」，維持細窄裁切，不補出整張紙。

紙張與文字一起依圖 2 的透視、畫面邊界及頭頸遮擋自然裁切，不為了讀完整段文案而移位、縮小或重排便條紙；畫外內容保持畫外。圖 4 只提供便條內容，不採用其整板構圖、板框或其他物件，不新增第二塊白板，不留下重複的示意橫線。

畫面描述：
這是一張略帶側角的小李單人情緒特寫。小李的頭部位於中央偏右，呈現完整頭部、可見頸部與下緣極少量肩線，其餘身體依圖 2 裁在畫外；左後方為便條白板局部，右側為窗戶。定格在小李收起先前的興奮，正向 Amy 小聲辯解「可是我們的產品真的環保啊？」的瞬間：臉朝畫面偏左，視線看向畫外左側的 Amy，眉毛內端略抬、眉心微皺，嘴角微微下壓，嘴巴小幅張開，呈現委屈、不解又想解釋的神情，不是憤怒爭辯、興奮微笑或誇張哭泣。下緣可見的肩線輕微內收，頭頸保持自然，不歪頭縮頸。畫面只出現小李一人；Amy、胸口、手臂、雙手與原海報均在畫外，不新增抓頭或其他手勢。除上述表情、視線及可見肩線微收外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入毛毯、寶特瓶、數據插圖、字幕、對話框、水印或額外疊字。
```



## 2026-10-19 staff_office cam_amy_ms_45deg empty GPT v1

- 用途：loc_staff_office 同機位空景 W2I；使用者指定局部生成，未推進其他階段。
- 工具：內建 image_gen／OpenAI；確切模型與費用未提供，未推測或填零；transparent_background=false。
- 圖片：[成品](../references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_gpt.png)；原生 1672×941，依使用者明確同意以 Pillow Lanczos 放大為 3840×2160、16:9、RGB PNG；非原生 4K 細節。
- 原生輸出：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-cdd69c5f-750b-4aa5-9418-ac997b9d3afb.png；保留原始檔。
- 驗證：已目視生成結果及完整解碼 4K 輸出；SHA-256 93a4624b48d809f0c5e2f679c6e902127a8f5612ebd06efa463c0260dc930723。
- 視覺檢視：主要構圖、空椅、隔板與螢幕遮擋接近白模，暖色日光及材質取自 CLP；非逐像素鎖定。
- 採用狀態：待使用者檢視，未更改 asset_manifest 或 scene_plan；v1 在中斷前已完成放大存檔，本次補記；v2 保留舊圖另存。

### 參考圖（實際順序）

1. D:/Dropbox/kj-om-projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_blender.png

### 完整提示詞

```text
參考圖說明：
圖 1 loc_staff_office.jpg：員工辦公室的場景外觀參考，提供材質、物件設計、風格、色調、光線，以及辦公桌道具、電腦螢幕、辦公椅與書櫃的外觀元素。
圖 2 cam_amy_ms_45deg_empty_blender.png：唯一的編輯底圖與構圖依據，決定鏡頭角度、透視、裁切、物件位置、尺度與遮擋。

生圖指引：
直接以圖 2 為編輯底圖進行精緻材質與外觀替換，完整保留圖 2 的攝影機位置、朝向、視野、畫面邊界、透視與空間配置。所有既有桌椅、螢幕、隔板、書本、盆栽、書櫃、窗戶與百葉窗保持圖 2 的相對位置、投影大小與遮擋關係。不要採用圖 1 的攝影機、裁切或擺放位置，不把圖 2 改成圖 1 的構圖，也不要拉遠、推近、旋轉、平移鏡頭或增加可見天花板。

將圖 2 所有表面替換成圖 1 的精緻外觀：柔和低飽和的藍綠色織物隔板與細緻白色框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細緻黑色網布辦公椅、白色書櫃及色調協調的書籍與文件夾、灰色紋理地毯、白色陶瓷盆栽與自然綠葉。將圖 1 的辦公用品設計、電腦螢幕設計、書籍文件及書櫃細節運用於圖 2 的對應物件，讓簡化白模成為完成的動畫電影場景；螢幕維持底圖所見的正反面及方向。辦公桌道具僅採用圖 1 中的元素，配置受圖 2 的桌面範圍、現有位置與遮擋約束，不另添無關裝飾或重新安排辦公室。

色調與光線以圖 1 為準：溫暖柔和的日光穿過百葉窗，搭配清爽柔和的室內填光、自然接觸陰影、細膩反射、窗外具有空氣透視的城市景色；曝光平衡，受控飽和度，保留布料、木紋、網布與地毯質感。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
一張空無一人的員工辦公室 45 度中景，構圖逐一對齊圖 2。前景左下的大型深色電腦螢幕維持原本輪廓、傾斜方向與遮擋，鍵盤位於前景桌面；空的網布辦公椅位於中央偏右，椅背上緣、扶手及下緣裁切沿用底圖；右下四本直立文件夾保持原位置與比例。藍綠隔板沿原透視切分辦公區，中後景螢幕、椅背、左側高盆栽、右後方書櫃與上方窗戶百葉窗均留在原位置。僅在原鏡頭中完成圖 1 的材質、風格與光線轉換，不加入任何人物、人影、動物或人形物件。

輸出：
只輸出一張完整的橫幅 16:9 PNG，要求 3840 × 2160 像素的 4K 高品質成圖。滿版畫面，無黑邊、無比較拼圖、無字幕、無浮水印、無標誌。
```


## 2026-10-19 staff_office cam_amy_ms_45deg empty GPT v2

- 用途：loc_staff_office 同機位空景 W2I；使用者指定局部生成，未推進其他階段。
- 工具：內建 image_gen／OpenAI；確切模型與費用未提供，未推測或填零；transparent_background=false。
- 圖片：[成品](../references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_gpt_v2.png)；原生 1672×941，依使用者明確同意以 Pillow Lanczos 放大為 3840×2160、16:9、RGB PNG；非原生 4K 細節。
- 原生輸出：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-e8a7f77f-5b34-42db-8742-b1abe3626757.png；保留原始檔。
- 驗證：已目視生成結果及完整解碼 4K 輸出；SHA-256 7921e16f2685c60649b0728f1997350385ed4212da04a9989b08b4adfd6a4804。
- 視覺檢視：主要機位、裁切與物件配置接近白模；前景四冊的封殼厚度、紙頁分層、網布椅與木紋可辨，無人物或動物。窗邊小盆栽與背景書籍細節有生成差異，非逐像素鎖定。
- 採用狀態：待使用者檢視，未更改 asset_manifest 或 scene_plan；v1 在中斷前已完成放大存檔，本次補記；v2 保留舊圖另存。

### 參考圖（實際順序）

1. D:/Dropbox/kj-om-projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_blender.png

### 完整提示詞

```text
參考圖說明：
圖 1 loc_staff_office.jpg：員工辦公室的場景外觀參考，提供材質、物件設計、風格、色調、光線，以及辦公桌道具、電腦螢幕、辦公椅與書櫃的外觀元素。
圖 2 cam_amy_ms_45deg_empty_blender.png：唯一的編輯底圖與構圖依據，決定鏡頭角度、透視、裁切、物件位置、尺度與遮擋。

生圖指引：
直接以圖 2 為編輯底圖進行精緻材質與外觀替換，完整保留圖 2 的攝影機位置、朝向、視野、畫面邊界、透視與空間配置。所有既有桌椅、螢幕、隔板、書本、盆栽、書櫃、窗戶與百葉窗保持圖 2 的相對位置、投影大小與遮擋關係。不要採用圖 1 的攝影機、裁切或擺放位置，不把圖 2 改成圖 1 的構圖，也不要拉遠、推近、旋轉、平移鏡頭或增加可見天花板。

將圖 2 所有表面替換成圖 1 的精緻外觀：柔和低飽和的藍綠色織物隔板與細緻白色框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細緻黑色網布辦公椅、白色書櫃及具有精緻實體質感、色調協調的書籍與檔案夾、灰色紋理地毯、白色陶瓷盆栽與自然綠葉。將圖 1 的辦公用品設計、電腦螢幕設計、書籍文件及書櫃細節運用於圖 2 的對應物件，讓簡化白模成為完成的動畫電影場景；螢幕維持底圖所見的正反面及方向。辦公桌道具僅採用圖 1 中的元素，配置受圖 2 的桌面範圍、現有位置與遮擋約束，不另添無關裝飾或重新安排辦公室。

重點材質要求：辦公桌上的道具、電腦螢幕、書櫃、書本與檔案夾都必須使用圖 1 的元素與精緻質感。所有書本與檔案夾都是有真實結構的物件：清楚可辨的封面厚度、書脊摺線、裝訂邊、層疊紙頁與細微不齊的紙邊、布面或紙面的封殼肌理、恰當的柔和高光和接觸陰影；前景四冊檔案夾依圖 2 保持數量、位置、外部尺度和裁切，呈現圖 1 的藍灰、灰綠、米白與暖灰質感，不保留白模單一光滑色塊或空白長方體的簡化外觀。右後方書櫃內的書本各有可信的薄厚差異、封面與紙頁、細節與陰影，保持圖 2 原有書櫃位置、大小和層板排列。電腦背殼有細緻霧面塑料與柔和圓角，桌面木紋尺度自然，金屬與塗裝框架反射適度。細節必須在合適景深中可辨，不用過度模糊掩蓋道具。

色調與光線以圖 1 為準：溫暖柔和的日光穿過百葉窗，搭配清爽柔和的室內填光、自然接觸陰影、細膩反射、窗外具有空氣透視的城市景色；曝光平衡，受控飽和度，保留布料、木紋、網布與地毯質感。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
一張空無一人的員工辦公室 45 度中景，構圖逐一對齊圖 2。前景左下的大型深色電腦螢幕維持原本輪廓、傾斜方向與遮擋，鍵盤位於前景桌面；空的網布辦公椅位於中央偏右，椅背上緣、扶手及下緣裁切沿用底圖；右下四本直立文件夾保持原位置與比例。藍綠隔板沿原透視切分辦公區，中後景螢幕、椅背、左側高盆栽、右後方書櫃與上方窗戶百葉窗均留在原位置。僅在原鏡頭中完成圖 1 的材質、風格與光線轉換，不加入任何人物、人影、動物或人形物件。

輸出：
只輸出一張完整的橫幅 16:9 PNG，要求 3840 × 2160 像素的 4K 高品質成圖。滿版畫面，無黑邊、無比較拼圖、無字幕、無浮水印、無標誌。
```

## 2026-10-19 shot_4.6.7 GPT v1 — Amy 過肩回應

- 使用者授權：依本輪貼上的完整 prompt，在 GPT 生成 shot_4.6.7 並存入專案 assets/images；本次生成 1 張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、預估費用與實際費用未由工具提供，不記為零。
- 模態／參數：五圖 W2I；referenced_image_paths 依下列順序，transparent_background=false。實際 prompt 以本次使用者原文為準，包含「她的臉與視線、身體都要朝畫面右側的小李」，未追加條件；先前 prompt 文件不冒充本次實際請求。
- 輸出：`assets/images/shot_4.6.7_gpt_v1.png`；1672×941、RGB PNG、2065830 bytes，保留工具原生尺寸，未裁切或縮放。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-a354bb75-80f7-41a4-9b8f-8e9a7af15b16.png`。
- 驗證：已看圖並對照本鏡要求，完整解碼圖片；原始檔與專案副本 SHA-256 相同：`f1e64a3552ffe2bdbe7cedd62f815b0e9068c2cdad80823a01c6aca8fb5fbced`。
- 視覺檢視：兩人過肩關係成立，Amy 在左側、臉與視線朝右側小李，小李後腦與花襯衫肩部在右側前景且頭頂／右側被裁切；手機／雙手／海報未入鏡。Amy 軀幹仍偏正面，未充分呈現使用者指定的身體朝右；Amy 頭部相對 blocks 放大，便條紙尺度／位置／裁切與部分文字有差異，前景小李也偏模糊，未完全符合深景深要求。不記為構圖與身體朝向通過。
- 採用狀態：待使用者檢視；未改 asset_manifest、scene_plan 或先前 prompt 文件，未自動追加生成，原始輸出保留。

### 實際送入的參考圖（順序固定）

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_ots_li_ms_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_ots_li_ms_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

### 實際送入的完整 prompt

```text
參考圖說明：
圖 1 cam_amy_ots_li_ms_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_amy_ots_li_ms_block_blender.png：本鏡過肩構圖底圖，決定兩人的位置、尺度、前後距離、可見範圍與遮擋。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側中景的紅色定位人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側前景的藍色定位人物。
圖 5 prop_whiteboard_incorrect.png：既有白板便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭身比例與裁切。Amy 保持左側中景的大小、頭頂留白、頭頸長度與肩線高度；小李維持右側近距離前景的頭側、後腦、頸部及肩部局部，頭頂與右側仍被畫面裁切。不要縮小前景小李以露出完整頭部，也不要放大 Amy、拉近鏡頭或改成兩人並排。

將紅色定位人物完整替換為圖 3 的 Amy，將藍色定位人物完整替換為圖 4 的小李；只呈現圖 2 可見的部位，不殘留白模、方塊頸部或色塊身體。人物圖只提供外觀與服裝，不採用其展示姿態或構圖。小李沿用棕色上梳短髮與藍底彩色花襯衫，不加眼鏡。Amy 的頭部與視線依本鏡表演轉向畫面右側的小李；其餘人物站位與身體尺度沿用圖 2。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留牆面日光、Amy 後方既有辦公椅、桌緣與右側白板局部；採近眼高、深景深，避免強烈散景掩蓋人物或背景配置。

白板便條紙的外輪廓、位置、大小、透視與遮擋完全依圖 2，只將示意橫線替換為圖 5 的對應圖文。上緣露出的綠紙對應「100%地球救星」，白板左下的藍紙對應「綠色神話」，其右下綠紙對應「天然之魂」；小李遮擋後僅露出的下方黃紙、右側中段粉紅紙、右下粉紅紙，分別對應「永續至尊」、「絕對循環」、「環保教主」。其餘被小李遮住或位於畫外的內容維持不可見。文字跟著紙張與人物遮擋自然裁切，不為了讀完整內容而移動紙張或人物。圖 5 不提供整板構圖，不新增第二塊白板，也不把便條上的誇大文案改成正確宣傳文案。

畫面描述：
這是一張從小李身後越過肩膀看向 Amy 的過肩中景，畫面只有兩人。小李的頭側、後腦與肩部佔據右側前景，身體朝向左側中景的 Amy；Amy 可見完整頭部、頸部、肩膀與上半身，下半身及雙手依圖 2 裁在畫外。定格在 Amy 開始溫和回應小李的瞬間：她的臉與視線、身體都要朝畫面右側的小李，下巴極輕微下收，呈現開始輕點頭的狀態，嘴唇微啟準備說「沒錯」，神情溫和、理解對方但立場清楚，不是責備、怒視或燦笑。小李安靜聆聽，維持前景位置，不轉頭看鏡頭，也不補出正面表情。Amy 的手機仍低持在畫外下方，雙手與海報均不入鏡，不呈現鏡末收手機的動作。除 Amy 指定的頭部方向、視線、表情與輕點頭起始姿態外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、證書、檢驗報告、圖表、寶特瓶、毛毯、水印或額外疊字。
```



## 2026-10-19 staff_office batch cam_amy_cu_emotion

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_amy_cu_emotion_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-658bf41d-4d1f-49d4-87a7-d233118ee648.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 9f2e277778523221570bf3a64f6233a14deb8bd9a695ec9c5ce387c205b64d40。
- 視覺檢視：特寫裁切、前景椅背上緣、右側雙螢幕、隔板及右後書櫃位置接近白模；書冊和布面質感成立；窗台新增三處小盆栽，百葉窗下緣略有變化。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_cu_emotion_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_amy_cu_emotion_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
緊裁切的空景特寫。畫面下緣中央偏右僅露出最近椅背的上緣與網布局部；中景右側大型螢幕、後方另一螢幕、右後書櫃局部及左側少量椅背與直立書冊，保持底圖位置與大小。上半部是窗戶與百葉窗，中央白柱沿用底圖。不要補全近處椅背、扶手、桌面或畫外道具，不要拉遠。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```


## 2026-10-19 staff_office batch cam_amy_mcu_15deg

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-fb3da1a4-a33f-42a4-8230-90491b3058d0.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 ca984c1affecda234a6b6f4073072a25a6be807b704492869375c90f6b48e4a0。
- 視覺檢視：最近空椅背、左下螢幕局部、右緣盆栽、背景螢幕及窗櫃位置接近白模；布料、紙頁及暖日光成立，沒有新增窗台盆栽；左後直立書冊數量／薄厚與白模有細微差異。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_amy_mcu_15deg_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
15 度微側的空工位中特寫。最近空椅背占畫面下方中央偏右，底部被裁掉；左下僅見大型螢幕局部。隔板交會位置、中景中央偏右螢幕、左後螢幕與空椅、右緣被裁切盆栽、右後書櫃及窗戶百葉窗均依底圖，保持椅背上緣高度與下緣裁切，不增加桌面可見範圍。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```


## 2026-10-19 staff_office batch cam_amy_mcu_selfie

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_amy_mcu_selfie_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-1bc91dff-f1a2-41f4-90ae-fe2e6f7be35d.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 e36b2523b253b9f00004d9b7b643a46d5456ab8f17d8125442604027c2f7918f。
- 視覺檢視：左下桌角、中央偏右空椅背、中景隔板交會與右側盆栽書冊的位置和裁切接近白模；無人物、手機或前景新增螢幕。書冊薄厚、植物葉形與後景細節有重繪差異。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_selfie_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_amy_mcu_selfie_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
底圖的稍微俯視空工位構圖：大面積空椅背位於中央偏右，下緣裁切；左下僅有桌角，前景沒有大型螢幕。中景隔板、右中螢幕、右緣盆栽與書冊、左側高盆栽、後方書櫃與窗戶維持原位置。檔名中的 selfie 只表示相機視角，不加入手機、手臂、人物、自拍介面或前景螢幕。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```


## 2026-10-19 staff_office batch cam_amy_ms_15deg

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-29c028ce-e549-424f-b46c-cefc8b66130c.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 558b6a69a236a8a0841a1074825c5da968efbe82ab80fb2ee2c6fe0dc489ee5d。
- 視覺檢視：15 度中景的前景左側螢幕裁切、中央偏右椅背及隔板交點接近白模；右側四冊書夾紙頁、盆栽、後方書櫃與暖日光成立，局部葉形和背景書冊有生成差異。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_amy_ms_15deg_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
15 度微側空工位中景。最近空椅背位於中央偏右，椅背頂部約在畫面中線，椅子下部被底邊裁切；左前景大型螢幕維持被左邊與下邊裁切的程度。右中盆栽與四冊書夾、隔板交會、前後螢幕、後方書櫃與百葉窗均維持底圖相對位置。不重新置中椅背，也不補全桌面。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```


## 2026-10-19 staff_office batch cam_board_ambience_front

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_board_ambience_front_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-e1751de1-2870-448e-b5a8-a232b5ecf5e8.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 fa6954cf48b2e49919d8261e2d543160ba12dd4820679a2a6603ba8524fff4dc。
- 視覺檢視：中央木框、兩排各五張無字色卡和小白標籤、左右窗戶裁切與白模接近；紙紋、木紋、暖窗光成立。框內材質變為織物／紙面，百葉細節與窗外樓景有生成差異。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_board_ambience_front_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_board_ambience_front_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
公佈欄正面特寫，中央淺木框矩形板完全依底圖位置和尺度，框內兩排各五張矩形色卡與各自底部小白標籤，保持數量、排列、間距與裁切。兩側窗戶及百葉窗局部沿底圖。使用圖 1 牆面、相框、柔和色卡和紙張的質感與暖日光；色卡維持無字，不加入人物照片、合照、標題、圖標或圖外桌椅。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```


## 2026-10-19 staff_office batch cam_desk_insert_iso

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_desk_insert_iso_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-c5eeb1cd-6f07-4e71-9638-f450161ea416.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 49a49d0857f5092ec50075cffd470172d1213c5a45a5467654253c6ad2b1e038。
- 視覺檢視：鍵盤對角線、左側螢幕裁切、小型方盒、右側椅子及扶手位置接近白模；木桌紋理、網布與灰毯質感成立。鍵帽仍為無字簡化形狀，扶手保留部分白模折面，非完整寫實鍵盤重建。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_desk_insert_iso_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_desk_insert_iso_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
高角度斜俯的桌面插鏡。鍵盤沿對角線從左上伸至右下，大小、長寬比、鍵盤外輪廓與桌面位置保持底圖；左側近鏡螢幕只露出被裁切的側背面。左上小型桌面方盒、右上空椅扶手與網布椅背局部、右側坐墊與灰色地毯都保持原位置和裁切。以參考圖的精緻深色鍵盤、霧面螢幕、淺木紋和網布質感完成渲染，不為展示辦公室而拉遠，也不新增書櫃或窗戶進畫面。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```


## 2026-10-19 staff_office batch cam_monitor_insert_front

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_monitor_insert_front_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-2c7647e9-5966-4a7a-b8de-a2d007c8d4b8.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 a6aec564de501b19529555aec220dcb7434ff39d8e554536212bf9b2159c86d9。
- 視覺檢視：空白螢幕占比、四邊透視和下緣裁切接近白模，無介面、文字或人物；外殼、玻璃反射和隔板織紋成立。左上背景新增少量植物葉片及上緣燈光，背景窗景未完全鎖定。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_monitor_insert_front_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_monitor_insert_front_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
電腦顯示器正面極近插鏡。螢幕占畫面絕大部分，保持底圖略有透視的四邊、外框位置、內面板邊界及下緣裁切；左側僅餘狹窄藍綠隔板與窗戶背景，底部少量木桌和淺色支架。將螢幕與外框做成參考圖的深色精緻顯示器材質，黑色面板保留空白，只容許淡淡玻璃反射。不要加入任何畫面內容、文字、介面、標誌、人像或新道具，不拉遠露出完整底座和鍵盤。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```

## 2026-10-19 shot_4.6.8 GPT v1 — 粉紅便條首幀

- 使用者授權：使用 shot_4.6.8 prompt 在 GPT 生圖；依已確認的粉紅便條版本，以五圖 W2I 生成 1 張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、預估與實際費用未由工具提供，不記為零。
- 參數：referenced_image_paths 依下列順序，transparent_background=false；原樣使用 prompt 文件，未追加條件。
- 輸出：`assets/images/shot_4.6.8_gpt_v1.png`；1672×941、RGB PNG、2275848 bytes，未裁切或縮放。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-4633171f-7ed2-40f9-93b7-65562e15392e.png`。
- 驗證：已看圖、完整解碼、核對原始檔與副本 SHA-256 相同：`03ab20207d696e6a727e435db8a5f976c5d644cd0aa915beffc2cf7b22a2e776`。
- 檢視：小李雙手持素面粉紅便條且尚未貼上、Amy 看紙面、兩人無海報或筆成立；人物頭部較 blocks 放大，尤其小李頭頂留白縮減，站位及部分白板便條文字／位置有差異，不記為完全貼合白模。
- 後續指示：使用者要求「amy要看著小李」，因此 v1 的 Amy 視線須修正；另做 v2，不覆蓋本圖。未更新 manifest。

### 實際送入的參考圖（順序固定）

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

### 實際送入的完整 prompt

```text
參考圖說明：
圖 1 cam_twoshot_ms_45deg_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_twoshot_ms_45deg_block_blender.png：三分之四雙人中景的構圖底圖，決定人物站位、前後距離、尺度、朝向與裁切。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側較近的紅色定位人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側較遠的藍色定位人物。
圖 5 prop_whiteboard_incorrect.png：既有白板便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭身比例、前後尺度與裁切。Amy 維持左側較近、小李維持右側較遠；保留各自頭頂留白、頭部大小、頸部長度及肩線高度，不拉近鏡頭、不把兩人移至同一深度，也不為容納手中便條而縮小或挪動人物。

將紅色定位人物完整替換為圖 3 的 Amy，將藍色定位人物完整替換為圖 4 的小李，只呈現圖 2 可見的部位，不補出畫外身體，不殘留白模或方塊肢體。人物圖只提供外觀與服裝，不採用其展示姿態或構圖。小李沿用棕色上梳短髮、藍底彩色花襯衫與白色內搭，不加眼鏡。小李的手臂及雙手依下方持便條的動作調整，其餘人物尺度沿用圖 2。

場景的材質、風格與光影採用圖 1，不改變圖 2 的空間配置。保留人物後方的彩色便條白板、左側 OA 桌面、右側窗格及盆栽，採近眼高、深景深與溫暖日光。

白板上既有便條紙完全依圖 2 的位置、大小、間距、透視與遮擋，只將示意橫線替換為圖 5 的對應圖文：上排由左至右為「100%地球救星」、「純天然無毒擁抱」、「零碳奇蹟」、「環保魔法」；中排黃紙為「地球救星毯」、粉紅紙為「絕對循環」；下排由左至右為「綠色神話」、「天然之魂」、「永續至尊」、「環保教主」。被人物遮住或裁在畫外的部分保持不可見，不縮小紙張以展示完整文字，不搬用圖 5 的整板構圖，不新增第二塊白板。本張是新便條尚未貼上的起始畫面，白板仍保留原有文案。

小李雙手拿著一張新的粉紅色便條紙，其顏色、紙張材質及橫向長方形比例沿用圖 1 白板右側中排的粉紅便條，實體大小相當，不放大成海報。紙面素面、沒有文字或圖案，留待後製貼上本鏡新標語；不要把圖 5 的舊文案複製到這張新便條。保留自然紙張厚度與輕微彎曲，不加硬框、紙板、夾板或認證符號。

畫面描述：
這是一張近眼高、三分之四角度的雙人中景，畫面只有 Amy 與小李兩人。Amy 在左側較近、小李在右側較遠，兩人的可見部位與下緣裁切沿用圖 2。定格在小李若有所悟、拿著粉紅便條準備貼上新標語的瞬間：他下巴輕微下收、眉眼放鬆，帶著理解後想提出新方案的神情，視線落在手中的便條；雙肘自然彎曲，兩手輕握便條兩側邊緣，將紙張托在胸前稍偏下，紙面朝 Amy 與鏡頭可見的方向，雙手不遮中央紙面，便條不遮臉。此時便條尚未碰到白板，仍與白板保持明顯距離，也尚未抬眼向 Amy 確認。Amy 的臉與身體朝向右側小李，視線落在他手中的粉紅便條，嘴巴自然閉合、專注觀察，雙手保持自然低垂，不先點頭肯定或給出贊許手勢；手機已收妥且不入鏡。兩人均不拿海報或筆。除上述持便條、表情、視線與 Amy 朝向調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、獨立數據圖卡、認證符號、實體毛毯、寶特瓶、水印或額外疊字。
```



## 2026-10-19 staff_office batch cam_office_entrance_wide

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_office_entrance_wide_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-b8dbbb3e-50fa-495b-835a-1358b33d4bd6.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 f79eb51bfe830e076d941a2c87fb232a0b1df4ddf4504232fe02e49dce204a4e。
- 視覺檢視：木門板、深色把手、右側兩層書櫃及窗戶裁切接近白模；書籍的封殼、紙頁、布紋及門木紋明確。沿用底圖門後可見高樓的構圖，未改成走廊；窗外樓景與少量下緣地毯有生成差異。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_office_entrance_wide_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_office_entrance_wide_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
嚴格照底圖實際取景：左側窗戶和百葉窗，中央偏右是一片高直的淺木色開啟門板與深色矩形把手，中央可見窗外高樓；最右側書櫃被畫面裁切，呈現兩層書籍與上方一小部分公佈欄。保留門板位置、寬度、角度、把手及所有裁切；維持原本能看見的窗外高樓。材質套用圖 1 木紋、白色塗裝、玻璃、紙本書籍和暖日光。不要因檔名 wide 而拉遠，不改造入口、不改成走廊、不插入前景工位。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```


## 2026-10-19 staff_office batch cam_office_reverse_wide

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_office_reverse_wide_empty_gpt.png)；原生 1672×941，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-9971f4e3-5885-42f7-8bf5-578a29c5bbe0.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 982b6ede50ef599ab87df17887ee793d7ae9f90c09a7394823aecfb322eae234。
- 視覺檢視：反向廣角、天花占比、左側走道、多排工位及右後木門位置接近白模，前景椅背裁切保留；材質與暖日光統一。盆栽葉量、右遠端植物、書冊數量細節和門把設計有重繪差異。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_office_reverse_wide_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_office_reverse_wide_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
辦公室反向廣角空景，底圖包含大面積格柵天花、燈具、左側走道及高盆栽、中央多排藍綠工位、前方多個深色螢幕與空椅、右後木門與書櫃，以及窗戶百葉窗。精確沿用每排隔板的透視交會、工位數量、天花比例、門的位置與前景裁切。圖 1 僅提供材質與光線，不旋轉房間或改成圖 1 的拍攝方向；不增加隔板、不刪掉前景椅背局部。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```

## 2026-10-19 shot_4.6.8 GPT v2 — Amy 看向小李

- 使用者指示：「amy要看著小李」。以 v1 為唯一底圖，內建 image_gen／OpenAI 進行一次局部 I2I；確切模型及費用未提供。
- 參數：referenced_image_paths 依下列清單，transparent_background=false。
- 輸出：`assets/images/shot_4.6.8_gpt_v2.png`；1672×941、RGB PNG、2159691 bytes，未裁切或縮放。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-2f4336a3-d1fa-42bd-a2b5-1e04b83fa9d4.png`。
- 驗證：已看圖、完整解碼，原始檔與副本 SHA-256 相同：`ad14cbe852db95051cb4ec8b4e3babe41af7ff3a333e399e7de1bf24a15c4b88`。
- 檢視：Amy 已抬眼看向右側小李的臉，頭部略抬轉；小李仍看素面粉紅便條，持紙與尚未貼上的狀態保留。Amy 的頭髮／頭頸輪廓有隨轉頭局部重畫，不能視為像素級不變；v1 與白模的比例／便條圖文差異未在本次修正。
- 採用狀態：待使用者確認，v1 保留，manifest 未改。此視線修正優先於先前 scene_plan／prompt 中 Amy 看紙面的描述；本次僅局部修圖，完整請求如下。

### 實際送入的參考圖

1. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.8_gpt_v1.png`

### 實際送入的完整 prompt

```text
以圖 1 shot_4.6.8_gpt_v1.png 為編輯底圖，只修改左側 Amy 的視線，以及為此必要的輕微頭部角度：讓她抬眼看向畫面右側小李的臉部／眼睛位置，注視小李本人，不再低頭看他胸前的粉紅便條紙，也不看鏡頭。維持 Amy 原有溫和、專注的表情，嘴巴保持自然閉合；保留她的五官、髮型、頭部大小、頭頂位置、頸部長度、身體朝向與站位。
保留小李的臉部表情與向下看便條紙的視線、髮型、花襯衫、站位、雙手與持紙動作。粉紅便條維持素面、大小與位置不變，仍未貼上白板。保留兩人以外的所有內容，包括白板便條紙的圖文、位置與遮擋、桌椅、窗戶、盆栽、光線、色調、景別與 16:9 裁切。不要重排構圖、放大人物、改字或加入新物件。
```



## 2026-10-19 staff_office batch cam_office_wide_level

- 用途：既有 kj-cinematic 場景空景 W2I 批次補齊，使用者已授權本批次；未推進整體 assets 核准。
- 工具：內建 image_gen／OpenAI；模型版本及實際費用未提供；transparent_background=false。
- 輸出：[成品](../references/scenes/staff_office/cameras/cam_office_wide_level_empty_gpt.png)；原生 1672×940，依使用者同意以 Lanczos 放大為 3840×2160、16:9 PNG，非原生 4K 細節。
- 原始檔：C:/Users/user/.codex/generated_images/01a15419-144a-7531-a184-0d62c43dfe7f/exec-c5160e03-c0a9-47fd-9b55-64d604d2705c.png；保留。
- 驗證：逐張檢視生成結果，4K 輸出完整解碼；SHA-256 2d349659e7d3a93e57e6debddc8b5b3b0090944e6400e8bf7528775e96d422f8。
- 視覺檢視：正向廣角全景、左前工位隔板、右側寬走道、後方窗櫃木門及主要家具排列接近白模，鏡頭前無新增牆窗遮擋；書冊紙頁與地毯木紋成立。後窗台有少量新增盆栽／書堆，個別家具輪廓與透視細節略有變化。；生成重繪非逐像素鎖定，待使用者檢視，未改 asset_manifest 或 scene_plan。

參考圖順序：

1. D:/kj-openMontage/projects/course-51-esg/clp/loc_staff_office.jpg
2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/staff_office/cameras/cam_office_wide_level_empty_blender.png

完整提示詞：

```text
參考圖說明：
圖 1 loc_staff_office.jpg：場景外觀參考，只提供材質、風格、色調、光線與物件設計。
圖 2 cam_office_wide_level_empty_blender.png：本鏡唯一編輯底圖，決定鏡頭、透視、裁切、物件位置和遮擋。

生圖指引：
直接編輯圖 2，完整保留其攝影機位置、朝向、視野、畫面邊界、物件投影尺度與空間配置。保留所有原有家具、道具、書櫃、窗戶、門與隔板的位置、數量和可見範圍，只替換外觀與材質。尤其不得增加盆栽、書堆或家具；圖 2 原本空白的窗台和櫃頂維持空白。不要採用圖 1 的鏡頭或構圖，不推近、拉遠、平移或旋轉鏡頭；畫外物件維持畫外，不為了展示參考圖元素而補入本鏡沒有的物件。
可見表面全部採用圖 1 的精緻設計：低飽和藍綠色織物隔板、細緻白色塗裝框架、溫潤淺木紋桌面、深色霧面電腦螢幕與鍵盤、細密黑色網布辦公椅、白色書櫃、灰色織紋地毯、陶瓷花盆與自然綠葉。對應物件原位替換，不留白模簡化質感。
辦公桌道具、電腦螢幕、書櫃、書本、檔案夾都使用圖 1 的元素與質感。書本和檔案夾有可信的封面厚度、書脊摺線、裝訂邊、層疊紙頁、細微紙邊、紙面或布面封殼肌理及接觸陰影，不畫成光滑色塊長方體；書櫃層板有合理厚度和柔和圓角；螢幕外殼有細緻霧面反射，保持原正反面朝向。細節尺度自然、柔和，避免過度銳化或模糊掩蓋。
色調與照明取自圖 1：溫暖日光透過百葉窗、柔和室內填光、自然接觸陰影、可信反射、平衡曝光和受控飽和度。窗外若可見，呈現圖 1 的柔和城市光色與大氣景深，維持圖 2 窗口的位置和開放範圍。
A polished, stylized 3D animated feature film aesthetic, featuring an unoccupied environment with no characters, people, or animals. Appealing shapes with softly rounded edges, thoughtfully composed architecture and props, finely detailed surface textures, believable materials and reflections, harmonious colors with controlled saturation, cinematic lighting suited to the scene, subtle atmospheric depth, and depth of field appropriate to the shot.

畫面描述：
辦公室廣角全景空景。前景左半為大面積藍綠工位隔板，近處螢幕、空椅和四冊書夾在其後；寬走道從右下延伸至右後，右側另有工位與局部木桌；背牆窗戶、書櫃、木門及天花比例完全按底圖。保持走道寬度、工位排列、家具數量、透視、取景邊界和開闊視線，不新增鏡頭前方的牆、窗框、玻璃或百葉窗遮擋。 全場空無一人，沒有任何人物、人影、動物或人形物件。

輸出：
一張滿版橫幅 16:9 PNG，要求 3840×2160 像素 4K 高品質圖。無黑邊、無比較拼圖、無字幕、無水印、無新增標誌。
```

## 2026-10-19 shot_4.6.9 GPT v1 — Amy 情緒特寫

- 使用者授權：使用修改後的 shot_4.6.9 prompt 在 GPT 生圖，採 cam_amy_cu_emotion_block_blender.png／SH13／85mm；本次以四圖 W2I 生成 1 張。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、預估與實際費用未提供，不記為零。
- 參數：referenced_image_paths 依下列順序，transparent_background=false；原樣使用 `artifacts/shot_4.6.9_image_prompt.md` 的 CU prompt，未追加條件。
- 輸出：`assets/images/shot_4.6.9_gpt_v1.png`；1672×941、RGB PNG、2117764 bytes，保留原生尺寸，未裁切或縮放。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-c4e7f05f-7215-4875-b41d-da85fefe4e82.png`。
- 驗證：已看圖並對照指定 CU 構圖，完整解碼圖片；原始檔與副本 SHA-256 相同：`ea4f4de39ab167838871aacf8cd910ba04e92ecd44b9b01246dd69f1d11a69b9`。
- 視覺檢視：Amy 單人、微笑張嘴、臉與視線朝畫面偏右成立，雙手／手機／其他角色及新粉紅便條未入鏡。下緣露出的肩膀與上胸多於 blocks，未完整遵從頭頸為主、僅少量肩線的裁切；視線偏右上，頭頸角度與輪廓略有差別。白板便條的位置、尺度、裁切與部分文字有差異，不記為完全符合構圖。
- 採用狀態：待使用者檢視；未改 asset_manifest、scene_plan 或 prompt，未自動追加生成，原始輸出保留。

### 實際送入的參考圖（順序固定）

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_cu_emotion_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_cu_emotion_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

### 實際送入的完整 prompt

```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：Amy 單人情緒特寫的構圖底圖，決定頭部與頸部的位置、尺度、朝向、裁切及白板便條的遮擋。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭部大小、頭頂留白、下巴位置、可見頸部長度與下緣裁切。本鏡以完整頭部及頸部為主，下緣僅露少量肩線與衣領；不要拉遠補出胸口、上臂或雙手，也不要再推近、放大頭部、裁掉髮頂或把人物往上移。

將紅色定位人物完整替換為圖 3 的 Amy，只替換圖 2 可見的頭部、頸部與下緣少量肩部，不殘留簡化頭部、方塊頸部或紅色白模。人物外觀採用圖 3，可見衣領與肩部延續灰色西裝外套及淺色襯衫，不採用人物參考圖的展示姿態或構圖。Amy 的臉、視線及僅露出的肩線朝畫面偏右，維持朝向小李的姿態，不改成正面直視鏡頭；不為了表現身體朝向而擴大取景。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左後方窗格、OA 隔板與螢幕局部，以及右後方既有白板的局部；不補出被人物遮住的桌面。採近眼高、深景深與溫暖日光，不用強烈背景模糊掩蓋配置。

白板便條紙的外輪廓、位置、大小、透視、人物遮擋及畫面裁切完全依圖 2，只將示意橫線替換為圖 4 的對應圖文：上方被畫面裁切的綠紙對應「100%地球救星」，右上邊緣只露局部的藍紙對應「純天然無毒擁抱」，右下方被下緣裁切的大片藍紙對應「綠色神話」，最右下角僅露極小紙邊的綠紙對應「天然之魂」。維持各紙原本的可見範圍，不補出整張紙。文字與紙張一起依透視及畫面邊界自然裁切，被 Amy 遮住的部分保持遮住，不為了讀完整文案而移位、縮小紙張或挪動人物。圖 4 只提供便條內容，不採用其整板構圖，不新增第二塊白板，不留下重複的示意橫線。上一鏡的新粉紅便條位於本機位畫外，不將它移入可見白板區。

畫面描述：
這是一張近眼高、略帶側角的 Amy 單人情緒特寫。Amy 的頭部位於畫面中央偏左，完整髮頂、頭部與頸部依圖 2 呈現，下緣只露少量肩線和衣領，胸口及其餘身體裁在畫外；左後方是窗格與辦公隔板局部，右後方是便條白板局部。定格在 Amy 開始肯定小李創意方向的瞬間：她的臉與可見肩線朝畫面偏右，雙眼看著畫外右側小李的臉部高度，不低頭看便條或轉看白板；嘴角自然上揚、眉眼放鬆，嘴唇微啟準備說「方向很棒！」，下巴只有極輕微下收，呈現開始溫和點頭的姿態。點頭只作細微頭部調整，保持原頭部尺度及自然頸部長度，不歪頭、縮頸或降低人物位置。表情是鼓勵對方繼續完善提案，不是大笑、誇張讚嘆或嚴厲責備。畫面只出現 Amy 一人，小李與小陳均不入鏡；胸口、手臂、雙手及已收妥的手機全部在畫外，不拿紙張或報告，不新增指手、比讚或認證手勢。除上述表情、視線及輕點頭起始姿態外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、檢驗報告、數據圖表、數字徽章、認證章、勾號、水印或額外疊字。
```


## 2026-10-19 shot_4.6.3 GPT v5 — 現行中景與朝右 30 度要求

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；使用者指定以下完整 Prompt，以 GPT 生成一張並保存至 Dropbox。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量及費用未提供，已事先告知無法估價。一次、一張，transparent_background=false，Prompt 正文原樣傳送（不含結尾 Markdown fence）。
- 輸出：[shot_4.6.3_gpt_v5.png](../assets/images/shot_4.6.3_gpt_v5.png)；實際保存於 `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v5.png`。
- 原始輸出：`C:/Users/user/.codex/generated_images/01a15436-86d2-71a1-93e2-48cbbf9480bf/exec-55010b71-e165-4ccd-8a16-39d5a7418fe8.png`，原檔保留。
- 檢視：Amy 單人、皺眉微張嘴、臉與視線朝畫外右側、直向手機背面朝觀眾且上緣低於下巴成立；軀幹仍偏正面，未符合身體一併朝右約 30 度。相對 blocks，人物頭頂較低、軀幹較窄，便條紙位置及裁切有差異；中段右側黃紙顯示較完整，上排紙張亦顯示較多文字。未新增第二塊白板，文字與字形未達精確貼圖。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG（接近但非精確 16:9），2,135,683 bytes；來源／目的地 SHA256 一致：`3f18cbe3fa4edfcb87613be4c543e45b7448338a482fa639784a030fb3ed1c91`。未裁切、放大或程式合成。
- 狀態：使用者指出「軀幹也要朝右」，接續局部修正；v5 保留，未確認採用，未更新 asset_manifest／scene_plan，未生成影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_ms_15deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_ms_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_ms_15deg_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_amy_ms_15deg_block_blender.png：構圖底圖，決定人物佔位、朝向、尺度，以及背景與便條紙的位置、透視、裁切和遮擋。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板便條紙的圖文內容參考。
圖 5 prop_smartphone.png：Amy 手中手機的實體外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物位置、頭身尺度、頭頂留白、肩線高度與下緣裁切。持手機所需的前臂及手部調整依下方畫面描述，其餘沿用圖 2。

將紅色定位人物完整替換為圖 3 的 Amy，只呈現圖 2 可見的身體部位，不殘留方塊軀幹、簡化頭部或長條四肢。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。肩膀、胸口、軀幹與臉部均沿用圖 2 朝畫面偏右的角度，維持自然斜側面，不把上半身轉成正對鏡頭後只轉動眼睛。

將場景的材質、風格與光影更新為圖 1 的外觀，空間配置仍依圖 2。保留左側既有 OA 桌、隔板、螢幕與窗格，以及右側和人物後方的同一塊白板、板框與下方筆槽；維持日間暖色自然光與深景深。

白板便條紙的外輪廓、位置、大小、間距、透視及裁切完全依圖 2，只把每張紙內的黑色示意橫線替換成圖 4 對應便條的圖文：
上緣由左至右的綠紙、淺藍紙與局部粉紅紙，分別對應「100% 地球救星！」、「純天然無毒擁抱」、「零碳奇蹟」。
中段 Amy 後方的淺藍紙對應「綠色神話」，右側黃紙對應「地球救星毯」。
下段綠紙與右側局部黃紙，分別對應「天然之魂」、「永續至尊」。
完整文字與字樣以圖 4 為準，貼合既有紙張的透視，接受人物、手機遮擋及畫面邊緣裁切。不要為了露出完整文案而移動人物、縮小或重排紙張。圖 4 的整板構圖、板框及其餘便條不參與生成；不新增第二塊白板或板中板，不保留重複的示意橫線，也不把誇大文案改成正確宣傳文案。

手機機身、邊框、厚度、背蓋與三鏡頭模組採用圖 5，尺寸與 Amy 的手掌相稱。圖 5 只提供同一支手機的實體外觀，不採用多視圖排列或「主管來電」介面。畫面只出現一支手機，螢幕朝向 Amy，觀眾主要看見背面與側邊，不展示搜尋文字、法規頁面或錄影介面。

畫面描述：
這是一張近眼高、略帶側角、55mm 視角的 Amy 單人中景。Amy 位於畫面中央偏左，可見完整頭部、頸部、肩膀與上半身，下緣裁切沿用圖 2；左側保留辦公區，右側與人物後方是既有白板。定格在 Amy 已用手機查證、正開口提醒小李的瞬間：身體與臉都要朝著畫面的右邊約30度(即amy的左手邊)，視線看向畫外右側的小李，眉心微皺、嘴唇微啟，神情專注、嚴肅且帶一點擔憂。畫面右側的前臂屈肘抬起，手掌自然握住直向手機，放在胸前偏右，手機上緣低於下巴，不遮住臉；手指自然環握機身，螢幕朝自己，背面朝觀眾。另一側手臂沿用圖 2 的垂放方向，手掌維持在畫外下方。畫面只出現 Amy 一人，小李與海報均在畫外。保持原有人物大小、位置、頭頂留白與背景裁切，不推近成中近景，不把 Amy 移到畫面正中央。除上述持手機姿勢、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，只呈現上述單一瞬間，不加入字幕、對話框、警告字卡、水印或額外疊字。
```


## 2026-10-19 shot_4.6.3 GPT v6 — 軀幹一併朝右

- Pipeline／階段：course-51-esg／kj-cinematic／assets／I2I；使用者看見 v5 後明確要求「軀幹也要朝右」，以 v5 做局部修正。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量及費用未提供，已事先告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v6.png](../assets/images/shot_4.6.3_gpt_v6.png)；實際保存於 `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v6.png`。
- 原始輸出：`C:/Users/user/.codex/generated_images/01a15436-86d2-71a1-93e2-48cbbf9480bf/exec-a2d38e3f-1a2a-4946-a64d-c32c2d0f37b2.png`，原檔及 v5 均保留。
- 檢視：相對 v5，肩膀、胸口、襯衫門襟與腰部已一併轉向畫右，近側肩臂及衣襟出現斜側透視，臉與視線仍朝右；手機、皺眉微張嘴及單人場景保留。背景便條紙、辦公區與光線整體延續 v5。角度屬視覺判讀，未宣稱精確 30 度；人物輪廓、臉部與持手機位置有局部重畫，原 v5 相對 blocks 的尺度及便條裁切差異仍在。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG（接近但非精確 16:9），2,111,380 bytes；來源／目的地 SHA256 一致：`95372d6df6bbe90671132322d7b131eced2f3bc4ce6431718ec0d94bbf775bd1`。未裁切、放大或程式合成。
- 狀態：已交付修正版，待使用者確認採用；未更新 asset_manifest／scene_plan，未生成影片，無既有 checkpoint／partial_progress 可同步。

有序參考圖：

1. `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v5.png`

完整 Prompt：

```text
以圖 1 shot_4.6.3_gpt_v5.png 為基礎做局部修正。使用者要求：「軀幹也要朝右」。唯一要修改的是 Amy 的軀幹朝向及因此連動的肩膀、衣服、腰部與手臂透視。

把 Amy 目前幾乎正對鏡頭的上半身，從肩膀、胸腔到腰部整體轉向畫面右側約 30 度，也就是向 Amy 自己的左手邊轉身，形成清楚可見的三分之二正面斜側姿態。她的胸口正面、襯衫門襟與骨盆都指向畫外右側的小李，和目前臉部的右轉方向一致。不是只轉頭、只轉眼睛、歪肩或側彎腰。畫面左側的肩膀（Amy 的右肩）較靠近觀眾，畫面右側持手機的肩膀（Amy 的左肩）退向後方；兩側肩膀、外套翻領、胸口及腰部呈現同一次整體右轉產生的自然透視，遠側衣襟較窄。必須看得出胸口已朝右，不能仍讓兩肩和襯衫正面平鋪朝向鏡頭。維持站直，不斜靠、不跨步、不變成完全側面。

保留圖 1 的同一位 Amy、臉部外觀、棕色短髮、綠色眼睛、皺眉與微張嘴的嚴肅提醒表情、看向畫外右側的視線、灰色西裝與白襯衫。保留人物在畫面中央偏左的站位、頭部位置與大小、頭頂留白、身高比例及下緣裁切。臉繼續朝畫右約 30 度，不轉回正面。只為了讓軀幹正確轉向而調整身體輪廓與衣服透視。

保留畫面右側的左手直向持同一支深灰三鏡頭手機的動作，手機位於胸前、上緣低於下巴、螢幕朝 Amy、背面朝觀眾，不遮臉。持手機的左上臂隨左肩的退後自然連動，前臂與手腕仍自然屈曲；另一側右手臂自然垂放、手掌維持畫外。只出現一位 Amy 和一支手機。

場景與相機完全保持圖 1：左側辦公桌、隔板、電腦、窗戶，右側原有白板、筆槽及每張彩色便條紙的位置、大小、圖文、裁切與日光均不重新設計；背景只接受轉身後人物輪廓帶來的必要遮擋變化。保持原圖 16:9 橫幅取景、風格與色彩，不推近、不平移、不新增人物或物件，不新增白板、字幕、對話框、水印或額外疊字。輸出一張修正版。
```


## 2026-10-19 shot_4.6.3 GPT v7 — MCU Blender 五圖重生

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；使用者指定 MCU Blender 空景及 blocks，要求以下完整 Prompt 原文重新生成一張。此為本輪圖片生成覆寫既有機位選擇的明確指示，未回寫 scene_plan。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量及費用未提供，已事先告知無法估價。一次、一張，transparent_background=false；Prompt 原文傳送（僅不含結尾 Markdown fence）。
- 輸出：[shot_4.6.3_gpt_v7.png](../assets/images/shot_4.6.3_gpt_v7.png)；實際保存於 `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v7.png`。
- 原始輸出：`C:/Users/user/.codex/generated_images/01a15436-86d2-71a1-93e2-48cbbf9480bf/exec-c73759b0-61cd-489f-8a67-2b5d59218042.png`，原檔保留。
- 生成前觀察：MCU 參考只有四張綠／藍紙，但使用者原文仍列粉紅／黃紙，已告知此差異後依明確要求原文送出；生成途中使用者更正為 MCU 四張綠／藍紙，因此本結果不能視為已滿足最新指示。
- 檢視：Amy 單人、微皺眉、微張嘴、臉與視線朝右、直向持手機成立；軀幹仍偏正面。白板多出粉紅及黃色便條，既有便條縮小且上緣裁切改變，並出現 MCU 參考畫外的下框／筆槽；不符合最新四張紙要求。相對 blocks 的人物尺度、肩線及頭頂留白亦有差異。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，2,028,539 bytes；來源／目的地 SHA256 一致：`a1614778b7e054ffab721d1485d0c3454fa4e671743714afd6d22e117e2d54c5`。未裁切、放大或程式合成。
- 狀態：使用者再指出「軀幹也要朝右」；將軀幹右轉及四張便條合併局部修正。v7 保留未採用；未更新 asset_manifest／scene_plan，未生成影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_blender.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_blender.png：行銷辦公室場景外觀參考圖。
圖 2 cam_amy_mcu_15deg_block_blender.png：構圖底圖，決定人物佔位、朝向、尺度，以及背景與便條紙的位置、透視、裁切和遮擋。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_whiteboard_incorrect.png：既有白板便條紙的圖文內容參考。
圖 5 prop_smartphone.png：Amy 手中手機的實體外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物位置、頭身尺度、頭頂留白、肩線高度與下緣裁切。持手機所需的前臂及手部調整依下方畫面描述，其餘沿用圖 2。

將紅色定位人物完整替換為圖 3 的 Amy，只呈現圖 2 可見的身體部位，不殘留方塊軀幹、簡化頭部或長條四肢。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。肩膀、胸口、軀幹(肩膀、胸口、腰部)與臉部均沿用圖 2 ，都一起一起朝畫面右邊約 30 度，維持自然斜側面，不把上半身轉成正對鏡頭後只轉動眼睛。

將場景的材質、風格與光影更新為圖 1 的外觀，空間配置仍依圖 2。保留左側既有 OA 桌、隔板、螢幕與窗格，以及右側和人物後方的同一塊白板、板框與下方筆槽；維持日間暖色自然光與深景深。

白板便條紙的外輪廓、位置、大小、間距、透視及裁切完全依圖 2，只把每張紙內的黑色示意橫線替換成圖 4 對應便條的圖文：
上緣由左至右的綠紙、淺藍紙與局部粉紅紙，分別對應「100% 地球救星！」、「純天然無毒擁抱」、「零碳奇蹟」。
中段 Amy 後方的淺藍紙對應「綠色神話」，右側黃紙對應「地球救星毯」。
下段綠紙與右側局部黃紙，分別對應「天然之魂」、「永續至尊」。
完整文字與字樣以圖 4 為準，貼合既有紙張的透視，接受人物、手機遮擋及畫面邊緣裁切。不要為了露出完整文案而移動人物、縮小或重排紙張。圖 4 的整板構圖、板框及其餘便條不參與生成；不新增第二塊白板或板中板，不保留重複的示意橫線，也不把誇大文案改成正確宣傳文案。

手機機身、邊框、厚度、背蓋與三鏡頭模組採用圖 5，尺寸與 Amy 的手掌相稱。圖 5 只提供同一支手機的實體外觀，不採用多視圖排列或「主管來電」介面。畫面只出現一支手機，螢幕朝向 Amy，觀眾主要看見背面與側邊，不展示搜尋文字、法規頁面或錄影介面。

畫面描述：
這是一張近眼高、略帶側角、55mm 視角的 Amy 單人中近景。Amy 位於畫面中央偏左，可見完整頭部、頸部、肩膀與上半身，下緣裁切沿用圖 2；左側保留辦公區，右側與人物後方是既有白板。定格在 Amy 已用手機查證、正開口提醒小李的瞬間：身體與臉都要朝著畫面的右邊約30度(即amy的左手邊)，視線看向畫外右側的小李，眉心微皺、嘴唇微啟，神情專注、嚴肅且帶一點擔憂。畫面右側的前臂屈肘抬起，手掌自然握住直向手機，放在胸前偏右，手機上緣低於下巴，不遮住臉；手指自然環握機身，螢幕朝自己，背面朝觀眾。另一側手臂沿用圖 2 的垂放方向，手掌維持在畫外下方。畫面只出現 Amy 一人，小李與海報均在畫外。保持原有人物大小、位置、頭頂留白與背景裁切，不推近成中近景，不把 Amy 移到畫面正中央。除上述持手機姿勢、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，只呈現上述單一瞬間，不加入字幕、對話框、警告字卡、水印或額外疊字。
```


## 2026-10-19 shot_4.6.3 GPT v8 — 四張綠藍便條與軀幹右轉

- Pipeline／階段：course-51-esg／kj-cinematic／assets／I2I；合併使用者最新更正「根據 MCU 參考圖只露出四張綠／藍便條就好」及「軀幹也要朝右」。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量及費用未提供，已事先告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v8.png](../assets/images/shot_4.6.3_gpt_v8.png)；實際保存於 `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v8.png`。
- 原始輸出：`C:/Users/user/.codex/generated_images/01a15436-86d2-71a1-93e2-48cbbf9480bf/exec-de16217a-b729-4603-9bd7-abdb8416fe8d.png`，原檔與舊版保留。
- 檢視：肩膀、胸口及可見軀幹已一併朝畫右，近側肩臂與衣襟有斜側透視；臉與視線持續朝右，皺眉微張嘴與手機背面朝觀眾保留。白板確實只剩上綠、上藍、中藍、右下綠四張，粉紅與黃色便條移除，未新增第二塊白板。
- 限制：便條紙尺寸與裁切尚未恢復 MCU 原圖；上排紙張仍幾乎完整可見，中段藍紙偏小，右下綠紙的右緣裁切不足，畫面底部仍留有原圖的白板下緣。人物頭身、肩線及頭頂留白亦未與 blocks 精確對齊。轉身角度為視覺判讀，不宣稱精確 30 度，未宣稱整體構圖完全通過。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，1,968,382 bytes；來源／目的地 SHA256 一致：`f2457d4d4e8ab3e3ff7ab5f63a4cdff86c08c4142b1aaaf39af096abd145c43b`。未裁切、放大或程式合成。
- 狀態：已交付最新修正版，待使用者確認採用；未自動追加生成，未更新 asset_manifest／scene_plan，未生成影片。

有序參考圖：

1. `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v7.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖用途：
圖 1 shot_4.6.3_gpt_v7.png：本次要局部修正的原圖，提供 Amy、手機及既有表情。
圖 2 cam_amy_mcu_15deg_empty_blender.png：本鏡正確的 MCU 背景，決定唯一白板及四張綠／藍便條紙的位置、尺度、透視與裁切。
圖 3 prop_whiteboard_incorrect.png：只提供四張指定便條紙內的圖文，不採用整板構圖、板框或其他便條。

以圖 1 為基礎，一次修正兩個目標：Amy 的軀幹也要朝畫面右側，以及白板恢復圖 2 的四張綠／藍便條構圖。其餘保持原圖。

軀幹轉向：
把 Amy 目前幾乎正對鏡頭的上半身，從肩膀、胸腔到腰部整體轉向畫面右側約 30 度，也就是向 Amy 自己的左手邊轉身，形成清楚可見的斜側姿態。她的胸口正面、襯衫門襟與腰部都朝畫外右側的小李，和目前臉部的右轉方向一致。畫面左側的肩膀（Amy 的右肩）較靠近觀眾，畫面右側持手機的肩膀（Amy 的左肩）退向後方；兩側肩膀、外套翻領、胸口及腰部呈現整體右轉產生的自然透視，遠側衣襟較窄，胸前正面從鏡頭轉開。必須看得出肩線、胸口和腰部一起向右，不能維持正面軀幹後只轉頭、只轉眼睛、歪肩或側彎腰。維持站直、不跨步、不變成完全側面。腰部若在畫外，保持畫外，只在可見軀幹延續同一轉向，不為了展示腰部而拉遠鏡頭。

保留圖 1 同一位 Amy 的臉、棕色短髮、綠色眼睛、眉心微皺與嘴唇微啟的擔憂嚴肅表情，以及看向畫外右側的視線。保留頭部位置與大小、頭頂留白、人物在畫面中央偏左的站位及下緣裁切。保持同一件灰色西裝與白襯衫，只為了轉身調整身體輪廓和衣服透視。保留畫面右側的左手直向持同一支深灰三鏡頭手機，手機放胸前、上緣低於下巴、螢幕朝自己、背面朝觀眾；左上臂隨左肩退後自然連動，前臂與手腕自然屈曲，另一側右手臂自然垂放、手掌在畫外。只出現一位 Amy 和一支手機。

白板與便條：
用圖 2 的同機位白板背景取代圖 1 錯誤的七張便條版面。移除圖 1 右上粉紅紙、右中黃紙、右下黃紙，移除錯誤露出的白板下框與筆槽，用同一塊既有白板表面填回；圖 2 的白板上、下、右邊界均在畫外，只保留原有左側垂直板邊，不新增框內框或第二塊白板。
畫面始終只有圖 2 那四張既有便條，恢復它們在圖 2 的原有大小與位置，並非只把圖 1 的其他顏色刪掉後留下縮小的紙：
1. 上緣偏中的綠紙：水平位置約畫面寬 47%～73%，上半部在畫面上緣以外，下緣約畫面高 15%。內容對應圖 3 的「100% 地球救星！」便條，只露自然裁切後的部分。
2. 上緣右側淺藍紙：由約畫面寬 77% 延伸到畫外右側，上半部亦在畫面上緣以外，下緣約畫面高 15%。內容對應圖 3 的「純天然無毒擁抱」便條。
3. 中段大淺藍紙：水平約 47%～74%，垂直約 50%～82%，部分在 Amy 與手機後方。內容對應圖 3 的「綠色神話」便條。
4. 右下綠紙：從約畫面寬 78% 延伸到畫外右側，垂直約 68%～96%。內容對應圖 3 的「天然之魂」便條，右側自然被畫面裁掉。

上述百分比用於定位圖 2 既有紙張輪廓，精確輪廓與透視依圖 2。將圖 3 對應四張紙的圖文放入這四個輪廓，替換原示意橫線，文字自然接受畫面邊緣裁切與人物遮擋，不為了露出完整文案縮小或移動紙張，不補出畫外的句子。不要生成粉紅紙、黃色紙或任何第五張便條。圖 3 的其餘內容完全不參與生成。

保留左側既有辦公桌、隔板、電腦、黑色窗格與窗外樹景，以及原有日光方向、立體動畫質感與色彩；相機位置與 MCU 取景保持不變，不推近、不拉遠、不平移。輸出一張 16:9 彩色修正版，不新增小李、海報、字幕、對話框、警告字卡、水印或額外疊字。
```



## 2026-10-19 shot_4.6.10 GPT v1 — 雙人中景對鏡收尾

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；依使用者要求使用修改後的 shot_4.6.10 prompt，原文與五張參考圖送出。
- 機位：cam_twoshot_ms_level（SH03_medium_two_shot／50mm／frame 103），Amy 左、小李右；Amy 開始轉向觀眾總結。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，事前已告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.10_gpt_v1.png](../assets/images/shot_4.6.10_gpt_v1.png)；保存於 `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.10_gpt_v1.png`。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-1cc38cb5-f797-4dda-a62a-f7f8065dfbd9.png`，原檔保留。
- 檢視：兩人中景、Amy 對鏡且嘴唇微啟、小李朝左聆聽、雙手垂放及右側中排素面粉紅便條成立。相對 blocks，兩人頭部偏大、頭頂留白減少，小李較高且偏右；Amy 略歪頭，部分便條位置／大小與人物遮擋仍有差異，文字尚需逐字校對，未完全符合原構圖。
- 連戲：素面粉紅紙供既定後製貼入「每件毛毯，都是由8個回收寶特瓶製成，溫暖你，也溫暖地球！」；本輪未執行文字後製，不恢復「絕對循環」。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，2,214,932 bytes；來源／目的地 SHA256 一致：`192f6a8d2c3368f45a9ae81c020018e9fc9aaf9482e2c2cd934b7ee06b4c0d09`。未裁切、縮放或程式合成。
- 狀態：候選圖待使用者檢視，asset_manifest／scene_plan／prompt 未改；未追加生成或製作影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：雙人中景構圖底圖，決定兩人的位置、尺度、頭身比例、距離、可見部位、裁切與白板便條配置。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的紅色定位人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側的藍色定位人物。
圖 5 prop_whiteboard_incorrect.png：既有白板便條紙的外觀與圖文內容參考；右側中排粉紅便條依本鏡連戲另行處理。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭身比例、頭頂留白、肩線高度與兩人間距。Amy 在左、小李在右，完整頭部、軀幹、手臂及部分手掌依圖 2 入鏡，下半身與手掌邊緣按原下緣裁切。不推近成單人特寫，不把兩人向中央靠攏，也不拉遠補出全身或完整手掌；不要放大頭部、縮短頸部、壓短軀幹或降低人物高度。

將紅色定位人物完整替換為圖 3 的 Amy，將藍色定位人物完整替換為圖 4 的小李；只呈現圖 2 可見部位，不殘留簡化頭部、方塊頸部或色塊身體。人物圖只提供外觀與服裝，不採用其展示姿態或構圖。Amy 延續棕色齊頸短髮、灰色西裝外套與淺色襯衫；小李延續棕色上梳短髮、藍底彩色花襯衫與棕色長褲，不加眼鏡。兩人身體方向及垂放手臂沿用圖 2；Amy 的頭部與視線依下述對鏡表演小幅調整，不改變站位、頭部尺度或肩線高度。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留兩人後方的同一塊便條白板、左右窗格、左側 OA 桌面與螢幕，以及白板下方既有辦公椅局部。採近眼高略俯視、深景深與溫暖自然日光，兩人及白板都清楚，不以強烈散景掩蓋配置。

白板便條紙的外輪廓、位置、大小、透視、人物遮擋與裁切依圖 2。除右側中排粉紅便條外，其餘紙張的示意橫線替換為圖 5 的對應圖文：上排由左至右為綠紙「100%地球救星」、藍紙「純天然無毒擁抱」、粉紅紙「零碳奇蹟」、黃紙「環保魔法」；中排黃紙對應「地球救星毯」；下方由左至右為藍紙「綠色神話」、綠紙「天然之魂」、黃紙「永續至尊」、粉紅紙「環保教主」。文字隨紙張透視與人物遮擋自然裁切，不為了讀完整文案而移動紙張或人物。圖 5 只提供各張便條內容，不採用其整板構圖，不新增第二塊白板，不保留示意橫線。

右側中排、原「絕對循環」所在的位置，已被 shot_4.6.8 貼上的新粉紅便條覆蓋。新紙維持圖 2 該位置的大小、輪廓與透視，貼平在白板上，靠近小李的部分依其輪廓自然遮擋；此張紙面保持素面粉紅，供後製貼入已確定的新標語，不生成舊「絕對循環」文字、示意橫線或臆造新文字。小李已放開便條，兩人手中均不持紙，不新增另一張粉紅便條，也不重新演出貼紙動作。

畫面描述：
這是一張 Amy 在左、小李在右的雙人中景，兩人的完整頭部、軀幹、自然垂放的手臂及可見手掌依圖 2 呈現，下半身及手掌邊緣維持原裁切，便條白板位於兩人後方。定格在 Amy 從與右側小李的對話轉向觀眾的起始瞬間：雙眼剛移向拍攝鏡頭，頭部跟隨視線略微轉回，臉仍帶輕微偏右角度，目光已與觀眾接觸。她眉眼自然、嘴角放鬆，神情誠懇而堅定，嘴唇微啟準備說「各位觀眾」；頭頸自然直立、下巴平穩，此刻尚未做後段強調語句的點頭。小李安靜看著左側 Amy 的臉，嘴巴自然閉合，保持原站位及雙手垂放姿態，不轉看鏡頭、不點頭、比讚或插話。Amy 的手機已收妥，兩人均不拿手機、海報、筆或檢驗報告，不伸臂自拍。畫面只有兩人，除 Amy 指定的頭部轉向、鏡頭視線、誠懇表情，以及白板右側中排已貼妥的新粉紅便條外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、結語字卡、檢驗報告、數據圖表、認證章、水印或額外疊字。
```

## 2026-10-19 shot_4.6.3 GPT v9 — 依 MCU 重建四張便條與放鬆姿態

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；使用者要求重新比對便條尺寸／裁切，並調整 Amy 僵硬軀幹。
- 原因與方法：v8 延續舊圖縮小便條及下框，軀幹旋轉要求又過於僵直。本輪重新檢視 v8、MCU empty／blocks，以原 MCU 五圖重建，未把 v8 當輸入；以原紙輪廓／百分比明寫裁切，胸腰允許自然微小角度差。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量及費用未提供，已事先告知。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v9.png](../assets/images/shot_4.6.3_gpt_v9.png)；實際保存於 `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v9.png`。
- 原始輸出：`C:/Users/user/.codex/generated_images/01a15436-86d2-71a1-93e2-48cbbf9480bf/exec-55b864fb-22c9-4731-a0b2-f06c5ed03943.png`。
- 檢視：四張紙的尺度與裁切已明顯回到 MCU；上兩張紙頂部被裁、中段藍紙放大、右下綠紙下移且右緣出畫，白板下框移除。依視覺邊界估計，上綠 x約47%～72.5%／下緣約15.4%，中藍 x約48%～74%／y約50%～82%，右下綠 x約78%起／y約68%～95%，與原圖接近，仍非像素級貼圖。紙內字形／換行有重畫。Amy 肩頸、左肘及握手機較放鬆，但軀幹又偏正面，尚未滿足原有朝右要求，接續只修軀幹。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，2,016,019 bytes；複製前後 SHA256 相同：`d6eb4a337e9fad407273f1a9dac9a89cdf8a87206177915b7429efa65f6745c7`。未裁切、放大或程式合成。
- 狀態：過程版本保留，未更新 asset_manifest／scene_plan。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_blender.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_blender.png：同機位空景，提供原有場景與四張便條紙。
圖 2 cam_amy_mcu_15deg_block_blender.png：本次唯一構圖底圖，紅色定位人物對應 Amy。
圖 3 char_amy.jpeg：Amy 的外觀與服裝參考，不採用展示姿態。
圖 4 prop_whiteboard_incorrect.png：只提供四張指定紙張內的文字筆跡與紙質，不提供整板版面。
圖 5 prop_smartphone.png：一支手機的機身外觀參考，不採用來電介面。

生圖指引：
直接編輯圖 2，將定位人物換成 Amy，將便條紙上的黑色橫線換成對應文字。保留圖 2 的固定 MCU 相機、背景透視及原取景。圖 1 只補充人物遮住的原場景外觀。這張照片已經在正確機位，不重新安排白板版面，也不為了讀完文字而拉遠鏡頭。

背景是鎖定的：原白板左側直框在畫面寬約 42%～44%，白板的頂、底、右邊界全在畫外。畫面底部是延續到畫外的白色板面，不能出現白板底框、橫向筆槽、腳架或地面。左側辦公桌、深色隔板、黑色螢幕與黑色窗格維持圖 2 的位置與外觀，保留圖 1 的日光方向與斜向光影。

四張紙的邊界是既有幾何，直接保留，先鎖住輪廓再填字。以整張畫面的左上角為 0%、右下角為 100%，紙張可見範圍如下：
A 上排綠紙：x=46.6%～72.5%，y=0%～15.4%。這只是整張綠紙被畫面上緣切掉後的下段。紙張上緣在畫外，絕對沒有留白可看見完整上邊，不把整張縮成一張小卡片。內文來自圖 4 左上「100% 地球救星！」紙張；上方標題及文字隨原紙一起在畫外裁掉，只留對應下段，不為了保留標題下移文字。
B 上排藍紙：x=76.6%～100%以外，y=0%～15.1%。紙張上邊與右邊都伸出畫外；不能看到完整頂邊或右邊，不能在紙與右邊界之間留白。內容來自圖 4「純天然無毒擁抱」，只呈現自然裁切後的下段與左側內容。
C 中段大藍紙：x=47.4%～73.9%，y=49.6%～81.8%。寬約畫面四分之一、高約畫面三分之一，是一張大紙，不是小便利貼。內容來自圖 4「綠色神話」，左下部分自然被 Amy 肩膀、手或手機遮擋。不要縮小或移到右上空白區。
D 右下綠紙：x=78.2%～100%以外，y=67.9%～95.8%。放在真正右下方，底邊接近畫面底部；右邊延伸出畫外，所以文句右端自然裁斷。內容來自圖 4「天然之魂」。不要把它上移至中央，不讓整張完整出現在畫內。
百分比用於辨認原圖輪廓，最終紙張的外形、比例、輕微透視及邊緣均直接沿用圖 2。圖 4 的每張紙只作為貼入各自輪廓的內容；超出取景的內容直接裁掉，嚴禁為了塞完整文案縮字、縮紙、移紙。畫面只有這四張紙，不加入黃色、粉紅色或其他紙張，不留下黑色示意橫線，不新增白板。

將紅色定位人物替換成圖 3 的 Amy，保留她的棕色微捲短髮、綠色眼睛、灰西裝白襯衫、自然成年人體態。位置、頭部尺度、頭頂留白及下緣裁切依圖 2，但不要把方塊人的方肩、直筒頸部或僵直躯幹套到真人比例的動畫角色；衣服包覆自然身體，有柔和摺痕與鬆量，不刻意收腰挺胸。人物的姿態調整依下方畫面描述。

手機外觀採圖 5，只出現一支，螢幕朝 Amy，背面與三鏡頭朝觀眾，尺寸與手掌相稱。不要來電介面、搜尋文字或其他手機螢幕展示。

畫面描述：
這是一張近眼高的 Amy 單人中近景，位於中央偏左，完整頭部與肩胸入鏡，腰部以下仍在畫外，視線看向畫外右側小李。Amy 剛查完手機，正用平靜但認真的口氣提醒對方，眉心輕皺、嘴唇微啟。整體仍朝畫右約 30 度，但姿勢像自然交談中的人：胸口與可見腰部都朝右，頭頸沿著身體自然延伸，肩頸放鬆下沉，胸腰有少量柔和轉角差，重心安定，不像把肩膀、胸腔、腰部焊死在同一軸線上。近側肩膀自然放鬆，沒有聳肩、軍姿、過度挺胸、後仰、強烈扭腰或模特兒擺拍。畫面右側的左上臂放鬆靠近身體，左肘較低，前臂自然屈曲，把手機輕鬆托握在胸前偏右、離身體少許，手機上緣低於下巴；手腕與前臂形成平順曲線，手指有鬆緊變化，不用力抓住、不把手機擠壓到胸口。另一側右手臂自然垂放、手掌在畫外。保留清楚的右轉方向，但身體呈現有呼吸感的自然站姿。畫面只出現 Amy 一人。除人物替換、這個表演及紙內文字外，全部沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不新增字幕、對話框、警告字卡、水印或額外疊字。
```



## 2026-10-19 shot_4.6.10 GPT v2 — correct 白板參考重生

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；使用者貼上完整 Prompt 要求重生，圖 5 改用 prop_whiteboard_correct.png。本次原文送出，未沿用 v1 的素面粉紅紙限制。
- 機位：cam_twoshot_ms_level（SH03_medium_two_shot／50mm／frame 103），五圖依指定順序輸入。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，事前已告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.10_gpt_v2.png](../assets/images/shot_4.6.10_gpt_v2.png)；保存於 `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.10_gpt_v2.png`，v1 保留。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-4b03f421-c7b7-4a72-a90a-480773b9ff91.png`，原檔保留。
- 生成前觀察：圖 5 的新標語位於中排原黃紙位置，已改為粉紅紙；右側仍有「絕對循環」。使用者文字仍列中排黃紙「地球救星毯」，且將右側中排粉紅便條排除於文字替換之外；已告知圖文差異，未自行改寫要求。
- 檢視：Amy 左側對鏡且嘴唇微啟、小李右側朝左、兩人空手垂放成立。新標語被生成在中排黃紙並混入「地球救星毯」標題，右側粉紅紙仍有四條示意橫線，不符合移除示意線及新粉紅便條的要求；文字與圖 5 未完全一致。兩人頭部仍偏大，小李頭頂較高，Amy 肩線／相對身高及部分便條位置、尺度、遮擋與 blocks 有差異。本版未通過上述項目。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，2,214,777 bytes；來源／目的地 SHA256 一致：`17259949d111086bcfb1cbcf6cc1214902b6d2050feb457bc66dacdccb4a211e`。未裁切、縮放或程式合成。
- 狀態：候選圖待使用者檢視，未確認採用；未修改 asset_manifest／scene_plan／獨立 prompt 檔。本輪實際原文以本紀錄為準，未追加生成或製作影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_correct.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：雙人中景構圖底圖，決定兩人的位置、尺度、頭身比例、距離、可見部位、裁切與白板便條配置。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的紅色定位人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側的藍色定位人物。
圖 5 prop_whiteboard_correct.png：既有白板便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭身比例、頭頂留白、肩線高度與兩人間距。Amy 在左、小李在右，完整頭部、軀幹、手臂及部分手掌依圖 2 入鏡，下半身與手掌邊緣按原下緣裁切。不推近成單人特寫，不把兩人向中央靠攏，也不拉遠補出全身或完整手掌；不要放大頭部、縮短頸部、壓短軀幹或降低人物高度。

將紅色定位人物完整替換為圖 3 的 Amy，將藍色定位人物完整替換為圖 4 的小李；只呈現圖 2 可見部位，不殘留簡化頭部、方塊頸部或色塊身體。人物圖只提供外觀與服裝，不採用其展示姿態或構圖。Amy 延續棕色齊頸短髮、灰色西裝外套與淺色襯衫；小李延續棕色上梳短髮、藍底彩色花襯衫與棕色長褲，不加眼鏡。兩人身體方向及垂放手臂沿用圖 2；Amy 的頭部與視線依下述對鏡表演小幅調整，不改變站位、頭部尺度或肩線高度。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留兩人後方的同一塊便條白板、左右窗格、左側 OA 桌面與螢幕，以及白板下方既有辦公椅局部。採近眼高略俯視、深景深與溫暖自然日光，兩人及白板都清楚，不以強烈散景掩蓋配置。

白板便條紙的外輪廓、位置、大小、透視、人物遮擋與裁切依圖 2。除右側中排粉紅便條外，其餘紙張的示意橫線替換為圖 5 的對應圖文：上排由左至右為綠紙「100%地球救星」、藍紙「純天然無毒擁抱」、粉紅紙「零碳奇蹟」、黃紙「環保魔法」；中排黃紙對應「地球救星毯」；下方由左至右為藍紙「綠色神話」、綠紙「天然之魂」、黃紙「永續至尊」、粉紅紙「環保教主」。文字隨紙張透視與人物遮擋自然裁切，不為了讀完整文案而移動紙張或人物。圖 5 只提供各張便條內容，不採用其整板構圖，不新增第二塊白板，不保留示意橫線。

小李已放開便條，兩人手中均不持紙，不新增另一張粉紅便條，也不重新演出貼紙動作。

畫面描述：
這是一張 Amy 在左、小李在右的雙人中景，兩人的完整頭部、軀幹、自然垂放的手臂及可見手掌依圖 2 呈現，下半身及手掌邊緣維持原裁切，便條白板位於兩人後方。定格在 Amy 從與右側小李的對話轉向觀眾的起始瞬間：雙眼剛移向拍攝鏡頭，頭部跟隨視線略微轉回，臉仍帶輕微偏右角度，目光已與觀眾接觸。她眉眼自然、嘴角放鬆，神情誠懇而堅定，嘴唇微啟準備說「各位觀眾」；頭頸自然直立、下巴平穩，此刻尚未做後段強調語句的點頭。小李安靜看著左側 Amy 的臉，嘴巴自然閉合，保持原站位及雙手垂放姿態，不轉看鏡頭、不點頭、比讚或插話。Amy 的手機已收妥，兩人均不拿手機、海報、筆或檢驗報告，不伸臂自拍。畫面只有兩人，除 Amy 指定的頭部轉向、鏡頭視線、誠懇表情，以及白板右側中排已貼妥的新粉紅便條外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、結語字卡、檢驗報告、數據圖表、認證章、水印或額外疊字。
```

## 2026-10-19 shot_4.6.3 GPT v10 — 鎖定 MCU 便條背景、自然右轉軀幹

- Pipeline／階段：course-51-esg／kj-cinematic／assets／I2I；v9 背景已改善但軀幹偏正面，沿同工具追加一次只動軀幹的相關修正，已先告知。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量及費用未提供。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v10.png](../assets/images/shot_4.6.3_gpt_v10.png)；實際保存於 `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v10.png`。
- 原始輸出：`C:/Users/user/.codex/generated_images/01a15436-86d2-71a1-93e2-48cbbf9480bf/exec-58b2be83-dafe-4633-9be2-8f82366b63ab.png`。
- 檢視：軀幹、肩線與衣襟已有朝右的斜側透視，保持放低的左肘、較低持機位置及放鬆肩頸；相較 v8 減少僵直扭轉與把手機緊貼胸口的姿態。臉及視線仍朝右，表情有局部重畫。四張紙沿用 v9 的正確主要邊界，上排頂部裁切、右上及右下右緣出畫成立，沒有白板下框或額外紙張。
- 便條比對：Pillow／NumPy 唯讀分析四個已知區域的 HSV 色塊可見邊界，下列為 [左,上,右,下]，單位為整張畫面百分比；屬色塊近似邊界，不代表字形或逐像素相同。
  - 上綠：MCU [46.6,0,72.5,15.5]；v10 [46.7,0,72.6,15.4]。
  - 上藍：MCU [76.5,0,100,15.1]；v10 [76.4,0,100,15.3]。
  - 中藍：MCU [47.4,49.5,73.8,81.7]；v10 [48.0,49.5,73.9,81.7]。左緣約差 0.6 個百分點，其餘主要邊界差約 0.2 個百分點內。
  - 右下綠：MCU [78.2,67.8,100,96.2]；v10 [78.2,67.8,100,96.3]。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，1,966,367 bytes；複製前後 SHA256 相同：`3d2d7cf13e6382bb1b526b42cfedfe6bec53fff7e0889a2e1d4adc13402972de`。未裁切、放大或程式合成。文字有重繪與換行變動，人物並非白模像素級重合；未宣稱精確 30 度。
- 狀態：已交付 v10，待使用者確認採用；保留 v9 及所有舊版，未更新 asset_manifest／scene_plan，未追加其他生成。

有序參考圖：

1. `D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.6.3_gpt_v9.png`

完整 Prompt：

```text
以圖 1 shot_4.6.3_gpt_v9.png 為編輯底圖，只修改 Amy 頸部以下的軀幹與隨之連動的手臂姿態。

讓她自然地轉身面向畫外右側的小李，胸口與可見腰部整體朝畫面右側約 30 度，與她現在臉部的朝向一致。不是只轉頭。畫面左側的右肩較靠近鏡頭，畫面右側的左肩退後，胸前襯衫及兩側外套有清楚的斜側透視，遠側衣襟變窄，不能再把胸口及兩肩攤平正對鏡頭。保留頭部位置、人物中央偏左的站位和原有人物大小。

這是日常對話中的自然站姿：肩頸放鬆，兩肩自然下沉，胸腰有一點柔和的角度差與自然重量感，身體略朝對話者靠近，軀幹曲線平順。避免軍姿、聳肩、刻意挺胸、繃緊腹部、強烈扭腰、後仰或時裝模特兒擺拍；西裝保留鬆量與柔軟皺摺，不塑造成僵硬盔甲。不要把肩膀、胸腔及腰部畫成同一塊僵直平板。

左手仍在畫面右側自然持同一支直向手機，沿用原圖較低、放鬆的持機高度，手機上緣明顯低於下巴，離胸口一小段距離。左上臂隨肩膀轉身但自然靠近身側，手肘放低，前臂與手腕形成流暢曲線，輕鬆托握而非緊抓。另一側手臂維持放鬆垂下。保留同一張臉、棕色短髮、眼睛、眉心微皺與說話表情，以及朝畫外右側的視線。

圖 1 的背景已經正確，完全保留：黑窗格、桌面、隔板、螢幕、日光斜線、白板表面與四張綠／藍紙。四張紙的每個邊緣、位置、大小、顏色、文字和裁切均不得改動；上排兩張保持頂部出畫，中藍紙保持大尺寸，右下綠紙保持右緣出畫，白板下框保持在畫外。只允許人體新輪廓自然遮擋背景，不改任何未被人物遮住的背景區域。不得縮紙、補出整張便條、移動字、出現板框或增加其他紙張。

保持原圖的近眼高中近景、取景、人物頭頂留白、下緣裁切、畫幅與光影。只輸出一張 16:9 修正版，不加人、字幕、對話框、水印或其他疊字。
```



## 2026-10-19 — street / cam_street_wide_low_angle / GPT v1

- 任務：街景簡模視角圖之風格／材質／光影重繪；非劇本 shot，沿用場景機位命名。
- 輸出：`references/scenes/street/cameras/cam_street_wide_low_angle_empty_gpt.png`，原生 1672×941 RGB PNG（2,393,428 bytes）。
- 工具：內建 image_gen，I2I；確切模型與費用未回傳，不填零；本輪 1 次生成。
- 原生輸出：`C:/Users/user/.codex/generated_images/01a12bb4-fa88-7152-87df-ca94a27216f3/exec-7def67a8-e8f4-443c-bdc2-622158421cd1.png`。
- 檢視：主要低角度取景、左右建築關係及無人空景成立；玻璃反射、石材、自然葉片與暖色日光改善。窗框細節、葉形、遠處建築細節有 AI 差異，非像素或 3D 幾何一致保證。未改來源 blend／Blender 底圖，未更新 asset_manifest 採用版本。

有序參考圖：

1. `D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_street_wide_low_angle_empty_blender.png` — 編輯底圖／構圖。
2. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/Amy_George_走回公司_2K.png` — 場景風格／材質／光影；不帶入人物。

完整 Prompt：

```text
Use case: style-transfer.
Input image 1 is the EDIT TARGET: the empty Blender street preview, cam_street_wide_low_angle_empty_blender.png.
Input image 2 is the STYLE AND SURFACE REFERENCE: Amy_George_走回公司_2K.png. Use only its environmental art direction, materials, color palette, daylight and atmosphere. Its woman and background pedestrians are not to be transferred.

Re-render image 1 as a polished cinematic stylized 3D animated-film environment with the rich surface treatment and inviting light of image 2. Keep image 1's exact low camera viewpoint, framing, perspective convergence, pedestrian corridor width, building silhouettes, facade divisions, doorway and canopy positions, paving perspective, and existing tree and planter positions. Preserve the left blue-glass office facade and the right warm limestone facade. Do not copy the reference image's camera or redesign the street.

Replace the flat blockout surface appearance with convincing blue-tinted architectural glazing, layered sky and building reflections, subtle metal window frames, finely textured warm limestone, and tactile pale stone paving with fine joints. Translate the existing simplified vegetation volumes into natural leafy trees and upright shrubs with varied small leaves, delicate branches and red-orange blossoms, within the same tree/planter footprints and approximate silhouettes. The orange spheres in the target are placeholders for flowering plants, not fruit. Refine the existing overhead canopies as thin transparent glass with metal supports while keeping their geometry and placement.

Match image 2's luminous cool cyan-blue daylight, warm golden sunlight grazing the right building and pavement, soft directional shadows, gentle atmospheric depth and warm/cool color contrast. Retain enough clarity to read the architecture. Do not retain the dull flat primitive shading of the target. This is an empty environment: zero people, silhouettes, human reflections, vehicles, signs, lettering or watermarks. Add no extra trees, planters, vines, buildings, canopies or street furniture. Deliver one full-frame landscape 16:9 image.
```


## 2026-10-19 shot_4.6.3 GPT v11 — 使用者原文五圖重生

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；依使用者本次貼上的完整 Prompt 原文生成，包含「完整頭部、頸部、肩膀與部分上半身入鏡(都要朝向畫面的右側約 30 度)」的新增強調。
- 參考：MCU Blender 空景與 blocks、Amy、incorrect 白板圖文、手機，共五張；沒有使用舊生成圖作底圖。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，事前已告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v11.png](../assets/images/shot_4.6.3_gpt_v11.png)；保存於 `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.3_gpt_v11.png`。v2～v10 保留。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-5a90fc00-5bbe-4996-8ca1-ccf73012094c.png`，原檔保留。
- 檢視：Amy 單人、臉與視線朝右略上、微皺眉與微張嘴、左手持深灰三鏡頭手機且上緣低於下巴成立。四張綠／藍便條及上排頂部出畫、右上／右下右緣出畫大致成立，沒有多出粉紅紙、黃紙、白板下框或筆槽。軀幹仍偏正面，未清楚達成與臉一致的朝右約 30 度；頭部較 blocks 偏大、頭頂留白減少。部分紙張邊界、遮擋、字形與換行仍有重畫，未宣稱像素級一致。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，1,976,251 bytes；來源／目的地 SHA256 一致：`9f9b23f3fe22142377db73f79232c6b38088d887780353cac54c4c2ed1948fe6`。未裁切、縮放或程式合成。
- 狀態：候選圖待使用者檢視，未更新 asset_manifest／scene_plan／獨立 prompt 檔；本輪實際原文及圖序以本紀錄為準。未追加生成或製作影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_blender.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_blender.png：同機位行銷辦公室空景，提供場景外觀、材質與光影。
圖 2 cam_amy_mcu_15deg_block_blender.png：本鏡構圖底圖，決定人物位置、尺度、頭頂留白、裁切，以及白板與四張便條紙的配置。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物，只提供外觀與服裝。
圖 4 prop_whiteboard_incorrect.png：四張指定便條紙的圖文與紙質參考，不提供整板構圖。
圖 5 prop_smartphone.png：Amy 手中手機的外觀參考，不採用多視圖排列或來電介面。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、背景配置、人物位置、頭部尺度、頭頂留白、自然頸部長度與下緣裁切。Amy 位於畫面中央偏左，完整頭部、頸部、肩膀與部分上半身入鏡(都要朝向畫面的右側約 30 度)；不要放大頭部、縮短頸部、把人物移到正中央，或拉遠補出腰部與完整手臂。人物朝向及持手機所需的肩臂調整依下述表演，其餘沿用圖 2。

將紅色定位人物完整替換為圖 3 的 Amy，延續棕色微捲短髮、綠色眼睛、灰色西裝外套與白色襯衫。只呈現本鏡可見的部位，不殘留方塊頸部、紅色軀幹或簡化四肢，也不把白模的方肩與僵直身體套到 Amy 身上。西裝自然包覆身體，保留柔軟摺痕與鬆量。

將場景材質與光影更新為圖 1 的外觀，空間配置仍以圖 2 為準。保留左側既有辦公桌、深色隔板、黑色螢幕與黑色窗格，以及右側同一塊白板及其斜向日光。採近眼高、固定機位與深景深，不用強烈散景掩蓋背景。

白板左側直框維持原位置；白板頂框、底框與右框均在畫外，不補出下方筆槽、腳架或地面。畫面只出現圖 2 原有的四張綠色／藍色便條，不增加粉紅紙、黃紙或第二塊白板。

四張便條的輪廓、大小、位置、透視與裁切直接沿用圖 2，只將紙內黑色示意橫線替換成圖 4 的對應圖文：
1. 上方綠紙對應「100%地球救星」。只露出原紙下段，上緣與上方部分文字在畫外，不把整張紙縮小或往下移以顯示完整標題。
2. 右上藍紙對應「純天然無毒擁抱」。紙張上緣及右緣均伸出畫外，保留原裁切，不補出完整頂邊或右邊。
3. 中段大藍紙對應「綠色神話」。維持約畫面四分之一寬、三分之一高的原尺寸，左下部分依 Amy 的肩膀、前臂及手機輪廓自然遮擋，不縮成小便條或移往空白處。
4. 右下綠紙對應「天然之魂」。維持靠近畫面底部的位置，右緣延伸出畫外；不把紙張上移，也不補出右側被裁掉的內容。

文字隨原紙透視、人物遮擋及畫面邊界自然裁切。超出取景的內容保持不可見，不為了塞入完整文案而縮字、縮紙、重排文字或移動人物。圖 4 的其他紙張及整板配置不參與生成；移除示意橫線，保留原有誇大文案，不改成正確宣傳標語。

手機採圖 5 的深灰機身、邊框厚度與三鏡頭模組，尺寸與 Amy 手掌相稱。只出現一支直向手機，螢幕朝 Amy，觀眾看見背面及側邊，不呈現來電介面、搜尋文字、法規頁面或錄影畫面。

畫面描述：
這是一張 Amy 單人的中近景，左側是辦公桌、隔板、螢幕與窗格局部，右側及人物後方是既有白板與四張綠／藍便條。定格在 Amy 已查完手機、抬眼向小李提醒的瞬間：她的臉、胸口與可見上半身都朝畫面右側約 30 度，雙眼看向畫外右側小李的臉部高度，眉心微皺、嘴唇微啟，表情認真而帶一點擔憂。軀幹必須呈現清楚但自然的右轉斜側透視，畫面左側的右肩較靠近鏡頭，畫面右側的左肩略退後，襯衫門襟與外套翻領隨胸口一起轉向右側；不要讓胸口正對鏡頭而只轉頭。肩頸放鬆，胸廓與可見軀幹保留自然曲線，不聳肩、刻意挺胸、後仰或強烈扭腰。左手位於畫面右側，自然托握手機於胸前偏右，手機上緣明顯低於下巴，與胸口保留少許距離；左上臂放鬆靠近身側，手肘自然放低，前臂、手腕與手指形成舒適的持握姿勢，不把手機緊壓胸口，也不為露出完整手肘而改變取景。另一側右手臂自然垂放，手掌保持在畫外。畫面只出現 Amy 一人，小李、海報與其他人物均不入鏡。除人物替換、自然右轉的姿態、持手機動作、表情視線及紙內圖文外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，只呈現上述單一瞬間，不加入字幕、對話框、警告字卡、水印或額外疊字。
```

## 2026-10-19 — street / Amy + George walking / block GPT v1–v2
- 任務：右側 Amy／George 並肩走路聊天，中後景五名路人；非劇本 shot，沿用場景機位命名。工具為 Blender 5.2.2 Cycles CUDA／64 samples＋內建 image_gen；確切 GPT 模型／費用未提供，共 2 次生成。
- 模型 `references/scenes/street/street_with_people.blend`；底圖 `references/scenes/street/cameras/cam_street_wide_low_angle_block_blender.png`（1920×1080）。單一 07_PEOPLE_BLOCKS 集合、7 人、每人 18 身體物件；原 1786 物件矩陣與相機不變。重開 blend、看圖及交付複製雜湊驗證通過。
- v1 `references/scenes/street/renders/archive/cam_street_wide_low_angle_block_gpt_v1.png`（1672×941 RGB，2,348,826 bytes）：外觀、互看聊天、走路及五名路人成立，但所有人物被放大。
- v2 `references/scenes/street/cameras/cam_street_wide_low_angle_block_gpt.png`（1672×941 RGB，2,263,223 bytes）：人物縮小修正版；主角仍比 block 小、腳底較高，背景路人尺度也非精確一致。兩版已視覺檢查與解碼，保留供使用者評鑑，不宣稱幾何精確對齊；未更改 manifest 採用。
- 原始空景模型／Blender 空景／GPT 空景保留；本次只做單張走路瞬間，沒有動畫。腳本 `.tmp/pose_street_walkers.py`；投影檢查 `.tmp/street_people_qa.json`。
v1 有序輸入：
1. `D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_street_wide_low_angle_empty_gpt.png`
2. `D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_street_wide_low_angle_block_blender.png`
3. `D:/Dropbox/kj-om-projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/Dropbox/kj-om-projects/course-51-esg/clp/char_george.png`
v1 完整 Prompt：
```text
參考圖說明：
圖 1 cam_street_wide_low_angle_empty_gpt.png：街景外觀參考圖，提供材質、自然植栽、反射、顏色、光影及氣氛。
圖 2 cam_street_wide_low_angle_block_blender.png：本次編輯底圖，提供相機取景、透視、所有人物的佔位、比例、行走姿勢與遮擋關係。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物；多視圖是同一位角色的外觀資料。
圖 4 char_george.png：George 人物參考圖，對應圖 2 的藍色人物；多視圖是同一位角色的外觀資料。

生圖指引：
以圖 2 為編輯底圖，保留其低角度相機、透視、物件配置、人物佔位、顯示範圍與遮擋關係。保留兩位主角的完整頭腳、畫面中的大小、彼此間距及腳下留白，不放大或前移主角。紅色定位人替換成圖 3 的 Amy，藍色定位人替換成圖 4 的 George；採用人物參考的臉、髮型、服裝與配件，不採用參考圖的展示站姿、拼貼構圖或背景。Amy 為棕色短髮、灰色褲裝的角色；George 保留灰髮、棕框眼鏡、棕色背心與奶油色襯衫，不能保留紅藍定位服裝或方塊肢體。
把圖 2 的背景材質、風格與光影更新為圖 1 的精緻街景外觀，保留圖 2 的空間配置；玻璃大樓、石材外牆、玻璃雨棚、自然樹葉與花盆延續圖 1，避免方塊植栽與平塗材質。灰色定位人替換為五名不同外觀的背景上班族，僅用常見商務便裝、低調各異的色彩及自然步行姿態；保持各自大小、位置和朝向，不複製主角五官、髮型或整套服裝。

畫面描述：
這是一張從近地面朝街道縱深拍攝的 16:9 全身雙人廣角畫面。Amy 與 George 並肩走在畫面右側的步行空間，兩人完整入鏡，避開花盆與入口。呈現邊走邊愉快聊天的一個瞬間：Amy 轉頭看向 George，嘴角帶笑，左手如底圖輕抬做小幅說話手勢，另一手自然擺動；George 轉頭看 Amy，微笑聆聽回應。兩人的身體沿著行走方向，雙腿維持底圖錯開的步態，膝蓋、肘部與肩頸自然放鬆，腳與鋪面有正確接觸、柔和投影和重量感。中後景五位路人自然走動，尺度隨距離縮小，主角周圍保持通暢。沿用圖 1 的溫暖金色日光、清透藍色玻璃反射與電影動畫質感。除表情、自然人體造型及上述材質替換外，其餘沿用圖 2。

輸出一張 16:9 彩色完整畫面；共七個人（Amy、George 與五名路人），不增加行人、不加入車輛、字幕、拼貼、標示或水印。
```
v2 有序輸入：
1. `references/scenes/street/renders/archive/cam_street_wide_low_angle_block_gpt_v1.png`（送出時使用同內容原生檔 `C:/Users/user/.codex/generated_images/01a12bb4-fa88-7152-87df-ca94a27216f3/exec-9a33e6bc-568e-4a6e-b3f9-a2d34c1c2e80.png`）。
2. `references/scenes/street/cameras/cam_street_wide_low_angle_block_blender.png`。
v2 完整 Prompt：
```text
以圖 1 的完整彩色街景作為唯一編輯底圖。圖 2 是相同相機的 Blender 人物佔位圖。
本次只修正七個人物在畫面中的大小與位置：圖 1 把所有人放大了，請讓每位人物的頭頂、腳底、身體中心及可見外框對齊圖 2 對應的 block。用圖 2 的人物投影比例與位置；不以圖 2 的方塊人體外觀或顏色取代正式人物。其餘完全保留圖 1 的材質、建築、鏡位、鋪面、天空、日光、雨棚和植物。
兩位主角仍然全身在畫面右側。Amy 對齊紅色 block：外框約佔整張圖 x=60.4%～71.2%，從畫面頂端往下 y=59.5%～98.6%。George 對齊藍色 block：x=74.5%～83.4%，從畫面頂端往下 y=57.3%～97.8%。這些座標只表示人物佔位，不能印在圖上。人物應明顯縮小，頭頂落在畫面中線以下，不能維持圖 1 現在的大人物比例。保留自然人體比例，不拉伸或壓扁身體。保留 Amy、George 的臉、服裝、愉快表情、轉頭看對方、抬手聊天與行走姿態。
背景五位路人也一一對齊圖 2 的五個灰色 block，縮小到正確遠近尺度；不新增、刪除或複製任何人。人物移動後露出的區域，連續補回原有圖 1 的街景，接觸陰影配合調整。只輸出一張 16:9 彩色圖片，無文字、水印或拼貼。
```


## 2026-10-19 shot_4.6.3 GPT v12 — GPT 空景與自身左轉原文

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；依使用者本次貼上的完整 Prompt 原文重生，圖 1 改為 cam_amy_mcu_15deg_empty_gpt.png，方向文字保留「朝向amy的左手邊約 30 度」及「朝amy的左手邊(左側)約 30 度」。
- 參考：MCU GPT 空景、Blender blocks、Amy、incorrect 白板圖文、手機，共五張；未以舊生成圖為輸入。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，事前已告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v12.png](../assets/images/shot_4.6.3_gpt_v12.png)；保存於 `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.3_gpt_v12.png`，舊版本保留。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-f1521cbf-2e45-41f4-a04f-9886d165c064.png`，原檔保留。
- 檢視：場景呈現圖 1 的明亮暖光與淺色窗框，Amy 單人、臉與視線朝右略上、微張嘴、左手持深灰三鏡頭手機且上緣低於下巴成立。四張綠／藍便條及上排頂部、右側紙邊出畫成立，沒有額外紙張或白板下框。軀幹仍偏正面，未清楚呈現與臉一致的自身左轉約 30 度；頭部較 blocks 偏大，中段藍紙左緣右移、紙寬縮窄，文字、換行與遮擋仍有重畫，未完全符合要求。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，2,178,197 bytes；來源／目的地 SHA256 一致：`f90a146ef17f2dfff967c094221ad0d1120b4d3314d1b394f8811c02d6ad6c01`。未裁切、縮放或程式合成。
- 狀態：候選圖待使用者檢視，未更新 asset_manifest／scene_plan／獨立 prompt 檔；本輪實際原文及圖序以本紀錄為準。未追加生成或製作影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_mcu_15deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_gpt.png：同機位行銷辦公室空景，提供場景外觀、材質與光影。
圖 2 cam_amy_mcu_15deg_block_blender.png：本鏡構圖底圖，決定人物位置、尺度、頭頂留白、裁切，以及白板與四張便條紙的配置。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物，只提供外觀與服裝。
圖 4 prop_whiteboard_incorrect.png：四張指定便條紙的圖文與紙質參考，不提供整板構圖。
圖 5 prop_smartphone.png：Amy 手中手機的外觀參考，不採用多視圖排列或來電介面。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、背景配置、人物位置、頭部尺度、頭頂留白、自然頸部長度與下緣裁切。Amy 位於畫面中央偏左，完整頭部、頸部、肩膀與部分上半身入鏡(都要朝向amy的左手邊約 30 度)；不要放大頭部、縮短頸部、把人物移到正中央，或拉遠補出腰部與完整手臂。人物朝向及持手機所需的肩臂調整依下述表演，其餘沿用圖 2。

將紅色定位人物完整替換為圖 3 的 Amy，延續棕色微捲短髮、綠色眼睛、灰色西裝外套與白色襯衫。只呈現本鏡可見的部位，不殘留方塊頸部、紅色軀幹或簡化四肢，也不把白模的方肩與僵直身體套到 Amy 身上。西裝自然包覆身體，保留柔軟摺痕與鬆量。

將場景材質與光影更新為圖 1 的外觀，空間配置仍以圖 2 為準。保留左側既有辦公桌、深色隔板、黑色螢幕與黑色窗格，以及右側同一塊白板及其斜向日光。採近眼高、固定機位與深景深，不用強烈散景掩蓋背景。

白板左側直框維持原位置；白板頂框、底框與右框均在畫外，不補出下方筆槽、腳架或地面。畫面只出現圖 2 原有的四張綠色／藍色便條，不增加粉紅紙、黃紙或第二塊白板。

四張便條的輪廓、大小、位置、透視與裁切直接沿用圖 2，只將紙內黑色示意橫線替換成圖 4 的對應圖文：
1. 上方綠紙對應「100%地球救星」。只露出原紙下段，上緣與上方部分文字在畫外，不把整張紙縮小或往下移以顯示完整標題。
2. 右上藍紙對應「純天然無毒擁抱」。紙張上緣及右緣均伸出畫外，保留原裁切，不補出完整頂邊或右邊。
3. 中段大藍紙對應「綠色神話」。維持約畫面四分之一寬、三分之一高的原尺寸，左下部分依 Amy 的肩膀、前臂及手機輪廓自然遮擋，不縮成小便條或移往空白處。
4. 右下綠紙對應「天然之魂」。維持靠近畫面底部的位置，右緣延伸出畫外；不把紙張上移，也不補出右側被裁掉的內容。

文字隨原紙透視、人物遮擋及畫面邊界自然裁切。超出取景的內容保持不可見，不為了塞入完整文案而縮字、縮紙、重排文字或移動人物。圖 4 的其他紙張及整板配置不參與生成；移除示意橫線，保留原有誇大文案，不改成正確宣傳標語。

手機採圖 5 的深灰機身、邊框厚度與三鏡頭模組，尺寸與 Amy 手掌相稱。只出現一支直向手機，螢幕朝 Amy，觀眾看見背面及側邊，不呈現來電介面、搜尋文字、法規頁面或錄影畫面。

畫面描述：
這是一張 Amy 單人的中近景，左側是辦公桌、隔板、螢幕與窗格局部，右側及人物後方是既有白板與四張綠／藍便條。定格在 Amy 已查完手機、抬眼向小李提醒的瞬間：她的臉、胸口與可見上半身都朝amy的左手邊(左側)約 30 度，雙眼看向畫外右側小李的臉部高度，眉心微皺、嘴唇微啟，表情認真而帶一點擔憂。軀幹必須呈現清楚但自然的右轉斜側透視，畫面左側的右肩較靠近鏡頭，畫面右側的左肩略退後，襯衫門襟與外套翻領隨胸口一起轉向右側；不要讓胸口正對鏡頭而只轉頭。肩頸放鬆，胸廓與可見軀幹保留自然曲線，不聳肩、刻意挺胸、後仰或強烈扭腰。左手位於畫面右側，自然托握手機於胸前偏右，手機上緣明顯低於下巴，與胸口保留少許距離；左上臂放鬆靠近身側，手肘自然放低，前臂、手腕與手指形成舒適的持握姿勢，不把手機緊壓胸口，也不為露出完整手肘而改變取景。另一側右手臂自然垂放，手掌保持在畫外。畫面只出現 Amy 一人，小李、海報與其他人物均不入鏡。除人物替換、自然右轉的姿態、持手機動作、表情視線及紙內圖文外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，只呈現上述單一瞬間，不加入字幕、對話框、警告字卡、水印或額外疊字。
```


## 2026-10-19 shot_4.6.3 GPT v13 — 頭頸肩胸整體朝右

- Pipeline／階段：course-51-esg／kj-cinematic／assets／I2I；依使用者要求「身體軀幹(臉、脖子、肩膀)要一起轉向畫面的右邊30度」，以 v12 局部修改整個上半身朝向。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，事前已告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.3_gpt_v13.png](../assets/images/shot_4.6.3_gpt_v13.png)；保存於 `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.3_gpt_v13.png`，v12 與其他舊版保留。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-08b77505-eb09-4bc0-a0c6-6bff9f95ee31.png`，原檔保留。
- 檢視：相較 v12，臉、脖子、肩線、胸口及衣襟已有一致朝畫面右側的斜側透視，近側右肩較清楚、遠側左肩退後，軀幹不再維持原正面姿態；視線仍朝右，左手持手機隨上半身連動，手機上緣低於下巴。頭髮、表情及手臂局部重畫，背景與四張便條的主要位置、文字及裁切維持 v12。依視覺確認本輪整體轉向已改善，未量測或宣稱精確 30 度；v12 已有中段藍紙尺寸偏差未在本輪修正。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，2,151,158 bytes；來源／目的地 SHA256 一致：`239874b7da977a8a973eb4b41f3dbb66f1c05f02b0e00624de1c6312cfd3fe85`。未裁切、縮放或程式合成。
- 狀態：已交付修正版待使用者確認採用，asset_manifest／scene_plan／獨立 prompt 檔未改；未追加生成或製作影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.3_gpt_v12.png`

完整 Prompt：

```text
以圖 1 shot_4.6.3_gpt_v12.png 為編輯底圖，只修改 Amy 的整體上半身朝向。使用者要求：「身體軀幹(臉、脖子、肩膀)要一起轉向畫面的右邊30度」。

讓 Amy 的臉、頭部、脖子、兩側肩膀、胸口與可見軀幹一起自然轉向畫面右側，最後相對正面鏡頭約 30 度。這是整個上半身一致的轉身：胸骨、襯衫門襟、外套翻領與臉部朝向都指向同一個畫外右側對話者。現在幾乎正對鏡頭的肩胸必須真正轉過去，不能只改眼睛、只轉頭或歪脖子。不要在臉部原有角度上額外再轉 30 度，最終讓臉與軀幹的朝向一致。

從觀眾看去，畫面左側的 Amy 右肩較靠近鏡頭，畫面右側的 Amy 左肩退向後方；近側肩膀與西裝側面較清楚，遠側肩膀及外套胸片因透視變窄。胸口、襯衫門襟與兩側翻領呈現清楚的右轉斜側透視，不再把兩肩與胸口平攤朝向鏡頭。為了完成這個轉身，可以重畫頭頸、肩胸、外套及相連手臂的輪廓；不要把原本正面的胸腔鎖死。頭頸自然直立，肩膀放鬆，不聳肩、側彎、後仰或強烈扭腰。

保留同一位 Amy 的五官辨識、棕色微捲短髮、綠色眼睛、灰色西裝及白色襯衫。她仍看著畫外右側的小李，眉心微皺、嘴唇微啟，維持認真提醒的表情。頭部與人物整體尺度、頭頂留白、中央偏左的佔位及下緣裁切沿用原圖，不推近、不拉遠、不搬動站位。

左手仍在畫面右側持同一支直向深灰三鏡頭手機，手機上緣低於下巴，維持原持機高度與離胸口的距離。左肩、左上臂、前臂及手腕隨上半身轉向自然連動，手肘放鬆、持握舒適；螢幕仍朝 Amy，觀眾主要看見背面。另一側右手臂維持自然垂放，不新增手勢或物件。

完整保留圖 1 的背景、原相機透視、光影與 16:9 畫幅，包括窗格、辦公桌、隔板、螢幕、白板及四張綠／藍便條。便條的每個邊緣、位置、大小、文字與裁切均沿用原圖，不縮放、移位或改字，不增加紙張、板框或筆槽。背景只接受轉身後人物輪廓造成的必要遮擋或露出，其餘區域保持原樣。

輸出一張修正版，讓臉、脖子、肩膀及胸口都清楚呈現同一次朝畫面右側約 30 度的自然轉身。不加字幕、對話框、水印或額外疊字。
```


## 2026-10-19 shot_4.6.10 GPT v3 — 十張便條與相對身高要求

- Pipeline／階段：course-51-esg／kj-cinematic／assets／W2I；依使用者本次完整 Prompt 原文生成，指定兩人髮頂約畫面高度 20%、下巴約 38%、肩頸交界約 45%，以及十張便條全部替換。
- 機位／參考：cam_twoshot_ms_level（SH03／50mm／frame 103），GPT 空景、Blender blocks、Amy、小李及 prop_whiteboard_correct.png，共五圖。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與費用未提供，事前已告知無法估價。一次、一張，transparent_background=false。
- 輸出：[shot_4.6.10_gpt_v3.png](../assets/images/shot_4.6.10_gpt_v3.png)；保存於 `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.6.10_gpt_v3.png`，v1／v2 保留。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a1537a-8da2-76e3-aef1-3c46884ed2a7/exec-54f5ce4b-0d75-456b-8e98-d2430125fc2a.png`，原檔保留。
- 檢視：Amy 左側對鏡、微張嘴，小李右側朝左聆聽，兩人空手垂放成立。十張便條均有圖文，沒有示意橫線；中排偏左已由黃紙改為新標語粉紅紙，沒有混入「地球救星毯」舊標題，右側粉紅紙恢復「絕對循環」文案。人物比例仍未符合：小李頭部明顯偏大且髮頂比 Amy 高，兩人的髮頂也未落在指定約 20% 高度；相對身高、頭部尺度及部分便條位置／遮擋與 blocks 仍有差異。字形與換行有重畫，未宣稱逐字或像素級一致。
- 連戲：本輪依使用者最新明示，新標語位於中排偏左原黃紙位置；覆蓋先前本鏡「右側粉紅紙留白供後製」的生成要求。本次未回寫其他鏡頭、scene_plan 或獨立 prompt 檔。
- 驗證：Pillow 完整解碼，1672×941 RGB PNG，2,245,483 bytes；來源／目的地 SHA256 一致：`926189cd48fd023a21537ef0300eb215886157d3b38b17e9289fb3ccde5bdecc`。未裁切、縮放或程式合成。
- 狀態：候選圖待使用者檢視，人物比例未通過，未確認採用；asset_manifest 未改，未追加生成或製作影片。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_ms_level_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_correct.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：雙人中景構圖底圖，決定兩人的位置、相對身高、頭身比例、距離、可見部位、裁切與白板便條配置。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側的紅色定位人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側的藍色定位人物。
圖 5 prop_whiteboard_correct.png：白板上各張便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭身比例、頭頂留白、肩線高度與兩人間距。Amy 在左、小李在右，完整頭部、頸部、軀幹、手臂及部分手掌依圖 2 入鏡，下半身與手掌邊緣按原下緣裁切。嚴格維持圖 2 兩人的頭部大小與相對高度：兩人頭頂（含髮型）均位於畫面高度約 20%（與上排便條紙下半部齊高，小李髮頂不可超過白板上框），下巴約在畫面高度 38%，肩頸交界約在畫面高度 45%，保留清楚直立的頸部與成年人自然頭身比例；不要放大頭部、縮短頸部，也不要把小李畫得比 Amy 高大。

將紅色定位人物完整替換為圖 3 的 Amy，將藍色定位人物完整替換為圖 4 的小李；只呈現圖 2 可見部位，不殘留簡化頭部、方塊頸部或色塊身體。人物圖只提供外觀與服裝，不採用其展示姿態或構圖。Amy 延續棕色齊頸微捲短髮、灰色西裝外套與淺色襯衫；小李延續棕色上梳短髮、藍底彩色花襯衫、白色內搭與棕色長褲，不加眼鏡。兩人站位與自然垂放的手臂沿用圖 2。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留兩人後方的同一塊便條白板、左右窗格、左側 OA 桌面與螢幕，以及白板下方既有辦公椅局部。採近眼高略俯視、深景深與溫暖自然日光，兩人及白板都清楚。

白板上全部十張便條紙的外輪廓、位置、大小、透視、人物遮擋與裁切完全依圖 2，將全部十張紙內的黑色示意橫線逐一替換為圖 5 對應位置的圖文與紙色，不保留任何黑色示意橫線：
- 上排由左至右四張：綠紙「100% 地球救星！」、淺藍紙「純天然無毒擁抱：」、粉紅紙「零碳奇蹟：」、黃紙「環保魔法：」。
- 中排兩張：中排偏左（原黃紙位置）依圖 5 改為粉紅紙「每件毛毯，都由8個回收寶特瓶製成。溫暖你，也溫暖地球。」，不混入舊標題「地球救星毯」；中排右側粉紅紙依圖 5 替換為「絕對循環：我們的包裝可以無限次回收，永不產生垃圾。」，不可殘留黑色示意橫線。
- 下排由左至右四張：淺藍紙「綠色神話：」、綠紙「天然之魂：」、黃紙「永續至尊：」、粉紅紙「環保教主：」。
文字隨紙張透視與人物遮擋自然裁切，不為了露出完整文案而移動紙張或人物。圖 5 只提供各張便條的顏色與文字內容，不採用其整板構圖，不新增第二塊白板。小李已放開便條，兩人手中均不持紙。

畫面描述：
這是一張 Amy 在左、小李在右的 50mm 雙人中景，兩人的完整頭部、直立頸部、軀幹、自然垂放的手臂及可見手掌依圖 2 呈現，下半身及手掌邊緣維持原裁切，便條白板位於兩人後方。定格在 Amy 從與右側小李的對話轉向觀眾的起始瞬間：雙眼剛移向拍攝鏡頭，頭部跟隨視線略微轉回，臉仍帶輕微偏右角度，目光已與觀眾接觸。她眉眼自然、嘴角放鬆，神情誠懇而堅定，嘴唇微啟準備說「各位觀眾」；頭頸自然直立、不歪頭，此刻尚未做後段強調語句的點頭。小李站在右側，臉朝左安靜看著 Amy，嘴巴自然閉合，保持原站位及雙手垂放姿態，不轉看鏡頭、不比手勢。Amy 的手機已收妥，兩人均不拿手機、海報、便條紙或筆，不伸臂自拍。畫面只有兩人，除 Amy 指定的頭部轉向、鏡頭視線、誠懇表情，以及白板十張便條替換為圖 5 圖文外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、結語字卡、檢驗報告、數據圖表、認證章、水印或額外疊字。
```


## 2026-10-19 shot_4.6.7 GPT v2 — 巨大前景與上半身朝右要求

- 專案／階段：course-51-esg／kj-cinematic／asset；只重做本鏡，以使用者本次完整 prompt 原文及指定五圖順序執行 W2I。
- 工具／供應商：內建 image_gen／OpenAI；未回傳確切模型名稱與計費，費用未知；本次只生成一次。
- 輸出：[shot_4.6.7_gpt_v2.png](../assets/images/shot_4.6.7_gpt_v2.png)；1672×941、RGB PNG、2096033 bytes。
- 原始輸出：`C:\Users\servi\.codex\generated_images\01a1537a-8da2-76e3-aef1-3c46884ed2a7\exec-f5f56cf8-a8c5-4464-9043-f5cdbbc6dd71.png`；保留原檔，複製至專案素材目錄。
- 目視結果：小李維持右側巨大前景、頭頂及右側裁切；Amy 的臉與視線朝右，兩人間有綠色辦公椅及木桌，手與手機未入鏡。淺藍便條呈現指定「綠色神話」文案，沒有示意橫線。
- 未通過項目：Amy 胸口與肩線仍偏正面，未明確呈現整個上半身約 35 度朝右；頭部相對底圖偏大、頸部可見長度較短。小李左耳與白板左框有間距，頸肩及白板遮擋未嚴格沿用底圖；淺藍紙高度偏小，下方綠紙與黃／粉紅紙可見範圍有差異。前景仍有柔化，未達要求的全畫面清晰。精確角度未量測。
- 驗證：已檢視生成圖與構圖底圖、Pillow 完整解碼，來源與專案複本內容一致；SHA-256 `8c141c2dceeb15a745ba4e58a11c3861adabdfe490b66b6263d2555168d25e43`。
- 狀態：待使用者檢視，未自動採用；保留 v1，未修改 asset_manifest.json、scene_plan 或獨立 prompt 檔，未追加生成。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_ots_li_ms_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_amy_ots_li_ms_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_li.jpeg`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_whiteboard_incorrect.png`

完整 Prompt：

```text
參考圖說明：
圖 1 cam_amy_ots_li_ms_empty_gpt.png：行銷辦公室場景外觀參考圖。
圖 2 cam_amy_ots_li_ms_block_blender.png：本鏡 55mm 過肩構圖底圖，決定兩人的位置、尺度、頭身比例、前後距離、可見範圍與白板遮擋關係。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側中景的紅色定位人物。
圖 4 char_li.jpeg：小李人物參考圖，對應圖 2 右側近距離前景的藍色定位人物。
圖 5 prop_whiteboard_incorrect.png：白板上各張便條紙的外觀與圖文內容參考。

生圖指引：
以圖 2 為編輯底圖，嚴格保留其取景、透視、物件配置、人物佔位、頭身比例與邊緣裁切：
- 右側近距離前景的小李（藍色定位人物）：必須維持圖 2 極近距離的巨大前景佔位（頭部橫跨畫面水平約 54%–100%，左耳外緣貼近中央白板左框，頭頂與右側頭部直接被畫面上緣與右緣裁切，粗壯頸部與肩部局部落於右下角）。嚴禁縮小或右移前景小李的頭部與頸部，不可露出完整後腦勺，也不可讓小李與白板左框之間退開距離。
- 左側中景的 Amy（紅色定位人物）：嚴格維持圖 2 左側位置（水平約 8%–43%）與自然成人頭身比例——頭頂（含髮型）位於畫面高度約 18%，保留圖 2 清楚直立的頸部長度，肩線位於畫面高度約 60%，胸口與上臂中段以下按圖 2 由底邊裁切。嚴禁將 Amy 的頭部放大、縮短頸部或拉近鏡頭。

將紅色定位人物完整替換為圖 3 的 Amy，將藍色定位人物完整替換為圖 4 的小李；只呈現圖 2 可見的部位，不殘留白模、方塊頸部或色塊身體。人物圖只提供 3D 角色外觀與服裝（Amy 為棕色齊頸微捲短髮、灰色西裝外套與米白襯衫；小李為棕色上梳短髮與藍底彩色花襯衫，不加眼鏡），不採用其展示姿態。注意：不照搬圖 2 紅色白模朝左的鼻子方向；Amy 的整個上半身軀幹（雙肩連線、胸口、西裝翻領與襯衫領口）、頭部與視線，都必須同步朝畫面右側的小李轉向約 35 度（呈朝右的三分之二側面：畫面左側的右肩轉向前方靠近鏡頭、畫面右側的左肩轉向後方遠離鏡頭，胸口斜向畫面右側的小李），嚴禁肩膀與胸口正對鏡頭而只有轉頭。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左後方米白牆面的溫暖斜射日光、Amy 右後方（畫面中央偏下，水平約 36%–54%）的草綠色布面辦公椅與淺木桌角，以及右側白板局部。全畫面採近眼高、深景深（Deep Depth of Field），前景小李的髮絲與花襯衫領肩、中景 Amy 與後方白板便條都保持清晰，避免強烈散景將前景小李模糊化。

白板便條紙的外輪廓、位置、大小、透視與小李造成的遮擋完全依圖 2，只將圖 2 可見便條內的黑色示意橫線替換為圖 5 對應位置的圖文：
- 白板左上角綠紙（對應「100% 地球救星！」）：右大半部被前景小李的左上方頭側與頭髮遮擋，僅在白板左框內側露出左側約三分之一的綠色紙條與每行開頭字樣，不可為了露出完整「100% 地球救星！」而縮小或移開小李的頭。
- 白板中下左側淺藍紙（位於小李左耳下方、頸部左側）：完整露出，替換為「綠色神話：全球最環保企業，我們是地球唯一的選擇。」。
- 白板下方偏中綠紙（位於淺藍紙右下方）：右半部被小李的前景頸部與左肩遮擋，僅露出左半張紙與左側字樣（「天然之魂：…」前半段）。
- 白板右下黃紙（小李頸部右側、右肩上方）：僅依圖 2 露出一小條黃色上緣，不露出正文。
- 畫面最右緣中段與下段的兩張粉紅紙（小李頭部與右肩最右側）：僅依圖 2 在畫面右邊界露出極窄的粉紅色紙邊而已，不露出文字區塊。
其餘被小李遮住或位於畫外的內容維持不可見。圖 5 不提供整板構圖，不新增第二塊白板，也不把便條上的誇大文案改成正確宣傳文案。

畫面描述：
這是一張從小李身後越過肩膀看向 Amy 的 55mm 過肩中景，畫面只有兩人。右側近距離前景由小李大比例的左後腦、左耳、頸部與花襯衫肩部局部佔據，頭頂與右側按圖 2 裁切，遮擋住後方白板的大半面積；左側中景為 Amy，可見完整頭部、直立頸部、肩膀與上半身，下半身及雙手依圖 2 裁在畫外，兩人之間的背景露出草綠色辦公椅與淺木桌角。定格在 Amy 開始溫和回應小李的瞬間：她的整個上半身（雙肩、胸口與西裝翻領）、臉部與視線都朝向畫面右側的小李（約 35 度朝右斜側身，非正面胸口朝鏡頭），下巴極輕微下收，呈現開始輕點頭的狀態，嘴唇微啟準備說「沒錯」，神情溫和、理解對方但立場清楚，不是責備、怒視或燦笑。小李安靜聆聽，維持圖 2 的近距離前景位置與遮擋，不轉頭看鏡頭，也不補出正面表情。Amy 的手機仍低持在畫外下方，雙手與海報均不入鏡，不呈現鏡末收手機的動作。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、證書、檢驗報告、圖表、寶特瓶、毛毯、水印或額外疊字。
```

## 2026-10-19 rd_office 全景空鏡 GPT v1 — Amy 辦公區質感轉繪

- 專案／階段：course-51-esg／kj-cinematic／場景機位圖局部 W2I；以指定辦公區圖片提供材質與光影，既有研發室全景鎖定構圖。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未提供，費用未知；本次生成 1 張。
- 輸出：[cam_room_wide_level_empty_gpt.png](../references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt.png)；1672×941、RGB PNG、2044180 bytes。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-c09a5169-b477-4a56-a2d6-4f720e2673d0.png`；保留原檔並複製至場景 cameras/。
- 目視結果：保留無人物全景、工作島、兩張高腳椅、左牆白板、右側窗戶和磁磚地板，暖光、木紋、玻璃瓶與金屬細節較自然。
- 差異：窗外新增可辨識的建築景觀，百葉窗開合、白板紙張、時鐘、樣品瓶及部分植物細節有變化；未達逐物件／像素級完全一致。待使用者檢視，未追加生成。
- 驗證：已看圖與底圖對照、Pillow 完整解碼，來源與專案複本 SHA-256 一致：`ef55d86ff2e40939a98bc46ae659af246226ea44df38a2ba6ae2f782bc649221`。
- 原始 Blender 機位圖與 .blend 保留，未修改 asset_manifest.json／scene_plan.json。

有序參考圖：

1. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/Amy辦公區/Amy座位0.png`：外觀參考。
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_blender.png`：編輯底圖。

完整 Prompt：

```text
參考圖說明：
圖 1 Amy座位0.png：材質、光影與寫實渲染質感參考。只參考其自然辦公室質感，不沿用該圖的格局、家具數量或攝影角度。
圖 2 cam_room_wide_level_empty_blender.png：本次唯一編輯底圖，是研發室 16mm 無人物全景；決定全部構圖、幾何、物件位置、尺度、透視、可見範圍與遮擋關係。

生圖指引：
直接編輯圖 2，保持圖 2 的相機位置、16mm 廣角透視、畫幅邊界、消失點、房間比例及所有物件位置。把圖 2 渲染成與圖 1 相同的細膩、可信、具有自然生活痕跡的寫實辦公空間影像。這是同一研發室的材質與光影升級，不是重新設計房間。

將圖 1 的米白與淺灰室內基調、暖木紋、霧面金屬、柔和低飽和綠色點綴、細膩表面紋理、自然反射與柔和間接照明，應用在圖 2 對應的既有物件上。牆面呈細緻塗料，木製檯面和層架有真實木紋，金屬桌架與儀器呈細微粗糙度，樣品瓶有玻璃透明度與合理反射，既有紙張、文件、織物樣品與植物有自然細節。保留圖 2 的淺灰磁磚地板及原有格線，地面不要改成地毯。保留兩張高腳椅的形狀、位置和尺度，材質變得自然細膩，不替換為圖 1 的辦公椅。既有實驗器材必須維持原用途和外形，不換成一般辦公桌或 OA 隔間。

光線質感跟隨圖 1：右側既有百葉窗透入柔和暖日光，室內有自然冷暖平衡，柔順高光、清楚但不生硬的接觸陰影及真實環境遮蔽；不要過曝、泛白或重度霧化。維持圖 2 原有窗戶、天花板格柵燈、工作島頂部金屬架、後方工作檯與櫃體，光線方向符合圖 2 的右側窗戶。材質要達到圖 1 的精緻程度，不保留低細節預覽渲染的塑膠感。

保留左牆時鐘、掛畫、白板和滅火器；中央工作島、樣品瓶與檯面物件；後方儀器、櫃體、掛畫與便條板；兩張高腳椅；右側窗戶、百葉窗、暖氣片及植物。保留每件物品原有數量、位置及遮擋。不要將圖 1 的多排 OA 隔間、書櫃、額外文件堆、辦公椅或遠方城市景觀搬入圖 2。不要增加人物、人物白模、動物、文字標題或裝飾。

畫面描述：
從房間前端以近眼高的 16mm 廣角正面看向紡織材料研發室：中央偏右的完整工作島及兩張高腳椅落在中景，後方研發設備與工作檯形成景深，左側白板牆與右側整排窗戶同時可見，前景維持寬敞的空地與磁磚格線。畫面保持圖 2 的開闊取景與所有邊緣裁切；全室無人物，深景深，近處至後方的器材與材質都清楚。最終效果像圖 1 同一套作品中的自然寫實室內環境圖，只有表面、細節與光影品質更新，空間仍完全是圖 2 的研發室。

輸出：
一張 16:9 橫幅彩色完整圖片，最高可用解析度，畫面填滿，不要拼貼、比較圖、邊框、字幕、水印或額外疊字。
```


## 2026-10-19 rd_office 全景空鏡 GPT v2 — 紡織材料研發配置

- 專案／階段：course-51-esg／kj-cinematic／場景機位圖局部 W2I；依使用者最新要求，由原始 Blender 底圖控制相機、透視、空間位置與遮擋，允許細化窗框、邊緣和材質；參考圖僅提供色彩、光線、材質，不移植物件。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未提供，費用未知；本次生成 1 張。
- 輸出：[cam_room_wide_level_empty_gpt_v2.png](../references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v2.png)；1672×941、RGB PNG、1994878 bytes。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-eb37ba5e-489b-41ed-b27e-72eb1cf74844.png`；原檔保留。
- 目視結果：可見紗線筒、纖維／粒料樣品瓶、布料試片／色卡、拉伸試驗機、電子天平及小型測量儀器；無人物，主要工作島、兩張高腳椅、窗牆、前景走道與廣角取景維持，未移植 OA 隔間或參考圖家具，窗外未出現前版清楚的城市建築。
- 差異：左側白板向左擴大、尺寸與邊界未完全符合底圖；檢測設備、椅腳、窗框／百葉窗等細節亦有重繪差異，不能視為逐物件或像素級鎖定已通過。新增紡織樣品內容符合本次配置授權，待使用者檢視。
- 驗證：已看圖對照、Pillow 完整解碼並確認來源與複本 SHA-256 一致：`e06540cf14410f427f201389006514052f15578c197fbd52f5b0eb67c2ddfb53`。
- 路徑釐清：本次文字中的 `D:/Dropbox_AI動畫製作_ESG/...` 不存在；使用上一輪已檢視的同一張圖之實際路徑 `D:/Dropbox/_AI動畫製作_ESG/...`。
- 狀態：保留前版 GPT、原始 Blender 圖及模型，未改 manifest／scene_plan，未追加生成。

有序參考圖：

1. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/Amy辦公區/Amy座位0.png`：僅色彩／光線／材質風格。
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_blender.png`：相機／透視／位置／遮擋底圖。

完整 Prompt：

```text
參考圖說明：
圖 1 Amy座位0.png：只提供色彩、光線和材質風格，不移植其中的任何物件、家具、格局、窗外景物或攝影角度。
圖 2 cam_room_wide_level_empty_blender.png：唯一編輯底圖。底圖控制相機、透視、空間位置、遮擋關係；允許細化窗框、邊緣和物件材質。

生圖指引：
直接編輯圖 2，將其完成為一家紡織材料公司的研發室，配置紡織材料研發相關物件。以圖 2 的原始 Blender 預覽為基礎，不沿用先前生成版本。保持 16mm 全景相機、觀察方向、房間比例、消失點、工作島和家具尺寸、前後距離、原有遮擋以及完整畫幅。牆面、地板、天花板、窗戶、工作島、層架、櫃體、兩張高腳椅的位置與結構以圖 2 為準。不要拉近、裁切或重新設計空間。

把底圖既有檯面、層架及樣品展示區上的泛用示意物件，細化為符合紡織材料研發用途的內容；只在既有承載表面合理配置少量相關物件，不新增桌子、隔間或大型置物架：
1. 在既有層架上配置整齊、尺寸適中的紗線筒、纖維束、樣品瓶；透明樣品瓶內可見白色與半透明的再生聚酯粒料、少量短纖維，搭配低調的小型樣品編號標籤。
2. 在工作島原有捲材與樣品堆的位置，呈現小卷機能布、整齊摺疊的織物試片、布料色卡與樣品冊。布料應可辨識纖維和織紋、布邊與自然軟度，呈專業材料樣品，不要變成大量成衣或商品陳列。
3. 將左後方底圖既有高型檢測機器細化為材料拉伸試驗設備，可見上下夾具與被夾持的窄條織物試片；保持機器原有位置、外輪廓佔位和尺度。既有檯面小型器材可細化為精密電子天平、手持織物色差儀及簡單樣品托盤，比例合理且不擁擠。
4. 在底圖既有白板與後方樣品板的範圍內，呈現精簡的材料測試記錄、小型曲線圖和少量布料樣片，不新增看板，不放宣傳標語或巨幅文字。保留既有電腦螢幕於原位置，供資料記錄。
以上新增或細化的紡織物件必須受底圖家具透視、表面位置、尺度與遮擋限制；不遮住原有主要設備，不在前景走道或椅子下新增物件。

整體色彩、照明和材質質感參考圖 1：自然的暖白牆、淺灰和木色、低飽和色調，細膩木紋、霧面金屬、自然玻璃反射、柔和右側窗光與室內間接光，營造可信的寫實研發工作空間。保留圖 2 的磁磚地面，不換成參考圖的地毯；不移植參考圖的 OA 隔板、書櫃、辦公椅、文件山、盆栽或城市景觀。植物只保留底圖已有位置。窗框可增加合理的接縫、壓條和邊緣細節，但原有窗洞範圍、框架分區和百葉窗遮擋服從底圖，不額外展示參考圖的窗外建築。材料更精緻、光影更自然，不造成輪廓位移或空間重排。

畫面描述：
這是一張從房間前端以近眼高廣角看向紡織材料研發室的無人物全景。中央偏右的完整工作島及兩張高腳椅維持底圖佔位，左側檢測設備與白板、後方樣品層架與工作檯、右側整排窗戶均維持原來的位置和遮擋；前景保留空曠的磁磚走道。紗線、纖維、聚酯粒料、布料試片與測試器材讓空間清楚呈現材料研發用途，數量克制、擺放有序。全畫面深景深，材質與器材清楚，無人物、白模或動物。

輸出：
一張 16:9 橫幅彩色圖片，最高可用解析度，完整畫面，不加字幕、水印、邊框、比較圖或額外疊字。
```


## 2026-10-19 rd_office 全景空鏡 GPT v3 — 改用研發_1 色光材質參考

- 專案／階段：course-51-esg／kj-cinematic／場景機位圖局部 W2I；使用者指定原始 Blender 底圖控制相機、透視、空間位置與遮擋，允許細化窗框、邊緣及物件材質；新參考圖僅提供色彩、光線與材質，不移植物件。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未提供，費用未知；本次生成 1 張。
- 輸出：[cam_room_wide_level_empty_gpt_v3.png](../references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v3.png)；1672×941、RGB PNG、2049806 bytes。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-b13e1124-b148-4650-9b68-1a41b4fa46ff.png`；保留原檔。
- 目視結果：無人物、原有廣角房間方向與主要工作區保留；呈偏灰藍的金屬、冷色窗光與暖色反射，具有紗線筒、纖維／粒料樣品瓶、織物卷／試片、拉伸測試機及小型檢測器材。未帶入參考圖人物或長條吊燈。
- 差異：工作島在畫面中略放大，白板左移且尺度仍有差異；百葉窗開合與窗外城市景觀被重繪，並新增層架小盆栽等細節。相機／空間未達像素級一致，完整物件與遮擋鎖定未通過，待使用者檢視；未追加生成。
- 驗證：已看圖對照、Pillow 完整解碼，來源與專案複本 SHA-256 一致：`dc969d8045255413ab4a64cf14022fd9a8e033b2353b465144a2a9c2c52245fb`。
- 狀態：保留原始底圖、Blender 模型與前版 GPT；未修改 manifest／scene_plan，未自動採用。

有序參考圖：

1. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/研發區/研發_1.png`：只提供色彩、光線與材質風格；不使用人物或具體物件配置。
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_blender.png`：相機／透視／位置／遮擋底圖。

完整 Prompt：

```text
參考圖說明：
圖 1 研發_1.png：只提供色彩、光線與材質風格。採用其精緻 3D 動畫電影場景的材質質感、低飽和灰藍調、柔和冷暖光及細膩金屬／玻璃反射。不移植圖中的人物、家具、設備、吊燈、窗景或空間格局。
圖 2 cam_room_wide_level_empty_blender.png：唯一編輯底圖，控制相機、透視、空間位置及遮擋關係。允許細化窗框、邊緣與物件材質。

生圖指引：
直接編輯圖 2，完成一間紡織材料公司的研發室。整張畫面以圖 2 的相機與幾何為硬性基準：16mm 廣角正面全景、原始觀察高度、消失點、房間比例、地板格線、家具尺度、前後距離、物件遮擋及畫面四邊裁切均保持不變。不要改成圖 1 的人物近景、低景深或不同實驗室。

保留圖 2 牆面、天花格板與格柵燈、窗洞、工作島、金屬上架、後方層架、櫃體、兩張高腳椅、暖氣片和植物的原有位置與外輪廓。左牆白板四角與外框必須完全留在原位，維持原有小尺寸，不向左或向下擴大；左側檢測設備亦維持原有佔位。只能在原有表面和設備範圍內細化功能與材質。

在底圖既有檯面、層架及樣品展示區配置下列紡織材料研發物件，透視、比例及遮擋服從底圖，不擠占走道：
- 將既有樣品瓶及層架示意物細化為透明的再生聚酯粒料瓶、纖維樣本瓶和數個紗線筒，可見細小粒料、短纖維及紗線纏繞紋理，低調的小標籤。
- 原有布卷與樣品堆的位置放機能織物小卷、整齊摺疊的布料試片、樣品冊及少量色卡；呈現柔軟布邊和織紋，不放成衣、人體模特兒或大量商品。
- 在左後方底圖既有高型設備的原尺寸和位置內，細化為具夾具和窄條織物試片的拉伸測試機；不增加另一台大型設備。既有檯面小器材位置配置小型電子天平、便攜式色差儀與少量樣品托盤，保留工作空間。
- 在既有小白板和後方樣品板的原邊界內呈現少量布樣、材料測試記錄與簡單曲線，保留原有電腦螢幕位置。圖表是小型工作資料，不做大標題或廣告標語。
以上內容是依紡織研發用途設計的物件，不複製圖 1 中可見的機器或其他物件。

風格完全參考圖 1 的環境渲染質感：乾淨而有微細紋理的灰白牆、低飽和灰藍金屬、細緻玻璃、柔和淺木色與布料纖維，優雅柔順的邊緣與合理微倒角，具有可信的表面粗糙度。採柔和的中性室內頂光與右側窗口偏冷自然光，帶輕微暖色反射和精緻接觸陰影，呈細膩的高品質 3D 動畫場景，而非強烈金黃夕照、粗糙白模或塑膠玩具材質。保留底圖磁磚地板和原有格線；窗框可細化接縫、壓條、邊緣與反射，但窗框佔位、百葉窗遮擋及窗洞結構不改變。不把圖 1 的長條吊燈、背景電視／螢幕、其他設備或人物帶入。無人物、無白模、無動物。

畫面描述：
從研發室前端以底圖的近眼高 16mm 廣角看向內部，中央偏右完整工作島與兩張高腳椅維持原始佔位，左側小白板與檢測設備、後方工作檯和樣品層架、右側窗牆保持原空間與遮擋，前景是空曠的磁磚走道。紗線、纖維、聚酯粒料、布料試片及小型測試器材清楚呈現紡織材料研發用途，物件有序、數量克制。環境材質與灰藍冷暖光採圖 1 的細緻 3D 動畫風格，但保持全景深景深、物件清楚及圖 2 的完整相機構圖。

輸出：
一張 16:9 橫幅彩色完整圖片，最高可用解析度。不加字幕、水印、邊框、拼貼、比較圖或額外疊字。
```


## 2026-10-19 rd_office 全景空鏡 GPT v4 — 改用研發_2 色光材質參考

- 專案／階段：course-51-esg／kj-cinematic／場景機位圖局部 W2I；從原始 Blender 圖生成，依使用者要求保留底圖相機、透視、空間位置與遮擋，允許窗框、邊緣及材質細化；新參考圖只提供色彩、光線、材質，不移植其物件。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未提供，費用未知；本次生成 1 張。
- 輸出：[cam_room_wide_level_empty_gpt_v4.png](../references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v4.png)；1672×941、RGB PNG、1938297 bytes。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-85982578-f487-419e-a691-cde9f57a10c7.png`；保留原檔。
- 目視結果：整體為明亮米白與中性灰，無人物；維持主要工作區方向、兩張高腳椅與前景走道，配置紗線筒、粒料／纖維樣品瓶、布卷／試片／色卡、拉伸測試機與小型測量器材。窗外保持柔和亮景，未出現 v3 的清晰城市建築，未帶入參考圖人物或長條吊燈。
- 差異：左側白板尺寸與位置仍有偏差，工作島和椅子輪廓／尺度有重繪，布料垂過前桌緣，部分遮擋及櫃體細節未完全沿用底圖。紡織物件及色光已呈現，但空間與遮擋完全鎖定未通過，待使用者檢視。
- 驗證：已看圖對照、Pillow 完整解碼，來源與專案複本 SHA-256 一致：`88dc3fbba651ab92cda2f4c67757791355e5c1c19055920c2c12f64f9ae1d42d`。
- 路徑釐清：使用者文字中的 `D:/Dropbox_AI動畫製作_ESG/...` 不存在；已使用同名圖片實際位置 `D:/Dropbox/_AI動畫製作_ESG/...`，生成前已看圖。
- 狀態：保留原始 Blender 圖、模型與全部前版；未更新 manifest／scene_plan，未自動採用或追加生成。

有序參考圖：

1. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/研發區/研發_2.png`：僅色彩、光線與材質風格。
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_blender.png`：相機／透視／位置／遮擋底圖。

完整 Prompt：

```text
參考圖說明：
圖 1 研發_2.png：色彩、光線和材質風格參考。只使用其明亮米白、中性灰、少量低飽和冷色、柔和日光與精緻 3D 動畫場景的材質質感，不移植圖中的人物、家具、機器、窗景或格局。
圖 2 cam_room_wide_level_empty_blender.png：唯一編輯底圖，控制相機、透視、空間位置及遮擋關係，允許細化窗框、邊緣和物件材質。

生圖指引：
以圖 2 為編輯底圖，將這個空間渲染為一家紡織材料公司的研發室。保留底圖 16mm 廣角相機、拍攝方向、相機高度、消失點、全景範圍、房間比例和全部固定結構。不要重新構圖或移動攝影機。工作島、上下層架、桌腳、櫃體、兩張高腳椅、左側檢測設備、白板、時鐘、掛畫、右側窗牆、暖氣片、地板格線及天花板格柵燈的輪廓位置、尺寸、透視和遮擋均以圖 2 為準。特別保留左牆白板與工作島原本的外框位置及大小，不為了配置樣品而擴大或移動它們。

請在圖 2 既有工作檯、層架和設備的原有範圍內，配置並細化少量紡織材料研發相關物件：
- 將部分既有樣品瓶及小型示意物件細化為再生聚酯粒料樣品瓶、纖維樣本瓶、幾個小型紗線筒；物件尺寸適中、擺放有序。
- 在既有布卷及樣品堆的位置呈現機能布料小卷、摺疊織物試片、布料色卡及樣品冊，具有纖維織紋和自然布邊；不讓布料垂落遮住原本可見的桌緣、桌腳或櫃體。
- 左側既有高型設備在原有外輪廓及佔位內細化為材料拉伸試驗機，內有夾具和窄條織物試片；檯面既有小器材位置可呈現精密電子天平、手持色差儀和樣品托盤。不要新增大型機台。
- 既有白板與樣品板內放少量布料試片、測試記錄與小型曲線圖；所有內容都留在原板框內，原有螢幕位置保持不變。
新增或細化內容遵守底圖承載表面、尺度、透視及遮擋，不增加桌子、置物架、隔間、植物或走道物件，不複製圖 1 中的機器。

將圖 1 的色彩、光線和材質風格應用到這些既有結構與紡織物件：明亮柔和的米白與中性灰基調，少量低飽和冷色，柔順的自然光、高品質間接照明與不生硬的陰影，乾淨細緻的烤漆金屬、霧面檯面、微木紋、玻璃與布料纖維質感。具有圖 1 的精緻 3D 動畫環境質感與自然表面細節，沒有粗糙預覽圖的塑膠感，也不添加誇張高光或泛霧。照明方向符合圖 2 的右側窗戶，既有天花格柵燈保持原位，不換成圖 1 的吊燈。窗框可細化材質、壓條和邊緣，但窗洞分區及百葉窗可見範圍保持底圖原狀；窗外仍維持底圖柔和、不可辨識的亮景，不增加城市建築。保留底圖磁磚與格線，不換地板材質種類。

畫面描述：
一張無人物的紡織材料研發室完整全景，中央偏右的工作島及兩張高腳椅、左牆白板與檢測設備、後方工作檯和樣品層架、右側窗牆都保持圖 2 的原始位置與遮擋；前景空曠走道不放東西。工作區可見數量克制的紗線、纖維與粒料瓶、布料樣本和材料測試器材。整體呈圖 1 明亮、柔和、細膩的 3D 動畫材質風格，使用深景深，使全景與器材清楚。無人物、無白模、無動物，不移植圖 1 的物件與空間。

輸出：
一張 16:9 橫幅彩色完整圖片，最高可用解析度，不裁切。不加入字幕、水印、邊框、拼貼、比較圖或額外疊字。
```


## 2026-10-19 rd_office 全景空鏡 GPT v5 — 採購辦公室色光材質參考

- 專案／階段：course-51-esg／kj-cinematic／場景機位圖局部 W2I；使用者指定原始 Blender 底圖控制相機、透視、空間位置與遮擋，允許細化窗框、邊緣及材質；採購辦公室圖只提供色彩、光線和材質風格，不移植物件。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未提供，費用未知；本次生成 1 張。
- 輸出：[cam_room_wide_level_empty_gpt_v5.png](../references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v5.png)；1672×941、RGB PNG、1917016 bytes。
- 原始輸出：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-3e84f20d-a302-4ebf-8ec5-e0a2115e3f20.png`；保留原檔。
- 目視結果：低飽和藍灰、柔和冷色窗光與灰白霧面材質成立，無人物，主要工作島佔位、兩張高腳椅及前景走道大致沿用；有紗線筒、纖維／粒料瓶、布卷／試片、拉伸試驗機、電子天平與小型測量器材。未帶入參考圖的大辦公椅、筆電或計算機，未採用參考圖散焦。
- 差異：左牆白板仍向左擴大，窗臺新增資料夾與收納盒，窗外／百葉窗及部分機器、櫃體和椅腳細節有重繪；空間與遮擋完全鎖定未通過，待使用者檢視。
- 驗證：已看圖對照、Pillow 完整解碼，來源與專案複本 SHA-256 一致：`a88f8e3884785ae3c649f25b7c34f8402518aa52258fce5a48c8a8cda01578fc`。
- 狀態：保留原始 Blender 圖、模型與全部前版，未改 manifest／scene_plan，未自動採用或追加生成。

有序參考圖：

1. `D:/kj-openMontage/projects/course-51-esg/clp/loc_procurement_office.jpeg`：僅色彩、光線與材質風格。
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_blender.png`：相機／透視／位置／遮擋底圖。

完整 Prompt：

```text
參考圖說明：
圖 1 loc_procurement_office.jpeg：僅提供色彩、光線和材質風格。使用其低飽和藍灰調、柔和偏冷自然窗光、灰白霧面材質、細緻表面紋理與克制反射。不移植其中的任何物件、家具、窗景或格局，也不採用其近景構圖或背景散焦。
圖 2 cam_room_wide_level_empty_blender.png：唯一編輯底圖。底圖控制相機、透視、空間位置、遮擋關係，允許細化窗框、邊緣、物件材質。

生圖指引：
直接編輯圖 2，這是一家紡織材料公司的研發室，請配置相關的物件。保持圖 2 的 16mm 廣角相機、取景、消失點、房間比例、所有固定結構和家具位置，完整保留原圖畫幅。不要移動或放大工作島、層架、椅子、左牆白板、機器或窗戶。材質風格轉換不應導致輪廓位移；使用同一底圖逐物件細化，保持原來的遮擋。
左牆白板維持圖 2 原有四角及尺寸，不向左延伸或放大；工作島的桌面四角和桌腳保持原位。兩張高腳椅保持原形狀、位置和大小。牆面、天花板格柵燈、地板磁磚格線、窗洞、百葉窗遮擋、暖氣片、時鐘、畫框和植物均按底圖保留。

紡織研發物件配置在底圖既有檯面、樣品層架與設備的範圍內，將泛用示意物件細化為具體功能，不擴張佔位：
- 幾個小型紗線筒、透明纖維樣本瓶與再生聚酯粒料瓶，瓶內可見纖維或細小粒料。
- 原有卷材和樣品堆的位置放少量機能布卷、折疊布料試片、布料色卡及樣品冊；布料全部留在桌面，不垂下改變桌緣遮擋。
- 左側原有高型設備細化為有夾具和窄條織物試片的材料拉伸測試機，外輪廓與尺度保持底圖；原有檯面小器材位置細化為小型電子天平、便攜式色差儀和樣品托盤，不新增大型機台。
- 既有白板與樣品板的原框內呈現少量織物試片和材料測試記錄，保持原板框邊界與位置。原有電腦螢幕保持原位。
物件克制、有序，尺度符合底圖；不新增桌子、隔間、椅子、層架或植物，不佔用前景走道。

色彩、光線和材質依圖 1：整體低飽和藍灰、灰白與細微米灰，霧面檯面及細膩烤漆金屬、柔和玻璃反射、輕微木紋和可辨識的織物纖維；自然微倒角及表面粗糙度帶來高品質細緻 3D 渲染質感。照明為寬廣柔和的冷色日光，從圖 2 右側既有窗戶進入，柔順陰影和細緻間接光，維持足夠亮度；不採金黃夕陽、硬烈日斑、深暗藍濾鏡或誇張光暈。底圖窗框可細化壓條、接縫與邊緣，但保持原窗洞分區和百葉窗遮擋；窗外維持柔和亮景，不加入圖 1 的城市建築。保留圖 2 地板磁磚種類與格線。參考圖只提供色光材質，不移植其中的辦公椅、筆電、計算機、文件堆、窗戶或其他具體物件。

畫面描述：
無人物的紡織材料研發室全景，中央偏右工作島、兩張高腳椅、左側白板與檢測機、後方樣品層架與工作檯、右側窗牆及前景空地完全沿用圖 2 的構圖和空間關係。紗線、粒料、纖維與織物樣品及小型測試器材呈現材料研發用途。場景採圖 1 柔和藍灰色光與精緻霧面材質，但全畫面維持深景深與清晰，遠近設備均可辨識。無人物、無白模、無動物。

輸出：
一張 16:9 橫幅完整彩色圖片，最高可用解析度，不裁切、不加字幕、水印、邊框、拼貼、比較圖或額外疊字。
```


## 2026-10-20｜street 第 01 遠景機位 empty_gpt｜待使用者評鑑

- 專案／pipeline／階段：course-51-esg／kj-cinematic／assets 局部街景 W2I。使用者已授權只生成 1 張；使用正式目前版本 Blender 底圖，未使用舊 cam_street_wide_low_angle_empty_gpt.png。
- 工具／供應商：內建 image_gen／OpenAI；確切模型版本、預估與實際費用皆未提供，記為未知。此次共 1 次生成，未追加。
- 輸出：[cam_twoshot_wide_low_angle_empty_gpt.png](../references/scenes/street/cameras/cam_twoshot_wide_low_angle_empty_gpt.png)；原生 1672×941、RGB PNG，未裁切、拉伸或重編碼。
- 原生來源：C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-42391c5b-f0e4-4b30-9f47-e34c7e882a59.png，原檔保留。
- 目視比較：低角度廣角、兩側樓體透視、中央消失區與道路寬度大致沿用；主要門窗分區、雨棚及植物種植位置保留。玻璃環境反射與室內深度、石材細紋及枝葉層次改善，塑膠／簡模感降低，遠端中央樓仍偏簡化。目視未見人物、人物倒影或人形剪影。
- 仍有偏差：暖光與亮部強度高於原始參考，地面反光偏亮，乾燥霧面感不完全達標；局部門窗細格、室內燈具／陳設及枝葉輪廓重繪，植物豐滿度變動，不能視為像素級結構鎖定。天空新增少量雲。
- 驗證：已實際查看兩張輸入及生成結果；Pillow 完整解碼通過，複製保留原生尺寸。狀態為待評鑑，未更新 manifest 採用、未修改 Blender／相機、未生成其餘八機位；未宣告九圖共同美術標準。

有序輸入（按使用者指定順序，覆蓋通用配方排序）：
1. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_wide_low_angle_empty_blender.png：唯一編輯底圖，控制相機／透視／構圖／物件配置。
2. D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/Amy_George_走回公司_2K.png：只提供材質／色彩／光影／氣氛，不移植人物與配置。

完整 Prompt（原文）：

```text
請編輯圖 1，將這張 Blender 街景渲染提升為精緻動畫電影質感的空景背景，參考圖 2 的材質、色彩、光影與氣氛。

【輸入圖的分工】
圖 1 是唯一的相機、透視、構圖與物件配置依據。
圖 2 僅供美術表現參考，不採用它的拍攝構圖、建築排列、植物配置或人物。

【保留本鏡頭】
維持圖 1 的低角度廣角取景、兩側高樓透視、道路消失點、天空範圍與畫面裁切。
保留建築、門窗、窗框分格、雨棚、道路、花盆及樹木的主要位置、尺寸、數量與遮擋關係。
不重新構圖，不拉近或拉遠鏡頭，不擴展街道，不新增場景物件。

【材質與細節提升】
沿用圖 1 已有的建築構造與植物造型，改善表面材質、細微紋理、接縫、邊緣高光及細節明暗。
玻璃應具有符合場景的環境反射、適量透明感與室內深度，不呈現單一藍色平面。
金屬窗框與門把具有克制、細緻的高光。
石材和鋪面具有適當尺度的微小紋理及粗糙度變化；地面保持乾燥，不變成濕亮鏡面。
植物保留現有種植位置、種類、主要輪廓與大致體積，細化枝條、薄葉與花朵，呈現自然疏密、葉片朝向及透光。
不把植物改回球狀或塑膠塊狀，也不額外增加樹木、花盆或藤蔓。

【色彩與光影】
參考圖 2 的冷藍環境與局部暖陽，呈現自然的冷暖層次。
依圖 1 的場景朝向與既有投影維持合理的光源方向。
加強自然接觸陰影、細節投影與材質反射，同時保留陰影深度。
暖光集中在合理的受光面，不把全畫面染成橘黃色，不過度提高飽和度、銳利度或泛光。

【空景與後續用途】
成品不得出現任何人物，包括主角、路人、人物倒影或人形剪影。
這張圖將作為後續加入人物的背景母圖，近中景需保留足夠細節，不刻意加重背景散景；遠景可有輕微空氣透視。

【輸出】
只輸出一張 16:9 高解析度圖片，不製作九宮格，不添加文字或標誌。
```


## 2026-10-20｜street 02～09 empty_gpt｜以 01 為共用美術參考

- 使用者本輪明確選定 01 `cam_twoshot_wide_low_angle_empty_gpt.png` 作為其餘八張的美術參考，授權各生成 1 張；這是 kj-cinematic／assets 的既有專案局部製作。
- 工具／供應商：內建 image_gen／OpenAI；確切模型版本、預估／實際費用均未提供，記為未知。共 8 次生成，無額外修正版。
- 全八張原生 1672×941 RGB PNG；未裁切、拉伸、重編碼，原生工具檔保留。正式輸出皆保存 cameras，同名檔未存在，未覆蓋既有成果。
- 已逐張看兩圖輸入及生成結果，目視未見人物、人物倒影／剪影；Pillow 全部完整解碼，8/8 SHA-256 與工具原檔一致。
- 共通改善：冷藍玻璃／暖色石材美術接近 01，玻璃深度、金屬、石材及植物細節提升；各自機位方向與主要構圖大致沿用，非像素級鎖定。共通偏差：地面偏亮、局部細格與枝葉重繪，個別樹池增加花草。
- 01 的「本次共用美術參考」選擇已由本輪指示確認；02～09 新產出仍供評鑑，未更改 asset_manifest／scene_plan 採用，未修改 Blender／相機，未生成任何人物。
- 本輪完整提示詞由「以下共通正文」＋兩個換行＋`【本鏡畫面】`＋換行＋下列逐鏡專用段落組成，文字原樣送入工具。
- 每次有序輸入固定為：圖 1 = 下列本機位 `<camera>_empty_blender.png` 正式目前版本，圖 2 = `D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_wide_low_angle_empty_gpt.png`。未使用原 MJ 圖、舊 cam_street_wide_low_angle_empty_gpt 或前張新產出接力。

共通正文：
```text
請編輯圖 1，將本機位 Blender 空景轉成與圖 2 同一套精緻動畫電影美術的街景背景。

【輸入分工】
圖 1 是本次唯一的編輯底圖，唯一決定相機位置、鏡頭角度、焦距、透視、構圖、畫面裁切與物件配置。
圖 2 是已選定的第 01 機位 empty_gpt，只提供材質、色彩、光影與氣氛。不要採用圖 2 的廣角構圖、街道消失點、天空面積、物件排列或取景方向；不要重新生成圖 2。

【保留本機位】
完整沿用圖 1 的畫幅、建築輪廓、門窗分格、立柱、門把、玻璃雨棚、路面邊界與鋪面透視線。
保留本鏡可見植物與花盆的位置、數量、尺寸、主要輪廓及遮擋。不從圖 2 移植本鏡畫外的樹木、花盆、雨棚或建築。
不拉遠、不拉近、不旋轉相機、不鏡像、不拓寬道路、不補出畫外天空與街道；沒有天空的近景必須維持沒有天空。

【共用美術】
匹配圖 2 的冷藍玻璃環境色、米白細緻石材、局部金色陽光與冷暖層次，以及精緻動畫電影的材質表現。
依圖 1 的朝向和既有投影維持合理光源方向；同一街景換角度，不將圖 2 的陽光投影直接貼在本鏡。不要比圖 2 更暖、更飽和或更泛光。
玻璃呈現自然環境反射、適量透明感與克制的室內深度，不能只是平塗藍色；反射不得出現人形。
金屬窗框與門把有細緻克制高光，保留既有邊界與細格。石材與鋪面有適當尺度微紋理、接縫和粗糙度變化；路面乾燥，不變成濕亮鏡面。
植物沿用圖 1 的種類、位置和主要枝幹，細化薄葉、透光與花朵，不改成球狀塑膠塊，不增加樹木或花盆。
改善圖 1 過度模糊而看不清的材質與邊緣，使近中景具備可用細節，不額外強化背景散景；仍保持本鏡景別，不為展現更多細節而擴展畫面。

【空景與輸出】
零人物：不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。即使這是供過肩或人物特寫使用的背景，此次只交付空景。
不新增場景物件。只輸出一張 16:9 橫幅高解析度完整圖片，不製作九宮格、拼貼、對照圖，不加文字、標誌、水印。
```

### 02｜cam_twoshot_ms_level
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_ms_level_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_twoshot_ms_level_empty_gpt.png](../references/scenes/street/cameras/cam_twoshot_ms_level_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-e788eb3e-ec30-4d1e-aa09-329e08e19917.png`。
- 本鏡畫面（原文）：本鏡為 02 平視雙人中景的空景：右側石材立面、玻璃門、成列方盆和樹木，左側玻璃大樓與樹木；街道向中間遠方延伸。保持圖 1 大面積前景鋪面與右前方方盆的大小和位置，上緣裁切沿用底圖，不改成 01 仰角廣角。
- 目視比較：平視街道、前景地面、右側雨棚與方盆位置大致保留；玻璃深度與樹葉改善。鋪面分格與枝葉輪廓重繪，地面反光偏亮，遠端樓體增加窗格。

### 03｜cam_twoshot_mws_profile
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_mws_profile_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_twoshot_mws_profile_empty_gpt.png](../references/scenes/street/cameras/cam_twoshot_mws_profile_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-d0076e55-b9d6-4972-ac0b-9919b76fd0dd.png`。
- 本鏡畫面（原文）：本鏡為 03 側面雙人全身機位的空景：畫面主要是側向近距離觀看的石材立柱、兩組高玻璃門、左邊緣裁切的樹木方盆與下方鋪面。保留每個柱、門框、門把位置和斜向透視；不要加入天空、整條街道或遠景大樓。
- 目視比較：側向立面、兩組玻璃門、柱位與左邊緣方盆大致保留；金屬與石材細節提升。門把、窗格及鋪面分格有差異，玻璃內新增燈光／植物反射，地面較亮。

### 04｜cam_george_ots_amy
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_george_ots_amy_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_george_ots_amy_empty_gpt.png](../references/scenes/street/cameras/cam_george_ots_amy_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-77364171-5f0c-4b93-b445-616f6ab68aab.png`。
- 本鏡畫面（原文）：本鏡為 04 過肩機位的空景：緊裁切玻璃門與米白立柱，左側及右側有石材柱，中央大片藍玻璃，左中偏下有長門把。保持底圖柱寬、門把座標、垂直門框及滿版立面裁切，不補天空、地面或街道全景。
- 目視比較：緊裁切立面、兩側柱位及左中門把大致保持，沒有改成廣角街景；玻璃增加大量街景與植物反射、室內燈光，門框細節與門把厚度有變。

### 05｜cam_amy_ots_george
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_amy_ots_george_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_amy_ots_george_empty_gpt.png](../references/scenes/street/cameras/cam_amy_ots_george_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-1218d588-5b10-4c57-acaa-53edb6a6c8bb.png`。
- 本鏡畫面（原文）：本鏡為 05 反向過肩機位的空景：深藍玻璃幕牆與細窗框網格，下半部為鋪面，右側邊緣有被裁切的樹幹與低方形樹池。保持樹池輪廓、右邊緣裁切、橫窗框高度及地面範圍；不改成另一側的米白立柱玻璃門，不加天空。
- 目視比較：反向幕牆、橫窗框高度、右側樹池與地面占比大致保留；樹池增加白色小花與低矮花草，局部窗格和鋪面分格重繪，暖光比底圖強。

### 06｜cam_george_mcu_45deg
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_george_mcu_45deg_empty_gpt.png](../references/scenes/street/cameras/cam_george_mcu_45deg_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-2df99098-4990-4607-b9a0-3340a8626ecb.png`。
- 本鏡畫面（原文）：本鏡為 06 中近景機位的空景：向左後方延伸的米白立柱玻璃門立面、成列白色方盆和樹木，右前景是被畫框裁切的大玻璃門，近中景方盆位於畫面中央偏左。精確保留方盆大小、位置、立柱間距、門把與斜向透視，不放寬取景。
- 目視比較：沿街立柱、方盆列及右前玻璃門構圖大致保留，枝葉與石材較清晰；右側門把尺寸／位置有變，遠側雨棚及玻璃內細節被補繪，地面偏亮。

### 07｜cam_amy_mcu_45deg
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_amy_mcu_45deg_empty_gpt.png](../references/scenes/street/cameras/cam_amy_mcu_45deg_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-50786447-57a5-4408-b919-483a942fa4f6.png`。
- 本鏡畫面（原文）：本鏡為 07 反向中近景機位的空景：藍黑玻璃幕牆、水平與垂直細窗框，偏右有樹幹和低方形樹池，前景是大面積冷色陰影及鋪面。保持幕牆斜向透視、樹池位置和大小、上邊緣枝葉裁切，不改成對面米白門廊。
- 目視比較：反向幕牆、偏右樹幹／樹池與前景地面大致保持，未改成對面門廊；樹池增添低矮花草，窗框細格和地面接縫重繪，暖陽範圍增大。

### 08｜cam_george_cu_emotion
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_george_cu_emotion_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_george_cu_emotion_empty_gpt.png](../references/scenes/street/cameras/cam_george_cu_emotion_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-81bbce4d-454c-42e1-b71d-c24e36c62b8a.png`。
- 本鏡畫面（原文）：本鏡為 08 特寫機位的空景：近距離滿版米白立柱與深藍玻璃門，左中和右中兩根寬柱，中央及右邊緣可見長門把。嚴格保持柱的橫向位置與寬度、門把高度、底圖輕微斜向透視和緊裁切；不新增花盆、天空、街道或雨棚。
- 目視比較：近距離米白柱與玻璃門緊裁切大致保留；窗框／柱位有小幅差異，門把更粗更突出，玻璃反射與室內細節增加。

### 09｜cam_amy_cu_emotion
- 圖 1：`D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/street/cameras/cam_amy_cu_emotion_empty_blender.png`；圖 2 如上，順序不變。
- 輸出（首版，待評鑑）：[cam_amy_cu_emotion_empty_gpt.png](../references/scenes/street/cameras/cam_amy_cu_emotion_empty_gpt.png)
- 原生來源：`C:/Users/user/.codex/generated_images/01a154e8-b7f3-7693-b161-c97d1eb0e184/exec-cdac99e1-463b-4f44-9bf4-f07e68773c92.png`。
- 本鏡畫面（原文）：本鏡為 09 反向特寫機位的空景：深藍玻璃幕牆與細窗框，中央有樹幹、低矮方形樹池，上邊緣裁切枝葉，底部為冷色陰影的鋪面。保持樹幹和樹池的中心位置、上緣枝葉裁切、窗框線條與地面占比，不改成對面米白石材門廊。
- 目視比較：反向幕牆、中央樹幹／樹池與地面占比大致保持；樹池增加低矮花草，枝葉密度提高，窗框分格與水平構件厚度有變。

## 2026-10-20 rd_office — 使用 GPT v3 外觀轉繪新版 Blender 側面／全景

- 專案／階段：course-51-esg／kj-cinematic／場景機位圖局部 W2I。使用者指定 GPT v3 為新外觀參考，兩張 .tmp Blender 檢查圖為編輯底圖；沿用原模型與機位，不製作影片。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、預估與實際費用未提供，已事先告知未知。共 3 次生成：側面 1 次、全景首版及構圖修正版各 1 次；transparent_background=false。
- 驗證：三張皆已目視比較、Pillow 完整解碼，均為 1672×941 RGB PNG，原生來源與專案複本 SHA-256 一致。
- 交付：側面 v1 與全景 v2；全景 v1 保留為偏差版本。原始參考、兩張 Blender 底圖、模型、manifest／scene_plan 均未修改；生成成功不代表已確認採用，也未達逐物件完全一致。

### 側面 v1
- 輸出：[cam_room_side_empty_v3style_gpt_v1.png](../references/scenes/rd_office/cameras/cam_room_side_empty_v3style_gpt_v1.png)；2190902 bytes。
- 原生來源：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-6fc304e9-ff40-4d43-9197-a69d3b8f49ec.png`。
- SHA-256：`b1b2c4e26413c6dde10f8861ece43e1a9080ae9d46665a597c0bad6c40a01296`。
- 有序輸入：圖 1 `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v3.png`（外觀）；圖 2 `D:/kj-openMontage/.tmp/rd_office_match_v3_20261019/cam_room_side_empty_v3_check.png`（編輯底圖）。
- 目視：保留右前側斜看工作島的機位、桌架主要位置與右下椅子裁切；織紋、玻璃內容物與金屬細節改善，無人物。白板增加小紙張、上下層架增添植物／樣品，培養皿由 2 個變為 3 個；物件數量與配置完全鎖定未通過，待使用者檢視。
- 完整 Prompt：

```text
參考圖說明：
圖 1 cam_room_wide_level_empty_gpt_v3.png：同一研發室的色彩、光線、材質與物件外觀參考；不是本張的機位。
圖 2 cam_room_side_empty_v3_check.png：唯一編輯底圖，鎖定側面機位、透視、位置、數量及遮擋。

生圖指引：
以圖 2 為唯一編輯底圖，直接提升這張 Blender 預覽的材質、表面細節和照明，成為與圖 1 同一套紡織材料公司研發室的精緻 3D 動畫場景。保持圖 2 相機、消失點、取景、家具尺度、地板格線、物件位置、數量與遮擋。圖 1 只供外觀與光線，不能把圖 1 的拍攝角度或物件擺法移植過來。房間、工作島、上下層架、金屬支架、桌櫃、椅子、左牆白板、窗框、天花格板和燈具均沿用圖 2 邊界。

將圖 2 已有的樣品瓶細化為含聚酯粒料／纖維的透明玻璃瓶；紗線筒呈現細密纏繞，保留原有米白、灰藍、深藍及少量棕色的配色位置。沿用既有摺疊布樣、樣品冊、檢測儀器、顯微鏡、電腦與植物，不增加一批新道具。中央一支米白布卷與桌緣兩片相鄰垂布保持圖 2 的位置和輪廓，以細緻織紋、纖維邊緣及柔軟厚度表現；旁邊兩個培養皿保持在布料外側。左牆白板維持四片布樣的 2×2 排列與右側測試曲線，框體大小與四角不變，不複製圖 1 更多紙張與樣品。螢幕維持圖 2 的織物檢測和曲線內容。

材質、灰藍色調、柔和中性頂光、側窗偏冷日光與輕微暖色反射採圖 1；呈現細膩木紋、灰白牆面、金屬微反射、透明玻璃及可信的接觸陰影。允許細化原有窗框接縫、邊緣微倒角和表面紋理，但不改變格局及遮擋。保持全景清楚、柔和自然的高品質 3D 動畫渲染。無人物、無人形白模、無動物、無新增裝飾，不把整個畫面改成新設計的研發室。

畫面描述：
從研發室右前側朝左後方斜看工作島，嚴格保留圖 2 的側面構圖與畫面四邊裁切。右側近景的電腦主機、螢幕、顯微鏡、桌緣垂布，以及右下只露出局部的椅子，維持原始尺度與裁切；工作島上下架向左後方延伸，左牆白板與時鐘仍在原位置。後方設備被層架遮住的部分保持遮住，不為了展示而挪開物件。不可改成圖 1 的正面全景，不放大白板，不移動層架立柱。

輸出：
一張 16:9 橫幅彩色完整圖片，最高可用解析度。單一畫面，無拼貼、比較圖、字幕、水印、外框或額外疊字。
```

### 全景 v1 — 構圖偏差版本
- 輸出：[cam_room_wide_level_empty_v3style_gpt_v1.png](../references/scenes/rd_office/cameras/cam_room_wide_level_empty_v3style_gpt_v1.png)；2025863 bytes。
- 原生來源：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-10dedfad-9b10-4518-a16b-4462e72adfa9.png`。
- SHA-256：`90729b74e59c731d148d771a246fc5c757169c48fd59ffa13413cebaa1e76d06`。
- 有序輸入：圖 1 `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v3.png`（外觀）；圖 2 `D:/kj-openMontage/.tmp/rd_office_match_v3_20261019/cam_room_wide_level_empty_v3_check.png`（編輯底圖）。
- 目視：大幅沿用圖 1 的白板、工作島及桌面配置，未遵從新版 Blender 底圖；構圖／配置未通過。已明確告知後補一次修正，保留此版本。
- 完整 Prompt：

```text
參考圖說明：
圖 1 cam_room_wide_level_empty_gpt_v3.png：同一研發室的色彩、光線、材質與物件外觀參考。
圖 2 cam_room_wide_level_empty_v3_check.png：唯一編輯底圖，鎖定新版 Blender 全景機位、透視、位置、數量及遮擋。

生圖指引：
以圖 2 為唯一編輯底圖，直接提升這張 Blender 預覽的材質、表面細節和照明，成為與圖 1 同一套紡織材料公司研發室的精緻 3D 動畫場景。保持圖 2 相機、消失點、取景、家具尺度、地板格線、物件位置、數量與遮擋。圖 1 只供外觀與光線，不能把圖 1 的拍攝角度或物件擺法移植過來。房間、工作島、上下層架、金屬支架、桌櫃、椅子、左牆白板、窗框、天花格板和燈具均沿用圖 2 邊界。

將圖 2 已有的樣品瓶細化為含聚酯粒料／纖維的透明玻璃瓶；紗線筒呈現細密纏繞，保留原有米白、灰藍、深藍及少量棕色的配色位置。沿用既有摺疊布樣、樣品冊、檢測儀器、顯微鏡、電腦與植物，不增加一批新道具。中央一支米白布卷與桌緣兩片相鄰垂布保持圖 2 的位置和輪廓，以細緻織紋、纖維邊緣及柔軟厚度表現；旁邊兩個培養皿保持在布料外側。左牆白板維持四片布樣的 2×2 排列與右側測試曲線，框體大小與四角不變，不複製圖 1 更多紙張與樣品。螢幕維持圖 2 的織物檢測和曲線內容。

材質、灰藍色調、柔和中性頂光、側窗偏冷日光與輕微暖色反射採圖 1；呈現細膩木紋、灰白牆面、金屬微反射、透明玻璃及可信的接觸陰影。允許細化原有窗框接縫、邊緣微倒角和表面紋理，但不改變格局及遮擋。保持全景清楚、柔和自然的高品質 3D 動畫渲染。無人物、無人形白模、無動物、無新增裝飾，不把整個畫面改成新設計的研發室。

畫面描述：
從研發室前端以近眼高 16mm 廣角看向內部，嚴格保留圖 2 正面全景的尺度、四邊裁切與空曠前景地板比例。完整工作島、兩張黃色高腳椅、左側白板與拉伸測試機、後方工作檯與層架、右側百葉窗與暖氣片皆保持圖 2 的原位置。桌面中央的米白布卷、兩片垂布、右側顯微鏡和電腦遵從新版底圖；不以圖 1 中較大的工作島、更多布卷或移位的白板取代它們。保持圖 2 的窗洞、窗框及百葉窗遮擋。

輸出：
一張 16:9 橫幅彩色完整圖片，最高可用解析度。單一畫面，無拼貼、比較圖、字幕、水印、外框或額外疊字。
```

### 全景 v2 — 構圖修正版
- 輸出：[cam_room_wide_level_empty_v3style_gpt_v2.png](../references/scenes/rd_office/cameras/cam_room_wide_level_empty_v3style_gpt_v2.png)；1980710 bytes。
- 原生來源：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-36b95104-ece4-42c3-82b4-adf25f58e377.png`。
- SHA-256：`b823d7ee53b19d914bd4fd9425c7e1456a05bb1f6270ebb64c5f8a6008ab661b`。
- 有序輸入：圖 1 `D:/kj-openMontage/.tmp/rd_office_match_v3_20261019/cam_room_wide_level_empty_v3_check.png`（唯一編輯底圖）；圖 2 `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v3.png`（只供外觀）。
- 圖序調整原因：首版過度複製第一張外觀參考，修正時將實際編輯圖放在首位，並同步改寫圖號／角色，優先落實使用者要求的底圖空間控制。
- 目視：恢復新版底圖的工作島尺度、前景地板比例、小白板位置與 2×2 布樣、單支米白布卷及相鄰兩片垂布；無人物。窗外城市景觀、百葉透光與部分表面細節重繪，非像素級鎖定。交付此版供檢視，未再生成。
- 完整 Prompt：

```text
參考圖說明：
圖 1 cam_room_wide_level_empty_v3_check.png：唯一編輯目標，是已更新物件的 Blender 全景。這次務必直接處理圖 1。
圖 2 cam_room_wide_level_empty_gpt_v3.png：只供材質、色彩和光線參考，不供構圖，不是輸出底圖。

生圖指引：
Edit IMAGE 1 in place. Transfer ONLY the rendering quality, surface textures and lighting character of IMAGE 2 onto IMAGE 1. The output must retain the complete camera composition and object arrangement of IMAGE 1. Do not reproduce IMAGE 2.

將圖 1 的紡織材料公司研發室渲染成圖 2 同樣的精緻 3D 動畫場景，保持圖 1 的所有房間輪廓、家具佔位、物件位置、透視、遮擋和四邊裁切。以細密織紋、透明玻璃內的纖維粒料、金屬與木材表面細節提升現有物件。灰白牆、灰藍金屬、低飽和織物、柔和中性頂光與側窗冷暖光採圖 2 的質感。

以下是必須保留的新版圖 1 內容：左牆較小的白板位於原位置，上方標題 MATERIAL R&D，左半只有四片布樣排成 2×2，右半是測試曲線；桌面中央只有一支米白布卷，桌緣並排一片米白、一片灰藍垂布；兩個小培養皿位於垂布右側；右側顯微鏡、螢幕與電腦主機不移動；層架上既有瓶罐、紗線筒、資料夾與植物保持原來的數量、位置和大小。不要加入圖 2 的更多布卷、額外植物、紙張或儀器，不要放大工作島、白板或椅子。保留圖 1 的較多前景地板和原有百葉窗遮擋。可細化邊緣與材質，但不重新設計物件或房間。

畫面描述：
完全使用圖 1 的近眼高正面廣角全景，完整工作島與兩張黃色高腳椅在原位置，左側白板和檢測機、右側窗牆和暖氣片保持原始空間關係。全景清楚，無人物、無人形白模、無動物。此圖與另一個側面機位共用相同的物件配置。

輸出：
一張與圖 1 相同取景的 16:9 橫幅彩色圖片，最高可用解析度。無字幕、水印、比較圖、拼貼或外框。
```



## 2026-10-20 — 研發室 64 組道具新版底圖，GPT v3 外觀轉繪

- 專案／階段：course-51-esg／kj-cinematic／assets，既有完整 Blender 預覽 I2I style-transfer；使用者指定兩張 cameras 底圖與 GPT v3 外觀參考。
- 工具：內建 `image_gen.imagegen`，2 次獨立編輯；模型及費用未由工具揭露，均未知。未使用 CLI／外部供應商，未追加生成。
- 交付：同目錄新檔，兩張皆 1672×941 RGB PNG；原始底圖、GPT v3、Blender、manifest／scene_plan 保留。已逐張目視、完整解碼及核對來源與交付檔 SHA-256。
- 目視：保留正面／側面機位、主要桌架配置、六個布卷及兩片垂布；側面右前景電腦主機遮擋與椅背裁切保留。玻璃、纖維、紗線及布料表面細化，無人物。全景窗外透光／模糊窗景與細字等有重繪，並非逐像素鎖定，未宣告 AI 轉繪逐件完全一致；待使用者檢視，未自動替換核准素材。

### 正面全景 v1
- 輸出：[wide_check_gpt_v1.png](../references/scenes/rd_office/cameras/wide_check_gpt_v1.png)；1988028 bytes。
- 原生來源：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-d64aedd1-55cc-4416-8436-58ca1a1acb7a.png`。
- SHA-256：`ac774f179f8a89050e6f2899515e67aa62eb39e511e70d2a99149cfa7c665fe0`。
- 有序輸入：圖 1 `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/wide_check.png`（唯一編輯底圖）；圖 2 `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v3.png`（僅材質、色彩與光線）。
- 完整 Prompt：

```text
Use case: style-transfer / I2I material and lighting refinement.
圖 1 是唯一編輯底圖；圖 2 cam_room_wide_level_empty_gpt_v3.png 只提供材質、色彩、光線及精緻寫實 3D 動畫場景風格。
Edit IMAGE 1 in place. Preserve IMAGE 1's exact camera, framing, perspective, silhouettes, room geometry, object inventory, positions, scale and occlusion. Transfer only rendering quality and surface appearance from IMAGE 2. Do not reproduce IMAGE 2's camera or rearrange the scene.

這是紡織材料公司的研發室。僅把圖 1 的材質與光影細化為圖 2 的質感：灰白牆面、淡木色檯面、灰藍金屬支架、透明玻璃罐及清楚可見的白色纖維／聚酯粒料／深藍樣品、細密紗線纏繞與布料織紋、柔和中性頂光與右側窗光、自然接觸陰影和細膩反射。物件表面允許微倒角與纖維細節，物件外輪廓、大小、擺放與透視保持圖 1。各物件保留圖 1 原有顏色，不能任意改變罐內樣品或線筒的配色位置。

圖 1 是已逐件建好的固定 3D 場景，不能新增、刪除、複製或搬移道具。保留上層架 8 個樣品罐、5 個線筒、原有兩組摺布與植物；下層架的 5 個樣品罐、5 個線筒、資料夾、樣品冊依圖 1 保持數量與遮擋，畫外或被遮住的物件不必強行顯露。桌上的三組儀器、兩個小樣品罐與較高樣品罐、手持色差儀、兩支白色瓶、紙張與布樣、筆筒、顯微鏡、單一螢幕、鍵盤、滑鼠與電腦主機，全按圖 1 位置。桌面中央恰好 6 個布卷：左右各一個米色布卷、左側上下疊兩個深藍布卷、中間上下疊兩個橫向淺色布卷；保留原來朝向及接觸關係。桌緣恰好兩片相鄰的米色與灰藍垂布，維持圖 1 長度、寬度、位置和重疊。左牆白板保留 2×2 四片布樣與右側曲線，不能抄入圖 2 更多紙張或布樣。保留圖 1 螢幕的織物與曲線分區。天花、窗洞、百葉、地板格線、檯架、抽屜、椅子、後方設備均不改造，維持原有遮擋。

輸出一張 16:9 橫幅完整彩色圖片，最高可用解析度。高品質自然寫實 3D 場景渲染，無人物、無動物、無額外道具、無外框、無拼貼、無水印或額外疊字。
本張構圖：嚴格使用圖 1 wide_check.png 的正面廣角全景。保留完整工作島、兩張黃色高腳椅、原本較多的前景地板、左側白板和檢測機、右窗牆與暖氣片。保持圖 1 原始邊界、視點與畫面比例，不放大工作島，不放大白板，不裁掉前景，不改變百葉遮擋來加入新的窗景。
```

### 側面斜角 v1
- 輸出：[side_check_gpt_v1.png](../references/scenes/rd_office/cameras/side_check_gpt_v1.png)；2042408 bytes。
- 原生來源：`C:/Users/servi/.codex/generated_images/01a154ba-8224-70a1-a116-dd986cb418ec/exec-3eaa61f2-74a7-4265-bab1-04ae409fd38a.png`。
- SHA-256：`99c3a3df50129cb6d889abd2d26d671a0e3877a356f1347bc5c5bc1c6f36a734`。
- 有序輸入：圖 1 `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/side_check.png`（唯一編輯底圖）；圖 2 `D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_room_wide_level_empty_gpt_v3.png`（僅材質、色彩與光線）。
- 完整 Prompt：

```text
Use case: style-transfer / I2I material and lighting refinement.
圖 1 是唯一編輯底圖；圖 2 cam_room_wide_level_empty_gpt_v3.png 只提供材質、色彩、光線及精緻寫實 3D 動畫場景風格。
Edit IMAGE 1 in place. Preserve IMAGE 1's exact camera, framing, perspective, silhouettes, room geometry, object inventory, positions, scale and occlusion. Transfer only rendering quality and surface appearance from IMAGE 2. Do not reproduce IMAGE 2's camera or rearrange the scene.

這是紡織材料公司的研發室。僅把圖 1 的材質與光影細化為圖 2 的質感：灰白牆面、淡木色檯面、灰藍金屬支架、透明玻璃罐及清楚可見的白色纖維／聚酯粒料／深藍樣品、細密紗線纏繞與布料織紋、柔和中性頂光與右側窗光、自然接觸陰影和細膩反射。物件表面允許微倒角與纖維細節，物件外輪廓、大小、擺放與透視保持圖 1。各物件保留圖 1 原有顏色，不能任意改變罐內樣品或線筒的配色位置。

圖 1 是已逐件建好的固定 3D 場景，不能新增、刪除、複製或搬移道具。保留上層架 8 個樣品罐、5 個線筒、原有兩組摺布與植物；下層架的 5 個樣品罐、5 個線筒、資料夾、樣品冊依圖 1 保持數量與遮擋，畫外或被遮住的物件不必強行顯露。桌上的三組儀器、兩個小樣品罐與較高樣品罐、手持色差儀、兩支白色瓶、紙張與布樣、筆筒、顯微鏡、單一螢幕、鍵盤、滑鼠與電腦主機，全按圖 1 位置。桌面中央恰好 6 個布卷：左右各一個米色布卷、左側上下疊兩個深藍布卷、中間上下疊兩個橫向淺色布卷；保留原來朝向及接觸關係。桌緣恰好兩片相鄰的米色與灰藍垂布，維持圖 1 長度、寬度、位置和重疊。左牆白板保留 2×2 四片布樣與右側曲線，不能抄入圖 2 更多紙張或布樣。保留圖 1 螢幕的織物與曲線分區。天花、窗洞、百葉、地板格線、檯架、抽屜、椅子、後方設備均不改造，維持原有遮擋。

輸出一張 16:9 橫幅完整彩色圖片，最高可用解析度。高品質自然寫實 3D 場景渲染，無人物、無動物、無額外道具、無外框、無拼貼、無水印或額外疊字。
本張構圖：嚴格使用圖 1 side_check.png 的側面斜角近景。右前景的大型電腦主機與螢幕遮擋、由近右向遠左延伸的工作檯與兩層架、左後方白板和高腳椅、畫面下緣被裁切的前景黃色椅背、上緣被裁切的金屬架，都必須維持圖 1 原樣。右側窗口大部分在畫外，不能移入畫面；不能變成圖 2 的正面全景、移遠相機或為了看見物品而挪開主機。
```


## 2026-10-20 factory 第一機位全景重繪 v2，待使用者確認

- 專案／階段：course-51-esg／kj-cinematic／assets 空景局部重繪，依 skills/kj/blender-view-restyle.md；本次僅一張。
- 工具：OpenAI 內建 image_gen 圖片編輯；實際模型版本、預估及實際費用未知；共 1 次生成。
- 圖 1／唯一底圖：D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_twoshot_wide_level_empty_blender.png（已確認 v7，1920×1080）。
- 圖 2／原始材質光影參考：D:/kj-openMontage/.tmp/factory_review/廠務部_空景圖2.png；原模型內嵌來源 D:/20260929/scene_4.5v2/廠務部_空景圖2.png，來源對照 .tmp/factory_reference_sources.json。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-f3490552-eab0-4678-9c01-b6e72b318f49.png。
- 專案副本：references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png；舊 empty_gpt.png 保留。
- 驗證：1672×941 RGB PNG，接近但非精確 16:9；Pillow 完整解碼與原生／副本 SHA256 一致。未裁切、縮放或拉伸。
- 目視：保留正面機位、雙紙堆／四束帶、棧板、左上直管與布束、平放水管捆、工具牆及右側鏤空箱；暖陽、紙纖維、木紋與地坪質感提升，無人物。AI 新增層架立柱孔洞，紙板邊緣／束帶與工具細節有重繪，牆面與地面日照明顯加強；不宣稱幾何逐像素一致。
- 狀態：首張待確認是否作為後續共用美術參考；其他九機位未生成，未更新 manifest／scene_plan，未修改模型、原機位及正式 Blender 底圖。專案目前未找到 checkpoint 檔，本次局部進度保存於本紀錄及交接文件。

### 完整實際提示詞（附件順序：圖 1 → 圖 2）

```text
請編輯圖 1，將這張 Blender 空景提升為高品質電影動畫用的自然細膩 3D 工廠場景，參考圖 2 的材質、色彩、光影與氣氛。
圖 1 cam_twoshot_wide_level_empty_blender.png（factory v7）是唯一的取景、透視、物件配置與遮擋依據。
圖 2 廠務部_空景圖2.png 僅供美術表現參考，不移植其構圖、建築／家具排列、植物配置或人物。不要重新生成圖 2。
色彩與光影採用圖 2 的柔暖日光、米白磚牆、溫暖褐色紙材與木材、灰色金屬、低飽和青綠／藍色工業配件，暖光與稍冷陰影自然平衡。提高圖 1 偏暗部位的可讀性，保持柔和接觸陰影，不加濃黃濾鏡或過曝泛光。

【保留本機位】
維持圖 1 的 16:9 畫幅、正面觀看方向、透視、構圖、邊界裁切、主要結構與遮擋。
兩堆大型瓦楞紙板、各自兩條垂直束帶、下方木棧板的高度、寬度、間距與輪廓完全依圖 1。兩紙堆佔據前景的比例不可縮小，不能把相機拉遠成整間工廠。
維持後方金屬層架、中央小抽屜與儀表、右後工具洞洞板與工具、右前景紙箱及灰色／黃色鏤空塑膠箱的原有配置、數量、尺度與遮擋。
尤其保留左上角被畫框裁切的圓形中空直管堆，管軸彼此平行，堆疊下寬上窄；保留旁邊淺綠綁束布料、中上層水平平放的黑色厚水管捆、各色壺罐與裝零件的木盒。不要將它們替換成整齊收納箱。
不旋轉相機、不鏡像、不拉遠或拉近；不補出畫框外的物品，不新增窗戶、捲門、吊燈、植物、垃圾桶或地面標線。

【材質與細節提升】
沿用圖 1 的構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。
紙板呈現圖 2 的自然厚度、細密瓦楞斷面、乾燥纖維與不規則邊緣；兩堆層次清楚但不過度銳化成黑色條紋。
金屬層架與管件呈現細膩灰鋼質感及少量使用痕跡，保留中空圓管；布料有細緻織紋；黑水管保留橡膠霧面；塑膠壺、箱與工具握把有柔和高光，不能所有物件都像塑膠。
木棧板、木盒及工具板呈現自然木紋與細小邊緣磨耗；磚牆保持圖 1 灰縫分格與原有斑駁，細化塗料質感。
地坪是乾燥灰色混凝土，使用圖 2 的細緻表面變化與柔和反光，但不變成濕地或鏡面，不新增圖 2 的黃色箭頭。
保留圖 1 物件固有色，合理紋理尺度，不任意新增髒污、零件、標籤或裝飾。
作為後續加入人物的背景母圖，全景細節清楚，不額外強化散景。

【空景與輸出】
零人物：不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。
只輸出一張 16:9 高解析度完整彩色圖片，不製作拼貼或九宮格，不加字幕、標誌、水印或外框。

【本鏡畫面】
本鏡為 factory 的第一張既有雙人全景空景，正面看向後牆：兩大堆綁束紙板與木棧板佔據前景中央，後方左側是金屬層架與物料，右側是木色工具掛板；右邊紙箱與疊放塑膠箱被邊界裁切，上方層架也被畫框裁切。嚴格保留圖 1 的紙堆比例、中央縫隙、層架立柱位置、工具板範圍及可見地板面積。
```


## 2026-10-20 factory 續作：三張完成後轉修側架

使用者授權以全景 v2 作共用美術，續作其餘機位；前三張完成後指出側架重複箱列，已選擇先修 Blender 側架。後續生成暫緩，已生成圖待核對側架修改影響。OpenAI 內建 image_gen，3 次生成，模型版本／預估及實際費用未知。目視主要構圖保留，暖光／金屬磨耗加強，孔洞、紙邊與工具細節有重繪。

### cam_twoshot_ms_level v2
- 圖1：D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_twoshot_ms_level_empty_blender.png
- 圖2（全數相同）：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png
- 原生：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-5d33a404-77d7-4ad6-a06a-47ef8c52d1ae.png
- 副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_ms_level_empty_gpt_v2.png
- 完整實際 prompt：
```text
圖1檔名：cam_twoshot_ms_level_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡是雙人中景空背景，兩堆紙板放大到佔據下方約三分之二，底部棧板在畫外；左紙堆完整頂面與右側厚度可見，右紙堆被右邊界裁切。後方左架有整捆中空直管和淺綠布束，中架有紅白藍壺、平放黑水管、線圈、六個開關及雙儀表；工具板只在最右側局部入鏡。左上有極小窗景邊緣，保持原裁切。不要恢復全景的棧板和完整地面。
```

### cam_amy_ms_15deg v2
- 圖1：D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_amy_ms_15deg_empty_blender.png
- 圖2（全數相同）：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png
- 原生：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-357e46b5-3849-4af7-aa60-a26bc5731ac9.png
- 副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_amy_ms_15deg_empty_gpt_v2.png
- 完整實際 prompt：
```text
圖1檔名：cam_amy_ms_15deg_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡是面向左側層架的斜向中景，單一紙堆佔畫面下半部及右側，兩條白束帶保留；左下紅色回收桶與極少黃色桶邊緣被畫框裁切；左牆上米白下灰綠。上方中空直管與布束被頂邊裁切，層架中層環件、兩層閥件木盒及金屬罐位置不變；右邊只見部分線圈。不加入工具牆或第二紙堆。
```

### cam_biao_ms_15deg v2
- 圖1：D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_biao_ms_15deg_empty_blender.png
- 圖2（全數相同）：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png
- 原生：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-364b9e07-b066-4a30-949a-b60f563d1ffb.png
- 副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_ms_15deg_empty_gpt_v2.png
- 完整實際 prompt：
```text
圖1檔名：cam_biao_ms_15deg_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡是面向工具板與右架的斜向中景，左下單一紙堆被左下邊界裁切，兩條束帶與頂面方向保留；左後木色工具板、右後層架上的盒件與彩色罐不變；右中兩紙箱、右下灰白及綠色鏤空塑膠箱保留遮擋及裁切。不要加入參考圖左側的直管或布料，不補完整棧板。
```


## 2026-10-20 factory 側架 v8 修正與九機位重繪完成，待評鑑

- 使用者選擇先修 Blender 側架；根因是 v7 只更新後牆三架，右牆整排貨架保留了舊版重複彩色箱列。本輪另存 .tmp/factory_workshop/factory_storage_v8.blend，沿用既有物料造型／材質搭配錯落組合及少量縮小箱件，原層架、後牆、人物及相機保留。腳本 .tmp/fix_factory_side_storage.py。
- 已重開模型，核對十機位／人物逐影格矩陣、鏡頭參數、人物網格與七張 packed images。物料組最低點與層板接觸差最大約0.00012 mm，非全場碰撞模擬。預覽修正過側架物料朝向；隱藏人物須先list快照再迭代，避免all_objects快取失效。模型存檔產生縮圖路徑警告，但重開與渲染成功。
- 僅 cam_biao_ms_15deg 與 cam_biao_ots_amy 的畫框涵蓋本次改動；兩張更新至 .tmp/factory_workshop/storage_v8_angles/（1920×1080，Cycles CUDA 96 samples，空景無景深），其餘沿用v7底圖。全景v2仍為所有圖片唯一共用美術參考。
- 本輪共10次內建image_gen／OpenAI生成（九機位＋標哥中景因側架更新追加v3）；確切模型及費用未知。舊圖均保留；全九張目視無人物、主要構圖與裁切保留，但不宣稱逐像素或工具數量完全一致，逐鏡差異見下。未更新manifest／scene_plan或正式Blender底圖，未commit/push。
- 來源稱謂更正：首張實際使用模型內嵌「廠務部_空景圖2.png」；交接紀錄已載明最原始參考在 D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/廠務區/，該內嵌圖與最原始圖的來源關係未確認。本輪沿用使用者已確認的全景v2，不再附原始參考圖。

### cam_biao_ms_15deg v3
- 有序輸入：圖1 D:/kj-openMontage/.tmp/factory_workshop/storage_v8_angles/cam_biao_ms_15deg_empty_blender.png；圖2 D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-432b1b00-cdc7-4026-9ccc-e41f99d34814.png
- 專案副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_ms_15deg_empty_gpt_v3.png
- 目視：v3依v8底圖更新最右側物料，保留紙堆、工具牆與前景箱籃；紙邊與工具細節有AI變化，v2保留作歷史。
- 完整實際 prompt：
```text
圖1檔名：cam_biao_ms_15deg_empty_blender.png（factory v8）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡是面向工具板與右架的斜向中景，左下單一紙堆被左下邊界裁切，兩條束帶與頂面方向保留；左後木色工具板、右後後牆層架上的盒件與彩色罐不變；最右側露出的側牆層架物料已更新，沿用圖1當前可見的板材、刷具與零件，不恢復彩色箱列；右中兩紙箱、右下灰白及綠色鏤空塑膠箱保留遮擋及裁切。不要加入參考圖左側的直管或布料，不補完整棧板。
```

### cam_amy_mcu_15deg v2
- 有序輸入：圖1 D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_amy_mcu_15deg_empty_blender.png；圖2 D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-54686390-5e7f-459c-aada-caebef3d2216.png
- 專案副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_amy_mcu_15deg_empty_gpt_v2.png
- 目視：Amy中近景保留上裁切管束與布料、環件、閥件盒及前景紙堆；鋼架孔洞／螺栓與材質細節有重繪。
- 完整實際 prompt：
```text
圖1檔名：cam_amy_mcu_15deg_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡是左側層架的中近景，米白／灰綠磚牆在左側，前景單一紙堆頂面及瓦楞面佔下半幅並延伸出右下邊界，保留兩條束帶與右束帶貼近右框的位置。左下只有紅桶上部；上邊被裁切的中空管堆、布束，中層環件與雙層閥件盒、右側金屬罐保持原位。無工具牆、無地面，不拉遠。
```

### cam_biao_mcu_15deg v2
- 有序輸入：圖1 D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_biao_mcu_15deg_empty_blender.png；圖2 D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-b6379424-ba47-4874-a6a3-cf055991796a.png
- 專案副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_mcu_15deg_empty_gpt_v2.png
- 目視：標哥中近景保留工具板、環件箱與罐件、下方紙堆和紙箱；工具細節及紙邊有差異。
- 完整實際 prompt：
```text
圖1檔名：cam_biao_mcu_15deg_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡是右側中近景，工具板佔左半、鋼架佔右半，前景紙板堆只佔下半且左側被裁切；左方束帶在畫外，右束帶可見。右下是兩個被裁切紙箱。層架中層雙柱堆疊黑環件、旁邊白／青藍／黃色罐，上層盒件，下層淺色圓棒與黑板及木條保持原位。無地面，不補前景塑膠箱。
```

### cam_amy_ots_biao v2
- 有序輸入：圖1 D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_amy_ots_biao_empty_blender.png；圖2 D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-0e406bd0-8129-4ce2-8eb9-31b41fb64277.png
- 專案副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_amy_ots_biao_empty_gpt_v2.png
- 目視：回收桶方向保留四張標牌的顏色順序及三桶、左緣少量藍桶、右前紙堆；桶身磨耗、牆面斑駁比底圖更強，標牌螺絲細節有變化。
- 完整實際 prompt：
```text
圖1檔名：cam_amy_ots_biao_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡為朝向回收桶牆的空景角度，並非工具牆方向。上方由左至右恰好四面青綠、綠、黃、紅回收符號牌，下方青綠、綠、黃桶及最左極少藍桶邊緣；右前景紙堆擋住右側回收桶，其右下被畫框裁切。保留牌子白色循環箭頭的既有樣式、顏色順序、間距，保留米白上牆／灰綠下牆的分界。圖2只有材質光影價值，不可把圖2工具架或雙紙堆構圖搬來，不能加入人物或過肩。
```

### cam_biao_ots_amy v2
- 有序輸入：圖1 D:/kj-openMontage/.tmp/factory_workshop/storage_v8_angles/cam_biao_ots_amy_empty_blender.png；圖2 D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-17d020e4-0372-43cc-8c4a-71f7141e4abb.png
- 專案副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_ots_amy_empty_gpt_v2.png
- 目視：側架依v8混合物料重繪，保留各層主要備件、耗材、箱件、左側紙堆與箱籃遮擋；未恢復舊版彩色箱列；立柱孔洞、物件邊緣及光斑有重繪。
- 完整實際 prompt：
```text
圖1檔名：cam_biao_ots_amy_empty_blender.png（factory v8）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡朝向側面層架，圖1已完成物料修正。兩座灰鋼架各層是不同組合的環件、木盒、刷具／木條、罐裝耗材、備用機件、開關面板與少量封閉收納箱；必須逐一依圖1保留種類、數量、顏色和擺放，不恢復舊版整齊彩色箱列。左架中層三個褐色瓶狀物、旁邊小紙盒與雙圓盤機件、下層彩色罐及工具機件；右架上層開關板、綠小箱與風扇備件，中層圓盤機件、黑箱及閥件木盒，下層彩色罐及最下層木板堆、白箱與黑環件，維持原位置、造型、支撐與遮擋。前景左邊單一紙堆、左下綠色和灰白鏤空箱、底部窄地板及原黃色線維持裁切。圖2只供美術，不加入工具牆，不變成圖2的雙紙堆全景；無人物或肩膀。
```

### cam_amy_cu_emotion v2
- 有序輸入：圖1 D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_amy_cu_emotion_empty_blender.png；圖2 D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-678f0d78-c86c-40c6-8293-851c4133f4e6.png
- 專案副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_amy_cu_emotion_empty_gpt_v2.png
- 目視：Amy特寫保留管束、布料、環件與閥件盒、紙堆緊裁切；灰綠牆分界增加掉漆，立柱接合細節有變化。
- 完整實際 prompt：
```text
圖1檔名：cam_amy_cu_emotion_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡為左側層架的緊特寫空背景：上方直管堆與布束被頂邊裁切；中層兩柱金屬環件、箱緣抹布、雙層閥件木盒與最右金屬罐保持原位置；左側米白／灰綠磚牆，左下僅一小角紅桶。前景紙板頂面佔底部約三分之一，瓦楞斷面和一條垂直束帶可見，右束帶在畫外；無地板或棧板，不增加景深模糊。
```

### cam_biao_cu_emotion v2
- 有序輸入：圖1 D:/kj-openMontage/.tmp/factory_workshop/storage_v7_angles/cam_biao_cu_emotion_empty_blender.png；圖2 D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png。
- 原生輸出：C:/Users/user/.codex/generated_images/01a1571e-6037-7491-859d-13402ba566a8/exec-7b5fd620-3624-4aa0-b7f9-18a095719158.png
- 專案副本：D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_cu_emotion_empty_gpt_v2.png
- 目視：標哥特寫保留工具板、後架環件罐材、前景紙堆與紙箱裁切；工具掛位細節、金屬磨耗與光斑有AI差異。
- 完整實際 prompt：
```text
圖1檔名：cam_biao_cu_emotion_empty_blender.png（factory v7）。
請直接編輯圖1，把本機位 Blender 空景轉成圖2同一套高品質自然細膩電影動畫3D場景背景。
圖1唯一決定相機位置、觀看方向、透視、構圖、邊界裁切、物件配置和遮擋。圖2 cam_twoshot_wide_level_empty_gpt_v2.png 是已確認的同場景共用美術，只提供材質、色彩、光影與氣氛；不要採用圖2的機位、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2柔暖日光、稍冷陰影、米白磚牆、灰色鋼材、自然褐色紙纖維／木材、低飽和工業配色；不逐張加強黃色、飽和度或泛光。同一場景換角度，依圖1朝向合理調整受光面與陰影，不複製圖2畫面座標上的日照斑。
【保留本機位】所有可見物件數量、位置、尺度、主要輪廓、表面原有顏色與遮擋依圖1。相機不旋轉、不鏡像、不拉遠或拉近。被畫框裁掉的物件維持裁切，不補出完整物件；畫外內容不搬入。保留所有層架橫梁和立柱、磚縫、工具、箱件、管件、紙堆與束帶的幾何關係，不新增配件。
【材質提升】改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與合理反射。紙板依圖2細緻乾燥纖維和瓦楞斷面，但保留圖1層次、頂面、堆疊外形及束帶。金屬呈灰鋼質感，木盒呈自然木紋，布料有織紋，橡膠霧面，塑膠有柔和高光。保留既有少量使用痕跡，不增添重度髒污，不把所有物件變成塑膠。牆面塗料細膩，保持圖1磚格與上下配色分界。地面若可見維持乾燥混凝土，只柔和反光；無地面則不要補地面。窗戶若在畫外，僅讓光線影響已有物件，不新增窗洞。
背景母圖需要近中景資訊清楚，不額外強化散景，不增加模糊。圖2看不到的物件維持圖1造型與固有色，只延續相同的材質細膩程度。
【空景與輸出】零人物、無肩膀、手臂、人體、倒影或人形白模，即使檔名包含角色或過肩仍是純空景。單張16:9橫幅最高可用解析度完整圖片，無拼貼、外框、水印或新增字幕。不新增窗戶、植物、裝飾、標線或圖1不存在的道具。
【本鏡畫面】本鏡為工具牆與右架的緊特寫空背景，左側工具板貼左邊裁切；右架頂層盒件被上邊裁切，中層雙柱黑環件、旁邊彩色罐與木盒，下層圓棒與黑板／木條維持配置。最下緣只見紙堆頂面與少量瓦楞、單條束帶，以及右下紙箱頂部。保持工具種類與掛位，不補出完整紙堆、地板或棧板。
```


最終存檔檢查：九張當前交付圖全為原生1672×941 RGB PNG（近16:9），Pillow完整解碼成功，九組原生輸出／專案副本SHA256一致；v8兩張Blender底圖1920×1080，已逐張目視。v7模型SHA256仍為7676551c6643dbfd564f9e60c77406244be0d7e60f001d44cf6ba8ffaceb1e63；v8為f8ff9aa784640a7f696c91c864aa4efcbc9fa7ed9ab84ff67b11319e2bb66c48。圖片未裁切或拉伸。


## 2026-10-20 shot_4.2.2 — GPT v2（待評鑑）

- 使用者授權：逐字使用最新五圖 prompt，在 GPT 生成一張並存入 assets/images。
- 圖片：assets/images/shot_4.2.2_gpt_v2.png；原生 1672×941 RGB PNG，未裁切拉伸，v1 保留。
- 工具：內建 image_gen；供應商 OpenAI；確切模型／費用未提供，未知；本次 1 次成功生成，無追加生成。
- 原圖：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-aa00f589-0cab-4731-ac6f-9c4ba49ce0e7.png。
- 檢查：目視輸入與輸出、PNG 完整解碼通過，來源與副本 SHA256 同為 b0aa198ffb53612b355f1415afe71832edc31952eced55949d71333fb40109cb。
- 觀察：左緣 Amy 已成灰色西裝袖與手，無紅色 blocks／頭部。小陳白袍、眼鏡、短鬍鬚及低頭握毯呈現；頭髮貼近上緣，頭頂留白與人物比例偏離 blocks。毛毯一角在白布下，但主要姿態較像掀起展示，未明確為從樣品堆底層抽出起始狀態；布樣與桌面局部配置有重繪。瓶子為藍蓋透明肋紋瓶，與前鏡 CLP 外形不同（本次未附瓶子參考）。待評鑑，未改 manifest／scene_plan／採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_chen_ms_15deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_chen_ms_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_chen.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_eco_blanket.png
- 完整實際 prompt（使用者原文）：
```text
參考圖說明：
圖 1 cam_chen_ms_15deg_empty_gpt.png：研發部樣品實驗室的場景外觀參考圖。
圖 2 cam_chen_ms_15deg_block_blender.png：小陳中景的構圖底圖。
圖 3 char_chen.jpeg：小陳人物參考圖，對應圖 2 的藍色定位人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 畫面左緣被裁切的紅色定位人物。
圖 5 prop_eco_blanket.png：環保毛毯的外觀與材質參考，多個視角展示的是同一款毛毯。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、人物佔位、大小比例、頭頂留白、背景配置與邊界裁切。不得拉遠鏡頭、擴展畫面或補出畫外身體。

將藍色定位人物替換為圖 3 的小陳，保留棕色蓬鬆捲髮、黑框眼鏡、短鬍鬚、白色實驗袍與深色襯衫。將左緣紅色定位人物的可見部分替換為圖 4 的 Amy，採用灰色西裝袖與相應膚色，只呈現底圖已有的局部軀幹、手臂與手，不補出頭部。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖。

場景材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留本鏡可見的木層架、玻璃材料罐、紗線筒、布樣、色卡板與電腦，不加入畫外的拉力測試機。人物接受與場景一致的右側窗光及環境光。

環保毛毯採用圖 5 的鼠尾草灰綠色、厚實柔軟絨面、包邊與米色布標；布標位於自然可見處時保留，不為展示標籤而扭轉毛毯。每種道具各一件，不複製參考圖的多視角排列。

畫面描述：
這是一張 50mm、眼高平視、15 度微側的小陳中景，中等景深，小陳的臉、雙手與毛毯前緣清楚可辨。小陳位於畫面中央偏右，腰部以下依圖 2 裁切；Amy 只在畫面最左緣露出原有局部身體與手臂。小陳微微側身朝向身旁實驗桌的布樣堆，調整肩臂與雙手，使兩手自然握住樣品堆底層露出的灰綠色毛毯前緣；毛毯仍有一部分壓在其他布樣下，呈現剛找到、準備抽出的起始瞬間，尚未整條展開或高舉。小陳略低頭看著手中的毛毯，嘴角帶著靦腆而無奈的淡淡苦笑，情緒克制。回收寶特瓶直立放在同一桌面、布樣堆旁的可見空位，瓶底確實接觸桌面。除上述取毯所需的上身、雙手、視線與表情調整，以及指定道具置入外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖。畫面只呈現小陳與左緣局部 Amy，不加入其他人物、字幕、標題、對話框或浮水印。
```



## 2026-10-20 shot_4.2.3 — GPT v1（待評鑑）

- 使用者授權：逐字使用本輪五圖 prompt，生成小陳雙手捧毯、Amy 觸摸絨面的版本，存入 assets/images。
- 圖片：assets/images/shot_4.2.3_gpt_v1.png；原生 1672×941 RGB PNG，未裁切拉伸。
- 工具：內建 image_gen；供應商 OpenAI；確切模型／費用未提供，未知；本次 1 次成功生成，無追加生成。
- 原圖：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-bf3f731f-3138-44f9-8fc2-ec9fa16ee6c3.png。
- 檢查：目視輸入與輸出、PNG 完整解碼通過，來源與副本 SHA256 同為 a1a8015c944e2e5f38793c3103bd4d2ba236cdc3fa6de03edf9d7ea0f6b24fa3。
- 觀察：Amy 灰袖手掌與指腹接觸灰綠毛毯、小陳白袍雙手承托（後側手大部分被毛毯遮擋）、Eco-Friendly 布標與兩人頭部畫外均呈現，無紅藍blocks。毛毯佔畫面較大；Amy 左側軀幹可見範圍增加，小陳軀幹佔位縮至右緣，未嚴格維持底圖人物比例與遮擋，桌緣及背景裁切有偏移。未見額外人物或手臂；待評鑑，未改 manifest／scene_plan／採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_blanket_insert_iso_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_blanket_insert_iso_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_chen.jpeg
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_eco_blanket.png
- 完整實際 prompt（使用者原文）：
```text
參考圖說明：
圖 1 cam_blanket_insert_iso_empty_gpt.png：研發部實驗桌的場景外觀參考圖。
圖 2 cam_blanket_insert_iso_block_blender.png：本鏡桌面、人物局部與遮擋關係的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側紅色定位人物。
圖 4 char_chen.jpeg：小陳人物參考圖，對應圖 2 右側藍色定位人物。
圖 5 prop_eco_blanket.png：環保毛毯的外觀與材質參考，多個視角展示的是同一款毛毯。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、桌緣高度、人物佔位、身體比例、背景配置與邊界裁切。不得拉遠鏡頭、擴展畫面或補出畫外身體。

將左側紅色定位人物的可見部分替換為圖 3 的 Amy，採用灰色西裝袖、捲起的袖口與相應膚色。將右側藍色定位人物的可見部分替換為圖 4 的小陳，採用白色實驗袍、深色襯衫與相應膚色。只呈現圖 2 已有的局部軀幹、手臂與手，兩人的頭部均保持在畫外。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留紅藍方塊外觀。

場景材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留可見的白色與深藍布卷、平鋪布樣、桌緣垂布及其他實驗用品，不補出被人物遮住的儀器。人物與道具接受一致的右側柔暖窗光、環境光與接觸陰影。

在兩人之間、小陳雙手捧著一條摺疊的環保毛毯。毛毯採用圖 5 的鼠尾草灰綠色、厚實柔軟絨面、同色包邊及米色「Eco-Friendly」布標。布標位於自然可見的一角，不為展示標籤而扭轉毛毯，不複製參考圖的多視角排列。

畫面描述：
這是一張 55mm、微俯視的毛毯觸感特寫插鏡，取景沿用圖 2。Amy 的局部手臂從畫面左側伸入，小陳的局部軀幹與手臂位於右側，兩人的臉都不入鏡。小陳雙手捧著摺疊的灰綠色毛毯。調整 Amy 可見的前臂、手腕與手指，使她掌心朝下、手指自然微張，以指腹輕輕貼住毛毯上表面，定格在剛接觸、感受柔軟質地的瞬間；接觸處的絨毛輕微壓伏，手指與布面之間有細緻接觸陰影，不懸空、不穿入布料，也不抓起毛毯。小陳靠近桌面的那隻手輕扶毛毯右側邊緣，另一隻手維持圖 2 的位置與裁切。毛毯由小陳雙手捧著，保留大片可見絨面與自然摺層。焦點落在 Amy 的指腹、接觸處絨毛與毛毯包邊，後方布卷輕柔失焦，仍可辨識實驗室環境。除指定觸摸與扶毯所需的手臂、手腕及手指調整、道具置入與景深調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖。人物只呈現 Amy 與小陳在底圖中的局部身體，不出現兩人的頭部，不增加其他人物或多餘手臂。不加入字幕、ESG 疊字、標題、對話框或浮水印；僅保留道具本身的布標與回收圖案。
```


## 2026-10-20 shot_4.5.1 — GPT v1（雙人全景，待評鑑）

- 使用者授權：逐字使用聊天最後確認的四圖 prompt，在 GPT 生成一次並存入指定 assets/images。
- 工具：內建 image_gen；供應商 OpenAI；確切模型版本與費用未提供、未知。本次 1 次成功生成，未追加生成。
- 圖片：assets/images/shot_4.5.1_gpt_v1.png；原生 1672×941 RGB PNG，未裁切或拉伸。
- 原生輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-af29d651-4e3f-4c75-a66e-1704ea0be9df.png
- 指定儲存路徑：D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.5.1_gpt_v1.png
- 檢查：輸入與輸出目視、PNG 完整解碼通過；來源／副本 SHA256 一致：98d0da298471046afc83508a300d08fd414d1efc430bff325361a046790c00f4。
- 觀察：Amy 左、標哥右；兩人黃帽、Amy 灰西裝且無反光背心、標哥眼鏡／灰鬍鬚／灰工作服均呈現，無額外人物或字幕。模型額外加入 Amy 抬手攤掌手勢；人物比例、頭頂留白與下緣裁切未完全依 blocks，兩人鞋子完整入鏡；背景工具及紙板細節有重繪。待使用者評鑑，未標為構圖完全通過。
- 狀態：未更新 asset_manifest／scene_plan 或採用版本，保留既有 shot_4.5.1.png；未製作影片或推進整個 assets 階段核准。
- 有序參考圖：
  1. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_empty_gpt_v2.png
  2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_wide_level_block_blender.png
  3. D:/Dropbox/kj-om-projects/course-51-esg/clp/char_amy.jpeg
  4. D:/Dropbox/kj-om-projects/course-51-esg/clp/char_biaoge.jpeg
- 完整實際 prompt（逐字沿用）：
```text
參考圖說明：
圖 1 cam_twoshot_wide_level_empty_gpt_v2.png：廠務暫存區的場景外觀參考圖。
圖 2 cam_twoshot_wide_level_block_blender.png：雙人全景構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側紅色定位人物。
圖 4 char_biaoge.jpeg：標哥人物參考圖，對應圖 2 右側藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其機位、透視、人物站位、大小比例、頭頂留白、可見範圍、邊界裁切與背景配置。

將左側紅色定位人物替換為圖 3 的 Amy，保留棕色微捲短髮、綠色眼睛、灰色西裝外套與米白色開領襯衫，加戴黃色工安帽，不穿反光背心。

將右側藍色定位人物替換為圖 4 的標哥，保留黃色工安帽、眼鏡、灰白短鬍鬚與灰色工作服。人物參考圖只提供外觀與服裝，不採用其展示姿態或多視角拼貼構圖。

場景材質、風格與光影採用圖 1，空間配置仍依圖 2。保留既有紙板堆、束帶、貨架、物料與工具板，人物接受與場景一致的柔暖日光及環境光。

畫面描述：
這是一張 40mm、近站姿眼高的雙人全景，中等景深，兩人與廠務背景均清楚可辨。Amy 位於左側，標哥位於右側，可見身體部位與畫面下緣裁切依圖 2。Amy 保持原站位，將頭部與上身自然轉向鏡頭，精神飽滿、自信親切地微笑，嘴唇微啟，呈現準備向觀眾介紹廠務部的開場瞬間。標哥保持原站位與自然站姿，帶著親切微笑看向 Amy，安靜聆聽。除上述頭部、上身朝向及表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，只呈現 Amy 與標哥兩人，不加入字幕、標題、對話框或浮水印。
```


## 2026-10-20 shot_4.2.4 — GPT v1（待評鑑）

- 使用者授權：使用前輪完整四圖 W2I prompt，在 GPT 生成一張並存入 assets/images。
- 圖片：assets/images/shot_4.2.4_gpt_v1.png；原生 1672×941 RGB PNG，未裁切拉伸。
- 工具：內建 image_gen；供應商 OpenAI；確切模型／費用未提供，未知；本次 1 次成功生成，無追加生成。
- 原圖：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-8c93a784-1062-4887-a504-4aaac34b66b9.png。
- 檢查：目視輸入與輸出、PNG 完整解碼通過，來源與副本 SHA256 同為 a445515d2f242cd5ed8f8c06fc7c419cc0e88629b2eab8d415042c3210d75df7。
- 觀察：Amy 左側中景、綠眼灰套裝、興奮鼓勵神情與小陳右前景白袍過肩呈現，無紅藍blocks或額外視覺符號。Amy 改用畫面左側手比劃，原靠畫面中央的手改垂下；頭部較大、頭頂留白減少，人物佔位及背景遮擋較底圖有偏移。待評鑑，未改 manifest／scene_plan／採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_amy_ots_chen_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_amy_ots_chen_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_chen.jpeg
- 完整實際 prompt（沿用前次回覆原文）：
```text
參考圖說明：
圖 1 cam_amy_ots_chen_empty_gpt.png：研發部實驗室的場景外觀參考圖。
圖 2 cam_amy_ots_chen_block_blender.png：過小陳肩拍 Amy 的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側紅色定位人物。
圖 4 char_chen.jpeg：小陳人物參考圖，對應圖 2 右前景藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、人物佔位、前後距離、大小比例、可見部位與遮擋關係。保留 Amy 的頭頂留白，以及小陳頭部、肩背和手臂在畫面邊界的原有裁切。不得拉遠鏡頭、擴展畫面、交換左右位置或補出畫外身體。

將左側紅色定位人物替換為圖 3 的 Amy，保留棕色及下巴的波浪短髮、綠色眼睛、灰色西裝外套與淺色襯衫。將右前景藍色定位人物替換為圖 4 的小陳，保留棕色蓬鬆捲髮、白色實驗袍與深色襯衫；黑框眼鏡只呈現此角度自然可見的部分，不為展示五官而轉成正面。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留紅藍方塊外觀。

場景的材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留 Amy 身後白色看板上的布料色卡與測試曲線圖，以及右後方木層架、玻璃材料罐、文件夾、紗線筒與實驗桌設備。只呈現圖 2 中原本可見的區域，不補出被人物遮擋的背景。人物接受與場景一致的柔暖窗光、環境光與自然陰影。

畫面描述：
這是一張 50mm、眼高平視、過小陳肩拍 Amy 的過肩中景。Amy 位於畫面左側中景，上半身與雙手的可見範圍依圖 2；小陳位於右前景，以後側頭部、耳朵、肩背及局部手臂形成前景遮擋，朝向 Amy 聆聽。Amy 看著小陳，眼睛明亮、眉毛微微揚起，帶著發現產品潛力的興奮與真誠鼓勵，嘴角上揚、雙唇微張，呈現剛開口分享好消息的瞬間。將 Amy 原本靠畫面中央抬起的手調整為手掌自然張開、手指放鬆，在胸前朝小陳做出鼓勵性的說明手勢；另一隻手保留圖 2 的位置與裁切。小陳保持朝向 Amy 的聆聽姿態，不回頭看鏡頭。淺景深聚焦 Amy 的眼睛與臉部，右前景小陳的肩背及後方材料層架輕柔失焦，仍能辨識人物與研發環境。除上述 Amy 的表情、視線與手勢調整，以及景深調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有 Amy 與小陳兩人。不加入字幕、對話框、標題、浮水印、歐盟旗幟、金幣、搖錢樹或市場圖表等額外視覺符號。
```



## 2026-10-20 shot_4.2.5 — GPT v1（待評鑑）

- 使用者授權：使用前輪完整三圖 W2I prompt，在 GPT 生成一張並存入 assets/images。
- 圖片：assets/images/shot_4.2.5_gpt_v1.png；原生 1672×941 RGB PNG，未裁切拉伸。
- 工具：內建 image_gen；供應商 OpenAI；確切模型／費用未提供，未知；本次 1 次成功生成，無追加生成。
- 原圖：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-41a199bd-af0e-49c8-847f-bcef55c4251c.png。
- 檢查：目視輸入與輸出、PNG 完整解碼通過，來源與副本 SHA256 同為 c104945d4763e9f117a410d3484c8b53a58218af385e1d5e0d269cad8cf46cf1。
- 觀察：小陳單人、白袍／黑框眼鏡／短鬍鬚及驚喜微笑呈現，無Amy／手／毛毯／象徵特效。明顯未符：頭部與視線朝畫面右側，與prompt指定左側相反；髮頂貼上緣，未保留頭頂留白。人物肩寬／比例及背景遮擋亦偏離blocks，不能宣告符合構圖與視線要求。待評鑑，未改 manifest／scene_plan／採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_chen_mcu_15deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_chen_mcu_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_chen.jpeg
- 完整實際 prompt（沿用前次回覆原文）：
```text
參考圖說明：
圖 1 cam_chen_mcu_15deg_empty_gpt.png：研發部實驗室的場景外觀參考圖。
圖 2 cam_chen_mcu_15deg_block_blender.png：小陳單人中近景的構圖底圖。
圖 3 char_chen.jpeg：小陳人物參考圖，對應圖 2 的藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、人物佔位、頭部與肩膀大小比例、頭頂留白、背景配置與邊界裁切。完整保留頭頂輪廓，不放大頭部或讓蓬鬆髮型碰到畫面上緣。不得拉遠或拉近鏡頭、擴展畫面、補出畫外身體。

將藍色定位人物替換為圖 3 的小陳，保留棕色蓬鬆捲髮、黑框眼鏡、棕色眼睛、短鬍鬚、白色實驗袍與深色襯衫。人物參考圖只提供五官、髮型與服裝，不採用其展示姿態或拼貼構圖，不保留藍色方塊外觀。

場景的材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留本鏡可見的木層架、深藍與淺色紗線筒、玻璃材料罐、文件夾、疊放樣品冊、布料色卡板，以及右下方局部電腦螢幕。只呈現底圖可見區域，不補出被小陳遮擋的背景。人物接受與場景一致的柔暖窗光及自然環境光，眼鏡反光保持克制，讓雙眼清楚可見。

畫面描述：
這是一張 70mm、眼高平視、15 度微側的小陳單人中近景，胸部以上入鏡，人物位置、肩線與裁切沿用圖 2。小陳的頭部微朝畫面左側，視線落在畫外 Amy 的眼睛方向，不看鏡頭。定格在他剛聽懂這條毛毯可能獲得市場肯定的瞬間：鏡片後的雙眼自然睜亮，眉毛微微上揚，嘴角開始揚起，雙唇稍微張開，帶著「真的假的？」的驚喜與重新燃起的期待。保留他原有靦腆、真誠的氣質，不做誇張瞪眼、張大嘴或狂喜表情。肩膀與軀幹保持圖 2 的姿態，雙手與毛毯留在畫面之外。淺景深聚焦雙眼、眼鏡邊框與臉部表情，後方材料層架及色卡板輕柔失焦，仍可辨識研發實驗室環境。除上述表情、視線與景深調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有小陳一人。不加入 Amy、畫外伸入的手、毛毯、字幕、對話框、標題或浮水印；不加入發光眼睛、星星、燈泡或其他象徵特效。
```



## 2026-10-20 shot_4.2.5 — GPT v2（視線修正，待評鑑）

- 使用者授權：將頭部與視線改朝畫面左側；以 v1 為唯一編輯底圖，另存 v2。
- 圖片：assets/images/shot_4.2.5_gpt_v2.png；原生 1672×941 RGB PNG，未裁切拉伸，保留 v1。
- 工具：內建 image_gen；供應商 OpenAI；確切模型／費用未提供，未知；修正生成 1 次。
- 原圖：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-8257445f-bf73-4d1e-96dd-09fcef7b8fbd.png。
- 檢查：目視確認鼻尖與瞳孔朝圖片左側，保持驚喜神情；背景左側深藍線筒、右側色卡板與螢幕未左右翻轉。PNG 完整解碼通過，來源與副本 SHA256 同為 e542718105bc5e5fb490e015202ca247561457de8abab45da3aefc4120f097ef。
- 觀察：本次指定頭部／視線修正已呈現，視線略朝左上；頭髮依新角度重繪，仍接近上緣。背景主要配置與身體位置保留，未做像素級一致保證。待評鑑，未改 manifest／scene_plan／採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.2.5_gpt_v1.png
- 完整實際 prompt：
```text
請局部編輯這張 shot_4.2.5 圖片，只修正小陳的頭部朝向與視線。

把小陳的頭部轉向畫面左側，也就是觀眾看到的圖片左邊；鼻尖朝向圖片左邊，雙眼的瞳孔與目光自然朝向畫外左側的 Amy。必須讓人清楚看出他在與畫面左側的人對話，不看鏡頭，也不看畫面右側。保持原本約15度微側的自然頭部角度，不轉成完全側面。

保留小陳棕色蓬鬆捲髮、黑框眼鏡、棕色眼睛、短鬍鬚、白色實驗袍與深色襯衫，保留雙眼明亮、眉毛微揚、雙唇微張的驚喜期待笑容。頭部在原位置自然轉向，頸部與眼鏡配合轉向調整，肩膀與軀幹保持原姿態。

除此之外，保持原圖的取景、人物位置與尺度、裁切、景深、色彩、光影及背景所有物件的位置。不可水平鏡像或左右翻轉整張圖片。背景左側的深藍紗線筒、右側的布料色卡板與電腦螢幕保持原側，不交換位置、不重排背景。不要加入人物、手、毛毯、字幕或特效。

輸出一張16:9彩色圖片。
```


## 2026-10-20 shot_4.5.2 — GPT v2（腰部以上雙人中景，待評鑑）

- 使用者授權：將 v1 再切近一些，改為腰部以上。
- 工具／配方：內建 image_gen／OpenAI／I2I；確切模型版本與費用未提供、未知。本次 1 次成功生成，未追加生成。
- 圖片：assets/images/shot_4.5.2_gpt_v2.png；原生 1672×941 RGB PNG，未另行裁切或拉伸。
- 原生輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-1266f009-d35a-4c7e-bf03-cff76cdac362.png
- 指定儲存路徑：D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.5.2_gpt_v2.png
- 檢查：目視已收近為腰線附近雙人中景，兩人安全帽完整、互看微笑及原服裝保留，雙手隨取景落在畫外；背景與衣物局部有 AI 重繪。PNG 完整解碼通過，來源／副本 SHA256 一致：c6addb399f14aea02ba607c9d13160f3f0eec07587a0bd8494dfbca956d1a395。
- 狀態：待評鑑，保留 v1 與既有無版本號圖；未改 asset_manifest／scene_plan 或採用版本。
- 有序參考圖：
  1. D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.5.2_gpt_v1.png
- 完整實際 prompt：
```text
以圖 1 shot_4.5.2_gpt_v1.png 為基礎，只將鏡頭取景收近為「兩人腰部以上的雙人中景」。

保持橫向 16:9、原本眼高拍攝方向與自然透視。Amy 在左、標哥在右，兩人都要留在畫內，頭部、安全帽與肩膀完整入鏡，帽頂僅留少量自然空間；畫面下緣切在兩人的腰線附近，腰部以下、髖部、大腿、腿與鞋都在畫外。兩人的臉與上半身明顯放大成為主體，保留兩人相望的對話空間；雙臂仍自然垂放，手掌若因此在畫外就保持畫外，不為了展示雙手而拉遠取景或抬高手臂。

保留原圖兩人的身分、五官、髮型、黃色工安帽、Amy 灰色西裝與米白襯衫、標哥眼鏡與灰白鬍鬚及灰色工作服；保留 Amy 帶好奇笑意看向標哥、嘴唇微啟，以及標哥親切微笑回望 Amy 的同一瞬間，不改表情、視線與人物關係。

背景仍是同一廠務暫存區，紙板堆、貨架與工具板維持原有相對配置，只隨收近取景自然裁切；保持原圖暖日光、材質、色調與 3D 電影動畫風格。不新增物件、不鏡像、不換角度、不增加人物。

輸出一張 16:9 彩色分鏡圖，不加字幕、文字、標題、對話框、外框或浮水印。
```


## 2026-10-20 shot_4.2.6 — GPT v1（待評鑑）

- 使用者授權：使用前輪完整五圖 W2I prompt，在 GPT 生成一張並存入 assets/images。
- 圖片：assets/images/shot_4.2.6_gpt_v1.png；原生 1672×941 RGB PNG，未裁切拉伸。
- 工具：內建 image_gen；供應商 OpenAI；確切模型／費用未提供，未知；本次 1 次成功生成，無追加生成。
- 原圖：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-2e3b17c8-c953-4927-9327-25f4f5a076ca.png。
- 檢查：目視輸入與輸出、PNG 完整解碼通過，來源與副本 SHA256 同為 f932442bae86e634af0222d6a2f2d2730d25fd6cc1b5d4a2661107b6071a297f。
- 觀察：Amy左／小陳右、對鏡微笑、比讚與雙手捧灰綠毛毯呈現，毛毯有Eco-Friendly布標，無紅藍blocks／額外人物／字幕／特效。Amy改用畫面左側手比讚、靠中央手垂下，與指定手別不同；兩人站位向中央靠攏、間距縮短，頭頂留白減少，身體比例與背景遮擋偏離blocks。待評鑑，未改 manifest／scene_plan／採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_twoshot_ms_level_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_twoshot_ms_level_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_chen.jpeg
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_eco_blanket.png
- 完整實際 prompt（沿用前次回覆原文）：
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：研發部樣品實驗室的場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：Amy 與小陳雙人平視中景的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側紅色定位人物。
圖 4 char_chen.jpeg：小陳人物參考圖，對應圖 2 右側藍色定位人物。
圖 5 prop_eco_blanket.png：環保毛毯的外觀與材質參考，多個視角展示的是同一款毛毯。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、人物佔位、兩人間距、身高差、大小比例、頭頂留白、背景配置與邊界裁切。兩人的頭部輪廓完整入鏡，不放大頭部，不讓髮型碰到畫面上緣。不得拉遠或拉近鏡頭、擴展畫面、交換左右位置或補出畫外身體。

將左側紅色定位人物替換為圖 3 的 Amy，保留棕色及下巴的波浪短髮、綠色眼睛、灰色西裝外套、捲起的袖口與淺色襯衫。將右側藍色定位人物替換為圖 4 的小陳，保留棕色蓬鬆捲髮、黑框眼鏡、棕色眼睛、短鬍鬚、白色實驗袍與深色襯衫。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留紅藍方塊外觀。

場景的材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留本鏡可見的雙層木架、玻璃材料罐、文件夾、紗線筒、布料色卡板、實驗桌設備、布卷與桌緣垂布。只呈現底圖可見區域，不補出被人物遮擋的物件。人物與毛毯接受一致的柔暖窗光、環境光與自然接觸陰影。

小陳懷中的環保毛毯採用圖 5 的鼠尾草灰綠色、厚實柔軟絨面、同色包邊與米色「Eco-Friendly」布標。毛毯只有一條，摺疊成方便雙手捧持的尺寸；布標位於自然可見的一角，不為展示標籤而扭轉毛毯，不複製參考圖的多視角排列。

畫面描述：
這是一張 48mm、眼高平視的雙人中景，Amy 在左、小陳在右，兩人站在研發實驗桌前，上半身及手部可見範圍沿用圖 2。Amy 的頭部與目光朝向正前方鏡頭，帶著自信、開朗的笑容，嘴唇微張，呈現準備向觀眾總結研發成果的瞬間。將 Amy 在圖 2 中靠畫面中央、原本抬起的那隻手調整為胸前比讚：拇指自然朝上，其餘四指收攏，手腕放鬆，手不要伸近鏡頭或遮住臉；另一隻手保持底圖的位置與裁切，不交換兩手動作。小陳同樣看向正前方鏡頭，露出靦腆而自豪的微笑，眼鏡後的雙眼清楚可見；調整雙臂與手掌，將摺疊的灰綠色毛毯穩穩捧在胸腹前，一手托住底部、另一手扶住側邊，使毛毯自然貼近身體，呈現柔軟摺層與受力形狀，不懸空、不遮住臉。中等景深讓兩人的眼睛、表情、比讚手勢與毛毯清楚可辨，背景稍柔化但仍保留研發實驗室的辨識度。除上述頭部、視線、表情、比讚及捧毯所需的手臂與手指調整，以及毛毯置入外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有 Amy 與小陳兩人。不加入其他人物、手機、自拍棒、字幕、標題、對話框、浮水印或超能力特效；僅保留毛毯本身的布標。
```


## 2026-10-20 shot_4.5.3 — GPT v1（待評鑑）

- 使用者授權：使用上一版 prompt 在 GPT 生圖，存入指定 assets/images；生成前已重申現有白模仍為近景，本次沿用現有三圖，未改 prompt 或白模。
- 工具／配方：內建 image_gen／OpenAI／W2I；確切模型版本與費用未提供、未知。本次 1 次成功生成，未追加生成。
- 圖片：assets/images/shot_4.5.3_gpt_v1.png；原生 1672×941 RGB PNG，未另行裁切或拉伸。
- 原生輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-66f30d73-aba0-4fb0-9c1f-4700a98ba5f2.png
- 指定儲存路徑：D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.5.3_gpt_v1.png
- 檢查：輸出目視與 PNG 完整解碼通過；來源／副本 SHA256 一致：1a6cb8fc9519bb988ce584ea9416c824350b0b9c7f9ea6b7ba9d94f754aa8c0b。
- 觀察：僅標哥一人，黃帽／眼鏡／灰鬍鬚／灰工作服與米色內搭呈現，朝畫左張嘴爽朗笑；白色與綠色料件箱的「金屬」「塑料」標籤清楚可辨。模型較原白模拉遠並重排人物在畫面中的位置，取景接近腰上，雙手仍在畫外；料件箱可見範圍增大，背景及人物比例未精確沿用白模。待使用者評鑑，未標為完整符合白模或後續手勢需求。
- 狀態：待評鑑，保留既有 shot_4.5.3.png；未改 asset_manifest／scene_plan 或採用版本，未生成影片。
- 有序參考圖：
  1. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/factory/cameras/cam_biao_ms_15deg_empty_gpt_v3.png
  2. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/factory/cameras/cam_biao_ms_15deg_block_blender.png
  3. D:/Dropbox/kj-om-projects/course-51-esg/clp/char_biaoge.jpeg
- 完整實際 prompt（逐字沿用）：
```text
參考圖說明：
圖 1 cam_biao_ms_15deg_empty_gpt_v3.png：廠務暫存區的場景外觀參考圖。
圖 2 cam_biao_ms_15deg_block_blender.png：本鏡構圖底圖。
圖 3 char_biaoge.jpeg：標哥人物參考圖，對應圖 2 的藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、透視、人物站位、大小比例、頭頂留白、邊界裁切與背景配置。

將藍色定位人物替換為圖 3 的標哥，保留黃色工安帽、眼鏡、灰白短鬍鬚、灰色工作服與米色內搭。人物參考圖只提供外觀與服裝，不採用其展示姿態或多視角拼貼構圖。

場景材質、風格與光影採用圖 1，空間配置仍依圖 2。保留紙板堆、束帶、工具板、貨架及既有物料，人物接受與場景一致的柔暖日光及環境光。

在畫面右側既有料件箱的可見正面補上分類標籤：白色箱標示「金屬」，綠色箱標示「塑料」。標籤貼合箱體表面與透視，保留箱體原有造型、位置及遮擋，不新增箱子，不將分類標籤貼在紙板堆上。

畫面描述：
這是一張 60mm、近站姿眼高、15 度微側拍的標哥單人腰上中景，中等景深，標哥的臉部清晰，身旁料件箱與分類標籤仍可辨識。標哥站在既有訪談位置，頭部自然朝向畫面左側、鏡外的 Amy，眼角帶笑、臉頰微微抬起，嘴巴自然張開，定格在開始爽朗笑出「哈哈」的瞬間，神情親切、豪爽而帶些自豪。肩膀放鬆，手臂保持自然起始姿態，尚未伸手指向料件箱，保留後續抬臂指箱的畫內空間。Amy 完全位於鏡外。除上述表情、視線與分類標籤外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，只呈現標哥一人。僅保留箱體上的「金屬」「塑料」分類標籤，不加入字幕、標題、對話框、金額圖卡或浮水印。
```


## 2026-10-20 shot_4.2.2 — GPT v3（過 Amy 肩新機位，待評鑑）

- 使用者授權：逐字使用最新五圖 prompt，以 GPT 生成一張並存至 assets/images。
- 工具／供應商：內建 image_gen／OpenAI；具體模型與費用未回傳，未知。生成一次。
- 輸出：assets/images/shot_4.2.2_gpt_v3.png；原生 1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-002d7465-d60f-47cb-8c28-a48dced1f25e.png
- 驗證：完整解碼成功；來源與副本 SHA256 一致：38208462b3fcea1569c2666648eca96d0328ac5eaf6606fd6564725d171e82f2。
- 目視觀察：Amy 後側頭部及灰色肩背在左前景，小陳在右側低頭取毯，一手拉毛毯包邊、另一手扶白色布卷；取毯動作清楚。毛毯露出面積仍比指定大，布卷排列有重繪，人物／構圖仍有些微偏移。未追加生成，未更改正式採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_chen_ots_amy_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/rd_office/cameras/cam_chen_ots_amy_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_chen.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_eco_blanket.png
- 完整實際 prompt（使用者原文）：
```text
參考圖說明：
圖 1 cam_chen_ots_amy_empty_gpt.png：研發部實驗室的場景外觀參考圖。
圖 2 cam_chen_ots_amy_block_blender.png：過 Amy 肩拍小陳的構圖底圖。
圖 3 char_chen.jpeg：小陳人物參考圖，對應圖 2 右側藍色定位人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左前景紅色定位人物。
圖 5 prop_eco_blanket.png：環保毛毯的外觀與材質參考，多個視角展示的是同一款毛毯。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、兩人前後距離、人物佔位、大小比例、頭頂留白與邊界裁切。維持 Amy 左前景、小陳右側中景的過肩關係，不交換左右、不鏡像背景，不拉遠鏡頭或補出畫外身體。

將右側藍色定位人物替換為圖 3 的小陳，保留棕色蓬鬆捲髮、黑框眼鏡、短鬍鬚、白色實驗袍與深色襯衫。頭部尺度依底圖，髮頂與畫面上緣之間保留原有空間。

將左前景紅色定位人物替換為圖 4 的 Amy，保留本角度可見的棕色短髮、後側頭部、灰色西裝肩背與局部手臂，沿用底圖裁切，不轉向鏡頭展示正臉。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留紅藍方塊外觀。

場景材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留本鏡可見的木層架、紗線筒、玻璃材料罐、文件夾、布卷、實驗設備與窗簾，不搬移桌面或重新排列背景。人物與道具接受一致的柔暖窗光及自然接觸陰影。

環保毛毯採用圖 5 的鼠尾草灰綠色、厚實絨面、同色包邊與米色布標。毛毯只有一條，藏在小陳身旁、兩人之間可見桌面上的既有布樣底層。大部分毯身仍被上層布樣壓住，只露出可抓取的前緣與一角；布標若被遮住就維持遮擋，不為展示標籤而翻轉毛毯。


畫面描述：
這是一張眼高平視、過 Amy 肩拍小陳的中景，取景沿用圖 2。Amy 的後側頭部與肩膀位於左前景，微微失焦；小陳在畫面右側，是清晰的主要人物。小陳站位不變，上身微微側向身旁實驗桌，將靠近布樣堆的手伸向底層毛毯，指尖夾住露出的灰綠色包邊，剛向自己拉出一小段；另一隻手扶穩上層布樣。只調整取毯所需的肩臂、手腕與手指，手部依原畫框自然裁切，不擴大取景。毛毯仍主要平放在桌上並被其他布樣壓住，露出的邊角受拉形成少量自然皺褶，沒有被雙手托到胸前，也沒有展開朝鏡頭展示。小陳略低頭看向毛毯，眉眼帶著些許無奈，嘴角浮現靦腆而自嘲的苦笑，呈現剛找回兩年前試作品的瞬間。Amy 保持面向小陳聆聽，不伸手搶拿毛毯。焦點以小陳臉部與取毯位置為主，前景 Amy 與遠處背景適度柔化。除上述取毯姿態、表情、視線與指定道具置入外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有小陳與左前景局部 Amy。不加入字幕、標題、對話框或浮水印，不加入額外人物或多餘手臂。
```



## 2026-10-20 shot_4.5.4 — GPT v1（待評鑑）

- 使用者授權：使用上一輪提供的完整三圖 prompt，以 GPT 生成一張並存至指定 assets/images。
- 工具／供應商：內建 image_gen／OpenAI；具體模型與費用未回傳，未知。生成一次。
- 輸出：assets/images/shot_4.5.4_gpt_v1.png；原生 1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-3a1d4233-5ada-47e1-898a-e394bb8577d1.png
- 驗證：完整解碼成功；來源與副本 SHA256 一致：b1648b08f2830787330add09ec0bc5dc13057dda159f3da552f71dca9c3825ee。
- 目視觀察：單人標哥、黃色工安帽、灰色工作服、眼鏡與灰白鬍鬚呈現；頭部及視線朝畫左（略左上），開心微笑；左側手低掌心向下、右側手高掌心向上，雙手完整且未遮臉。頭部較blocks縮小，軀幹及手臂露出較多，人物佔位與背景遮擋有變動，取景未完全保留。未追加生成，未更改正式採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_mcu_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_mcu_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_biaoge.jpeg
- 完整實際 prompt：
```text
參考圖說明：
圖 1 cam_biao_mcu_15deg_empty_gpt_v3.png：廠務現場的場景外觀參考圖。
圖 2 cam_biao_mcu_15deg_block_blender.png：標哥中近景的構圖底圖。
圖 3 char_biaoge.jpeg：標哥人物參考圖，對應圖 2 戴黃色工安帽的藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、人物佔位、頭部尺度、肩膀位置、背景配置與邊界裁切。不得拉遠鏡頭、擴展畫面或縮小人物來容納手勢。工安帽與畫面上緣的裁切關係沿用底圖，不為露出整頂帽子而重新構圖。

將藍色定位人物替換為圖 3 的標哥，保留黃色工安帽、灰黑短髮、濃眉、細金屬框眼鏡、灰白短鬍鬚、灰色工作服、淺灰肩部條帶與米色內搭。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留方塊外觀。

場景材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留本鏡可見的左側工具掛板、前景瓦楞紙板堆，以及右側貨架、收納盒與材料罐；背景依人物自然遮擋，不補出被身體擋住的物件。人物接受與場景一致的暖色自然光及環境光，保留工安帽簷下、眼鏡與衣領的自然陰影。

畫面描述：
這是一張 75mm、近站姿眼高、15 度微側的標哥中近景，取景沿用圖 2。標哥位於畫面中央偏右，胸部以下依原畫框裁切。頭部微微轉向畫面左側，鼻尖朝左，雙眼看向畫左鏡外的 Amy，不看鏡頭或畫面右側。標哥帶著爽朗而自豪的笑容，嘴巴微張、兩頰上提，呈現正要說明「這一來一回」的瞬間。調整雙肩、手臂與手腕，讓原本位於畫外的雙手抬至胸前、進入畫面下半部：畫面左側的手略低，掌心斜向下；畫面右側的手略高，掌心斜向上，兩手自然分開，形成準備比劃支出與收入的起始姿勢。手指放鬆微彎，雙手與手指完整留在既有畫框內，手肘可在畫外，不遮住下巴或臉部，不做數鈔票、握拳或比讚動作。雙手空手，沒有帳本、鈔票或其他新增道具。焦點落在標哥的臉部與胸前雙手，背景適度柔化，仍可辨識工具板、紙板堆與貨架。除上述表情、視線與抬手比劃所需的局部調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有標哥一人，Amy 保持在畫外。不加入額外人物、多餘手臂、字幕、金額、收支圖表、E 字樣、標題、對話框或浮水印。
```



## 2026-10-20 shot_4.5.4 — GPT v2（視線修正，待評鑑）

- 使用者授權：眼神看向畫面左側，修正 v1 看似左後方的視線。
- 工具／供應商：內建 image_gen／OpenAI；具體模型與費用未知；本次局部編輯1次。
- 輸出：assets/images/shot_4.5.4_gpt_v2.png；1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-44f2f231-0c86-4f50-a4da-73b197f6944b.png
- 驗證：完整解碼成功，來源與副本SHA256一致：0e798305647c208e637ef3ba5ee9edda7e6c26600715ae925261c3ed7c3d7d47。
- 目視：瞳孔與眼瞼略向下調整，較v1水平朝畫左；改動幅度小，左後方觀感是否消除仍待使用者評鑑。頭部、雙手姿勢及背景構圖大致保留，未鏡像。保留v1，未改manifest。
- 唯一編輯底圖：D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.5.4_gpt_v1.png
- 完整實際 prompt：
```text
請局部編輯這張標哥分鏡圖，只修正雙眼的注視方向。
標哥應看向畫面的正左側、與自己雙眼同高的鏡外對話者 Amy。對話者在他的左前方，而不是他的左後方。將兩眼虹膜與瞳孔從現在偏左上、回望後方的方向，調整為自然一致的水平向畫左注視；眼神放平，不仰望、不往左後方回瞥，也不看鏡頭。雙眼聚焦同一位近距離對話者，不鬥雞眼，不把瞳孔擠到極端眼角。必要時僅微調眼瞼，使眼神自然放鬆，保留開心說話的笑容。
其餘沿用原圖：頭部角度、工安帽、眼鏡框、眉毛、鼻子、嘴巴、鬍鬚、人物大小與位置、身體、左右手的高度及掌心方向、服裝、背景、光影、景深、相機取景與所有邊界裁切均保持。不要轉動整個頭部或身體，不鏡像，不拉遠或重新構圖，不新增人物或物件。
輸出一張相同16:9比例的彩色分鏡圖，不加入任何文字或浮水印。
```



## 2026-10-20 shot_4.5.4 — GPT v3（朝向 Amy，待評鑑）

- 使用者指出v2仍不對，要求注視Amy。檢視雙人及過肩blocks，確認Amy在畫左且較矮；改為連同頭部轉向、略低頭，不能只平移瞳孔。
- 工具／供應商：內建image_gen／OpenAI；模型及費用未知；本次生成1次。
- 唯一編輯底圖：assets/images/shot_4.5.4_gpt_v1.png；未將其他機位輸入生成。
- 輸出：assets/images/shot_4.5.4_gpt_v3.png；1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-c835746f-7856-4763-b524-dc466c8dec23.png
- 完整解碼與來源副本SHA256通過：a6ea78fe716f337eb1aa59b89e2c64dc0a0286e343ecc52caea7dbd49c7f0a9e。
- 目視：頭部比v1更朝畫左且下巴放低，手勢與主要背景保留；眼球仍略偏上，尚不能判定完全達成看向較矮Amy的要求，待使用者評鑑。保留v1/v2，未改正式採用設定。
- 完整實際prompt：
```text
編輯這張既有分鏡圖，修正標哥「與鏡外 Amy 對視」的頭部姿態與眼神。原圖仍像抬頭向左後方側瞥，這正是必須修正的問題，不要只把瞳孔移動一點點。

場面關係：Amy 站在畫面左側鏡外，與標哥面對面交談，Amy 較矮，眼睛低於標哥。標哥應將注意力直接放在面前這位 Amy 的眼睛上。
請將標哥整個頭部連同安全帽與眼鏡，比原圖再明顯向畫面左側轉約20度，呈現朝左的四分之三偏側臉；下巴稍微放低，消除抬頭仰望。鼻尖與臉部朝向左側鏡外的 Amy。雙眼自然沿鼻尖所朝的方向，略向下看著 Amy 的眼睛；瞳孔在眼眶內保持自然，不要眼球向側邊極端轉動，不回望後方，不看左上方、不看背景工具架、不看鏡頭。表情仍是開心向她解釋成果的爽朗笑容，保留原本張嘴說話的感覺。讓觀者清楚看出他正在專注與左側較矮的對話者對話，而非眼睛側瞟、頭部朝另一個方向。

只重繪完成上述轉頭、略低頭及自然對視所需的頭部、帽子、眼鏡、眼睛與頸部銜接。保留標哥相貌、灰白鬍鬚、人物尺度和身體站位、灰色工作服、兩手比劃姿勢、手指、背景物件及其佈局、光影、相機方向和原畫框。不要移動相機、拉遠鏡頭、鏡像或重新構圖。Amy 全程在畫外，不加入任何人物或道具。
輸出一張與原圖相同比例的16:9彩色分鏡圖，無字幕、標題、標記或浮水印。
```


## 2026-10-20 shot_4.5.3 — GPT v2（綠籃比例與標籤朝向修正，待評鑑）

- 使用者授權：綠色籃子比例不對，塑料標籤須與金屬標籤平行。
- 工具／供應商：內建 image_gen／OpenAI；具體模型版本及費用未知；本輪共 3 次局部編輯，前兩次未修到位，第三次另存 v2。
- 專案輸出：assets/images/shot_4.5.3_gpt_v2.png；1672×941 RGB PNG。
- 驗證：目視修正結果、完整解碼成功、來源與副本 SHA256 一致：6e99185e63c22939eb5126578af6c209403b9066cfc8b714249a62699cb4d0bb。
- 保留 v1；未改白模、scene_plan、asset_manifest 或正式採用。

### 本輪第 1 次編輯
- 原始輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-d3db4223-5366-4c83-9f19-4d5d82af0601.png
- 目視結果：未通過：綠籃格柵略有改變，但塑料標籤仍左高右低，與金屬標籤方向相反；僅保留工具原始輸出，未作為專案 v2。
- 實際參考圖（有序）：
  1. D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.5.3_gpt_v1.png
- 完整實際 prompt：
```text
以圖 1 shot_4.5.3_gpt_v1.png 為編輯底圖，只修正畫面最右下方的綠色塑膠料件籃及其「塑料」標籤。這是局部幾何與透視修正。

以旁邊白色「金屬」料件籃為比例和方向基準：將綠色籃修正為同類型、合理長寬高比例的硬質矩形周轉籃，保留綠色、鏤空格柵、厚實上框與角柱。綠籃位於白籃右後方，尺度符合這個深度，不能呈現被拉高、壓窄、扭曲或張開的箱體。維持其原有右後方位置，以及畫面右邊和下邊的自然裁切，不為了展示完整籃子而改構圖。

關鍵修正：綠籃的正面必須與白色「金屬」籃的正面平行、朝向一致，不可一個往左斜、一個往右斜。綠籃上口前緣、正面橫框、格柵的橫向邊線要與白籃相應邊線呈現一致的透視方向，箱體開口、深度與厚度合理連續。

保留白籃與「金屬」標籤原樣。將綠籃「塑料」標籤平整貼在修正後的正面，標籤的上邊、下邊及中文字基線在畫面中都要與「金屬」標籤的相應邊線平行，傾斜方向及角度一致；不可維持原圖兩標籤向相反方向傾斜的狀態。兩張標籤使用相近的矩形長寬比例與字級，仍清楚寫著「金屬」與「塑料」，不新增任何字。標籤必須隨籃子表面貼合，不懸浮、不只旋轉一張平面紙來掩蓋錯誤箱體透視。

完整保留標哥的臉、表情、眼鏡、鬍鬚、黃色工安帽、服裝、姿勢、人物比例與所在位置；保留白籃、紙板堆、束帶、貨架、工具板、紙箱、燈光、色調、景深和原來取景。除了綠籃及其標籤這個局部外，其餘畫面不重設、不移動、不拉近或拉遠。

輸出一張與原圖相同的 16:9 彩色分鏡圖，不新增字幕、浮水印、外框或其他人物。
```

### 本輪第 2 次編輯
- 原始輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-8aef4cc8-ba40-4fbe-873b-058cd047a6f0.png
- 目視結果：未通過：即使指定兩標籤左低右高，模型仍保留相反朝向；僅保留工具原始輸出，未作為專案 v2。
- 實際參考圖（有序）：
  1. C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-d3db4223-5366-4c83-9f19-4d5d82af0601.png
- 完整實際 prompt：
```text
請局部修改圖 1 右下角的綠色籃子，修正仍然錯誤的正面朝向。不要改任何人物、白籃或背景。

目前白籃「金屬」標籤的右上角高於左上角，上下邊線都是「左下往右上」斜升；但綠籃「塑料」標籤卻向相反方向斜降，這就是必須修掉的錯誤。

請重新構造綠籃的朝向，使它貼有標籤的正面與白籃貼有標籤的正面朝向完全相同，兩者是平行擺放的一對長方形籃子，而不是互相垂直或向兩側張開。綠籃仍位於白籃右後方、部分在畫面右邊外，大小比例以白籃同型籃為準，深度合理，不拉高壓窄。

請特別落實下面的可見幾何結果：
綠色籃子貼標籤的整個正面，其上橫框、下橫框以及「塑料」標籤的上邊與下邊，都必須像白色「金屬」標籤一樣，從畫面左側較低的位置延伸到右側較高的位置。塑料標籤右上角必須比左上角高，右下角必須比左下角高，四角及文字基線的傾斜角度與金屬標籤一致。不要再畫成左高右低。依這個正面重建綠籃的側面、箱口和格柵，使標籤真正貼在平整正面上，不只是把紙牌單獨旋轉。

「金屬」白籃是完全固定的方向基準，不要為了遷就綠籃而改白籃或金屬標籤。只保留兩個文字「金屬」「塑料」，字級和標籤比例相近。

人物、表情、五官、衣服、紙堆、貨架、工具、白籃、鏡位、取景、光影及色調全部沿用圖 1。只改綠籃與塑料標籤。輸出單張16:9圖片，不加其他文字或浮水印。
```

### 本輪第 3 次編輯
- 原始輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-8f186853-58f6-4039-b269-23473d35bec5.png
- 目視結果：本次修正版：綠籃依白籃形狀與朝向重建，兩籃正面同向，塑料／金屬標籤上下邊與文字基線均朝右上方延伸，目視近似平行；綠籃長寬高觀感更接近白籃，右緣自然出框。人物表情、取景及其餘場景大致保留；屬 AI 重繪，未作像素級不變或精確幾何量測宣稱。
- 實際參考圖（有序）：
  1. D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_4.5.3_gpt_v1.png
- 完整實際 prompt：
```text
Reference image: shot_4.5.3_gpt_v1.png.

Edit this image. Completely REPLACE the green crate at the lower right. Make the new green crate an identical duplicate of the ivory crate beside it: identical rectangular shape, width-to-height ratio, lattice, and most importantly IDENTICAL ROTATION. Translate that duplicate to the right, without rotating it, and color it green. Keep it on the same row as the ivory crate with their front faces coplanar. Much of the green duplicate may extend outside the right edge of the picture. This is correct; do not rotate or compress it just to fit.

The two front top rails must form one straight rising diagonal across the image, rising from lower left to upper right. The two front label panels must be parallel parallelograms with identical slopes. The existing ivory crate's label 金屬 slopes upward to the right. The new green crate's label 塑料 must ALSO slope upward to the right, with its right corners visibly HIGHER than its left corners. Use the white crate front as a literal geometric template for the green front. On the 1672x941 canvas, the new green label can have corners approximately top-left (1545,815), top-right (1655,791), bottom-right (1655,876), bottom-left (1545,900). Its text baseline also rises toward the right, matching 金屬. It is attached flat to the crate. Keep the Chinese text exactly 金屬 and 塑料.

Preserve the man, face, expression, hardhat, clothing, crop, ivory crate, cardboard, shelves, tools and lighting. Only reconstruct the green crate and its label. Produce one finished 16:9 image without annotations.
```


## 2026-10-20 shot_4.5.4 — GPT v4（依使用者附圖修正視線，待評鑑）

- 使用者授權：眼神依新附圖方向重新修正；附圖方向優先於先前文字推定。
- 工具／供應商：內建image_gen／OpenAI；模型及費用未知；生成1次。
- 輸出：assets/images/shot_4.5.4_gpt_v4.png；1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-6d2623ec-760b-4c4b-9a83-347bf1f2a411.png
- 完整解碼與來源副本SHA256通過：febef6bd188648a7c861db5b568e618186c4dde5d917c8b50c955f4dcec5e2d1。
- 目視：面部朝向與瞳孔相對位置更接近附圖，消除前版極左側瞥；雙手姿勢與主要背景保留，笑容開口較參考大，衣領／扣子有局部重繪。待使用者確認，未改正式採用版本。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/assets/images/shot_4.5.4_gpt_v3.png
  2. C:/Users/user/AppData/Local/Temp/codex-clipboard-5476b473-8ab5-457a-8541-7b0d70b43974.png
- 完整實際prompt：
```text
請對圖1進行局部編輯，使用圖2精確指定標哥的眼神與頭部方向。
圖1：待修正的16:9分鏡，提供唯一的構圖、人物身體、雙手、場景與光影。
圖2：使用者指定的正確頭眼方向近照，只作頭部姿態、眼球方向和注視感的參考，不能採用圖2的取景、背景或裁切。

將圖1標哥的頭眼朝向調整成圖2的樣子：請直接觀察並匹配圖2兩顆虹膜、瞳孔在眼白中的相對位置、眼瞼開合、雙眼共同注視方向，以及臉部朝向、鼻尖方向與頭部微傾的關係。圖2是方向的最高依據，不要再沿用圖1向極左邊側瞥的眼睛。圖2中眼球較居中、面部較朝向觀者，眼神自然落向畫面左前方的對話者；請把這種自然對視感轉移到圖1。需要時一起調整臉部旋轉角度、帽子、眼鏡與頸部銜接，使頭眼一致，而不是只平移瞳孔。保留標哥的相貌與開心說話的笑容，不誇大眼睛。

圖1中的人物頭部大小、人物站位、身體、衣服、左右手及全部手指姿勢、紙板堆、左側工具板、右側貨架、材質、光線、景深及16:9邊界裁切均保留。只修改達成圖2頭眼方向所需的局部。不要把圖2的背景搬入，不貼入方形照片，不產生拼貼，不添加Amy或任何其他人物，不改相機、不縮放、不鏡像。
輸出單張16:9彩色分鏡圖，不加文字或浮水印。
```



## 2026-10-20 shot_4.5.5 — GPT v1（待評鑑）

- 使用者授權：使用上一輪三圖prompt，以GPT生圖並存入assets/images。
- 工具／供應商：內建image_gen／OpenAI；模型及費用未知；生成1次。
- 輸出：assets/images/shot_4.5.5_gpt_v1.png；1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-abb73211-7d81-4f41-bfb5-dae21250f4b6.png
- 完整解碼與來源副本SHA256通過：6f1e0233b8c22fc739eb528d53ccc3623d81d0e875457c070c13ef498669a216。
- 目視：Amy戴黃色工安帽、灰色西裝且無反光背心，朝畫右微笑說話，雙手在畫外；紙板堆與貨架及回收桶保留。眼神略向右上，下巴下收不明顯；人物軀幹較窄且頭部尺度／肩膀位置偏離blocks，帽頂完整入鏡。待評鑑，未追加生成或改採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_amy_ms_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_amy_ms_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 完整實際prompt：
```text
參考圖說明：
圖 1 cam_amy_ms_15deg_empty_gpt_v3.png：廠務現場的場景外觀參考圖。
圖 2 cam_amy_ms_15deg_block_blender.png：Amy 單人中景的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、人物佔位、頭部尺度、肩膀位置、背景配置與邊界裁切。不得拉遠鏡頭、擴展畫面、放大頭部或補出畫外身體。底圖已有的身體裁切優先，不為呈現完整腰部或雙手而重新構圖。

將紅色定位人物替換為圖 3 的 Amy，保留棕色微捲短髮、綠色眼睛、灰色西裝外套、捲起的袖口與白色襯衫。本場 Amy 戴黃色工安帽，不穿反光背心；工安帽自然戴在頭上，短髮從帽緣兩側與後方露出。帽頂若超出原畫框，依原取景自然裁切，不縮小人物來容納帽子。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留紅色方塊外觀。

場景材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留 Amy 身後綁束的瓦楞紙板堆、金屬貨架、材料收納盒、管材與盤繞線材，以及畫面左緣可見的回收桶與雙色牆面。背景依人物自然遮擋，不搬移紙板堆或重新排列貨架物品。人物接受與場景一致的暖色自然光及環境光，工安帽簷下、髮際與衣領保留自然陰影。

畫面描述：
這是一張 60mm、近站姿眼高、15 度微側的 Amy 單人中景，取景沿用圖 2。Amy 位於畫面中央偏左，身體保持原有站位，朝向畫面右側鏡外的標哥。她的臉部與雙眼共同朝向標哥，注視右前方對話者的眼睛；視線自然集中，不看鏡頭、不向右後方貨架側瞥，也不誇張仰望。Amy 眉毛略提，眼神明亮而肯定，嘴角上揚、嘴巴微張，呈現正要說「沒錯！」的瞬間。下巴開始輕輕下收，定格在肯定點頭的起始姿態，不低頭看地面。雙肩放鬆，上臂靠近身側，雙手尚未抬起指向走道，沿用底圖下緣的自然裁切，不刻意補出畫外手部。她的神情帶著對標哥成果的認同與讚許。焦點落在 Amy 的臉部，背景適度柔化，仍能辨識紙板堆、貨架與回收桶。除上述工安帽置入、頭部微調、視線與表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有 Amy 一人，標哥保持在畫外。走道位於本鏡前側畫外，不為展示走道而改變取景。不加入堆高機、其他人物、多餘手臂、統計牌、字幕、E 或 S 字樣、數字圖卡、標題、對話框或浮水印。
```



## 2026-10-20 shot_4.5.5 — GPT v2（胸部以上近景，待評鑑）

- 使用者授權：再切近景一些，胸部以上。
- 工具／供應商：內建image_gen／OpenAI；模型及費用未知；生成1次。
- 唯一編輯底圖：assets/images/shot_4.5.5_gpt_v1.png。
- 輸出：assets/images/shot_4.5.5_gpt_v2.png；1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-019908f5-4a5f-4445-854e-a4c4e3a607d8.png
- 完整解碼與來源副本SHA256通過：b3a5f013e888c552489e28dea4c5aeff7253177f008e178a34b8d85a0a4c7d57。
- 目視：已收緊為胸部以上，腰部／袖口／手肘未入鏡，朝右視線與微笑大致保留；帽頂被上緣略裁切，背景有局部重繪，非像素級裁切。保留v1，未改採用設定。
- 完整實際prompt：
```text
編輯這張Amy分鏡圖，只將取景收緊為「胸部以上近景」。
在同一拍攝方向與透視下向Amy推近取景，畫面下緣切在胸口中段，僅呈現胸部以上、雙肩、頸部、頭部與黃色工安帽；不再看到腰部、西裝下襬、手肘、袖口或雙手。頭部與肩膀在畫面中明顯放大，保持自然比例。工安帽完整保留，帽頂上方留少量呼吸空間。Amy位於畫面中央偏左，右側保留看向鏡外標哥的視線空間，整體仍為16:9橫幅。
保留原圖Amy的相貌、棕色短髮、綠色眼睛、黃色工安帽、灰色西裝與白色襯衫、開心說話的表情、嘴巴開合、頭部角度及原有朝畫右的視線。不得改變臉部朝向或動作，不新增手勢。保留原圖的暖光、色調、動畫風格與景深。
背景應隨同取景等比例收緊，只保留新畫框內可見的原有紙板堆、貨架與牆面；不為保留所有背景物件而移動它們，不新增物件，不鏡像或改變拍攝方向。只有Amy一人，不加文字、字幕、圖卡或浮水印。輸出一張16:9彩色分鏡圖。
```


## 2026-10-20 shot_1.3.1 — GPT v1（幻想購物台，待評鑑）

- 使用者授權：使用前一則三圖 R2I prompt 生成圖片，存入專案 images 資料夾。
- 工具／供應商：內建 image_gen／OpenAI；具體模型版本及費用未知；本輪生成 1 張。
- 輸出：assets/images/shot_1.3.1_gpt_v1.png；1672×941 RGB PNG。
- 原始輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-d57b100f-7dd4-4406-a453-fe739f716ff0.png
- 驗證：完整解碼成功、來源與副本 SHA256 一致：d27c4882f8728c44809a46dacba0f52e65d944912d74c7f31056e0b4f1afc01c。
- 目視：主管單人站在展示台後、正面腰上構圖、直視鏡頭誇張露齒笑；雙手托扶一個白罐綠蓋膠囊罐，標籤朝鏡頭、金色光暈與閃光呈現；ESG／濃縮膠囊及三個圖徽可辨，舞台主要配置保留。嘴巴張開程度較 prompt 的微張更大、雙手向前展示；無額外人物或疊字。不是像素級構圖或相機焦距驗證。
- 未修改 scene_plan、CLP 或 asset_manifest；未正式採用。
- 有序參考圖：
  1. D:/Dropbox/kj-om-projects/course-51-esg/clp/loc_tvshow.png
  2. D:/Dropbox/kj-om-projects/course-51-esg/clp/char_supervisor.jpeg
  3. D:/Dropbox/kj-om-projects/course-51-esg/clp/prop_capsules.png
- 完整實際 prompt（逐字沿用前一則交付）：
```text
3D Pixar animation style, stylized character design, warm studio rim lighting, 8k render.

參考圖：
圖 1：D:\Dropbox\kj-om-projects\course-51-esg\clp\loc_tvshow.png
幻想電視購物攝影棚（loc_tvshow），提供舞台配置、展示台、背景裝飾、材質與燈光。

圖 2：D:\Dropbox\kj-om-projects\course-51-esg\clp\char_supervisor.jpeg
主管（char_supervisor）人物設定圖，提供五官、髮型、身形與服裝；不沿用參考圖的憂愁表情或多視角拼貼。

圖 3：D:\Dropbox\kj-om-projects\course-51-esg\clp\prop_capsules.png
ESG 濃縮膠囊（prop_capsules）道具設定圖，提供同一藥罐的不同視角；本鏡只出現一罐，採用圖中左側的正面包裝。

畫面：
幻想中的電視購物節目現場，只有主管一人入鏡。他居中站在圖 1 的白金色弧形展示台後，面向鏡頭，雙眼直視觀眾，眉毛上揚、雙頰抬起，露出燦爛誇張的露齒笑容，嘴巴微張，呈現購物台王牌主持人正要熱情開講的瞬間。表演帶有綜藝節目的荒誕喜感與過度自信。

主管外觀嚴格沿用圖 2：蓬鬆略凌亂的黑色短髮、濃眉、明顯鼻形與淡淡鬍渣，穿捲起袖口的淺藍色襯衫、鬆開的棕色領帶。保留角色辨識特徵，將原本焦慮的神情改為興奮推銷的笑容。

主管雙手將單一藥罐舉至胸前，一手托住罐底，另一手扶住側面，罐身直立、正面標籤朝向鏡頭。雙手、手指與完整藥罐清楚入鏡，手指不遮住產品名稱，藥罐不遮住臉部。保留圖 3 的白色塑膠罐身、綠色直紋旋蓋、綠色金邊「ESG」字樣、繁體中文「濃縮膠囊」，以及綠葉、藍色人物、金色盾牌三個圓形徽章。罐身周圍帶柔和金色光暈與少量閃光，仍能清楚辨識包裝；不把罐身改成金屬金色，不複製成三罐。

背景沿用圖 1 的青綠色中央背板、地球、白金色 ESG 立體字、金色上升箭頭，以及洋紅與青藍側板。保留展示台與背板的前後關係，依中景自然裁切舞台，背景文字允許被人物遮擋。場景是絢麗的購物攝影棚，呈現把 ESG 誤當速效萬靈丹的幻想氣氛。

攝影：
35mm，正面微仰角中景，主管居中，取景約腰部以上，下緣帶入展示台桌面，頭頂保留適量空間。臉部、雙手與藥罐構成主要視覺焦點，中等景深，背景稍柔化但仍可辨識購物台佈景。高調飽和舞台光搭配暖金色輪廓光，臉部與產品標籤明亮清晰，光暈不過曝。

輸出：
一張 16:9 彩色分鏡圖。保留場景與包裝原有文字，不新增字幕、促銷標語、價格、電話、對話框或浮水印。不要加入 Amy、觀眾、其他主持人、多餘手臂或人物設定圖拼貼。
```


## 2026-10-20 shot_4.5.6 — GPT v1（指定MCU機位，待評鑑）

- 使用者授權：逐字使用最新四圖prompt，改用cam_biao_mcu_15deg構圖，以GPT生成一張並保存。
- 工具／供應商：內建image_gen／OpenAI；模型及費用未知；生成1次。
- 輸出：assets/images/shot_4.5.6_gpt_v1.png；1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-87e4dfaf-dee6-4f5b-a53b-e89108f6d3cf.png
- 完整解碼與來源副本SHA256通過：e44eac536dd7795d3b791b193661a9f8665a3a9645eb6d376ba872fea594c7c8。
- 目視：標哥胸部以上、黃色工安帽、灰色工作服、微笑與左前方對視呈現，雙手畫外；頭眼方向接近指定近照。人物頭肩輪廓、肩膀位置及背景遮擋未精確沿用blocks，帽頂被上緣裁切；背景工具與紙板細節重繪。待使用者評鑑，未追加生成或改正式採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_mcu_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_biao_mcu_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_biaoge.jpeg
  4. C:/Users/user/AppData/Local/Temp/codex-clipboard-5476b473-8ab5-457a-8541-7b0d70b43974.png
- 完整實際prompt：
```text
參考圖說明：
圖 1 cam_biao_mcu_15deg_empty_gpt_v3.png：廠務現場的場景外觀參考圖。
圖 2 cam_biao_mcu_15deg_block_blender.png：標哥胸部以上中近景的構圖底圖。
圖 3 char_biaoge.jpeg：標哥人物參考圖，對應圖 2 戴黃色工安帽的藍色定位人物。
圖 4 codex-clipboard-5476b473-8ab5-457a-8541-7b0d70b43974.png：使用者指定的標哥頭部與眼神方向參考，只提供自然對視的方向，不採用其背景或取景。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、人物佔位、頭部尺度、肩膀位置、背景配置與邊界裁切。維持胸部以上中近景，不拉遠鏡頭、不擴展畫面、不縮小人物，也不補出腰部或雙手。工安帽與畫面上緣的裁切關係沿用底圖，不為露出整頂帽子而重新構圖。

將藍色定位人物替換為圖 3 的標哥，保留黃色工安帽、灰黑短髮、濃眉、細金屬框眼鏡、灰白短鬍鬚、灰色工作服、淺灰肩部條帶與米色內搭。人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留方塊外觀。

頭部與雙眼的對視方向參考圖 4，保留其臉部朝向、頭部微傾與瞳孔在眼白中相對位置所形成的自然注視感。標哥正在看畫面左前方鏡外的 Amy，不是向左後方回望。不要只把瞳孔推到左側眼角，也不要將圖 4 的頭部大小或取景套入本鏡。頭部轉向與眼球方向應協調，保持自然對話的感覺。

場景材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留本鏡可見的左側工具掛板、下方瓦楞紙板堆，以及右側貨架、收納盒與材料罐。背景依人物自然遮擋，不補出被身體擋住的物件，不重新排列貨架或搬移紙板堆。人物接受與場景一致的暖色自然光及環境光，保留帽簷下、眼鏡、鬍鬚與衣領的自然陰影。

畫面描述：
這是一張 75mm、近站姿眼高、15 度微側的標哥單人中近景，取景沿用圖 2。標哥位於畫面中央偏右，只呈現胸部以上，身體下緣依底圖裁切。頭部與雙眼朝向左前方鏡外的 Amy，對視方向依圖 4。他帶著溫暖、坦率而樸實的笑容，眉眼放鬆，嘴巴微張，呈現正要回答「是啊，維護安全，人人有責嘛！」的瞬間。表情傳達這是自己理所當然會做的事，尚未進入後段疑惑或意外領悟的反問。雙肩自然放鬆，雙手保持在畫外，尚未抬手抓安全帽，不比劃收支，也不比讚。工安帽正常戴在頭上，沒有被抬起或移位。焦點落在標哥的眼睛與臉部，背景柔化，仍可辨識工具板、紙板堆與貨架。除上述頭眼方向與表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有標哥一人，Amy 保持在畫外。不加入其他人物、多餘手臂、字幕、ESG 字樣、標語、統計牌、圖表、對話框或浮水印。
```


## 2026-10-20 shot_1.3.1 — GPT v2（原始三圖重作，待評鑑）

- 使用者授權：「這張圖不對，重作」。v1 被否決，未指定具體不符部位；已提出可選澄清並等待，生成前尚未收到補充。
- 本輪假設：依既有分鏡與三張原始 CLP 重新生成，著重原主管臉型／年齡感、正面站姿、胸前持罐；這是暫定重作方向，非使用者已確認的問題診斷。
- 工具／供應商：內建 image_gen／OpenAI；具體模型版本及費用未知；本輪生成 1 張。
- 輸出：assets/images/shot_1.3.1_gpt_v2.png；1672×941 RGB PNG。
- 原始輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-9008d098-a1fc-4d97-82d2-6ea48a003b0c.png
- 驗證：完整解碼成功、來源與副本 SHA256 一致：ac2729790f5609951e1800601b87a70f12cf8a6b7fe8ec511b370cd3cac9f310。
- 目視：主管頭部與軀幹較 v1 正面端正，笑嘴張開幅度縮小、長臉與皺紋年齡感較明顯；雙手胸前托扶單一白罐綠蓋藥罐，標籤與金色光暈可見，展示台與青綠／洋紅舞台保留。是否符合使用者所指問題仍待評鑑，不宣稱已解決未知不符原因。
- 保留 v1；未改 scene_plan、CLP、asset_manifest 或正式採用。
- 有序參考圖：
  1. D:/Dropbox/kj-om-projects/course-51-esg/clp/loc_tvshow.png
  2. D:/Dropbox/kj-om-projects/course-51-esg/clp/char_supervisor.jpeg
  3. D:/Dropbox/kj-om-projects/course-51-esg/clp/prop_capsules.png
- 完整實際 prompt：
```text
3D Pixar animation style, stylized character design, warm studio rim lighting, 8k render.

重新製作 shot_1.3.1 的單張彩色電影分鏡，使用以下三張原始參考重新構圖。

圖 1：D:\Dropbox\kj-om-projects\course-51-esg\clp\loc_tvshow.png
loc_tvshow，幻想電視購物攝影棚。提供既有白金色弧形展示台、青綠背板、地球與 ESG 立體字、上升箭頭、洋紅與青藍側板的位置關係、材質及舞台光。

圖 2：D:\Dropbox\kj-om-projects\course-51-esg\clp\char_supervisor.jpeg
char_supervisor，唯一人物的身份與服裝參考。嚴格保留這位中年東亞主管的偏長臉型、下顎與下巴形狀、濃黑眉毛、鼻形、眼睛比例、耳形、黑色短髮、淡鬍渣和年齡感。沿用淺藍色捲袖襯衫、鬆開的棕色領帶。圖中的悲傷表情只改成熱情笑容，不因此變成另一張更年輕、圓臉、過度美化的臉。不採用設定圖的拼貼、多視角、背景或展示姿勢。

圖 3：D:\Dropbox\kj-om-projects\course-51-esg\clp\prop_capsules.png
prop_capsules，同一個藥罐的多角度設定，不是三個不同產品。本鏡只出現一個藥罐，白色塑膠罐身、綠色直紋旋蓋，採圖中左側正面標籤，綠色金邊 ESG、繁體中文「濃縮膠囊」、綠葉／藍色人物／金色盾牌三個圓形徽章。保持參考的瓶身高寬比例，不額外加入散落膠囊。

單一瞬間的畫面：
主管正面居中站在圖 1 既有弧形展示台後，肩膀朝正前方，頭部保持端正，雙眼直接看向拍攝鏡頭。他化身綜藝感十足的電視購物主持人，雙頰抬起、眼神興奮、露齒燦笑，嘴唇略分開，正要充滿自信地介紹商品。表情誇張而有喜感，仍保持圖 2 的五官結構，不張成大喊的圓形嘴、不歪頭。

主管雙手在自己胸前托舉一個藥罐，一手托住底部，另一手扶住側面，手肘自然彎曲靠近身體。藥罐位在胸部前方、下巴以下，正面朝鏡頭，手指避開標籤。不要把手臂向鏡頭伸直、不要利用近大遠小放大藥罐。臉部、兩隻手與整個藥罐同時清楚可見，比例自然。罐子周圍有柔和金色光暈與少量星芒，標籤和輪廓清晰，白罐綠蓋不變成金屬金罐。

構圖與場景：
35mm，正面微仰角中景，約腰部以上，頭頂留適量空間，主管位於畫面中央，展示台桌面與少量白金色前緣出現在畫面下方。保留圖 1 中央背板和展示台的原有空間關係；攝影機只是向中央主持位置收近取景，不重新設計一個舞台。人物可自然遮住背景部分 ESG 字樣，舞台左右裝飾依中景裁切，不為塞進所有物件而拉成全景。僅主管一人入鏡，沒有 Amy、觀眾或其他主持人。

高調絢麗、暖金色與青綠／洋紅舞台燈光，臉部、手部與產品受光一致；中等景深，臉與包裝清晰，背景稍柔化。畫面呈現主管把 ESG 當速效萬靈丹的荒誕購物台幻想。

輸出一張 16:9 彩色分鏡圖。只保留參考場景與包裝本來的文字，不增加字幕、促銷字卡、價格、電話、對話框或浮水印。不出現多餘手臂、重複人物、重複藥罐或設定圖拼貼。
```


## 2026-10-20 shot_4.5.7 — GPT v1（待評鑑）

- 使用者授權：使用上一輪完整四圖prompt，以GPT生圖並存入assets/images。
- 工具／供應商：內建image_gen／OpenAI；模型及費用未知；生成1次。
- 輸出：assets/images/shot_4.5.7_gpt_v1.png；1672×941 RGB PNG。
- 來源：C:/Users/user/.codex/generated_images/01a157ec-764d-7b12-8d88-60c90bdd42f8/exec-27b899ac-9db7-411a-94d7-3b17825df0f1.png
- 完整解碼與來源副本SHA256通過：f1761015442f7ff938e846c909197ed49837558e01576bc3285c3d0ad4ac2f25。
- 目視：Amy左側面向鏡頭雙手比讚，標哥右側微笑，兩頂工安帽完整入鏡，Amy無反光背心。兩人較底圖靠近中央、間距縮短及身高差縮小，標哥眼神偏左上而非明確注視Amy臉部；背景細節有重繪。待評鑑，未追加生成或改正式採用設定。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/factory/cameras/cam_twoshot_ms_level_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_biaoge.jpeg
- 完整實際prompt：
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt_v3.png：廠務現場的場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：Amy 與標哥雙人中景的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 左側紅色定位人物。
圖 4 char_biaoge.jpeg：標哥人物參考圖，對應圖 2 右側藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其拍攝方向、取景、透視、兩人站位、彼此距離、大小比例、背景配置與邊界裁切。維持 Amy 在左、標哥在右，不交換左右、不將兩人移向畫面中央，不拉遠鏡頭或補出畫外身體。人物下緣沿用底圖裁切，不為露出完整腰部而重新構圖。

將左側紅色定位人物替換為圖 3 的 Amy，保留棕色微捲短髮、綠色眼睛、灰色西裝外套、捲起的袖口與白色襯衫。Amy 戴黃色工安帽，不穿反光背心；短髮自然從帽緣兩側及後方露出。

將右側藍色定位人物替換為圖 4 的標哥，保留黃色工安帽、灰黑短髮、濃眉、細金屬框眼鏡、灰白短鬍鬚、灰色工作服、淺灰肩部條帶與米色內搭。兩人的工安帽自然貼合頭部，不放大帽子；保留底圖頭部尺度與站位，兩頂帽子完整位於畫框內。

人物參考圖只提供外觀與服裝，不採用其展示姿態或拼貼構圖，不保留紅藍方塊外觀。

場景材質、物件外觀、風格與光影採用圖 1，空間配置仍依圖 2。保留兩人身後的兩堆綁束瓦楞紙板、中央間隙、金屬貨架、管材、綁束布料、盤繞線材、材料容器與工具掛板。背景依兩人自然遮擋，不補出被人物擋住的物件，不搬移紙板堆或重新排列貨架。人物接受與場景一致的暖色自然光及環境光，保留帽簷下、衣領與手指間的自然陰影。

畫面描述：
這是一張 45mm、近站姿眼高平視的雙人中景，取景沿用圖 2。Amy 位於畫面左側，標哥位於右側，保留兩人原有間距與身高差。Amy 的站位不變，上身與頭部轉向鏡頭，雙眼自然看向鏡頭中的觀眾，帶著熱情、真誠的笑容，嘴巴微張，呈現感謝標哥與第一線同仁的瞬間。調整 Amy 的肩臂、手腕與手指，讓雙手抬至胸前，兩個大拇指明確向上，其餘四指自然彎曲握攏；兩手適度分開，完整留在畫框內，不遮住臉部，不伸向鏡頭造成誇張放大，也不與標哥身體重疊。標哥雙肩放鬆，頭部與雙眼自然朝向畫左 Amy 的臉，嘴角上揚，露出受到肯定時開心而略帶靦腆的憨厚微笑；下巴輕收，呈現微微頷首致意的姿態。他的雙臂自然垂放，手部沿用原畫框的可見範圍，不跟著比讚、不抓安全帽。兩人的臉與 Amy 的雙手都清楚可辨，背景適度柔化，仍能辨識整齊的廠務暫存區。除 Amy 面向鏡頭、雙手比讚，以及標哥的視線、表情與輕微頷首調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，畫面只有 Amy 與標哥兩人。不加入其他人物、多餘手臂、堆高機、字幕、S 或 ESG 字樣、標語、統計牌、圖卡、對話框或浮水印。
```


## 2026-10-20 shot_1.3.1 — GPT v3（完整雙腿與鞋子，待評鑑）

- 使用者更正：「腳都不見」。本輪改為全身構圖，並將主管置於展示台前方，使下半身不受桌台遮擋。
- 工具／供應商：內建 image_gen／OpenAI；具體模型版本及費用未知；本輪 I2I 1 次。
- 輸出：assets/images/shot_1.3.1_gpt_v3.png；1672×941 RGB PNG。
- 原始輸出：C:/Users/user/.codex/generated_images/01a157fd-63b8-7a01-a27f-957ae00f24d5/exec-938f634f-2713-4ed8-adfb-4f98f93e9af4.png
- 驗證：完整解碼成功、來源與副本 SHA256 一致：06dfc01476c72a900a2c0120dfd6dd19b03d327aa81a3430a27b28f2a5033822。
- 目視：頭頂、腰部、完整雙腿與兩隻棕色皮鞋全部入鏡；雙腳落地、有接觸陰影，鞋下仍有地板留白；展示台位於身後，沒有遮住腿部。主管笑容、藍襯衫棕領帶、胸前單罐白綠包裝及暖色舞台保留；取景拉遠後標籤細字較小。人物上下留白未精確依 prompt 百分比，但本次完整腳部需求已呈現。
- 原 scene_plan 仍記中景／展示台後；本版依最新要求作全身／展示台前候選，採用後再同步後續製作。未改 manifest，保留 v1／v2。
- 有序參考圖：
  1. D:/Dropbox/kj-om-projects/course-51-esg/assets/images/shot_1.3.1_gpt_v2.png
  2. D:/Dropbox/kj-om-projects/course-51-esg/clp/char_supervisor.jpeg
  3. D:/Dropbox/kj-om-projects/course-51-esg/clp/loc_tvshow.png
- 完整實際 prompt：
```text
修改圖 1，將原本腰部以上的取景改成完整全身鏡頭，明確呈現主管的雙腿與兩隻鞋。

參考圖：
圖 1：D:\Dropbox\kj-om-projects\course-51-esg\assets\images\shot_1.3.1_gpt_v2.png
編輯底圖。保留主管身份、笑容、上半身服裝、雙手胸前托扶單一膠囊罐的動作、藥罐包裝與金色光暈、舞台風格與燈光。
圖 2：D:\Dropbox\kj-om-projects\course-51-esg\clp\char_supervisor.jpeg
只補充主管完整身形、棕色長褲、棕色皮帶與棕色皮鞋的外觀及自然上下身比例；不採用其憂愁表情或拼貼構圖。
圖 3：D:\Dropbox\kj-om-projects\course-51-esg\clp\loc_tvshow.png
提供拉遠後可見的同一舞台、地板與弧形展示台外觀。

必要修改：
把鏡頭明顯拉遠，主管從頭髮頂端到左右鞋尖、鞋底全部入鏡。主管正面居中站在展示台前方的舞台地板上，展示台留在他的身後，讓雙腿沒有任何桌台或其他物件遮擋。畫面最前方不要再有橫跨下半身的櫃台。不要把桌台變透明，也不要讓腿穿過桌子。

主管頭頂約在畫面高度的 10%，鞋底約在 87%，下方留出約 13% 可見地板。必須看見腰部、臀部、兩條完整褲管、膝部、腳踝，以及兩隻完整棕色皮鞋。雙腳自然分開、穩穩接觸地面，有接觸陰影，身體四肢比例沿用圖 2。不能只延長上半身或把腰部以下藏在台後，不能截斷膝蓋、腳踝或鞋尖。

主管繼續看鏡頭、興奮微張嘴露齒笑，雙手在胸前展示同一白罐綠蓋 ESG 濃縮膠囊；罐子大小相對人體合理，不能為保持字體尺寸而放大產品。其餘沿用圖 1，只為全身取景調整相機距離與人物相對展示台的站位。背景中央 ESG 舞台與原有裝飾保留。

輸出一張 16:9 橫幅彩色全身分鏡圖。只有主管一人，不增加字幕、價格、電話、浮水印或其他人物。
```


## 2026-10-20 supervisor_office — cam_supervisor_ots_amy 空景 GPT（待評鑑）

- 流程：kj-cinematic 場景機位外觀素材局部續作；依 skills/kj/blender-view-restyle.md。使用者指定單張底圖與原始美術參考，沒有既有本機位 GPT 成果；專案未找到 checkpoint／partial_progress 檔，不補造過往核准狀態。
- 工具／供應商：內建 image_gen／OpenAI；具體模型版本及費用未知；本輪 1 次 I2I。
- 輸出：references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_empty_gpt.png；1672×941 RGB PNG。
- 原始輸出：C:/Users/user/.codex/generated_images/01a1586a-2ba2-7d70-8f63-dbf5215624c3/exec-0ca02108-bc26-4825-9101-22d96f9af007.png
- 驗證：來源與副本均完整解碼；SHA256 相同：53e396e379714162b42ec278676bb6b339d77d3821aef05bf3f1e2177292bbe9。
- 目視：已逐張對照底圖、參考圖與成品：公告板、藍灰高背椅、牆角、窗台、桌面、兩份報告、文件堆及檯燈的主要位置與裁切大致保留；木紋、軟木、皮革、紙邊、暖日光及金屬反射提升，空景無人物。偏差：窗外新增遠方樓群，既有樓房外觀亦被細化；部分紙張色彩、圖釘及文件邊緣有 AI 變動，日光陰影比底圖強。未宣稱像素級幾何一致，未追加生成。
- 保留底圖、參考圖與工具原圖；未修改 Blender、其他機位、scene_plan 或 manifest，尚未確認採用。
- 有序輸入：
  1. D:/Dropbox/kj-om-projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_empty_blender.png
  2. D:/Dropbox/kj-om-projects/course-51-esg/clp/loc_supervisor_office_5.png
- 完整實際 prompt：

```text
請編輯圖 1，將這張 Blender 空景提升為圖 2 那樣的高質感動畫電影 3D 場景，參考圖 2 的材質、色彩、光影與氣氛。
圖 1 cam_supervisor_ots_amy_empty_blender.png 是唯一的取景、透視、物件配置與遮擋依據。
圖 2 loc_supervisor_office_5.png 僅供美術表現參考，不移植其構圖、家具排列、植物配置或可見範圍。
色彩與光影採用圖 2 的溫暖蜂蜜色至胡桃木棕、深藍灰皮革、米白牆面與紙張、暖橘棕軟木公告板、白色烤漆檯燈及金屬關節，窗外清爽的藍天與日間城市；右側窗戶自然日光帶暖色高光，搭配較冷的天空環境補光，柔和但具方向性的陰影。保留細膩而可信的材質與溫暖明亮的動畫電影質感，不過度泛光。

【保留本機位】
維持圖 1 的 16:9 橫幅、觀看方向、消失點、主要結構、遮擋及緊裁切。這是從訪客側向主管座椅看的桌面近距離視角，不是圖 2 的整間辦公室全景。
保留圖 1 左側大型木框公告板、其上每張紙張與便條的數量、位置、大小與圖釘；公告板頂部與左側被畫框裁切的方式不能改變。中左深藍灰高背椅仍保持既有位置、尺度、背靠主要輪廓與桌面遮擋，不能重新設計為圖 2 的遠景椅子。
中央偏右牆角柱與牆上紙張、右側窗框與窗台、窗外右緣被裁切的一座樓房，各自保持圖 1 的位置、比例與遮擋。窗外只細化既有可見建築的玻璃、窗格與天空，不新增整排城市天際線，不搬入圖 2 的中央高樓。
保留前景桌面邊界、灰色桌墊、下方兩份報告、右側文件堆、藍筆、小型灰藍矩形文具與右側白色檯燈，數量、相互位置及重疊關係沿用圖 1。
不旋轉相機、不鏡像、不拉遠或拉近，不為展示完整物件而補出被裁切部分；沒有地板、天花板、訪客椅、盆栽、矮櫃或完整百葉窗的區域，不自行新增這些內容。

【材質與細節提升】
沿用圖 1 的構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。
木質桌面和公告板木框呈現圖 2 的自然木紋與柔潤清漆高光；公告板呈現細密真實軟木顆粒；高背椅為圖 2 同色系深藍灰皮革，細緻皮紋與既有分片邊緣柔軟接縫，但不增加新分片、鈕扣或配件。
既有紙張保持各自外框、釘點、排列及主色，將白模的粗灰條細化為低對比報告線條、表格與輕微手寫筆跡，僅作自然辦公文件細節，不添加大標題或可辨識的品牌文字。紙堆保留原有體積、層數觀感、頂面方向及錯落邊界，用細薄紙邊、紙纖維和輕微頁角起伏改善質感，不能增加第二堆或改變其位置。
檯燈沿用圖 1 的燈罩外形、支臂關節、直立燈桿、底座形狀與位置，呈現霧面米白烤漆、適量金屬反射；降低白模燈罩內側死白過曝，使內緣層次清晰，同時維持亮燈觀感。
牆面微細霧面塗料、窗框細緻金屬烤漆、玻璃透光與自然反射，紋理尺度合理。所有表面保持乾燥與整潔，不加入髒污、鏽蝕或過強鏡面反光。
依圖 1 的窗口位置與物體方向重建自然日光，陰影應服從本鏡透視，不把圖 2 的光斑直接貼到本鏡。
作為後續加入人物的背景母圖，保留清楚可用的近中景材質與公告板資訊，不額外強化散景。

【空景與輸出】
零人物：不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。即使檔名含主管、Amy 或過肩，本次仍只交付空景。
只輸出一張與圖 1 相同 16:9 橫幅的高解析度完整圖片，不製作拼貼或對照圖，不加字幕、標誌或浮水印。

【本鏡畫面】
50mm 平視中景的空景版本，視線越過前景桌面看向左中景主管高背椅。公告板佔左上大半畫面，椅背在其前方；桌面向右延伸，右側厚疊文件位於白色檯燈前，檯燈燈罩位於右上中部並朝左下照射，右後方窗口在畫框右緣截斷。下緣報告與文具依底圖裁切，保持椅背、公告板、牆角、窗台、燈桿及文件堆的同一幾何關係與大小。
```


## 2026-10-20 marketing_office — v3 全景底圖 GPT 重繪 v2（待評鑑）

- 流程：kj-cinematic 場景機位外觀素材局部重繪；依 skills/kj/blender-view-restyle.md 建立首張模式。使用者指定 v3 底圖與原始美術參考；專案內未找到 checkpoint／partial_progress 檔，不補造核准狀態。
- 工具／供應商：內建 image_gen／OpenAI；確切模型版本、預估及實際費用未知；本輪 1 次圖片編輯，無重試。
- 輸出：references/scenes/marketing_office/cameras/cam_twoshot_wide_level_empty_gpt_v2.png；原生 1672×941 RGB PNG，未裁切或拉伸。
- 原始輸出：C:/Users/servi/.codex/generated_images/01a158c6-d4d1-72d1-b771-139d10bc5e8f/exec-483d9746-6c11-45a7-8b3e-7f21b001bd45.png
- 驗證：已完整解碼工具原圖與專案副本，格式／尺寸一致，兩檔 SHA256 同為 262e7316b6d66366ddd4ff4a549db4feaba4f7ee9ad76067d03f029646b6c9f1。
- 目視：已對照兩張輸入與成品。白板主要外框、十張便條及排列、桌椅／隔板配置、主要窗格、窗台盆栽及左下葉片裁切大致保留，無人物。材質更細緻，日光更接近原始美術參考；暖陽、地面高光與窗格投影比底圖強。窗外枝葉更茂密偏金黃，樓房立面與可見建築細節有所重繪；白板腳輪、桌面布料折邊、便條灰線及局部家具輪廓有細微變動，不宣稱像素級幾何一致。
- 保留原有無版本號 GPT 圖、兩張輸入與工具原圖；未修改 Blender、其他機位、scene_plan 或 manifest；尚未確認採用或指定為共用美術。
- 有序輸入：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_wide_level_empty_blender_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/clp/loc_marketing_office.png
- 完整實際 prompt：

```text
請編輯圖 1，將這張 Blender 空景提升為圖 2 那樣的高質感動畫電影 3D 場景，參考圖 2 的材質、色彩、光影與氣氛。
圖 1 cam_twoshot_wide_level_empty_blender_v3.png 是唯一的取景、透視、物件配置與遮擋依據。
圖 2 loc_marketing_office.png 僅供美術表現參考，不移植其構圖、建築／家具排列、植物配置或人物。
色彩與光影採用圖 2 的溫暖奶油白牆面與窗框、淺蜂蜜色木桌、柔和鼠尾草綠布面座椅、藍灰織物隔板、米色地磚、自然翠綠及金黃樹葉。暖金日光搭配柔和偏冷的藍天環境補光，明亮、乾淨、溫暖而細膩，不過度泛黃或泛光。

【保留本機位】
維持圖 1 的 16:9 畫幅、觀看方向、消失點、主要結構與遮擋。圖 1 的相機與圖 2 不同，必須完整保留圖 1 的構圖。
保留後牆及右牆的每一扇窗、窗框分格、立柱、窗台、牆角線、天花邊界與地磚透視。畫面左側不新增門，畫面底部不新增台階或展示台。
保留中間偏右的大型移動白板、銀白金屬邊框、橫置筆槽、兩根長支腳、底座及黑色腳輪的既有位置、尺寸、輪廓與遮擋。
白板必須保留圖 1 的全部十張彩色便條及各自灰色橫線，位置、尺寸、色彩順序不改：頂排四張為淡綠、淡藍、淡粉、淡黃；中排右側兩張為淡黃、淡粉；左側一張較低的淡藍；底排右側三張為淡綠、淡黃、淡粉。不能改成圖 2 的空白白板，不新增文字、便條或圖案。
保留白板左後方工作桌及其白色桌腳、桌下淺灰抽屜櫃、藍灰隔板、左側完整綠椅、白板下方被遮擋的綠椅與遠處局部椅背，各自數量、大小與遮擋完全遵循圖 1。不要把被白板擋住的物件搬到旁邊展示。
桌面原有厚折疊布料堆、橫排三色線錐、白色鍵盤、滑鼠、側向薄型螢幕、藍綠筆筒與筆、前側薄布樣，保持圖 1 的物件種類、位置、尺度與前後關係；布料不是書，不新增咖啡杯。
右窗台已有白盆植物與左下角被裁切的前景葉片，位置及主要輪廓保持圖 1；其餘植物以圖 1 的可見範圍為準，不搬入圖 2 更多盆栽。
不旋轉相機、不鏡像、不拉遠或拉近，不移植參考圖中本鏡畫外的物件。不為了展示完整物件而補出被裁切部分。

【材質與細節提升】
沿用圖 1 的構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。
淺木桌面有細緻自然木紋與柔潤高光；折疊布料呈現柔軟厚度、纖維與折邊，線錐呈現細密纏繞線紋；布樣有薄柔布邊，不能改為精裝書本。椅面與隔板有細密織物、合理接縫及柔軟感，維持原有外形。筆筒霧面藍綠、白色鍵帽分明，側向螢幕保持原角度與薄度。
白板為乾淨白色微光澤表面，金屬框和支腳有適度反射與細緻倒角；十張便條為薄紙，保留原有灰色線條與版面，不改成厚板。
牆與窗框為暖白霧面塗料，窗玻璃清透、有細微反射。米色地磚有精細石質微紋、低調縫線及柔和半霧面反光；保持乾燥，不做濕地、鏡面地板或大面積死白過曝。
窗外保留圖 1 的樹幹、主要樹枝、樹冠區域與樓房位置，在原有體積內細化自然薄葉、葉脈、透光與遠景層次；不新增樹木或搬動樓房。改善原有葉片的僵硬與稀疏白模感，枝葉自然連接但不擴張成遮住全部窗景的樹牆。植物不得變成球塊。
依圖 1 的窗口位置、既有光線方向與地面投影呈現暖日光與柔和陰影，陰影服從本鏡透視，不把圖 2 的光斑直接貼到本鏡。
維持合理紋理尺度與細節密度，不增加髒污或配件。作為後續加入人物的背景母圖，保留近中景清楚可用的資訊，不額外強化散景。

【空景與輸出】
零人物：不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。
只輸出一張與圖 1 一致的 16:9 高解析度橫幅完整圖片，不製作拼貼或九宮格，不加字幕、標誌或水印。

【本鏡畫面】
本鏡為辦公室內平視廣角空景，前方大面積米色地磚延伸至後牆及右牆窗戶，天花上緣保留原有裁切。白板在中央偏右，正面幾乎朝向鏡頭，十張便條完整可見；左後方工作區沿圖 1 的透視向後延伸，最近綠椅在左中景，桌面局部被白板遮擋。右側整排暖白窗框斜向遠方，白盆植物在中右窗台；左下僅露出前景植物的部分葉片。保持白板、桌沿、椅腳、窗台與地磚消失點的原有幾何關係和畫面佔比。
```



## 2026-10-20 marketing_office — v4 全景底圖 GPT 重繪 v3（待評鑑）

- 流程：kj-cinematic 場景機位外觀素材局部續作，沿用 skills/kj/blender-view-restyle.md 建立首張模式；本輪依使用者指定改用 v4 底圖及相同原始美術參考。
- 工具／供應商：內建 image_gen／OpenAI；確切模型版本、預估及實際費用未知；本輪 1 次圖片編輯，無重試。
- 輸出：references/scenes/marketing_office/cameras/cam_twoshot_wide_level_empty_gpt_v3.png；原生 1672×941 RGB PNG，未裁切或拉伸。
- 原始輸出：C:/Users/servi/.codex/generated_images/01a158c6-d4d1-72d1-b771-139d10bc5e8f/exec-52cae1da-8018-485e-a8b1-ee63fca47c89.png
- 驗證：工具原圖與專案副本均完整解碼，格式／尺寸一致，SHA256 同為 a07f9d7403271e95a841a004ca17beeeefe068c45c8a5c27c574a33505049419。
- 目視：已對照 v4 底圖、原始參考及成品。主要構圖、白板十張便條、窗格、桌椅／隔板與窗台盆栽大致保留，無人物；窗外保留較密實低位樹冠及後方高樓。偏差：樹冠局部高度／枝葉輪廓改變，遠樓立面與輪廓略有變動，天空新增白雲；葉色更金黃，日光、地面反射與葉影較強，布料折邊及白板腳輪有細節重繪。不宣稱像素級幾何一致。
- 保留原有 GPT／GPT v2、v4 底圖、參考圖及工具原圖；未修改 Blender、其他機位、scene_plan 或 manifest；待使用者評鑑。
- 有序輸入：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_office/cameras/cam_twoshot_wide_level_empty_blender_v4.png
  2. D:/kj-openMontage/projects/course-51-esg/clp/loc_marketing_office.png
- 完整實際 prompt：

```text
請編輯圖 1，將這張 Blender 空景提升為圖 2 那樣的高質感動畫電影 3D 場景，參考圖 2 的材質、色彩、光影與氣氛。
圖 1 cam_twoshot_wide_level_empty_blender_v4.png 是唯一的取景、透視、物件配置與遮擋依據。
圖 2 loc_marketing_office.png 僅供美術表現參考，不移植其構圖、建築／家具排列、植物配置或人物。
色彩與光影採用圖 2 的溫暖奶油白牆面與窗框、淺蜂蜜色木桌、柔和鼠尾草綠布面座椅、藍灰織物隔板、米色地磚、自然翠綠及金黃樹葉。暖金日光搭配柔和偏冷的藍天環境補光，明亮、乾淨、溫暖而細膩，不過度泛黃或泛光。

【保留本機位】
維持圖 1 的 16:9 畫幅、觀看方向、消失點、主要結構與遮擋。圖 1 的相機與圖 2 不同，必須完整保留圖 1 的構圖。
保留後牆及右牆的每一扇窗、窗框分格、立柱、窗台、牆角線、天花邊界與地磚透視。畫面左側不新增門，畫面底部不新增台階或展示台。
保留中間偏右的大型移動白板、銀白金屬邊框、橫置筆槽、兩根長支腳、底座及黑色腳輪的既有位置、尺寸、輪廓與遮擋。
白板必須保留圖 1 的全部十張彩色便條及各自灰色橫線，位置、尺寸、色彩順序不改：頂排四張為淡綠、淡藍、淡粉、淡黃；中排右側兩張為淡黃、淡粉；左側一張較低的淡藍；底排右側三張為淡綠、淡黃、淡粉。不能改成圖 2 的空白白板，不新增文字、便條或圖案。
保留白板左後方工作桌及其白色桌腳、桌下淺灰抽屜櫃、藍灰隔板、左側完整綠椅、白板下方被遮擋的綠椅與遠處局部椅背，各自數量、大小與遮擋完全遵循圖 1。不要把被白板擋住的物件搬到旁邊展示。
桌面原有厚折疊布料堆、橫排三色線錐、白色鍵盤、滑鼠、側向薄型螢幕、藍綠筆筒與筆、前側薄布樣，保持圖 1 的物件種類、位置、尺度與前後關係；布料不是書，不新增咖啡杯。
右窗台已有白盆植物與左下角被裁切的前景葉片，位置及主要輪廓保持圖 1；其餘植物以圖 1 的可見範圍為準，不搬入圖 2 更多盆栽。
不旋轉相機、不鏡像、不拉遠或拉近，不移植參考圖中本鏡畫外的物件。不為了展示完整物件而補出被裁切部分。

【材質與細節提升】
沿用圖 1 的構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。
淺木桌面有細緻自然木紋與柔潤高光；折疊布料呈現柔軟厚度、纖維與折邊，線錐呈現細密纏繞線紋；布樣有薄柔布邊，不能改為精裝書本。椅面與隔板有細密織物、合理接縫及柔軟感，維持原有外形。筆筒霧面藍綠、白色鍵帽分明，側向螢幕保持原角度與薄度。
白板為乾淨白色微光澤表面，金屬框和支腳有適度反射與細緻倒角；十張便條為薄紙，保留原有灰色線條與版面，不改成厚板。
牆與窗框為暖白霧面塗料，窗玻璃清透、有細微反射。米色地磚有精細石質微紋、低調縫線及柔和半霧面反光；保持乾燥，不做濕地、鏡面地板或大面積死白過曝。
窗外嚴格保留圖 1 v4 的樹冠高度、分布、枝葉遮擋區域，以及後方高樓的位置、數量、尺度和主要輪廓：窗外下半部是較密實的分枝樹冠，上半部仍有大片清透天空與幾棟遠樓。只在既有體積內細化自然薄葉、葉脈、透光與遠景層次，不新增高聳樹幹、獨立樹木、樓房或搬動樓房；不恢復成其他版本的疏散放射狀樹枝。樓房沿用 v4 的淡藍灰遠景層次，改善現有窗格與立面材質，不改建築輪廓或塞滿天空。植物不可變成球塊，也不可升高樹冠遮住 v4 上半窗原有的天空。
依圖 1 的窗口位置、既有光線方向與地面投影呈現暖日光與柔和陰影，陰影服從本鏡透視，不把圖 2 的光斑直接貼到本鏡。
維持合理紋理尺度與細節密度，不增加髒污或配件。作為後續加入人物的背景母圖，保留近中景清楚可用的資訊，不額外強化散景。

【空景與輸出】
零人物：不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。
只輸出一張與圖 1 一致的 16:9 高解析度橫幅完整圖片，不製作拼貼或九宮格，不加字幕、標誌或水印。

【本鏡畫面】
本鏡為辦公室內平視廣角空景，前方大面積米色地磚延伸至後牆及右牆窗戶，天花上緣保留原有裁切。白板在中央偏右，正面幾乎朝向鏡頭，十張便條完整可見；左後方工作區沿圖 1 的透視向後延伸，最近綠椅在左中景，桌面局部被白板遮擋。右側整排暖白窗框斜向遠方，白盆植物在中右窗台；左下僅露出前景植物的部分葉片。保持白板、桌沿、椅腳、窗台與地磚消失點的原有幾何關係和畫面佔比。
```



## 2026-10-20 coffee_shop v13 空景風格重繪 GPT v2（待評鑑）
- 範圍：kj-cinematic 場景素材；指定全景一張，排除牆面藤蔓。
- 工具：內建 image_gen（OpenAI）；模型版本、預估及實際費用：未知；生成1次。
- 有序輸入：
  1. references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_blender_v13.png
  2. clp/loc_coffee_shop_left_far.jpg
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt_v2.png
- 目視：無人物、無牆面藤蔓，主要視角／桌椅／四幅掛畫配置保留。木紋與植物畫細節改善；窗外葉片、糕點櫃內糕點與局部杯耳細節改變，葉影與暖陽較強，非像素級幾何一致。未自動採用、未重試。
- 完整實際 prompt：
```text
Use case: style-transfer. 請編輯圖1，將這張Blender咖啡館空景提升為圖2的高質感3D動畫場景美術。
圖1 cam_twoshot_wide_level_empty_blender_v13.png 是唯一取景、透視、物件配置與遮擋依據。圖2 loc_coffee_shop_left_far.jpg 僅供材質、色彩、光影與氣氛參考，不移植圖2構圖、家具排列、貨架或植物配置。
色彩與光影：溫潤蜂蜜色木材、深橄欖綠牆面、奶油白陶瓷與石材、霧黑金屬；左側窗外自然暖陽，柔和天空補光，細膩接觸陰影，安靜舒適的精緻3D動畫咖啡館。避免整體過橘與過強泛光。
【保留本機位】
維持圖1的16:9橫幅、相機位置、觀看方向、消失點、構圖和裁切。保留門窗分格、立柱、四張植物掛畫的尺寸及位置、五盞黑吊燈、後牆木板與橫飾條、全部既有桌椅、杯碟糖罐、窗邊桌與高腳椅、右側吧台與曲面玻璃糕點櫃、後側咖啡機水槽及菜單板的位置、數量、尺度、主要輪廓。保留右緣桌椅與筆電的原裁切，不補出全貌。不旋轉、不鏡像、不拉遠或拉近，不添加圖2左側大貨架。
【材質與細節提升】
沿用圖1的構造與物件種類，改善自然木紋、粗糙度、接縫、倒角高光、接觸陰影與金屬玻璃反射。木地板保持乾燥溫潤的柔和緞面，保留可辨識的板縫，不變成濕亮鏡面。杯碟表現細膩陶瓷，吧台淺色石材有微妙質感。植物掛畫呈現清楚且精緻的植物插畫，保持原畫框尺度與留白。窗外樹木以圖1原有輪廓和遮擋呈現細膩葉片與自然透光，原有小盆栽保留原位。
【重要排除】
牆壁上完全不要藤蔓、爬藤、垂吊枝葉。絕對不要將圖2牆上的藤蔓移植進來，掛畫周圍與木牆保持乾淨，吊燈與風管周圍也不要藤蔓。只保留圖1原有盆栽與窗外樹木；掛畫內的植物圖案正常保留。
【本鏡畫面】
平視廣角看向咖啡館後方木牆，左側為窗與橄欖綠立柱，中央前景方桌兩椅與兩杯碟，後方第二組小桌椅；右側吧台、糕點櫃與咖啡設備，右緣裁切一組桌椅。嚴格保留圖1這套幾何關係，讓美術品質接近圖2而不改成圖2視角。
【空景與輸出】
零人物，無人體、倒影或人形剪影。作為後續加入人物的背景，不額外強化散景，近中景清晰。只輸出一張16:9高解析度完整圖片，不拼貼，不加字幕、標誌或水印。
```



## 2026-10-20 coffee_shop v13＋三組道具 GPT v3（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本、預估／實際費用未知；生成1次。
- 有序輸入：
  1. references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_blender_v13.png
  2. clp/loc_coffee_shop_left_far.jpg
  3. clp/prop_menu.png
  4. clp/prop_coffee_set.png
  5. clp/prop_shelf_coffee_cups.png
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt_v3.png
- 目視：無人物與牆面藤蔓；三塊菜單有品名價格、桌面白瓷杯碟與木蓋糖罐、右牆層架白瓷杯組均呈現。主要視角與桌椅／四幅掛畫位置保留。
- 偏差：層架生成8組杯碟（道具圖及prompt指定6組）；左側前景窗台額外出現一盆小盆栽；暖陽葉影較強、糕點與窗外枝葉細節改變。未宣稱幾何完全一致；未重試、未改manifest採用。
- 完整實際prompt：
```text
Use case: style-transfer and reference-guided prop integration.
請編輯圖1，將Blender咖啡館空景提升為圖2的精緻溫暖3D動畫場景，並把圖3、4、5的指定道具外觀整合到圖1既有的對應物件上。輸出一張完整16:9空景。
【有序圖片與責任】
圖1 cam_twoshot_wide_level_empty_blender_v13.png：唯一編輯底圖，固定機位、透視、裁切、建築、桌椅與物件佔位。
圖2 loc_coffee_shop_left_far.jpg：只提供美術材質、色彩、光影與氣氛，不移植其構圖、貨架或植物配置，尤其不要牆面藤蔓。
圖3 prop_menu.png：右牆既有三塊菜單的外觀及文字參考。
圖4 prop_coffee_set.png：桌上既有咖啡杯、杯碟與糖罐的外觀參考，這是同一組道具的細節展示，不是要把整張拼圖放進場景。
圖5 prop_shelf_coffee_cups.png：吧台後方既有木層架上的整排咖啡杯碟外觀參考，底部大杯只是細節特寫，不是額外巨型杯。
【固定本機位】
完全沿用圖1平視廣角，左窗與橄欖綠立柱、後木牆、中央兩組桌椅、右吧台糕點櫃與咖啡機。保持四幅植物掛畫大小位置、五盞吊燈、門窗分格、家具數量位置尺度、桌板與地板邊界、層架與右緣桌椅／筆電的裁切。不得旋轉、鏡像、改變消失點、拉近拉遠，不補出被裁切部分，不新增圖2左側貨架。
【指定道具整合，必須呈現】
1. 右上牆三塊既有菜單：保留圖1所在位置、框的尺寸與各自透視，改為圖3暖木框、深墨綠黑板、奶油白清楚字體。三塊從左至右依圖3內容，每塊標題COFFEE。
左板：Espresso 3.0 / Americano 3.5 / Latte 4.0 / Cappuccino 4.0。
中板：Mocha 4.5 / Caramel Macchiato 4.5 / Flat White 4.0 / Cold Brew 4.0。
右板：Matcha Latte 4.5 / Chai Latte 4.5 / Hot Chocolate 4.0 / Iced Coffee 4.0。
文字與細分隔線自然符合右牆的斜向透視，保持可讀，不把菜單移到正面牆。
2. 桌上的咖啡杯與糖罐：所有既有杯碟套用圖4溫潤象牙白釉面陶瓷、圓潤杯腹、弧形杯耳與淺碟，杯內可見咖啡與淡金色crema。保持原有杯碟數量、佔位與相對座椅的杯耳方向。中央前後兩桌的糖罐改為圖4白瓷圓柱罐、圓肩、厚木蓋與小木旋鈕，蓋子蓋好；依既有糖罐佔位與適合桌面的尺寸，不增加開蓋罐或陳列大罐。不可把參考圖的多角度示意全部複製進來。
3. 右側吧台後方、菜單下方的既有木層架：將原本簡化白色容器呈現為圖5同款白瓷咖啡杯與杯碟，六組沿層架整齊排列，合理縮小並符合透視，各杯有弧形杯耳、每杯配一只淺碟，保留層架位置與支架。不要把六組杯另放中央客桌，不新增一條展示架，不生成道具特寫小窗。咖啡機上的既有小杯保留。
【美術提升】
圖2的溫潤蜂蜜色自然木紋、深橄欖綠牆、奶油白石材與陶瓷、霧黑金屬、柔和金色日光由左窗射入，搭配自然補光與細緻接觸陰影。提升接縫、微紋理、倒角高光、玻璃與金屬反射，木地板乾燥柔和緞面，不濕亮、不過橘、不過度泛光。掛畫維持植物插畫，窗外樹木與原有盆栽在原位置細化；不額外加強散景，近中景清晰。
【重要排除】
牆面完全無藤蔓、爬藤或垂吊枝葉。圖2的藤蔓絕對不要渲染進來。木牆、掛畫周圍、風管、吊燈及層架邊緣保持無爬藤。保留原盆栽及窗外樹，掛畫內植物圖案正常保留。零人物、人體、人物倒影及人形剪影。
輸出一張高解析度16:9完整場景，不做拼貼、道具板或多視圖。不加字幕、水印或額外標誌。
```



## 2026-10-20 coffee_shop GPT v4：單杯耳重繪（待評鑑）
- 工具：內建image_gen／OpenAI；模型、預估／實際費用未知；本輪1次生成。
- 有序輸入：
  1. references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_blender_v13.png
  2. clp/loc_coffee_shop_left_far.jpg
  3. clp/prop_menu.png
  4. clp/prop_coffee_set.png
  5. clp/prop_shelf_coffee_cups.png
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt_v4.png
- 驗收：全圖及前桌放大目視，前景左杯僅左側一個杯耳，右杯僅右側一個杯耳；無牆面藤蔓、無人物，層架為6組杯碟，左前窗台未新增盆栽。PNG 1672×941 RGB；完整解碼與複本SHA256核對。
- 偏差：杯身多了參考圖沒有的金色圖案，左菜單漏Americano；不宣稱道具完全一致，不自動重試或採用。
- v3問題：前桌左杯曾生成額外杯耳，先前全景檢查未辨識；本輪特別放大檢查杯身與輪廓。僅從成圖確認生成瑕疵，不能歸因於Blender模型。
- 完整實際prompt：
```text
Use case: style-transfer and reference-guided prop integration.
編輯圖1 Blender咖啡館空景，以圖2的材質色彩光影提升為精緻溫暖3D動畫場景，整合圖3至5指定道具。一張完整16:9圖片。
【圖片角色】
圖1 cam_twoshot_wide_level_empty_blender_v13.png 是唯一機位、透視、構圖、物件位置、尺度與遮擋依據。
圖2 loc_coffee_shop_left_far.jpg 只供美術參考，不移植構圖、貨架或牆面藤蔓。
圖3 prop_menu.png 是右牆三塊菜單的內容與材質。
圖4 prop_coffee_set.png 是既有桌面杯碟與木蓋糖罐外觀，圖中多角度是同一道具的展示，不是要放入多個道具或合併多角度。
圖5 prop_shelf_coffee_cups.png 是吧台後方既有木層架的六組白瓷杯碟外觀，大杯特寫不放入場景。
【最高優先：正確的單杯耳結構】
所有咖啡杯每只只有唯一一個C形杯耳。Each cup has exactly ONE handle total, attached on ONE side only. Never two handles. Never a second handle on the front, back, opposite side, or inside the cup. Do not blend multiple reference views into one cup.
特別注意中央第一張前景桌的左邊咖啡杯：唯一杯耳在該杯的畫面左側；杯腹正面與畫面右側均為完整光滑連續的白瓷曲面，沒有第二個杯耳、環、突出物或假杯耳形狀的高光。杯中咖啡、杯口橢圓與杯碟都正常。
中央前景桌右杯也只有唯一一個杯耳，保留底圖的方向；後桌、窗邊、右緣桌、層架、咖啡機上的所有可見咖啡杯都遵守一杯一耳。若杯耳被透視遮住就自然遮住，絕不為展示杯耳而加第二個。請在輸出前逐只檢視杯耳結構。
【保持底圖】
保持圖1平視廣角的相機位置、消失點、裁切和16:9構圖，左窗與綠色立柱，後木牆四幅植物掛畫，五盞黑吊燈、中央兩組桌椅、右吧台糕點櫃、咖啡機、水槽及層架。全部家具位置、數量與尺度不變，不旋轉、不鏡像、不拉遠拉近。保持右緣桌椅筆電裁切。窗台只保留底圖已有盆栽；左側最前方空窗台仍然空著，不新增盆栽。
【道具】
右牆三塊菜單保留原位置大小與斜向透視，暖木框／深墨綠黑板／奶油白字。每板標題COFFEE，從左至右：
左板 Espresso 3.0 / Americano 3.5 / Latte 4.0 / Cappuccino 4.0。
中板 Mocha 4.5 / Caramel Macchiato 4.5 / Flat White 4.0 / Cold Brew 4.0。
右板 Matcha Latte 4.5 / Chai Latte 4.5 / Hot Chocolate 4.0 / Iced Coffee 4.0。
桌面既有杯碟改為圖4溫潤象牙白釉面陶瓷、圓杯腹、唯一單側弧形杯耳、淺碟與杯中咖啡crema；保持原數量與位置。兩張中央桌的糖罐為圓肩白瓷圓柱罐、厚木蓋與小木旋鈕，蓋好，大小符合底圖佔位，不增加罐。
右牆菜單下方既有木層架以圖5呈現恰好六組白瓷杯碟，6 cups and 6 saucers total on that shelf, not eight，整齊排列且各杯只有一個杯耳，保持層架支架與位置。不另加層架。咖啡機上既有小杯保留。
【美術】
溫潤蜂蜜木紋、深橄欖綠牆、奶油白石材陶瓷、霧黑金屬、左窗柔和暖陽與自然補光。改善微紋理、倒角高光、接觸陰影、玻璃金屬反射。乾燥緞面木地板，不濕亮、不過橘、不過度泛光；近中景清晰，不額外增加景深。掛畫維持植物插畫；原有盆栽與窗外樹細化，不新增植物。
【排除】
牆面完全沒有藤蔓、爬藤、垂吊枝葉，圖2牆面植物不得移植；掛畫周圍、風管、吊燈及層架周圍無藤蔓。掛畫內植物圖案正常保留。零人物、人體或人物倒影。無拼貼、特寫小窗、字幕、水印。只輸出一張完整高解析度場景。
```



## 2026-10-20 coffee_shop GPT v5：杯耳朝坐者右手（未通過）
- 工具：內建image_gen／OpenAI；模型與預估／實際費用未知；本輪1次。
- 有序輸入：
  1. references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_blender_v13.png
  2. clp/loc_coffee_shop_left_far.jpg
  3. clp/prop_menu.png
  4. clp/prop_coffee_set.png
  5. clp/prop_shelf_coffee_cups.png
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt_v5.png
- 放大驗收未通過：前桌左杯杯耳仍朝畫面左側，沒有朝坐者右手／近相機方向；後桌左右杯出現雙杯耳。前桌局部仍有疑似殘留杯耳輪廓。層架8組杯碟，非指定6組。無牆面藤蔓與人物，杯身無金色圖案，左菜單恢復Americano。
- 檢查圖：.tmp/coffee_v5_cups_inspection.png（僅放大檢查，不修改交付圖）。原生PNG 1672×941 RGB，完整解碼及複本SHA256核對。未採用、未追加生成。
- 完整實際prompt：
```text
Use case: reference-guided style-transfer. 請從圖1 Blender底圖重繪一張完整16:9高品質3D動畫咖啡館空景，以圖2提供美術，以圖3～5提供指定道具。
有序輸入：圖1 cam_twoshot_wide_level_empty_blender_v13.png 唯一決定相機、透視、物件佔位及遮擋；圖2 loc_coffee_shop_left_far.jpg 只提供色彩材質光影，不提供構圖或藤蔓；圖3 prop_menu.png 為右牆菜單；圖4 prop_coffee_set.png 為桌上杯碟及糖罐；圖5 prop_shelf_coffee_cups.png 為吧台後層架杯組。道具圖中的多角度只是同一物件的外觀展示，不能合併為多杯耳造型，也不將參考拼圖放進場景。

【最高優先：每杯唯一一個杯耳，依座位右手方向】
Each coffee cup has exactly ONE physical C-shaped handle total, never two. Every seated customer's cup handle points to THAT CUSTOMER'S right hand, not the viewer's right.
中央前景桌左側椅子的坐者朝畫面右方看向桌面，所以左杯唯一杯耳應朝靠近相機／桌面前緣方向，沿前後深度軸，不能另在杯子的畫面左邊或右邊再加一耳。這是一個由杯身前側自然突出的白瓷立體環形把手，有合理透視與遮擋，不是杯身圖案。
中央前景桌右側椅子的坐者朝畫面左方看向桌面，所以右杯唯一杯耳應朝遠離相機／桌面後緣方向，沿前後深度軸；它大部分可被杯身遮擋，只露合理輪廓即可，絕不為了讓人看清把手而補第二個側耳。
後方中央小桌亦是左右相對座位，同樣左杯朝近相機、右杯朝遠離相機。右緣桌杯耳根據它實際對應椅子的坐姿右手側，不一律朝畫面右方。窗邊杯依椅子朝窗的方向轉到坐者右手側。
只轉動杯子本身，保持杯碟中心、杯中咖啡、桌椅、相機和杯子數量不變。唯一杯耳被遮擋是正常，不可用新增杯耳補償。所有咖啡機與層架上的杯子也只有一個杯耳。
杯身為乾淨光滑的純象牙白瓷，NO logo, NO emblem, NO gold pattern, NO printed ornament。不能把正面杯耳變成金色圖案。輸出前檢查每只杯是否出現第二個耳或裝飾圖案。

【圖1幾何與空景】
保持圖1原機位、平視廣角、消失點、裁切、四幅植物掛畫位置大小、五盞黑吊燈、門窗分格、綠立柱、全部桌椅、吧台、糕點櫃、咖啡機與水槽配置，右緣桌椅筆電維持裁切。不要旋轉、鏡像、拉近或拉遠。不要添加圖2左側貨架。保留原有盆栽，左前窗台原本空處保持空著。
牆壁完全無藤蔓、爬藤、垂吊葉，不移植圖2的藤蔓。掛畫、風管、吊燈、層架周圍乾淨無藤蔓；畫中的植物插畫保留。無人物、人體、倒影或人形剪影。

【指定道具】
三塊右牆菜單保持圖1框的位置大小與斜向透視，採圖3木框、墨綠黑板、奶油白字，三塊標題COFFEE。每塊必須有四個品項，不漏行：
左：Espresso 3.0；Americano 3.5；Latte 4.0；Cappuccino 4.0。
中：Mocha 4.5；Caramel Macchiato 4.5；Flat White 4.0；Cold Brew 4.0。
右：Matcha Latte 4.5；Chai Latte 4.5；Hot Chocolate 4.0；Iced Coffee 4.0。
圖4桌面杯碟為溫潤象牙白釉面、圓潤杯腹、淺碟，杯中咖啡與淡金色crema。中央兩桌既有糖罐套用白瓷圓肩罐、木蓋與小木旋鈕，蓋好、保持適合桌面大小。保持原杯碟和糖罐數量。
圖5用於右牆菜單下方既有層架，恰好六只白瓷咖啡杯和六只杯碟，合理透視整齊排列，單杯耳，保留層架支架；不要新增架子或搬到客桌。咖啡機上既有小杯保留。

【美術】
圖2的溫潤蜂蜜色木紋、深橄欖綠牆、奶油白石材陶瓷、霧黑金屬與柔和左窗暖陽，搭配自然補光、細緻接觸陰影、玻璃金屬反射與倒角。木地板乾燥緞面，不濕亮，不過橘或過度泛光。近中景清晰，不增加散景。窗外樹與原盆栽在原輪廓內細化。
輸出一張高解析度16:9完整場景，不拼貼、不加小窗、字幕、水印。
```



## 2026-10-20 coffee_shop GPT v6：指定五圖重繪，杯耳未通過
- 工具：內建 image_gen／OpenAI；確切模型及預估／實際費用未知；本輪1次。
- 有序輸入：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_blender_v13.png；clp/loc_coffee_shop_left_far.jpg；clp/prop_menu.png；clp/prop_coffee_set.png；clp/prop_shelf_coffee_cups.png。
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt_v6.png（原生PNG 1672×941 RGB）。
- 驗收：無人物／牆面藤蔓；三菜單、木蓋糖罐、層架六組杯碟已呈現，主要構圖保留但暖陽及葉影增強。前桌左杯仍有側耳＋正面突起，未滿足單杯耳；後桌左杯仍朝畫面左側。未宣稱所有杯耳方向通過。
- 已完整解碼、來源與複本SHA256一致；放大檢查圖 .tmp/coffee_v6_cups_inspection.png。未採用、未追加生成，未改模型／舊版／manifest。
- 完整實際 prompt：
```text
Edit image 1 into a polished cinematic 3D animated coffee shop empty background. Image 1 alone controls viewpoint, perspective, furniture, framing and occlusion. Image 2 supplies warm wood, olive green, soft sunlight and material finish only. Image 3 supplies the three menu designs. Image 4 supplies plain ivory porcelain coffee cups, saucers and wooden-lidded sugar jars. Image 5 supplies the SIX shelf cups and saucers. Never paste the reference sheets or their backgrounds into the scene.

CRITICAL physical cup construction and orientation:
Each cup has exactly ONE attached handle, a single ceramic loop with two attachment points. No cup may have two handles. Completely remove the old handle when rotating a cup. Do not leave a side handle while drawing a new front handle.
At BOTH central tables, the person in the LEFT chair would face right: their right hand is toward the camera. Thus the LEFT cup's ONLY handle projects toward the camera, from the FRONT face of the cup. Depict this handle nearly EDGE-ON as a narrow vertical ivory ceramic loop with thickness and a small shadow on the front of the cup. Its left and right silhouettes remain smooth uninterrupted bowl contours: NO sideways ear on either silhouette.
At BOTH central tables, the person in the RIGHT chair would face left: their right hand is away from the camera. Thus the RIGHT cup's ONLY handle projects away from the camera, BEHIND the cup, naturally largely hidden by the bowl. Both side silhouettes remain plain smooth bowl contours; do not add a visible side handle to compensate.
For the right-edge table and window-counter cup, orient the sole handle toward the actual seated user's right side based on the chair facing direction. Preserve cup/saucer centers and counts.
All cups on the espresso machine and shelf also have exactly one handle each. All porcelain is plain ivory, no gold emblem, no decorative pattern. Handle detail is ceramic geometry, never printed ornament. Cup coffee has a natural crema surface.

Architecture: match image 1 exactly in its wide eye-level view, left windows and olive pillars, four framed botanical prints, five black pendant lamps, two central tables with opposing chairs, stools, right counter, glass pastry case, sink, espresso machine, shelf and right-edge cropped laptop/table/chair. Do not import image 2's left merchandise shelving. No added furniture or plants. Keep the nearest left windowsill empty as in image 1.
Absolutely NO wall vines or trailing foliage anywhere. No ivy around art, pipes, lights or shelves. Keep existing upright potted plants and outdoor trees only. Botanical artwork inside frames remains.
Zero people, limbs, human silhouettes or human reflections.

Props: transform the three existing right-wall boards with image 3's wood frame, dark green chalkboard and cream lettering, preserving their original oblique perspective and footprint. Each title COFFEE, four rows each:
left: Espresso 3.0 / Americano 3.5 / Latte 4.0 / Cappuccino 4.0
middle: Mocha 4.5 / Caramel Macchiato 4.5 / Flat White 4.0 / Cold Brew 4.0
right: Matcha Latte 4.5 / Chai Latte 4.5 / Hot Chocolate 4.0 / Iced Coffee 4.0
Use image 4's rounded cups and shallow saucers for existing table settings; both central sugar jars have rounded shoulders, white ceramic bodies, thick wood lids with small wood knobs. Keep lids closed and preserve their positions.
On the single existing shelf directly below the menus place exactly SIX ivory cups on SIX saucers, evenly spaced in perspective, based on image 5. Do not copy the detail views as extra cups. Keep the existing espresso machine cups separate.

Finish: honey wood with fine grain, dark olive painted wall, cream stone, satin black metal, soft warm daylight from the left windows, subtle realistic ceramic and glass reflections, natural contact shadows, fine bevels. Dry satin floor, restrained warm colors, no excessive orange cast, bloom or mirror-like floor. Keep near and middle ground clearly readable. One complete high-resolution 16:9 image, no collage, inset, caption or watermark. Before output, check all four central table cups: left handles edge-on at front, right handles hidden at rear, NEVER two handles.
```



## 2026-10-20 coffee_shop GPT v7：cafe3 美術與三道具（杯耳方向未通過）
- 工具：內建 image_gen／OpenAI；確切模型、預估及實際費用未知；本輪1次。
- 有序輸入：
  1. references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_blender_v13.png
  2. D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/cafe/cafe3.png
  3. clp/prop_menu.png
  4. clp/prop_coffee_set.png
  5. clp/prop_shelf_coffee_cups.png
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt_v7.png
- 驗收：無人物／牆上藤蔓；四掛畫與主要構圖保留，三菜單、白瓷杯碟及木蓋糖罐已帶入，層架可見六組杯碟。前後桌杯耳仍朝畫面左右，未符合坐者右手方向；目前可見杯耳未見雙耳。暖陽與葉影較底圖強，右菜單前兩價格有偏差。此版未通過完整需求，不採用、不追加重試。
- 原生PNG 1672×941 RGB，完整解碼與原生複本SHA256一致。
- 完整實際 prompt：
```text
請編輯圖1 Blender空景，以圖2 cafe3.png 的精緻自然木材、日光、色彩和材質重繪成一張高質感16:9咖啡館場景。圖1是唯一的相機、透視、裁切、佈局與遮擋依據。圖2只供美術，不移植書架、家具排列或任何藤蔓。圖3提供右牆菜單；圖4提供桌上咖啡杯、碟子、糖罐；圖5提供右牆吧台上方層架的六組杯碟。參考圖的多角度是同一物件示意，不是要複製拼圖。
最高優先：所有杯子各只有一個實體C形杯耳，絕不雙耳。桌上杯耳必須轉向各座位坐者的右手側。
中央前桌：左椅坐者面向右方，其右手朝相機，因此左杯把手位於杯身正前方朝相機，呈窄而有厚度的縮短透視環形，杯身左右兩側都沒有側耳。右椅坐者面向左方，其右手朝後牆，因此右杯把手在杯身後方，可被杯身完全遮住，不要為了展示把手而加側耳。
後方中央桌同樣左杯唯一把手朝相機、右杯唯一把手朝後牆。右緣桌杯依既有座位面向桌心的右手側轉向。窗邊杯依高腳椅朝窗的坐姿右側轉向。保持杯碟位置，僅旋轉杯子。所有杯子是素白瓷，沒有印花、金色標誌或圖案。前向把手是真正有孔的白瓷把手，不是印在杯身上的紋樣。杯耳可被遮擋；不要畫額外輪廓。
保持圖1的左側木窗、綠色立柱、四幅植物掛畫的尺寸位置、黑色吊燈、後牆木板、窗台及高腳椅、兩張中央桌椅、右側吧台、甜點玻璃櫃、咖啡機、水槽與畫面右邊裁切的桌椅筆電。保持相機消失點及完整原裁切，不旋轉、不鏡像、不變焦。左前方空窗台保持空著。
牆壁、窗框、天花、燈具、層架完全沒有藤蔓、爬藤或垂吊枝葉。保留底圖原有盆栽與窗外樹木，僅在原體積內細化；保留掛畫內的植物插畫。不新增植物。
右牆三菜單的木框、墨綠底、奶油白字取自圖3，保持原位置大小和透視。每板標題COFFEE，左板四行Espresso 3.0 / Americano 3.5 / Latte 4.0 / Cappuccino 4.0；中板Mocha 4.5 / Caramel Macchiato 4.5 / Flat White 4.0 / Cold Brew 4.0；右板Matcha Latte 4.5 / Chai Latte 4.5 / Hot Chocolate 4.0 / Iced Coffee 4.0。
桌上杯碟套用圖4圓潤象牙白陶瓷、咖啡crema及淺碟，保留數量大小位置；兩桌糖罐套用白瓷圓肩圓柱罐、厚木蓋與木旋鈕，蓋好且尺寸符合原佔位。圖5的恰好六組杯碟排列在右牆菜單下現有木架：six cups and six saucers, each cup one handle, not eight cups。咖啡機已有杯子保留且每杯一耳。
美術參考圖2：自然溫潤木紋、細緻材質、清透窗玻璃、柔和暖陽和自然補光、合理接觸陰影與金屬反射。保留圖1的地板木材，不改石材；乾燥緞面、不過度鏡亮、不過橘、不過曝。細化木紋、倒角、陶瓷釉面，保持近中景清晰，不增加散景。
零人物、人體、手臂、人物倒影。只輸出一張完整16:9高解析度機位圖，無拼貼、無水印、無字幕。輸出前逐一檢查前後桌四杯的單耳與朝向，不可將杯子預設成左右側耳。
```


## 2026-10-20 coffee_shop 雙人平視中景空景 GPT v1（待評鑑）
- 流程：blender-view-restyle.md；kj-cinematic 場景機位素材局部重繪。
- 工具／供應商：內建 image_gen／OpenAI，1 次生成；確切模型與費用未知。
- 圖 1（唯一編輯底圖）：references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_blender.png
- 圖 2（美術參考）：clp/loc_coffee_shop_front_far.png
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt.png
- 原生 PNG 1672×941 RGB；完整解碼與來源／交付複本 SHA256 一致，未縮放裁切。
- 目視：主要中景構圖、前後桌椅、左窗邊檯與右吧台／甜點櫃、三幅掛畫裁切大致保留，無人物或牆面藤蔓。暖陽及地面葉影較強；糖罐蓋新增較明顯旋鈕，後桌右杯出現側向杯耳，前桌左杯耳孔仍不清晰，植物／掛畫細節重繪，並非幾何完全一致。
- 保留底圖與 Blender；未改 manifest 採用或其他機位，未追加生成。

### 完整實際 prompt
```text
請編輯圖1，將這張Blender咖啡館空景提升為圖2的精緻3D動畫場景質感。
圖1 cam_twoshot_ms_level_empty_blender.png 是唯一的取景、透視、物件配置、尺寸、裁切與遮擋依據。
圖2 loc_coffee_shop_front_far.png 僅供材質、色彩、光影與氣氛參考，不移植其廣角構圖、家具排列或畫外物件，不重新生成圖2。
色彩光影參照圖2：自然蜂蜜色木材、橄欖綠牆柱、奶油白陶瓷，左側窗戶柔和暖陽與自然環境補光；適度陰影層次，避免過橘、過曝或過強泛光。

【保留本機位】
維持圖1的16:9畫幅、平視中景、消失點、觀看方向及緊裁切。不要拉遠展示整間店。
原位保留前景一張木桌與兩把左右裁切木椅、後方一張較小木桌與兩椅、左側窗邊高桌及高腳椅、窗框與綠柱、植物盆栽、筆電與杯子、後牆三幅可見且部分被上緣裁切的植物掛畫、右側白檯面木吧台與玻璃甜點櫃。保留全部物件數量、尺度、輪廓與遮擋。
兩張中央桌各保留兩個素白杯及碟子和一個有木蓋的白色糖罐，保持杯碟佔位與圖1杯耳朝向，每杯僅一耳；被杯身遮住的杯耳不用補出。不要新增杯耳、金色圖案或印花。
不要補出圖1畫外的咖啡機、菜單、吊燈、層架或右側其他桌椅。不旋轉相機、不鏡像、不改視野。

【材質與細節提升】
保持圖1各構造，只提升自然木紋、接縫、細微倒角高光、接觸陰影、粗糙度與反射。木材具有圖2的細緻溫潤自然紋理，乾燥緞面，避免塑膠感和濕亮鏡面地板。
白瓷杯碟有柔和釉面與圓潤邊緣；糖罐保留原大小與蓋子。甜點櫃為清透曲面玻璃與細緻金屬邊框，保留圖1的輪廓位置。牆上植物插畫清晰自然，框的位置尺寸不變。
盆栽沿用原位置、種類、主要體積，只細化葉片與透光，不新增植物，不加牆面藤蔓。窗玻璃保留自然透光反射，不複製圖2畫面座標上的光斑。
近中景材質保持清晰，作為後續加入人物的背景，不額外增加景深或散景。

【本鏡畫面】
鏡頭正對木質後牆，前景桌面橫跨中央下半部、兩椅在左右下緣裁切，後桌置於畫面中央更遠處；左邊只見一部分窗邊工作檯與高腳椅，右邊吧台和玻璃甜點櫃被畫面右緣裁切。保持兩桌的前後比例、椅背位置和後牆掛畫裁切完全依圖1，不套用圖2較寬的取景。

零人物、人體、手臂、人物倒影或剪影。只輸出一張完整16:9高解析度圖片，無拼貼、無字幕、無水印。

```

## 2026-10-20 coffee_shop 中景空景 GPT v2（JPG 參考；待評鑑）

- 工具：內建 image_gen；供應商：OpenAI；模型版本／費用未知；生成1次。
- 有序輸入：
  1. references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_blender.png
  2. clp/loc_coffee_shop_front_far.jpg
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v2.png
- 觀察：主要中景構圖、前後桌椅與掛畫裁切保留，無人物；前桌左杯新增側耳而保留原正面突起，未符合單杯耳；後桌杯耳亦有變化，糖罐木蓋新增小把手，日照陰影加強。未追加重試或採用。
- 完整實際提示詞：

```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感3D動畫美術的場景背景。
圖1 cam_twoshot_ms_level_empty_blender.png 唯一決定相機位置、觀看方向、透視、構圖、畫面裁切及物件配置。
圖2 loc_coffee_shop_front_far.jpg 是使用者指定的美術參考，只提供材質、色彩、光影與氣氛。不要採用圖2的拍攝角度、消失點、畫面排列或可見範圍，不要重新生成圖2。
匹配圖2溫潤蜂蜜色木材、低飽和橄欖綠柱、乳白陶瓷、自然柔和暖陽與細緻陰影，不額外加強橙色、飽和度或泛光。依圖1朝向維持左窗採光，投影隨本鏡合理變化。

【保留本機位】
維持圖1的16:9畫幅、平視中景、消失點、主要結構與緊裁切。不旋轉相機、不鏡像、不拉遠或拉近。
原位保留前景一張木桌與左右兩把被下緣裁切的木椅、後方一張較小木桌與兩椅、左側部分窗邊高桌與高腳椅、窗框與綠柱、盆栽、筆電與杯子、後牆三幅可見且部分被上緣裁切的植物掛畫、右側白檯面木吧台及玻璃甜點櫃。所有物件的位置、數量、尺度、主要輪廓與遮擋以圖1為準。
中央兩張桌各保留兩個素白杯與碟子、一個帶蓋白色糖罐，杯耳沿圖1朝向，每杯僅一耳，被遮住的耳不用補出。糖罐蓋細化為自然木質。不要新增圖案或配件。
不為了展示完整物件補出裁切部分，不補圖1畫外的菜單、咖啡機、層架、其他桌椅或完整吊燈。

【材質與細節提升】
沿用圖1構造與物件種類，只提升木紋、粗糙度、接縫、細微倒角高光、接觸陰影與反射。木牆、木地板和桌椅具有圖2的細緻自然紋理和乾燥緞面，不做濕亮鏡面或塑膠質感。
白瓷杯碟呈現柔和釉面，玻璃甜點櫃清透、金屬邊框精細，保持原有甜點數量與位置，不改成圖2的甜點排列。
植物保留原位、種類與主要體積，細化薄葉與透光，不新增植物或牆面藤蔓。掛畫維持尺寸、位置與既有植物畫題，只提升清晰度。
保留近中景可用資訊，不額外增加散景，不複製圖2畫面座標上的光斑。

【本鏡畫面】
鏡頭正對木質後牆，前景桌面佔畫面中央下半部，兩側椅背很大且坐墊、椅腳被下緣裁切；後桌位於中央遠處；左側僅見部分窗邊高桌，右側吧台延伸出畫框。後牆兩幅大植物畫和右上一幅較小畫被頂邊裁切。前後兩桌比例、椅背位置、吧台輪廓和所有裁切嚴格依圖1。

【空景與輸出】
零人物，不得出現人體、肩膀、手臂、人物倒影或人形剪影。
只輸出一張16:9高解析度完整圖片，無拼貼、字幕、標誌或水印。
```


## 2026-10-20 coffee_shop 中景空景 GPT v3：杯耳與糖罐蓋局部修正

- 工具：內建 image_gen／OpenAI；生成1次；模型版本與費用未知。
- 有序輸入：1. references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v2.png；2. references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_blender.png（僅杯耳方向／平蓋參考）。
- 輸出：references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
- 目視結果：左前杯多餘側耳已去除、朝鏡頭的窄杯耳保留；前後糖罐木蓋把手均已移除；主要構圖、暖色與日照保持，AI重繪細微紋理非像素級不變。保留v2，未更新採用設定。
- 完整實際提示詞：

```text
Edit image 1 only with two extremely small local corrections. Image 1 is the approved v2 cafe appearance and sole source of composition, lighting, colors, material style, framing, and every object. Image 2 is the original Blender view and is ONLY a reference for the front-left cup handle orientation and flat sugar jar lids; do NOT transfer its lighting or materials.
1. On the nearest table, the left white cup currently has an unwanted C-shaped loop sticking out to screen-left AND a narrow vertical handle viewed edge-on on its front-facing surface. REMOVE ONLY the extra C-shaped loop protruding to the left (approximately x=620–648, y=590–637 on image 1 at 1672x941). Restore the background where this loop was. KEEP the existing narrow vertical front-facing handle, in exactly its existing position and orientation pointing toward the viewer, matching image 2. This cup must have exactly ONE handle, the existing front-facing edge-on handle. Do not remove that front-facing handle or rotate the cup. Keep the cup body, rim, coffee, saucer and placement unchanged.
2. On BOTH white sugar jars (one on each central table), remove the small upright wooden knob from the center of each lid. Keep the wooden disk lids, making their tops smooth and flat, with no handle, peg, knob, stem or raised center. Keep the jar bodies, lid diameters, positions and materials unchanged.
Preserve everything else in image 1 unchanged: all other cups and handles, tables, chairs, wall boards, framed botanical pictures, window, plants, laptop, display case, pastries, counter, camera, shadows, sunlight and exact warm color grading. No redesign, no reframing, no extra objects, no people. Output one complete image with the same aspect ratio as image 1.
```


## 2026-10-20 investment_office 廣角空景 GPT 首版（待評鑑）
- 流程：skills/kj/blender-view-restyle.md，原 pipeline kj-cinematic 場景素材局部製作。
- 有序輸入：1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_blender.png`；2. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/投資辦公室/投資辦公室_陰天_16_9.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_gpt.png`。
- 原生圖：`C:/Users/servi/.codex/generated_images/01a159dc-73fa-7290-884d-4831251087e3/call_3f95166402404026ba86f989a0e06b2a.png`。
- 工具／供應商：內建 image_gen／OpenAI；1 次生成，確切模型與費用未知。
- 檢查：PNG 1672×941 RGB 完整解碼成功，原生圖與專案複本 SHA256 一致；未裁切或拉伸。
- 目視：零人物，主要構圖、桌椅配置、筆電與投影圖表保留；陰天漫射光與木紋／皮革細節改善。圖表細小文字與局部反射經重繪，非像素級幾何一致；未自動採用、未重試。

### 完整實際 prompt
```text
Use case: style-transfer. 請編輯圖1，將 Blender 投資辦公室空景提升為圖2的高質感寫實建築室內渲染，參考圖2的材質、色彩、光影與氣氛。圖1 cam_threeshot_wide_level_empty_blender.png 是唯一的取景、透視、物件配置與遮擋依據。圖2 投資辦公室_陰天_16_9.png 僅供美術表現參考，不移植其構圖、家具排列或相機高度。色彩與光影採用圖2明亮但柔和的陰天漫射日光、灰白室內表面、自然暖棕木材與棕褐皮革、低飽和冷灰城市背景；改善圖1過暗的曝光，同時維持柔和立體感，不加入直射陽光或金黃色調。
【保留本機位】維持圖1的16:9畫幅、觀看方向、消失點、主要結構與遮擋。保留本鏡門窗分格、天花板木格柵、投影機、燈具、門把、地面邊界、會議桌與所有椅子的位置、數量、尺度與主要輪廓。不旋轉相機、不鏡像、不拉遠或拉近。不採用圖2較低且較遠的角度；圖1桌面延伸並裁出整個畫面下緣，絕對不要顯示圖2那種完整桌子前緣或桌腳。圖1後牆投影幕上的財務柱狀圖、折線圖、表格與現有內容要保留，不改成圖2空白幕；桌子遠端偏右的單一打開筆電要保留，螢幕仍為黑色。不增加其他桌面配件。
【材質與細節提升】沿用圖1構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。會議桌和頂部格柵呈現圖2自然細緻的棕色木紋；椅面呈現柔軟但保持原輪廓的棕褐皮革，帶細小紋理與細緻接縫；金屬扶手及椅腳有克制的鍍鉻高光；左側玻璃隔間呈現通透且合理的室內反射；灰色地面呈現圖2細織地毯質感，保留圖1分格與邊界。右側窗外保留圖1建築位置、大小和可見範圍，呈現柔和陰天冷灰光，不換成圖2城市佈局。維持乾燥霧面表面，不加髒污或過度鏡面反光。近中遠景材質均清楚，作為後續加入人物的背景母圖，不強化散景。
【本鏡畫面】正對會議室後牆投影幕的水平廣角空景。長木桌從畫面下緣佔滿前景向後牆收束，左右為棕色高背會議椅，最前方兩側椅子被畫框裁切；左邊深色玻璃隔間與門，右邊落地窗及近距離辦公樓，頂部木格柵與吊掛投影機。嚴格保留圖1的空間幾何及裁切。
【輸出】零人物、零人體、零人物倒影或剪影。只輸出一張16:9高解析度完整圖片，不拼貼，不加字幕、標誌或水印。
```

## 2026-10-20 investment_office tower 空景 GPT v1（待評鑑）
- 流程：kj-cinematic assets／skills/kj/blender-view-restyle.md，單一指定機位重繪。
- 有序輸入：1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_tower_wide_low_angle_empty_blender.png`；2. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/倫敦區/倫敦金融大樓B.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_tower_wide_low_angle_empty_gpt.png`；原生1672×941 RGB PNG，未裁切／拉伸。
- 工具：內建 image_gen／OpenAI，1次；確切模型與預估／實際費用未知。
- 原生來源：`C:/Users/servi/.codex/generated_images/01a159df-3937-74b0-8ef7-c920e67e4b7c/call_dbd9715171094685b00d793b585cc136.png`。
- 驗證：完整解碼通過，來源與交付SHA256一致（9d824895759c934600d57ee66abbffa66104c86ce3ef1468d13dcc4a6a6be432）。已逐圖目視比較：主樓群佔位／裁切大致保留，冷藍暴雨、濕屋頂與玻璃反光生效，無明顯人物；窗格與亮燈分布改變，部分灰色牆面更玻璃化，遠處新增少量樓影，地面反光增強。非像素級幾何一致，尚待使用者評鑑；未改模型、manifest或其他機位，未重試。

### 完整實際 Prompt
```text
請編輯圖 1，將這張 Blender 空景提升為精緻電影級城市暴雨場景，參考圖 2 的材質、色彩、光影與氣氛。
圖 1 cam_tower_wide_low_angle_empty_blender.png 是唯一的取景、透視、物件配置與遮擋依據。
圖 2 倫敦金融大樓B.png 僅供美術表現參考，不移植其構圖、建築排列或地標。不要加入河流、橋梁、摩天輪、尖塔或小黃瓜大樓。
色彩與光影採用圖 2 的深海軍藍、冷鋼藍與青藍雨霧，厚重暴風雲、細長雨絲、濕潤表面冷光及零星辦公室燈光；維持近景建築清楚可讀，遠處有適度雨霧。天空有限可見區域呈現陰雲冷光，不為展示閃電而擴展天空。
【保留本機位】
維持圖 1 的16:9畫幅、觀看方向、消失點、主要結構與遮擋。嚴格保留每棟方形大樓的位置、數量、尺度、輪廓、樓層橫帶、窗格與平屋頂機房。圖中主樓是畫面左中大型方形高樓，中央後方有纖細玻璃塔，右方有另一座大型方樓；保持全部建築相互遮擋與相對高度。最上緣與左右、下緣被裁切的建築繼續裁切。不旋轉相機、不鏡像、不拉遠或拉近。不要因機位名稱而改成地面仰拍，以實際圖1為準。
【材質與細節提升】
沿用圖 1 的構造與物件種類，改善玻璃幕牆的粗糙度、金屬框接縫、細微倒角高光、接觸陰影與雨天反射。窗戶有細緻冷藍反射及少量柔和室內燈光，保持窗格節奏，不新增密集發光裝飾。屋頂與既有地面呈現雨濕反光和細微水膜，不改成河道。保留原有灰白實體牆與玻璃面的差別。均勻簡模提升為有真實材質層次的高品質電影CG；不藉材質轉換重設計建築，不新增招牌、天線、植物或配件。雨絲覆蓋畫面但不遮蔽主要結構，不額外強化散景。
【本鏡畫面】
本鏡是密集金融區高樓群的廣角視野，相機在樓群中上部高度，能看到多棟屋頂與正側立面。左中最大方樓從上方約十分之一延伸出畫面底部，右方大樓頂部約在上方五分之一。中央窄玻璃樓及後方高樓保留原位。地面只在中下部樓縫少量可見，天空主要在上緣及樓間，保留整體緊密構圖與層次。
【空景與輸出】
零人物，不出現路人、人體、人物倒影或人形剪影。只輸出一張16:9高解析度完整圖片，不拼貼，不加字幕、標誌、水印；不複製圖2右下角星形標記。
```

## 2026-10-20 investment_office 廣角空景 GPT v2：簡報調暗版（待評鑑）
- 使用者要求：正在開會簡報，燈光調暗，另存一版本。
- 唯一輸入：`references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_gpt.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_gpt_v2.png`。
- 原生圖：`C:/Users/servi/.codex/generated_images/01a159dc-73fa-7290-884d-4831251087e3/call_f3dfb09c321c446e90d3b2d2445e267f.png`。
- 工具／供應商：內建 image_gen／OpenAI，1次生成；確切模型及費用未知。
- 驗證：1672×941 RGB PNG 完整解碼及複本 SHA256 通過；目視室內明顯調暗、窗外維持白天、投影幕突出，桌椅及筆電構圖保留。燈具仍微亮；細部文字與紋理非像素級保留。保留首版，未自動採用或重試。
### 完整實際 prompt
```text
Use case: lighting-weather. Edit this exact image into a moderately dimmed daytime presentation-in-progress lighting variant. Change lighting only. Preserve the exact camera, framing, 16:9 composition, perspective, furniture count, furniture geometry, wood and leather materials, glass partition, ceiling slats, projector, window divisions and exterior buildings. Keep the single open laptop with its black screen and the exact financial charts on the projection screen. No people or human reflections. Dim the ceiling spotlights and recessed lights substantially to a low meeting-presentation setting; reduce artificial illumination and bright highlights across the table, chairs and ceiling. Make the interior visibly but moderately darker, approximately one stop darker in the central room, with soft realistic shadows and readable wood grain and leather details. Retain soft overcast DAYLIGHT through the right windows, with the exterior staying daytime and brighter than the interior. The projection screen should retain its current readable chart content and brightness, now perceptually the main focal point against the dimmer wall. Preserve gentle indirect fill so the room is usable for participants taking notes. Do not make it a night scene, a blacked-out cinema or a dramatic dark blue room. Do not apply a uniform dark overlay to the whole image; change the illumination physically coherently, preserving projection brightness and exterior daylight. Do not add curtains, blinds, extra objects, light beams, fog, text or watermarks. Output one complete image with the original framing.
```

## 2026-10-20 investment_office tower GPT v2：白天陰雨（待評鑑）
- 使用者要求：改成白天，陰雨天。沿用 blender-view-restyle／imagegen 局部編輯。
- 唯一輸入：`references/scenes/investment_office/cameras/cam_tower_wide_low_angle_empty_gpt.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_tower_wide_low_angle_empty_gpt_v2.png`（原生1672×941 RGB PNG，未裁切拉伸）。
- 工具／供應商：內建 image_gen／OpenAI，1次；確切模型、預估與實際費用未知。
- 原生來源：`C:/Users/servi/.codex/generated_images/01a159df-3937-74b0-8ef7-c920e67e4b7c/call_d725f8870e904b0795d0bbac523e0abb.png`。
- 驗證：完整解碼與來源／複本SHA256一致（9a509320c3405b1bc883e5e8dee2d01781964318ff2c3064c9f980244fed3229）；目視天空與環境已為明亮灰白陰天，雨絲／濕潤表面保留，主要樓群構圖與裁切維持，少量暖窗燈仍可見。細微反射與紋理經重繪，非像素級一致。保留v1，未改模型或manifest，待使用者評鑑。
### 完整實際 Prompt
```text
編輯這張圖片，只將時間與照明從深藍夜間暴雨改為明確的白天陰雨天。維持原圖相機、透視、完整取景、裁切、每棟建築的位置、尺度、輪廓、屋頂機房、窗格及遮擋關係，保持相同高品質電影CG材質，不重新設計城市。
天空改為白天厚重但明亮的淺灰至中灰陰雲，沒有陽光直射、藍天、夕陽或閃電。整幅由柔和漫射日光照亮，建築正面和側面清楚可見，有自然的中灰、銀灰與微冷灰藍色調，去除濃重海軍藍夜色和青藍發光。保留可見的細雨絲、濕玻璃、屋頂積水與樓間雨霧，反光改為柔和灰白天空反射，避免夜景霓虹式亮光。窗內人工燈光大幅減弱，在白天環境光下不搶眼；保留玻璃與金屬的精緻層次，暗部仍有細節。這是正在下雨的陰天日間金融區，不是黃昏或夜晚。近中景清晰，遠景輕微雨霧。
不新增或移除建築、不加人物、車輛、地標、植物、文字、標誌或水印。只輸出一張與輸入相同橫向畫幅的完整圖片。
```

## 2026-10-20 coffee_shop 其餘13機位 GPT 空景重繪（待評鑑）

工具：內建 image_gen／OpenAI，各機位1次、共13次；模型版本／費用未知。全數PNG 1672×941 RGB，完整解碼與原生檔複本SHA256一致；逐張目視無人物。共用圖2固定 clp/loc_coffee_shop_front_far.jpg。保留已確認中景v3，不更新manifest，不追加重試。以下列出各鏡完整實際提示詞。

### cam_amy_cu_emotion
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png。
觀察：主要取景、咖啡機頂四杯／下方兩杯保留；磨豆機豆粒更清楚，牆面日照陰影較強，金屬細節有重繪。
完整實際提示詞：
請編輯圖1 cam_amy_cu_emotion_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】本鏡緊框咖啡機及左側磨豆機，咖啡機頂部四杯、出水區兩杯與碟子，保留螢幕和蒸汽管，頂部層架與右側和下方椅背均被裁切。只有圖1的咖啡機區域，不補全店、窗或菜單。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_amy_mcu_45deg
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png。
觀察：主要取景與裁切保留，前杯單耳、糖罐無把手；蓋面保留底圖小孔，窗影和木紋較強。
完整實際提示詞：
請編輯圖1 cam_amy_mcu_45deg_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】斜向中近景，咖啡機和磨豆機在中上方，前景一張大椅背、右側一把椅子、左下部分糖罐和杯碟。維持咖啡機頂四杯及出水區兩杯，上方層架被裁切；保留所有截斷。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_amy_ms_15deg
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_amy_ms_15deg_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_amy_ms_15deg_empty_gpt.png。
觀察：主要吧台構圖、前景兩杯方向與平木蓋保留；咖啡機出水區小杯疑似新增另一側杯耳，磨豆機顯示文字變動，暖光較強。
完整實際提示詞：
請編輯圖1 cam_amy_ms_15deg_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】斜向吧台中景，左甜點櫃、中間水龍頭、右咖啡機和磨豆機，前景左下桌上兩杯與糖罐，右側大椅背。右前杯耳位於杯後方而非側邊，不補出側耳；左下杯耳保持圖1方向與裁切。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_amy_ots_george
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png。
觀察：主要空過肩取景與前景杯耳方向保留、糖罐無把手；頂部盆栽新增垂落枝葉，日照較強，咖啡機杯耳及數字有細微變化。
完整實際提示詞：
請編輯圖1 cam_amy_ots_george_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】朝向吧台的空過肩機位，咖啡機與磨豆機位於左上，畫面右半木牆、前景中央大椅背，底部兩杯（遠杯耳朝左、近杯耳朝右）和左糖罐，右邊另有被截斷桌椅。維持圖1視角，不加入肩膀。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_coffee_insert_low45deg
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_coffee_insert_low45deg_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_coffee_insert_low45deg_empty_gpt.png。
觀察：單杯特寫與杯耳左後朝向保留，無額外側耳；奶泡圓環細化，杯內原白色連接突起仍在，木紋與日照加強。
完整實際提示詞：
請編輯圖1 cam_coffee_insert_low45deg_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】桌上單杯近特寫，杯碟位於正中偏右佔大部分畫面，杯耳沿圖1朝左後方，後方椅腳與木地板、左邊被裁切糖罐邊緣。咖啡表面保留簡單圓環泡沫，用自然奶泡質感細化而非新增拉花；杯內白色連接處不是湯匙，不新增湯匙或第二杯耳。不要拉遠或補出店內全景。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_george_cu_emotion
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png。
觀察：綠柱、窗框、局部畫框與兩椅背裁切保留；窗外新增大量葉片且店面細節變動，未完全遵守不增植物；牆紋與受光加強。
完整實際提示詞：
請編輯圖1 cam_george_cu_emotion_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】窗邊極緊近景，左窗玻璃與木框，右橄欖綠柱面與右上被截斷畫框，左下高腳椅背及最底緣另一椅背。保留窗外原有店面輪廓，不增加植物、人、杯子、桌面或完整畫框，不拉遠。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_george_mcu_45deg
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png。
觀察：室內窗框、綠柱、椅背與底緣杯罐裁切保留，BOOKS文字保留；窗外新增左側枝葉／店內細節，右盆栽仍偏幾何，木蓋保留小孔且無把手。
完整實際提示詞：
請編輯圖1 cam_george_mcu_45deg_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】朝窗邊的中近景，左窗外既有BOOKS店面、中央綠柱與上緣截斷植物畫、前後兩個椅背，右窗小盆栽，底緣部分咖啡杯和最右糖罐。保留BOOKS原文字及視角、截斷位置，不移植圖2室內全景。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_george_ms_15deg
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_george_ms_15deg_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_george_ms_15deg_empty_gpt.png。
觀察：主要窗邊配置、兩盆栽及筆電、前杯朝向與平木蓋保留；窗外枝葉增多、葉形及高光改變，畫面暖陽較強。
完整實際提示詞：
請編輯圖1 cam_george_ms_15deg_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】朝窗邊的中景，左高腳椅和大綠柱，右後窗邊高桌上兩盆栽、筆電及一杯，兩張高腳椅，前景桌椅與兩杯一糖罐。保留前杯朝左前方的單杯耳及最右杯的截斷，不移動窗或家具。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_george_ots_amy
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png。
觀察：主要窗邊空過肩裁切、前景杯耳左右方向與無把手木蓋保留；窗外增加葉叢、店面細節重繪，綠柱光影更強。
完整實際提示詞：
請編輯圖1 cam_george_ots_amy_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】朝窗的空過肩視角，窗與窗外店面佔左上，右半大片綠柱、右上植物畫被裁切，前景和後方高腳椅重疊，下緣桌面左杯耳朝左、右近杯耳朝右，糖罐在右後方。保持窗外招牌裁切，不加人物肩膀。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_notebook_insert_high45deg
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_notebook_insert_high45deg_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_notebook_insert_high45deg_empty_gpt.png。
觀察：斜俯桌面、兩杯位置方向與裁切保留，未加筆記本；奶泡圓環仍較硬，木紋及窗影加強，杯內原白色突起保留。
完整實際提示詞：
請編輯圖1 cam_notebook_insert_high45deg_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】高角度桌面近景，左上被截斷杯碟，右上偏中央另一杯碟，上緣只有一段糖罐，大片木桌面橫斜佔據畫面、右下椅墊、少量木地板及下方黑色桌腳。雖名稱有notebook，底圖沒有筆記本或筆，不添加。兩杯耳方向按圖1，保留簡單圓環奶泡，不新增湯匙。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_table_insert_top
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_gpt.png。
觀察：俯拍兩杯位置、左杯耳朝下／右杯耳朝上及無把手木蓋保留；木蓋保留小孔，奶泡圈仍較硬，木紋與窗影加強。
完整實際提示詞：
請編輯圖1 cam_table_insert_top_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】垂直俯拍桌面，左下白杯與碟、右上白杯與碟，上方中央白糖罐，左右邊緣只有椅墊局部。左杯單杯耳朝畫面下、右杯單杯耳朝畫面上，嚴格維持，不改為左右側耳，不新增湯匙；咖啡維持簡單圓環奶泡，不加新拉花。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_twoshot_mws_45deg
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_twoshot_mws_45deg_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_twoshot_mws_45deg_empty_gpt.png。
觀察：主要斜側家具構圖保留，但左上木牆被改成綠牆，兩糖罐新增把手，前後桌右杯新增側耳、前桌左杯疑似雙耳；未通過細節要求，僅保存待評鑑。
完整實際提示詞：
請編輯圖1 cam_twoshot_mws_45deg_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】斜側中廣景，前景中央桌子兩杯與糖罐、左右木椅，左後另一桌、右後吧台、水槽、甜點櫃、咖啡機與磨豆機，上方架上白色罐狀物維持原數量種類，不換為杯組。底圖的各杯耳朝向必須保留，右杯耳被杯身遮擋就不要補出。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

### cam_twoshot_wide_level
有序輸入：圖1 references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_blender.png；圖2 clp/loc_coffee_shop_front_far.jpg。輸出：references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt.png。
觀察：主要正面全景與四畫、三菜單橫線及層架罐狀物保留；中央前後桌杯耳改為朝左右、糖罐新增把手，甜點形狀／排列變化，未通過細節要求。
完整實際提示詞：
請編輯圖1 cam_twoshot_wide_level_empty_blender.png，將本機位空景轉成圖2 loc_coffee_shop_front_far.jpg 的高質感3D動畫美術。圖1唯一決定機位、方向、透視、構圖、裁切、物件位置數量尺度與遮擋；圖2只供材質、色彩、光影與氣氛。不要重新生成圖2，不採圖2的拍攝角度、消失點或家具排列。
【保留】保持圖1全部主要結構、窗格、立柱、家具、設備與植物輪廓；不旋轉、鏡像、拉遠、拉近，不補被裁切的部分，不移植畫外物件。杯子為素白、無圖案，每杯只有一個杯耳，方向和可見輪廓嚴格按圖1；正面窄條是杯耳的端面，保留它且不得再補側邊C形耳。被杯身遮住的耳維持遮擋。糖罐保持白色瓶身，使用平滑木質圓片蓋，無把手、無旋鈕、無突出中心。
【美術】匹配圖2蜂蜜色自然木材、低飽和橄欖綠牆柱、柔和乳白釉陶瓷、清透玻璃、細緻金屬和暖陽。改善木紋尺度、粗糙度、接縫、倒角高光、接觸陰影和合理反射，乾燥緞面而非濕亮或塑膠。依圖1本機位朝向和光源形成合理陰影，不複製圖2畫面上的光斑，不額外加強飽和、橙色或泛光。已有植物僅在原體積內細化葉片與透光，不新增植物或藤蔓。保留近中景細節，不額外增加散景。
【本鏡畫面】正面全景，左窗和綠柱、窗邊高腳桌椅，中央前後兩桌與四木椅，右L形吧台、甜點櫃、咖啡機、層架、三塊菜單，四幅植物畫與吊燈。維持底圖各物件數量位置：層架的白色罐狀物仍是圖1原物件，不照圖2換成杯子；菜單保留原標題COFFEE與既有橫線，不發明新文字。中央桌左杯只保留朝鏡頭的窄杯耳，對面杯耳被遮擋則不新增側耳。
【輸出】零人物、人體、手臂、肩膀、人物倒影或剪影。只輸出一張與圖1一致16:9的高解析度完整圖片，無拼貼、字幕或水印。

## 2026-10-20 staff_office 廣角空景 GPT v2（待評鑑）
- 流程：skills/kj/blender-view-restyle.md；kj-cinematic 場景機位外觀局部生成。
- 工具／供應商：內建 image_gen／OpenAI；1 次生成；確切模型與費用未知。
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_blender.png ② D:\Dropbox\_AI動畫製作_ESG\B0_MJ圖\Amy辦公區\Amy座位0.png
- 輸出：references/scenes/staff_office/cameras/cam_office_wide_level_empty_gpt_v2.png；1672×941 RGB PNG。原無版本號 GPT 圖保留。
- 原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\call_195212b185474809a323a9253994288a.png
- 驗證：完整解碼成功，來源與副本 SHA256 相同：1749DF007319D1D37FA3906F2939B5CD6AD09CA98512A578FA7B66AE6D8DCB5A。
- 目視：無人物，主要隔間／走道／螢幕／書櫃／門及裁切保留。布面、地毯、窗外建築與日光細節提升；天花板新增通風口，植物葉片更茂密，百葉窗投影更明顯；非像素級幾何一致。未追加生成、未更改模型／manifest／採用設定。
### 完整實際 prompt
```text
請編輯圖 1，將這張 Blender 空景提升為圖 2 的高質感電影級辦公室場景背景，細緻而自然的寫實材質與精緻3D美術。圖 1 cam_office_wide_level_empty_blender.png 是唯一的取景、透視、物件配置與遮擋依據。圖 2 Amy座位0.png 僅供美術表現參考，不移植其構圖、建築／家具排列、植物配置或人物。不要重新生成圖2。色彩與光影採用圖2的低飽和青綠布面隔板、暖淺木桌面、米白牆壁與金屬框、灰色細織地毯，柔和暖日光與中性室內頂燈、窗外偏冷的城市建築，營造平靜自然的辦公室氣氛。讓暖光依圖1窗戶位置合理進入，不將圖2光斑直接貼過來。
【保留本機位】維持圖1的16:9畫幅、觀看方向、消失點、主要結構與遮擋。保留本鏡可見所有窗戶與百葉窗分格、立柱、右後方木門與門把、地面邊界、天花板格線及燈具的位置與排列。隔間、螢幕、座椅、書籍、書櫃、佈告板及植物的位置、數量、尺度與主要輪廓保持圖1。不旋轉相機、不鏡像、不拉遠或拉近，不移植參考圖中本鏡畫外的物件。不為了展示完整物件而補出被裁切部分。
【材質與細節提升】沿用圖1構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。青綠隔板呈現細密織物而非粗糙噪點，淺木桌面有自然細木紋，白色框架具有細膩烤漆與柔和高光，灰色方塊地毯有細密纖維與原本交錯拼接方向，螢幕保持原有黑色，黑色辦公椅保持原造型並改善材質細節。書櫃原有書本呈現真實紙張與書脊質感。植物保留位置、數量、主要枝幹及體積，細化薄葉、葉脈與透光，不新增植物。保持乾燥霧面表面，不加鏡面地板、不添加髒污。不搬入圖2的便條紙、紙堆、筆筒、額外設備、櫃體或家具。作為後續加入人物的背景母圖，近中遠景保持可用細節，不額外強化散景。
【本鏡畫面】廣角平視看向辦公區後牆，左側及中央是多排青綠低隔間，前景左半部是大型橫向隔板及其後黑色螢幕和椅背；中央偏右的灰色地毯走道向後牆收束，右側另有隔間及被畫框裁切的木桌。後牆中央偏右有兩座相鄰低書櫃，右後方有木門，左側與後牆、右牆都有大型百葉窗，天花板格線構成明確透視。精確保持前景隔板上緣、走道寬度、後牆書櫃與右後木門的相對關係。
【空景與輸出】零人物，不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。只輸出一張與圖1一致16:9比例的高解析完整圖片，不製作拼貼，不加字幕、標誌或水印。
```

## 2026-10-20 investment_office 共用美術採用及其餘10張室內空景

- 使用者明確採用 `references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_gpt_v2.png` 作為室內共用美術參考：簡報時調暗人工照明、窗外陰天白晝、投影幕保持明亮。此選定不代表全部人物分鏡已採用。
- 本批10張均直接參照上述v2；大樓外觀不在室內照明範圍。內建 image_gen／OpenAI，每鏡1次，共10次；確切模型及費用未知。所有原圖與Blender底圖保留；新生成各鏡待評鑑，不自動修改asset_manifest或scene_plan。

### cam_harrison_cu_emotion
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_harrison_cu_emotion_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_harrison_cu_emotion_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-9c7b6dc8-eb1f-4a2e-8e75-51ca75008f8b.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。椅背與窗框主要位置保留，皮革紋理較強；窗外亮窗及玻璃反射增加。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：極近距離正對一張棕色椅背，椅背佔下方大部，底端裁切；背景為窗框和辦公樓，右側灰白區域。嚴格保留椅背大小和頂緣高度，無桌面、無投影幕，不補椅腳。
```

### cam_harrison_mcu_45deg
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_harrison_mcu_45deg_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_harrison_mcu_45deg_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-e3905267-76e3-4f91-b4cb-53b6edc80a08.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。中央椅背、右側裁切椅、窗框保留；窗外遠景建築與亮窗較底圖豐富。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：中近距離正對一張高背椅，椅背中央、底部裁切，後方落地窗與大樓，右側畫框只露另一張椅子的側面，右下少量桌邊。保留窗框、窗外樓體大小及右側裁切。
```

### cam_harrison_ots_analyst2
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_harrison_ots_analyst2_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_harrison_ots_analyst2_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-24225335-26f5-4423-8098-d45fd8f21737.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。三張椅背與桌面窄帶保留；窗外樓體表面、遠景城市及反射新增細節。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：橫向隔桌望向落地窗；中間偏右完整上部椅背，左右邊緣各裁切一張椅背；桌面僅佔畫面下方窄帶。背景窗格、中央較矮樓體及灰色天空維持原位置，不加入人物或過肩。
```

### cam_sandy_cu_emotion
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_sandy_cu_emotion_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_sandy_cu_emotion_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-2a8e44a1-35a5-49cc-a886-04b2c31ffe8a.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。空牆、左木面、右黑邊保留，未新增家具；牆面局部光照較底圖明亮。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：極近景只有大面積灰色牆面、左側窄幅深棕木面及最右側黑色直邊。保持極簡空牆構圖和所有邊界位置，不加家具、投影畫面、窗戶、裝飾、門把或燈具。僅細化霧面牆漆及細木紋，保留柔和簡報照明。
```

### cam_sandy_mcu_15deg
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_sandy_mcu_15deg_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_sandy_mcu_15deg_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-3660397c-a311-4a1d-bc2b-53ccab75ca3f.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。牆面／木面／局部幕框構圖保留，投影表格仍為裁切；文字與紋理經重繪。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：近景以灰牆為主，左側深棕木面，最右側是裁切的投影幕黑框和資產表格一小段。維持牆／木面分界、幕框位置及投影文字裁切，不補完整幕，不加門把或家具。
```

### cam_sandy_ms_15deg
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_sandy_ms_15deg_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_sandy_ms_15deg_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-f14e751f-e91e-4f72-b476-ed13ae3c949a.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。雙門把及局部投影表格保留；幕下接觸陰影較強，字型細節經重繪。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：中景灰牆，左側深棕門板和兩根長直金屬門把，右側裁切投影幕財務表格及下方黑色幕框。保留門把位置、投影表格文字及數字，不補出完整幕或新家具。
```

### cam_sandy_mws_front
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_sandy_mws_front_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_sandy_mws_front_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-a16a1080-9148-4804-b156-656d5a62e485.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。投影四區圖表、左椅、門把及右下筆電保留；左上新增一個嵌燈，左緣木面與底部踢腳線細節改變，待評鑑。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：正面中廣景，投影幕佔上中部大範圍，完整四區財務圖表與黑框；左邊雙門把及裁切椅子，底部窄桌面，右下裁切筆電黑螢幕。保留原構圖及所有圖表／文字；室內較暗但投影清晰。
```

### cam_sandy_ots_harrison
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_sandy_ots_harrison_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_sandy_ots_harrison_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-050d3e6a-0f15-4e05-ad52-6c6461ebbf88.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。前景椅背遮擋、筆電與斜向投影幕保留；桌面局部反光較強、圖表細字經重繪。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：斜向望向投影幕，畫面右前景巨大裁切椅背遮擋部分桌面／筆電／幕，左後方一張椅子與木門、雙門把；桌面斜向延伸，頂部木格柵。保留前景遮擋與原有財務圖表，不露出被椅背遮擋的區域。
```

### cam_table_insert_iso
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_table_insert_iso_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_table_insert_iso_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-efd79926-820a-4bb1-948b-3033ed4d6cb4.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。斜向桌邊及左上椅面／扶手裁切保留，空桌未添道具；木紋與亮暗分布重繪。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：俯斜角桌面插入鏡，木桌佔絕大部分畫面，左上角僅少量棕色椅面和弧形金屬扶手，桌邊斜向。維持木紋方向、桌邊角度與原裁切，不放筆電、文件、手或其他配件；採同場景較暗而細節可讀的簡報照明。
```

### cam_table_insert_top
- 有序輸入：1. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_table_insert_top_empty_blender.png`；2. `D:\Dropbox\kj-om-projects\course-51-esg\references\scenes\investment_office\cameras\cam_threeshot_wide_level_empty_gpt_v2.png`。
- 輸出：`references/scenes/investment_office/cameras/cam_table_insert_top_empty_gpt.png`；原生圖：`C:\Users\servi\.codex\generated_images\01a159dc-73fa-7290-884d-4831251087e3\exec-90c8eab2-21d6-483d-8d89-7cad4ce88a20.png`。
- 驗證：1672×941 RGB PNG 完整解碼、複本SHA256通過；零人物。較窄椅面露出量及木桌裁切大致保留，未添道具；木紋與光照非像素級一致。
```text
Use case: style-transfer. 請編輯圖1，將本機位 Blender 空景轉成與圖2同一套高質感寫實室內美術。圖1唯一決定相機、透視、構圖、裁切、物件位置、數量及遮擋。圖2 cam_threeshot_wide_level_empty_gpt_v2.png 是使用者核准的共用美術參考，只提供材質、色彩和簡報燈光，不得移植其廣角構圖、可見範圍、家具或投影幕到圖1。不要重新生成圖2。
匹配圖2調暗的室內簡報照明：低亮度人工照明、灰色牆面、自然棕木與棕褐皮革、克制金屬反射；窗外仍是陰天白晝，窗光為柔和冷灰漫射，不改成夜景。若圖1可見投影幕，保留原有圖表／文字與明亮投影；依圖1實際朝向重新形成合理光影，不貼圖2光斑。不逐張增加亮度、暖色、飽和度或泛光。保留圖1門窗分格、建築輪廓、家具及設備形狀與尺度，改善木紋、皮革細紋、接觸陰影、粗糙度及細微倒角，不新增物件或配件，不補全畫外部分，不移動相機。牆面保持乾燥霧面，玻璃反射自然；背景可用細節清楚，不額外強化景深。零人物、身體部位、人體倒影與剪影。只輸出一張16:9完整高解析度空景，不拼貼、不加字幕水印。
本鏡畫面：俯視桌面插入鏡，木桌佔絕大部分畫面，最上緣僅窄幅棕色椅面與少量金屬扶手。保持此機位原本較窄的椅面露出量、桌邊與木紋角度，不套用其他桌面機位，不加文件、手或配件。
```

## 2026-10-20 shot_2.1.1 GPT v1｜七圖合併參考板，待評鑑

- 配方：kj-cinematic assets／W2I；使用者指定完整 prompt，核准四張人物圖兩兩合併。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知。前次七圖請求因最多五個路徑被拒，無圖片；本次五圖生成一次。
- 輸出：assets/images/shot_2.1.1_gpt_v1.png；1672×940 RGB PNG，原生尺寸未裁切或拉伸。
- 原生來源：C:/Users/servi/.codex/generated_images/01a159eb-2377-7e83-a3a4-49a26c045ad2/exec-43893f9d-1605-4f57-b3f3-d25104573fc0.png
- 有序實際輸入：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png
  3. D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png
  4. D:/kj-openMontage/.tmp/shot_2.1.1_background_board.png
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png
- 圖3由 char_george.png／char_amy.jpeg 原尺寸左右並排（11008×3072）；圖4由 char_officelady.png／char_barista.png 原尺寸左右並排（3072×1024）；未裁切素材。其餘原圖不變。
- 驗證：完整解碼成功，來源／副本 SHA256 一致：a6a0d3982c83b5f63158935ed3a1dd98ff231edfc60e5e6493f393c04e6be5bd。
- 目視：四人入鏡，Amy 握匙在杯中、抬眼求助，George 專注聆聽；女客坐在筆電前，咖啡師局部入鏡。主要佈景保留，但主角較 blocks 向內靠且前傾，George 手部改變，咖啡師可見範圍增加；構圖非精確保留，待使用者評鑑。未重試、未更新 manifest 採用。

### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt_v3.png：咖啡館場景外觀參考。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖與人物佔位參考。
圖 3 shot_2.1.1_leads_board.png：左半部為 char_george.png 的 George 外觀，對應圖 2 左側藍色人物；右半部為 char_amy.jpeg 的 Amy 外觀，對應圖 2 右側紅色人物。
圖 4 shot_2.1.1_background_board.png：左半部為 char_officelady.png 的背景女客外觀，對應圖 2 左後方紫色人物；右半部為 char_barista.png 的咖啡師外觀，對應圖 2 最右緣綠色人物。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、人物佔位、整體大小、可見範圍與遮擋關係。維持人物與桌面的距離、頭頂留白及畫面邊緣裁切。

將四個定位人物替換為對應角色，人物外觀、服裝及自身頭身比例採用圖 3 與圖 4 的對應角色區域，不採用參考圖的展示姿態或排版。人物坐入既有座椅，只呈現圖 2 中可見的身體部位；右緣咖啡師維持局部入鏡，不補出完整身體。

將場景材質、風格與光影更新為圖 1 的外觀，保留溫暖日光、木質牆面與植物掛畫，不改變圖 2 的空間配置。

咖啡杯碟與糖罐採用圖 5 的外觀，數量、位置與比例依圖 2。每只杯子只有一個杯耳，糖罐為白瓷罐身與木蓋。圖 5 的多視角展示不代表增加道具。

畫面描述：
這是一張坐姿近眼高、輕微俯拍的雙人中景，40mm 視角。George 在畫面左側、Amy 在右側，隔著木桌相向而坐，兩人的頭部、上半身、前臂與桌面清楚可見，下半身依圖 2 裁切。

Amy 眉心微皺，帶著焦急求助的神情，抬眼望向 George，嘴唇微張。一手握著小匙，匙端浸在面前的拿鐵中，呈現攪拌中的一個瞬間；咖啡杯仍放在原來的杯碟上。只調整完成握匙所需的手指、手腕與前臂，其餘肩膀、軀幹與坐姿沿用圖 2。

George 神情沉著、專注看著 Amy，雙手自然維持圖 2 的桌邊位置，面前的咖啡杯仍在杯碟上。

左後方女客維持坐在窗邊筆電前的姿態，右緣咖啡師維持站在吧台後的局部身影。背景人物的位置、朝向與遮擋依圖 2，不移到前景。畫面共四人，其中咖啡師僅局部可見。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


## 2026-10-20 shot_2.1.2 GPT v1｜待評鑑

- 配方：kj-cinematic assets／W2I；沿用使用者指定 prompt 與五張參考圖。
- 工具／供應商：內建 image_gen／OpenAI；生成1次，確切模型與費用未知。
- 輸出：assets/images/shot_2.1.2_gpt_v1.png；1672×941 RGB PNG，原生尺寸未裁切或拉伸。
- 原生來源：C:/Users/servi/.codex/generated_images/01a159eb-2377-7e83-a3a4-49a26c045ad2/exec-d26e279d-8dd1-4815-a405-ec230e2fb2ae.png
- 有序輸入：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png
  3. D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png
- 圖3沿用 George／Amy 原圖左右並排參考板，未裁切內容。
- 驗證：完整解碼與來源複本 SHA256 核對通過：15d4c07383085423b069a769f3b1171195081289c1f6046d87b256372e0ecfc1。
- 目視：Amy 焦慮、望向左方與攤手成立，只有 Amy 臉孔可見；頭頂留白減少，George 擴大為明顯左下肩膀前景，咖啡師可見範圍增加，糖罐木蓋有孔且缺少參考圖旋鈕。未完全符合構圖／道具要求，待評鑑；未重試、未改 manifest 採用。

### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖與人物佔位參考。
圖 3 shot_2.1.1_leads_board.png：左半部為 George，對應圖 2 左下角極小的藍色局部；右半部為 Amy，對應圖 2 中央紅色人物。
圖 4 char_barista.png：咖啡師外觀，對應圖 2 最左緣綠色身體局部。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、整體大小、可見範圍與遮擋關係。保持 Amy 頭頂留白、身體與椅背的位置，以及桌面在畫面下緣的裁切。

將紅色定位人物替換為圖 3 右半部的 Amy，外觀、服裝與自身頭身比例依人物參考，不採用參考板的展示姿態或構圖。

George 僅替換圖 2 左下角原有的極小可見局部，衣料採用圖 3 左半部的對應服裝；不得擴大為過肩前景，不補出頭部、臉孔或完整肩膀。

左緣綠色定位人物替換為圖 4 咖啡師的對應服裝，只保留圖 2 已入鏡的身體局部，不補出頭部或臉孔。

將場景材質、風格與光影更新為圖 1 的外觀，保留溫暖日光、原木牆面、吧台、磨豆機與咖啡機，不改變圖 2 的空間配置。

畫面下緣的咖啡杯碟與糖罐採用圖 5 的外觀，位置、比例及裁切依圖 2。杯子只有一個杯耳，糖罐為白瓷罐身與木蓋；不因參考圖呈現多個視角而增加道具。

畫面描述：
這是一張坐姿近眼高、微側拍的 Amy 中特寫，65mm 視角。Amy 坐在畫面中央略偏右，頭部與上半身為主體，前臂及桌面僅在畫面下方局部可見。George 留在左下角極小的前景範圍，咖啡師只在最左緣露出身體局部。全畫面只有 Amy 的臉可辨識。

Amy 已停止攪拌，眉心皺起、嘴角微微下垂，嘴唇微張，頭略微偏斜，眼神望向畫外左側對坐的 George，呈現對 ESG 完全摸不著頭緒、擔心工作績效的焦慮與無奈。

在原本下方可見的手部範圍內，一手微微鬆開、掌心略向上，呈現小幅無奈攤手的瞬間，不抬到胸口或臉旁。僅調整表情、頭部微傾及必要的手腕與手指，肩膀、胸口與軀幹維持圖 2 朝向對坐者的姿態，不轉身回望鏡頭。咖啡杯仍放在原杯碟上，不舉杯。

焦點落在 Amy 的眼睛與表情，背景適度柔化，仍能辨識咖啡機、磨豆機與木牆。除上述表演調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


## 2026-10-20 shot_1.1.1 GPT v1（待評鑑）

- 圖片：`assets/images/shot_1.1.1_gpt_v1.png`
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知。生成一次，未重試。
- 有序參考圖：
  1. `references/scenes/investment_office/cameras/cam_tower_wide_low_angle_empty_gpt_v2.png`
  2. `references/scenes/investment_office/cameras/cam_tower_wide_low_angle_block_blender.png`
- 驗證：1672×941 RGB PNG，完整解碼與來源複本 SHA256 相符。白天陰雨、冷灰藍樓群、高空微俯視及中央後方上部會議室微光成立；前景窗燈與室內細節增加，局部屋頂與立面有重繪差異。待評鑑，未改 manifest 採用。

完整 prompt：

```text
參考圖說明：
圖 1 cam_tower_wide_low_angle_empty_gpt_v2.png：倫敦金融區場景外觀參考，提供白天陰雨、建築材質、風格與光影。
圖 2 cam_tower_wide_low_angle_block_blender.png：構圖底圖，提供建築位置、比例、透視、取景與遮擋關係。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、建築配置、顯示範圍與前後遮擋關係。將場景材質、風格與光影更新為圖 1 的外觀，不採用底圖的簡化材質。

保留圖 2 中央後方階梯狀玻璃金融大樓上部既有的亮燈會議室位置，使其透出克制、柔和的室內微光。不要將會議室移到前景大樓，也不要擴大成整層強烈發光。

畫面描述：
這是一張從高空微俯視倫敦金融區的大遠景，呈現鏡頭尚未向目標大樓推進的起始畫面。中央後方的目標金融大樓由兩側及前景高樓包圍，建築高度、屋頂裁切與互相遮擋均沿用圖 2；透過樓群間隙可見其上部亮燈會議室。

時間為白天陰雨，灰白厚雲覆蓋天空，冷灰藍色漫射日光照亮玻璃帷幕與濕潤屋頂，細雨穿過樓群。遠處建築在薄薄雨霧中逐漸淡去，近中景仍維持清楚的結構與玻璃窗格。會議室微光形成低調的視覺焦點，整體呈現冷靜、嚴肅、帶有投資審查壓力的氛圍。

採深景深，不加入運動模糊，不突出可辨識人物。除上述材質、天候與會議室微光外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、字卡、標誌或浮水印。
```


## 2026-10-20 shot_2.2.1 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.2.1_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；生成 1 次。
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 相同。
- 目視：Amy 微皺眉、嘴唇微張、雙手未抬起；George 被擴大為左側頭肩前景，Amy 視線偏左上，人物尺度與頭頂留白偏離 blocks，背景細節重繪。未完全符合 prompt，待使用者評鑑；未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 4 char_george.png：George 人物參考圖，對應圖 2 左下角極少量可見的藍色人物局部。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將紅色定位人物替換為圖 3 的 Amy，左下角藍色定位人物局部替換為圖 4 的 George。只呈現圖 2 中可見的身體部位，不補出畫外身體，不擴大 George 的入鏡範圍。人物外觀與服裝採用人物參考圖，不採用其展示姿態或構圖，不保留紅藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留咖啡機、磨豆機、木牆、桌椅與前景杯具的相對位置及裁切。

畫面描述：
這是一張 65mm、坐姿近眼高、微側角度的 Amy 中特寫。Amy 坐在畫面中央偏右，頭部、肩膀、上半身與部分前臂可見，下半身在畫外；頭頂留白、肩膀高度與身體尺度依圖 2。George 只在畫面左下角露出極少量前景局部。

Amy 已收起開心的笑容，嘴角不再上揚，眉頭輕輕皺起，呈現務實、帶著疑問的神情。她的臉與視線朝畫面左側、坐在對面的 George，看向對方眼睛的高度，不看鏡頭、不向上望。嘴唇微微分開，像是正準備說「等一下」。雙手仍停留在圖 2 的原有位置，尚未抬手，也尚未做出搓指手勢。肩膀與軀幹維持圖 2 的坐姿。

日間溫暖自然光沿用圖 1，淺景深聚焦 Amy 的眼睛與表情，背景咖啡設備和木牆柔和虛化但仍可辨識。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外文字。
```



## 2026-10-20 shot_2.1.3 GPT v1｜待評鑑

- 配方：kj-cinematic assets／W2I；沿用使用者指定完整 prompt 與五張參考圖。
- 工具／供應商：內建 image_gen／OpenAI；生成1次，確切模型與費用未知。
- 輸出：assets/images/shot_2.1.3_gpt_v1.png；1672×941 RGB PNG，原生尺寸未裁切或拉伸。
- 原生來源：C:/Users/servi/.codex/generated_images/01a159eb-2377-7e83-a3a4-49a26c045ad2/exec-0a7ace51-a65d-4d5a-a3c4-ce13dd283f50.png
- 有序輸入：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png
- 驗證：完整解碼與來源複本 SHA256 核對通過：a4bf12a839b473162808164836dca942a7b690b1d1cfc8a8c2538facae040575。
- 目視：兩人／Amy後腦肩背／George溫和微笑、握杯柄與杯底離碟成立，碟上無重複杯，糖罐與Amy杯未露出。George較blocks偏左、頭部較大且頭頂留白減少，另一手位置改變，杯子離碟距離較指定小空隙大；構圖未精確保留。未追加生成、未更新manifest採用；尚未驗證後續W2V。

### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_george_ots_amy_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_george_ots_amy_block_blender.png：構圖與人物佔位參考。
圖 3 char_george.png：George 外觀，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 外觀，對應圖 2 右前景紅色人物。
圖 5 prop_coffee_cup.png：白瓷咖啡杯與杯碟外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、整體大小、可見範圍與遮擋關係。維持 George 的頭頂留白、與桌面的距離，以及 Amy 頭肩在右前景的佔比與裁切。

將藍色定位人物替換為圖 3 的 George，紅色定位人物替換為圖 4 的 Amy。人物外觀、服裝與自身頭身比例依人物參考，不採用參考圖的展示姿態或構圖。人物坐入既有座椅，只呈現圖 2 中可見的身體部位。

將場景材質、風格與光影更新為圖 1 的外觀，保留木框大窗、墨綠牆柱、植物掛畫與日間暖陽，不改變圖 2 的空間配置。圖 1 是空景，人物置入後應依圖 2 遮擋背景與桌面；不要為了展示空景中的另一只杯子或糖罐而移動 Amy 或重新安排道具。

George 的咖啡杯與杯碟採用圖 5 的外觀。杯子只有一個杯耳，杯碟維持圖 2 的桌面位置與比例；參考圖中的多個視角不代表增加杯子。

畫面描述：
這是一張從 Amy 肩後看向 George 的過肩鏡頭，60mm 視角，坐姿近眼高、輕微俯拍。George 位於畫面左側中景，臉部、上半身及桌邊手部可見；Amy 的後腦、頭髮與肩背佔據右前景，保持圖 2 的遮擋範圍，不轉頭露出正臉。畫面只有兩人。

George 神情沉著，帶著溫和安撫的微笑，視線看向對坐的 Amy。一手握住面前原有咖啡杯的杯柄，杯子保持直立，停在原杯碟正上方，杯底與碟面之間留有清楚可見的小段空隙，呈現準備放回杯碟的瞬間。杯碟留在桌上，碟上不留第二只杯子，咖啡不灑出。

只調整握杯所需的手指、手腕與前臂，其餘肩膀、胸口、軀幹及另一隻手沿用圖 2；此刻不另外攤手。Amy 維持面向 George 的聆聽姿態，頭肩不額外轉動。

焦點落在 George 的眼睛、表情與持杯的手，Amy 的前景頭肩及窗外景物適度柔化，仍保留清楚的輪廓與空間層次。除上述持杯與表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


## 2026-10-20 shot_1.1.2 GPT v1（待評鑑）

- 圖片：`assets/images/shot_1.1.2_gpt_v1.png`
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知。一次生成，未重試。
- 配方：W2I；完整沿用使用者核准的 prompt 與五張參考圖。
- 有序參考圖：
  1. `references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_gpt_v2.png`
  2. `references/scenes/investment_office/cameras/cam_threeshot_wide_level_block_blender.png`
  3. `clp/char_sandy.jpeg`
  4. `clp/char_harrison.jpeg`
  5. `clp/char_analyst2.jpg`
- 驗證：1672×941 RGB PNG，完整解碼與來源複本 SHA256 相符。目視三人數量、Sandy 指圖／持簡報器、Harrison 抱臂及 Analyst 2 朝投影幕成立；室內調暗與窗外陰天保留。相對 blocks，Sandy 頭頂提高、Harrison 輪廓與椅背較偏右，人物比例與椅位有變化；玻璃倒影與圖表細字有重繪差異。待使用者評鑑，未更新 manifest 採用。

完整 prompt：

```text
參考圖說明：
圖 1 cam_threeshot_wide_level_empty_gpt_v2.png：會議室場景外觀參考。
圖 2 cam_threeshot_wide_level_block_blender.png：三人全景構圖底圖。
圖 3 char_sandy.jpeg：Sandy（char_sandy）人物參考，對應圖 2 後方投影幕左側的紅色人物。
圖 4 char_harrison.jpeg：Harrison（char_harrison）人物參考，對應圖 2 右側靠窗的藍色人物。
圖 5 char_analyst2.jpg：Analyst 2（char_analyst2）人物參考，對應圖 2 左側的灰色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、三人的位置與比例，以及桌面、椅背對身體的遮擋關係。不要拉近鏡頭或放大人物。

將三個定位人物分別替換為圖 3、圖 4、圖 5 的角色。人物外觀、髮型、五官與服裝採用對應參考圖，不採用人物表的展示姿態或分格構圖。只呈現圖 2 中可見的身體部位，不補出被桌椅遮住的下半身。兩位坐姿角色直接坐入原有座椅，不新增椅子。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留胡桃木長桌、棕色皮椅、木格柵天花、投影機、左側玻璃隔間及右側落地窗。投影幕沿用圖 1 的財務圖表版面、長條圖與折線圖，桌上筆電維持原位置。玻璃中的人物倒影須對應實際人物，不形成額外與會者。

畫面描述：
這是一張 26mm、會議室眼高平視的三人全景。鏡頭從長桌前端朝後方投影幕拍攝，桌面占據前景並向畫面中央延伸。Sandy 站在投影幕左側，Harrison 坐在畫面右側靠窗的原座位，Analyst 2 坐在畫面左側原座位。全場只有這三位角色。

Sandy 保持專業、專注的神情，左手抬起指向投影幕上的財務圖表，右手在腰際持簡報器，臉部略朝向 Harrison，呈現準備說明財務表現的瞬間。保留參考圖中的黑框眼鏡、棕色束髮、深色褲裝西服及藍色識別證掛繩。

Harrison 坐在既有高背皮椅內，雙臂交疊於胸前，頭部朝 Sandy 與投影幕方向，神情冷峻、目光銳利，安靜審視簡報。維持圖 2 的軀幹位置與椅背遮擋，只調整雙臂及必要的頭部角度以完成指定表演。

Analyst 2 維持左側坐姿，頭部與視線轉向後方投影幕，神情專注，呈現正在聆聽的狀態，不看鏡頭。身體與手部沿用圖 2 的可見範圍。

室內維持圖 1 為簡報而調暗的照明，投影幕明亮可辨，窗外是白天陰天的金融區高樓，冷色漫射日光由右側進入。人物受到同一場景光線照明，保留角色參考的精緻 3D 動畫質感。整體氛圍安靜、嚴肅，呈現正式投資審查現場。

採深景深，三人、桌面與投影幕均清楚可辨。除上述人物替換、表情、視線與手勢調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、額外字卡或浮水印。
```


## 2026-10-20 shot_2.1.4 GPT v1｜待評鑑

- 配方：kj-cinematic assets／W2I；使用者指定原 prompt 與三圖。
- 工具／供應商：內建 image_gen／OpenAI；生成1次，確切模型與費用未知。
- 輸出：assets/images/shot_2.1.4_gpt_v1.png；1672×941 RGB PNG，原生尺寸未裁切或拉伸。
- 原生來源：C:/Users/servi/.codex/generated_images/01a159eb-2377-7e83-a3a4-49a26c045ad2/exec-55e4c159-db03-4b2e-8689-c37bc866df6a.png
- 有序輸入：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 驗證：完整解碼與來源複本 SHA256 核對通過：95eea712479f31be9a5a7ae4e41355d456ab31bd7de3dff72dbe36383b8a5426。
- 目視：Amy單人頭肩、睜眼抬眉、微張嘴與輕微歪頭成立，視線朝畫外左側，手／桌面未入鏡，未見明顯側身回頭；頭部較blocks放大、上移，頭頂留白減少，背景局部細節有重繪差異。待使用者評鑑，未重試、未改manifest採用。

### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_amy_cu_emotion_block_blender.png：構圖與人物佔位參考。
圖 3 char_amy.jpeg：Amy 外觀，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、整體大小、可見範圍與遮擋關係。保持 Amy 頭頂留白、頭部在畫面中的位置，以及肩膀與上胸在下緣的裁切，不推近鏡頭或放大頭部。

將紅色定位人物替換為圖 3 的 Amy。人物五官、髮型、服裝與自身頭身比例依人物參考，不採用參考圖的展示姿態或排版。只呈現圖 2 中可見的身體部位。

將場景材質、風格與光影更新為圖 1 的外觀，保留日間暖陽、原木牆面、咖啡機與磨豆機，不改變圖 2 的空間配置。Amy 置入後依圖 2 遮擋身後設備，不為了展示完整咖啡機而移動人物。

畫面描述：
這是一張坐姿近眼高、微側拍的 Amy 頭肩特寫，100mm 視角。Amy 位於畫面中央略偏右，完整頭部、肩膀與部分上胸可見，手部與桌面留在畫外。畫面只有 Amy 一人。

Amy 聽到「企業健康指標」這個新比喻，眼睛因好奇與驚奇而睜大，眉毛輕輕抬起，嘴唇微張，呈現正要反問的瞬間。頭部輕微側傾，視線看向畫外左側對坐的 George，不直視鏡頭。

只調整表情、視線與輕微歪頭；肩膀、胸口及軀幹維持圖 2 朝向對坐者的姿態。頭與胸口朝向同一位對坐者，不做側身回頭的姿勢。表情帶有求知的疑惑，不張大嘴或呈現驚嚇。

焦點落在 Amy 的雙眼與面部表情，背景咖啡機、磨豆機與木牆適度柔化，仍能辨識原有環境。除上述表演調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


## 2026-10-20 shot_2.2.2 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.2.2_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；生成 1 次。
- 目視：George 左前景過肩、Amy 右中景及雙臂低放呈現；Amy 視線偏左上、嘴角略上揚，無奈表情不足。人物尺度、頭頂留白及手部可見範圍偏離 blocks，George 頭頂裁切、背景細節重繪。待使用者評鑑，未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_amy_ots_george_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 4 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將紅色定位人物替換為圖 3 的 Amy，藍色定位人物替換為圖 4 的 George。只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用人物參考圖，不採用其展示姿態或構圖，不保留紅藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。桌椅、杯碟、吧台與咖啡機維持圖 2 的位置、透視及遮擋關係。

畫面描述：
這是一張 60mm、坐姿近眼高平視、從 George 身後越過肩膀拍攝 Amy 的過肩鏡頭。George 的後腦、頸部、肩背與部分手臂佔據左前景，左側及下方由畫面邊緣裁切，保持圖 2 的前景大小，不轉頭露出正臉。Amy 坐在右側中景，頭部、上半身與桌邊部分手臂可見，下半身在畫外。兩人隔桌對坐，保留圖 2 的人物間距、Amy 頭頂留白及前後景比例。

Amy 眉心輕皺，嘴角略微下壓，嘴唇微張，呈現冷靜、務實又有些無奈的神情，像是正準備解釋公司對成本的現實考量。她的頭部朝向畫面左側對坐的 George，視線落在對方眼睛的高度，不看鏡頭、不向上望。

這是雙手攤開之前的起始瞬間。Amy 的雙臂仍低放在桌邊，沿用圖 2 的位置，手指自然放鬆，尚未將雙手抬起或向兩側展開。被 George 前景遮住的手部維持遮擋，不為展示雙手而移動人物或改變取景。肩膀與軀幹維持圖 2 的坐姿。杯子留在桌面杯碟上。

沿用圖 1 的日間暖陽與木質咖啡館氛圍。淺景深聚焦 Amy 的眼睛與表情，George 的前景頭肩及後方咖啡設備柔和虛化，仍保留清楚的輪廓與空間層次。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、角色標籤或參考圖分格。
```


驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。


## 2026-10-20 staff_office 其餘10機位：以已確認廣角v2為共用美術（新圖待評鑑）
- 使用者確認 cam_office_wide_level_empty_gpt_v2.png 為共用參考，授權其餘全部 empty_blender 重繪；每鏡直接使用同一v2，未串接新圖。
- 工具／供應商：內建 image_gen／OpenAI，各1次、共10次；確切模型／費用未知。全數無人物，完整解碼及來源／複本 SHA256 通過；舊版、Blender及manifest保留，未追加重試。

### cam_amy_cu_emotion v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_cu_emotion_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_cu_emotion_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-338897e6-51c7-423c-ba68-d067332b1a27.png
- SHA256：2909086b16d9989c133a4ab2fbd8d8bb9af818b16cd369b9a9507d0ce994af88；目視：保留緊裁切、椅背／螢幕／隔板位置及空景；窗外樓景、布紋與投影重繪，非像素級一致。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：緊裁切近景，上半是後牆百葉窗與中央白柱，右下書櫃與書本；前景下緣被裁切的黑色網布椅背，右側大黑螢幕，左側斜向青綠隔間。保持這些物件畫面佔比，沒有地板或天花板，不補出。
```

### cam_amy_mcu_15deg v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_mcu_15deg_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_mcu_15deg_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-c32d2ecc-2f09-465f-8f74-6f4c101dcef7.png
- SHA256：6b1d0f312715ceea5039a4658a6a83043d9f91df8aeb13be317a61ede786c07d；目視：椅背、左下螢幕、右緣盆栽及背景遮擋維持；窗外樓景及日光斑紋不同。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：近景，中央下方大型黑網布椅背，左下裁切黑螢幕，右緣裁切白盆綠植；後方青綠隔間及兩層螢幕遮擋，背景百葉窗和右側書櫃。保持椅背、隔板上緣及窗柱相對位置，不補地板或天花板。
```

### cam_amy_mcu_selfie v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_mcu_selfie_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_mcu_selfie_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-c11a81e7-0a1c-440f-b29d-62c2441209a2.png
- SHA256：edcc5ca4e0a56876ee58f418cf16e915b61e18c7418c05b0a4285354c5322441；目視：斜向隔板、桌角、椅背及兩座書櫃保留；盆栽葉形與紋理有差異。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：稍斜側近景，黑網布椅背佔中央偏右下部，左下僅一角木桌；青綠隔板橫跨畫面並有左側斜向交叉線。左後高綠植和佈告板，右後兩座書櫃、白盆綠植與一排直立書本。保留略傾的觀看角度與裁切，無人物、無自拍手機。
```

### cam_amy_ms_15deg v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_ms_15deg_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_ms_15deg_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-67b93f34-7940-477b-b4e4-15de2f698790.png
- SHA256：371980e8956f2d9564579faac32e85c2a73fc1d38ac6332f7b03609474e6d51e；目視：椅背、左前螢幕、右後盆栽與書櫃保留；百葉窗投影更明顯。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：中景，空黑網布椅居中偏右，左下大黑螢幕被畫框裁切；青綠隔板橫跨下半，後方有黑螢幕與右側盆栽書籍，背景窗戶百葉、右側書櫃、左邊一角佈告板。保持原取景，不補桌面或天花板。
```

### cam_amy_ms_45deg v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_ms_45deg_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_amy_ms_45deg_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-41e411d8-b3eb-4506-a5ac-2f3b89f70851.png
- SHA256：80047e56da8d257608329c6a7912cefa2c73377b0bc79dd380774319fe24b021；目視：空椅扶手／腰靠、鍵盤、右前四冊書及走道保留；葉片與材質重繪，非逐像素一致。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：斜側中景，中央完整可見空黑網布椅、扶手和腰靠，左前大黑螢幕，底部木桌、鍵盤，右前四冊直立書籍。右側窄走道、後方隔間、左後綠植及右後白書櫃。保持所有物件位置與遮擋，鍵盤造型與鍵列不重新設計。
```

### cam_board_ambience_front v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_board_ambience_front_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_board_ambience_front_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-175b8ce7-4ee7-4e9c-b390-83b5f85ef93d.png
- SHA256：7cae4131a469f9d1b1fc5516f3eb26548187fa6be7290fd19068c1562415c1cd；目視：兩排各五張卡片、空白標籤與中央佈告板保留；木框接角與窗外樓景變動。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：正面緊裁切佈告板特寫：淺木框白底，精確保留兩排各五張彩色矩形卡片及每張底端小白標籤，所有卡片保持空白無字。中央白牆、左右裁切百葉窗及窗外樓景。不可改成辦公區全景，無桌椅、無地面或天花板。
```

### cam_desk_insert_iso v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_desk_insert_iso_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_desk_insert_iso_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-5cac181f-b2d8-4ae5-8662-813b86d198d0.png
- SHA256：ffeaf94b79e742c0cae1a307ee9fb3d30057199c7163257d79b40cd2c032751e；目視：鍵盤、盒子、螢幕裁切與空椅保留；後方原灰白板面被改成青綠布面，與底圖有偏差。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：斜俯桌面插入特寫：木桌上斜向長鍵盤佔大半畫面，左上小長方形盒子，左緣裁切螢幕背面，右上裁切空網布椅、扶手、腰靠和坐墊，後方少量灰地毯。保持原鍵帽排列和無字狀態，不新增滑鼠或紙筆，不擴展為辦公室全景。
```

### cam_monitor_insert_front v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_monitor_insert_front_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_monitor_insert_front_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-d11a3af2-05ea-4e1f-be4f-f36e479739aa.png
- SHA256：d5e673ff663285b6e43462b485f3bfebcd9e29ec8ebe9e9f2398ca9e2a48403d；目視：黑色空螢幕及外框、底座、裁切保留，未增加UI文字或人物；背景樓景與受光不同。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：正面螢幕特寫，大黑色關閉螢幕及寬外框佔據幾乎全畫面，底部米白底座與一小段淺木桌，左邊與右邊窄幅青綠隔板及上緣少量窗戶。保留黑色空屏，不加UI、文字、圖案或人物反射；不縮小螢幕，不補出辦公室全景。
```

### cam_office_entrance_wide v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_entrance_wide_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_entrance_wide_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-fb79eb1c-226a-4152-bbb1-625a8d5db809.png
- SHA256：6b6b15693bfa1b2ba2525d215981d2d53254d19b0efd1f0148cab3fe16b862d3；目視：門板／黑門把／右側裁切書櫃與百葉配置保留；窗外新增遠處樓群、下緣地毯紋理可見，非完全不變。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：近距離入口局部構圖，中央偏右是窄長木門板及下方黑色直立門把，中央開口看見窗外兩座高樓與藍灰天空，左右窗戶百葉，右側裁切兩層白書櫃與右上佈告板。即使檔名含wide仍保持這張緊裁切，不補門框全貌、門廳、走道、天花板，不改門開啟角度。
```

### cam_office_reverse_wide v2
- 有序輸入：① D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_reverse_wide_empty_blender.png ② D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_wide_level_empty_gpt_v2.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\staff_office\cameras\cam_office_reverse_wide_empty_gpt_v2.png；1672×941 RGB PNG；原生來源：C:\Users\servi\.codex\generated_images\01a159e7-e2e0-7122-b027-67a2123cd35a\exec-442300f8-03a6-4e0d-9adc-3dc0a3ace7d4.png
- SHA256：fef9fffa014be13e068dae86dd8395df14abb8066354217d08820cc4fa885f18；目視：斜廣角、左走道、前景隔間／螢幕、書櫃及木門保留；未見新增天花通風口，日光與葉形有重繪差異。
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的場景背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_office_wide_level_empty_gpt_v2.png 是已確認共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。匹配圖2低飽和青綠細織布隔板、米白烤漆框架與牆面、淺暖木材、黑色螢幕及網布椅、乾燥灰色方塊地毯、自然暖日光與冷色城市窗景、精緻寫實3D美術；不逐張加強暖色、飽和度或泛光。依圖1窗戶朝向保持合理受光與投影，不照搬圖2的光斑。
保留圖1所有可見門窗分格、立柱、地面邊界、家具設備、書籍及植物的位置、數量、尺度和主要輪廓與遮擋。不旋轉、不鏡像、不拉遠拉近，不補全被裁切的物件，不增加畫外家具、窗戶、天花板、通風口、植栽或配件。只提升微紋理、細微倒角、粗糙度、接縫、接觸陰影及合理反射，保持原有物件種類與造型；植物只在原體積內細化葉片，不新增植物。保持霧面乾燥表面、不加髒污或鏡面地板，不加入額外紙張、便條或道具。近中景保持可用清晰度，不額外強化景深散景。
零人物，不得有人體、肩膀、手臂、人形倒影或剪影，機位名稱含Amy也只交付空景。只輸出一張16:9高解析完整圖片，不拼貼、不加字幕、標誌或水印。
本鏡畫面：斜向廣角空景，左側窄走道、白柱與高綠植，前景橫向青綠隔板、大黑螢幕和黑網布椅背，隔間交叉線延伸至右側；後方白書櫃、右後木門、環繞百葉窗及格狀天花板。保持本機位與圖2不同的方向、左側走道位置、前景裁切及原有天花燈數量，不新增通風口。
```

## 2026-10-20 shot_1.1.2 GPT v2（站位修正未通過）

- 圖片：`assets/images/shot_1.1.2_gpt_v2.png`
- 原圖／唯一輸入：`assets/images/shot_1.1.2_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；確切模型及費用未知；I2I 一次生成。
- 使用者要求 Sandy 靠近投影幕、消除腿部卡在扶手的觀感。
- 驗證：1672×941 RGB PNG，完整解碼及來源複本 SHA256 相符。Sandy 縮小，但橫向位置變化不足，下半身仍與扶手重疊；模型反而移除了她左側後方椅子的椅背，未符合保留家具要求。此版本未通過指定修正驗收，未採用或自動重試。

完整 prompt：

```text
以圖 1（shot_1.1.2_gpt_v1.png）為唯一編輯原圖，僅修正 Sandy 的站位及其直接相關的遮擋、接觸陰影與玻璃倒影。

Sandy 是投影幕左側戴黑框眼鏡、穿深色西服、掛藍色識別證的女性。現在她的腿與左側最後一張椅子的扶手重疊，看起來卡在椅子中。請將她整個人向後移到更靠近投影布幕的牆前、位於最後一張椅子後方的講解區，並略向畫面右側移，使身體位於投影幕左邊緣前方，遠離椅子的扶手與座面。她與椅子應有明確的前後距離，不可站在椅子的扶手圈內，不可穿透椅子或桌子。人物隨退後適度縮小，保持正確透視與成人身體比例；雙腳站在後方地板上，下半身若被長桌自然遮住就保留遮擋，不必刻意露出雙腳。

保留 Sandy 的五官、髮型、眼鏡、服裝、識別證、專業神情，以及左手指向圖表、右手腰際持簡報器的動作。可微調手臂角度配合新的站位，使其自然指示螢幕，不大幅遮住圖表。移走原位置的人物並恢復該處原有背景，不留下人物殘影或多餘肢體；玻璃倒影隨新站位合理更新。

其餘全部沿用原圖：固定鏡位、16:9 取景、桌子與全部椅子的位置及數量、右側 Harrison 的抱臂坐姿、左側 Analyst 2 的坐姿與視線、投影幕與財務圖表、筆電、窗外樓景、室內光線、色調、3D 動畫質感。不要移動椅子來解決穿插問題，不新增人物。輸出一張完整彩色分鏡圖，不加文字標註或浮水印。
```


## 2026-10-20 shot_2.1.4 GPT v2｜依附圖修正軀幹，待評鑑
- 工具：內建 image_gen／OpenAI，局部編輯1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.4_gpt_v2.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/assets/images/shot_2.1.4_gpt_v1.png
2. C:/Users/servi/AppData/Local/Temp/codex-clipboard-60501570-a0c2-4ea6-81ed-283cac8a1178.png
- 目視：領口、門襟與肩胸輪廓有調整，表情／頭部／背景大致保留；軀幹方向改動有限，尚不能確認已完全符合附圖方向。未追加重試，未採用。
- 根因：原prompt以blocks固定軀幹方向，不能準確表達使用者指定的新方向；本次明確以附圖肩線／胸口／領口取代原軀幹限制。
### 完整實際 prompt
```text
請局部編輯圖1（shot_2.1.4_gpt_v1.png）。圖2是使用者指定的身體朝向參考。只修正圖1中Amy的肩膀、胸口、軀幹及衣服在這些部位的透視，使其方向與圖2一致：依圖2可見的左右肩前後關係、肩線角度、胸口平面、西裝左右翻領寬度及白襯衫門襟走向，重現同樣的坐姿軀幹朝向。以圖2的實際姿態為準，不只是把頭轉向左側，也不要以圖1的原肩線為固定限制。頸部與肩膀自然連接。
圖1是唯一的成品、構圖與背景底圖。保留圖1的Amy五官、髮型、驚奇睜眼抬眉、微張嘴、輕微歪頭及朝畫外左側的視線，保留頭部大小位置、頭頂留白、原畫幅與取景、光影、咖啡機、磨豆機、木牆及椅背。圖2僅提供軀幹姿態，不移植圖2的裁切、背景佈局或人物大小。服裝仍是原灰色西裝與白襯衫，只依新軀幹方向調整衣料透視與自然褶皺。手部與桌面仍在畫外，只有Amy一人。輸出一張16:9彩色圖片，無字幕、無標籤、無分格。
```


- 驗證：(1672, 941) RGB PNG，完整解碼與來源複本SHA256通過：61d01d63559565812d8cc6ebdf1ca88d83bf3f580536e01b459dd77068ada500。原生來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-06e1ad41-f4ca-472d-8a71-e5eac12cb4b2.png

## 2026-10-20 shot_1.1.2 GPT v3（待評鑑）

- 圖片：`assets/images/shot_1.1.2_gpt_v3.png`
- 工具：內建 image_gen／OpenAI；確切模型與費用未知，生成一次。
- 完整使用使用者重新提供的 prompt，W2I 原五圖重新生成，非編輯v2。
- 有序參考圖：
  1. `references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_gpt_v2.png`
  2. `references/scenes/investment_office/cameras/cam_threeshot_wide_level_block_blender.png`
  3. `clp/char_sandy.jpeg`
  4. `clp/char_harrison.jpeg`
  5. `clp/char_analyst2.jpg`
- 驗證：1672×941 RGB PNG，完整解碼與來源複本 SHA256 相符。三人及指定手勢成立，後方椅背保留，Sandy 下半身主要由桌面遮擋；仍靠近左側扶手，未能由此圖確定雙腳與椅子的實際空間間距。人物大小、椅位、圖表與倒影有重繪差異。待使用者評鑑，未重試或更新採用。

完整 prompt：

```text
參考圖說明：
圖 1 cam_threeshot_wide_level_empty_gpt_v2.png：會議室場景外觀參考。
圖 2 cam_threeshot_wide_level_block_blender.png：三人全景構圖底圖。
圖 3 char_sandy.jpeg：Sandy（char_sandy）人物參考，對應圖 2 後方投影幕左側的紅色人物。
圖 4 char_harrison.jpeg：Harrison（char_harrison）人物參考，對應圖 2 右側靠窗的藍色人物。
圖 5 char_analyst2.jpg：Analyst 2（char_analyst2）人物參考，對應圖 2 左側的灰色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、三人的位置與比例，以及桌面、椅背對身體的遮擋關係。不要拉近鏡頭或放大人物。

將三個定位人物分別替換為圖 3、圖 4、圖 5 的角色。人物外觀、髮型、五官與服裝採用對應參考圖，不採用人物表的展示姿態或分格構圖。只呈現圖 2 中可見的身體部位，不補出被桌椅遮住的下半身。兩位坐姿角色直接坐入原有座椅，不新增椅子。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留胡桃木長桌、棕色皮椅、木格柵天花、投影機、左側玻璃隔間及右側落地窗。投影幕沿用圖 1 的財務圖表版面、長條圖與折線圖，桌上筆電維持原位置。玻璃中的人物倒影須對應實際人物，不形成額外與會者。

畫面描述：
這是一張 26mm、會議室眼高平視的三人全景。鏡頭從長桌前端朝後方投影幕拍攝，桌面占據前景並向畫面中央延伸。Sandy 站在投影幕左側(靠近投影幕)，Harrison 坐在畫面右側靠窗的原座位，Analyst 2 坐在畫面左側原座位。全場只有這三位角色。

Sandy 保持專業、專注的神情，左手抬起指向投影幕上的財務圖表，右手在腰際持簡報器，臉部略朝向 Harrison，呈現準備說明財務表現的瞬間。保留參考圖中的黑框眼鏡、棕色束髮、深色褲裝西服及藍色識別證掛繩。

Harrison 坐在既有高背皮椅內，雙臂交疊於胸前，頭部朝 Sandy 與投影幕方向，神情冷峻、目光銳利，安靜審視簡報。維持圖 2 的軀幹位置與椅背遮擋，只調整雙臂及必要的頭部角度以完成指定表演。

Analyst 2 維持左側坐姿，頭部與視線轉向後方投影幕，神情專注，呈現正在聆聽的狀態，不看鏡頭。身體與手部沿用圖 2 的可見範圍。

室內維持圖 1 為簡報而調暗的照明，投影幕明亮可辨，窗外是白天陰天的金融區高樓，冷色漫射日光由右側進入。人物受到同一場景光線照明，保留角色參考的精緻 3D 動畫質感。整體氛圍安靜、嚴肅，呈現正式投資審查現場。

採深景深，三人、桌面與投影幕均清楚可辨。除上述人物替換、表情、視線與手勢調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、額外字卡或浮水印。
```


## 2026-10-20 shot_2.1.4 GPT v3｜使用者新prompt重生，待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.4_gpt_v3.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 目視：單人頭肩、睜眼抬眉微張嘴與向左視線成立，無手部或桌面。肩胸／領口方向與前版不同，但不能僅由單張圖確認與畫外George的三維方向完全一致；頭部仍較blocks放大、頭頂留白減少。未追加生成、未採用。
### 完整實際 prompt（逐字使用使用者原文）
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_amy_cu_emotion_block_blender.png：構圖與人物佔位參考。
圖 3 char_amy.jpeg：Amy 外觀，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、整體大小、可見範圍與遮擋關係。保持 Amy 頭頂留白、頭部在畫面中的位置，以及肩膀與上胸在下緣的裁切，不推近鏡頭或放大頭部。

將紅色定位人物替換為圖 3 的 Amy。人物五官、髮型、服裝與自身頭身比例依人物參考，不採用參考圖的展示姿態或排版。只呈現圖 2 中可見的身體部位。

將場景材質、風格與光影更新為圖 1 的外觀，保留日間暖陽、原木牆面、咖啡機與磨豆機，不改變圖 2 的空間配置。Amy 置入後依圖 2 遮擋身後設備，不為了展示完整咖啡機而移動人物。

畫面描述：
這是一張坐姿近眼高、微側拍的 Amy 頭肩特寫，100mm 視角。Amy完整頭部、肩膀與部分上胸可見，手部與桌面留在畫外。畫面只有 Amy 一人。

Amy 聽到「企業健康指標」這個新比喻，眼睛因好奇與驚奇而睜大，眉毛輕輕抬起，嘴唇微張，呈現正要反問的瞬間。頭部輕微側傾，視線看向畫外左側對坐的 George，不直視鏡頭。

只調整表情、視線與輕微歪頭；肩膀、胸口及軀幹維持圖 2 朝向對坐者的姿態。頭、脖子、肩膀、胸口，都朝向對坐的George位子。表情帶有求知的疑惑，不張大嘴或呈現驚嚇。

焦點落在 Amy 的雙眼與面部表情，背景咖啡機、磨豆機與木牆適度柔化，仍能辨識原有環境。除上述表演調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


- 驗證：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：a04f803ecb8a97d585fd2f45b5be95b046edb1877d601ee614600ea313c0c057。原生來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-b3ba9677-6318-4ac1-b8e3-94e604964a1a.png

## 2026-10-20 shot_2.2.3 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.2.3_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；生成 1 次。
- 目視：Amy 單人頭肩特寫、雙手畫外、向左看及眉心微皺呈現；笑容較明顯、單側苦笑不夠清楚，視線略偏左上。人物頭部尺度／肩膀位置與頭頂留白偏離 blocks，背景設備細節重繪。待使用者評鑑，未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將紅色定位人物替換為圖 3 的 Amy，只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖，不保留紅色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留木牆、咖啡機、磨豆機、吧台與局部椅背的相對位置及裁切。

畫面描述：
這是一張 100mm、坐姿近眼高、微側角度的 Amy 單人臉部特寫。Amy 位於畫面中央略偏右，頭部、頸部、肩膀與上胸入鏡，下方由畫面邊緣裁切。頭部大小、頭頂留白、肩膀高度及背景遮擋依圖 2。畫面只有 Amy 一人，George 位於畫外，不加入他的頭肩或其他前景人物。

Amy 面朝畫面左側對坐的 George，視線自然落向畫外左側、與自己坐姿眼高相近的位置，不看鏡頭、不抬眼望向左上方。她眉心微皺，一側眉毛稍稍挑起，嘴角只有一側輕微牽起，嘴唇微張，呈現帶著無奈與自嘲的苦笑。眼神仍有對老闆反應的擔憂，笑意克制，不是開心微笑，也不是憤怒瞪視。

這是準備開口吐槽「我如果這樣去報告」的起始瞬間。雙手仍在畫面下方之外，尚未抬到臉旁，不出現指著太陽穴的手指。肩膀與軀幹保持圖 2 的坐姿，不聳肩、不轉身面向鏡頭。

沿用圖 1 的日間暖陽與木質咖啡館氛圍。淺景深清楚呈現 Amy 的眼睛、眉毛與嘴角，後方咖啡機、磨豆機與木牆形成柔和散景，仍保留可辨識的輪廓。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、角色標籤或參考圖分格。
```


驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。

## shot_2.1.4 GPT v4｜四圖姿態參考，待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.4_gpt_v4.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/assets/images/shot_2.1.4_short_v2.png
- 目視：近正面肩胸、頭頸與輕微歪頭更接近指定short_v2，驚奇反問成立；輸出亦帶入圖4的人物大小／位置與背景配置，未嚴格保留圖2的頭頂留白與背景透視。未追加重試或採用。
### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_amy_cu_emotion_block_blender.png：場景配置、人物位置與取景範圍參考。
圖 3 char_amy.jpeg：Amy 的五官、髮型、服裝與頭身比例參考。
圖 4 shot_2.1.4_short_v2.png：Amy 身體朝向與頭肩姿態的主要參考，提供肩線、胸口平面、頭頸關係及臉部觀看角度。

生圖指引：
以圖 2 為編輯底圖，保留背景透視、物件配置、Amy 的座位位置與整體畫面佔比。保持頭頂留白及肩膀與上胸在下緣的裁切，不推近鏡頭或放大頭部。

將紅色定位人物替換為圖 3 的 Amy。五官、髮型、服裝與自身頭身比例採用圖 3，不採用角色設定圖的展示姿態或排版。

Amy 的肩膀、胸口、軀幹與頭頸姿態以圖 4 為準。重現圖 4 的左右肩前後關係、肩線角度、胸口朝向、西裝翻領比例及白襯衫門襟走向。允許調整圖 2 定位人物的肩胸角度，以符合圖 4；不要只轉動頭部或眼睛。

將場景材質、風格與光影更新為圖 1 的外觀，保留日間暖陽、原木牆面、咖啡機與磨豆機，不改變背景物件位置。背景依調整後的人物輪廓自然遮擋，不為了展示完整咖啡機而移動人物。

畫面描述：
這是一張坐姿近眼高的 Amy 頭肩特寫，100mm 視角。完整頭部、肩膀與部分上胸可見，手部與桌面留在畫外。畫面只有 Amy 一人。

Amy 採用圖 4 的近正面坐姿：胸口接近朝向鏡頭，略朝畫面左側，雙肩自然展開。頭部略朝畫面左側並輕微側傾，頸部自然承接胸口方向，沒有明顯扭頸回望。左右肩的可見寬度、衣領透視與頭部相對肩膀的位置，均以圖 4 為準。

Amy 聽到「企業健康指標」這個新比喻，眼睛因好奇與驚奇而睜大，眉毛輕輕抬起，嘴唇微張，呈現正要反問的瞬間。視線看向畫外左側對坐的 George，不直視鏡頭。表情帶有求知的疑惑，不張大嘴或呈現驚嚇。

焦點落在 Amy 的雙眼與面部表情，背景咖啡機、磨豆機與木牆適度柔化，仍能辨識原有環境。

參考優先順序：人物位置與取景範圍依圖 2；人物姿態、肩胸方向與臉部角度依圖 4；人物外觀依圖 3；場景材質與光影依圖 1。人物姿態與圖 2 不同時，以圖 4 為準。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


- 驗證：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：0ee12d1fca9c61954f62468b2d1aea6aa5194bfe09bd3257c414f0b073322593。原生來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-cee29abc-5f4f-46e0-b778-040a003a92dd.png

## 2026-10-21 shot_1.1.3 GPT v1（待評鑑）

- 圖片：`assets/images/shot_1.1.3_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；確切模型與費用未知，生成一次。
- 配方：W2I；完整沿用使用者核准的 prompt。
- 有序參考圖：
  1. `references/scenes/investment_office/cameras/cam_sandy_mws_front_empty_gpt.png`
  2. `references/scenes/investment_office/cameras/cam_sandy_mws_front_block_blender.png`
  3. `clp/char_sandy.jpeg`
- 驗證：1672×941 RGB PNG，完整解碼與來源複本 SHA256 相符。單人 Sandy、左手指示／右手簡報器、張嘴匯報與完整圖表成立；前景椅子保留，扶手遮擋腿部。相較 blocks，Sandy 頭頂明顯提高、人物放大、左手指示範圍向右延伸，表情較開朗；非完全保留人物比例。圖表細字有重繪差異。待使用者評鑑，未重試或更新採用。

完整 prompt：

```text
參考圖說明：
圖 1 cam_sandy_mws_front_empty_gpt.png：會議室投影幕區域的場景外觀參考。
圖 2 cam_sandy_mws_front_block_blender.png：Sandy 與投影幕中全景構圖底圖。
圖 3 char_sandy.jpeg：Sandy（char_sandy）人物參考，對應圖 2 左側的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、投影幕與家具配置、人物佔位、比例、可見範圍與遮擋關係。不要拉近鏡頭、放大人物或增加頭部比例。

將紅色定位人物替換為圖 3 的 Sandy。五官、髮型、眼鏡、服裝與識別證採用圖 3，不採用人物表的展示姿態或分格構圖。只呈現圖 2 已入鏡的身體範圍，不補出畫面下方的雙腳。

將場景材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。投影幕沿用圖 1 的 Capital Investment Portfolio 標題、圖表版面、長條圖、折線圖及表格；保留左緣椅子局部、下緣長桌與右下角筆電的裁切範圍。

畫面描述：
這是一張 34mm、平視正面取景的單人中全景。Sandy 位於畫面左側，靠近投影幕左前方；大型投影幕占據畫面中央至右側。她的頭部、軀幹與上段腿部可見，下半身依圖 2 被前景家具及畫面下緣遮擋。

Sandy 站在投影幕前的講解區，與前景椅子保持清楚的前後關係。椅子扶手是她前方的遮擋物，不穿入她的腿部，人物不站在座椅或扶手圈內。保留原有椅子，不以刪除家具來消除重疊。

Sandy 神情自信、專業，眉眼放鬆而專注，嘴唇微張，呈現剛開始向畫外 Harrison 匯報的瞬間。她的臉部與視線略朝向畫外右側的 Harrison，不直視鏡頭；肩膀與軀幹維持圖 2 的朝向。

她的左手抬起，以自然的指示手勢朝向投影幕上的財務圖表；右手在腰際握住簡報遙控器。手臂整體方向沿用圖 2，僅調整手腕與手指使指示動作自然，不大幅遮住圖表。保留黑框眼鏡、棕色束髮、深色褲裝西服、淺色襯衫與藍色識別證掛繩。

全畫面只有 Sandy 一位人物。Harrison 與其他與會者均在畫外，不加入他們的頭部、肩膀或前景剪影。

室內保持為簡報而調暗的照明，投影幕明亮，人物臉部與服裝仍清楚可辨。光線、材質與色調依圖 1，人物保留圖 3 的精緻 3D 動畫質感。Sandy 與財務圖表均清晰，呈現穩健、自信的正式商務簡報氛圍。

除上述人物替換、表情、視線與必要手勢調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、額外字卡或浮水印。
```


## 2026-10-21 shot_2.2.4 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.2.4_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；生成 1 次。
- 原七圖 prompt 僅因五圖輸入上限調整人物參考圖編號；人物原圖原尺寸左右並排，未裁切。主角板左 George／右 Amy；背景板左女客／右咖啡師。
- 目視：四人入鏡，George 微笑回應、Amy 聆聽、雙手低放；Amy 視線偏左上，主角較 blocks 前傾且手部靠攏，咖啡師可見範圍增加及朝向改變，糖罐仍為平木蓋而非小圓木鈕。待使用者評鑑，未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png
3. D:/kj-openMontage/.tmp/shot224_leads.png
4. D:/kj-openMontage/.tmp/shot224_background.png
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt_v3.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 shot224_leads.png：左半部 char_george.png 為 George 人物參考圖，對應圖 2 左側藍色人物；右半部 char_amy.jpeg 為 Amy 人物參考圖，對應圖 2 右側紅色人物。
圖 4 shot224_background.png：左半部 char_officelady.png 為背景女客參考圖，對應圖 2 左後方紫色人物；右半部 char_barista.png 為咖啡師參考圖，對應圖 2 最右緣綠色人物。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、人物佔位、整體大小、可見範圍與遮擋關係。維持人物與桌面的距離、頭頂留白及畫面邊緣裁切，不將兩位主角往中央靠攏。

將四個定位人物替換為對應角色，人物外觀與服裝採用圖 3 與圖 4 的對應角色區域，不採用其展示姿態或排版。只呈現圖 2 中可見的身體部位，不補出畫外身體。咖啡師維持最右緣局部入鏡，不擴大可見範圍，不保留彩色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留木質牆面、植物掛畫、窗邊座位、吧台與點心展示櫃的相對位置。

咖啡杯碟與糖罐採用圖 5 的外觀，數量、位置、比例與杯耳朝向依圖 2。每只杯子只有一個杯耳；糖罐為白瓷罐身與帶小圓木鈕的木蓋。圖 5 的多視角展示不代表增加道具，不帶入展示背景。

畫面描述：
這是一張 40mm、坐姿近眼高、輕微俯見桌面的雙人中景。George 位於畫面左側、Amy 位於右側，隔著木桌相向而坐。兩人的頭部、上半身、前臂、手部與部分大腿可見，下方依圖 2 裁切，保持原本的坐姿、身體朝向與人物間距。

George 面朝畫面右側的 Amy，目光看向她的眼睛，眉眼放鬆，嘴角帶著克制、理解的微笑，嘴唇微張，像是準備回應「妳問的，正是現在所有老闆們的痛點」。頭部保持自然直立，呈現開始點頭之前的瞬間。雙手仍自然低放在圖 2 的桌邊位置，尚未抬起比出等號，不拿杯子。

Amy 面朝畫面左側的 George，目光落在他的眼睛，嘴唇輕合，眉心仍有一點疑問，但神情已轉為專注聆聽。她保持圖 2 的肩膀、軀幹與手臂位置，不攤手、不攪拌咖啡，也不轉頭看鏡頭。

左後方女客維持坐在窗邊筆電前的姿態，右緣咖啡師維持站在吧台後的局部身影。背景人物的位置、朝向與遮擋依圖 2，不參與主角對話。畫面共四人，其中咖啡師僅局部可見。

兩位主角面前的咖啡杯留在杯碟上，糖罐維持桌面中央位置。沿用圖 1 的溫暖日光與精緻 3D 動畫質感，中等景深讓兩位主角的表情清楚可辨，背景適度柔化。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、等號圖形、對話框、角色標籤或參考圖分格。
```


驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。

## 2026-10-21 shot_1.2.1 GPT v1（待評鑑）

- 使用者指定改用 cam_amy_ms_45deg_block_blender，逐字使用已確認 prompt。
- 輸出：assets/images/shot_1.2.1_gpt_v1.png
- 工具：內建 image_gen；供應商 OpenAI；模型版本及費用未知；生成一次。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_gpt_v2.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png
- 目視：Amy 雙手打字、看向左側螢幕，頭部完整；手機位於右側鍵盤與文件冊之間並呈現來電介面。人物比例、手部位置及背景遮擋偏離 blocks，神情略帶微笑，手機小字未逐字確認。未改採用設定或 scene_plan，未追加生成。

```text
參考圖說明：
圖 1 cam_amy_ms_45deg_empty_gpt_v2.png：辦公室場景外觀參考圖。
圖 2 cam_amy_ms_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_smartphone.png：智慧型手機外觀及主管來電介面參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、頭頂留白、可見範圍與遮擋關係。

將紅色定位人物替換為 Amy，人物五官、棕色短髮、灰色西裝與米白襯衫採用圖 3，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體部位。雙手維持在鍵盤區域，將方塊手形轉為自然打字姿態，手指輕彎、指尖靠近鍵帽。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左前景螢幕背面、右前景直立文件冊及後方隔板、書櫃與窗戶的配置。

在畫面右側、鍵盤與直立文件冊之間的空白桌面加入一支智慧型手機，螢幕朝上平放，尺度與鍵盤相稱，不被文件冊或手臂遮住。手機外觀與來電介面採用圖 4；只生成一支手機，不帶入該參考圖的多視角排列。

畫面描述：
這是一張從 Amy 工位前方斜側 45 度、略微俯視的中景。Amy 坐在網布辦公椅上，頭部完整入鏡，上半身與鍵盤上的雙手可見，下半身在桌面後方。沿用圖 2 的人物位置與裁切，不拉近或放大人物。

捕捉主管來電剛開始的瞬間：Amy 身體略向工作區前傾，神情專注，視線朝向畫面左側的電腦螢幕，雙手仍維持打字姿態，尚未伸手接電話。桌上的手機螢幕剛亮起，顯示圖 4 的聯絡人頭像、「主管」、「來電」與紅綠接聽按鈕。

手機保持平放並與桌面接觸，不加入浮空、跳動殘影或漫畫震動線。Amy 與桌面工作區清晰，背景柔和呈現辦公室縱深，不為凸顯手機而改變鏡位或誇大手機尺寸。除上述人物替換、打字姿態與新增手機外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、額外疊字或水印；保留手機螢幕內的來電介面。
```


## 2026-10-21 shot_2.1.5 GPT v1｜待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.5_gpt_v1.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
- 目視：George單人頭肩、微笑張嘴、向畫外右側視線與通透眼鏡成立，無手／杯／桌面；頭部較blocks放大上移、頭頂留白減少，收下巴點頭感不明顯，背景主要配置保留。未追加重試或採用。
### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_george_cu_emotion_block_blender.png：構圖與人物佔位參考。
圖 3 char_george.png：George 外觀，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、整體大小、可見範圍與遮擋關係。保持 George 頭頂留白、頭部在畫面中的位置，以及肩膀與上胸在下緣的裁切，不推近鏡頭或放大頭部。

將藍色定位人物替換為圖 3 的 George。五官、灰白髮型、棕色眼鏡、鬍鬚、服裝與自身頭身比例採用圖 3，不採用角色設定圖的展示姿態或排版。只呈現圖 2 中可見的身體部位。

將場景材質、風格與光影更新為圖 1 的外觀，保留日間暖陽、局部木框窗、墨綠牆柱、植物掛畫與椅背，不改變圖 2 的空間配置。George 置入後自然遮擋身後環境，不為了展示完整掛畫或窗景而移動人物。

畫面描述：
這是一張坐姿近眼高、微側拍的 George 頭肩特寫，100mm 視角。完整頭部、肩膀與部分上胸可見，手部、咖啡杯與桌面留在畫外。畫面只有 George 一人。

George 帶著溫和而肯定的微笑，下巴略收，呈現輕輕點頭回應「沒錯」的瞬間。嘴唇自然微張，眼神專注看向畫外右側對坐的 Amy，流露沉穩、自信且耐心解釋的神情，不直視鏡頭。

肩膀、胸口及軀幹沿用圖 2 的坐姿與朝向；頭部自然承接頸部及胸口方向，只為點頭稍微收下巴，不額外扭轉脖子或形成側身回望。保留圖 2 的肩線與左右肩前後關係，不套用圖 3 的正面站姿。

焦點落在 George 的雙眼、眼鏡與面部表情，鏡片保持通透，不以強烈反光遮住眼睛。背景窗景、墨綠牆柱與植物掛畫適度柔化，仍可辨識原有環境。除上述表情與輕微點頭調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、EPS 字樣、對白文字、角色標籤或參考圖分格。
```


- 驗證：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：bd3cc7cee4504b611940501414032ffcd65a9d0f9901f81fe60e24c43770c80b。原生來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-d4dab815-37b1-417f-b6b3-108fd09f8c1d.png

## 2026-10-21 shot_1.2.1 GPT v2（手機方向修正，待評鑑）
- 輸入：assets/images/shot_1.2.1_gpt_v1.png（唯一底圖）
- 輸出：assets/images/shot_1.2.1_gpt_v2.png
- 內建 image_gen／OpenAI，模型版本與費用未知，生成一次。
- 目視：來電介面已旋轉180度，按鈕靠Amy、頭像靠鏡頭；人物與主要構圖保留。手機機身充電孔仍在鏡頭側，整支機身旋轉指令未完全遵從；螢幕小字有重繪。未更改正式採用設定。
```text
請局部編輯這張圖片，只修正桌面上手機的朝向。將整支手機沿桌面平面旋轉180度，保持手機在原來的位置、原尺寸、平放於桌面及原透視。手機底端（充電孔那端）朝向坐在桌後的Amy，手機頂端朝向鏡頭與桌前緣；手機螢幕的「主管」「來電」、頭像與紅綠按鈕必須隨整支手機一起旋轉，使Amy從自己的座位方向能正向閱讀，鏡頭方向看到的介面則是倒向的。不是只翻轉文字，也不是將手機翻面；螢幕仍朝上，維持原來的主管來電介面。其餘所有內容保持原圖，包括Amy的臉、表情、髮型、服裝、姿勢、雙手、鍵盤、螢幕、文件冊、辦公室背景、構圖與光影。輸出一張16:9彩色圖片，不加字幕或水印。
```


## 2026-10-21 shot_2.1.6 GPT v1｜待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.6_gpt_v1.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_table_insert_top_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png
- 目視：四隻手、無臉、兩杯碟與自然拿鐵奶泡、中央留白及無疊字成立。糖罐增加木旋鈕但仍保留孔洞，未符合無孔要求；手部位置／姿態與blocks有偏差，下方兩手較上移。未追加生成、未採用。
### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_table_insert_top_empty_gpt.png：咖啡館桌面材質與光影參考。
圖 2 cam_table_insert_top_block_blender.png：構圖、道具配置與人物局部佔位參考。
圖 3 char_george.png：George 外觀與服裝，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 外觀與服裝，對應圖 2 右側紅色人物。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、俯拍角度、透視、桌面配置、人物佔位、可見範圍與遮擋關係。保持兩組杯碟、糖罐及四隻手在畫面中的位置與比例，不旋轉畫面、不改為正上方垂直俯視。

將左側藍色人物的可見局部替換為圖 3 的 George，右側紅色人物的可見局部替換為圖 4 的 Amy。只呈現圖 2 已入鏡的手、前臂、衣袖及身體邊緣，不補出頭部、臉孔或完整身體，不採用角色設定圖的展示姿態或排版。

George 可見衣袖採用圖 3 的米色襯衫與捲袖，身體邊緣依可見部位呈現棕色背心或深色長褲；Amy 採用圖 4 的灰色西裝衣袖與對應服裝。將方塊手替換為自然的人類手部，維持原本放在桌上的位置與朝向，手指自然放鬆。

將桌面、椅子與周邊地板的材質、風格及光影更新為圖 1 的外觀，保留暖色窗光與自然木紋，不改變圖 2 的物件配置。

兩組咖啡杯碟與糖罐的外觀以圖 5 為準。保留圖 2 的道具位置、比例及杯柄朝向，每只杯子只有一個完整杯柄。咖啡表面採用圖 5 的自然拿鐵奶泡，不沿用 blocks 的多邊形白圈。

糖罐為白瓷罐身、完整木蓋與中央木製旋鈕，蓋上沒有撒粉孔，不沿用圖 1 或圖 2 的打孔蓋。糖罐維持畫面上緣原有位置與裁切，不為了展示完整蓋子而向下移動。圖 5 的多視角展示不代表增加道具。

畫面描述：
這是一張 50mm 視角、高位斜俯拍的桌面插鏡。原木桌面佔據主要畫面，George 的咖啡杯碟在左下方，Amy 的咖啡杯碟在右上方，糖罐位於上方中央，位置與透視依圖 2。

George 坐在畫面左側，Amy 坐在右側。兩人各有兩隻手與部分前臂從畫面左右邊緣進入，維持圖 2 的自然桌邊姿態。全畫面共四隻手，沒有臉孔；不額外加入指點、攤手、握杯或攪拌動作。

兩只咖啡杯都安放在各自杯碟上，糖罐保持關閉。維持桌面中央既有的空白木紋區域，供後續疊加字卡，不新增道具或圖案。

桌面、手部、杯碟與糖罐保持清楚，呈現自然接觸陰影與柔和陶瓷反光。除上述人物與道具外觀替換外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感。不加入 E、S、G 字母、字幕、圖示、對白文字、標籤或參考圖分格。
```


- 驗證：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：6c2bb9e503c2480683a3c836eb88942c02b2144a5edfaa5d4c4b47bcbb057923。原生來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-1cb3e964-d769-4a8e-a916-cdd2921e5984.png

## 2026-10-21 shot_1.1.4 GPT v1（待評鑑）

- 圖片：`assets/images/shot_1.1.4_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；確切模型與費用未知，生成一次。
- 配方：W2I；完整使用核准 prompt。
- 有序參考圖：
  1. `references/scenes/investment_office/cameras/cam_harrison_ots_analyst2_empty_gpt.png`
  2. `references/scenes/investment_office/cameras/cam_harrison_ots_analyst2_block_blender.png`
  3. `clp/char_harrison.jpeg`
  4. `clp/char_analyst2.jpg`
- 驗證：1672×941 RGB PNG，完整解碼與來源複本 SHA256 相符。Harrison 抱臂／閉嘴／冷峻表情及模糊前景成立；相較blocks主體放大偏右、前景多露出 Analyst 2 白襯衫肩部，窗外柔焦較弱，低頭沉思不明顯。待評鑑，未重試或改採用。

完整 prompt：

```text
參考圖說明：
圖 1 cam_harrison_ots_analyst2_empty_gpt.png：會議室靠窗座位的場景外觀參考。
圖 2 cam_harrison_ots_analyst2_block_blender.png：越過 Analyst 2 拍攝 Harrison 的構圖底圖。
圖 3 char_harrison.jpeg：Harrison（char_harrison）人物參考，對應圖 2 中央偏右的藍色人物。
圖 4 char_analyst2.jpg：Analyst 2（char_analyst2）人物參考，對應圖 2 左側極近前景的局部頭部與頸部。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、兩人的佔位與比例、頭頂留白，以及前景遮擋與裁切關係。不要拉近鏡頭或放大 Harrison。

將藍色定位人物替換為圖 3 的 Harrison，五官、銀灰色後梳髮型、濃眉與深色細條紋西服均採用圖 3，不採用人物表的展示姿態或構圖。直接坐入原有棕色高背皮椅，不新增椅子；只呈現圖 2 可見的身體部位，下半身維持被桌面遮擋。

將左側極近前景人物替換為圖 4 的 Analyst 2，只替換圖 2 已入鏡的後腦、頭部側後緣及頸部局部。髮型採用圖 4 的棕色波浪髮；不露出正臉、不轉頭看鏡頭，不補出完整頭部、肩膀或軀幹。保留原本被畫面左緣與上下邊界裁切的前景輪廓。

將場景材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留棕色皮椅、金屬扶手、前景胡桃木桌面、落地窗框及窗外金融大樓。

畫面描述：
這是一張 45mm、坐姿眼高平視的過肩鏡頭。鏡頭越過畫面左側 Analyst 2 的模糊局部後腦，拍攝桌子對面的 Harrison。Harrison 位於中央偏右，頭部、上半身與交疊的雙臂可見；桌面橫跨畫面下方，身後是棕色高背皮椅及陰天金融區窗景。全畫面只有這兩位角色，只有 Harrison 的臉部可辨識。

Harrison 雙臂交疊於胸前，軀幹維持圖 2 略靠椅背的坐姿。下巴微收，頭部輕微低垂，眉頭略緊、嘴唇閉合，呈現聽完財務簡報後短暫沉思、即將追問非財務指標的起始瞬間。眼神冷靜而銳利，視線朝向畫外 Sandy 所在的簡報區，不與前景 Analyst 2 對視，也不直視鏡頭。只微調頭部與表情，不改變肩胸朝向、抱臂姿態或座位位置。

Analyst 2 維持圖 2 的前景位置與朝向，僅作為模糊的空間層次，不增加表情或手勢。Sandy 在畫外，不加入她的身影。

場景維持圖 1 的白天陰天光線與為簡報而調暗的室內亮度，冷色漫射日光透過落地窗進入。Harrison 的臉部與眼神清楚可辨，銀灰髮絲、深色西服與皮椅材質自然融入同一光線，保持人物參考的精緻 3D 動畫質感。

焦點落在 Harrison 的眼睛與臉部，左側極近前景明顯柔焦，窗外大樓適度柔化但仍能辨識窗格與建築輪廓。整體氛圍克制、冷峻，帶有正式投資審查的壓力。

除上述人物替換與必要的表情、頭部調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、額外字卡或浮水印。
```


## 2026-10-21 shot_1.2.2 GPT v1（待評鑑）
- 輸出：assets/images/shot_1.2.2_gpt_v1.png
- 內建 image_gen／OpenAI；模型版本與費用未知；生成一次，逐字使用使用者確認 prompt。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_gpt_v2.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png
- 目視：Amy 左手持手機貼左耳、手機背面朝外，右手停鍵盤，嘴微張、無笑容，未後仰且無第二支手機；視線仍偏向左側螢幕，人物輪廓／比例及背景細節偏離 blocks。待使用者評鑑，未改正式採用設定或 scene_plan。
```text
參考圖說明：
圖 1 cam_amy_ms_45deg_empty_gpt_v2.png：辦公室場景外觀參考圖。
圖 2 cam_amy_ms_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_smartphone.png：智慧型手機外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、頭頂留白及裁切範圍。

將紅色定位人物替換為 Amy，人物五官、棕色短髮、灰色西裝與米白襯衫採用圖 3，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體部位。

依接電話的動作調整 Amy 的左手與左前臂：左手由鍵盤區抬起，握住手機並貼近左耳，也就是畫面右側、較少被電腦螢幕遮擋的一側。右手維持在鍵盤附近，自然停下打字。肩膀、軀幹與座位位置沿用圖 2，容許抬臂所需的自然肩部變化。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左前景螢幕背面、右前景直立文件冊，以及後方隔板、書櫃與窗戶。

手機外觀採用圖 4，只生成一支握在 Amy 手中的手機，桌面不再出現第二支。手機直立，頂端聽筒靠近耳朵，底端充電孔朝下、靠近下顎；螢幕朝向 Amy 的臉，背面與三鏡頭朝向外側。不要為了展示來電介面而把螢幕翻向鏡頭。

畫面描述：
這是一張從 Amy 工位前方斜側 45 度、略微俯視的中景。畫面中只有 Amy 一人，坐在網布辦公椅上，頭部完整入鏡，上半身與桌面工作區可見，下半身被桌面遮擋。沿用圖 2 的人物尺度與頭頂留白，不拉近或放大人物。

捕捉 Amy 剛接通電話、開始聽到主管急促聲音的瞬間：她左手將手機貼在左耳，右手停在鍵盤旁；眉毛微微抬起，雙眼略張，嘴唇輕微分開，流露突然警覺與困惑，沒有笑容。視線從電腦工作區稍微移開，朝前方偏下，不看鏡頭。

此刻身體仍保持坐姿，尚未往後仰，手機也尚未拉離耳朵，為後續被咆哮聲嚇到的動作保留起點。頭部可為接電話略微轉動，但維持原有位置與尺度。

Amy 的臉、握手機的手與手機清晰可辨，辦公室背景保留自然縱深。除上述接電話姿態、表情與視線調整外，其餘沿用圖 2。不加入主管人物、分割畫面、對話框或漫畫聲波。

輸出一張 16:9 彩色分鏡圖，不加入字幕、額外疊字或水印。
```


## 2026-10-21 shot_2.2.5 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.2.5_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；生成1次。
- 目視：George 莊重微張嘴、右手低放、Amy 右前景背影及白瓷杯碟呈現；人物尺度／位置、頭頂留白與背景遮擋偏離 blocks，George 右手部分裁切，視線略偏右上。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_george_ots_amy_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右前景紅色人物。
圖 5 prop_coffee_cup.png：白瓷咖啡杯與杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、人物佔位、比例、可見範圍與遮擋關係。維持 George 的頭頂留白、肩膀高度及 Amy 的前景大小，不將兩人往中央靠攏。

將藍色定位人物替換為圖 3 的 George，紅色定位人物替換為圖 4 的 Amy。人物外觀與服裝採用對應參考圖，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體部位，不補出畫外身體，不保留紅藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留木框大窗、窗外街景、墨綠牆柱、局部植物掛畫與桌椅的相對位置。圖 1 中因移除人物而露出的物件，仍須依圖 2 的人物遮擋，不為展示道具而移開 Amy。

可見咖啡杯與杯碟的外觀採用圖 5，位置、大小與杯耳朝向依圖 2。杯子為純白亮釉陶瓷，只有一個杯耳，內有拿鐵。圖 5 的多視角展示不代表增加杯子，不帶入展示背景。

畫面描述：
這是一張 60mm、坐姿近眼高微俯、從 Amy 身後越過肩膀拍攝 George 的過肩鏡頭。George 位於左側中景，頭部、上半身、部分前臂及桌邊手部可見；Amy 的後腦、頸部、肩背與部分手臂佔據右前景，右側及下方依圖 2 裁切。畫面只有兩人，只有 George 的臉清楚可辨，Amy 不轉頭露出正臉。

George 面朝畫面右側對坐的 Amy，目光穩定落在她的眼睛位置，不看鏡頭、不抬眼望向上方。他收起上一鏡帶懸念的微笑，眉毛微微收攏，嘴角平穩，嘴唇微張，呈現沉著、莊重而篤定的神情，像是正準備說「那種時代已經過去了」。表情有說服力，但不憤怒、不瞪眼、不誇張張嘴。

這是揮手示意翻篇之前的起始瞬間。George 的右手仍低放在圖 2 左下方的桌邊位置，手指自然放鬆，尚未抬起；另一隻手維持圖 2 的位置與遮擋。肩膀、軀幹與坐姿沿用圖 2，不前傾靠近 Amy，不舉杯。

Amy 維持圖 2 面向 George 的坐姿與頭肩朝向，作為安靜聆聽的右前景，不增加手勢。George 面前的咖啡杯仍放在原杯碟上。

沿用圖 1 的日間暖陽，保留窗邊柔和光線與墨綠牆面的色調。淺景深聚焦 George 的眼睛及表情，眼鏡保持清晰，不以強烈反光遮住眼睛；Amy 的前景頭肩與窗外街景適度柔化。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、標語、對話框、角色標籤或參考圖分格。
```


驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。

## 2026-10-21 shot_1.1.5 GPT v1（待評鑑）

- 圖片：`assets/images/shot_1.1.5_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；確切模型與費用未知，生成一次。
- 配方：W2I；完整沿用核准 prompt。
- 有序參考圖：
  1. `references/scenes/investment_office/cameras/cam_sandy_ms_15deg_empty_gpt.png`
  2. `references/scenes/investment_office/cameras/cam_sandy_ms_15deg_block_blender.png`
  3. `clp/char_sandy.jpeg`
- 驗證：1672×941 RGB PNG，完整解碼與來源複本 SHA256 相符。Sandy 單人、緊眉閉嘴僵笑、左手停在指圖姿勢／右手持簡報器與原財務表格成立；相較blocks頭部放大上移、肩胸朝向與手臂角度有變，遙控器拇指輕觸按鍵不明確。待使用者評鑑，未重試或更新採用。

完整 prompt：

```text
參考圖說明：
圖 1 cam_sandy_ms_15deg_empty_gpt.png：會議室投影幕旁的場景外觀參考。
圖 2 cam_sandy_ms_15deg_block_blender.png：Sandy 單人中景構圖底圖。
圖 3 char_sandy.jpeg：Sandy（char_sandy）人物參考，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物位置與比例、頭頂留白、軀幹朝向及畫面裁切。不要拉近鏡頭、放大人物或增加頭部比例。

將紅色定位人物替換為圖 3 的 Sandy。五官、髮型、黑框眼鏡、深色褲裝西服、淺色襯衫與藍色識別證掛繩採用圖 3，不採用人物表的展示姿態或分格構圖。只呈現圖 2 已入鏡的身體部位，不補出畫外下半身。

將場景材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左側深色木門與兩支金屬長把手、中間灰牆，以及右側投影幕的局部表格與黑色邊框。投影內容維持圖 1 的財務表格，不切換到下一張投影片。

畫面描述：
這是一張 50mm、眼高平視、15 度微側取景的 Sandy 單人中景。Sandy 位於畫面中央偏左，腰部以上入鏡；右側保留被畫面邊界裁切的投影幕表格。全畫面只有 Sandy 一人。

Sandy 剛聽到畫外 Harrison 對 ESG 指標的追問，原本自信的笑容僵在臉上。嘴角勉強維持微微上揚，但嘴唇輕抿、下顎緊繃；眉心略微收緊，眼神帶著短暫錯愕與不自在，呈現努力維持專業的尷尬神情，不是開朗微笑或誇張驚嚇。她的視線仍朝向畫外 Harrison，不直視鏡頭。

她的左臂暫時停留在圖 2 原本指示投影幕的位置，手指略顯僵硬，呈現講解手勢突然停住的瞬間。右手在原本腰際位置握住黑色簡報遙控器，拇指輕觸按鍵、尚未按下，其餘手指稍微收緊，表現即將遲疑操作的緊張感。僅調整表情、手指與必要的手腕角度，肩膀、胸口及雙臂整體位置沿用圖 2。

這是一個無對白的停頓瞬間，嘴巴不呈現說話口型。以僵住的笑容與握簡報器的細節表現緊張，不加入汗滴、漫畫符號、動作線、手部殘影或額外肢體。

室內保持為簡報而調暗的照明，光線、材質與色調依圖 1，整體冷靜肅穆。人物保留圖 3 的精緻 3D 動畫質感，臉部與握簡報器的右手清楚可辨；採中等景深，背景投影表格仍能辨識，不過度模糊。

除上述人物替換、表情與必要手部調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、額外字卡或浮水印。
```


## 2026-10-21 shot_2.1.7 GPT v2｜待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。既有v1保留。
- 輸出：assets/images/shot_2.1.7_gpt_v2.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png
- 目視：George左前景過肩、Amy擔憂微張嘴及對話視線成立，無額外藤蔓／疊字；Amy頭部放大、手部改位，George局部側臉／眼鏡可見，糖罐與前杯較blocks多露出，糖罐木蓋仍有孔，遮擋／道具要求未全過。未追加生成或採用。
### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_amy_ots_george_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_amy_ots_george_block_blender.png：構圖與人物佔位參考。
圖 3 char_george.png：George 外觀，對應圖 2 左前景藍色人物。
圖 4 char_amy.jpeg：Amy 外觀，對應圖 2 右中景紅色人物。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、整體大小、可見範圍與遮擋關係。保持 George 頭肩在左前景的佔比與裁切，以及 Amy 在右中景的位置、頭頂留白和桌面可見範圍，不推近鏡頭或放大 Amy。

將藍色定位人物替換為圖 3 的 George，紅色定位人物替換為圖 4 的 Amy。人物五官、髮型、服裝與自身頭身比例依人物參考，不採用角色設定圖的展示姿態或排版。人物坐入既有座椅，只呈現圖 2 已入鏡的身體部位。

George 保持背對鏡頭、面向 Amy 的過肩前景，呈現灰白頭髮、後腦、頸部與棕色背心肩背，不轉頭露出完整臉孔。

將場景材質、風格與光影更新為圖 1 的外觀，保留日間暖陽、原木牆面、服務吧台、磨豆機與義式咖啡機，不改變圖 2 的空間配置。背景物件數量與配置依圖 2，不移植圖 1 額外垂下的藤蔓。

桌面可見杯碟與糖罐的外觀採用圖 5，位置、比例及可見範圍依圖 2。每只杯子只有一個杯柄；糖罐若有可見局部，採用白瓷罐身與無孔木蓋。被 George 遮住的道具維持遮擋，不為了展示完整杯碟或糖罐而移動人物或道具。

畫面描述：
這是一張從 George 肩後看向 Amy 的過肩鏡頭，60mm 視角，坐姿近眼高平視。George 的後腦與肩背位於左前景，Amy 坐在右中景，臉部、上半身與部分桌邊手部可見。畫面只有兩人，Amy 是唯一清楚可辨識的臉孔。

Amy 身體沿著面向 George 的方向微微前傾，保持坐在原座位上。眉頭輕蹙，眉心略收，眼神帶著遲疑與擔憂，嘴唇微張，呈現正要探問「是不是很複雜、很難懂」的瞬間。視線看向左前景對坐的 George，不直視鏡頭。

前傾幅度小，不縮短兩人的座位距離，不改成大幅探身。頭部、頸部與胸口自然維持對話方向，不側身回望。雙手保持圖 2 原有桌邊位置，手指自然放鬆，不額外攤手、指點、握杯或攪拌。咖啡杯維持放在杯碟上。

George 維持聆聽姿態，頭肩位置與朝向沿用圖 2。焦點落在 Amy 的雙眼與擔憂表情，George 的前景頭肩及後方設備適度柔化，保留可辨識的輪廓與空間層次。

除 Amy 指定的輕微前傾與表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


- 驗證：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：f8519ff8d1bcaed2735f4eefaa787c7ecb93eb99f918f0b571d717ca9aa02689。原生來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-b995ea26-a5fc-48fe-9dc3-85cf86c679a7.png

## 2026-10-21 shot_2.2.6 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.2.6_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；生成1次。
- 目視：George 單人頭肩特寫、微笑微張嘴、雙手畫外且眼鏡未遮瞳孔呈現；視線偏右上，人物頭部放大且頭頂留白減少，肩膀位置及背景遮擋偏離 blocks。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_george_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、可見範圍與遮擋關係。

將藍色定位人物替換為圖 3 的 George，只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖，不保留藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左側木框窗與窗外街景、後方墨綠牆柱、右上方植物掛畫及局部椅背的相對位置與裁切。

畫面描述：
這是一張 100mm、坐姿近眼高、微側角度的 George 單人臉部特寫。George 位於畫面中央，頭部、頸部、肩膀與上胸入鏡，下方依圖 2 裁切。頭部大小、頭頂留白、肩膀高度及背景遮擋維持圖 2。畫面只有 George 一人，Amy 位於畫外，不加入她的頭肩或其他前景人物。

George 的臉朝向畫面右側對坐的 Amy，雙眼自然看向畫外右側、與坐姿眼高相近的位置，不看鏡頭、不抬眼望向右上方。他的眉心放鬆，眼神專注而堅定，嘴角輕輕上揚，嘴唇微張，呈現溫暖、自信、鼓勵對方的微笑，像是正準備說「而這套新規則，就是妳說服老闆的最大王牌！」。笑意克制，不咧嘴大笑，不呈現嘲諷或得意神情。

這是向前微傾之前的起始瞬間。George 的頭部、肩膀與軀幹維持圖 2 的自然坐姿，尚未靠近鏡頭。雙手留在畫外，不加入指人、比讚、持牌或舉杯手勢。

沿用圖 1 的日間暖陽，窗邊柔和光線照亮 George 的臉部與銀灰頭髮。眼睛保留自然明亮的高光，眼鏡不以強烈反光遮住瞳孔。淺景深聚焦眼睛與微笑，木框窗、墨綠牆面及植物掛畫柔和虛化，仍保留可辨識的輪廓。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、王牌圖案、對話框、角色標籤或參考圖分格。
```


驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。

## 2026-10-21 shot_1.2.3 GPT v1（左右分割，待評鑑）
- 輸出：assets/images/shot_1.2.3_gpt_v1.png
- 工具：內建 image_gen／OpenAI；模型版本與費用未知；生成一次，逐字使用使用者確認的左右分割 prompt。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_supervisor_ms_15deg_block_blender.png
2. D:/kj-openMontage/projects/course-51-esg/clp/loc_supervisor_office_1.jpg
3. D:/kj-openMontage/projects/course-51-esg/clp/char_supervisor.jpeg
4. D:/kj-openMontage/projects/course-51-esg/assets/images/shot_1.2.2_gpt_v1.png
5. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 目視：左右各半且背景分離，主管右手持電話／左手抬起、Amy左手接電話／右手停鍵盤，人物頭部完整、朝中央，焦急與擔憂表情呈現。主管抬手靠中央且部分指尖裁切，背景紙張及人物比例有重繪；未改正式採用設定或scene_plan。
```text
參考圖說明：
圖 1 cam_supervisor_ms_15deg_block_blender.png：左半主管畫面的機位、人物佔位及背景配置參考，藍色定位人物對應主管。
圖 2 loc_supervisor_office_1.jpg：主管辦公室的材質、色彩、光影與美術參考，不採用此圖的廣角構圖。
圖 3 char_supervisor.jpeg：主管的五官、髮型與服裝參考。
圖 4 shot_1.2.2_gpt_v1.png：右半 Amy 在自己座位區接電話的場景、人物位置與持電話姿態參考。
圖 5 char_amy.jpeg：Amy 的五官、髮型與服裝參考。

整體構圖：
輸出一張 16:9 電影式左右分割畫面。中央垂直分界，左半與右半各占畫面寬度 50%，兩側都是獨立的辦公空間與獨立鏡頭。

各半幅以人物為中心重新裁切，保留完整頭部、適量頭頂留白及必要的持電話與手勢空間；不要把兩張橫幅圖直接壓窄，不拉長人物。兩人的頭部顯示尺度接近，眼睛高度大致對齊。

左半：主管在自己的辦公室通話。
依圖 1 的 15 度微側機位與人物位置，將藍色定位人物替換為圖 3 的主管，呈現頭部至上半身。保留身後文件佈告板、牆面與藍色辦公椅的配置，將簡化材質更新為圖 2 的精緻辦公室外觀，不移植圖 2 的桌面廣角或窗景構圖。

主管穿捲袖藍色襯衫、鬆開的棕色領帶，黑色短髮略凌亂。右手握一支深色手機貼在右耳，也就是左半畫面靠外緣的一側；手機頂端靠耳朵、底端朝下，螢幕朝臉、背面朝外。

左手抬至胸口旁、靠近中央分界的一側，手掌斜朝上、手指自然張開，停在即將焦急比劃的起始位置，不越過中央分界。主管身體略向前傾，眉頭緊皺、內側眉角抬高，額頭帶少量汗珠，嘴巴張開正在說話，表情焦急而無助，像帶著哭腔警告增資失敗將影響擴廠與年終獎金。臉部略朝畫面右側，不直視鏡頭。

右半：Amy 在自己的座位區接電話。
以圖 4 為畫面基礎，依右半直幅範圍裁切，保留 Amy 完整頭部、上半身、接電話的左手與部分桌面。人物外觀依圖 5。保留青綠隔板、網布椅與後方書櫃窗景，左前景可見部分電腦螢幕，維持她自己的辦公座位環境。

Amy 延續圖 4 的姿勢，左手握手機貼在左耳，也就是右半畫面靠外緣的一側，手機背面朝外；右手停在鍵盤附近。她安靜聆聽，眉毛微抬、眼睛略張、嘴唇輕微分開，神情擔憂與錯愕，沒有笑容。臉部與視線略朝畫面左側，形成兩側人物朝向中央的視覺呼應，但兩人並非同處一室。此刻尚未開口反問。

空間與畫面限制：
兩個辦公室嚴格分開，各自保留參考圖的背景，不融合成同一間房，不讓桌面、手臂或物件跨越中央分界。畫面總共只有主管與 Amy 兩人，每人各持一支手機，桌面不增加其他手機。

人物採一致的精緻 3D 動畫電影質感，各自沿用所在場景的日間光線。臉部、手機與手勢清晰，背景柔和虛化。只呈現同一通電話中的單一瞬間，不加入揮手殘影、多重手臂、漫畫聲波或對話框。

輸出一張 16:9 彩色左右分割分鏡圖，不加入字幕、姓名標籤、額外文字或水印。
```


## 2026-10-21 shot_1.1.6 GPT v1（待評鑑）

- 圖片：`assets/images/shot_1.1.6_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；確切模型與費用未知，生成一次。
- 配方：W2I；完整沿用核准 prompt。
- 有序參考圖：
  1. `references/scenes/investment_office/cameras/cam_sandy_ots_harrison_empty_gpt.png`
  2. `references/scenes/investment_office/cameras/cam_sandy_ots_harrison_block_blender.png`
  3. `clp/char_sandy.jpeg`
  4. `clp/char_harrison.jpeg`
- 驗證：1672×941 RGB PNG，完整解碼與來源複本 SHA256 相符。Sandy 緊張歉疚／微張嘴／掌心向上指圖／持簡報器、Harrison 後腦及高背椅遮擋成立；相較blocks，Sandy 明顯放大且頭頂提高，左臂角度降低，Harrison 頭部輪廓與朝向有變；非完全保留原人物比例。待使用者評鑑，未重試或更新採用。

完整 prompt：

```text
參考圖說明：
圖 1 cam_sandy_ots_harrison_empty_gpt.png：會議室投影幕與長桌的場景外觀參考。
圖 2 cam_sandy_ots_harrison_block_blender.png：越過 Harrison 拍攝 Sandy 的構圖底圖。
圖 3 char_sandy.jpeg：Sandy（char_sandy）人物參考，對應圖 2 左中景的紅色人物。
圖 4 char_harrison.jpeg：Harrison（char_harrison）人物參考，對應圖 2 右側前景、椅背上方的銀髮人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、人物位置與比例，以及前景椅背、桌面對人物的遮擋關係。不要拉近鏡頭、放大 Sandy 或減少她上方的留白。

將紅色定位人物替換為圖 3 的 Sandy。五官、棕色束髮、黑框眼鏡、深色褲裝西服、淺色襯衫與藍色識別證掛繩採用圖 3，不採用人物表的展示姿態或分格構圖。身體可見範圍沿用圖 2，下半身由長桌遮擋，不補出雙腳。

將右側前景人物替換為圖 4 的 Harrison，只呈現圖 2 椅背上方已可見的銀灰色後梳頭髮、後腦與頭頸局部。不露出正臉，不轉頭回望，不補出被高背椅遮住的肩膀、軀幹或手臂。保留右側邊界對頭部的裁切，以及高背椅原有的大小、位置與遮擋範圍。

將場景材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左側深色木門、空椅、灰牆、木格柵天花、胡桃木長桌，以及右側前景高背椅與桌上筆電。投影幕沿用圖 1 的財務圖表版面、長條圖、折線圖與表格，不自行新增 ESG 數值或警告文字。

畫面描述：
這是一張 42mm、坐姿視角平視的過肩鏡頭。Harrison 的局部後腦與高背椅占據畫面右側前景，Sandy 站在左中景、靠近投影幕左側，長桌由前景延伸至她身前。全畫面只有 Sandy 與 Harrison 兩位人物，只有 Sandy 的臉部可辨識。

Sandy 呈現即將吞吞吐吐回答的瞬間。眉心微微收緊，內側眉梢略抬，原本的自信笑容消失；嘴唇微張，下顎稍顯緊繃，神情心虛、歉疚而不安，努力維持專業。她望向右側前景 Harrison 所在的位置，不直視鏡頭，不露出開朗笑容或誇張哭相。

她的左臂維持圖 2 朝向簡報的整體方向，手腕略微放鬆、手掌稍向上，形成無奈指示簡報的姿勢；右手仍在原本腰際位置握住黑色簡報遙控器。僅調整表情、視線與必要的手腕、手指，肩膀、胸口及軀幹位置沿用圖 2，不向鏡頭前傾或跨步移位。

Harrison 安靜坐在前景原座位，保持面向 Sandy 的後腦方向，呈現不動聲色的聆聽狀態。椅背遮住的部位維持遮擋，不為表現聆聽而新增可見手勢。

室內維持圖 1 為簡報而調暗的照明，投影幕明亮，Sandy 的臉部與服裝仍清楚可辨。人物融入場景光線，保持參考人物的精緻 3D 動畫質感，整體氛圍肅穆而尷尬。

焦點落在左中景 Sandy 的臉部與表情，右側前景 Harrison 的後腦與椅背適度柔焦，投影幕圖表仍能辨識。不要以景深模糊掩蓋 Sandy 的表情或手勢。

除上述人物替換與必要的表情、視線、手部調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、額外字卡或浮水印。
```


## 2026-10-21 shot_1.2.4 GPT v1（待評鑑）
- 輸出：assets/images/shot_1.2.4_gpt_v1.png
- 工具：內建 image_gen／OpenAI；模型版本與費用未知；生成一次，逐字使用確認 prompt。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v2.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png
- 目視：左手手機貼左耳、背面朝外，右手胸前抬起完整可見，雙眼瞪大及張嘴錯愕呈現；視線偏左上，人物頭部變大、頭頂留白減少，人物比例與背景遮擋偏離blocks。未改正式採用設定或scene_plan。
```text
參考圖說明：
圖 1 cam_amy_ms_15deg_empty_gpt_v2.png：Amy 座位區的場景外觀參考圖。
圖 2 cam_amy_ms_15deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_smartphone.png：智慧型手機外觀參考圖，只採用機身外觀，不採用來電介面。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、頭頂留白、可見範圍與遮擋關係。

將紅色定位人物替換為 Amy，五官、棕色短髮、灰色西裝與米白襯衫採用圖 3，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體範圍，不補出畫外的桌面、鍵盤或下半身。

依本鏡表演調整雙臂與雙手：Amy 左手握手機貼在左耳，也就是畫面右側；右手由下方抬至胸前，停在畫面中央偏左、螢幕右緣與軀幹之間的可見區域。容許自然抬臂所需的肩部變化，其餘人物位置與尺度沿用圖 2。

手機外觀採用圖 4。只生成一支手機，直立貼近左耳，頂端聽筒靠耳朵、底端充電孔朝下、靠近下顎；螢幕朝 Amy 的臉，背面與三鏡頭朝外。手指自然環握，不遮住眼睛與嘴巴。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左前景螢幕、網布椅、青綠隔板、後方書櫃、盆栽與百葉窗的位置及遮擋。

畫面描述：
這是一張 Amy 在自己辦公座位接電話的單人中景，採 15 度微側、接近眼高的略微俯視角度。頭部完整入鏡，上半身與胸前手勢可見，左前景螢幕遮住部分身體，沿用圖 2 的裁切與頭頂留白。

捕捉 Amy 聽到年終獎金可能發不出來、剛要反問「這麼嚴重？」的瞬間。她左手仍把手機貼在左耳，雙眼瞪大，眉毛抬起且眉心微微收攏，嘴唇剛張開，流露錯愕、不解與擔憂，沒有笑容。

右手僵在胸前半空，手肘彎曲，手掌斜朝上，手指自然微張，像原本要說話卻被消息驚得停住。整隻手清楚位於畫面內，不被前景螢幕遮住，不碰臉、不指向鏡頭，也不做誇張揮舞。

Amy 保持坐姿，肩頸略微繃緊，沒有大幅後仰。頭部略朝畫面左側，視線落在鏡頭左側的畫外前方，不直視觀眾。手機仍貼耳，沒有拉開或換手。

臉部、持手機的手與胸前右手清晰可辨，背景保持自然辦公室縱深。除上述接電話姿態、右手位置、表情與視線調整外，其餘沿用圖 2。

畫面中只有 Amy 一人，不加入主管、分割畫面、對話框、漫畫驚嘆號或動作殘影。

輸出一張 16:9 彩色分鏡圖，不加入字幕、額外疊字或水印。
```


## 2026-10-21 shot_2.1.8 GPT v1｜待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.8_gpt_v1.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
4. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png
- 目視：George單人微笑抬手、無孔木蓋與旋鈕成立；人物放大上移、頭頂留白減少，肩胸角度及另一手位置與blocks不同。 未追加重試或採用。
### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖與人物佔位參考。
圖 3 char_george.png：George 外觀，對應圖 2 的藍色人物。
圖 4 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、物件配置、人物佔位、整體大小與裁切。保持 George 的頭頂留白、座位位置，以及下緣咖啡杯和右下角糖罐的可見範圍，不推近鏡頭或放大人物。

將藍色定位人物替換為圖 3 的 George，五官、灰白頭髮、眼鏡、鬍鬚、服裝與自身頭身比例依圖 3，不採用角色設定圖的展示姿態或構圖。

場景材質、風格與光影採用圖 1，保留木框窗、窗外綠意、墨綠牆柱、植物掛畫與椅子，空間配置依圖 2。

咖啡杯碟與糖罐外觀依圖 4，位置、比例及裁切依圖 2。杯子只有一個杯柄；糖罐採用白瓷罐身、無孔木蓋與中央木旋鈕，不沿用場景圖的打孔蓋，不為展示完整道具而移動它們。

畫面描述：
這是一張坐姿近眼高、微側拍的 George 中特寫，65mm 視角。George 的完整頭部、上半身與部分前臂可見，咖啡杯及糖罐在畫面下緣局部入鏡。畫面只有 George 一人。

George 帶著輕鬆幽默、安撫對方的微笑，嘴唇自然微張，眼神看向畫外右側對坐的 Amy，不直視鏡頭。

一隻手從桌邊稍微抬起至下胸附近，手掌自然張開、略朝 Amy，手指放鬆，呈現準備輕輕擺手說「不會不會」的起始瞬間。手不高過肩膀、不遮住臉，也不做誇張招手。另一隻手維持原本桌邊位置。

只調整揮手所需的手指、手腕與前臂，其餘肩膀、胸口、軀幹與坐姿沿用圖 2。咖啡杯仍放在原杯碟上。

焦點落在 George 的雙眼與親和笑容，眼鏡保持通透；背景適度柔化，保留窗框與綠牆的可辨識輪廓。除上述表演調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```

## 2026-10-21 shot_2.1.9 GPT v1｜待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.9_gpt_v1.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/assets/images/shot_2.1.4_short_v2.png
- 目視：Amy單人笑意、向左好奇視線與近正面肩胸成立；頭部放大上移、頭頂留白減少，構圖非精確保留blocks。 未追加重試或採用。
### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：咖啡館場景外觀參考。
圖 2 cam_amy_cu_emotion_block_blender.png：場景配置、人物位置與取景範圍參考。
圖 3 char_amy.jpeg：Amy 的五官、髮型、服裝與頭身比例參考。
圖 4 shot_2.1.4_short_v2.png：Amy 的肩胸方向與頭頸姿態參考，不沿用其驚奇表情。

生圖指引：
以圖 2 為編輯底圖，保留背景透視、物件配置、Amy 的座位位置與整體畫面佔比。保持頭頂留白及肩膀與上胸在下緣的裁切，不推近鏡頭或放大頭部。

將紅色定位人物替換為圖 3 的 Amy。人物五官、髮型、服裝與自身頭身比例採用圖 3，不採用角色設定圖的展示姿態或排版。

Amy 的肩線、胸口平面、左右翻領比例、襯衫門襟走向及頭頸關係依圖 4。允許調整圖 2 的肩胸角度以符合圖 4，但不移植圖 4 的人物大小、畫面位置或背景配置。

場景材質、風格與光影依圖 1，保留原木牆面、咖啡機、磨豆機與暖色日光，背景物件位置依圖 2，並依人物輪廓自然遮擋。

畫面描述：
這是一張坐姿近眼高的 Amy 頭肩特寫，100mm 視角。完整頭部、肩膀與部分上胸可見，手部與桌面留在畫外，畫面只有 Amy 一人。

Amy 採用圖 4 的近正面坐姿，胸口略朝畫面左側，頭頸自然承接肩胸方向，不形成扭頸回望。

Amy 聽到 George 幽默的安撫，原先緊繃的眉心放鬆，嘴角輕輕揚起，雙頰略抬，嘴唇微張，呈現剛要輕笑反問的瞬間。眼神明亮，帶著好奇、期待與輕微的不敢置信，看向畫外左側對坐的 George，不直視鏡頭。

表情是卸下壓力後的自然笑意，不大笑、不誇張露齒，不保留上一鏡的擔憂皺眉，也不加入眼淚或淚痕。

焦點落在 Amy 的雙眼與笑容，咖啡機、磨豆機與木牆適度柔化。人物姿態依圖 4，外觀依圖 3，位置與取景依圖 2，場景材質與光影依圖 1。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```

## 2026-10-21 shot_2.1.10 GPT v1｜待評鑑
- 工具：內建 image_gen／OpenAI，W2I生成1次；確切模型／費用未知。
- 輸出：assets/images/shot_2.1.10_gpt_v1.png。
- 有序輸入：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png
3. D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png
4. D:/kj-openMontage/.tmp/shot_2.1.1_background_board.png
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png
- 目視：四人、George雙手展開與Amy聆聽、無孔木蓋旋鈕成立；人物比例／手位／座椅呈現與blocks有差異，咖啡師露出範圍增加，Amy偏微笑。 未追加重試或採用。
### 完整實際 prompt
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt_v3.png：咖啡館場景外觀參考。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖與人物佔位參考。
圖 3 shot_2.1.1_leads_board.png：左半部為 George，對應圖 2 左側藍色人物；右半部為 Amy，對應圖 2 右側紅色人物。
圖 4 shot_2.1.1_background_board.png：左半部為背景女客，對應圖 2 左後方紫色人物；右半部為咖啡師，對應圖 2 最右緣綠色人物。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、桌椅配置、人物座位、整體大小、可見範圍與遮擋關係。保持兩位主角的頭頂留白、座位間距及畫面邊緣裁切，不推近鏡頭或放大人物。

將四個定位人物替換為圖 3、圖 4 的對應角色，外觀、服裝與自身頭身比例依人物參考，不採用參考板的展示姿態或排版。人物坐入既有座椅，只呈現圖 2 中可見的部位；右緣咖啡師維持局部入鏡。

場景材質、風格與光影依圖 1，保留溫暖日光、木質牆面、植物掛畫與吧台，空間配置依圖 2，不新增牆面藤蔓。

杯碟與糖罐採用圖 5 的外觀，數量、位置與比例依圖 2。每只杯子只有一個杯柄；糖罐為白瓷罐身、無孔木蓋與中央木旋鈕。參考圖中的多視角展示不代表增加道具。

畫面描述：
這是一張坐姿近眼高的雙人中景，40mm 視角。George 在左、Amy 在右，隔著木桌相向而坐，兩人的頭部、上半身、前臂與桌面清楚可見，下半身依圖 2 裁切。

George 帶著親切、鼓勵思考的神情，嘴唇微張，視線看向 Amy。身體沿面向 Amy 的方向輕微前傾，仍坐在原位；雙手在桌面上方低低地自然展開，掌心略朝上，手指放鬆，呈現準備提出引導問題的瞬間。兩手不高舉、不指向鏡頭，也不碰撞或遮住咖啡杯。

只調整輕微前傾與展手所需的軀幹、手臂、手腕及手指，不移動椅子或縮短兩人的座位距離。

Amy 專注看著 George，嘴唇輕合，眉眼放鬆，帶著開始思考的神情。雙手自然維持圖 2 的桌邊位置，不攪拌、不舉杯、不額外托腮。兩只咖啡杯都留在各自杯碟上。

左後方女客維持坐在窗邊筆電前的姿態；右緣咖啡師維持吧台後的局部身影。背景人物的位置、朝向與遮擋依圖 2，不移到前景。畫面共四人，其中咖啡師僅局部可見。

兩位主角與桌面保持清楚，背景保留足夠環境細節。除 George 指定的表演調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，保留參考圖的精緻 3D 動畫質感，不加入字幕、對白文字、角色標籤或參考圖分格。
```


### 本批檔案驗證
- shot_2.1.8：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：ad723e329c3ce8e68521eee6c541c78c60409e64df24c9fef7acc109dc961276；來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-e597c35b-93e0-44e3-b160-ec6739a69e19.png
- shot_2.1.9：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：f92e69f1554e438a9be311ec2e24ac821dcdafcfb2a6f3301bab48cfdaafd996；來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-435c7a18-ba8c-4f2a-852d-81375c92a4de.png
- shot_2.1.10：(1672, 941) RGB PNG，完整解碼／來源複本SHA256通過：48655200248f44ac6ade6324a148c7dc3b34b9bd8f1f250f4a9034db55223ba1；來源：C:\Users\servi\.codex\generated_images\01a159eb-2377-7e83-a3a4-49a26c045ad2\exec-4638ee3e-2aa7-4437-8371-9cd10414fa23.png

## 2026-10-21 shot_1.2.4 GPT v2（近景，待評鑑）
- 使用者要求再切近景；唯一輸入：assets/images/shot_1.2.4_gpt_v1.png。
- 輸出：assets/images/shot_1.2.4_gpt_v2.png。
- 內建 image_gen／OpenAI，生成一次，模型版本及費用未知。
- 目視：臉部與手機明顯放大、原錯愕表情與左上視線大致保留；髮頂被上緣輕微裁切，右手掌下部被下緣裁切，背景細節重繪。未覆蓋v1或改正式採用設定。
```text
請編輯這張圖片，將鏡頭切近一點，改成較緊的胸部以上近景。以Amy的臉部、左手貼耳的手機及胸前抬起的右手為中心，收緊左右背景與下方軀幹的取景，讓表情更突出。頭髮頂端完整入鏡並保留少量留白，持手機的左手及胸前右手的所有手指完整可見；可以裁切下方手肘及胸部以下身體。保留原圖的臉部表情、眼神方向、髮型、服裝、兩手姿勢、手機方向與接電話動作，不改變人物表演。保持原本相機方向與透視，僅切近取景，不鏡像、不轉換角度。背景仍是原辦公室，左前景螢幕僅保留裁切後自然可見部分，不新增或搬動物件。輸出一張16:9彩色近景分鏡圖，不加文字、字幕或水印。
```


## 2026-10-21 shot_1.2.5 GPT v1（待評鑑）
- 輸出：assets/images/shot_1.2.5_gpt_v1.png
- 內建 image_gen／OpenAI；模型版本與費用未知；生成一次，逐字使用使用者確認 prompt。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/clp/loc_supervisor_office_1.jpg
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_supervisor_mcu_15deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_supervisor.jpeg
- 目視：主管右手手機貼右耳、左手向畫右前方指去，皺眉張嘴與額頭汗珠呈現，指尖完整；指向手臂伸出幅度大於胸前起始狀態，人物偏左、頭頂留白減少，背景重繪且右側出現窗框。未改正式採用設定或scene_plan。
```text
參考圖說明：
圖 1 loc_supervisor_office_1.jpg：主管辦公室的材質、色彩、光影與美術參考，不採用其廣角構圖。
圖 2 cam_supervisor_mcu_15deg_block_blender.png：本鏡構圖與機位參考，藍色定位人物對應主管。
圖 3 char_supervisor.jpeg：主管的五官、髮型、身形與服裝參考，不採用其展示姿態或拼版構圖。

生圖指引：
依圖 2 的 15 度微側、平視胸上近景構圖，保留人物佔位、頭部尺度、頭頂留白、背景配置與裁切範圍。將藍色定位人物替換為圖 3 的主管，不保留方塊造型或簡化材質。

主管外觀依圖 3，保留略凌亂的黑色短髮、濃眉、明顯鼻形與淡鬍渣，穿捲袖藍色襯衫與鬆開的棕色領帶。畫面只呈現胸部以上，不補出腰部或整張辦公桌。

保留圖 2 身後的文件佈告板、牆面與藍色辦公椅位置；材質、紙張質感與日間光線採用圖 1。不要移植圖 1 的廣角桌面、窗景或其他畫外物件。

畫面描述：
畫面只有主管一人，坐在自己的辦公室，頭部完整入鏡，臉部與胸前手勢是視覺焦點。

主管右手握一支深色手機貼在右耳，也就是畫面左側，延續前一鏡的接電話方向。手機直立，頂端靠耳朵、底端朝下，螢幕朝臉、背面朝外；手指自然環握，不遮住眼睛或嘴巴。

左手抬至胸前、位於畫面右側，食指伸出，朝畫面前方略偏右指去，其餘手指自然彎曲。手勢帶有急迫交辦任務的意味，不直接戳向鏡頭，不誇大手指透視。手掌與食指完整入鏡，不遮臉；容許抬臂所需的自然肩部變化，其餘人物位置沿用圖 2。

捕捉主管急切打斷 Amy、剛要說出「現在沒時間解釋！」的瞬間：眉頭壓低並向中央收攏，眼神集中，嘴巴剛張開，表情不耐煩而堅決。額頭保留少量汗珠，呈現壓力尚未解除，但已從慌亂求救轉為不容推辭地下達任務。沒有笑容，不做悲傷哭泣表情。

上半身略向前傾，頭部與視線朝畫面右前方，不直視鏡頭。手機始終貼耳，左手停在指向前方的單一瞬間，不加入揮動殘影或多隻手。

採 65mm 鏡頭感、平視固定機位與淺景深，臉部、手機及指向前方的手清晰可辨，背景柔和虛化。人物維持精緻 3D 動畫電影質感，服裝與臉部辨識度忠於圖 3。

輸出一張 16:9 彩色分鏡圖，不加入 Amy、分割畫面、字幕、對話框、額外文字或水印。
```


## 2026-10-21 shot_2.2.7 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.2.7_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成1次。
- 目視：Amy驚奇微張嘴與三人呈現；George被擴大成左側頭肩前景、咖啡師入鏡範圍增加，Amy視線偏左上，人物尺度／留白偏離blocks。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
5. D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 4 char_george.png：George 人物參考圖，對應圖 2 左下角極少量可見的藍色人物局部。
圖 5 char_barista.png：咖啡師人物參考圖，對應圖 2 最左緣綠色人物局部。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、可見範圍與遮擋關係。

將定位人物替換為對應角色，外觀與服裝採用圖 3 至圖 5，不採用參考圖的展示姿態或構圖。只呈現圖 2 中可見的部位，不補出畫外身體。George 維持左下角極少量局部，咖啡師維持最左緣局部，不擴大兩人的入鏡範圍，不保留彩色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留咖啡機、磨豆機、木牆、桌椅與前景杯具的相對位置及裁切。

畫面描述：
這是一張 65mm、坐姿近眼高、微側角度的 Amy 中特寫。Amy 位於中央偏右，頭部、上半身與部分前臂可見，下半身在畫外。頭部尺度、頭頂留白與肩膀高度依圖 2。畫面共三人，但只有 Amy 的臉可辨識，另外兩人僅有邊緣局部入鏡。

Amy 面朝畫面左側對坐的 George，視線落在對方坐姿眼睛的高度，不看鏡頭、不向左上方仰望。她眉毛輕輕抬起，雙眼明亮而略微睜大，嘴唇自然微張，嘴角帶著剛浮現的笑意，呈現突然理解新觀點、充滿驚奇與求知慾的神情，像是正準備追問「企業做好事，才能賺到錢？」。不誇張瞪眼，不張大嘴尖叫。

這是眼睛一亮、尚未前傾的起始瞬間。肩膀與軀幹維持圖 2 的坐姿，雙手仍低放在原本位置，尚未握拳抬到胸前。咖啡杯留在杯碟上，不攪拌、不舉杯。

沿用圖 1 的日間暖陽與精緻 3D 動畫質感，淺景深聚焦 Amy 的眼睛與表情，後方咖啡設備及木牆柔和虛化。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、角色標籤或參考圖分格。
```


## 2026-10-21 shot_2.3.1 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.3.1_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成1次。
- 目視：George單人微笑、手臂低放呈現；人物偏左且頭部放大，視線偏右上、手部裁切及肩膀位置偏離blocks。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、可見範圍與遮擋關係。

將藍色定位人物替換為圖 3 的 George。外觀與服裝採用圖 3，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體部位，不補出畫外身體，不保留藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留木框窗、窗外街景、墨綠牆柱、植物掛畫、右側盆栽與局部桌面道具的位置及裁切。

畫面描述：
這是一張 65mm、坐姿近眼高、微側角度的 George 中特寫。George 位於畫面中央附近，頭部、上半身與部分前臂可見，手部與咖啡杯依圖 2 在下緣局部呈現。保持圖 2 的頭部大小、頭頂留白與肩膀高度。畫面只有 George 一人，Amy 在畫外，不增加右前景頭肩。

George 面朝畫面右側對坐的 Amy，目光自然落在對方坐姿眼睛的高度，不看鏡頭、不抬眼向右上方看。他眉眼舒展，嘴角輕輕上揚，嘴唇微張，呈現沉穩、有條理、準備開始講解的導師神情，像是正要說「他們是透過三個階段的努力」。

這是抬手比出「三」之前的起始瞬間。雙臂與可見手部仍維持圖 2 的低放位置，手指自然放鬆，尚未舉到胸前。頭部、肩膀與軀幹保持原本坐姿，不前傾，不舉杯。

沿用圖 1 的日間暖陽與精緻 3D 動畫質感，淺景深聚焦 George 的眼睛與表情。眼鏡不以強烈反光遮住瞳孔，後方窗景與墨綠牆面柔和虛化。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、數字「3」、階段圖表、對話框或參考圖分格。
```


## 2026-10-21 shot_2.3.8 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.3.8_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成1次。
- 目視：四人、主角微笑與糖罐木鈕呈現；主角前傾、手靠近杯子，Amy視線略偏左上，咖啡師入鏡範圍增加且轉為背面，人物比例／留白偏離blocks。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png
3. D:/kj-openMontage/.tmp/shot224_leads.png
4. D:/kj-openMontage/.tmp/shot224_background.png
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt_v3.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 shot224_leads.png：左半部為 George，對應圖 2 左側藍色人物；右半部為 Amy，對應圖 2 右側紅色人物。
圖 4 shot224_background.png：左半部為背景女客，對應圖 2 左後方紫色人物；右半部為咖啡師，對應圖 2 最右緣綠色人物。
圖 5 prop_coffee_set.png：白瓷咖啡杯碟與木蓋糖罐外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、人物佔位、比例、可見範圍與遮擋關係。維持人物與桌面的距離、頭頂留白及畫面邊緣裁切，不將主角往中央靠攏。

將四個定位人物替換為對應角色。人物外觀與服裝採用圖 3、圖 4 的對應角色區域，不採用其展示姿態或排版。只呈現圖 2 中可見的部位；右緣咖啡師保持局部入鏡，不補出完整身體，不保留彩色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留木牆、植物掛畫、窗邊座位、吧台與點心展示櫃的位置。

咖啡杯碟與糖罐採用圖 5 的外觀，數量、位置、比例與杯耳朝向依圖 2。每只杯子只有一個杯耳；糖罐為白瓷罐身與帶小圓木鈕的木蓋。多視角展示不代表增加道具，不帶入參考圖背景。

畫面描述：
這是一張 40mm、坐姿近眼高、輕微俯見桌面的雙人中景。George 在左、Amy 在右，隔著木桌相向而坐。兩人的頭部、上半身、前臂、手部與部分大腿可見，下方依圖 2 裁切。

George 面朝 Amy，目光與她自然相接，眉眼放鬆，嘴角帶著溫和、篤定的微笑，嘴唇微張，像是準備說「所以妳看」。這是展開雙手總結之前的瞬間，雙手仍低放在圖 2 的桌邊位置，手指放鬆，尚未向兩側展開。肩膀與軀幹維持原本坐姿。

Amy 看向 George 的眼睛，原本疑惑的眉心已舒展，嘴唇輕合、嘴角浮現理解的微笑，呈現剛把三個階段串聯起來、恍然大悟的神情。頭部維持自然位置，尚未開始點頭，雙手仍在圖 2 的桌邊位置，不比讚、不攤手。

左後方女客維持坐在窗邊筆電前的姿態；咖啡師維持最右緣、吧台後的局部身影。背景人物不參與對話，不擴大入鏡範圍。畫面共四人，其中咖啡師僅局部可見。

兩位主角的咖啡杯留在杯碟上，糖罐維持桌面中央位置。沿用圖 1 的日間暖陽與精緻 3D 動畫質感，中等景深讓兩位主角的表情清楚可辨，背景適度柔化。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、金錢符號、圖表、對話框、角色標籤或參考圖分格。
```


三鏡驗證：皆為1672×941 RGB PNG，完整解碼及來源副本SHA256核對通過。

## 2026-10-21 shot_1.1.7 GPT v1（待使用者評鑑）

- 工具／供應商：內建 image_gen／OpenAI（GPT）；工具未提供確切模型與費用，未知。各生成一次，無重試。
- 輸出：assets/images/shot_1.1.7_gpt_v1.png；1672×941 RGB PNG；完整解碼與來源複本 SHA256 一致。
- 目視檢查：右手、細條紋袖口與桌面插鏡成立；食指抬起幅度較細微，皮膚質感偏寫實。
- 未變更 asset_manifest 或正式採用設定。
- 參考圖（傳入順序，專案相對路徑）：
  1. references/scenes/investment_office/cameras/cam_table_insert_iso_empty_gpt.png
  2. references/scenes/investment_office/cameras/cam_table_insert_iso_block_blender.png
  3. clp/char_harrison.jpeg

完整 prompt：
```text
參考圖說明：
圖 1 cam_table_insert_iso_empty_gpt.png：胡桃木桌面與皮椅局部的場景外觀參考。
圖 2 cam_table_insert_iso_block_blender.png：Harrison 右手與桌面的構圖底圖。
圖 3 char_harrison.jpeg：Harrison（char_harrison）人物參考，僅提供手部膚色、年齡質感及西服袖口外觀。

生圖指引：
以圖 2 為編輯底圖，保留桌面透視、手腕位置、前臂進入畫面的方向、手部比例與裁切範圍。不拉近鏡頭，不補出人物臉部或完整身體。

將簡化方塊手替換為 Harrison 的自然右手，藍色袖子替換為圖 3 的深色細條紋西服袖口及少量白襯衫袖緣。方塊手指僅作位置引導，不照搬其簡化數量與形狀；呈現自然的五指結構，依角度保留合理遮擋，不強行攤開全部手指。

桌面、皮椅與金屬扶手的材質、風格及光影採用圖 1，空間配置沿用圖 2。

畫面描述：
這是一張 60mm、高角度斜俯拍的桌面手部特寫。Harrison 的右前臂從畫面上方伸入，手背朝上，手指朝畫面下方延伸，手部位於畫面中央附近。胡桃木桌面占據大部分畫面，左上角僅保留原有西服與座椅局部。

右手手腕穩定靠近桌面，手指自然微彎，食指指尖略微抬離木面，其餘手指輕靠桌面，呈現即將開始第一次輕敲的瞬間。手部帶有克制的緊繃感，不握拳、不拍桌，不加入動作殘影或重複手指。

焦點落在指尖、指節及其接近桌面的區域，遠處木紋與椅子輕微柔化。採圖 1 的冷靜室內光線，手部與西服保留人物參考的精緻 3D 動畫質感。

除手部自然化與上述指尖姿態外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、文字標註或浮水印。
```

## 2026-10-21 shot_1.1.8 GPT v1（待使用者評鑑）

- 工具／供應商：內建 image_gen／OpenAI（GPT）；工具未提供確切模型與費用，未知。各生成一次，無重試。
- 輸出：assets/images/shot_1.1.8_gpt_v1.png；1672×941 RGB PNG；完整解碼與來源複本 SHA256 一致。
- 目視檢查：抱臂坐姿成立；抱臂位置較低、人物較飽滿，表情比要求更強烈近怒容，背景柔焦偏弱。
- 未變更 asset_manifest 或正式採用設定。
- 參考圖（傳入順序，專案相對路徑）：
  1. references/scenes/investment_office/cameras/cam_harrison_mcu_45deg_empty_gpt.png
  2. references/scenes/investment_office/cameras/cam_harrison_mcu_45deg_block_blender.png
  3. clp/char_harrison.jpeg

完整 prompt：
```text
參考圖說明：
圖 1 cam_harrison_mcu_45deg_empty_gpt.png：會議室皮椅與陰天高樓窗景的場景外觀參考。
圖 2 cam_harrison_mcu_45deg_block_blender.png：Harrison 抱臂坐姿的構圖底圖。
圖 3 char_harrison.jpeg：Harrison（char_harrison）人物參考，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物位置與比例、頭頂留白、坐姿、雙臂交疊及椅背遮擋。不要拉近鏡頭或放大頭部；實際可見範圍依圖 2，不因中特寫名稱再裁切畫面。

將藍色定位人物替換為圖 3 的 Harrison，採用其五官、銀灰色後梳髮型、濃眉、深色細條紋西服、白襯衫與領帶，不採用人物表的展示姿態。人物直接坐入原有皮椅，不新增椅子。

場景材質、風格與光影採用圖 1，保留落地窗框、窗外高樓、皮椅與畫面邊緣家具的位置。

畫面描述：
這是一張 65mm、坐姿平視微側取景的 Harrison 單人中特寫。頭部與上半身位於畫面中央，交疊的雙臂依圖 2 保持可見，身後為棕色高背皮椅與陰天玻璃帷幕高樓。全畫面只有 Harrison 一人。

Harrison 維持雙臂交疊、身體略靠椅背的姿勢，神情冷淡而帶有審判意味。眉頭輕壓、眼神銳利，嘴唇微微分開，呈現開始說出「So, it's a black box」的瞬間。視線朝向畫外 Sandy 所在的簡報區，不直視鏡頭，不微笑、不怒吼，也不增加指人或拍桌手勢。

焦點落在眼睛與臉部，窗外大樓適度柔焦，仍能辨識建築輪廓。光線維持圖 1 的陰天冷色漫射光與調暗的室內亮度，人物保留圖 3 的精緻 3D 動畫質感。

只調整必要的表情與嘴部，其餘姿態、比例和配置沿用圖 2。台詞中的黑箱是比喻，不生成實體黑箱或圖示。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、額外字卡或浮水印。
```

## 2026-10-21 shot_1.1.9 GPT v1（待使用者評鑑）

- 工具／供應商：內建 image_gen／OpenAI（GPT）；工具未提供確切模型與費用，未知。各生成一次，無重試。
- 輸出：assets/images/shot_1.1.9_gpt_v1.png；1672×941 RGB PNG；完整解碼與來源複本 SHA256 一致。
- 目視檢查：單人 Sandy、指圖與簡報器成立；緊張眉形但嘴角略帶笑，頭部放大上移，左臂角度較低。
- 未變更 asset_manifest 或正式採用設定。
- 參考圖（傳入順序，專案相對路徑）：
  1. references/scenes/investment_office/cameras/cam_sandy_mcu_15deg_empty_gpt.png
  2. references/scenes/investment_office/cameras/cam_sandy_mcu_15deg_block_blender.png
  3. clp/char_sandy.jpeg

完整 prompt：
```text
參考圖說明：
圖 1 cam_sandy_mcu_15deg_empty_gpt.png：灰牆、木門與投影幕局部的場景外觀參考。
圖 2 cam_sandy_mcu_15deg_block_blender.png：Sandy 單人中特寫構圖底圖。
圖 3 char_sandy.jpeg：Sandy（char_sandy）人物參考，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留人物位置與比例、頭頂留白、肩胸朝向、左臂伸向右側投影幕的方向，以及畫面下緣的裁切。不放大人物，不讓頭髮貼近上邊界。

將紅色定位人物替換為圖 3 的 Sandy，採用其五官、棕色束髮、黑框眼鏡、深色西服、淺色襯衫與藍色識別證掛繩，不採用人物表的展示姿態。只呈現底圖可見的身體部位，不補出畫外右手或完整遙控器。

場景材質、風格與光影採用圖 1；保留左側木門邊緣、身後灰牆及右側投影表格的裁切位置，不更換簡報內容。

畫面描述：
這是一張 65mm、眼高平視、15 度微側取景的 Sandy 單人中特寫。她的頭部與胸肩是主體，左臂依圖 2 延伸至畫面右側，投影表格只露出邊緣。全畫面只有 Sandy 一人。

Sandy 在壓力下試圖小心地接話，內側眉梢略抬、眉心帶有緊張，嘴唇微微張開，呈現剛要說出「but」的遲疑瞬間。視線望向畫外 Harrison，眼神缺乏把握，神情退縮而仍試圖維持專業，不微笑、不哭泣、不誇張驚恐。

頭部可輕微收下巴，肩膀與軀幹仍沿用圖 2，不以縮身、前傾或轉身改變構圖。左手維持原有指示範圍，手指略放鬆，不新增攤開雙手或舉手辯論的動作。

焦點落在眼睛與猶豫的嘴部，灰牆及投影表格適度柔焦。光線與色調依圖 1，保留人物參考的精緻 3D 動畫質感。

除表情、視線及必要的細微頭部與手指調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤或浮水印。
```

## 2026-10-21 shot_1.1.10 GPT v1（待使用者評鑑）

- 工具／供應商：內建 image_gen／OpenAI（GPT）；工具未提供確切模型與費用，未知。各生成一次，無重試。
- 輸出：assets/images/shot_1.1.10_gpt_v1.png；1672×941 RGB PNG；完整解碼與來源複本 SHA256 一致。
- 目視檢查：Harrison 緊臉特寫、強烈目光與背景柔焦成立；臉部與肩膀較底圖放大，朝向更正面、視線近鏡頭。
- 未變更 asset_manifest 或正式採用設定。
- 參考圖（傳入順序，專案相對路徑）：
  1. references/scenes/investment_office/cameras/cam_harrison_cu_emotion_empty_gpt.png
  2. references/scenes/investment_office/cameras/cam_harrison_cu_emotion_block_blender.png
  3. clp/char_harrison.jpeg

完整 prompt：
```text
參考圖說明：
圖 1 cam_harrison_cu_emotion_empty_gpt.png：皮椅背與陰天高樓窗景的場景外觀參考。
圖 2 cam_harrison_cu_emotion_block_blender.png：Harrison 臉部特寫構圖底圖。
圖 3 char_harrison.jpeg：Harrison（char_harrison）人物參考，對應圖 2 的人物。

生圖指引：
以圖 2 為編輯底圖，保留頭部位置、大小、頭頂留白、肩部裁切、相機角度及椅背與窗框的位置。不再推近，不裁掉頭髮，不把人物移向畫面邊緣。

將定位人物替換為圖 3 的 Harrison，採用其臉型、銀灰色後梳髮型、濃眉、眼睛、鼻形、皺紋及西服外觀，不採用人物表的展示構圖。只呈現底圖可見的頭頸、肩膀與西服上部，不補出雙手或抱臂。

場景材質、風格與光影採用圖 1，保留棕色皮椅背、窗框及窗外高樓的配置。

畫面描述：
這是一張 85mm、平視的 Harrison 單人臉部特寫。頭部居中，肩膀與西服上部由畫面下緣裁切，身後可見棕色皮椅背及陰冷高樓。全畫面只有 Harrison 一人。

Harrison 目光凌厲、眉峰壓低，下顎收緊，嘴唇微微分開，呈現果斷打斷 Sandy、即將說出「Risk is not attractive」的瞬間。表情不容置疑但保持克制，不怒吼、不露出誇張齜牙，也不微笑。視線鎖定畫外 Sandy，頭部與肩胸朝向基本沿用圖 2，不轉成正對鏡頭的宣傳肖像。

焦點精準落在雙眼、眉頭與面部細節，皮椅背與窗外建築適度柔焦。採圖 1 的冷色陰天光線，保持臉部可辨識，不新增戲劇性聚光或過黑陰影。人物保持圖 3 的精緻 3D 動畫質感。

除上述表情與必要的嘴部調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、台詞、ON HOLD 字卡或浮水印。
```

## 2026-10-21 shot_1.1.11 GPT v1（待使用者評鑑）

- 工具／供應商：內建 image_gen／OpenAI（GPT）；工具未提供確切模型與費用，未知。各生成一次，無重試。
- 輸出：assets/images/shot_1.1.11_gpt_v1.png；1672×941 RGB PNG；完整解碼與來源複本 SHA256 一致。
- 目視檢查：右手握紅柄銀座印章、書面文字與尚未蓋印成立；底面懸空及投影可辨，手部皮膚偏寫實。
- 未變更 asset_manifest 或正式採用設定。
- 參考圖（傳入順序，專案相對路徑）：
  1. references/scenes/investment_office/cameras/cam_table_insert_top_empty_gpt.png
  2. references/scenes/investment_office/cameras/cam_table_insert_top_block_blender.png
  3. clp/char_harrison.jpeg
  4. clp/prop_proposal_document.png
  5. clp/prop_stamp_onhold.png

完整 prompt：
```text
參考圖說明：
圖 1 cam_table_insert_top_empty_gpt.png：胡桃木桌面的場景外觀參考。
圖 2 cam_table_insert_top_block_blender.png：手握印章與計畫書的俯拍構圖底圖。
圖 3 char_harrison.jpeg：Harrison（char_harrison）人物參考，僅提供右手膚色、年齡質感及西服袖口外觀。
圖 4 prop_proposal_document.png：大成公司增資計畫書外觀參考。
圖 5 prop_stamp_onhold.png：ON HOLD 印章及印記樣式參考。

生圖指引：
以圖 2 為編輯底圖，保留實際俯拍透視、桌面方向、計畫書位置與裁切，以及手臂從畫面上方伸入的關係。不改成另一個垂直俯視機位，不補出臉部。

將方塊手替換為 Harrison 的自然右手，藍色衣袖替換為圖 3 的深色細條紋西服袖口與白襯衫袖緣。手指自然包握印章握柄，不照搬方塊手的簡化指數，不與握柄互相穿透。

圖 2 的計畫書採用圖 4 的白色封面、深藍書脊、深藍標題與淺藍綠圖形。封面文字沿用「大成公司」「增資計畫書」「CAPITAL INCREASE PROPOSAL」。只生成一本平放的計畫書，不複製參考圖中的多視角書冊。

印章採用圖 5 的紅色圓潤握柄、銀灰色金屬長方形底座、黑色橡膠底面及紅底白字 ON HOLD 側面標牌。只生成一枚印章，不帶入參考圖旁邊獨立展示的紅色印記。

桌面與座椅局部的材質、光影依圖 1。

畫面描述：
這是一張 50mm、沿用圖 2 斜俯角度的桌面手部插鏡。計畫書居於畫面中央，下方仍依底圖裁切；Harrison 的右手從上方伸入，牢牢握住印章。

作為即將蓋印的起始畫面，將手與印章一同略微抬起，使橡膠底面與計畫書封面之間留有清楚但很小的間隙。印章底面平行於書面，對準原本預定的落印位置，呈現蓄勢下壓前的瞬間。除此之外，不移動書冊或改變手臂的進入方向。

此刻封面尚未留下紅色 ON HOLD 印記；不在印章仍懸空時提前生成完成印記，不加入飛濺墨水、震動線或重複手部。保留自然的懸空陰影與物件厚度。

焦點落在握章手、印章與書面，周圍木紋適度柔化。光線克制、冷靜，手部與道具融入同一精緻 3D 動畫畫面。

輸出一張 16:9 彩色分鏡圖，保留道具本身的文字，不加入額外字幕、字卡或浮水印。
```

## 2026-10-21 shot_1.1.12 GPT v1（待使用者評鑑）

- 工具／供應商：內建 image_gen／OpenAI（GPT）；工具未提供確切模型與費用，未知。各生成一次，無重試。
- 輸出：assets/images/shot_1.1.12_gpt_v1.png；1672×941 RGB PNG；完整解碼與來源複本 SHA256 一致。
- 目視檢查：辦公區廣角、單人 Amy、隔板遮擋與日間光線成立；Amy 睜眼朝工作區、低頭幅度輕微。未逐物件像素級驗證空間一致性。
- 未變更 asset_manifest 或正式採用設定。
- 參考圖（傳入順序，專案相對路徑）：
  1. references/scenes/staff_office/cameras/cam_office_wide_level_empty_gpt_v2.png
  2. references/scenes/staff_office/cameras/cam_office_wide_level_block_blender.png
  3. clp/char_amy.jpeg

完整 prompt：
```text
參考圖說明：
圖 1 cam_office_wide_level_empty_gpt_v2.png：行政辦公區的場景外觀參考。
圖 2 cam_office_wide_level_block_blender.png：辦公區廣角全景與 Amy 工位的構圖底圖。
圖 3 char_amy.jpeg：Amy（char_amy）人物參考，對應圖 2 中景中央的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留廣角取景、透視、多排工位、中央走道、隔板與螢幕配置，以及 Amy 的位置、大小與遮擋關係。不拉近鏡頭，不放大 Amy，不降低隔板來露出人物。

將紅色定位人物替換為圖 3 的 Amy，採用其棕色短波浪髮、五官、灰色西服與淺色襯衫，不採用人物表的展示姿態。直接坐入原有工位座椅，不新增椅子。只呈現圖 2 可見的頭部與上半身，雙手、桌面工作區及下半身若被隔板與螢幕遮住，維持遮擋。

場景材質、風格與光影採用圖 1，保留圖 2 的工位數量、薄荷綠隔板、書櫃、盆栽、百葉窗、門與天花配置。場景圖只提供外觀，不改變構圖底圖的空間比例。

畫面描述：
這是一張 22mm、較高機位望向開放辦公區的廣角全景，畫面呈現尚未向 Amy 工位推進的起始狀態。多排薄荷綠工位由前景延伸至後方，走道保持通暢。Amy 坐在中景中央的原工位，人物在廣闊辦公室中維持底圖的小比例。

Amy 正專注工作，頭部略低，視線落在自己面前的螢幕與工作區，神情平靜認真，呈現尚未被急促來電打斷的瞬間。肩膀與軀幹維持原坐姿，不站起、不轉頭看鏡頭、不提前拿起手機。隱藏在隔板後的雙手與手機不補到可見區域。

全畫面只呈現 Amy 一位人物，其餘工位維持空置，不自行加入同事。

採圖 1 明亮的日間辦公室光線，百葉窗透入自然日光，保留柔和窗影、木質桌面、布面隔板及植物材質。Amy 保持人物參考的精緻 3D 動畫質感，與辦公室的光線一致。

採深景深，工位、走道、窗戶與書櫃均清楚可辨，不以人物特寫或背景散景取代辦公區全景。

除人物替換與輕微低頭工作的姿態外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、手機鈴聲符號、震動線、字卡或浮水印。
```



## 2026-10-21 shot_1.2.6 GPT v1（待評鑑）
- 輸出：assets/images/shot_1.2.6_gpt_v1.png
- 內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成一次，逐字使用確認prompt。
- 有序參考圖：["D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_gpt_v2.png","D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_15deg_block_blender.png","D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg","D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png"]
- 目視：左手手機貼左耳、右手畫外與不安表情呈現；視線偏左上而非左下，人物輪廓／尺度及背景遮擋偏離blocks。
- 未改正式採用設定或scene_plan。
```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_gpt_v2.png：場景外觀參考圖。
圖 2 cam_amy_mcu_15deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_smartphone.png：手機機身外觀參考，不採用來電介面。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部尺度、頭頂留白、可見範圍與背景遮擋。

將紅色定位人物替換為圖 3 的 Amy，保留棕色短髮、灰色西裝與米白襯衫，不採用人物參考圖的展示姿態。只呈現原構圖可見的身體部位，不補出桌面或下半身。

調整左臂，讓 Amy 左手握手機貼在左耳，也就是畫面右側。手機外觀採用圖 4，頂端靠耳朵、底端朝下，螢幕朝臉、背面與三鏡頭朝外。左手自然環握，手機與手指不遮住眼睛和嘴巴。右手低放在畫外，不增加胸前手勢。

場景材質、色彩與光影採用圖 1，不改變圖 2 的隔板、辦公椅、螢幕、書櫃與百葉窗配置。

畫面描述：
這是一張平視、15 度微側的肩胸以上近景，畫面只有 Amy 一人。頭部完整入鏡，沿用圖 2 的人物比例與裁切。

捕捉 Amy 剛要弱弱說出「報告協理，ESG我也不懂啊……」的瞬間。她眉頭緊蹙、內側眉角微微抬高，眼神不安，嘴角下垂，嘴唇輕微分開，呈現想求饒卻沒有把握的無助神情。沒有笑容、不流淚、不張嘴大哭。

下巴稍微收低，視線朝畫面左前方偏下，不看鏡頭。肩膀略微縮起，左手仍將手機貼耳，身體沒有大幅後仰。

臉部與持電話的手清晰，背景柔和虛化，保留原辦公室日間光線。除接電話姿態、表情及視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入其他人物、分割畫面、字幕、對話框或水印。
```

## 2026-10-21 shot_1.2.7 GPT v1（待評鑑）
- 輸出：assets/images/shot_1.2.7_gpt_v1.png
- 內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成一次，逐字使用確認prompt。
- 有序參考圖：["D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v2.png","D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_block_blender.png","D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg","D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png"]
- 目視：手機仍貼左耳、雙眼張大、嘴微張且未後仰；視線偏左上，人物尺度／頭頂留白及背景遮擋偏離blocks。
- 未改正式採用設定或scene_plan。
```text
參考圖說明：
圖 1 cam_amy_ms_15deg_empty_gpt_v2.png：場景外觀參考圖。
圖 2 cam_amy_ms_15deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_smartphone.png：手機機身外觀參考，不採用來電介面。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、比例、頭頂留白、可見範圍及遮擋關係。

將紅色定位人物替換為圖 3 的 Amy，服裝與外觀忠於參考，不採用其展示姿態。維持原中景裁切，不補出畫外桌面、鍵盤或下半身。

Amy 左手握手機貼近左耳，也就是畫面右側。手機外觀依圖 4，頂端靠耳朵、底端朝下，螢幕朝臉、背面朝外。右手低放在畫外，不增加手勢。

場景材質、風格與光影更新為圖 1，保留圖 2 左前景螢幕、網布椅、青綠隔板與後方書櫃百葉窗的配置。

畫面描述：
這是一張平視、15 度微側的 Amy 單人中景。頭部完整入鏡，上半身可見，左前景螢幕保留原遮擋範圍。

捕捉主管突然從電話裡提高音量、Amy 剛被震住的瞬間。她雙眼突然張大，眉毛抬起，嘴唇微張，表情由求饒轉為錯愕，沒有笑容。肩頸略微繃緊，下巴稍向後收，但軀幹仍停留在原座位位置，不做誇張後仰。

左手此刻仍把手機貼近左耳，尚未移到眼前，也尚未低頭查看螢幕。視線僵在畫面左前方，不直視鏡頭。這是後續主管掛斷、Amy 緩緩移開手機的動作起點。

人物與手機清晰，背景保留中等景深。主管只有電話聲，不出現在畫面，不加入主管小視窗、聲波、驚嘆號或動作殘影。除上述接電話姿態與反應外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、額外文字或水印。
```

## 2026-10-21 shot_1.2.8 GPT v1（待評鑑）
- 輸出：assets/images/shot_1.2.8_gpt_v1.png
- 內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成一次，逐字使用確認prompt。
- 有序參考圖：["D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_gpt_v2.png","D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_15deg_block_blender.png","D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg","D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png"]
- 目視：左手手機已離耳、背面朝鏡頭，低頭與困惑神情呈現；手機頂端高於指定下巴位置，視線對準螢幕的程度待評鑑，人物尺度與背景遮擋有變。
- 未改正式採用設定或scene_plan。
```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_gpt_v2.png：場景外觀參考圖。
圖 2 cam_amy_mcu_15deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。
圖 4 prop_smartphone.png：手機機身外觀參考，不採用來電介面。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部尺度、頭頂留白、裁切與背景配置。

將紅色定位人物替換為圖 3 的 Amy，外觀與服裝忠於參考，不採用其展示姿態。只呈現原構圖可見的肩胸以上範圍，不為展示手機拉遠鏡頭。

調整左臂與左手：手機已從左耳移開，現在由左手直立握在臉前偏左、也就是畫面右側，距離臉部約二十至三十公分。手機頂端約在下巴高度，手機與握持手的下部可以自然延伸至畫面下緣之外，不遮住臉部。

手機外觀依圖 4，螢幕朝向 Amy，背面與三鏡頭朝向鏡頭，頂端朝上、底端朝下。不要為展示螢幕而翻轉手機，不加入仍在來電的介面。右手留在畫外。

場景材質、風格與光影更新為圖 1，不改變圖 2 的空間配置。

畫面描述：
這是一張平視、15 度微側的 Amy 單人肩胸以上近景，頭部完整入鏡。

電話已被主管掛斷。Amy 低頭些許，雙眼明確看向畫面右下方、自己左手中的手機螢幕。眉心輕微收攏，眼神迷茫，嘴唇剛分開，像準備一字一頓地念出「E……S……G……」。神情困惑而恍惚，沒有笑容，也不是驚恐尖叫。

身體停在椅上，肩膀稍微鬆下來，手機保持離耳、停在眼前的狀態。只有這一個瞬間，不加入忙音符號或文字。

臉部與眼睛清晰，手機外觀仍可辨識，背景青綠隔板與百葉窗柔和虛化。除指定持手機姿態、低頭與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入其他人物、仙丹、幻想物件、字幕、對話框或水印。
```

## 2026-10-21 shot_1.2.9 GPT v1（待評鑑）
- 輸出：assets/images/shot_1.2.9_gpt_v1.png
- 內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成一次，逐字使用確認prompt。
- 有序參考圖：["D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_cu_emotion_empty_gpt_v2.png","D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_cu_emotion_block_blender.png","D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg"]
- 目視：頭部完整、嘴微張、手機與雙手畫外，背景柔焦；視線明顯朝上而非接近鏡頭方向遠處，頭部比例與肩部可見範圍偏離blocks。
- 未改正式採用設定或scene_plan。
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt_v2.png：辦公室場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：臉部特寫構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、頭部佔位、比例、頭頂留白與裁切範圍。

將定位人物替換為圖 3 的 Amy，保留棕色短髮、綠色眼睛、五官與可見衣領，不採用人物參考圖的展示姿態或拼版構圖。完整保留頭頂與下巴，僅呈現原構圖中少量可見的肩部。手機與雙手均在畫外，不為展示道具擴大取景。

將背景的材質、色彩與日間光線更新為圖 1，不改變圖 2 的隔板、椅背、螢幕、書櫃與百葉窗配置；依特寫的極淺景深柔和虛化背景。

畫面描述：
這是一張 85mm 鏡頭感、平視的 Amy 單人臉部特寫。頭部居中，沿用圖 2 的尺度與留白，雙眼是視覺焦點。

捕捉 Amy 從困惑開始轉入白日夢的瞬間。她的眉心略微放鬆，嘴唇微微分開，表情恍惚，沒有笑容。視線從下方手機移到接近鏡頭方向的遠處，像看穿眼前事物，沒有與觀眾互動的神情。

以自然的目光放空表達注意力飄走，兩眼方向協調，保留正常綠色虹膜、瞳孔與眼睛高光，不做鬥雞眼、翻白眼、發光瞳孔或誇張瞳孔放大。臉部與眼睛本身保持清晰，不用模糊五官表現失焦。

此刻仍在辦公室，背景尚可隱約辨識，只是柔和失焦。這是後續鏡頭推近雙眼、背景化為光斑的起始畫面；本張不加入幻想世界、魔法粒子、光圈或轉場疊影。

輸出一張 16:9 彩色分鏡圖，不加入其他人物、字幕、額外文字或水印。
```


## 2026-10-21 shot_2.4.1 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.4.1_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成1次。
- 目視：Amy皺眉微張嘴、低放手臂及George過肩呈現；Amy視線偏左上，George頭頂裁切，人物比例／留白／遮擋偏離blocks。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_amy_ots_george_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 4 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、可見範圍與遮擋關係。

將紅色定位人物替換為圖 3 的 Amy，藍色定位人物替換為圖 4 的 George。外觀與服裝採用人物參考圖，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體部位，不補出畫外身體，不保留紅藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留木牆、吧台、咖啡機、桌椅與杯碟的位置及裁切，不額外加入黑板菜單。

畫面描述：
這是一張坐姿近眼高平視、從 George 身後越過肩膀拍攝 Amy 的過肩鏡頭。George 的後腦、頸部、肩背與部分手臂佔據左前景，左側及下方依圖 2 裁切，不轉頭露出正臉。Amy 位於右側中景，頭部、上半身與桌邊部分手臂可見。保持兩人的距離、頭頂留白及前後景比例，畫面只有兩人。

Amy 面朝左側對坐的 George，視線落在對方坐姿眼睛的高度，不看鏡頭、不向左上方仰望。她眉頭輕皺，一側眉毛略微挑起，嘴角平穩而不帶笑意，嘴唇微張，呈現正在思考漏洞、帶著保留的質疑神情，像是準備說「可是……上有政策，下有對策」。表情認真而有疑問，不憤怒、不誇張瞪眼。

這是開始提出疑問、尚未抬手比劃的瞬間。Amy 的雙臂仍低放在圖 2 的桌邊位置，手指自然放鬆，尚未抬到胸前；被 George 遮住的手部維持遮擋。肩膀、軀幹與坐姿沿用圖 2，不前傾。George 保持面向 Amy 的安靜聆聽姿態。

沿用圖 1 的日間暖陽與精緻 3D 動畫質感。淺景深聚焦 Amy 的眼睛與表情，George 前景及背景咖啡設備柔和虛化。咖啡杯留在杯碟上。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、角色標籤或參考圖分格。
```


## 2026-10-21 shot_2.4.2 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.4.2_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成1次。
- 目視：George單人認真微張嘴、手臂低放呈現；頭部放大、留白減少，視線略偏右上，手部裁切及肩膀位置偏離blocks。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、可見範圍與遮擋關係。

將藍色定位人物替換為圖 3 的 George。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體部位，不補出畫外身體，不保留藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留木框窗、窗外街景、墨綠牆柱、植物掛畫、右側盆栽與局部桌面道具的位置及裁切。

畫面描述：
這是一張坐姿近眼高、微側角度的 George 中特寫。George 位於畫面中央附近，頭部、上半身與部分前臂可見，咖啡杯及手部依圖 2 在下緣局部呈現。頭部大小、頭頂留白、肩膀位置與身體尺度依圖 2，不另行放大或收緊裁切。畫面只有 George 一人，Amy 位於畫外。

George 面朝畫面右側對坐的 Amy，雙眼穩定看向對方坐姿眼睛的高度，不看鏡頭、不向右上方仰望。他眉心輕輕收攏，嘴角自然平穩，嘴唇微張，呈現理解對方疑問、認真承認現實的神情，像是正準備說「沒錯，光有政策，企業不見得會認真落實」。不微笑，不憤怒，保留沉著可信的導師氣質。

這是開始點頭回應之前的瞬間。頭部、肩膀與軀幹維持圖 2 的自然坐姿，尚未前傾。雙臂與可見手部仍低放在原本位置，右手食指尚未抬起，不比三、不指人、不舉杯。

沿用圖 1 的日間暖陽與精緻 3D 動畫質感，淺景深聚焦 George 的眼睛及表情。眼鏡保持清晰，不以強烈反光遮住瞳孔；窗景與墨綠牆面柔和虛化。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、圖表、對話框、角色標籤或參考圖分格。
```


## 2026-10-21 shot_2.4.7 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.4.7_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡生成1次。
- 目視：George單人嚴肅微張嘴、雙手與桌面畫外呈現；頭部放大、留白減少，軀幹顯得前傾、肩膀位置及背景遮擋偏離blocks，視線較接近鏡頭。未重試或改採用設定。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整實際 prompt：

```text
參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_george_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、可見範圍與遮擋關係。

將藍色定位人物替換為圖 3 的 George。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。只呈現圖 2 中可見的身體部位，不補出畫外身體，不保留藍色 blocks 外觀。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留左側木框窗、後方墨綠牆柱、右上方局部植物掛畫及椅背的位置與裁切。

畫面描述：
這是一張坐姿近眼高、微側角度的 George 單人臉部特寫。George 的頭部、頸部、肩膀與上胸入鏡，下方依圖 2 裁切。保持圖 2 的頭部大小、頭頂留白及肩膀高度，不把臉放大到貼近畫面上緣。畫面只有 George 一人，Amy、雙手與桌面均在畫外。

George 面朝畫面右側的 Amy，視線穩定落在對方坐姿眼睛的高度，不看鏡頭、不向右上方仰望。他眉毛略微壓低並向眉心收攏，眼神專注、堅定而有說服力，嘴角平穩、沒有笑意，嘴唇微張，像是正準備一字一句說出「這三股力量來得又急又猛」。表情帶著急迫感與重量，但不怒吼、不咬牙、不誇張瞪眼。

頭部、肩膀與軀幹維持圖 2 的自然坐姿，不向鏡頭前傾。雙手保持畫外，不為呈現敲桌動作而加入拳頭、手臂或桌面，也不改變取景。

沿用圖 1 的日間暖陽與精緻 3D 動畫質感。眼鏡不以強烈反光遮住瞳孔，淺景深清楚呈現眼睛、眉毛與嘴部表情；窗景、墨綠牆面及植物掛畫柔和虛化。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、警告符號、圖表、對話框、角色標籤或參考圖分格。
```


三鏡驗證：皆為1672×941 RGB PNG，完整解碼及來源副本SHA256核對通過。

## 2026-10-21 GPT 批次：shot_2.1.11–14、16–21、23–27、29
使用內建 image_gen / OpenAI；實際模型及費用未知。16鏡共17次調用，14張輸出；14首批無可用結果後再次調用仍被output moderation_blocked，25同樣被拒。未採用。道具拼板由原始coffee_set、prop_notebook、prop_pen完整上下排列，未重繪。

### shot_2.1.11
結果：assets/images/shot_2.1.11_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：攤手提問成立；糖罐仍為孔洞蓋，桌面與前景遮擋偏離底圖。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png"]
完整送出prompt：<br>shot_2.1.11<br>參考圖說明：<br>圖1 cam_george_ots_amy_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_george_ots_amy_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀，替換藍色人物。<br>圖4 char_amy.jpeg：Amy外觀，替換紅色人物。<br>圖5 prop_coffee_cup.png：咖啡道具外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>越過Amy肩膀觀看George的過肩中近景，60mm坐姿近眼高。George左側至中央，Amy後腦肩膀在右前景，大小遮擋依圖2。George正溫和詢問『如果這間公司開在妳家隔壁，妳希望它符合什麼條件？』注視Amy、略抬眉、親切微笑、嘴唇自然微張。一手身側低處小幅向外攤開示意隔壁，手不伸向鏡頭。咖啡杯在原位置杯碟上。Amy保持聆聽只見原有後腦肩膀。焦點George雙眼與表情，前景柔化，不新增房屋建築圖示。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.12
結果：assets/images/shot_2.1.12_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：思考及單指成立；George擴大成左前景，咖啡師可見範圍擴大。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png", "D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.12<br>參考圖說明：<br>圖1 cam_amy_mcu_45deg_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_mcu_45deg_block_blender.png：構圖與佔位編輯底圖。<br>圖3 shot_2.1.1_leads_board.png：角色外觀拼板：左George替換藍色，右Amy替換紅色。<br>圖4 char_barista.png：咖啡師外觀，替換綠色局部。<br>圖5 prop_coffee_set.png：咖啡杯碟糖罐外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>Amy斜側中近景65mm坐姿近眼高，上半身與原可見手部入鏡。她思考『開在我家隔壁？嗯……』輕側傾頭、眉心略收、看畫外左側George、嘴唇微張。捕捉準備列第一條件：一手低處自然抬起伸出一根手指，餘指放鬆彎曲，另一手靠近桌面。不要同時表演噪音廢水氣味三情境。左下George只保留原有極小局部，不擴成過肩前景；左側咖啡師只保留局部軀幹，不補頭部。Amy唯一清楚主要臉孔，背景咖啡機磨豆機木牆柔化。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.13
結果：assets/images/shot_2.1.13_gpt_v1.png；1672×940 RGB；解碼與複本SHA256一致
目視：雙手攤開期待表情成立；桌面與糖罐暴露增加。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.13<br>參考圖說明：<br>圖1 cam_amy_ots_george_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_ots_george_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀，替換藍色人物。<br>圖4 char_amy.jpeg：Amy外觀，替換紅色人物。<br>圖5 prop_coffee_set.png：咖啡道具外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>越過George肩膀觀看Amy的過肩中近景60mm。George後腦肩膀佔左前景，Amy右側中景。Amy說『最好是很乾淨、很環保的樣子』，看George、眼神明亮、眉毛舒展、期待自然微笑、嘴唇略張。雙手下胸附近小幅向外攤開掌心略上，表達乾淨舒適期待；手只呈現原可見範圍，George與下緣遮住部分維持遮擋，頭略低頷。焦點臉部手勢，不加葉片地球綠光環保圖示，不新增垂藤。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.14
結果：未生成圖片；shot14首批未保存錯誤；第二次回傳moderation_blocked，request e10a0f71-645b-421a-b6eb-87f030b9c9d0
目視：未產出圖片；輸出安全審查 moderation_blocked（other）。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png"]
完整送出prompt：<br>shot_2.1.14<br>參考圖說明：<br>圖1 cam_george_cu_emotion_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_george_cu_emotion_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀替換藍色。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>George頭肩特寫100mm坐姿近眼高，完整頭部肩膀部分上胸，手桌畫外。George正溫和說『很好，妳剛才所說的幾點……』，注視畫外Amy、嘴角微揚、眼角柔和笑意、眉放鬆、嘴唇自然微張。捕捉輕點頭肯定，下巴僅略低，成熟親切導師神情不誇張大笑。焦點雙眼眼鏡表情，綠牆窗光畫作柔化，只有George一人。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.16
結果：assets/images/shot_2.1.16_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：筆記本筆外觀及書寫成立；咖啡師消失，左前景殘留藍色，桌面範圍增加。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png", "D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png", "D:/kj-openMontage/.tmp/esg_notebook_props_board.png"]
完整送出prompt：<br>shot_2.1.16<br>參考圖說明：<br>圖1 cam_amy_mcu_45deg_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_mcu_45deg_block_blender.png：構圖與佔位編輯底圖。<br>圖3 shot_2.1.1_leads_board.png：角色外觀拼板：左George替換藍色，右Amy替換紅色。<br>圖4 char_barista.png：咖啡師外觀，替換綠色局部。<br>圖5 esg_notebook_props_board.png：道具拼板：上咖啡杯碟糖罐、中prop_notebook.png筆記本、下prop_pen.png筆。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>Amy斜側中近景65mm。聽懂George後理解淺笑，輕低頭看面前筆記本。捕捉記重點瞬間：右手握筆書寫，左手輕扶筆記本，肩放鬆，上半身僅略前傾。加入筆記本與書寫是本鏡對定位圖必要調整，其餘構圖保持。筆記本與筆依圖5中下部：綠色布面封皮、米色橫線內頁的攤開筆記本，深灰筆身銀色配件的按壓筆。筆記本平放在Amy面前、身體與杯碟之間可用桌面，橫線朝向Amy，尺寸符合手部比例；不移動杯碟糖罐。只呈現原裁切內可見局部，不拉遠展示整本，頁面文字留待後製，不生成假文字。George左下極小局部與咖啡師左側無頭軀幹保持原裁切。重點是理解後認真記錄神情。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.17
結果：assets/images/shot_2.1.17_gpt_v1.png；1672×940 RGB；解碼與複本SHA256一致
目視：掌心朝上提問成立；糖罐孔洞蓋，前景與桌面遮擋偏差。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png"]
完整送出prompt：<br>shot_2.1.17<br>參考圖說明：<br>圖1 cam_george_ots_amy_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_george_ots_amy_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀，替換藍色人物。<br>圖4 char_amy.jpeg：Amy外觀，替換紅色人物。<br>圖5 prop_coffee_cup.png：咖啡道具外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>越過Amy肩膀看George過肩中近景60mm，George左至中，Amy後腦肩在右前景。George正問『那對人呢？妳會希望這間公司怎麼對待員工、鄰居、客戶、供應商？』看Amy略抬眉，溫和好奇嘴唇微張。一手低處略抬掌心向上，把下一個問題交給Amy，開放自然，不逐一數四類對象，另一手放鬆。Amy專注聆聽。焦點George神情與提問手勢，不加人群圖示。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.18
結果：assets/images/shot_2.1.18_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：胸前手勢真誠表情成立；咖啡師消失，George前景擴大。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png", "D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.18<br>參考圖說明：<br>圖1 cam_amy_mcu_45deg_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_mcu_45deg_block_blender.png：構圖與佔位編輯底圖。<br>圖3 shot_2.1.1_leads_board.png：角色外觀拼板：左George替換藍色，右Amy替換紅色。<br>圖4 char_barista.png：咖啡師外觀，替換綠色局部。<br>圖5 prop_coffee_set.png：咖啡杯碟糖罐外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>Amy斜側中近景65mm，看畫外左George，說『對員工，當然要提供合理薪資福利，關心他們成長和幸福感囉。』一手輕放自己上胸、手指自然舒展，真誠表達身為員工感受，另一手靠桌。肩軀幹沿圖2不轉向鏡頭。認真溫暖眼神、眉柔和抬起、淡淡笑意、嘴唇自然微張，不宣誓或激昂演講。George左下極小局部與咖啡師左側無頭局部依原裁切。焦點眼睛神情胸前手勢。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.19
結果：assets/images/shot_2.1.19_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：向前攤手成立；糖罐移到畫面右側，桌面增加。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.19<br>參考圖說明：<br>圖1 cam_amy_ots_george_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_ots_george_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀，替換藍色人物。<br>圖4 char_amy.jpeg：Amy外觀，替換紅色人物。<br>圖5 prop_coffee_set.png：咖啡道具外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>越過George肩膀看Amy過肩中近景60mm，George左前景、Amy右中景。Amy說『對客戶則要誠實，賣安全又可靠產品』，注視George、認真自信、眉自然、嘴唇微張、溫和堅定。一手桌面上方低處略向前伸、掌心斜上、手指自然併攏，坦誠強調安全可靠。頭略低頷另一手放鬆。手依機位自然遮擋，不越過George輪廓刻意展示。不加商品包裝盾牌認證圖示。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.20
結果：assets/images/shot_2.1.20_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：四人與交握雙手成立；背景咖啡師完整頭部入鏡，杯內有白色突起。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png", "D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png", "D:/kj-openMontage/.tmp/shot_2.1.1_background_board.png", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.20<br>參考圖說明：<br>圖1 cam_twoshot_ms_level_empty_gpt_v3.png：咖啡館場景外觀。<br>圖2 cam_twoshot_ms_level_block_blender.png：構圖與佔位編輯底圖。<br>圖3 shot_2.1.1_leads_board.png：角色外觀拼板：左George替換藍色，右Amy替換紅色。<br>圖4 shot_2.1.1_background_board.png：背景人物拼板：左上班族女性替換紫色，右咖啡師替換綠色。<br>圖5 prop_coffee_set.png：咖啡杯碟糖罐外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>坐姿近眼高雙人中景40mm，George左Amy右隔木桌對坐。Amy說『對供應商要像夥伴一樣公平合作一起進步』，捕捉自己的雙手輕交握示意合作，雙手身前低處手指自然，不跟George握手、不另外同時伸展雙臂。Amy看George真誠自信笑容，George專注看她微笑下巴稍低表示認同。背景上班族女性及咖啡師各自活動，位置裁切依圖2，不參與對話。桌面兩組杯碟糖罐保持，不加社區景象或合作圖示。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.21
結果：assets/images/shot_2.1.21_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：無人物橫向平板深色螢幕成立；奶泡環硬、杯內白色突起，糖罐完整入鏡。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_table_insert_top_empty_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/prop_ipad_landscape.png", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.21<br>參考圖說明：<br>圖1 cam_table_insert_top_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_table_insert_top_empty_blender.png：構圖與佔位編輯底圖。<br>圖3 prop_ipad_landscape.png：橫向平板硬體外觀。<br>圖4 prop_coffee_set.png：杯碟糖罐外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>木桌高角度斜俯近景50mm，圖2為無人物空景底圖，不適用角色替換。保留桌面透視兩組杯碟位置杯耳朝向糖罐可見範圍。在兩杯之間桌面空處加入唯一一台橫向平板，平放螢幕朝上，真實比例不重疊杯碟糖罐。硬體邊框厚度材質依圖3，不複製正背側三視圖排版。螢幕乾淨低反光深色底面，完整螢幕區供後製，不複製投資數字金融圖表。暖陽在木桌白杯碟，平板清楚，無人物手臂手部懸浮圖示文字。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.23
結果：assets/images/shot_2.1.23_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：筆記本筆與低頭微笑成立；左前景George仍藍色，背景咖啡師範圍增加。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png", "D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png", "D:/kj-openMontage/.tmp/esg_notebook_props_board.png"]
完整送出prompt：<br>shot_2.1.23<br>參考圖說明：<br>圖1 cam_amy_mcu_45deg_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_mcu_45deg_block_blender.png：構圖與佔位編輯底圖。<br>圖3 shot_2.1.1_leads_board.png：角色外觀拼板：左George替換藍色，右Amy替換紅色。<br>圖4 char_barista.png：咖啡師外觀，替換綠色局部。<br>圖5 esg_notebook_props_board.png：道具拼板：上咖啡杯碟糖罐、中prop_notebook.png筆記本、下prop_pen.png筆。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>Amy斜側中近景65mm。輕低頭看面前環境與社會責任筆記，滿意理解淺笑。捕捉看完輕點頭瞬間、下巴略低肩放鬆。右手握筆自然停紙面附近，左手靠筆記本，不同時指點或大幅書寫。筆記本與筆依圖5中下部：綠色布面封皮、米色橫線內頁的攤開筆記本，深灰筆身銀色配件的按壓筆。筆記本平放在Amy面前、身體與杯碟之間可用桌面，橫線朝向Amy，尺寸符合手部比例；不移動杯碟糖罐。只呈現原裁切內可見局部，不拉遠展示整本，頁面文字留待後製，不生成假文字。E、S與具體筆記需要可讀時後製。焦點理解後安心滿意表情，George左下極小局部及咖啡師左側無頭局部維持圖2。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.24
結果：assets/images/shot_2.1.24_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：單指及提問表情成立；人物比例與頭頂留白需使用者評鑑。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.24<br>參考圖說明：<br>圖1 cam_george_mcu_45deg_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_george_mcu_45deg_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀替換藍色。<br>圖4 prop_coffee_set.png：咖啡道具外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>George斜側中近景65mm坐姿近眼高，原頭頂留白上半身桌面裁切。說『最後一個問題，妳會希望這間公司的管理方式是什麼樣子？』看畫外Amy略抬眉、專注親切嘴唇微張。胸前至肩高度之間輕豎一根食指，其餘自然收攏表示最後一題，手指不擋臉不朝鏡頭不訓誡。另一手放鬆身體原朝向。窗光綠牆畫作柔化杯碟糖罐原位。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.25
結果：未生成圖片；image generation failed: http 400 Bad Request: Some("{\n  \"error\": {\n    \"message\": \"Your request was rejected by the safety system. If you believe this is an error, contact us at help.openai.com and include the request ID 8ffa2446-a844-4000-8b8f-d387a060de16.\",\n    \"type\": \"image_generation_user_error\",\n    \"param\": null,\n    \"code\": \"moderation_blocked\",\n    \"moderation_details\": {\n      \"moderation_stage\": \"output\",\n      \"categories\": [\n        \"other\"\n      ]\n    }\n  }\n}")
目視：未產出圖片；輸出安全審查 moderation_blocked（other）。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png"]
完整送出prompt：<br>shot_2.1.25<br>參考圖說明：<br>圖1 cam_george_ots_amy_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_george_ots_amy_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀，替換藍色人物。<br>圖4 char_amy.jpeg：Amy外觀，替換紅色人物。<br>圖5 prop_coffee_cup.png：咖啡道具外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>越過Amy肩膀看George過肩中近景60mm，George左至中、Amy後腦肩右前景。George問『如果妳是投資大眾，會不會擔心決策不透明、或老闆自肥？』注視Amy，上半身小幅前傾眉心略收嘴唇微張，認真關切引導思考仍溫和，不怒不責備。雙手自然原低處不加指責手勢。前傾不變成靠近鏡頭大幅放大。焦點提問神情，不新增老闆金錢負面情境圖示。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.26
結果：assets/images/shot_2.1.26_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：抬手積極回答成立；前景及桌面遮擋改變。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg", "D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png"]
完整送出prompt：<br>shot_2.1.26<br>參考圖說明：<br>圖1 cam_amy_ots_george_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_ots_george_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀，替換藍色人物。<br>圖4 char_amy.jpeg：Amy外觀，替換紅色人物。<br>圖5 prop_coffee_set.png：咖啡道具外觀。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>越過George肩膀看Amy過肩中近景60mm，George後腦肩左前景遮擋、Amy右中景。Amy積極回應『如果可以許願，我希望誠實透明公司，賺錢正當，決策公平』。剛開始回答瞬間眼明亮眉稍抬、自信笑意嘴唇微張，一手自然抬到肩以下掌心斜向George，手指放鬆，興致勃勃提想法。手勢克制不過頭不宣誓、不同時數手指。另一手低處，肩軀幹沿圖2。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.27
結果：assets/images/shot_2.1.27_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：認真表情與既定身體方向成立；頭頂留白少，構圖接近第四參考。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg", "D:/kj-openMontage/projects/course-51-esg/assets/images/shot_2.1.4_short_v2.png"]
完整送出prompt：<br>shot_2.1.27<br>參考圖說明：<br>圖1 cam_amy_cu_emotion_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_amy_cu_emotion_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_amy.jpeg：Amy外觀替換紅色。<br>圖4 shot_2.1.4_short_v2.png：肩膀胸口頭頸朝向參考，非構圖表情參考。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>Amy頭肩特寫100mm坐姿近眼高，完整頭部肩膀部分上胸，手桌畫外。大小位置頭頂留白裁切依圖2；肩膀胸口頭頸朝向參考圖4自然連貫，不照搬圖4驚奇表情。Amy說『不能欺騙股東客戶，不要危害金融市場穩定』，看畫外左George，穩定認真眼神、眉略收、嘴唇自然說話。捕捉輕搖頭否定一瞬，頭只小幅轉動仍與George視線交流，堅定有原則，不怒目撇嘴瞪眼。焦點眼睛表情，咖啡機磨豆機木牆柔化，只有Amy一人。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

### shot_2.1.29
結果：assets/images/shot_2.1.29_gpt_v1.png；1672×941 RGB；解碼與複本SHA256一致
目視：筆記本筆及祝賀反應成立；Amy為手貼胸而非單指，桌面右側新增延伸板，咖啡師完整入鏡。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png", "D:/kj-openMontage/.tmp/shot_2.1.1_leads_board.png", "D:/kj-openMontage/.tmp/shot_2.1.1_background_board.png", "D:/kj-openMontage/.tmp/esg_notebook_props_board.png"]
完整送出prompt：<br>shot_2.1.29<br>參考圖說明：<br>圖1 cam_twoshot_ms_level_empty_gpt_v3.png：咖啡館場景外觀。<br>圖2 cam_twoshot_ms_level_block_blender.png：構圖與佔位編輯底圖。<br>圖3 shot_2.1.1_leads_board.png：角色外觀拼板：左George替換藍色，右Amy替換紅色。<br>圖4 shot_2.1.1_background_board.png：背景人物拼板：左上班族女性替換紫色，右咖啡師替換綠色。<br>圖5 esg_notebook_props_board.png：道具拼板：上咖啡杯碟糖罐、中prop_notebook.png筆記本、下prop_pen.png筆。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>坐姿近眼高雙人中景40mm。George左Amy右隔木桌對坐。George正說『恭喜妳Amy，妳已經把ESG核心精神全都自己說出來了』，看Amy溫暖肯定笑容，雙手身前低處自然攤開掌心略上。Amy眉輕抬、驚喜明亮雙眼、開心不可思議笑容，一手輕指自己胸口，另一手靠桌面筆記本。本張只指自己，不同時再指筆記本。筆記本與筆依圖5中下部：綠色布面封皮、米色橫線內頁的攤開筆記本，深灰筆身銀色配件的按壓筆。筆記本平放在Amy面前、身體與杯碟之間可用桌面，橫線朝向Amy，尺寸符合手部比例；不移動杯碟糖罐。只呈現原裁切內可見局部，不拉遠展示整本，頁面文字留待後製，不生成假文字。背景上班族女性咖啡師保持原活動不轉頭祝賀。氣氛溫暖自然生活化。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

## 2026-10-21 shot_2.5.1 GPT v1（待評鑑）

- 圖片：assets/images/shot_2.5.1_gpt_v1.png；1672×941 RGB PNG。
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；成功生成1次。原7張輸入因工具最多5張限制遭前置拒絕，未生成；使用者授權Python拼接後再提交。
- 配方：W2I，供後續I2V的首幀候選；未修改manifest或採用狀態。
- 拼圖：原尺寸上下拼接、不裁切，60px標題帶；主角上George／下Amy，背景上char_officelady／下char_barista，原圖保留。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png
  3. D:/kj-openMontage/.tmp/shot251_main_refs.png
  4. D:/kj-openMontage/.tmp/shot251_background_refs.png
  5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png
- 主角拼圖來源：clp/char_george.png、clp/char_amy.jpeg；背景拼圖來源：clp/char_officelady.png、clp/char_barista.png。
- 驗證：目視四角色／左右對坐／暖色場景保留；Amy較預定姿態前傾且雙手靠攏、點頭不明顯；George亦略前傾，咖啡師比blocks露出更多身體，人物比例與背景非精確對齊。完整解碼及來源複本SHA256核對通過。未重試。

完整 prompt：

```text
參考圖說明：
圖1 cam_twoshot_ms_level_empty_gpt_v3.png：場景外觀參考圖。
圖2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖3 shot251_main_refs.png：上半部為George人物參考，對應圖2左側藍色人物；下半部為Amy人物參考，對應圖2右側紅色人物。
圖4 shot251_background_refs.png：上半部為紫衣女客人物參考，對應圖2後方窗邊紫色人物；下半部為咖啡師人物參考，對應圖2右側吧台邊緣綠色人物。
圖5 prop_coffee_set.png：咖啡杯碟與糖罐的外觀參考圖。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。
杯碟與糖罐的外觀採用圖5，數量、位置及遮擋沿用圖2，不複製道具參考圖中的多視角展示物件。保留後方紫衣女客及綠圍裙咖啡師的原有位置與可見範圍，兩人維持背景角色，不看鏡頭、不參與主角對話。

畫面描述：
這是一張40mm、坐姿近眼高平視的雙人中景。George坐在畫面左側，Amy坐在右側，兩人隔桌相對；人物比例、桌面與手部可見範圍沿用圖2。
Amy看著George，下巴微收，停在輕輕點頭表示認同的瞬間，神情若有所思，嘴唇微啟。她的身體保持自然坐姿，尚未明顯前傾；雙手輕放桌面，呈現認同對方說法、準備接續提出疑問的狀態。George帶著溫和微笑專注看著Amy，肩膀放鬆，雙手自然停在桌邊。
採中景深，兩位主角與桌面清楚，背景人物不搶焦。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```


## 2026-10-21 supervisor_office 廣角空景 GPT，待評鑑
- 流程：kj-cinematic 場景素材局部重繪，依 skills/kj/blender-view-restyle.md；專案根目錄無 checkpoint 檔，本次不改採用。
- 工具／供應商：內建 image_gen／OpenAI，1 次；確切模型版本、預估及實際費用未知。
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_blender.png；2. clp/loc_supervisor_office_5.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png；PNG 1672×941 RGB。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/call_9fe04cff884e4efca1ff0491021c00df.png。
- 檢查：完整 PNG 解碼、來源與存檔 SHA256 相同；目視無人物，桌椅、公告板、窗框及文件／檯燈主要位置保留。暖木與藍皮革呈現，日光較強；窗外增加遠樓，右盆露出更多，植物輪廓改變、左前葉片更模糊。未宣稱幾何完全一致，未重試或更新 manifest。

完整實際 prompt：
```text
請編輯圖1，將這張Blender空景提升為精緻3D動畫電影場景背景，參考圖2的材質、色彩、光影與氣氛。圖1 cam_twoshot_wide_level_empty_blender.png 是唯一的取景、透視、物件配置與遮擋依據。圖2 loc_supervisor_office_5.png 僅供美術表現參考，不移植其構圖、家具排列、植物配置或人物。色彩與光影採用圖2明亮晴日、溫暖木色、灰白牆、柔和藍色皮革座椅、清透藍天城市、綠葉暖陽透光的精緻3D動畫美術。
【保留本機位】維持圖1的16:9畫幅、觀看方向、消失點、主要結構與遮擋。保留可見窗框、中央豎框、頂部百葉、窗台、左側被裁切公告板與牆上紙張、辦公桌、桌面文具文件、左右座椅及右側植物的位置、數量、尺度與主要輪廓。不旋轉相機、不鏡像、不拉遠或拉近，不移植圖2的右側櫃子、側窗、掛畫或其他畫外家具。不補出被裁切部分。前景左下的大葉片保留原本位置及裁切，不移植圖2整盆植物。
【材質與細節提升】沿用圖1構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。桌面及桌體呈現圖2暖橡木紋理；左右原有座椅套用圖2柔和藍色細紋皮革與金屬扶手，維持圖1椅背大小位置及裁切。左公告板為木框軟木板，既有紙張增加自然紙纖維、細小不可辨讀的辦公筆記線條，保留原位置數量，不新增紙張。白色檯燈保留圖1燈罩朝向、位置與尺度，呈現陶瓷烤漆與金屬桿，不過曝。桌面文件堆保留高度及位置，細化紙張邊緣及陰影；既有桌墊、筆記本、紙張與文具保留。窗外依圖1既有樓群位置與高低輪廓細化立面窗格、遠景空氣透視，將簡化雲片細化為自然白雲，不能改成圖2的城市構圖。右側已有植物保留主要枝幹、位置及體積，在原輪廓內細化葉片形態、葉脈與透光，修復簡化多邊形葉片，不增加盆栽。表面乾淨乾燥、合理霧面和局部反光，不加髒污、過度鏡面或塑膠感。依本鏡窗向呈現自然暖日光與柔和陰影，不直接照搬圖2畫面上的光斑；不額外強化散景，近中景細節清晰。
【本鏡畫面】本鏡是靠近桌面的平視廣角空景，木桌從畫面左下延伸至中間偏右，文件堆與白檯燈位於桌面後端、中央偏左；左側大椅背被畫面左緣裁切，右側訪客椅背及金屬扶手被右緣與下緣裁切。後方大窗佔據畫面中央及右上大部分，中央窗框約在畫寬六成三處；左上公告板只露局部。右側高大綠植延伸出右邊界，前景左下葉片遮住一小部分桌面。保持這些幾何關係，不把圖2的較遠全室視角取代圖1。
【空景與輸出】零人物，不得出現人體、手臂、肩膀、人物倒影或人形剪影。只輸出一張16:9高解析度完整圖片，不拼貼、不加字幕、標誌或水印。
```

## 2026-10-21 shot_2.1.14 使用者授權原prompt重試
內建image_gen／OpenAI，1次；模型費用未知。HTTP400 moderation_blocked，output階段，分類other；request ID 3190d982-0eda-4f13-beed-eeb79083ed0b。未產出圖片，未採用，未再重試。
有序參考：["D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png", "D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png", "D:/kj-openMontage/projects/course-51-esg/clp/char_george.png"]
完整prompt：<br>shot_2.1.14<br>參考圖說明：<br>圖1 cam_george_cu_emotion_empty_gpt.png：咖啡館場景外觀。<br>圖2 cam_george_cu_emotion_block_blender.png：構圖與佔位編輯底圖。<br>圖3 char_george.png：George外觀替換藍色。<br>生圖指引：以圖2為編輯底圖，保留其取景、透視、空間配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、頭部位置及畫面下緣裁切，不推近鏡頭或放大人物。定位人物替換為指定角色，五官髮型服裝與自身頭身比例依角色參考，不採展示姿態或排版。場景材質色彩光影依圖1，保留日間暖陽與精緻3D動畫質感；家具設備裝飾的位置數量依圖2，不新增垂藤。直接坐入既有椅子，不增加椅子。只依本鏡描述調整表情視線與必要局部手勢，其餘保持底圖。被人物遮擋的物件保持遮擋。道具參考僅供外觀，不複製多視圖或增加數量；糖罐為白色罐身、實心木蓋與中央木鈕，不是打孔調味罐。只呈現同一個瞬間，不畫多組手臂、殘影或分格。<br><br>畫面描述：<br>George頭肩特寫100mm坐姿近眼高，完整頭部肩膀部分上胸，手桌畫外。George正溫和說『很好，妳剛才所說的幾點……』，注視畫外Amy、嘴角微揚、眼角柔和笑意、眉放鬆、嘴唇自然微張。捕捉輕點頭肯定，下巴僅略低，成熟親切導師神情不誇張大笑。焦點雙眼眼鏡表情，綠牆窗光畫作柔化，只有George一人。<br>輸出一張16:9彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或參考圖排版。

## 2026-10-21 shot_2.5.2 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.5.2_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：Amy雙手胸前展開起勢已呈現；咖啡師被放大至左側前景、可見範圍過多，Amy視線偏左上，頭部較底圖大。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png

完整 prompt：

```text
參考圖說明：
圖1 cam_amy_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_amy.jpeg：Amy人物參考圖，對應圖2紅色人物。
圖4 char_barista.png：咖啡師人物參考圖，對應圖2最左邊緣局部綠色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張50mm、近眼高微側拍攝的Amy中特寫。Amy的頭部與上半身位置沿用圖2，不加入George前景；左邊緣的咖啡師只保留底圖既有的局部可見範圍。
Amy看向畫外左側的George，眉毛微揚、眼睛略微睜大，帶著好奇又半信半疑的表情。她的雙手剛抬到胸前下方，掌心相對、手指自然彎曲，兩手之間保留適度距離，呈現即將向兩側展開、比出「很大」的起始姿態。雙手位於原有畫框內，不為容納手勢改成更遠的景別。
淺景深聚焦Amy的臉與手。畫面不出現鯨魚、品牌標誌或想像圖案。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.5.3 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.5.3_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：Amy歪頭／單眉與俏皮笑意可見，手在畫外；視線偏左上、頭部較底圖大，聳肩細微。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

完整 prompt：

```text
參考圖說明：
圖1 cam_amy_cu_emotion_empty_gpt.png：場景外觀參考圖。
圖2 cam_amy_cu_emotion_block_blender.png：構圖底圖。
圖3 char_amy.jpeg：Amy人物參考圖，對應圖2紅色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張85mm、近眼高平視的Amy臉部特寫，頭肩裁切與人物大小沿用圖2，畫面只有Amy一位人物。
Amy看向畫外的George，頭部輕微偏斜，一側眉毛略抬，嘴角帶著不太確定的俏皮笑意；肩膀微微提起，呈現準備聳肩反問的起始狀態。表情混合困惑與一絲僥倖，不做驚恐表情。手部維持畫外，不補入手勢。
淺景深聚焦眼神與嘴角，背景柔和虛化。畫面不出現蝦米、噴嚏特效或地震效果。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.5.4 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.5.4_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：George右手食指抬起、Amy右側過肩保留；George與桌面較底圖放大，糖罐蓋仍為孔洞樣式。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

完整 prompt：

```text
參考圖說明：
圖1 cam_george_ots_amy_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2藍色人物。
圖4 char_amy.jpeg：Amy人物參考圖，對應圖2右前景紅色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張60mm、近眼高平視的過肩鏡頭，從Amy肩後拍向George。George位於左中景，Amy的後腦與肩膀位於右前景，大小與遮擋沿用圖2。
George看著Amy，表情溫和卻篤定，嘴角略帶安定人心的笑意。他的右手抬至胸前下方，食指自然豎起，其餘手指放鬆彎曲，停在即將輕輕搖動食指提醒對方的起始姿態；左手仍自然靠近桌面。此刻雙手尚未交扣。Amy維持面向George的聆聽坐姿，只呈現底圖可見的後腦與肩部。
淺景深聚焦George的臉與抬起的手，Amy前景柔和失焦。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.7.1 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.1_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：Amy雙手靠攏、George左側過肩保留；Amy較底圖放大且表情略帶笑意，視線略高。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整 prompt：

```text
參考圖說明：
圖1 cam_amy_ots_george_empty_gpt.png：場景外觀參考圖。
圖2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖3 char_amy.jpeg：Amy人物參考圖，對應圖2紅色人物。
圖4 char_george.png：George人物參考圖，對應圖2左前景藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張60mm、近眼高平視的過肩鏡頭，從George肩後拍向Amy。George後腦與肩膀位於左前景，Amy位於右中景，裁切與遮擋沿用圖2。
Amy看著George，收起先前玩笑的神情，眉眼舒展但態度認真，嘴唇微啟，呈現剛理解事情本質的表情。她的雙手在身前、靠近桌面的位置輕輕靠攏，手指自然接近，不做祈禱姿勢；上半身微微朝對話方向傾斜。George保持朝向Amy的聆聽姿態，頭部微收，呈現準備點頭肯定的狀態。
淺景深聚焦Amy，George前景柔和失焦。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.1.14 GPT v1，新 prompt，待評鑑
- 使用者授權：使用本輪確認的完整 prompt 在 GPT 生成一張，存入 assets/images。
- 圖片：assets/images/shot_2.1.14_gpt_v1.png（1672×941 RGB PNG）。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知。W2I 首幀，生成1次成功，未重試。
- 有序參考圖：references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png；references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png；clp/char_george.png。
- 驗證：完整 PNG 解碼及來源／複本 SHA256 一致。目視為 George 單人頭肩、暖窗光、微笑微張嘴，無文字；相較 blocks 頭頂留白減少、頭部較大且側傾，未完全遵守端正頭部與構圖要求，待使用者評鑑。未更新 manifest／checkpoint／採用設定。

完整 prompt：
```text
shot_2.1.14

參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：咖啡館場景外觀參考圖。
圖 2 cam_george_cu_emotion_block_blender.png：構圖底圖，提供人物位置、朝向、取景與遮擋關係。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、空間配置、人物佔位與可見範圍。維持頭頂留白、頭部在畫面中的位置、肩膀範圍及畫面下緣裁切，不推近鏡頭或放大人物。

將藍色定位人物替換為圖 3 的 George，五官、灰白髮型、棕框眼鏡、短鬍鬚、服裝與自然頭身比例均依人物參考圖。只呈現底圖可見的身體部位，不採用人物參考圖的展示姿態、多視圖或排版。

場景材質、色彩、風格與光影採用圖 1，保留日間溫暖窗光與精緻 3D 動畫質感。窗框、綠色牆柱、植物掛畫及可見椅背的位置與遮擋依圖 2。

畫面描述：
這是一張坐姿近眼高、100mm 長焦視角的單人頭肩特寫。George 位於畫面中央附近，完整頭部、雙肩及部分上胸入鏡，手部與桌面在畫外。臉部朝向沿用圖 2，視線自然落在畫外對坐的 Amy，不看鏡頭。

George 正要溫和回應「很好。妳剛才所說的幾點」。捕捉他露出讚許微笑、準備輕點頭的起始瞬間：頭部自然端正，眉間放鬆，眼神柔和，嘴角輕輕上揚，嘴唇微張。表情成熟、親切而克制，帶有導師肯定對方的感受，不誇張大笑。

焦點落在 George 的雙眼與臉部表情，眼鏡不遮蔽眼神；背景的窗景、綠牆與植物掛畫柔和虛化。畫面只出現 George 一人，不加入 Amy 或其他人物。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或分格。
```


## 2026-10-21 supervisor_office 其餘10機位重繪，待評鑑
使用者確認 cam_twoshot_wide_level_empty_gpt.png 作為本批唯一共用美術參考；依 blender-view-restyle.md，內建 image_gen／OpenAI，各生成一次，共10次。確切模型、預估／實際費用未知。廣角原圖與既有過肩GPT保留；未修改 Blender、manifest 或 scene_plan。

### amy_cu_emotion
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-72fed42f-3423-4ab4-ac21-e2a9ada0b263.png
- 目視：無人物，緊裁切保留；百葉厚度與間距略變、光線更暖。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：緊裁切側窗背景，橫向百葉佔上半部，左邊裁切綠植，下左兩個紫色資料夾，下右文件托盤，椅背只有下緣可見。保留大面積灰藍窗面，不新增城市或桌面。
```

### amy_mcu_15deg
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_amy_mcu_15deg_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_amy_mcu_15deg_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-8b7926bb-0e73-4888-9211-772d43b76805.png
- 目視：無人物，原主要佔位保留；收納檯面變木色、椅背新增金屬側邊、葉影較強。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：側窗中近景，左側綠植約佔四分之一，百葉在上方，兩個紫色資料夾位於左下後方，右側雙層文件盤；藍椅背佔下半中央偏右並被下緣截斷。維持側窗與收納櫃幾何。
```

### amy_ms_15deg
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-d117bc41-a9f9-45ae-9464-198746d0b761.png
- 目視：無人物，主要佔位保留；收納檯面變木色、椅背皮紋粗、左下露出盆緣。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：側窗中景，綠植佔左三分之一，百葉橫跨上方，後方收納櫃可見開放格及盒子，兩個紫色資料夾與右方雙層文件盤原位保留；中央偏右藍椅背及底部少量扶手保持尺度。
```

### amy_ots_supervisor
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-f767bd42-8ed0-4209-a4a4-19154ea00835.png
- 目視：無人物，檯燈／文件／植物／椅位置保留；窗外新增樓群及綠地，葉形和扶手細節改變。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：斜向側窗空過肩構圖，近景桌面與文件堆位於下方，左側大白檯燈朝右下，中央偏左綠植、右側完整椅背與扶手，後方百葉及開放格收納櫃。左窗只細化已有樓形，不移植廣角主窗。
```

### supervisor_cu_emotion
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_supervisor_cu_emotion_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_supervisor_cu_emotion_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-69a06d49-36f4-442f-8b60-64c3abce8b98.png
- 目視：無人物，紙張位置及緊裁切大致保留；軟木與皮革紋理粗，增加斜向日光。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：公告板緊特寫空景，藍椅背從底部伸入，軟木板及原位紙張佔大部分畫面，右側一條白牆及紙張。保持紙張大小數量，沒有窗、桌、植物，勿補出。
```

### supervisor_mcu_15deg
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_supervisor_mcu_15deg_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_supervisor_mcu_15deg_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-bfd80129-cced-4d77-a93d-1aeb63888dd2.png
- 目視：無人物，公告板／椅背位置保留；紙張有微幅形變，日光較強。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：公告板中近景空景，椅背在下半中央偏左，公告板右緣約畫寬四分之三，右側白牆和紙張。保留公告板下框，沒有窗景桌面植物，不新增。
```

### supervisor_ms_15deg
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_supervisor_ms_15deg_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_supervisor_ms_15deg_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-0563a9df-f163-4886-af35-1e7e8765e9a8.png
- 目視：無人物，主要構圖保留；椅背邊框及皮紋改變，右牆新增葉影。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：公告板中景空景，藍椅在中央偏左，木框公告板滿佈原位紙張，右側白牆紙張，下右角只有少量文件堆及桌緣。維持各紙張分布與裁切，無窗不補窗。
```

### supervisor_ots_amy
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_empty_gpt_v2.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-78990912-efce-4b68-a6ed-5fbd1bdaf839.png
- 目視：無人物，主要構圖保留；右上新增原底圖未見百葉，窗外樓群增加，燈罩角度略變。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：面向公告板的空過肩構圖，左中藍椅背，左後公告板原位紙張，右邊局部主窗與檯燈，近景桌面上右側文件堆、下方桌墊兩組文件與小筆記本。保留檯燈朝左下及其底座位置，不加人物肩膀。
```

### table_insert_iso
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_table_insert_iso_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_table_insert_iso_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-0f434e50-2806-4a86-ad56-6a8af3cc5f59.png
- 目視：無人物，俯斜桌面構圖及三條灰標保留；桌墊新增縫線，木紋較粗。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：桌面俯斜特寫，暖木桌、灰色桌墊，右上厚文件堆、下方兩組文件、右側藍筆與灰藍筆記本；白檯燈只有右上底座和被上緣截斷的支桿，左邊極少椅背扶手。不要補燈罩、窗景、植物或整張桌子。保留文件上原有三條灰色標記的形狀與位置。
```

### twoshot_ms_level
- 有序輸入：1. references/scenes/supervisor_office/cameras/cam_twoshot_ms_level_empty_blender.png；2. references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png。
- 輸出：references/scenes/supervisor_office/cameras/cam_twoshot_ms_level_empty_gpt.png；PNG 1672×941 RGB；完整解碼及來源複本SHA256一致。
- 原生來源：C:/Users/servi/.codex/generated_images/01a15a44-f4b2-71f2-aa1a-f90fdbfc00af/exec-66884282-15e5-4abc-9638-cfd610b73e95.png
- 目視：無人物，主窗及桌椅關係保留；上緣新增百葉，左緣新增公告板可見部分，植物／盆露出及前葉輪廓變化。
- 完整實際prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切及物件配置。圖2 cam_twoshot_wide_level_empty_gpt.png 是已確認的共用美術參考，只提供材質、色彩、光影與氣氛；不要採用圖2的拍攝角度、消失點、排列或可見範圍，不要重新生成圖2。
保留圖1所有可見家具、窗框、百葉窗、公告板紙張、設備、植物的位置、數量、尺度和主要輪廓及遮擋。不旋轉、不鏡像、不推拉相機，不補出裁切物件，不移植圖2畫外物件。材質匹配圖2暖橡木、柔和藍色細紋皮革及金屬扶手、灰白牆、木框軟木板、自然紙張和綠葉；保留圖1原有紫色資料夾和灰色收納件。改善微紋理、接縫、倒角高光、接觸陰影和反射，不改造型或增加配件。植物只在原體積內細化葉脈、薄葉和透光，不增加植物。百葉維持原來覆蓋範圍，不打開或移除；不可見城市的機位不能自行添加城市或窗景。紙張保留數量位置，允許細小不可辨讀辦公筆記，不加醒目文字。乾淨乾燥的合理霧面，勿過度塑膠或鏡面反光。匹配圖2暖日光與自然冷暖關係，依圖1朝向合理投影，不逐張增加飽和、泛光或暖色，不直接照搬參考圖光斑。不強化景深散景，保留近中景細節。
零人物，無主角、人體、手臂、肩膀、人物倒影或人形剪影，即使名稱含過肩也只做空景。輸出一張16:9高解析度完整圖，不拼貼、不加字幕、標誌或水印。
本鏡畫面：平視雙人中景空景，桌面從底部伸向中央，文件堆與白燈在中間偏左，主窗豎框約畫寬57%，兩椅各由左右緣裁切，右側植物，下方中央大葉片遮擋桌面。保留比參考圖更緊的構圖；細化既有樓群而不改樓群位置。
```

## 2026-10-21 shot_2.7.4 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.4_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：Amy微張嘴與凝重表情可見，手維持低位；頭部較底圖大，左邊緣咖啡師未保留。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png

完整 prompt：

```text
參考圖說明：
圖1 cam_amy_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_amy.jpeg：Amy人物參考圖，對應圖2紅色人物。
圖4 char_barista.png：咖啡師人物參考圖，對應圖2最左邊緣局部綠色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張50mm、近眼高微側拍攝的Amy中特寫，人物大小與裁切沿用圖2，不補入George前景；咖啡師僅保留底圖左邊緣既有的局部。
Amy看向畫外左側的George，雙眼略微睜大、嘴唇小幅張開，停在輕輕倒抽一口氣的瞬間。眉間帶著凝重，肩膀略有緊繃，呈現剛感受到競爭壓力、即將點頭認同的狀態。雙手自然放低，身體尚未明顯前傾，保留後續轉為詢問政府輔導措施的表演空間。
淺景深聚焦Amy的眼神與表情，不做誇張驚嚇。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.7.5 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.5_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：四角色、George攤手、Amy持筆與筆記本呈現；筆尖已近似接觸頁面、筆記本偏大，咖啡師可見範圍增加，人物與桌面未精確對齊blocks。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_ms_level_block_blender.png
  3. D:/kj-openMontage/.tmp/shot251_main_refs.png
  4. D:/kj-openMontage/.tmp/shot251_background_refs.png
  5. D:/kj-openMontage/.tmp/esg_coffee_notebook_pen_refs.png

完整 prompt：

```text
參考圖說明：
圖1 cam_twoshot_ms_level_empty_gpt_v3.png：場景外觀參考圖。
圖2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖3 shot251_main_refs.png：上半部George對應圖2藍色人物，下半部Amy對應圖2紅色人物。
圖4 shot251_background_refs.png：上半部紫衣女客對應圖2後方紫色人物，下半部咖啡師對應圖2綠色人物。
圖5 esg_coffee_notebook_pen_refs.png：由上到下為咖啡杯碟與糖罐、筆記本、筆的外觀參考圖。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。
杯碟與糖罐的外觀採用圖5上方，數量、位置及遮擋沿用圖2，不複製道具參考圖中的多視角展示物件。保留後方紫衣女客及綠圍裙咖啡師的原有位置與可見範圍，兩人維持背景角色，不看鏡頭、不參與主角對話。
筆記本外觀採用圖5中間，筆的外觀採用圖5下方。在Amy面前、靠近她的桌沿放置一本攤開的筆記本，避開既有杯碟；筆由Amy右手持握。只新增這兩件指定道具，保留其餘桌面物件的位置。

畫面描述：
這是一張40mm、近眼高平視的雙人中景，George在左、Amy在右，桌面與雙方手部可見，構圖沿用圖2。
George看著Amy，露出讓人安心的微笑，右手在身前低處微微抬起，掌心朝上，停在準備自然攤手說明的起始姿態。Amy專注看著George，表情稍微放鬆；右手自然握住圖5下方的筆，筆尖停在圖5中間攤開筆記本的頁面上方，尚未開始書寫，左手輕扶頁面邊緣。
筆記本放在Amy面前靠近桌沿的位置，不壓住杯碟或糖罐，頁面保留淡色橫線，不生成可讀文字。採中景深，主角與記錄動作清楚，背景人物不搶焦。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.1.25 GPT v1，新 prompt，待評鑑
- 使用者授權：使用本輪確認的完整 prompt 在 GPT 生成一張，存入 assets/images。
- 圖片：assets/images/shot_2.1.25_gpt_v1.png（1672×941 RGB PNG）。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知。W2I 首幀，生成1次成功，未重試。
- 有序參考圖：references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png；references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png；clp/char_george.png；clp/char_amy.jpeg；clp/prop_coffee_cup.png。
- 驗證：完整PNG解碼及來源／複本SHA256一致。目視 George 認真微張嘴、前傾，Amy 背面過肩與一組杯碟成立；George 頭部較底圖大、留白減少、手臂姿態改變，右下新增可見椅背，待評鑑。未修改manifest／checkpoint／採用。

完整 prompt：
```text
shot_2.1.25

參考圖說明：
圖 1 cam_george_ots_amy_empty_gpt.png：咖啡館場景外觀參考圖。
圖 2 cam_george_ots_amy_block_blender.png：構圖底圖，提供人物位置、朝向、取景與遮擋關係。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色定位人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右前景的紅色定位人物。
圖 5 prop_coffee_cup.png：白色陶瓷咖啡杯與杯碟的外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、空間配置、人物佔位、可見範圍與遮擋關係。維持兩人的前後距離、畫面佔比、頭頂留白及下緣裁切，不推近鏡頭或放大 George。

將藍色定位人物替換為圖 3 的 George，紅色定位人物替換為圖 4 的 Amy。人物五官、髮型、服裝與自然頭身比例依各自參考圖，不採用參考圖的展示姿態、多視圖或排版。Amy 保持背向鏡頭的過肩角度，只呈現底圖可見的後腦、肩背與局部手臂，不轉頭露出正臉。

場景的材質、色彩、風格與光影採用圖 1，保留日間溫暖窗光與精緻 3D 動畫質感；窗框、綠色牆柱、植物掛畫、桌椅的位置依圖 2。人物坐在既有座位，不增加椅子。

George 面前可見的咖啡杯與杯碟採用圖 5 的外觀，位置、大小及杯耳方向依圖 2。圖 5 的多視角只用於辨識同一件道具，不增加杯碟數量。被 Amy 遮擋的桌面與物件維持遮擋，不為展示道具而移開人物。

畫面描述：
這是一張越過 Amy 肩膀看向 George 的過肩中景，60mm 長焦視角，坐姿近眼高、略微俯視。George 位於畫面左側至中央，完整頭部與上半身可見；Amy 的後腦與肩背佔據右前景，沿用圖 2 的遮擋範圍。桌面下方可見 George 面前的一組白色咖啡杯碟。

捕捉 George 開始提問的瞬間。他上半身輕微前傾，臉與視線朝向對坐的 Amy，嘴唇自然微張，眉心輕收，神情認真、關切而溫和，帶著邀請對方思考的意味。他正在問：「如果你是投資大眾，妳會不會擔心它的決策不透明、或是老闆自肥？」這句話只作為表演語境，不出現在畫面上。

前傾幅度小，保留 George 原有座位與人物大小；手臂及可見手部沿用圖 2 的自然低位，不額外抬手或指向 Amy。Amy 維持面向 George 的聆聽姿態。

以淺景深聚焦 George 的雙眼與提問神情，眼鏡不遮蔽眼神；右前景 Amy 與窗外背景柔和虛化，仍可辨識髮型與服裝。畫面只有 George 和 Amy 兩人。除上述 George 的輕微前傾、表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、圖解、角色標籤、浮水印或分格。
```

## 2026-10-21 shot_2.8.1 GPT v1（待評鑑）

- 圖片：`assets/images/shot_2.8.1_gpt_v1.png`
- 工具：內建 image_gen；供應商 OpenAI；確切模型／費用未知；生成一次。
- 驗證：1672×941 RGB PNG，完整解碼、來源與交付複本 SHA256 一致。
- 目視：主管左／Amy右、閱讀報告與微笑聆聽成立；報告一頁抬起、下緣接觸桌面，兩人頭部較 blocks 大且頭頂留白較少，構圖非完全一致。未重試、未改採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_twoshot_wide_level_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_supervisor.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

完整 prompt：
```text
參考圖說明：
圖 1 cam_twoshot_wide_level_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_twoshot_wide_level_block_blender.png：雙人構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將兩個定位人物替換為對應角色，畫面中只有主管與 Amy 兩人。只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用圖 3、圖 4，不採用人物參考圖的展示姿態、表情或構圖，不保留 blocks 的方塊造型。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留胡桃木桌面、藍灰色座椅、軟木公佈欄、白色檯燈、文件堆、窗外城市與盆栽的外觀，維持明亮日間的辦公室氛圍。

畫面描述：
這是一張 35mm、眼高平視、從辦公桌側面拍攝的雙人廣角畫面。主管坐在畫面左側的高背椅上，Amy 坐在畫面右側的訪客扶手椅上，兩人隔桌相向。沿用圖 2 的人物大小與頭頂留白，保留桌面對主管下半身的遮擋，以及 Amy 下身在畫面下緣的裁切；左下前景保留植物葉片。

主管面前的桌面上攤開一份 ESG 分析報告，雙手輕扶報告兩側，紙張下緣仍接觸桌面。他的頭部微微低垂，視線落在報告上，眉頭舒展，嘴角浮現滿意而肯定的微笑，呈現讀完重點、準備點頭稱讚的瞬間。保留圖 3 的五官、髮型與服裝，但將其憂愁神情改為欣慰與認可。

Amy 保持面向主管的坐姿，肩膀自然放鬆，帶著謙遜、安心的微笑看著主管，安靜聆聽，雙手自然安放於身前。兩人不看鏡頭。人物與辦公室背景清晰可辨，維持深景深。

依上述表演調整主管的頭部、視線及雙手，並調整 Amy 的表情與手部姿態；其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```



## 2026-10-21 shot_2.7.7 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.7_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：Amy皺眉、微張嘴、手在畫外已呈現；頭部較blocks大，眼神略偏上方。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_cu_emotion_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

完整 prompt：

```text
參考圖說明：
圖1 cam_amy_cu_emotion_empty_gpt.png：場景外觀參考圖。
圖2 cam_amy_cu_emotion_block_blender.png：構圖底圖。
圖3 char_amy.jpeg：Amy人物參考圖，對應圖2紅色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張85mm、近眼高平視的Amy臉部特寫，頭肩大小與裁切沿用圖2，畫面只有Amy一位人物。
Amy看向畫外的George，眉頭微蹙，眉心形成輕微皺褶，眼睛略微睜大，嘴唇微啟，呈現聽見法規逐年加強後、帶著壓力準備追問的瞬間。下巴略收，神情緊張而好奇，不呈現驚恐或哭泣。手部維持畫外。
淺景深聚焦眼睛與眉間，背景柔和虛化。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.7.10 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.10_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：Amy雙手接近太陽穴、苦笑姿態已呈現，未加金箍；咖啡師在左側被放大，可見範圍過多，Amy視線偏左上。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_mcu_45deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_barista.png

完整 prompt：

```text
參考圖說明：
圖1 cam_amy_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_amy.jpeg：Amy人物參考圖，對應圖2紅色人物。
圖4 char_barista.png：咖啡師人物參考圖，對應圖2最左邊緣局部綠色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張50mm、近眼高微側拍攝的Amy中特寫，頭部與上半身大小沿用圖2，不加入George前景；咖啡師僅保留左邊緣既有局部。
Amy看向畫外左側的George，眉毛微抬，嘴角帶著無奈又好笑的苦笑。雙手已抬至臉部兩側，手指自然張開，指尖接近但尚未壓住太陽穴，停在準備用雙手抱住頭側、模仿越勒越緊的起始姿態。手掌不遮住眼睛，手肘自然彎曲，維持原有取景。
淺景深聚焦Amy的表情與雙手，表演逗趣但不痛苦。頭上不出現實體金箍、頭帶或魔法特效。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.7.11 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.11_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：George笑容及Amy右前景過肩保留；George較底圖放大，視線接近鏡頭方向，頷首幅度細微。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

完整 prompt：

```text
參考圖說明：
圖1 cam_george_ots_amy_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2藍色人物。
圖4 char_amy.jpeg：Amy人物參考圖，對應圖2右前景紅色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張60mm、近眼高平視的Amy過肩鏡頭，George位於左中景，Amy後腦與肩膀位於右前景，構圖沿用圖2。
George看著Amy，眼角帶著自然笑意，嘴角上揚、嘴唇微開，呈現被她的比喻逗笑、即將輕輕點頭回應的瞬間。頭部略微下收，肩膀放鬆，雙手仍自然靠近桌面，尚未展開後續解說的攤手動作。Amy維持朝向George的聆聽姿態。
淺景深聚焦George溫和的笑容，Amy前景柔和失焦。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.7.12 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.12_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：Amy偏頭提問、雙手低置與George左側過肩保留；Amy略放大、視線略偏高，雙手靠攏放桌面。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_amy_ots_george_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整 prompt：

```text
參考圖說明：
圖1 cam_amy_ots_george_empty_gpt.png：場景外觀參考圖。
圖2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖3 char_amy.jpeg：Amy人物參考圖，對應圖2紅色人物。
圖4 char_george.png：George人物參考圖，對應圖2左前景藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張60mm、近眼高平視的George過肩鏡頭，George後腦與肩膀位於左前景，Amy位於右中景，構圖沿用圖2。
Amy看著George，頭部輕微偏斜，眉毛微揚，嘴唇微啟，呈現準備詢問未上市櫃中小企業處境的神情。她的雙手自然靠近桌面，右手尚未抬起或彈指；此刻仍在提問，不提前呈現已找到答案的得意笑容。George保持朝向Amy的專注聆聽姿態。
淺景深聚焦Amy的臉，George前景柔和失焦。不加入燈泡或其他頓悟圖示。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.7.13 GPT v1（待評鑑）

- 輸出：assets/images/shot_2.7.13_gpt_v1.png；[1672, 941] RGB PNG；完整解碼及來源複本SHA256通過。
- 工具／供應商：內建 image_gen／OpenAI；模型及費用未知。W2I首幀，各生成1次，未重試、未更改採用。
- 目視：四角色、雙人全景與Amy低頭持筆記錄已呈現；主角比blocks大，咖啡師移至右側咖啡機前且全身可見，未保留原吧台遮擋位置。
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_twoshot_wide_level_block_blender.png
  3. D:/kj-openMontage/.tmp/shot251_main_refs.png
  4. D:/kj-openMontage/.tmp/shot251_background_refs.png
  5. D:/kj-openMontage/.tmp/esg_coffee_notebook_pen_refs.png

完整 prompt：

```text
參考圖說明：
圖1 cam_twoshot_wide_level_empty_gpt.png：場景外觀參考圖。
圖2 cam_twoshot_wide_level_block_blender.png：構圖底圖。
圖3 shot251_main_refs.png：上半部George對應圖2藍色人物，下半部Amy對應圖2紅色人物。
圖4 shot251_background_refs.png：上半部紫衣女客對應圖2後方紫色人物，下半部咖啡師對應圖2綠色人物。
圖5 esg_coffee_notebook_pen_refs.png：由上到下為咖啡杯碟與糖罐、筆記本、筆的外觀參考圖。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。
杯碟與糖罐的外觀採用圖5上方，數量、位置及遮擋沿用圖2，不複製道具參考圖中的多視角展示物件。保留後方紫衣女客及綠圍裙咖啡師的原有位置與可見範圍，兩人維持背景角色，不看鏡頭、不參與主角對話。
筆記本外觀採用圖5中間，筆的外觀採用圖5下方。在Amy面前、靠近她的桌沿放置一本攤開的筆記本，避開既有杯碟；筆由Amy右手持握。只新增這兩件指定道具，保留其餘桌面物件的位置。

畫面描述：
這是一張28mm、平視的咖啡館雙人全景，George在左、Amy在右對坐，兩人的全身可見範圍、桌椅比例與空間留白沿用圖2，不放大主角或拉近鏡頭。
George面向Amy，下巴微收、神情篤定而鼓勵，嘴唇微啟，呈現準備點頭說出最後結論的狀態，雙手自然靠近桌面。Amy坐姿專注，視線落在面前攤開的筆記本，右手握筆、筆尖剛接觸頁面，左手輕扶本子，停在準備記下總結的瞬間。
筆記本與筆分別採用圖5中間與下方的道具參考，置於Amy面前，不移動原有杯碟與糖罐；頁面不生成可讀文字。保留窗邊紫衣女客與吧台綠圍裙咖啡師，兩人維持背景活動位置。採深景深保留咖啡館空間的清楚層次，暖陽方向依圖1。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

## 2026-10-21 shot_3.7.1 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.1_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未提供；一次生成，未重試。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/call_d3d20ab4234b49c699147b5b59ce7eec.png
- 驗證：Pillow 完整解碼，1672×941 RGB PNG；來源與存檔 SHA256 相同。
- 目視：主管欣喜低頭看攤開報告、Amy 微笑聆聽成立；無百葉窗與額外公告板。人物頭部較底圖大、頭頂留白減少；主管前傾，Amy 雙手改為桌面交握，未保留底圖手位。待使用者評鑑，未修改採用設定。
- 有序參考圖（相對專案根目錄）：
  1. references/scenes/supervisor_office/cameras/cam_twoshot_ms_level_empty_gpt.png
  2. references/scenes/supervisor_office/cameras/cam_twoshot_ms_level_block_blender.png
  3. clp/char_supervisor.jpeg
  4. clp/char_amy.jpeg
  5. clp/prop_proposal_document.png

完整 prompt：
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：雙人中景構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側紅色人物。
圖 5 prop_proposal_document.png：計畫書裝訂與材質參考圖；本鏡呈現攤開內頁，不呈現參考圖的封面標題。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。

將左側藍色定位人物替換為圖 3 的主管，右側紅色定位人物替換為圖 4 的 Amy。畫面只有這兩位人物，只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用圖 3、圖 4，不採用人物參考圖的展示姿態與表情。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留桌面文件、檯燈、窗外城市與右側綠植的配置；不加入圖 2 沒有的百葉窗或額外公告板。

計畫書的裝訂與紙張材質採用圖 5，只呈現一本攤開的計畫書，不複製道具展示圖中的多視角排列，不露出「增資計畫書」封面。

畫面描述：
這是一張眼高平視、45mm 視角的雙人對坐中景。主管位於畫面左側，Amy 位於右側，兩人隔著辦公桌相對而坐；雙方頭部、上半身與手部入鏡，下半身依底圖裁切，桌面延伸至畫面下緣。

主管低頭看著自己面前攤開的 ESG 五步驟推動計畫書，雙手輕扶左右頁緣，書本仍由桌面承托。眉眼舒展、嘴角揚起，呈現滿面春風、十分肯定計畫內容，正準備開口稱讚的瞬間。配合閱讀動作調整主管的頭部、前臂與手部，保持原有座位與軀幹位置。

Amy 保持右側坐姿，朝向主管，視線落在主管臉上，露出欣喜而謙遜的自然微笑，安靜聆聽；雙手沿用底圖位置自然放鬆。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 同批4鏡生成遭拒（未產出圖片）

工具／供應商：內建 image_gen／OpenAI；每鏡提交1次，HTTP400，code=moderation_blocked、moderation_stage=output、categories=[other]。工具未提供更具體原因，模型及費用未知。未重試、未改寫規避或更換供應商。
原始訊息：Your request was rejected by the safety system. If you believe this is an error, contact us at help.openai.com and include the request ID.

### shot_2.5.9

- HTTP400 moderation_blocked, output, category other；request ID：7ff86fc5-3895-4ffc-85ae-19e387bf376b
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

提交 prompt：

```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張50mm、近眼高微側拍攝的George中特寫，上半身位置與裁切沿用圖2，畫面只有George一位人物。
George看向畫外右側的Amy，眉頭輕收，眼神認真，嘴唇微啟，保持提醒風險時的嚴肅表情。他的右手停在胸前下方、靠近軀幹的位置，手掌略朝外，準備做出向外排除的短促手勢，尚未推到最外側；左手自然放低。此刻尚未露出說貓咪笑話時的笑容。
淺景深聚焦George的眼神與手部，保持自然對話感。畫面不加入貓、供應鏈圖示或踢人的動作。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

### shot_2.7.2

- HTTP400 moderation_blocked, output, category other；request ID：9ac77d5d-cf3a-4da3-8f78-048331014721
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
  4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

提交 prompt：

```text
參考圖說明：
圖1 cam_george_ots_amy_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2藍色人物。
圖4 char_amy.jpeg：Amy人物參考圖，對應圖2右前景紅色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張60mm、近眼高平視的Amy過肩鏡頭。George位於左中景，Amy後腦與肩膀位於右前景，構圖沿用圖2。
George正視Amy，下巴微收，停在鄭重頷首的起始位置。神情沉穩堅定，眉毛自然，嘴唇微啟，帶著理解現實壓力、仍鼓勵對方迎接挑戰的態度。雙手自然靠近桌面，不加入額外指點或揮動手勢。Amy保持專注聆聽的朝向。
淺景深聚焦George的眼神與面部，前景Amy柔和失焦。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

### shot_2.7.3

- HTTP400 moderation_blocked, output, category other；request ID：1f4a498c-6f72-4026-8456-924d2ac44d29
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

提交 prompt：

```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張50mm、近眼高微側拍攝的George中特寫，人物位置與取景沿用圖2，畫面只有George一位人物。
George看向畫外右側的Amy，眼神懇切而有力量，眉頭略收，嘴唇微啟。右手在胸前下方自然握成拳頭，手肘保持彎曲，拳頭靠近軀幹，停在即將小幅向前推進以加強語氣的起始姿態。左手自然放低，肩膀保持放鬆；神情是積極激勵，不是生氣或威嚇。
淺景深聚焦臉與拳頭。畫面不加入跑道、跑者或競賽圖示。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

### shot_2.7.8

- HTTP400 moderation_blocked, output, category other；request ID：879a34d8-a5bf-423a-b66a-c02b155d5e0b
- 有序參考圖：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

提交 prompt：

```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。
將定位人物替換為參考圖說明中的對應角色，只呈現圖2中可見的部位，不補出畫外身體。人物外觀與服裝採用各自人物參考圖，不採用參考圖的展示姿態、多視圖排版或背景；不保留blocks的方塊外形與定位服裝顏色。
將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。場景空景圖不作為刪除人物的依據。人物與場景的光線方向、接觸陰影及材質質感一致。
依下方畫面描述調整指定表情、視線與肢體，其餘沿用圖2。

畫面描述：
這是一張50mm、近眼高微側拍攝的George中特寫，人物位置與裁切沿用圖2，畫面只有George一位人物。
George看向畫外右側的Amy，神情清楚、耐心而有條理，嘴唇微啟。雙手抬到胸前下方，左右手掌大致相對、彼此距離較近，手肘彎曲，停在即將向兩側水平展開以說明涵蓋範圍擴大的起始姿態。雙手高度相近，此刻不做單手向上抬升的第二個動作。
在原有畫框內呈現手勢，不縮小人物或拉遠鏡頭。淺景深兼顧臉與雙手，不加入圖表或階梯。除上述指定調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、分鏡編號或浮水印。
```

本批參考拼圖均經使用者授權Python處理：shot251_main_refs上George／下Amy，shot251_background_refs上char_officelady／下char_barista；esg_coffee_notebook_pen_refs由上到下prop_coffee_set／prop_notebook／prop_pen，保留完整原圖、不裁切。拼圖位於repo .tmp/；原圖位於本專案clp/。本批15次提交，11張生成並保存、4鏡遭拒；shot_2.5.1未修改。


## 2026-10-21 shot_2.8.2 GPT v1（待評鑑）
- 圖片：`assets/images/shot_2.8.2_gpt_v1.png`；內建 image_gen／OpenAI；確切模型與費用未知；本鏡生成一次。
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 一致。目視：Amy微笑與主管左前景成立；Amy頭部放大、留白減少，手部靠近桌沿，前景肩背遮擋改變。 未重試、未改採用。
- 有序參考圖：圖1：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_empty_gpt.png`；圖2：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_block_blender.png`；圖3：`D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`；圖4：`D:/kj-openMontage/projects/course-51-esg/clp/char_supervisor.jpeg`

```text
參考圖說明：
圖 1 cam_amy_ots_supervisor_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_ots_supervisor_block_blender.png：主管過肩拍 Amy 的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側紅色人物。
圖 4 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左前景藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將兩個定位人物替換為對應角色，畫面中只有 Amy 與主管兩人。人物外觀與服裝採用圖 3、圖 4，不採用人物參考圖的展示姿態或構圖。主管只呈現圖 2 可見的後腦、頸部與肩背，不補出正面臉孔或完整身體。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。空景圖不作為刪除前景主管的依據。

畫面描述：
這是一張 50mm、眼高平視、越過主管肩膀拍攝 Amy 的中景。主管的大幅頭肩背影位於左前景並被畫面邊緣裁切，Amy 坐在右側訪客扶手椅上，上半身及雙手可見，下半身被桌面遮擋。保留圖 2 的人物大小、頭頂留白與前後景比例。

Amy 看著左前方的主管，眉眼舒展，露出如釋重負、禮貌而明亮的笑容。她的上身剛開始微微前傾，下巴略收，停在準備輕輕點頭致謝的起始姿態；雙手自然放鬆地安放於扶手附近。主管維持面向 Amy 的聆聽姿勢。

焦點落在 Amy 的眼睛與笑容，左前景主管略柔化，背景盆栽、百葉窗與矮櫃仍可辨識。依上述表演調整 Amy 的表情、頭部與上身，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_2.8.3 GPT v1（待評鑑）
- 圖片：`assets/images/shot_2.8.3_gpt_v1.png`；內建 image_gen／OpenAI；確切模型與費用未知；本鏡生成一次。
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 一致。目視：主管前傾追問、Amy右前景成立；頭部放大、眉形略憂慮，報告沿用灰色條塊而非正常圖表，窗上仍有百葉。 未重試、未改採用。
- 有序參考圖：圖1：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_empty_gpt_v2.png`；圖2：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_block_blender.png`；圖3：`D:/kj-openMontage/projects/course-51-esg/clp/char_supervisor.jpeg`；圖4：`D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

```text
參考圖說明：
圖 1 cam_supervisor_ots_amy_empty_gpt_v2.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_ots_amy_block_blender.png：Amy 過肩拍主管的構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右前景紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將兩個定位人物替換為對應角色，畫面中只有主管與 Amy 兩人。人物外觀與服裝採用圖 3、圖 4，不採用人物參考圖的展示姿態或構圖。Amy 只呈現圖 2 可見的後側頭部、頸部與肩背，不補出正面臉孔。

將場景的材質、風格與光影更新為圖 1 的外觀，空間配置及窗戶可見範圍仍依圖 2，不額外延伸圖 1 的百葉窗。空景圖不作為刪除前景 Amy 的依據。

畫面描述：
這是一張 50mm、眼高平視、越過 Amy 肩膀拍攝主管的中景。主管坐在左側中景的高背椅上，頭部、上身與桌面雙手可見；Amy 的頭肩背影佔據右前景並被右側及下緣裁切。保留圖 2 的人物大小、頭頂留白及前景遮擋比例。

主管的視線已從報告移向 Amy，身體剛開始微微前傾，雙手輕扶在桌面攤開報告的兩側，紙張平放於桌面。他保留一點友善笑意，眉毛略抬，嘴唇微分，呈現話鋒一轉、準備追問具體推動方法的瞬間；神情認真、期待回答，不帶怒氣。

Amy 仍面向主管，肩背剛開始略微繃緊，呈現被突然追問時短暫停住的姿態；不為表現她的反應而轉向鏡頭。

採中景深，主管的臉部與雙手清楚，Amy 前景略柔化。依上述表演調整主管的頭部、上身及雙手，以及 Amy 的肩背，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_2.8.4 GPT v1（待評鑑）
- 圖片：`assets/images/shot_2.8.4_gpt_v1.png`；內建 image_gen／OpenAI；確切模型與費用未知；本鏡生成一次。
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 一致。目視：Amy驚訝、視線向左成立；頭髮幾乎頂住上緣，頭頂留白少於底圖。 未重試、未改採用。
- 有序參考圖：圖1：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_empty_gpt.png`；圖2：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_block_blender.png`；圖3：`D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：Amy 臉部特寫構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭部比例、顯示範圍與裁切。

將定位人物替換為 Amy，畫面中只有 Amy 一人。人物外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或構圖。只呈現圖 2 可見的頭部、頸部及肩胸，不補出手部、桌面或其他人物。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張 85mm、眼高平視的 Amy 臉部特寫。Amy 的頭肩居中，臉部維持圖 2 朝向畫面左側的微側角度，頭頂留白與肩胸裁切沿用圖 2。

Amy 看著畫面左側鏡外的主管，原本的笑容剛剛消失，雙眉抬起、眼睛開始睜大，下巴微微下落，嘴唇張開一小段，呈現剛聽懂「推動策略也要自己規劃」時的錯愕瞬間，準備發出驚訝的第一聲。表情帶有職場喜劇的不可置信感，保留人物原有五官比例，不將眼睛或嘴巴拉伸變形。

焦點清楚落在眼睛與臉部，後方綠葉、紫色檔案盒及水平百葉窗柔和虛化。只調整上述表情及視線，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_2.8.5 GPT v1（待評鑑）
- 圖片：`assets/images/shot_2.8.5_gpt_v1.png`；內建 image_gen／OpenAI；確切模型與費用未知；本鏡生成一次。
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 一致。目視：主管熱情微笑且無手部／桌面入鏡；頭部略側傾、位置偏左，構圖非完全一致。 未重試、未改採用。
- 有序參考圖：圖1：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_supervisor_mcu_15deg_empty_gpt.png`；圖2：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_supervisor_mcu_15deg_block_blender.png`；圖3：`D:/kj-openMontage/projects/course-51-esg/clp/char_supervisor.jpeg`

```text
參考圖說明：
圖 1 cam_supervisor_mcu_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_mcu_15deg_block_blender.png：主管單人中特寫構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與裁切。

將定位人物替換為主管，畫面中只有主管一人。人物外觀與服裝採用圖 3，不採用人物參考圖的憂愁表情、展示姿態或構圖。只呈現圖 2 可見的頭部、肩膀及胸部；雙手與桌面位於畫外，不為呈現手勢而拉遠鏡頭或將手舉入畫面。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張 65mm、眼高平視、15 度微側的主管單人中特寫。主管坐在高背椅上，頭胸居中，維持圖 2 朝向畫面右側的角度、人物大小及頭頂留白。背景為軟木公佈欄與轉角牆面。

主管看著畫面右側鏡外的 Amy，眉毛輕輕揚起，眼神明亮，嘴角上揚形成熱情、自信的笑容，嘴唇略微分開，停在準備笑著回應「當然啊」的瞬間。他的肩膀自然打開，上身帶著鼓勵對方的親切姿態，呈現對 Amy 能力深具信心、準備把她捧為 ESG 專家的神情。保留人物的五官與成熟感，不沿用參考圖中的苦惱神態。

採中淺景深，主管臉部清晰，公佈欄與便條略柔化。依上述表演調整表情、視線與肩膀，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_2.8.6 GPT v1（待評鑑）
- 圖片：`assets/images/shot_2.8.6_gpt_v1.png`；內建 image_gen／OpenAI；確切模型與費用未知；本鏡生成一次。
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 一致。目視：Amy單人中景與左向視線成立；笑容較明顯，無奈／疑惑感偏弱，頭頂留白減少。 未重試、未改採用。
- 有序參考圖：圖1：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_empty_gpt.png`；圖2：`D:/kj-openMontage/projects/course-51-esg/references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_block_blender.png`；圖3：`D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

```text
參考圖說明：
圖 1 cam_amy_ms_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_ms_15deg_block_blender.png：Amy 單人中景構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與裁切。

將定位人物替換為 Amy，畫面中只有 Amy 一人。人物外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或構圖。維持圖 2 的上半身取景，以及手部、扶手與下半身在畫面下緣的裁切，不補出完整椅子或畫外身體。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張 50mm、眼高平視、15 度微側的 Amy 單人中景。Amy 坐在訪客扶手椅上，頭部及上半身居中，身體與臉部維持圖 2 朝向畫面左側的角度。左側保留盆栽，後方保留百葉窗、紫色檔案盒及公文架的位置。

Amy 看著畫面左側鏡外的主管，眉毛略抬，眼睛自然張開，嘴唇輕輕分開，呈現聽完吹捧後帶點疑惑的「喔？」反應。她的嘴角浮現很淡的無奈笑意，眼神仍專注，肩膀稍微放鬆；頭部尚未低下，停在準備眨眼、再點頭接受任務之前的起始姿態。表情保留猶豫與逐漸被說動的感覺，不提前變成興奮慶祝。

雙臂保持自然安放於扶手附近，只呈現原構圖可見的部分。採中景深，Amy 的臉部清楚，背景仍可辨識。依上述表演調整表情、視線與肩膀，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.1 GPT v2（局部修圖，待評鑑）
- 輸出：assets/images/shot_3.7.1_gpt_v2.png；保留 v1，未改採用設定。
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；生成一次。
- 唯一輸入：assets/images/shot_3.7.1_gpt_v1.png。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/call_b3c62888f9fb4c5d831142ce799f1f0d.png
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 相同。目視 Amy 前方多餘桌板已移除，主桌右緣直線延伸；雙手放在大腿上，主管閱讀、兩人表情與主要背景保留。
完整 prompt：
```text
局部編輯這張圖片，保留原有畫面尺寸與構圖。只修正畫面右側 Amy 前方的桌板與她的手臂姿態：移除 Amy 原本雙手下方多長出來的右側木桌板延伸部分。辦公桌應是一張單純的長方形桌面，其右側邊緣從畫面中間偏右、文件堆右後方的桌角，沿原有透視朝畫面下方筆直延伸；不要在 Amy 前方另外突出一塊桌板，不要有 L 形延伸、側桌或托盤。移除延伸桌板後，Amy 與主桌右側邊緣之間呈現自然空隙及原有室內背景。保留中央及左側主桌、主管手下的攤開報告、文件堆、檯燈與前景所有既有道具。
Amy 雙肩放鬆，兩條手臂自然向下，雙手輕鬆放在自己的大腿上，不放桌面、不交握在桌緣；依原有取景和主桌遮擋自然顯示，不刻意補出畫外下肢。Amy 的頭部位置、臉孔、微笑、看向主管的視線、髮型、灰色套裝和座位位置維持原樣。
其他部分保持原圖：主管的外觀、表情、閱讀動作、位置與大小，背景窗戶、城市、植物、椅子、日照、色彩、3D 動畫材質、鏡頭角度和裁切不變。不增加人物、家具、字幕或文字。輸出一張修正後的彩色圖片。
```

## 2026-10-21 shot_2.8.4 GPT v2（以 shot_2.8.6 v1 修改，待評鑑）
- 圖片：`assets/images/shot_2.8.4_gpt_v2.png`；內建 image_gen／OpenAI；確切模型／費用未知；生成一次。
- 唯一輸入：`assets/images/shot_2.8.6_gpt_v1.png`，作為 I2I 原圖。
- 目視：已切近至頭肩，雙眼睜大、嘴張開且無笑意；下緣仍可見少量西裝領口與肩頂，髮頂留白很少。保留原圖，未重試或改採用。
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 一致。
```text
以圖 1（shot_2.8.6_gpt_v1.png）為唯一原圖進行修改。
將鏡頭切近為 Amy 肩膀以上的臉部近景：畫面下緣切在肩膀上緣附近，只保留頭部、頸部與少量肩頂，不呈現胸口、手臂、雙手或桌面。完整保留髮頂並留少量呼吸空間，維持橫式 16:9。保持原圖的微側拍攝方向與看向畫面左側鏡外主管的視線。
將原本帶笑的表情改成明確的驚訝、不可置信：雙眉抬高，雙眼睜大，下巴略微下落，嘴巴自然張開成驚呼的形狀，嘴角不帶笑意。保留 Amy 的五官辨識、綠色眼睛、棕色波浪短髮與原有成熟 3D 動畫比例，不誇張拉伸五官。
除切近取景與表情外，保留原圖角色外觀、灰色西裝、光線方向、暖色日光、3D 動畫材質與辦公室背景。背景隨近景自然裁切並柔和虛化，維持原有百葉窗、左側綠葉與檔案盒的空間關係，不新增人物或物件。
輸出一張 16:9 彩色圖片，不加入文字、字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.7.1 GPT v3（Amy 手指搭桌緣，待評鑑）
- 輸出：assets/images/shot_3.7.1_gpt_v3.png；保留舊版，未改採用設定。
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；生成一次。
- 唯一輸入：assets/images/shot_3.7.1_gpt_v2.png。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/call_58a9a97f39554105950468e1379e69a7.png
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 相同。目視雙手分開、指頭自然輕搭既有桌緣，未加回多餘桌板；主管、人物表情與主要背景保留。
完整 prompt：
```text
局部編輯此圖，只調整右側女性 Amy 的雙臂與雙手姿態。Amy 保持原有坐姿、肩膀位置、頭部、微笑與看向主管的視線。讓她雙肘自然彎曲，前臂舒適地向左前方伸向現有主桌的右側邊緣。雙手分開自然擺放，掌心向下、手腕放鬆，兩手手指微微彎曲，指腹與指尖輕輕搭在既有木桌右側桌緣上，呈現輕鬆、優雅、正在聆聽的自然姿態。兩手沿桌緣前後錯開少許，指頭自然舒展，不交握、不握拳、不抓緊桌緣、不張開成爪狀。手指接觸的桌緣就是原圖已存在、從文件堆右後方桌角斜向畫面下緣延伸的那一條直線邊緣；手臂跨越椅子與桌子間的空隙去接觸它。嚴格保留這條桌緣的原有位置、角度與形狀，不能為托住手掌而擴大桌面，不能在 Amy 前面加回凸出的木桌板、L 形延伸或側桌。保留自然人體關節與正確手指結構。
其餘畫面維持原圖：主管及他的閱讀動作、表情、報告、桌面道具、Amy 的服裝和身體比例、椅子、窗戶、城市、植物、暖陽、3D 動畫風格、攝影角度、原有構圖與裁切。輸出一張相同橫式比例的彩色圖片，不加字幕或額外文字。
```

## 2026-10-21 shot_2.5.9 GPT v1
- 圖片：assets/images/shot_2.5.9_gpt_v1.png（1672×941 RGB），待評鑑，未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 驗證：完整 PNG 解碼及來源複本 SHA256 一致。目視單人、認真表情與右手抬起成立；頭部較 blocks 大、頭頂留白較少，上半身偏左，左手姿態有所改變。未重試。
- 有序參考圖：
  1. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. clp/char_george.png

完整 prompt：
```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2的藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係，維持原有頭頂留白。

將藍色定位人物替換為George。人物五官、灰白頭髮、眼鏡、短鬍鬚與服裝採用圖3，不採用圖3的展示姿態、多視圖排版或背景。只呈現圖2取景範圍中的身體部位，不補出畫外身體；不保留定位人物的方塊外形與藍色服裝。

將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。人物與場景的光線方向、接觸陰影及材質質感一致。

畫面描述：
這是一張50mm、坐姿近眼高、微側角度拍攝的George單人中特寫。George坐在原有木椅上，上半身居中，頭部大小、肩膀位置與下緣裁切沿用圖2，保留下緣局部可見的咖啡杯與右側糖罐。

George面向畫外右側的Amy，視線落在對方坐姿的眼睛高度。他眉頭輕收，眼神認真，嘴唇微啟，呈現正在提醒對方重要風險的表情，尚未露出笑容。右手輕抬至胸前下方，手肘靠近身體，手指自然伸展、掌心略朝外，停在即將向外示意的起始位置；左手維持自然放低的姿態。除右手與指定表情、視線外，其餘姿態沿用圖2。

日間暖陽與柔和陰影依圖1，淺景深聚焦George的雙眼與面部，背景保持可辨識的咖啡館空間。畫面只有George一位人物，Amy位於畫外。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、圖示、分鏡編號或浮水印。
```
## 2026-10-21 shot_4.1.1 GPT v1（座位直播，待評鑑）
- 輸出：assets/images/shot_4.1.1_gpt_v1.png；未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_cc4e299be5894bd5af66e699639c60aa.png
- 有序參考圖：1. clp/char_amy.jpeg；2. references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v2.png。
- 驗證：1672×941 RGB PNG，完整解碼／來源複本 SHA256 相同。目視單人坐姿、直視鏡頭、右手打招呼、服裝與辦公室背景成立；張口笑容較大、左手部分貼近下緣。未重試。
- 本次依使用者指定改為座位固定鏡頭直播；原自拍 Match Cut 不適用，尚未回寫 scene_plan。

完整 prompt：
```text
3D Pixar animation style, stylized character design, warm studio rim lighting.

參考圖1為 Amy（char_amy），提供人物五官、髮型、身形與服裝。保留棕色微捲短髮、側分瀏海、綠色眼睛、淡雀斑、灰色西裝外套與米白色襯衫。
參考圖2為 Amy 的行政辦公座位，提供構圖、座椅位置、辦公室配置、材質與日間光線。

畫面只有 Amy 一人。Amy 坐在參考圖2前景中央的黑色網背辦公椅上，身體自然直立，面向固定在辦公桌前方、接近眼睛高度的直播鏡頭。她直視鏡頭，露出明亮親切、充滿精神的笑容，嘴唇微張，呈現正在向直播觀眾說「哈囉！大家好」的瞬間。右手抬至肩膀附近，掌心朝向鏡頭、五指自然舒展，準備揮手打招呼；左手自然放在桌面，肩膀放鬆。

採直播鏡頭本身的觀看視角，平視固定中景，呈現 Amy 頭頂至腰部附近，頭頂保留適度空間，完整容納打招呼的手。沿用參考圖2的背景與透視，前景左側螢幕不遮住 Amy 的臉與手勢。保留薄荷綠隔板、後方辦公螢幕、書櫃、盆栽，以及百葉窗透入的明亮柔和日光。背景適度柔化，仍能辨識她坐在自己的日常工作座位。

整體自然、輕鬆、有朝氣，像上班途中在座位開啟「Amy 的 ESG 大尋寶」直播。16:9 橫幅，單一完整畫面。無手持手機、無自拍伸臂、無額外人物、無攝影棚設備；不生成文字、字幕、REC 圖示或直播介面。
```


## 2026-10-21 shot_2.7.2 GPT v1
- 圖片：assets/images/shot_2.7.2_gpt_v1.png（1672×941 RGB），待評鑑，未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 驗證：完整 PNG 解碼及來源複本 SHA256 一致。目視雙人過肩與Amy背面失焦成立；George頭部較大、頭頂留白減少、微側傾且帶笑，手臂姿態改變，右下多露出另一只杯。未重試。
- 有序參考圖：
  1. references/scenes/coffee_shop/cameras/cam_george_ots_amy_empty_gpt.png
  2. references/scenes/coffee_shop/cameras/cam_george_ots_amy_block_blender.png
  3. clp/char_george.png
  4. clp/char_amy.jpeg

完整 prompt：
```text
參考圖說明：
圖1 cam_george_ots_amy_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2左中景的藍色人物。
圖4 char_amy.jpeg：Amy人物參考圖，對應圖2右前景的紅色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。維持George原有頭部大小與頭頂留白，以及Amy在右前景的佔畫面比例。

將藍色定位人物替換為圖3的George，將紅色定位人物替換為圖4的Amy。人物外觀與服裝採用各自人物參考圖，不採用其展示姿態、多視圖排版或背景。只呈現圖2中可見的身體部位，不補出畫外身體；不保留定位人物的方塊外形與藍色、紅色服裝。

將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。圖1只提供場景外觀，人物與桌面物件的遮擋關係仍以圖2為準。人物與場景的光線方向、接觸陰影及材質質感一致。

畫面描述：
這是一張60mm、坐姿近眼高平視的過肩鏡頭，從Amy身後拍攝George。George坐在左中景，可見頭部、上半身與桌邊局部手臂；Amy的後腦、肩背與局部手臂位於右前景，沿用圖2的裁切與遮擋，不轉頭露出正臉。畫面只有George與Amy兩位人物。

George看向Amy的眼睛，頭部端正、下巴略收，停在即將鄭重頷首的起始狀態。他神情沉穩堅定，眉毛自然，嘴唇微啟，帶著肯定對方領悟、鼓勵對方迎接挑戰的態度，表情克制、不誇張微笑。肩膀與軀幹保持圖2的位置，雙手沿用圖2靠近桌面的姿態，不新增指點或揮動手勢。Amy維持朝向George的坐姿，安靜專注聆聽。

保留圖2桌面咖啡杯與杯碟的位置及可見範圍。日間暖陽與柔和陰影依圖1，淺景深聚焦George的雙眼與面部，右前景Amy的髮絲與肩背柔和失焦，仍保留可辨識輪廓。除上述指定表情、視線與頭部微調外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、圖示、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.7.3 確認 prompt 生成失敗
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；調用一次。
- HTTP 400 moderation_blocked；moderation_stage: output；categories: other。
- request ID：95abc29a-0a72-4b9f-8fcd-cf6580008624。
- 未產圖、未建立圖片檔、未重試、未改採用。
- 有序參考圖：
  1. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. clp/char_george.png

完整 prompt：
```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2的藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。維持原有頭部大小、頭頂留白與肩膀位置。

將藍色定位人物替換為George。人物五官、灰白頭髮、眼鏡、短鬍鬚與服裝採用圖3，不採用圖3的展示姿態、多視圖排版或背景。只呈現圖2取景範圍中的身體部位，不補出畫外身體；不保留定位人物的方塊外形與藍色服裝。

將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。人物與場景的光線方向、接觸陰影及材質質感一致。

畫面描述：
這是一張50mm、坐姿近眼高、微側角度拍攝的George單人中特寫。George坐在原有木椅上，上半身居中，頭部、肩膀與下緣裁切沿用圖2，保留下緣局部可見的咖啡杯與右側糖罐。畫面只有George一位人物，Amy位於畫外右側。

George看向Amy坐姿的眼睛高度，眼神懇切而堅定，眉頭輕收，嘴唇微啟，呈現鼓勵對方立即採取行動的神情。表情有精神、有迫切感，保持自然對話時的克制。

他的右手在胸前下方自然握拳，拇指輕貼彎曲的手指外側，手腕平直，手肘彎曲並靠近身體。拳頭停在靠近軀幹的位置，作為下一步小幅向前推進、加強語氣的起始姿態。拳頭低於下巴，不遮住臉部。左手維持圖2自然放低的姿態，肩膀放鬆，軀幹位置不變。

日間暖陽與柔和陰影依圖1，淺景深以George的雙眼與面部為主要焦點，握拳手勢清楚可辨，背景保持可辨識的咖啡館空間。除上述右手、表情與視線調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、圖示、分鏡編號或浮水印。
```

## 2026-10-21 shot_3.7.2 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.2_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-bd036820-54ea-4ab2-9d8a-596e9ed6e883.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：97de594c7cc73f82e6a6ef75ec85c14cdcf3cd2dc0c23517a729a97e57086d14。
- 目視：Amy微笑與微前傾成立，人物頭部較底圖大、頭頂留白較少。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_block_blender.png → clp/char_amy.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_ms_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_ms_15deg_block_blender.png：Amy 單人中景構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將紅色定位人物替換為圖 3 的 Amy，只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或表情。畫面只有 Amy 一人。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
畫面描述：
這是一張眼高平視、50mm 視角、15 度微側的 Amy 單人中景。Amy 坐在訪客椅上，頭部與上半身入鏡，手部及下半身沿底圖下緣自然裁切。
Amy 朝向畫外主管，露出誠懇而謙遜的微笑，下巴略收、上身輕微前傾，呈現剛開始欠身致謝的瞬間，神情自然得體。保持原有座位與人物比例，不誇張鞠躬。雙手延續指尖輕搭畫外桌緣的姿態，不為展示手部新增桌面或改變裁切。
除上述表演調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.3 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.3_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-55ecaa61-e151-43ba-ba71-05483e5147fb.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：d873162e2836a1410e97e2e063fa5670e501eff34791a0a017d846fcd0c409cb。
- 目視：主管托腮成立，表情偏憂慮，頭部放大、留白減少。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_supervisor_ms_15deg_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_supervisor_ms_15deg_block_blender.png → clp/char_supervisor.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_supervisor_ms_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_ms_15deg_block_blender.png：主管單人中景構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 的藍色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將藍色定位人物替換為圖 3 的主管，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或憂愁表情。畫面只有主管一人，Amy 位於畫外。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留背景公告板、椅背與畫面下緣既有桌面裁切，不擴大取景以展示報告。
畫面描述：
這是一張眼高平視、50mm 視角、15 度微側的主管單人中景。主管坐在辦公桌後，頭部與上半身居中，桌面僅在畫面下緣局部可見。
主管剛收起上一鏡的笑容，眼神專注，眉頭輕微聚攏，嘴角放鬆，呈現認真思考下一步規劃的表情，視線朝向畫外 Amy。一隻手自然抬起，指節輕靠下巴，另一隻手留在桌面下緣的原有範圍，不刻意露出畫外計畫書。抬手一側的前臂與手勢可配合調整，其餘軀幹及座位沿用底圖。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.4 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.4_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-cafa7c83-e237-4516-acc1-7f9b398a025c.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：d86a615ff4da3bdb6f4d405c802852c492bbe9508a363bd00b634a6732d3c642。
- 目視：兩人過肩構圖、Amy雙手指尖搭桌緣成立；Amy頭部較大，主管前景輪廓與遮擋略變。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_block_blender.png → clp/char_amy.jpeg → clp/char_supervisor.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_ots_supervisor_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_ots_supervisor_block_blender.png：越過主管肩頭拍 Amy 的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側中景紅色人物。
圖 4 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左側前景藍色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將紅色定位人物替換為圖 3 的 Amy，左側藍色前景人物替換為圖 4 的主管。人物外觀與服裝採用對應參考圖，不採用其展示姿態。畫面共兩人，主管只保留底圖可見的局部頭部背側、肩背與裁切，不補出正臉或完整身體。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
畫面描述：
這是一張眼高平視、50mm 視角的過肩中景。主管的局部頭肩位於左前景，Amy 坐在右側中景訪客椅上，隔桌看著主管。
Amy 神情開朗、毫無戒心，帶著肯定的微笑，眼神專注於主管，下巴剛開始輕輕下收，呈現準備點頭回答的瞬間。雙肩放鬆，雙肘自然彎曲，雙手分開，指尖輕搭自己面前既有桌緣；手腕柔和，不交握、不抓緊桌沿。只調整完成這個姿態所需的前臂與手部，不能向 Amy 座位延伸桌板。
主管前景姿態沿用底圖，不加入額外手勢。除上述調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.5 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.5_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-d44b3f12-4aae-4c2b-bde1-3fd05ab94010.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：a4d5ed2db749553f4c1841c0ad791c160e43c3865e73ac8aa8033f0c69fa982a。
- 目視：主管前傾與Amy背面過肩成立，無新增百葉；桌面計畫書仍偏底圖簡化條狀外觀，未充分套用道具材質，人物比例略變。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_empty_gpt_v2.png → references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_block_blender.png → clp/char_supervisor.jpeg → clp/char_amy.jpeg → clp/prop_proposal_document.png
完整 prompt：
```text
參考圖說明：
圖 1 cam_supervisor_ots_amy_empty_gpt_v2.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_ots_amy_block_blender.png：越過 Amy 肩頭拍主管的構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左側中景藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側前景紅色人物。
圖 5 prop_proposal_document.png：計畫書裝訂與材質參考圖，只取道具外觀，不呈現封面標題或多視角排列。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將藍色定位人物替換為圖 3 的主管，右側紅色前景人物替換為圖 4 的 Amy。人物外觀與服裝採用對應參考圖，不採用其展示姿態。畫面共兩人，Amy 只保留底圖可見的局部後腦、髮絲與肩背，不轉身露出正臉。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。不加入圖 2 外窗上方原本沒有的百葉窗。
桌面攤開的計畫書採用圖 5 的裝訂與紙張材質，維持底圖位置與透視，只顯示內頁，不呈現「增資計畫書」封面。
畫面描述：
這是一張眼高平視、50mm 視角的過肩中景。主管位於左側中景，坐在桌後；Amy 的局部頭肩位於右前景，兩人隔桌相對。
主管身體剛開始輕微前傾，目光熱切而專注地望向 Amy，眉毛略抬，嘴角帶著勸說意味的微笑，呈現準備交付重要任務的瞬間。雙手仍自然靠近桌面，尚未伸指指定人選，保留後續抬手指向 Amy 的動作空間。
Amy 保持面向主管的聆聽姿態，頭肩尚未出現受驚反應。除主管輕微前傾與表情調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.6 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.6_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-2f7b23bf-447d-485d-bd7f-66fd5c962a56.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：ea32e62595303ebdae6e1986f15e33469728347960cb39faba66c0efdaedad50。
- 目視：Amy驚訝表情成立；視線朝畫面右方，與前鏡向左的對話視線不連戲；頭部較大、留白減少。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_block_blender.png → clp/char_amy.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：Amy 臉部特寫構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部大小、頭頂留白、肩部裁切與背景配置。
將紅色定位人物替換為圖 3 的 Amy。人物外觀與服裝採用圖 3，不採用其展示姿態或微笑表情。畫面只有 Amy 一人，只呈現底圖可見的頭肩，不補出手部、桌面或畫外身體。
將場景的材質、風格與光影更新為圖 1 的外觀，背景依本鏡淺景深柔和虛化，不改變物件位置。
畫面描述：
這是一張眼高平視、85mm 視角的 Amy 臉部特寫，頭肩居中，保持底圖原有微側朝向。
Amy 剛聽到自己被指派，身體短暫僵住，雙眼明顯睜大，眉毛抬起，嘴唇微張、下巴略微落下，呈現錯愕又難以置信的瞬間。視線仍朝向畫外主管，帶著「怎麼又是我」的喜劇反應，但維持原有五官比例，不把眼球放大或嘴巴拉成誇張變形。
雙手在畫外，不為呈現指向自己的動作而把手伸入特寫。除表情調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.7 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.7_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-f944aa8c-a53f-4d68-862f-92bb3dd4a6bc.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：d358f282a062d8f1d934af73eb734cd34e9aac194ad59a2b11a4ac6833a78ebb。
- 目視：主管鼓勵微笑與微張嘴成立；頭部偏大、留白減少、側傾較明顯。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_supervisor_cu_emotion_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_supervisor_cu_emotion_block_blender.png → clp/char_supervisor.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_supervisor_cu_emotion_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_cu_emotion_block_blender.png：主管臉部特寫構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 的藍色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部大小、頭頂留白、肩部裁切與背景配置。
將藍色定位人物替換為圖 3 的主管。人物外觀與服裝採用圖 3，不採用其展示姿態或憂愁表情。畫面只有主管一人，只呈現底圖可見的頭肩，不加入 Amy、手部、計畫書或桌面。
將場景的材質、風格與光影更新為圖 1 的外觀，背景公告板依本鏡淺景深柔和虛化，不改變物件位置。
畫面描述：
這是一張眼高平視、85mm 視角的主管單人特寫，頭肩居中，保持底圖原有微側朝向。
主管望向畫外 Amy，眼神專注而篤定，眉毛輕微抬起，嘴角帶著安撫與鼓勵的淺笑，嘴唇自然微啟，呈現正準備耐心說服她的瞬間。表情誠懇、有把握，帶著主管不容輕易推辭的堅定感，不做狡詐笑容或誇張擠眉弄眼。
本鏡手部位於畫外，不為拍桌或承諾獎勵的動作改變特寫取景。除表情調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.8 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.8_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-f1da71ce-2ff8-4387-9d48-0cc5800e91c8.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：2fa3842cb72d11ee96a2ab6eeb55df8bce7dfdf1b966bc660f8f28134c5d9806。
- 目視：Amy勉強苦笑與為難眉眼成立；頭部較大，表情偏溫和，肩部裁切略變。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_mcu_15deg_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_mcu_15deg_block_blender.png → clp/char_amy.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_mcu_15deg_block_blender.png：Amy 單人中特寫構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將紅色定位人物替換為圖 3 的 Amy。人物外觀與服裝採用圖 3，不採用其展示姿態或開朗微笑。畫面只有 Amy 一人，只呈現底圖可見的頭部、肩膀與上胸，不補出畫外手部或桌面。
將場景的材質、風格與光影更新為圖 1 的外觀，背景依本鏡淺景深柔和虛化，不改變物件位置。
畫面描述：
這是一張眼高平視、65mm 視角、15 度微側的 Amy 單人中特寫，頭部與肩胸以上居中入鏡。
Amy 仍看向畫外主管，眉心微收、內眉抬起、眉尾下垂，眼神流露為難與無奈。嘴角勉強牽起一點不對稱的苦笑，嘴唇微啟，呈現猶豫著準備說「這……這……」的瞬間。肩膀略微鬆下，保持坐姿，表情有職場喜劇的苦瓜臉意味，但不哭泣、不做誇張崩潰表情。
雙手維持畫外，不因手勢改變取景。除上述表情與輕微肩部調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_4.1.2 GPT v1（座位同仁／走廊無人，待評鑑）
- 輸出：assets/images/shot_4.1.2_gpt_v1.png，1672×941 RGB PNG；未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_a5a98957ce6f418aba4771a4dbcd4260.png
- 有序參考圖：
  1. references/scenes/staff_office/cameras/cam_office_wide_level_empty_gpt_v2.png
  2. references/scenes/staff_office/cameras/cam_office_wide_level_block_blender.png
  3. clp/char_amy.jpeg
  4. assets/images/shot_5.1.2.png
- 驗證：完整解碼及來源複本SHA256一致。目視Amy坐姿／雙手示意、六位同仁坐著辦公、走廊無人成立；後排仍有空椅，未完全滿足所有可見工位有人；Amy位置與構圖偏移、頭部側傾。未重試。

完整 prompt：
```text
參考圖說明：
圖1：辦公室場景外觀參考，提供材質、風格與日間光影。
圖2：廣角構圖底圖，提供取景、透視、工位配置及 Amy 的位置與比例。
圖3：Amy 人物參考，對應圖2中央偏左的紅色定位人物。
圖4：其他同仁的外觀、服裝與坐著辦公狀態參考。只參考坐在工位的人物，不帶入走廊中的三位站立或行走人物，不採用此圖的構圖、夕陽色調或額外道具配置。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、桌椅及隔板配置、Amy 佔位與比例、可見範圍及遮擋關係。維持辦公室廣角構圖，不拉近、不放大 Amy。

將紅色定位人物替換為 Amy，五官、髮型、身形與灰色西裝、米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。只呈現取景及隔板遮擋下可見的身體部位。

將場景材質、風格與光影更新為圖1的外觀，保留圖2的空間配置。人物與場景的光線方向、接觸陰影及3D動畫質感一致。

除了 Amy 的座位，圖2其餘每個可見工位都安排一位同仁坐在原有辦公椅上工作，一個工位一人。依圖4坐著的同仁呈現不同髮型、膚色與簡潔商務休閒服裝，避免複製相同臉孔，也不要複製 Amy。所有同仁面向各自桌上的螢幕，專注閱讀或操作鍵盤滑鼠，不看鏡頭、不向 Amy 揮手。身體自然受到既有螢幕、椅背及隔板遮擋，不為露出人物而移動家具，也不透過隔板顯示被遮住的身體。

畫面描述：
這是一張22mm、平視固定鏡頭的行政辦公室廣角全景。Amy 坐在圖2原有座位，位於畫面中央略偏左，隔著薄荷綠屏風露出頭部與部分上半身。前景工位、中央走道與後方書櫃建立空間縱深。

Amy 面向鏡頭，一側眉毛輕輕挑起，嘴角帶著神祕、俏皮又自信的微笑，嘴唇微啟，呈現即將分享「明察暗訪發現了寶藏」的瞬間。雙肘自然彎曲，雙手輕抬至胸前兩側、略高於隔板上緣，掌心微朝上，停在即將向周圍辦公區展開介紹手勢的起始位置。手勢適中、不遮臉，其餘坐姿與位置沿用圖2。

周圍同仁全部坐在各自工位安靜辦公，營造正常工作中的辦公室氛圍。中央走廊、工位間通道與後方門口全部保持無人；沒有站立、行走、交談或穿越走道的人物，沒有走廊人影。

採用圖1明亮柔和的日間自然光，深景深保留整體辦公室清晰度。「寶藏」僅透過 Amy 的表情與手勢暗示，不出現寶箱、金幣或魔法光效。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、文字、直播介面、REC圖示或浮水印。
```


## 2026-10-21 shot_2.7.3 相同 prompt 授權重試失敗
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；調用一次。
- HTTP 400 moderation_blocked；moderation_stage: output；categories: other。
- request ID：c73d02c9-d480-4012-9b7b-9dad2ed5b8c9。
- 依使用者授權以相同 prompt／三圖重試一次；仍未產圖、未建立圖片檔、未再重試、未改採用。
- 有序參考圖：
  1. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. clp/char_george.png

完整 prompt：
```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2的藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。維持原有頭部大小、頭頂留白與肩膀位置。

將藍色定位人物替換為George。人物五官、灰白頭髮、眼鏡、短鬍鬚與服裝採用圖3，不採用圖3的展示姿態、多視圖排版或背景。只呈現圖2取景範圍中的身體部位，不補出畫外身體；不保留定位人物的方塊外形與藍色服裝。

將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。人物與場景的光線方向、接觸陰影及材質質感一致。

畫面描述：
這是一張50mm、坐姿近眼高、微側角度拍攝的George單人中特寫。George坐在原有木椅上，上半身居中，頭部、肩膀與下緣裁切沿用圖2，保留下緣局部可見的咖啡杯與右側糖罐。畫面只有George一位人物，Amy位於畫外右側。

George看向Amy坐姿的眼睛高度，眼神懇切而堅定，眉頭輕收，嘴唇微啟，呈現鼓勵對方立即採取行動的神情。表情有精神、有迫切感，保持自然對話時的克制。

他的右手在胸前下方自然握拳，拇指輕貼彎曲的手指外側，手腕平直，手肘彎曲並靠近身體。拳頭停在靠近軀幹的位置，作為下一步小幅向前推進、加強語氣的起始姿態。拳頭低於下巴，不遮住臉部。左手維持圖2自然放低的姿態，肩膀放鬆，軀幹位置不變。

日間暖陽與柔和陰影依圖1，淺景深以George的雙眼與面部為主要焦點，握拳手勢清楚可辨，背景保持可辨識的咖啡館空間。除上述右手、表情與視線調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、圖示、分鏡編號或浮水印。
```

## 2026-10-21 shot_3.7.2 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.2_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-bd036820-54ea-4ab2-9d8a-596e9ed6e883.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：97de594c7cc73f82e6a6ef75ec85c14cdcf3cd2dc0c23517a729a97e57086d14。
- 目視：Amy微笑與微前傾成立，人物頭部較底圖大、頭頂留白較少。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_ms_15deg_block_blender.png → clp/char_amy.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_ms_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_ms_15deg_block_blender.png：Amy 單人中景構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將紅色定位人物替換為圖 3 的 Amy，只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用人物參考圖的展示姿態或表情。畫面只有 Amy 一人。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
畫面描述：
這是一張眼高平視、50mm 視角、15 度微側的 Amy 單人中景。Amy 坐在訪客椅上，頭部與上半身入鏡，手部及下半身沿底圖下緣自然裁切。
Amy 朝向畫外主管，露出誠懇而謙遜的微笑，下巴略收、上身輕微前傾，呈現剛開始欠身致謝的瞬間，神情自然得體。保持原有座位與人物比例，不誇張鞠躬。雙手延續指尖輕搭畫外桌緣的姿態，不為展示手部新增桌面或改變裁切。
除上述表演調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.3 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.3_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-55ecaa61-e151-43ba-ba71-05483e5147fb.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：d873162e2836a1410e97e2e063fa5670e501eff34791a0a017d846fcd0c409cb。
- 目視：主管托腮成立，表情偏憂慮，頭部放大、留白減少。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_supervisor_ms_15deg_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_supervisor_ms_15deg_block_blender.png → clp/char_supervisor.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_supervisor_ms_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_ms_15deg_block_blender.png：主管單人中景構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 的藍色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將藍色定位人物替換為圖 3 的主管，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或憂愁表情。畫面只有主管一人，Amy 位於畫外。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。保留背景公告板、椅背與畫面下緣既有桌面裁切，不擴大取景以展示報告。
畫面描述：
這是一張眼高平視、50mm 視角、15 度微側的主管單人中景。主管坐在辦公桌後，頭部與上半身居中，桌面僅在畫面下緣局部可見。
主管剛收起上一鏡的笑容，眼神專注，眉頭輕微聚攏，嘴角放鬆，呈現認真思考下一步規劃的表情，視線朝向畫外 Amy。一隻手自然抬起，指節輕靠下巴，另一隻手留在桌面下緣的原有範圍，不刻意露出畫外計畫書。抬手一側的前臂與手勢可配合調整，其餘軀幹及座位沿用底圖。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.4 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.4_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-cafa7c83-e237-4516-acc1-7f9b398a025c.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：d86a615ff4da3bdb6f4d405c802852c492bbe9508a363bd00b634a6732d3c642。
- 目視：兩人過肩構圖、Amy雙手指尖搭桌緣成立；Amy頭部較大，主管前景輪廓與遮擋略變。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_ots_supervisor_block_blender.png → clp/char_amy.jpeg → clp/char_supervisor.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_ots_supervisor_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_ots_supervisor_block_blender.png：越過主管肩頭拍 Amy 的構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側中景紅色人物。
圖 4 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左側前景藍色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將紅色定位人物替換為圖 3 的 Amy，左側藍色前景人物替換為圖 4 的主管。人物外觀與服裝採用對應參考圖，不採用其展示姿態。畫面共兩人，主管只保留底圖可見的局部頭部背側、肩背與裁切，不補出正臉或完整身體。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
畫面描述：
這是一張眼高平視、50mm 視角的過肩中景。主管的局部頭肩位於左前景，Amy 坐在右側中景訪客椅上，隔桌看著主管。
Amy 神情開朗、毫無戒心，帶著肯定的微笑，眼神專注於主管，下巴剛開始輕輕下收，呈現準備點頭回答的瞬間。雙肩放鬆，雙肘自然彎曲，雙手分開，指尖輕搭自己面前既有桌緣；手腕柔和，不交握、不抓緊桌沿。只調整完成這個姿態所需的前臂與手部，不能向 Amy 座位延伸桌板。
主管前景姿態沿用底圖，不加入額外手勢。除上述調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.5 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.5_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-d44b3f12-4aae-4c2b-bde1-3fd05ab94010.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：a4d5ed2db749553f4c1841c0ad791c160e43c3865e73ac8aa8033f0c69fa982a。
- 目視：主管前傾與Amy背面過肩成立，無新增百葉；桌面計畫書仍偏底圖簡化條狀外觀，未充分套用道具材質，人物比例略變。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_empty_gpt_v2.png → references/scenes/supervisor_office/cameras/cam_supervisor_ots_amy_block_blender.png → clp/char_supervisor.jpeg → clp/char_amy.jpeg → clp/prop_proposal_document.png
完整 prompt：
```text
參考圖說明：
圖 1 cam_supervisor_ots_amy_empty_gpt_v2.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_ots_amy_block_blender.png：越過 Amy 肩頭拍主管的構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 左側中景藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側前景紅色人物。
圖 5 prop_proposal_document.png：計畫書裝訂與材質參考圖，只取道具外觀，不呈現封面標題或多視角排列。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將藍色定位人物替換為圖 3 的主管，右側紅色前景人物替換為圖 4 的 Amy。人物外觀與服裝採用對應參考圖，不採用其展示姿態。畫面共兩人，Amy 只保留底圖可見的局部後腦、髮絲與肩背，不轉身露出正臉。
將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。不加入圖 2 外窗上方原本沒有的百葉窗。
桌面攤開的計畫書採用圖 5 的裝訂與紙張材質，維持底圖位置與透視，只顯示內頁，不呈現「增資計畫書」封面。
畫面描述：
這是一張眼高平視、50mm 視角的過肩中景。主管位於左側中景，坐在桌後；Amy 的局部頭肩位於右前景，兩人隔桌相對。
主管身體剛開始輕微前傾，目光熱切而專注地望向 Amy，眉毛略抬，嘴角帶著勸說意味的微笑，呈現準備交付重要任務的瞬間。雙手仍自然靠近桌面，尚未伸指指定人選，保留後續抬手指向 Amy 的動作空間。
Amy 保持面向主管的聆聽姿態，頭肩尚未出現受驚反應。除主管輕微前傾與表情調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.6 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.6_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-2f7b23bf-447d-485d-bd7f-66fd5c962a56.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：ea32e62595303ebdae6e1986f15e33469728347960cb39faba66c0efdaedad50。
- 目視：Amy驚訝表情成立；視線朝畫面右方，與前鏡向左的對話視線不連戲；頭部較大、留白減少。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_cu_emotion_block_blender.png → clp/char_amy.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：Amy 臉部特寫構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部大小、頭頂留白、肩部裁切與背景配置。
將紅色定位人物替換為圖 3 的 Amy。人物外觀與服裝採用圖 3，不採用其展示姿態或微笑表情。畫面只有 Amy 一人，只呈現底圖可見的頭肩，不補出手部、桌面或畫外身體。
將場景的材質、風格與光影更新為圖 1 的外觀，背景依本鏡淺景深柔和虛化，不改變物件位置。
畫面描述：
這是一張眼高平視、85mm 視角的 Amy 臉部特寫，頭肩居中，保持底圖原有微側朝向。
Amy 剛聽到自己被指派，身體短暫僵住，雙眼明顯睜大，眉毛抬起，嘴唇微張、下巴略微落下，呈現錯愕又難以置信的瞬間。視線仍朝向畫外主管，帶著「怎麼又是我」的喜劇反應，但維持原有五官比例，不把眼球放大或嘴巴拉成誇張變形。
雙手在畫外，不為呈現指向自己的動作而把手伸入特寫。除表情調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.7 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.7_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-f944aa8c-a53f-4d68-862f-92bb3dd4a6bc.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：d358f282a062d8f1d934af73eb734cd34e9aac194ad59a2b11a4ac6833a78ebb。
- 目視：主管鼓勵微笑與微張嘴成立；頭部偏大、留白減少、側傾較明顯。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_supervisor_cu_emotion_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_supervisor_cu_emotion_block_blender.png → clp/char_supervisor.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_supervisor_cu_emotion_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_supervisor_cu_emotion_block_blender.png：主管臉部特寫構圖底圖。
圖 3 char_supervisor.jpeg：主管人物參考圖，對應圖 2 的藍色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部大小、頭頂留白、肩部裁切與背景配置。
將藍色定位人物替換為圖 3 的主管。人物外觀與服裝採用圖 3，不採用其展示姿態或憂愁表情。畫面只有主管一人，只呈現底圖可見的頭肩，不加入 Amy、手部、計畫書或桌面。
將場景的材質、風格與光影更新為圖 1 的外觀，背景公告板依本鏡淺景深柔和虛化，不改變物件位置。
畫面描述：
這是一張眼高平視、85mm 視角的主管單人特寫，頭肩居中，保持底圖原有微側朝向。
主管望向畫外 Amy，眼神專注而篤定，眉毛輕微抬起，嘴角帶著安撫與鼓勵的淺笑，嘴唇自然微啟，呈現正準備耐心說服她的瞬間。表情誠懇、有把握，帶著主管不容輕易推辭的堅定感，不做狡詐笑容或誇張擠眉弄眼。
本鏡手部位於畫外，不為拍桌或承諾獎勵的動作改變特寫取景。除表情調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_3.7.8 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.7.8_gpt_v1.png；工具：內建 image_gen／OpenAI；模型及費用未知，一次生成，未重試／改採用。
- 原圖：C:/Users/servi/.codex/generated_images/01a15a55-906a-7631-8713-085d85eef47e/exec-f1da71ce-2ff8-4387-9d48-0cc5800e91c8.png
- 驗證：完整解碼，1672×941 RGB；來源複本 SHA256 相同：2fa3842cb72d11ee96a2ab6eeb55df8bce7dfdf1b966bc660f8f28134c5d9806。
- 目視：Amy勉強苦笑與為難眉眼成立；頭部較大，表情偏溫和，肩部裁切略變。
- 有序參考圖：references/scenes/supervisor_office/cameras/cam_amy_mcu_15deg_empty_gpt.png → references/scenes/supervisor_office/cameras/cam_amy_mcu_15deg_block_blender.png → clp/char_amy.jpeg
完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_mcu_15deg_empty_gpt.png：主管辦公室場景外觀參考圖。
圖 2 cam_amy_mcu_15deg_block_blender.png：Amy 單人中特寫構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。
生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、人物大小、頭頂留白、顯示範圍與遮擋關係。
將紅色定位人物替換為圖 3 的 Amy。人物外觀與服裝採用圖 3，不採用其展示姿態或開朗微笑。畫面只有 Amy 一人，只呈現底圖可見的頭部、肩膀與上胸，不補出畫外手部或桌面。
將場景的材質、風格與光影更新為圖 1 的外觀，背景依本鏡淺景深柔和虛化，不改變物件位置。
畫面描述：
這是一張眼高平視、65mm 視角、15 度微側的 Amy 單人中特寫，頭部與肩胸以上居中入鏡。
Amy 仍看向畫外主管，眉心微收、內眉抬起、眉尾下垂，眼神流露為難與無奈。嘴角勉強牽起一點不對稱的苦笑，嘴唇微啟，呈現猶豫著準備說「這……這……」的瞬間。肩膀略微鬆下，保持坐姿，表情有職場喜劇的苦瓜臉意味，但不哭泣、不做誇張崩潰表情。
雙手維持畫外，不因手勢改變取景。除上述表情與輕微肩部調整外，其餘沿用圖 2。
輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```

## 2026-10-21 shot_4.1.2 GPT v1（座位同仁／走廊無人，待評鑑）
- 輸出：assets/images/shot_4.1.2_gpt_v1.png，1672×941 RGB PNG；未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_a5a98957ce6f418aba4771a4dbcd4260.png
- 有序參考圖：
  1. references/scenes/staff_office/cameras/cam_office_wide_level_empty_gpt_v2.png
  2. references/scenes/staff_office/cameras/cam_office_wide_level_block_blender.png
  3. clp/char_amy.jpeg
  4. assets/images/shot_5.1.2.png
- 驗證：完整解碼及來源複本SHA256一致。目視Amy坐姿／雙手示意、六位同仁坐著辦公、走廊無人成立；後排仍有空椅，未完全滿足所有可見工位有人；Amy位置與構圖偏移、頭部側傾。未重試。

完整 prompt：
```text
參考圖說明：
圖1：辦公室場景外觀參考，提供材質、風格與日間光影。
圖2：廣角構圖底圖，提供取景、透視、工位配置及 Amy 的位置與比例。
圖3：Amy 人物參考，對應圖2中央偏左的紅色定位人物。
圖4：其他同仁的外觀、服裝與坐著辦公狀態參考。只參考坐在工位的人物，不帶入走廊中的三位站立或行走人物，不採用此圖的構圖、夕陽色調或額外道具配置。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、桌椅及隔板配置、Amy 佔位與比例、可見範圍及遮擋關係。維持辦公室廣角構圖，不拉近、不放大 Amy。

將紅色定位人物替換為 Amy，五官、髮型、身形與灰色西裝、米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。只呈現取景及隔板遮擋下可見的身體部位。

將場景材質、風格與光影更新為圖1的外觀，保留圖2的空間配置。人物與場景的光線方向、接觸陰影及3D動畫質感一致。

除了 Amy 的座位，圖2其餘每個可見工位都安排一位同仁坐在原有辦公椅上工作，一個工位一人。依圖4坐著的同仁呈現不同髮型、膚色與簡潔商務休閒服裝，避免複製相同臉孔，也不要複製 Amy。所有同仁面向各自桌上的螢幕，專注閱讀或操作鍵盤滑鼠，不看鏡頭、不向 Amy 揮手。身體自然受到既有螢幕、椅背及隔板遮擋，不為露出人物而移動家具，也不透過隔板顯示被遮住的身體。

畫面描述：
這是一張22mm、平視固定鏡頭的行政辦公室廣角全景。Amy 坐在圖2原有座位，位於畫面中央略偏左，隔著薄荷綠屏風露出頭部與部分上半身。前景工位、中央走道與後方書櫃建立空間縱深。

Amy 面向鏡頭，一側眉毛輕輕挑起，嘴角帶著神祕、俏皮又自信的微笑，嘴唇微啟，呈現即將分享「明察暗訪發現了寶藏」的瞬間。雙肘自然彎曲，雙手輕抬至胸前兩側、略高於隔板上緣，掌心微朝上，停在即將向周圍辦公區展開介紹手勢的起始位置。手勢適中、不遮臉，其餘坐姿與位置沿用圖2。

周圍同仁全部坐在各自工位安靜辦公，營造正常工作中的辦公室氛圍。中央走廊、工位間通道與後方門口全部保持無人；沒有站立、行走、交談或穿越走道的人物，沒有走廊人影。

採用圖1明亮柔和的日間自然光，深景深保留整體辦公室清晰度。「寶藏」僅透過 Amy 的表情與手勢暗示，不出現寶箱、金幣或魔法光效。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、文字、直播介面、REC圖示或浮水印。
```


## 2026-10-21 shot_4.1.3 GPT v1（指定中特寫，待評鑑）
- 輸出：assets/images/shot_4.1.3_gpt_v1.png，1672×941 RGB PNG；未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_0709aca415aa4b7eb1a5d4377ad4f07f.png
- 有序參考圖：
  1. references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_gpt_v2.png
  2. references/scenes/staff_office/cameras/cam_amy_mcu_15deg_block_blender.png
  3. clp/char_amy.jpeg
  4. assets/images/shot_5.1.2.png
- 驗證：完整解碼／來源複本SHA256一致；右手握拳、看向鏡頭、三位背景同仁辦公成立；頭頂留白減少、頭部側傾、肩膀與下緣裁切偏離白模，張口笑容較大。未重試。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_mcu_15deg_empty_gpt_v2.png：場景外觀參考，提供辦公室材質、風格與日間光影。
圖2 cam_amy_mcu_15deg_block_blender.png：構圖底圖，提供取景、透視、Amy 的佔位、比例與裁切。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的紅色定位人物。
圖4 shot_5.1.2.png：背景同仁的外觀、服裝與坐著辦公狀態參考。只參考坐在工位的人物，不帶入走廊中的人物，不採用此圖的構圖、夕陽色調或額外道具。

生圖指引：
以圖2為編輯底圖，保留取景、透視、家具配置、人物位置、頭部大小、肩膀位置、頭頂留白及畫面下緣裁切。不拉遠、不推近，不為呈現手勢而改成中景或全身景。

將紅色定位人物替換為 Amy。五官、棕色短髮、綠色眼睛、灰色西裝與米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。以自然人體比例替換簡化白模，不保留方塊外形、長方形脖子或紅色服裝。只呈現圖2取景範圍內的身體部位。

將場景材質、風格與光影更新為圖1的外觀，保留圖2的空間配置。人物與場景光線方向、陰影及3D動畫質感一致。

背景取景內的其他工位安排同仁坐在原有座椅上辦公，外觀參考圖4。他們面向各自螢幕，專注工作，不看鏡頭。依家具與 Amy 的遮擋，只露出實際可見的局部頭肩，不為展示同仁而移動螢幕、隔板或放大背景。畫外工位不補入畫面，所有通道保持無人。

畫面描述：
這是一張接近坐姿眼高、約15度微側角度的 Amy 中特寫。Amy 坐在原有黑色網背辦公椅上，頭部與肩胸佔據畫面主要區域，位置與大小沿用圖2。保留左下角局部螢幕與身後的隔板、辦公螢幕、書櫃及百葉窗。

Amy 將臉與視線自然轉向鏡頭，眼睛明亮有神，眉毛微抬，露出充滿期待與行動力的笑容，嘴唇微張，像正在邀請觀眾探索工作中改變世界的超能力。表情熱情自信，避免怒吼或過度誇張。

她的右肘彎曲，右手自然握拳抬至右肩旁、畫面左側，拳頭完整落在畫面內且不遮擋臉部，停在即將輕輕振臂喊出「Let's Go!」的起始位置。手腕保持自然，拇指置於彎曲手指外側。左手自然放低於取景之外，不額外補入。除右臂、表情與看向鏡頭的調整外，其餘坐姿、肩膀及軀幹位置沿用圖2。

明亮柔和的日間光線依圖1，焦點集中在 Amy 的雙眼與面部，背景同仁及辦公環境輕微柔化。整體輕快、有精神，維持日常辦公室直播的親切感，不加入手機、自拍棒、超能力光效或探險裝備。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、文字、直播介面、REC圖示或浮水印。
```

## 2026-10-21 shot_2.7.3 掌心朝上新版 prompt 生成失敗
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；調用一次。
- HTTP 400 moderation_blocked；moderation_stage: output；categories: other。
- request ID：acc7e8d7-d003-476c-b5cc-15b1c037cd9a。
- 使用者確認將握拳改為掌心略朝上的鼓勵手勢。未產圖、未建立圖片檔、未重試、未改採用。
- 有序參考圖：
  1. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. clp/char_george.png

完整 prompt：
```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2的藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。維持原有頭部大小、頭頂留白與肩膀位置。

將藍色定位人物替換為George。人物五官、灰白頭髮、眼鏡、短鬍鬚與服裝採用圖3，不採用圖3的展示姿態、多視圖排版或背景。只呈現圖2取景範圍中的身體部位，不補出畫外身體；不保留定位人物的方塊外形與藍色服裝。

將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。人物與場景的光線方向、接觸陰影及材質質感一致。

畫面描述：
這是一張50mm、坐姿近眼高、微側角度拍攝的George單人中特寫。George坐在原有木椅上，上半身居中，頭部、肩膀與下緣裁切沿用圖2，保留下緣局部可見的咖啡杯與右側糖罐。畫面只有George一位人物，Amy位於畫外右側。

George看向Amy坐姿的眼睛高度，神情專注、誠懇而堅定，眉毛自然，嘴唇微啟，正在鼓勵她把握機會、一起努力跟上企業轉型的腳步。他的表情帶著信心與支持，嘴角放鬆，保持自然交談的神態。

George的右手輕抬至胸前下方，手肘彎曲並靠近身體，掌心略朝上，手指自然微彎，呈現向對方說明與鼓勵的小幅手勢。手掌靠近軀幹、低於下巴，不遮住臉部。左手維持圖2自然放低的姿態，肩膀放鬆，軀幹位置不變。

日間暖陽與柔和陰影依圖1，淺景深以George的雙眼與面部為主要焦點，右手手勢清楚可辨，背景保持可辨識的咖啡館空間。除上述右手、表情與視線調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、圖示、分鏡編號或浮水印。
```

## 2026-10-21 shot_4.7.1 GPT v1（座位直播結語，待評鑑）
- 輸出：assets/images/shot_4.7.1_gpt_v1.png，1672×941 RGB PNG；未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_e1c084879d8b4b38b23e8107b3977b57.png
- 有序參考圖：
  1. references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v2.png
  2. references/scenes/staff_office/cameras/cam_amy_ms_15deg_block_blender.png
  3. clp/char_amy.jpeg
  4. assets/images/shot_5.1.2.png
- 驗證：完整解碼／來源複本SHA256一致。坐姿微笑面向鏡頭、雙手畫外、三位背景同仁辦公成立；人物比例與肩膀位置未完全貼合白模。未重試。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_ms_15deg_empty_gpt_v2.png：場景外觀參考，提供辦公室材質、風格與日間光影。
圖2 cam_amy_ms_15deg_block_blender.png：構圖底圖，提供取景、透視、Amy 的座位、人物比例及裁切。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的紅色定位人物。
圖4 shot_5.1.2.png：背景同仁的外觀、服裝與坐著辦公狀態參考。只參考坐在工位的人物，不帶入走廊中的人物，不採用此圖的構圖、夕陽色調或額外道具。

生圖指引：
以圖2為編輯底圖，保留取景、透視、家具配置、人物佔位、頭部大小、肩膀位置、頭頂留白與下緣裁切。保持座位中景，不推近、不拉遠。

將紅色定位人物替換為 Amy。五官、棕色短髮、綠色眼睛、灰色西裝與米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。以自然人體比例替換簡化白模，不保留方塊外形、長方形脖子或紅色服裝。

將場景材質、風格與光影更新為圖1的外觀，保留圖2的空間配置。人物與場景的光線方向、接觸陰影及3D動畫質感一致。

背景取景內的其他工位安排同仁坐在原有座椅上辦公，外觀參考圖4。一個工位一人，同仁面向各自螢幕專注工作，不看鏡頭。依 Amy、隔板及螢幕的遮擋，只呈現實際可見的局部頭肩，不移動家具來展示人物。畫外工位不補入畫面，所有通道保持無人。

畫面描述：
這是一張50mm、接近坐姿眼高、約15度微側角度的固定中景。Amy 坐在自己的黑色網背辦公椅上，頭部與上半身的位置、比例及裁切沿用圖2。保留左側前景的局部螢幕，以及身後薄荷綠隔板、辦公螢幕、書櫃、盆栽與百葉窗。

Amy 身體自然坐直，肩膀放鬆，臉與視線轉向鏡頭，像正在對直播觀眾做這次 ESG 尋寶的結語。她眼神明亮而篤定，眉毛自然舒展，帶著溫暖、滿足與自信的微笑，嘴唇微啟，呈現親切說話的瞬間。頭部保持自然端正，不誇張側傾、不大笑或喊叫。

雙臂自然放低，雙手留在畫面下緣之外，不刻意抬手、不揮拳、不比出發手勢。整體姿態沉穩放鬆，讓表情與直視鏡頭的眼神傳達真誠的總結感。維持直播鏡頭本身的觀看視角，不出現手機、自拍棒或攝影設備，也不額外加入報告書或展示道具。

採用圖1明亮柔和的日間光線，焦點落在 Amy 的雙眼與面部，背景同仁和辦公環境適度柔化、仍可辨識。整體氛圍溫暖、積極，呈現完成探索後回到日常工作座位、與觀眾分享收穫的感覺。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、文字、直播介面、REC圖示或浮水印。
```

## 2026-10-21 shot_2.7.8 GPT v1
- 圖片：assets/images/shot_2.7.8_gpt_v1.png（1672×941 RGB），待評鑑，未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；生成一次。
- 驗證：完整 PNG 解碼及來源複本 SHA256 一致。目視單人、雙手分開相對與說明姿態成立；人物頭部較blocks大、頭頂留白減少、頭部側傾、上身偏左，雙手間距較寬。未重試。
- 有序參考圖：
  1. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_empty_gpt.png
  2. references/scenes/coffee_shop/cameras/cam_george_mcu_45deg_block_blender.png
  3. clp/char_george.png

完整 prompt：
```text
參考圖說明：
圖1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2的藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。維持原有頭部大小、頭頂留白與肩膀位置。

將藍色定位人物替換為George。人物五官、灰白頭髮、眼鏡、短鬍鬚與服裝採用圖3，不採用圖3的展示姿態、多視圖排版或背景。只呈現圖2取景範圍中的身體部位，不補出畫外身體；不保留定位人物的方塊外形與藍色服裝。

將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。人物與場景的光線方向、接觸陰影及材質質感一致。

畫面描述：
這是一張50mm、坐姿近眼高、微側角度拍攝的George單人中特寫。George坐在原有木椅上，上半身居中，頭部、肩膀與下緣裁切沿用圖2，保留下緣局部可見的咖啡杯與右側糖罐。畫面只有George一位人物，Amy位於畫外右側。

George看向Amy坐姿的眼睛高度，神情專注、耐心而有條理，眉毛自然，嘴唇微啟，正在清楚解釋企業適用範圍逐步擴大的概念。表情平穩、自信，保持自然交談的神態。

他的雙手抬至胸前下方，雙肘彎曲並靠近身體。左右手掌大致相對，彼此保留小段間距，手指自然舒展、微微彎曲，雙手高度相近，停在即將向兩側水平展開的起始位置。兩手清楚分開，不交疊、不接觸，保持低於下巴，不遮住臉部。肩膀放鬆，軀幹位置不變。

雙手在原有取景範圍內自然入鏡，維持人物大小與相機距離。日間暖陽與柔和陰影依圖1，淺景深以George的雙眼與面部為主要焦點，雙手輪廓與手勢清楚可辨，背景保持可辨識的咖啡館空間。除上述雙手、表情與視線調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、圖示、分鏡編號或浮水印。
```

## 2026-10-21 shot_4.7.2 GPT v1（座位直播結語，待評鑑）
- 輸出：assets/images/shot_4.7.2_gpt_v1.png（1672×941 RGB PNG）；內建 image_gen／OpenAI，確切模型與費用未知，生成一次，未改採用。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_f805477d9c3e45a2a6acf0d47831aa91.png
- 有序參考圖：references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_gpt_v2.png；references/scenes/staff_office/cameras/cam_amy_mcu_15deg_block_blender.png；clp/char_amy.jpeg；assets/images/shot_5.1.2.png。
- 驗證：完整解碼／來源複本SHA256一致。雙手分開相對、背景三位同仁辦公成立；頭頂留白減少、肩膀與裁切偏離白模，手距略大。未重試。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_mcu_15deg_empty_gpt_v2.png：場景外觀參考，提供辦公室材質、風格與日間光影。
圖2 cam_amy_mcu_15deg_block_blender.png：構圖底圖，提供取景、透視、Amy 的佔位、比例與裁切。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的紅色定位人物。
圖4 shot_5.1.2.png：背景同仁的外觀、服裝與坐著辦公狀態參考。只參考坐在工位的人物，不帶入走廊中的人物，不採用此圖的構圖、夕陽色調或額外道具。

生圖指引：
以圖2為編輯底圖，保留取景、透視、家具配置、人物位置、頭部大小、肩膀位置、頭頂留白與下緣裁切。維持中特寫，不為呈現手勢而拉遠或縮小人物。

將紅色定位人物替換為 Amy。五官、棕色短髮、綠色眼睛、灰色西裝與米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。以自然人體比例替換簡化白模，不保留方塊外形、長方形脖子或紅色服裝。

將場景材質、風格與光影更新為圖1的外觀，保留圖2的空間配置。人物與場景的光線方向、接觸陰影及3D動畫質感一致。

背景取景內的其他工位安排同仁坐在原有座椅上辦公，外觀參考圖4。同仁面向各自螢幕專注工作，不看鏡頭。依 Amy、隔板與螢幕的遮擋，只露出實際可見的局部頭肩，不移動家具來展示人物。畫外工位不補入畫面，所有通道保持無人。

畫面描述：
這是一張65mm、接近坐姿眼高、約15度微側角度的 Amy 中特寫。Amy 坐在自己的黑色網背辦公椅上，頭部與肩胸佔據畫面主要區域，位置、大小及裁切沿用圖2。保留左下角局部螢幕，以及身後隔板、辦公螢幕、書櫃與百葉窗。

Amy 身體自然坐直，肩膀放鬆，臉與視線轉向鏡頭，正在向直播觀眾傳達結語中的核心信念。她目光穩定、真誠而有力量，眉毛自然舒展，嘴角帶著克制而溫暖的微笑，嘴唇微啟，呈現認真說話的瞬間。頭部自然端正，不誇張側傾、不大笑、不皺眉怒吼。

雙肘靠近身體，雙手抬至胸前下方，在畫面下部自然可見。兩掌相對、相隔約一個拳頭的距離，手指放鬆微彎，停在即將向內靠攏、象徵凝聚大家力量的起始位置。雙手尚未接觸，不拍手、不十指交扣、不擺祈禱姿勢，也不遮擋臉部。前臂依原有下緣自然裁切，不補出完整手肘或桌面。除雙臂手勢、表情與視線外，其餘人物位置與軀幹姿態沿用圖2。

採用圖1明亮柔和的日間光線，淺景深聚焦 Amy 的雙眼與面部，背景同仁與辦公環境柔和失焦但仍可辨識。整體沉穩、溫暖且具有鼓舞感，像在熟悉的工作座位上，真誠邀請每位觀眾一起參與。

維持直播鏡頭本身的觀看視角，不出現手機、自拍棒、攝影設備、報告書或象徵力量的特效。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、文字、直播介面、REC圖示或浮水印。
```

## 2026-10-21 shot_2.7.3 GPT v1（cu_emotion近景）
- 圖片：assets/images/shot_2.7.3_gpt_v1.png（1672×941 RGB），待評鑑，未改採用。
- 工具／供應商：內建 image_gen／OpenAI；確切模型與費用未知；本次生成一次。
- 驗證：完整 PNG 解碼及來源複本 SHA256 一致。目視單人頭肩近景、雙手桌面畫外、向右說話成立；頭部較blocks大、頭頂留白減少，肩膀位置與頭部角度有偏差。未重試。
- 有序參考圖：
  1. references/scenes/coffee_shop/cameras/cam_george_cu_emotion_empty_gpt.png
  2. references/scenes/coffee_shop/cameras/cam_george_cu_emotion_block_blender.png
  3. clp/char_george.png

完整 prompt：
```text
參考圖說明：
圖1 cam_george_cu_emotion_empty_gpt.png：場景外觀參考圖。
圖2 cam_george_cu_emotion_block_blender.png：構圖底圖。
圖3 char_george.png：George人物參考圖，對應圖2的藍色人物。

生圖指引：
以圖2為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。維持原有頭部大小、頭頂留白、肩膀位置及下緣裁切。

將藍色定位人物替換為George。人物五官、灰白頭髮、眼鏡、短鬍鬚與服裝採用圖3，不採用圖3的展示姿態、多視圖排版或背景。只呈現圖2中可見的身體部位，不補出畫外身體；不保留定位人物的方塊外形與藍色服裝。

將場景的材質、風格與光影更新為圖1的外觀，不改變圖2的空間配置。人物與場景的光線方向、陰影及材質質感一致。

畫面描述：
這是一張坐姿近眼高、微側角度拍攝的George單人頭肩近景。George位於畫面中央，可見完整頭部、頸部、肩膀與部分上胸，其餘身體由畫面下緣裁切。頭部朝向與人物大小沿用圖2，保留髮頂上方的空間。雙手與桌面位於畫外。

George看向畫外右側的Amy，視線落在對方坐姿的眼睛高度。他眉頭輕收，眼神專注、懇切而堅定，嘴唇微啟，呈現正在鼓勵對方積極迎接企業轉型挑戰的說話瞬間。表情帶著清楚的信念與適度的迫切感，嘴角自然放鬆，維持克制的交談神態。

George的頭部保持端正，肩膀自然放鬆，身體位置沿用圖2。以面部表情傳達「大家已經開始行動，我們也要努力跟上」的激勵意味。

日間暖陽與柔和陰影依圖1，淺景深聚焦George的雙眼與面部。背景保留原有木框窗、綠色牆柱、局部植物掛畫與椅背的配置，呈現柔和失焦的咖啡館空間。畫面只有George一位人物。除上述表情與視線調整外，其餘沿用圖2。

輸出一張16:9彩色分鏡圖，呈現單一連貫畫面，不加入字幕、對話框、圖示、分鏡編號或浮水印。
```

## 2026-10-21 shot_2.6.1 GPT v1（熟睡貓首幀，待評鑑）
- 輸出：assets/images/shot_2.6.1_gpt_v1.png（1672×941 RGB PNG）；內建image_gen／OpenAI，模型費用未知；生成一次，T2I無參考圖，未改採用。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_e0ad75a3fea94a12b64717aa5a8a56c9.png
- 驗證：完整解碼／複本SHA256一致；單隻橘白貓閉眼蜷睡、完整入鏡、無文字人物成立；毛髮偏寫實、佔比偏大、兩側翻身空間偏少。未重試。
完整 prompt：
```text
3D Pixar animation style, stylized character design, warm studio rim lighting.

畫面只有一隻圓潤可愛的橘白虎斑貓，沒有任何人物。貓咪蜷臥在米色布藝沙發的柔軟坐墊中央，身體放鬆，四肢自然收攏，頭輕輕枕在前爪旁，尾巴沿著身體側邊彎曲。雙眼完全閉上，耳朵自然放鬆，嘴巴閉合，呈現毫無戒心、睡得非常香甜的瞬間。橘色虎斑與白色毛區清晰，毛髮柔軟，身體有自然重量感，坐墊在身體下方輕微下陷。

場景是 George 家中溫馨明亮的日間客廳。午後暖陽從畫外側面的窗戶照入，在米色沙發上形成柔和光影。背景只保留簡潔的抱枕與少量室內綠色植栽，不堆滿裝飾。整體舒適、安靜，帶有輕鬆幽默的生活感。

採50mm鏡頭，沙發坐墊高度平視，固定鏡頭，中近景寵物特寫。貓咪完整入鏡並位於畫面中央，頭、耳朵、身體與尾巴均不裁切。四周保留適度坐墊空間，尤其身體兩側留出後續翻身的餘地；不把貓咪塞滿畫面。淺景深聚焦貓咪，後方抱枕與植栽柔和失焦，仍可辨識客廳環境。

這是一張後續動畫的熟睡起始畫面，只呈現同一個瞬間：貓咪尚未驚醒、尚未張望、尚未翻身。不睜眼、不張嘴、不豎起警戒耳朵，不加入動作殘影、多重姿勢或分格畫面。

輸出一張16:9彩色分鏡圖，不加入字幕、文字、睡眠符號、對話框、擬聲字或浮水印。
```

## 2026-10-21 shot_4.7.3 GPT v1（座位直播道別，待評鑑）
- 輸出：assets/images/shot_4.7.3_gpt_v1.png（1672×941 RGB PNG）；內建image_gen／OpenAI，確切模型與費用未知，生成一次，未改採用。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/call_5637e4b2f2da4a2c8aba25878af7cb6d.png
- 有序參考圖：
  1. references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v2.png
  2. references/scenes/staff_office/cameras/cam_amy_ms_15deg_block_blender.png
  3. clp/char_amy.jpeg
  4. assets/images/shot_5.1.2.png
- 驗證：完整解碼／來源複本SHA256一致。坐姿微笑、右手完整入鏡道別、三位同仁辦公成立；頭部略側傾、頭頂留白減少、人物比例與肩位偏離白模，背景增加小盆栽。未重試。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_ms_15deg_empty_gpt_v2.png：場景外觀參考，提供辦公室材質、風格與日間光影。
圖2 cam_amy_ms_15deg_block_blender.png：構圖底圖，提供取景、透視、Amy 的座位、人物比例與裁切。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的紅色定位人物。
圖4 shot_5.1.2.png：背景同仁的外觀、服裝與坐著辦公狀態參考。只參考坐在工位的人物，不帶入走廊中的人物，不採用此圖的構圖、夕陽色調或額外道具。

生圖指引：
以圖2為編輯底圖，保留取景、透視、家具配置、人物佔位、頭部大小、肩膀位置、頭頂留白與下緣裁切。維持座位中景，不拉遠、不推近，不為呈現手勢而改變人物比例。

將紅色定位人物替換為 Amy。五官、棕色短髮、綠色眼睛、灰色西裝與米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。以自然人體比例替換簡化白模，不保留方塊外形、長方形脖子或紅色服裝。

將場景材質、風格與光影更新為圖1的外觀，保留圖2的空間配置。人物與場景光線方向、接觸陰影及3D動畫質感一致。

背景取景內的其他工位安排同仁坐在原有座椅上辦公，外觀參考圖4。同仁面向各自螢幕專注工作，不看鏡頭、不跟著揮手。依 Amy、隔板與螢幕的遮擋，只呈現實際可見的局部頭肩，不移動家具來展示人物。畫外工位不補入畫面，所有通道保持無人。

畫面描述：
這是一張50mm、接近坐姿眼高、約15度微側角度的固定中景。Amy 坐在自己的黑色網背辦公椅上，頭部與上半身的位置、比例及裁切沿用圖2。保留左側前景局部螢幕，以及身後薄荷綠隔板、辦公螢幕、書櫃、盆栽與百葉窗。

Amy 身體自然坐直，肩膀放鬆，臉與視線轉向鏡頭。她帶著完成分享後滿足、親切而略帶俏皮的笑容，雙眼自然睜開，嘴唇微啟，像正在對直播觀眾說「我們下次見！掰掰！」。頭部自然端正，不誇張側傾、不大笑或喊叫。

右肘自然彎曲，右手抬至右肩旁、畫面左側，掌心朝向鏡頭，五指自然舒展並略微分開，手腕放鬆，停在即將輕輕左右揮手道別的起始位置。整隻手完整落在畫面內，不遮臉、不與前景螢幕重疊，也不向鏡頭過度前伸造成手掌放大。左臂自然放低，左手留在畫面下緣之外。除右臂手勢、表情與視線外，其餘姿態沿用圖2。

採用圖1明亮柔和的日間光線，焦點集中在 Amy 的雙眼與面部，背景同仁及辦公環境適度柔化。整體溫暖、輕快、有收尾的滿足感，維持熟悉工作座位上的直播告別氛圍。

這張圖片只呈現準備揮手的單一瞬間，尚未眨眼，也尚未伸手關閉直播。維持直播鏡頭本身的觀看視角，不出現手機、自拍棒、攝影設備、報告書或超能力特效。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、文字、直播介面、REC圖示或浮水印。
```


## 2026-10-21 shot_3.8.2 GPT v1（待評鑑）
- 圖片：`assets/images/shot_3.8.2_gpt_v1.png`
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；1 次生成。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：George 單人微笑、嘴唇略張、雙手畫外；視線偏左上，頭部傾斜、肩膀輪廓及背景遮擋偏離 blocks，背景細節重繪。未追加生成或更新正式採用。

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：商辦街道同機位場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George（char_george）人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、大小比例、顯示範圍與遮擋關係。保留頭頂留白、肩膀位置及胸部裁切，不放大頭部、不拉近鏡頭。

將藍色定位人物替換為 George，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。保留灰白後梳髮、深棕色方框眼鏡、白色短鬍鬚、棕色背心、米白襯衫與深棕色領帶。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。人物接受與街景一致的溫暖日光，眼鏡反光柔和，雙眼仍清楚可見。

畫面描述：
這是一張眼高平視、斜側約 45 度的 George 單人中近景。George 的頭部、雙肩與胸部入鏡，身體位置及裁切沿用圖 2，雙手與腰部位於畫外。背景為商辦大樓的米白石材立柱、落地玻璃門，以及向畫左遠方延伸的花台與行道樹。

捕捉 George 邊走邊轉頭回應 Amy、準備開口打趣的瞬間。軀幹保持底圖的行進朝向，臉部略轉向畫左，視線自然落在畫左鏡外 Amy 的臉部高度，不看鏡頭、不仰望天空。

George 眉毛輕輕挑起，眼神帶著看穿 Amy 來意的幽默笑意，嘴角微微上揚，嘴唇略張，呈現即將說出「你是剛好碰到我？」的親切、半開玩笑神情。表情放鬆自然，不做誇張大笑或嘲諷表情。

畫面只出現 George 一人，不加入 Amy 的頭部、肩膀或手，也不加入書本。採用淺景深，George 的眼睛與面部清晰，背景柔和失焦，仍能辨識玻璃門、石柱及植栽的空間關係。除上述頭部朝向、視線與表情外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、文字或浮水印。
```


## 2026-10-21 shot_3.8.1 GPT v1（待評鑑）
- 圖片：`assets/images/shot_3.8.1_gpt_v1.png`
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；1 次生成。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_wide_low_angle_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_wide_low_angle_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：雙人全身、Amy 左手招呼與五名路人呈現；主角明顯放大、頭頂位置上移、步態及路人位置朝向偏離 blocks。未追加生成或改正式採用。

### 完整 prompt
```text
參考圖說明：
圖 1 cam_twoshot_wide_low_angle_empty_gpt.png：商辦街道場景外觀參考圖。
圖 2 cam_twoshot_wide_low_angle_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy（char_amy）人物參考圖，對應圖 2 前景紅色人物。
圖 4 char_george.png：George（char_george）人物參考圖，對應圖 2 前景藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、大小比例、顯示範圍與遮擋關係。維持人物在整幅街景中的原有尺度，不放大人物、不拉近鏡頭、不將兩人移到畫面中央。

將紅色定位人物替換為 Amy，藍色定位人物替換為 George。人物外觀與服裝分別採用圖 3、圖 4，不採用人物參考圖的展示姿態或構圖。保留 Amy 的灰色西裝與棕色短髮，以及 George 的方框眼鏡、灰白髮、鬍鬚、棕色背心與領帶。

將背景五名灰色定位人物替換為穿日常通勤服裝的遠景路人，保持各自位置、尺度與行走朝向，不複製 Amy 或 George 的外觀，不保留方塊人形。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。人物接受與街景一致的溫暖日光，鞋底與地面有自然接觸陰影。

畫面描述：
這是一張 35mm 鏡頭感、低角度微仰視的雙人全景。兩位主角位於畫面右側人行道，Amy 在左、George 在右，兩人從頭到鞋完整入鏡，保留底圖的身高差、間距、腳底位置及上方大面積建築與天空。街道向遠方延伸，背景五名路人沿用底圖位置，畫面共七人。

捕捉 Amy 剛快步追到 George 身旁、準備開口打招呼的瞬間。兩人身體仍朝鏡頭方向行走，雙腿維持底圖的跨步狀態。Amy 頭部與視線轉向畫右的 George，眉毛微抬，嘴唇略張，帶著稍微氣喘卻熱情開心的笑容；靠近 George 的左手屈肘抬起，手掌自然張開，停在開始揮手招呼的位置，右手低放隨步伐自然擺動。

George 保持輕鬆步行姿態，頭部略轉向畫左的 Amy，視線落在她臉上，露出溫和、略帶驚喜的微笑，雙臂保持自然低放。兩人看向彼此，不直視鏡頭。

保留街道的開闊感與自然深景深，人物、建築和街道仍可辨識，不將背景化成大片模糊。除上述表情、視線與招呼手勢外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、文字或浮水印。
```

# 2026-10-21 staff_office 夜景參考圖
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未揭露；單次編輯。
- 輸入：`clp/loc_staff_office.png`。
- 輸出：`clp/loc_staff_office_night.png`（1672×941 RGB），完整解碼通過。
- 目視：窗外深藍夜色及建築燈光、室內頂燈亮起、日照條紋移除；主要構圖及家具保留。待使用者評鑑，未改採用。
- 完整 prompt：Edit the provided office reference into a nighttime scene. Preserve the exact camera, framing, perspective, room geometry, furniture layout, teal cubicle dividers, desks, black monitors, chairs, bookshelves, plants, wall art, blinds, open door, carpet and polished stylized 3D rendering. Change only time of day and lighting: through every window show a dark deep navy night sky and the same surrounding city buildings with a few softly illuminated windows. Remove all daylight, golden sunlight shafts and sun-cast blind stripes from walls, furniture and carpet. Keep the existing ceiling light panels turned on, providing soft warm-neutral indoor office illumination with natural shadows; outdoors distinctly dark, interior still clearly readable. No people, no new objects, no moon added, no text. Match original landscape aspect ratio and composition.

# 2026-10-21 staff_office 深夜減燈 v2
- 用途：scene 3.9 Amy 獨自加班的空景參考；使用者要求減少頂燈。
- 內建 image_gen／OpenAI 單次編輯；模型與費用未知。
- 輸入 `clp/loc_staff_office_night.png`；輸出 `clp/loc_staff_office_night_v2.png`，1672×941 RGB，完整解碼通過。
- 目視僅左側一組頂燈亮起，其餘區域昏暗，構圖保留；未加入人物、未改採用。分鏡原設僅桌燈與螢幕，本版依本次要求保留少量頂燈。
- 完整 prompt：Edit this exact nighttime office image for scene 3.9 of an animated ESG course, the atmosphere of Amy working alone very late after everyone has left. This is an EMPTY location reference: do not add Amy or any people. Reduce ceiling lighting dramatically: switch OFF all visible ceiling fluorescent panels except ONE small panel above the left middle row of cubicles. Off panels must visibly be dark, non-emissive grey fixtures, not white glowing rectangles. The remaining panel emits only a subdued localized warm-neutral pool of light. Most of the office, especially the right side, rear shelves, and foreground aisle, is in deep soft shadow with very faint cool blue nighttime window fill. Aim for quiet, solitary late-night overtime, cinematic low-key lighting, not the evenly bright office in the input. Keep enough shadow detail to recognize the furniture. Preserve exact camera, framing, perspective, layout, geometry, cubicle colors, furniture, monitors, plants, books, wall art, blinds, open door, dark blue city night and original stylized 3D materials. Do not add desk lamps or props, do not change monitor content. Only change indoor lighting and its resulting shadows/exposure. No sunlight, no people, no text. Keep landscape aspect ratio.

# 2026-10-21 staff_office 夜景 v3：僅中排頂燈
- 使用者認為 v2 太暗，指定回到 v1，保留中排並取消左右外排頂燈。
- 內建 image_gen／OpenAI，單次編輯，模型費用未知。
- 輸入 `clp/loc_staff_office_night.png`；輸出 `clp/loc_staff_office_night_v3.png`（1672×941 RGB），完整解碼通過。
- 目視中排三組頂燈亮起，左右外排熄滅，室內保持接近 v1 亮度；待評鑑，未改採用。
- 完整 prompt：Make a precise lighting edit to this supplied V1 nighttime office image. The ceiling has THREE longitudinal rows of rectangular light panels receding toward the back wall. Keep ONLY THE CENTER ROW switched ON at its original full brightness: the cropped panel near top center, the panel around x=850 y=93, and the farther panel around x=905 y=140 (coordinates relative to the 1672x941 reference). Switch OFF every panel in the LEFTMOST row (approximately x=150 y=22, x=450 y=105, x=620 y=145) and RIGHTMOST row (approximately x=1320 y=80, x=1230 y=130). These side fixtures remain physically in place but are non-emissive neutral gray. Do not remove ceiling geometry. Crucially preserve a comfortably readable, moderately bright interior close to the supplied V1 reference exposure: the lit center row should provide broad soft bounced illumination across desks, teal cubicles, carpet and bookshelves. Only a modest reduction in brightness at the sides; NO extremely dark shadows, NO moody underexposure, NO dramatic darkening of the whole image. Preserve exact framing, camera, layout, objects, materials, colors, dark blue city nighttime view and empty room. No people or new objects. Change only which ceiling lamps are on and the corresponding subtle lighting. Landscape image matching reference.

# 2026-10-21 staff_office 夜景 v4：室內約暗 20%
- 使用者核准以 v3 將室內環境約暗 20%，中排三組頂燈與窗外維持原亮度。
- 內建 image_gen／OpenAI 單次編輯；模型費用未知。
- 輸入 `clp/loc_staff_office_night_v3.png`；輸出 `clp/loc_staff_office_night_v4.png`（1672×941 RGB），完整解碼通過。
- 目視室內較暗、家具可辨、中排三組亮燈及夜景保留；20% 為生成提示目標，非精確光度校準。待評鑑，未改採用。
- 完整 prompt：Edit this exact office night reference V3 with ONE subtle lighting adjustment only: lower the perceived brightness of the INTERIOR ROOM SURFACES by approximately 20 percent compared with the input, to create a quiet late-night overtime atmosphere while keeping furniture and details clearly readable. Desks, teal cubicle partitions, walls, ceiling surfaces and carpet should be moderately darker, with natural soft shadows, not crushed blacks. Keep EXACTLY the same THREE CENTER-ROW ceiling light panels ON and keep their luminous panel brightness unchanged. All left and right outer-row ceiling panels remain OFF. Preserve the nighttime city outside every window at its original brightness and appearance. Do not globally darken the windows or the three luminous panels. Preserve camera, framing, geometry, furniture, objects, colors, materials and stylized 3D rendering exactly; no new objects, no people, no screen light added, no text. This is a restrained 20% interior ambience reduction, not a dramatic dark scene. Keep original landscape aspect ratio.



## 2026-10-21 staff_office 螢幕空景夜景 GPT v3（待評鑑）
- 輸出：references/scenes/staff_office/cameras/cam_monitor_insert_front_empty_gpt_v3.png（1672×941 RGB）。內建image_gen／OpenAI，模型及費用未知，生成一次。
- 有序參考圖：1. references/scenes/staff_office/cameras/cam_monitor_insert_front_empty_blender.png；2. clp/loc_staff_office_night_v4.png。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-49cf834c-3dfd-4425-b229-bd4485f5b20e.png
- 驗證：完整解碼／來源複本SHA256一致。螢幕緊特寫、空白黑屏、無人物、夜間冷暖光成立；主要邊界接近底圖，隔板織紋較強，百葉／窗外細節有所改變，非像素級一致。保留舊版，未改模型或採用，未重試。

完整 prompt：
```text
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的夜間場景背景。
圖1 cam_monitor_insert_front_empty_blender.png 唯一決定相機位置、觀看方向、透視、構圖、畫面裁切及物件配置。
圖2 loc_staff_office_night_v4.png 是同一場景的共用美術參考，只提供材質、色彩、光影與氣氛。不要採用圖2的拍攝角度、消失點、畫面排列或可見範圍；不要重新生成圖2。
匹配圖2低照度但家具仍清晰可辨的夜間辦公室：柔和暖色室內燈光、深青綠布面隔板、淺木色桌面、霧面深灰黑設備、米白框架，以及窗外深藍夜色和稀疏城市燈光。不逐張加強飽和度、暖色或泛光。依圖1朝向維持合理光源方向，不把圖2投影直接貼到本鏡。消除圖1白天的明亮窗景與日光感。

【保留本機位】
維持圖1的16:9畫幅、觀看方向、消失點、主要結構與遮擋。保留螢幕外框、內部顯示區、下方銀灰底邊、桌面、隔板、窗框與百葉窗的原有位置、數量、尺度與主要輪廓。
不旋轉相機、不鏡像、不拉遠或拉近，不移植參考圖中本鏡畫外的物件。不為展示完整物件而補出被裁切部分；不新增鍵盤、滑鼠、檯燈、椅子、植物或天花板。

【材質與細節提升】
沿用圖1構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。螢幕框呈細緻霧面深灰材質，隔板呈圖2的青綠織物質感，桌面保留細緻淺木紋，窗框與底邊維持柔和低光澤。
螢幕顯示區維持關閉狀態的均勻深灰黑色空白面，只有極輕微合理環境反射，不顯示文件、文字、圖示、介面或窗戶鏡像。保持乾燥乾淨，不增加髒污、強烈鏡面反光或塑膠感。
作為後續加入螢幕內容的空景母圖，不額外強化散景，保留邊界與材質細節。

【本鏡畫面】
近距離正面略帶透視的電腦螢幕插鏡。大型螢幕佔據畫面大部分，外框位置、內部顯示區四角及梯形透視嚴格依圖1；左側保留較寬的隔板與窗景，右側僅有狹窄背景，下緣保留原有銀灰邊條及局部木桌裁切。窗外可見區域改成圖2同一夜間城市的色彩與亮度，不能擴大窗景。整體明暗匹配夜景v4，保留螢幕框與隔板可辨的層次。

【空景與輸出】
零人物，不出現人體、手臂、人物倒影或人形剪影。只輸出一張16:9高解析度完整彩色圖片，不製作拼貼，不加字幕、標誌或水印。
```


## 2026-10-21 cafe 平視廣角空景 GPT 首張（待評鑑）

- 輸入依序：
  1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_twoshot_wide_level_empty_blender.png`
  2. `D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/cafe/Cafe_2.png`
- 輸出：`references/scenes/cafe/cameras/cam_twoshot_wide_level_empty_gpt.png`
- 工具／供應商：內建 image_gen／OpenAI；生成 1 次；確切模型與費用未知。
- 驗證：PNG 1672×941 RGB 完整解碼，來源與交付複本 SHA256 一致。四椅兩桌及空景成立；較參考圖光影更強、更暖，桌腳轉木色，前桌下緣底座露出增加，植物葉叢較茂密、遠樓細節增加。非像素級幾何一致；待使用者評鑑，未改採用或追加生成。

### 完整實際 prompt

```text
請編輯圖 1，將這張 Blender 空景提升為高質感 3D 動畫電影場景，參考圖 2 的材質、色彩、光影與氣氛。
圖 1 cam_twoshot_wide_level_empty_blender.png 是唯一的取景、透視、物件配置與遮擋依據。
圖 2 Cafe_2.png 僅供美術表現參考，不移植其構圖、家具排列、植物配置或人物。
色彩與光影採用圖 2 的米灰布料、暖米白桌面、柔和珊瑚橘靠墊、自然綠葉、淡青藍玻璃窗景與溫柔暖日光，整體舒適、精緻，柔和明暗與自然間接光。
【保留本機位】
維持圖 1 的16:9畫幅、觀看方向、消失點、主要結構與遮擋。
保留本鏡可見窗格、立柱、地面邊界、四張扶手椅、兩張圓桌、設備及植物的位置、數量、尺度與主要輪廓。
不旋轉相機、不鏡像、不拉遠或拉近，不移植參考圖中本鏡畫外的物件。
不為了展示完整物件而補出被裁切部分。
【材質與細節提升】
沿用圖 1 的構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。
四張扶手椅使用參考圖的米灰色細織布料，既有靠墊使用柔和珊瑚橘；維持椅子原本輪廓與靠墊數量。圓桌採暖米白霧面桌面、細緻暖木色邊緣；咖啡杯碟採暖奶油米色陶瓷。前桌原有閉合書本、筆、攤開書本與單杯碟的擺位尺寸保持不變，後桌保留小盆栽與書冊。地板為低反光暖淺灰，窗框為淺暖灰，右側既有設備呈低調米白表面，不增加配件。
植物保留圖 1 種類、位置與主要枝幹，在原有體積內細化薄葉與透光，不新增植物。
玻璃呈淡青藍透明質感與自然反射，保持既有窗外建築的形體與排列，材質細化且遠景低對比。
維持合理紋理尺度與細節密度，避免球塊狀植物、平塗玻璃與塑膠感。
表面乾燥、布料與地板霧面，不無故增加鏡面反光或髒污。
保留近中景可用資訊，作為後續加入人物的背景母圖，不額外強化散景，不複製圖 2 的人物或強烈背景模糊。
【本鏡畫面】
本鏡為咖啡廳靠窗座位區的平視廣角空景。前景左右各一張大扶手椅，前圓桌位於下方中央並被畫框截去部分底座；中景左右各一張扶手椅，中間一張較小圓桌；大面積落地窗與窗外城市建築位於後方。左側高植物、兩側較低植物、後桌小盆栽與右緣被裁切設備皆依圖 1 原位保留。精確維持前後兩組座位的大小關係、桌椅重疊及窗框位置。
【空景與輸出】
零人物：不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。
只輸出一張16:9高解析度完整圖片，不製作拼貼或九宮格，不加字幕、標誌或水印。
```



## 2026-10-21 staff_office 四機位夜景 GPT v3（待評鑑）
依使用者確認改用empty_blender，重複ms_15deg僅一次；monitor沿用既有v3。工具：內建image_gen／OpenAI，確切模型與費用未知，每機位生成一次。四張皆1672×941 RGB PNG，完整解碼與來源複本SHA256一致，目視零人物及夜景成立，非像素級幾何一致。保留舊版，未重試、未改採用或Blender。

### cam_amy_ms_45deg
- 輸出：references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_gpt_v3.png
- 有序輸入：1. references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_blender.png；2. clp/loc_staff_office_night_v4.png。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-f2e696d0-5022-4591-92bf-d9087d405a1d.png
- 觀察：45度中景配置及鍵盤保留，植物葉片與書本細節變化。
完整 prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套美術的夜間背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切與物件配置；圖2 loc_staff_office_night_v4.png 只提供同一場景的材質、色彩、光影與氣氛。不要採用圖2的廣角、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2低照度但家具仍可辨的夜間辦公室：有限的柔和暖色室內頂光、窗外深藍城市夜色和稀疏窗燈。保持其亮度層次，不額外增亮、壓黑、提高飽和度或泛光。消除底圖白天光照，不新增檯燈或畫外光源造成的強光斑。依本機位方向給出合理受光與陰影，不照搬參考圖的畫面座標投影。
【保留本機位】
維持圖1的16:9畫幅、主要結構、遮擋、門窗分格、立柱、窗框百葉、地面邊界、桌椅、設備、書本及植物的位置、數量、尺度和主要輪廓。不旋轉、鏡像、拉遠、推近，不增添物件，不補出畫外或被遮住的部分。
【材質與細節】
青綠隔板呈細緻布紋，米白框架柔和低光澤，黑灰設備霧面，椅背為細密網布，桌面為淺木紋，書櫃與地毯依參考圖。改善細微倒角高光、接縫與接觸陰影，不重新設計造型。保持乾淨乾燥，不加髒污、強烈鏡面或塑膠感；紋理不要過粗過強。可見植物只在既有輪廓體積內細化葉片，不新增盆栽或枝葉群。螢幕保持原有黑色空白外觀，不新增文字或介面。作為後續加入人物的背景母圖，不額外強化散景。
【空景與輸出】
零人物，不出現主角、同仁、人體、手臂、人形剪影或人物倒影。只輸出一張16:9高解析度完整彩色圖，不拼貼，不加字幕、標誌、水印。
【本鏡畫面】
圖1為 cam_amy_ms_45deg_empty_blender.png。45度微俯工位中景：左前景大螢幕背面、下方木桌與鍵盤、中央偏右網背椅及扶手、右下四本立書；保留右側狹窄地板、背景隔板交叉線、左側高盆栽與後方書櫃。
```

### cam_amy_cu_emotion
- 輸出：references/scenes/staff_office/cameras/cam_amy_cu_emotion_empty_gpt_v3.png
- 有序輸入：1. references/scenes/staff_office/cameras/cam_amy_cu_emotion_empty_blender.png；2. clp/loc_staff_office_night_v4.png。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-832cdc6f-5257-437c-890f-0af97f92a9f4.png
- 觀察：緊特寫保留，隔板花紋較強，百葉片數／細節變化。
完整 prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套美術的夜間背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切與物件配置；圖2 loc_staff_office_night_v4.png 只提供同一場景的材質、色彩、光影與氣氛。不要採用圖2的廣角、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2低照度但家具仍可辨的夜間辦公室：有限的柔和暖色室內頂光、窗外深藍城市夜色和稀疏窗燈。保持其亮度層次，不額外增亮、壓黑、提高飽和度或泛光。消除底圖白天光照，不新增檯燈或畫外光源造成的強光斑。依本機位方向給出合理受光與陰影，不照搬參考圖的畫面座標投影。
【保留本機位】
維持圖1的16:9畫幅、主要結構、遮擋、門窗分格、立柱、窗框百葉、地面邊界、桌椅、設備、書本及植物的位置、數量、尺度和主要輪廓。不旋轉、鏡像、拉遠、推近，不增添物件，不補出畫外或被遮住的部分。
【材質與細節】
青綠隔板呈細緻布紋，米白框架柔和低光澤，黑灰設備霧面，椅背為細密網布，桌面為淺木紋，書櫃與地毯依參考圖。改善細微倒角高光、接縫與接觸陰影，不重新設計造型。保持乾淨乾燥，不加髒污、強烈鏡面或塑膠感；紋理不要過粗過強。可見植物只在既有輪廓體積內細化葉片，不新增盆栽或枝葉群。螢幕保持原有黑色空白外觀，不新增文字或介面。作為後續加入人物的背景母圖，不額外強化散景。
【空景與輸出】
零人物，不出現主角、同仁、人體、手臂、人形剪影或人物倒影。只輸出一張16:9高解析度完整彩色圖，不拼貼，不加字幕、標誌、水印。
【本鏡畫面】
圖1為 cam_amy_cu_emotion_empty_blender.png。緊特寫空景：下緣只露網背椅頂部，右中景兩片螢幕背面，左側局部椅背與立書，上半部百葉窗和中間立柱，右後書櫃。保持緊裁切，不補出座椅全貌或桌面。
```

### cam_amy_mcu_15deg
- 輸出：references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_gpt_v3.png
- 有序輸入：1. references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_blender.png；2. clp/loc_staff_office_night_v4.png。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-c397b56b-db03-430d-8e7d-e33356cf5442.png
- 觀察：中特寫配置保留，右緣植物葉片輪廓改變，百葉與窗外細節變化。
完整 prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套美術的夜間背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切與物件配置；圖2 loc_staff_office_night_v4.png 只提供同一場景的材質、色彩、光影與氣氛。不要採用圖2的廣角、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2低照度但家具仍可辨的夜間辦公室：有限的柔和暖色室內頂光、窗外深藍城市夜色和稀疏窗燈。保持其亮度層次，不額外增亮、壓黑、提高飽和度或泛光。消除底圖白天光照，不新增檯燈或畫外光源造成的強光斑。依本機位方向給出合理受光與陰影，不照搬參考圖的畫面座標投影。
【保留本機位】
維持圖1的16:9畫幅、主要結構、遮擋、門窗分格、立柱、窗框百葉、地面邊界、桌椅、設備、書本及植物的位置、數量、尺度和主要輪廓。不旋轉、鏡像、拉遠、推近，不增添物件，不補出畫外或被遮住的部分。
【材質與細節】
青綠隔板呈細緻布紋，米白框架柔和低光澤，黑灰設備霧面，椅背為細密網布，桌面為淺木紋，書櫃與地毯依參考圖。改善細微倒角高光、接縫與接觸陰影，不重新設計造型。保持乾淨乾燥，不加髒污、強烈鏡面或塑膠感；紋理不要過粗過強。可見植物只在既有輪廓體積內細化葉片，不新增盆栽或枝葉群。螢幕保持原有黑色空白外觀，不新增文字或介面。作為後續加入人物的背景母圖，不額外強化散景。
【空景與輸出】
零人物，不出現主角、同仁、人體、手臂、人形剪影或人物倒影。只輸出一張16:9高解析度完整彩色圖，不拼貼，不加字幕、標誌、水印。
【本鏡畫面】
圖1為 cam_amy_mcu_15deg_empty_blender.png。中特寫空景：中央下半部網背椅被畫框裁切，左下局部螢幕，右側邊緣盆栽，後方螢幕與書櫃。保留椅背頂線高度與隔板斜線，不放大可見範圍。
```

### cam_amy_ms_15deg
- 輸出：references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v3.png
- 有序輸入：1. references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_blender.png；2. clp/loc_staff_office_night_v4.png。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-f8c199a9-c2b4-4c5d-a152-621ebf1c307d.png
- 觀察：中景配置保留，前景椅網較暗，百葉與窗外細節變化。
完整 prompt：
```text
請編輯圖1，將本機位Blender空景轉成與圖2同一套美術的夜間背景。圖1唯一決定相機位置、觀看方向、透視、構圖、裁切與物件配置；圖2 loc_staff_office_night_v4.png 只提供同一場景的材質、色彩、光影與氣氛。不要採用圖2的廣角、消失點、物件排列或可見範圍，不要重新生成圖2。
匹配圖2低照度但家具仍可辨的夜間辦公室：有限的柔和暖色室內頂光、窗外深藍城市夜色和稀疏窗燈。保持其亮度層次，不額外增亮、壓黑、提高飽和度或泛光。消除底圖白天光照，不新增檯燈或畫外光源造成的強光斑。依本機位方向給出合理受光與陰影，不照搬參考圖的畫面座標投影。
【保留本機位】
維持圖1的16:9畫幅、主要結構、遮擋、門窗分格、立柱、窗框百葉、地面邊界、桌椅、設備、書本及植物的位置、數量、尺度和主要輪廓。不旋轉、鏡像、拉遠、推近，不增添物件，不補出畫外或被遮住的部分。
【材質與細節】
青綠隔板呈細緻布紋，米白框架柔和低光澤，黑灰設備霧面，椅背為細密網布，桌面為淺木紋，書櫃與地毯依參考圖。改善細微倒角高光、接縫與接觸陰影，不重新設計造型。保持乾淨乾燥，不加髒污、強烈鏡面或塑膠感；紋理不要過粗過強。可見植物只在既有輪廓體積內細化葉片，不新增盆栽或枝葉群。螢幕保持原有黑色空白外觀，不新增文字或介面。作為後續加入人物的背景母圖，不額外強化散景。
【空景與輸出】
零人物，不出現主角、同仁、人體、手臂、人形剪影或人物倒影。只輸出一張16:9高解析度完整彩色圖，不拼貼，不加字幕、標誌、水印。
【本鏡畫面】
圖1為 cam_amy_ms_15deg_empty_blender.png。15度中景空景：中央偏右網背椅、左下前景螢幕、右側盆栽與立書，後方多排隔板螢幕與窗下書櫃；維持椅背大小、各物件遮擋與底部裁切。
```



## 2026-10-21 shot_3.8.3 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.3_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：雙人中景、吐舌、微笑與三名路人呈現；兩人間距縮短，人物尺度、頭頂留白與背景遮擋偏離 blocks，路人朝向改變。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_ms_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_ms_level_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 左側紅色人物。
圖 4 char_george.png：George 人物參考，對應圖 2 右側藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物位置、大小比例、身高差、間距與裁切。將紅色人物替換為圖 3 的 Amy，藍色人物替換為圖 4 的 George；人物圖只提供外觀與服裝，不採用展示姿態。
背景三名可見灰色人物替換為一般通勤路人，保留位置、比例與遮擋，不複製主角外觀。
場景材質、風格與溫暖日光採用圖 1，不改變圖 2 的空間配置。

畫面描述：
眼高平視的雙人中景，Amy 在左、George 在右，大腿以上同框，維持並肩朝鏡頭方向行走的姿態。
Amy 看向畫右的 George，眉毛略抬，帶著被識破心思的不好意思笑意，舌尖剛微微露出，捕捉俏皮吐舌的起始瞬間。左前臂沿用底圖的微抬位置，手掌自然放鬆，右手低放。
George 轉頭看向 Amy，露出溫暖、帶點會心的微笑，雙臂自然低放。兩人不看鏡頭。
保持中等景深與開闊街景。除表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.4 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.4_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：單人溫和微笑、嘴唇略張、雙手畫外呈現；視線偏左上、頭部側傾，人物位置與肩膀輪廓偏離 blocks。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、頭部大小、肩膀位置、頭頂留白與胸部裁切。
將藍色人物替換為圖 3 的 George，外觀與服裝依人物參考，不採用展示姿態。
場景材質、風格與光影採用圖 1，空間配置沿用圖 2。

畫面描述：
眼高平視、斜側中近景，George 頭部、雙肩與胸部入鏡，雙手位於畫外。
他維持輕鬆行走的上身姿態，臉部轉向畫左鏡外的 Amy，下巴輕輕收低，呈現開始點頭詢問的瞬間。眉眼放鬆，嘴角帶著溫和微笑，嘴唇略張，神情專注而願意傾聽。
視線落在 Amy 的臉部高度，不看鏡頭、不望向天空。畫面只出現 George，不加入 Amy 或書本。
淺景深聚焦眼睛與面部，背景玻璃門、石柱與植栽柔和失焦。除上述表演外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.5 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.5_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：嘆氣無奈表情、左手掌朝上與一名路人呈現；人物頭部放大、頭頂留白減少，左手伸出較多、路人姿態與背景細節重繪。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物尺度、頭頂留白、胸部裁切與背景配置。
將紅色人物替換為圖 3 的 Amy，人物圖只提供外觀與服裝。
右後方灰色人物替換為一名穿通勤服裝的遠景路人，保留位置與模糊程度。
場景材質、風格與溫暖日光採用圖 1。允許依本鏡表演略微放低 Amy 雙肩，其餘人物佔位不變。

畫面描述：
眼高平視、斜側中近景，Amy 胸部以上入鏡，左前臂微抬。
捕捉她開始重重嘆氣的瞬間：雙肩鬆垮下沉，眉心微皺，上眼瞼略垂，嘴唇張開吐氣，神情無奈疲憊，沒有笑容。
頭部與視線朝向畫右鏡外 George，左手維持低位、掌心略朝上，像準備向他倒苦水；右手留在畫外。
前景只有 Amy，背景保留一名路人，不加入 George。淺景深聚焦 Amy，背景玻璃帷幕柔和失焦。除肩膀與表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.6 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.6_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：開朗笑容與胸前雙掌相對、尚未接觸呈現；視線偏左上，人物尺度及肩膀輪廓偏離 blocks。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物位置、頭部尺度、肩膀位置與胸部裁切。
將藍色人物替換為圖 3 的 George，人物外觀與服裝依參考圖。
場景材質、風格與溫暖日光採用圖 1，空間配置不變。
本鏡允許調整雙臂與雙手，將雙手抬到胸前拍手起始位置，不因此拉遠鏡頭或縮小人物。

畫面描述：
George 單人斜側中近景，胸部以上入鏡。他看向畫左鏡外的 Amy，眉毛輕揚，雙眼帶著鼓勵的笑意，嘴角明顯上揚，嘴唇微張。
雙手抬到胸前，兩掌相對、尚未接觸，捕捉準備輕拍雙手恭喜她的瞬間。手勢位於下巴以下，不遮住臉部或領帶上端。
他的神情開朗真誠，像認為這是難得的職涯機會，不呈現同情、挖苦或誇張狂笑。
畫面只出現 George；淺景深聚焦面部，雙手仍可辨識。除手勢與表情外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.7 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.7_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：Amy 抱頭焦慮、George 右前景過肩呈現；Amy 視線偏右上、頭頂留白減少，軀幹朝向與人物尺度、前景遮擋偏離 blocks。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_ots_george_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_ots_george_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_amy_ots_george_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 左中景紅色人物。
圖 4 char_george.png：George 人物參考，對應圖 2 右前景藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留過肩取景、透視、兩人大小比例、位置與遮擋。
紅色人物替換為圖 3 的 Amy，藍色人物替換為圖 4 的 George；人物圖只提供外觀與服裝。
George 僅呈現底圖可見的後腦、肩頸與上身局部，不轉成正臉。
場景材質、風格與光影採用圖 1。允許 Amy 改變雙臂姿態以呈現抱頭動作，不移動她的軀幹位置。

畫面描述：
越過右前景 George 肩膀拍攝左中景 Amy 的過肩鏡，畫面共兩人。
Amy 雙手剛抬到頭部兩側，指尖輕觸太陽穴附近的頭髮，手肘自然向外，雙手不遮住眼睛與嘴巴。
她眉頭緊皺、眉心抬起，眼睛帶著焦慮，嘴巴張開，呈現剛開始抱頭訴苦的瞬間。視線朝向右前景 George，神情像擔心自己無法說服同事改變習慣。
George 保持耐心聆聽的朝向，前景輪廓與遮擋沿用底圖。對焦 Amy，George 前景與玻璃帷幕背景柔和失焦。
除 Amy 的雙臂、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```



## 2026-10-21 shot_3.8.8 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.8_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：Amy 左前景後腦、George 右側微笑呈現；George 視線較靠近鏡頭，手臂及胸部可見範圍改變，人物尺度與背景遮擋偏離 blocks。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_ots_amy_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_ots_amy_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_ots_amy_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 左前景紅色人物。
圖 4 char_george.png：George 人物參考，對應圖 2 右中景藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留過肩取景、透視、人物尺度、位置、可見部位與遮擋。
紅色人物替換為圖 3 的 Amy，藍色人物替換為圖 4 的 George。人物圖只提供外觀與服裝。
Amy 僅呈現底圖可見的後腦與肩部，不補出正面表情。
場景材質、風格與溫暖日光採用圖 1，空間配置沿用圖 2。

畫面描述：
越過左前景 Amy 肩膀拍攝右中景 George 的過肩鏡，畫面共兩人。
George 臉部與視線朝向左前景 Amy，眉眼舒展，嘴角帶著篤定、略有幽默感的微笑，嘴唇微張，捕捉開始安慰她的瞬間。
他的神情平靜而有把握，像相信 Amy 的機靈足以讓她找到方法；不做嘲諷或誇張大笑。手臂維持底圖位置，不新增指點或拍肩動作。
對焦 George 的雙眼與面部，Amy 前景柔和失焦，背景玻璃門與石柱保留可辨識的輪廓。
除 George 表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.9 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.9_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：合十、懇求表情與一名路人呈現；頭部明顯放大、頭頂留白減少、視線偏右上，手指頂端接近下巴，路人朝向與背景細節重繪。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物尺度、頭頂留白與胸部裁切。
紅色人物替換為圖 3 的 Amy。右後方灰色人物替換為一名通勤路人，保留位置與模糊程度。
場景材質、風格與光影採用圖 1。
允許將 Amy 雙臂改為胸前合十姿態，其餘身體位置不變，不拉遠鏡頭。

畫面描述：
Amy 斜側中近景，胸部以上入鏡。她雙手在胸前剛合攏，手指自然朝上，手掌位於下巴以下，不遮住臉。
頭部與視線朝向畫右鏡外的 George，內側眉毛微抬，眼眶有輕微水光但沒有淚滴，嘴唇略張，露出撒嬌又急切的懇求神情，像準備請他認真給建議。
不要呈現大哭或過度誇張的悲傷。前景只有 Amy，背景保留一名路人，不加入 George。
淺景深聚焦 Amy 的眼睛與合十手勢。除手勢、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.10 GPT 生成失敗（未出圖）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 錯誤：HTTP 400 moderation_blocked，moderation_stage=output，categories=[other]，request ID 558746ad-22c9-4d0a-ae88-518deff22548。未取得圖片；未重試或修改 prompt。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_cu_emotion_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_cu_emotion_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留頭肩特寫、透視、頭部大小、頭頂留白、肩膀與畫面下緣裁切。
將藍色人物替換為圖 3 的 George，不採用人物參考圖的展示姿態。
場景材質、風格與溫暖日光採用圖 1，不改變圖 2 的空間配置。

畫面描述：
George 單人頭肩情緒特寫，臉部略朝畫左，視線落在畫左鏡外 Amy 的臉上。
捕捉他剛輕笑、準備給出建議的瞬間：嘴角微揚，嘴唇略張，眼神溫暖而專注，笑意克制，帶著即將認真說明的沉穩感。
雙手仍在畫外，不提前加入豎起食指的動作。頭部自然直立，不仰頭、不看鏡頭。
淺景深聚焦眼睛、眉毛與嘴角，背景石柱與玻璃門柔和失焦。除表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不生成「變革關鍵：人」或其他字幕、文字、浮水印。
```


## 2026-10-21 shot_3.8.11 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.11_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：頭肩特寫、微歪頭疑惑、雙手畫外與一名路人呈現；視線偏右上，頭部輪廓與肩膀位置偏離 blocks，路人及背景細節重繪。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_cu_emotion_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_cu_emotion_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留頭肩特寫、透視、人物尺度、留白與裁切。
將紅色人物替換為圖 3 的 Amy。
右後方灰色人物替換為一名遠景通勤路人，維持位置、比例與柔焦。
場景材質、風格與溫暖日光採用圖 1，不改變空間配置。

畫面描述：
Amy 頭肩情緒特寫，雙手在畫外。她剛聽到關鍵字而微微一怔，下巴略抬，頭部只有輕微側傾。
視線朝畫右鏡外 George 的臉，眉毛微抬，眉心帶一點疑惑，雙眼專注而好奇，嘴唇輕輕分開，捕捉準備反問「人？」的瞬間。
表情是從焦慮轉向思索，不是驚恐或興奮大笑；視線不飄向天空。
前景只有 Amy，背景保留一名路人。淺景深聚焦雙眼，保留原有頭頂留白。除頭部微小姿態與表情外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.12 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.12_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：雙人中景、Amy 放低雙手、George 雙掌相對尚未交扣呈現；背景可見四名路人而非三名，兩人間距縮短、人物比例與留白偏離 blocks。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_ms_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_ms_level_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 左側紅色人物。
圖 4 char_george.png：George 人物參考，對應圖 2 右側藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、兩人尺度、身高差、間距與大腿裁切。
將紅色人物替換為 Amy，藍色人物替換為 George，外觀與服裝分別採用圖 3、圖 4。
背景三名可見灰色人物替換為通勤路人，維持原有位置與遮擋。
場景材質、風格與溫暖日光採用圖 1。允許調整雙方手臂以呈現本鏡表演，軀幹位置不變。

畫面描述：
眼高平視雙人中景，Amy 左、George 右，並肩朝鏡頭方向行走。
George 看向 Amy，下巴微收，露出肯定、循循善誘的微笑。雙手抬到胸前，掌心相對，指尖接近但尚未交扣，呈現準備以交扣手勢說明「緊緊相連」的起始狀態。
Amy 的左手由底圖抬起位置放低，雙臂自然放鬆，轉頭專注看著 George，眉眼平靜、嘴唇輕合，呈現認真吸收建議的神情。
兩人不看鏡頭，保留中等景深與原有街景。除手臂、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```



## 2026-10-21 shot_3.8.13 GPT 生成失敗（未出圖）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 錯誤：HTTP 400 moderation_blocked，moderation_stage=output，categories=[other]，request ID 907cfc2a-bc9a-458a-b0ac-acab2e3df96b。未取得圖片；未重試或修改 prompt。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物尺度、頭頂留白與胸部裁切。
將藍色人物替換為圖 3 的 George，場景材質、風格與溫暖日光採用圖 1。
允許調整雙臂與雙手，使手掌出現在胸前，不因手勢改變鏡頭遠近或軀幹位置。

畫面描述：
George 單人斜側中近景，胸部以上入鏡。他看向畫左鏡外 Amy，眼神明亮，眉毛略抬，嘴角帶著有信心的微笑，嘴唇微張，呈現正向鼓勵的神情。
雙肘彎曲，雙手在下胸前分開，兩掌朝上、手指自然舒展，停在準備往上托舉的起點，表達工作價值可以提升。雙手不遮住臉，不高舉過肩。
人物面部與手勢清楚，背景玻璃門、石柱與植栽柔和失焦。畫面只有 George，不加入 Amy。
除手勢、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.14 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.14_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：睜大眼與微張嘴、微抬左臂及一名路人呈現；視線偏右上，左手呈下垂圓握形、手指不清，人物頭部尺度及路人朝向偏離 blocks。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物位置、尺度、頭頂留白與胸部裁切。
紅色人物替換為圖 3 的 Amy，右後方灰色人物替換為一名遠景通勤路人，保留位置與柔焦。
場景材質、風格與光影採用圖 1。人物外觀與服裝依圖 3，不採用展示姿態。

畫面描述：
Amy 斜側中近景，肩胸以上入鏡，左前臂維持底圖的微抬位置，手掌自然放鬆，不增加新手勢。
捕捉她剛聽到「提升競爭力、讓工作更有價值」的瞬間：雙眼比原本睜大，眉頭舒展，眉毛微抬，嘴唇略張，神情好奇、若有所思，像正在重新理解 ESG 的意義。
頭部與視線朝畫右鏡外 George，不看鏡頭，尚未露出完全頓悟的大笑。
前景只有 Amy，背景保留一名路人。淺景深聚焦雙眼與面部。除表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.15 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.15_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：王大哥單人全身、迷彩背心與綠色供應鏈、金色箭頭勳章呈現；計算機抬至胸前而非腰部，背景多出一台計算機，大量單據與圖標較繁複、上方留白不足。未替換既有 HyperFrames 成果。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/clp/char_wang.jpeg`
2. `D:/kj-openMontage/projects/course-51-esg/clp/prop_calculator.png`

### 完整 prompt
```text
參考圖說明：
圖 1 char_wang.jpeg：採購主管王大哥（char_wang）人物外觀與服裝參考。
圖 2 prop_calculator.png：財務計算機（prop_calculator）外觀參考，只採用一台計算機，不生成三視圖排版。

畫面描述：
製作一張 Pixar 風格的 3D 概念敘事分鏡，呈現採購主管透過綠色供應鏈，從只被視為花成本的人，轉變為替公司創造價值的英雄。

畫面只有一位王大哥，居中全身入鏡，平視、35mm 鏡頭感，中等景深。外觀與服裝嚴格採用圖 1：灰黑短髮、頭頂稀疏、方形眼鏡、米色短袖襯衫、迷彩多口袋背心、卡其長褲與棕色鞋。不改穿針織背心，不加披風、盔甲或超級英雄制服。

王大哥站姿穩定、挺胸，臉上露出自信而踏實的微笑，眼神朝向觀眾。左手在腰部附近托著圖 2 的計算機，機身略朝鏡頭，保留深灰黑色外殼、紅色數字顯示與按鍵外觀；右手自然放鬆。

場景為抽象的概念劇場。畫面左側以低彩度灰色帳房氛圍與少量成本單據象徵舊有印象；右側以翠綠色連線串接工廠、運輸與葉片圖標，形成清晰但不繁雜的綠色供應鏈網絡，搭配金色向上箭頭與一枚發光價值勳章圖標。
王大哥位於兩種氛圍交界，主要接受右側綠金色榮耀光線，臉部仍保持自然膚色。勳章與箭頭位於背景，不遮住人物、手部或計算機。

這是同一空間中的單張定格，不做前後對照雙人複製、不做漫畫分格。George 僅為後續畫外音，不出現在圖片中。
保留畫面上方適量乾淨空間供後製標題使用。

輸出一張 16:9 彩色分鏡圖，不生成標題、字幕、說明文字或浮水印。
```


## 2026-10-21 shot_3.8.16 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.16_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：右手托下巴、微張嘴與一名路人呈現；視線偏右上、微笑較明顯，頭頂留白與人物尺度偏離 blocks，路人姿態重繪。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_amy_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、人物尺度、頭頂留白與胸部裁切。
紅色人物替換為圖 3 的 Amy。右後方灰色人物替換為一名遠景通勤路人，維持位置與柔焦。
場景材質、風格與溫暖日光採用圖 1。
允許調整 Amy 雙臂：右手抬起輕托下巴，左手放低，不改變軀幹位置或鏡頭遠近。

畫面描述：
Amy 斜側中近景，胸部以上入鏡。她右手指節輕托下巴下方，手指不遮住嘴唇，左手放低至畫外。
下巴略收，捕捉開始輕輕點頭的瞬間。她看向畫右鏡外 George，眉心只有輕微思索感，雙眼專注，嘴唇略張，像正在確認自己剛理解的方向。
表情比先前平靜，帶著逐漸抓到重點的認真與期待，不做誇張頓悟或大笑。
前景只有 Amy，背景保留一名路人。淺景深聚焦面部與托下巴的右手。除手勢、表情與視線外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```


## 2026-10-21 shot_3.8.17 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；本鏡 1 次提交，未重試。
- 圖片：`assets/images/shot_3.8.17_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：雙人全身步行、彼此微笑及玻璃反射呈現；人物放大並移向畫左，步態、手臂與腳底位置偏離 blocks，相鄰雙手接近重疊，尚未拍肩。
- 未更新正式採用 manifest。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_mws_profile_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_twoshot_mws_profile_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_twoshot_mws_profile_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_twoshot_mws_profile_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考，對應圖 2 左前景紅色人物。
圖 4 char_george.png：George 人物參考，對應圖 2 右後側藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留側面取景、透視、人物位置、大小比例、前後關係、間距、腳底位置與全身構圖。
將紅色人物替換為圖 3 的 Amy，藍色人物替換為圖 4 的 George；人物圖只提供外觀與服裝。
場景材質、風格與金暖日光採用圖 1，不改變圖 2 的空間配置。
玻璃內若保留人物反射，須對應替換後角色與原有反射位置，不保留紅藍方塊人影。

畫面描述：
眼高平視的雙人側面中廣景，Amy 在左前景、George 在右後側，兩人全身與鞋子完整入鏡，沿商辦大樓前人行道朝畫右前方邁步。
維持圖 2 的跨步姿態與軀幹朝向。Amy 頭部略轉向 George，眼神專注，嘴角浮現輕微而有信心的笑意，帶著重新獲得方向的期待。
George 溫暖地看向 Amy，嘴唇略張，露出信任、鼓勵的微笑，捕捉開始叮囑她尋找「小勝利」的瞬間。雙手沿用底圖的自然行走位置，尚未伸手拍肩。
畫面只有兩位主角及其合理反射，不新增路人。保持中等景深與開闊留白，陽光方向、地面接觸陰影和玻璃反射彼此一致。
除表情與視線外，其餘沿用圖 2，不放大人物、不拉近鏡頭。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或浮水印。
```



## 2026-10-21 cafe 全景 cam_room_wide_overview GPT v1
- 工具：內建 image_gen／OpenAI；模型版本、預估及實際費用：未知；單次生成1張。
- 有序輸入：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_room_wide_overview_empty_blender.png（唯一編輯底圖）
  2. D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/cafe/Cafe_2.png（美術參考；使用者路徑缺反斜線，已定位原檔）
- 輸出：references/scenes/cafe/cameras/cam_room_wide_overview_empty_gpt.png
- 觀察：零人物、四椅兩桌、茶水台及三回收桶保留；光影比參考偏暖偏強，層架新增／細化垂吊葉與杯罐，桌面書冊簡化、前桌杯碟細節改變，天花通風口與部分裁切偏移，非精確幾何一致。待使用者評鑑；未重試或更新採用。
- 驗證：PNG完整解碼、1672×941 RGB，複本SHA256一致。

### 完整實際 prompt
```text
請編輯圖 1，將這張 Blender 空景提升為高質感 Pixar 風格 3D 動畫電影室內背景，參考圖 2 的材質、色彩、光影與氣氛。
圖 1 cam_room_wide_overview_empty_blender.png 是唯一的取景、透視、物件配置與遮擋依據。
圖 2 Cafe_2.png 僅供美術表現參考，不移植其構圖、建築／家具排列、植物配置或人物。
色彩與光影採用圖2的灰米色布藝、珊瑚橘抱枕、奶油色圓桌與細緻木質邊緣、自然綠葉、淡青灰玻璃與窗外城市，以及柔和溫暖日光搭配清爽冷色窗光；不加重金黃濾鏡、泛光或飽和度。參考圖未顯示的茶水台沿用底圖造型，以協調的暖白霧面櫃體與淺色檯面處理。
【保留本機位】
維持圖1的16:9畫幅、高位廣角觀看方向、消失點、主要結構與遮擋。
保留本鏡可見門窗分格、立柱、門把、天花板燈帶與通風口、地面邊界、家具、設備及植物的位置、數量、尺度與主要輪廓。
不旋轉相機、不鏡像、不拉遠或拉近，不移植參考圖中本鏡畫外的物件。
不為展示完整物件而補出被裁切部分，左下吧檯與高腳椅、右下沙發仍按圖1裁切。
【材質與細節提升】
沿用圖1構造與物件種類，改善布料微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與玻璃反射。
四張扶手椅及前景局部沙發維持原輪廓與尺寸，呈現圖2灰米色織布；既有抱枕呈珊瑚色。兩張圓桌呈奶油色霧面桌面，保留底圖桌腳幾何。已有杯碟呈暖米色陶瓷，不增加杯子或道具。
植物保留種類、位置與主要枝幹，在原有體積內細化薄葉和透光，不新增植物，不擴大葉叢。
保持乾燥霧面室內表面、合理紋理尺度與細節密度，避免塑膠質感、過強鏡面反光或髒污。
作為後續加入人物的背景母圖，近中遠景保持可用清晰度，不移植圖2的強散景。
【本鏡畫面】
本鏡從休息室左前方高位斜看室內，左及後方為落地窗和城市高樓，中央四張扶手椅分成前後兩組，各圍一張小圓桌；後右側為冰箱、吊櫃、層架、檯面、水槽、微波爐、咖啡機等茶水設備，右側有三個回收桶。左下角裁切吧檯與高腳椅，右下角裁切前牆沙發，最右側保留門及牆面。保留此一廣角空間關係、家具重疊、前後桌大小和位置，不把場景改成圖2的平視雙人近景。
【空景與輸出】
零人物：不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。不要帶入圖2的兩位人物。
只輸出一張16:9高解析度完整圖片，不製作拼貼或九宮格，不加字幕、標誌或水印。
```



## 2026-10-21 shot_3.9.1 GPT v1（草案螢幕，待評鑑）
- 輸出：assets/images/shot_3.9.1_gpt_v1.png（1672×941 RGB PNG）。內建image_gen／OpenAI，模型與費用未知，生成一次，未改採用。
- 唯一輸入：references/scenes/staff_office/cameras/cam_monitor_insert_front_empty_gpt_v3.png。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-3dbc5ada-4722-493f-857b-0f07f6390ca5.png
- 驗證：完整解碼／來源複本SHA256一致。目視標題《ESG 推動管理辦法與獎懲細則草案》正確、正文空白及游標成立；螢幕構圖與夜景保留，工具列較繁複、標題較大，尺規數字不規則。未重試。

完整 prompt：
```text
以參考圖 cam_monitor_insert_front_empty_gpt_v3.png 為唯一編輯底圖，只修改螢幕內部顯示內容及螢幕亮起造成的微弱鄰近補光。

保留原圖的相機角度、透視、螢幕大小與位置、外框厚度、畫面裁切、下方銀灰邊條、局部木桌、青綠隔板、窗框百葉與窗外夜景。不拉遠、不推近、不鏡像，不補出鍵盤或其他畫外物件。

將原本黑色的螢幕顯示區改成開啟中的 Word 文件編輯畫面。介面簡潔，上方保留低調的工具列，中央顯示白色文件頁面。整個介面必須貼合原螢幕顯示區的四角與透視，不能超出邊框，也不能變成浮在畫面上的平面字卡。

文件上方清楚顯示以下繁體中文標題，逐字正確：
《ESG 推動管理辦法與獎懲細則草案》

標題採端正、正式的黑色字體，大小適合閱讀，完整落在頁面範圍內。標題下方的正文完全空白，只在第一個正文段落的行首顯示一條細直文字輸入游標，呈現尚未寫出內容、停滯不前的瞬間。沒有其他段落、表格、圖表、插圖、選取反白、彈出視窗或錯誤訊息。

螢幕發出柔和的冷白光，白色頁面保持可讀、不過曝；只在鄰近螢幕邊框與桌面產生微弱、合理的冷色補光。維持原圖深夜辦公室的低照度、暖色室內微光與深藍窗外夜色，不把整間辦公室照亮，也不新增檯燈。

畫面沒有任何人物、手部或人物倒影。整體安靜、停滯，讓正式冗長的標題與大片空白正文形成對比。

輸出一張16:9彩色分鏡圖，保留原圖3D動畫場景質感。除螢幕內必要的文件介面與指定標題外，不加入字幕、旁白文字、圖示特效或浮水印。
```



## 2026-10-21 shot_3.8.10 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知。本輪 1 次提交。
- 圖片：`assets/images/shot_3.8.10_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 核對通過。
- 目視：George 單人頭肩、微笑微張嘴及雙手畫外呈現；視線偏左上，肩膀較窄、頭肩比例與背景遮擋偏離 blocks，背景細節重繪。待使用者評鑑，未改正式採用。
- 參考圖依序：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_cu_emotion_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_cu_emotion_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色衣身定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭部大小、頭頂留白、肩膀位置、顯示範圍與遮擋關係。

將定位人物替換為圖 3 的 George，只呈現圖 2 中可見的頭部、肩膀與上胸，不補出畫外身體。人物五官、灰白髮型、棕色眼鏡、短鬍鬚與服裝採用圖 3，不採用人物參考圖的展示姿態或構圖；不保留 blocks 的簡化五官與方塊外觀。

將場景的材質、風格與溫暖日光更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張平視、85mm 視角的 George 單人頭肩情緒特寫。George 位於畫面中央，頭部略朝畫左，肩膀與上胸延伸至畫面下緣，雙手位於畫外。畫面只有 George 一人，Amy 位於畫左鏡外。

捕捉 George 剛輕笑、準備開口給出建議的瞬間：嘴角輕微上揚，嘴唇自然微張，眉心放鬆，眼神溫暖、專注，帶著即將認真說明的沉穩感。頭部自然直立，下巴保持水平，雙眼看向畫左鏡外 Amy 的臉，視線不向上飄、不看鏡頭。雙手保持畫外，尚未抬手或豎起食指。

淺景深聚焦 George 的雙眼與面部表情，背景石材立柱、玻璃門與金屬門框柔和失焦。保留圖 2 的頭頂留白與人物比例，不放大頭部或重新裁切。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、字卡、對話框或浮水印。
```


## 2026-10-21 cafe 全景 GPT v2：冰箱手把與杯子局部修正
- 有序輸入（唯一編輯底圖）：references/scenes/cafe/cameras/cam_room_wide_overview_empty_gpt.png
- 輸出：references/scenes/cafe/cameras/cam_room_wide_overview_empty_gpt_v2.png
- 工具：內建 image_gen／OpenAI；模型、預估與實際費用未知，1次編輯。
- 目視：冰箱右側上下手把移除，靠窗左側上下手把保留；咖啡機右側改為三個分離直立杯，杯口及杯柄可辨。整體構圖與暖光保留，材質微紋理略有變化。PNG完整解碼／複本SHA256通過，1672×941 RGB。待使用者評鑑，未重試或改採用。
### 完整實際 prompt
```text
Edit this existing image with only two localized corrections. Preserve the exact camera, framing, image dimensions, furniture, architecture, colors, lighting, shadows and every other scene detail. (1) The stainless steel refrigerator near the back window incorrectly has handles on BOTH left and right edges. Remove ALL handles on the RIGHT edge of both upper freezer door and lower fridge door (the edge next to the kitchen counter). Reconstruct smooth uninterrupted stainless steel where those right handles were. Keep only the existing LEFT-edge handles on both doors, on the side nearest the window/plants. Preserve the horizontal separation between the two doors, and preserve the fridge size and shape. (2) On the countertop immediately to the RIGHT of the coffee machine, replace the warped merged cup cluster with three simple individual ivory ceramic mugs neatly standing upright side by side. Each mug must have a clean symmetrical cylindrical body, a circular open rim shown as a correct perspective ellipse, a flat base resting on the counter, and exactly one normal C-shaped handle attached to its own body. Separate mugs clearly with small gaps; no melted, fused, stacked or distorted cup forms. Keep this small group within the original cup cluster area. Do not change the coffee machine, the shelf cups above, or the cup on the foreground round table. No people or text. Output a single complete edited image, not a collage.
```



## 2026-10-21 shot_3.8.10 GPT v2 視線修正（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知；1 次編輯生成。
- 圖片：`assets/images/shot_3.8.10_gpt_v2.png`
- 唯一參考圖：`D:/kj-openMontage/projects/course-51-esg/assets/images/shot_3.8.10_gpt_v1.png`
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過。
- 目視：雙眼虹膜移向畫左，視線較水平；頭部角度、微笑、服裝與主要背景構圖保留，鬍鬚等細節有輕微重繪，非逐像素不變。保留 v1，未改正式採用。
### 完整 prompt
```text
局部編輯這張圖片。只修改 George 雙眼的虹膜與瞳孔位置，將目前朝畫面左上方的視線改為水平看向畫面左側、鏡外與他眼睛同高度的 Amy。雙眼協調地朝觀眾所見的左側看，虹膜與瞳孔在眼裂中的垂直位置自然居中，不上翻、不往上看，也不看鏡頭。維持原本眼皮形狀、眉毛、眼鏡、頭部角度、下巴高度、微笑與微張的嘴。不要加入 Amy。除必要的虹膜與瞳孔位置調整外，所有其他內容保持原樣：同一人物五官與身份、頭髮、鬍鬚、服裝、姿勢、人物大小與位置、畫面裁切、背景建築與玻璃反射、光影、色彩、景深及16:9比例均不變。不新增文字或物件。
```


## 2026-10-21 shot_3.9.2 GPT v1（夜間抓頭，待評鑑）
- 輸出：assets/images/shot_3.9.2_gpt_v1.png（1672×941 RGB PNG）；內建image_gen／OpenAI，確切模型與費用未知，生成一次，未改採用。
- 有序參考圖：1. references/scenes/staff_office/cameras/cam_amy_ms_45deg_empty_gpt_v3.png；2. references/scenes/staff_office/cameras/cam_amy_ms_45deg_block_blender.png；3. clp/char_amy.jpeg。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-07335045-45f6-4fec-be22-0a2b28e62623.png
- 驗證：完整解碼／來源複本SHA256一致。單人夜景、雙手接觸頭髮、煩躁望向螢幕成立；Amy頭部降低、軀幹前傾與原白模坐姿不同，表情較焦慮。未重試。
完整 prompt：
```text
參考圖說明：
圖1 cam_amy_ms_45deg_empty_gpt_v3.png：夜間場景外觀參考，提供材質、色彩、光影與氣氛。
圖2 cam_amy_ms_45deg_block_blender.png：構圖底圖，提供取景、透視、家具配置、人物位置、比例與遮擋。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的紅色定位人物。

生圖指引：
以圖2為編輯底圖，保留取景、透視、桌椅配置、人物佔位、頭部大小、頭頂留白及畫面裁切。不推近、不拉遠，不為呈現手勢而放大人物或移動家具。

將紅色定位人物替換為 Amy。五官、棕色微捲短髮、綠色眼睛、灰色西裝與米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。以自然人體比例替換簡化白模，不保留方塊外形、長方形脖子或紅色服裝。

將場景材質、色彩與光影更新為圖1的夜間外觀，保留圖2的空間配置。維持窗外深藍夜色、稀疏城市燈光與低照度暖色室內光。不要沿用圖2的白天亮度，不新增檯燈或其他道具。

畫面描述：
這是一張32mm、45度微側、略微俯視的工位中景。Amy 坐在圖2原有的黑色網背辦公椅上，位於畫面中央偏右。左側前景的大螢幕背面、桌上鍵盤、右下立書、椅子扶手與後方隔板的位置及遮擋沿用圖2。

Amy 正因寫不出管理辦法而感到疲憊、煩躁。她眉頭緊蹙，眼皮略顯沉重，嘴巴微張，呈現壓抑不住抱怨的瞬間。視線朝向左前方電腦螢幕，不看觀眾，也不露出笑容。

她雙肘彎曲、雙手抬至頭部兩側，手指自然張開並輕觸兩側髮根，停在即將煩躁抓亂頭髮的起始位置。手指結構自然，雙手不遮住眼睛與主要表情，不拉扯出誇張髮束。肩膀略微繃緊，軀幹仍保持坐在原位，尚未趴向桌面。除雙臂、手勢與指定表情外，其餘人物位置、比例與坐姿沿用圖2。

電腦顯示面朝向 Amy、背面朝向觀眾，不能把文件文字畫在螢幕背面。畫外可見不到的顯示面發出微弱冷白光，自然照亮 Amy 靠近螢幕的一側臉頰與手指；其餘夜間光影沿用圖1，不將整間辦公室照亮。

畫面只有 Amy 一位人物，其他工位與通道全部無人。中景深保留桌面與辦公室空間關係，背景較暗但仍可辨識。整體呈現深夜獨自加班、卡關又無奈的職場喜劇感。

這是一張動作起始畫面，只呈現雙手剛接觸頭髮的瞬間，不同時呈現抓頭與趴桌，不加入動作殘影、汗滴圖示或多重姿勢。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、對話框、文字、圖示或浮水印。
```



## 2026-10-21 cafe 全景 GPT v3：層板杯罐／紙杯／茶几杯耳
- 輸入（唯一底圖）：references/scenes/cafe/cameras/cam_room_wide_overview_empty_gpt_v2.png
- 輸出：references/scenes/cafe/cameras/cam_room_wide_overview_empty_gpt_v3.png
- 工具：內建 image_gen／OpenAI，單次編輯1張；模型與費用未知。
- 觀察：層板杯罐輪廓較規整，前茶几杯僅見右側單耳；微波爐和咖啡機間仍為兩柱狀白色物，紙杯重疊杯緣不明顯，未完整符合堆疊紙杯要求。後桌盆栽右側出現疑似多餘杯耳／淺色輪廓。保留v2，不重試，不改採用，待使用者評鑑。
- 驗證：PNG1672×941 RGB完整解碼、複本SHA256一致。
### 完整實際 prompt
```text
Edit the attached existing image with THREE localized corrections only. Preserve the exact wide camera, framing, architecture, furniture positions, plants, warm lighting and overall colors.
1. Rebuild the malformed coffee mugs and storage bottles/jars on BOTH wall shelves above the coffee machine. Keep the shelves and plants exactly in place. Each lower-shelf mug must be an individual clean ivory ceramic cylinder with a circular rim in correct perspective, flat base on the shelf, and exactly ONE normal C-shaped handle attached to that mug. No extra handles, fused vessels, warped silhouettes or melting forms. Upper-shelf bottles and canisters must be separate upright rotationally symmetric vessels with straight central axes, clean elliptical rims/lids, sensible necks, solid bases resting on the shelf, and visible small gaps between objects. Retain the same approximate object count, sizes, off-white palette and arrangement, without adding decorative objects.
2. On the COUNTERTOP in the gap BETWEEN the microwave on the left and coffee machine on the right, replace the existing tall misshapen containers with one neat vertical nested STACK OF WHITE DISPOSABLE PAPER CUPS. Show clearly repeated rolled circular rim bands along the top of the stack, tapered paper cup profile, open top cup, no handles, no lids, no straws, no text or logos. Stack rests upright on the countertop and fits within that existing gap. Keep microwave, coffee machine, and the three ceramic mugs to the RIGHT of the machine unchanged.
3. The coffee cup on the foreground central ROUND COFFEE TABLE has a malformed duplicate handle. Correct this cup to have EXACTLY ONE small C-shaped handle on its right side, with a smooth uninterrupted wall on its left side. Remove any second ear, extra loop or handle-like protrusion. Preserve the cup's existing position, size, color and coffee, with a clean elliptical rim and normal ceramic shape. If any other small-table coffee cup is visible, it too must have only one handle. Do not alter the small plant on the rear side table.
Keep the refrigerator's existing handles ONLY on its LEFT window-facing edge; do not add handles on its right edge. Zero people. Output one complete edited image with original aspect ratio, no collage or labels.
```



## 2026-10-21 shot_3.9.3 GPT v1（閉眼沉思，待評鑑）
- 輸出：assets/images/shot_3.9.3_gpt_v1.png（1672×941 RGB PNG）；內建image_gen／OpenAI，模型與費用未知，生成一次，未改採用。
- 有序輸入：1. references/scenes/staff_office/cameras/cam_amy_cu_emotion_empty_gpt_v3.png；2. references/scenes/staff_office/cameras/cam_amy_cu_emotion_block_blender.png；3. clp/char_amy.jpeg。
- 來源：C:/Users/servi/.codex/generated_images/01a15a6c-30e2-76e1-87ac-3f617a6eb6a8/exec-53644e81-9b60-479a-aee7-6c7e7bc8c53c.png
- 驗證：完整解碼／來源複本SHA256一致；閉眼閉口、輕微蹙眉、單人夜景成立，未出現George。相較白模面部佔比縮小、露出較多肩胸與衣領，頭頂留白略少，未完全符合緊裁切。未重試。
完整 prompt：
```text
參考圖說明：
圖1 cam_amy_cu_emotion_empty_gpt_v3.png：夜間場景外觀參考，提供辦公室材質、色彩、光影與氣氛。
圖2 cam_amy_cu_emotion_block_blender.png：構圖底圖，提供取景、透視、頭部位置、大小、頭頂留白及下緣裁切。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的定位人物。

生圖指引：
以圖2為編輯底圖，保留取景、透視、人物佔位、頭部大小、頭頂留白、背景配置與遮擋關係。維持臉部特寫，不推近、不拉遠，不為展示服裝而補出胸部或雙手。

將定位人物替換為 Amy。五官、棕色微捲短髮、淡雀斑與可見的灰色西裝、米白色襯衫採用圖3，不採用設定圖的展示姿態、多視圖排版或背景。以自然人體比例替換簡化白模，不保留方塊外形、長方形脖子或紅色服裝。肩膀與衣領只呈現原構圖下緣可見的少量部分。

將場景材質、色彩與光影更新為圖1的夜間外觀，保留圖2的窗框、百葉、隔板、螢幕、書櫃及椅背位置。不要沿用圖2的白天亮度，不新增檯燈、人物或道具。

畫面描述：
這是一張85mm、坐姿眼高平視的 Amy 臉部特寫。Amy 坐在原有辦公椅上，頭部居中，大小、朝向與裁切沿用圖2。頭頂保持原有留白，下緣僅露出少量衣領與肩部，手臂和雙手都在畫外。

Amy 已放下前一鏡抓頭的雙手，輕輕閉上雙眼，呈現深呼吸、讓自己沉靜下來的瞬間。眼皮自然闔上，不用力擠眼；眉心仍有一點疲憊與緊繃，但已開始放鬆。嘴唇輕輕閉合，嘴角自然，不露齒、不微笑、不說話。下顎放鬆，頭部保持端正，不低垂睡著，也不向後仰。

她的神情帶著專注的內省，像正在心裡重新聽見一段重要提醒。這一刻尚未睜眼、尚未露出頓悟笑容，為後續眉頭舒展與靈感浮現保留表演空間。髮型保留 Amy 原有棕色短髮輪廓，可有前一鏡碰觸頭髮後的輕微鬆亂，不誇張蓬炸。

夜間光影依圖1，以柔和暖色室內光勾勒臉頰與髮絲，搭配畫外螢幕微弱的冷色補光。面部有清楚而柔和的明暗層次，背景維持低照度深藍夜景，不突然變成白天，也不使用強烈光暈或發光特效。

淺景深聚焦 Amy 的面部與閉合眼瞼，身後百葉窗、螢幕與書櫃自然柔化，仍保留原有位置及空間關係。整體安靜、克制，呈現煩躁之後重新整理思緒的情緒轉折。

畫面只有 Amy 一位人物。George 僅存在於後續畫外音中，不出現他的身影、倒影、回憶畫面或半透明人像；其他工位無人。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、文字、對話框、思考泡泡、燈泡圖示或浮水印。
```



## 2026-10-21 shot_3.9.4 GPT v1（待評鑑）
- 工具：內建 image_gen；供應商：OpenAI；模型與費用：工具未提供。
- 輸出：assets/images/shot_3.9.4_gpt_v1.png；1672×941 RGB。
- 參考圖（依輸入順序）：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
  4. D:/kj-openMontage/projects/course-51-esg/clp/prop_smartphone.png
- 驗證：PNG 完整解碼、來源與複本 SHA256 一致。單人夜景、左手持手機／機背朝鏡、低頭觀看成立；頭頂留白減少、頭部下俯側傾及肩胸裁切偏離白模，右食指落在手機邊緣，無法確認觸及螢幕。未重試，未改採用。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_mcu_15deg_empty_gpt_v3.png：夜間辦公室場景外觀參考，提供材質、色彩與光影。
圖2 cam_amy_mcu_15deg_block_blender.png：構圖底圖，提供取景、透視、人物位置、頭部大小、頭頂留白與裁切。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的紅色定位人物。
圖4 prop_smartphone.png：手機外觀參考，只採用深灰色機身與背面三鏡頭，不採用來電介面或多視圖排版。

生圖指引：
以圖2為編輯底圖，保留相機角度、透視、人物佔位、頭部尺度、頭頂留白與背景配置。維持肩胸以上的中特寫，不放大頭部，不拉遠補出桌面、腰部或下半身。

將定位人物替換為圖3的 Amy，保留棕色微捲短髮、淡雀斑、灰色西裝與米白色襯衫。使用自然人體比例，不保留白模的方塊身體、長方形脖子或紅色服裝，不採用人物設定圖的展示姿勢。

僅為持手機與觀看螢幕調整前臂、雙手、視線及少量頭部俯角；肩膀、軀幹與座位沿用圖2。手機置於胸前、畫面下方偏右，不遮住臉部。手肘可在畫外，不為呈現完整手臂而改變構圖。

場景材質、色彩與光影採用圖1的夜間外觀。保留圖2的百葉窗、薄荷綠隔板、書櫃、背景螢幕、椅背與左下前景螢幕的位置及遮擋關係，不沿用白模的白天亮度。

手機採用圖4的外觀，畫面只出現一支手機。手機直立，頂端朝上、底端朝下，螢幕面向 Amy，背面與三鏡頭朝向攝影機。不要為了展示短影音而將螢幕翻向觀眾，不出現「主管來電」介面。

畫面描述：
這是一張從 Amy 工位前方偏側15度、坐姿眼高平視的65mm中特寫。Amy 獨自坐在既有網布辦公椅上，頭部完整入鏡，肩胸以上可見，人物大小與頭頂留白沿用圖2。她剛從前一鏡閉眼沉思中睜開雙眼，左手已將手機拿到胸前，右手食指輕觸螢幕下半部，處於準備向上滑動瀏覽的瞬間。手機及握持處位於畫面下緣以上，手腕與前臂依原構圖自然裁切。她的視線落在手機螢幕上，頭部輕微下俯但不低垂，眉心的緊繃已放鬆，眉毛略微抬起，眼神帶著重新探索的好奇；嘴唇微微分開，像正在輕聲自問「大家到底愛看什麼」，尚未露出明顯笑容或興奮表情。手機正在播放探險短影音，但本鏡從機背方向拍攝，不要求看見螢幕內容；僅以微弱暖色螢幕光映亮她的下頰與雙眼，亮度自然，不使用誇張發光特效。室內柔和暖光與窗外深藍夜色延續圖1，臉部清楚可辨，背景百葉窗、隔板與書櫃自然虛化。畫面只有 Amy 一人，其他工位與走廊無人，整體安靜、專注，呈現思緒開始轉向新方向的瞬間。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、對話框、思考泡泡、燈泡圖示、手機畫面浮窗或浮水印。
```



## 2026-10-21 shot_5.2.1 GPT v1（待評鑑）
- 圖片：`assets/images/shot_5.2.1_gpt_v1.png`
- 工具：內建 image_gen；供應商：OpenAI；模型／費用：工具未提供，未知；生成 1 次。
- 使用者授權新版雙人中景，重新取景，不使用原三人 blocks。未改 scene_plan 或正式採用設定。
- 驗證：1672×941 RGB PNG，完整解碼及來源 SHA256 相符。
- 觀察：Sandy 左側站立、Harrison 右側坐姿，三隻手共同交接單台平板，背面朝鏡頭；兩人頭頂完整。Sandy 微笑較明顯，Harrison 視線較接近左側，未明確低頭看平板；手持角度仍待使用者評鑑。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_threeshot_wide_level_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/clp/char_sandy.jpeg`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_harrison.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_ipad_landscape.png`

```text
參考圖說明：
圖 1 cam_threeshot_wide_level_empty_gpt.png：會議室環境、材質與風格參考；不沿用其全景構圖。
圖 2 char_sandy.jpeg：分析師一號 Sandy 的外觀與服裝參考。
圖 3 char_harrison.jpeg：Mr. Harrison 的外觀與服裝參考。
圖 4 prop_ipad_landscape.png：平板電腦外觀參考。

生圖指引：
在圖 1 的同一間會議室內重新取景，製作 Sandy 將平板遞給 Harrison 的雙人中景。人物外觀與服裝分別依照圖 2、圖 3，平板外觀依照圖 4。參考圖僅提供指定素材，不帶入人物展示姿態或多視角排版。

畫面描述：
眼高、略帶側面的雙人中景，Sandy 位於畫面左側，站在 Harrison 座位旁；Harrison 位於畫面右側，坐在原有棕色皮椅上。Sandy 腰部以上與 Harrison 坐姿上半身入鏡，兩人頭頂完整保留。木質會議桌邊緣出現在畫面下方，雙方手部與平板清楚可見，不被桌面或椅背遮擋。

畫面定格在平板交接的瞬間：Sandy 身體略朝 Harrison 傾近，雙手托住一台橫向平板的兩側，將平板送至他面前；Harrison 向前伸出一隻手，手指剛接住平板靠近自己的下緣，Sandy 尚未鬆手。兩人的手各自接觸不同位置，不重疊糾纏。平板位於兩人之間、桌面上方，大小符合真實手持比例。

平板螢幕朝向 Harrison，略微向上傾斜，讓他能自然低頭閱讀；鏡頭主要看見平板背面與薄側邊，不為了展示螢幕而將它轉向觀眾。

Sandy 神情自信而恭敬，嘴唇微張，目光看向 Harrison，正在說明新提案。Harrison 神情沉穩專注，視線落在正在接過的平板上，尚未露出批准的笑容。

背景延續原會議室的木質、玻璃與棕色皮椅。晴朗日光從落地窗照入，形成明亮柔和的暖色光線，窗外金融大樓清晰可辨。背景略柔化，視覺焦點集中在兩人的表情與交接平板的手部。畫面僅出現 Sandy 與 Harrison，其他與會者位於取景範圍外。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```



## 2026-10-21 shot_3.8.13 GPT 再次生成失敗（未出圖）
- 依使用者指定最新 prompt 與三張參考圖提交 1 次，未重試。
- 工具／供應商：內建 image_gen／OpenAI；模型版本與費用未知。
- 錯誤：HTTP 400 moderation_blocked，moderation_stage=output，categories=[other]；request ID 7b0bdb14-b7fe-4cb7-8155-fb6dfb0303f1。未取得圖片，未改正式採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`
### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色衣身定位人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物位置與比例、頭頂留白、軀幹朝向及畫面裁切。不拉近鏡頭、不放大頭部、不為容納手勢重新安排人物位置。

將藍色定位人物替換為圖 3 的 George。五官、灰白髮型、棕色眼鏡、短鬍鬚、米色襯衫、棕色背心與領帶採用圖 3，不採用人物參考圖的展示姿態或分格構圖，不保留 blocks 的簡化五官與方塊外觀。

將場景材質、風格與溫暖日光更新為圖 1 的外觀，空間配置與遮擋關係沿用圖 2。保留玻璃門、石材立柱與沿街花台的原有位置。

畫面描述：
這是一張眼高平視、斜側約 45 度取景的 George 單人中特寫。頭部、肩膀與胸前區域依圖 2 入鏡，下半身位於畫外。畫面只有 George 一人，Amy 位於畫左鏡外。

George 正準備向 Amy 說明 ESG 能提升同事的競爭力與工作價值。他眉梢微微舒展，眼神明亮而專注，嘴角帶著有信心的溫和微笑，嘴唇自然微張，呈現真誠、鼓勵與有說服力的神情。

頭部略朝畫左，下巴保持自然水平。雙眼水平看向畫左鏡外 Amy 的臉；虹膜與瞳孔在眼裂中的垂直位置自然居中，不向上翻、不看天空、不看鏡頭。

雙肘彎曲，前臂抬至下胸前，雙手自然分開，掌心朝上，手指放鬆微彎，停在即將向上托舉的起始位置。手勢開闊而克制，雙手不交扣、不握拳、不指人，不遮住臉部。允許為此調整手臂與手掌，肩膀、軀幹位置及人物尺度仍沿用圖 2。

焦點落在 George 的眼睛、表情與胸前手勢；背景玻璃門、石柱和綠植柔和失焦，保持圖 1 的溫暖日光與人物參考的精緻 3D 動畫質感。

這是一張動作起始畫面，只呈現雙手準備向上托舉的單一瞬間，不加入動作殘影、上升箭頭或概念圖示。除上述表情、視線與手臂姿態調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、字卡、對話框或浮水印。
```


## 2026-10-21 shot_5.2.2 GPT v1（待評鑑）
- 圖片：`assets/images/shot_5.2.2_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；模型與費用未知；成功生成 1 次，之前六圖請求於參數檢查被拒、未出圖。
- 使用者同意人物原圖並排為一張，只調整 prompt 圖號。人物合圖由兩張 5504×3072 原圖無縮放並排，11008×3072。
- 目視：Sandy 指向攤開報告、Harrison 右前景、日照及投影圖表呈現；Sandy 明顯放大、頭頂留白減少，Harrison 頭肩範圍增加，偏離 blocks。平板背面朝鏡頭。待使用者評鑑，未改採用設定。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_sandy_ots_harrison_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_sandy_ots_harrison_block_blender.png`
3. `D:/kj-openMontage/.tmp/shot_5.2.2_character_refs.png`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_proposal_document.png`
5. `D:/kj-openMontage/projects/course-51-esg/clp/prop_ipad_landscape.png`

```text
參考圖說明：
圖 1 cam_sandy_ots_harrison_empty_gpt.png：會議室場景外觀參考圖。
圖 2 cam_sandy_ots_harrison_block_blender.png：構圖底圖。
圖 3 shot_5.2.2_character_refs.png：左半為 Sandy（char_sandy.jpeg），對應圖 2 左側紅色人物；右半為 Harrison（char_harrison.jpeg），對應圖 2 右前景人物。兩張原人物參考圖並排。
圖 4 prop_proposal_document.png：報告書裝訂、材質與外觀參考圖。
圖 5 prop_ipad_landscape.png：橫向平板外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、桌椅配置、人物佔位、比例與遮擋關係。Sandy 保持在畫面左側中景，Harrison 的後腦與椅背位於右前景；不為了露出 Harrison 的臉或雙手而改變機位。

人物外觀與服裝採用圖 3 的左半 Sandy、右半 Harrison，不採用其展示姿態。只替換圖 2 可見的人物部位，不補出被椅背或桌面遮住的身體。

場景材質與風格採用圖 1，光線依本鏡改為明亮暖和的日間。自然日光由畫外落地窗方向照入，使 Sandy 的臉部、木質桌面與皮椅清晰可辨，不新增畫內窗戶或改動空間格局。

報告書外觀採用圖 4，呈現打開的白色內頁與深藍書脊；平板外觀採用圖 5，每種道具各一件。參考圖的多視角展示不作為多件實物。

畫面描述：
這是一張 42mm、坐姿眼高平視的過肩中景，越過右前景 Harrison 的後腦與椅背拍向 Sandy。Sandy 頭部完整入鏡，下半身被會議桌遮擋，人物大小與頭頂留白沿用圖 2。焦點落在 Sandy，前景 Harrison 略微柔化。

Sandy 站姿挺直，神情自信、專業而有說服力，眉眼舒展，嘴唇微張，視線朝向右前景的 Harrison。將 blocks 原本抬起指向投影幕的手臂放下，改為向桌面伸出，食指指向靠近她一側、攤開的永續報告內頁。報告位於她自然伸手可及的位置，內頁可見整齊的數據表與圖表。另一隻手自然低放，不拿簡報遙控器。

這一瞬間只呈現「指出報告中的證據」，不同時指向平板。平板已交給 Harrison，位於右前景桌面、螢幕朝向他；允許受椅背遮擋，不為了完整展示而移動人物或椅背。Harrison 的頭部略朝報告方向轉動，維持專注聆聽的姿態。

後方投影幕保留原有位置、大小與透視，內容改為簡潔的減碳及工安績效圖表，作為說明背景，不加入核准投資的標語。室內維持明亮、溫暖而專業的氣氛，畫面只有 Sandy 與 Harrison。

除上述手勢、道具、投影內容與日照調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```



## 2026-10-21 shot_3.9.5 GPT v1（待評鑑）
- 工具：內建 image_gen；供應商：OpenAI；模型與費用：工具未提供。
- 輸出：assets/images/shot_3.9.5_gpt_v1.png；1672×941 RGB。
- 參考圖（依輸入順序）：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 驗證：PNG完整解碼、來源與複本SHA256一致。單人夜景、坐姿胸前雙拳、開心振奮成立；頭部側傾、視線偏畫面左上而非直視鏡頭，頭頂留白減少、肩位與軀幹比例偏離白模。未重試、未改採用。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_ms_15deg_empty_gpt_v3.png：夜間辦公室場景外觀參考，提供材質、色彩與光影。
圖2 cam_amy_ms_15deg_block_blender.png：構圖底圖，提供取景、透視、人物位置、比例、頭頂留白與裁切。
圖3 char_amy.jpeg：Amy 人物參考，對應圖2的紅色定位人物。

生圖指引：
以圖2為編輯底圖，保留相機角度、透視、人物佔位、頭部大小、頭頂留白、背景配置及前景遮擋。維持15度微側的單人中景，不推近、不拉遠，不補出畫外下半身。

將紅色定位人物替換為圖3的 Amy，保留棕色微捲短髮、淡雀斑、灰色西裝與米白色襯衫。採用自然人體比例，不保留白模的方塊身體、長方形脖子或紅色服裝，不採用人物設定圖的展示姿勢。

調整雙臂與雙手，使兩手在胸前握拳，拳頭自然分開，不相碰、不遮擋臉部，雙拳位於畫面內且不被左前景螢幕遮住。容許握拳動作所需的自然肩部變化，軀幹保持原座位位置。此刻仍坐在既有網布辦公椅上，尚未站起。

將場景的材質、色彩與光影更新為圖1的夜間外觀。保留圖2的百葉窗、隔板、書櫃、盆栽、螢幕與椅背配置，不沿用白模的白天亮度，不新增檯燈或其他道具。

畫面描述：
這是一張從 Amy 工位前方偏側15度拍攝的50mm單人中景，相機維持圖2的高度與透視。Amy 坐在原有辦公椅上，上半身與胸前雙拳清楚可見，下半身在畫外，左前景保留原有螢幕遮擋。她已結束上一鏡的手機瀏覽，手機位於畫外，不出現在手中；此刻上身挺直，雙肘彎曲，兩手剛在胸前握成拳頭，捕捉靈感轉化為決心、即將起身宣告的瞬間。她抬頭看向鏡頭，雙眼明亮而專注，眉毛自然揚起，眉心完全舒展，嘴角上揚、嘴唇微張，像剛開始說出「大家愛看故事！」；表情帶著找到答案的喜悅與篤定，不是憤怒、挑釁或戰鬥姿態。棕色短髮延續前鏡的略微鬆亂，服裝保持一致。柔和暖色室內光與微弱螢幕補光照亮面部，窗外保持深藍夜色，情緒的振奮透過眼神與姿態表現，不突然提高整間辦公室亮度。中等景深讓 Amy 的面部與雙拳清楚，背景略柔化但仍可辨識原有空間。畫面只有 Amy 一人，其他工位與走廊無人。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、「ESG 尋寶獵人」字卡、對話框、燈泡圖示、發光特效或浮水印。
```



## 2026-10-21 shot_5.2.2 GPT v2（連戲重設，待評鑑）
- 圖片：`assets/images/shot_5.2.2_gpt_v2.png`
- 工具：內建 image_gen／OpenAI；模型與費用：未知；生成1次。
- 按使用者確認新版prompt逐字生成，延續shot_5.2.1雙人中景。保留v1，未改正式採用或scene_plan。
- 驗證：1672×941 RGB PNG，完整解碼與來源SHA256相符。
- 目視：Sandy仍在Harrison旁並指向報告，Harrison低頭、平板背面朝鏡頭，背景大致延續。Sandy指示手與prompt指定靠近Harrison側不同；Harrison持平板位置移至畫右、另一手新增指報告動作；報告偏大、人物姿態略重繪，待評鑑。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_5.2.1_gpt_v1.png`
2. `D:/kj-openMontage/projects/course-51-esg/clp/prop_proposal_document.png`

```text
參考圖說明：
圖 1 shot_5.2.1_gpt_v1.png：連戲與編輯底圖，提供機位、人物外觀、站位、場景與光線。
圖 2 prop_proposal_document.png：報告書外觀、裝訂與材質參考。

生圖指引：
以圖 1 為編輯底圖，延續同一鏡位、景別、透視與人物大小。保留 Sandy 在畫面左側、站在 Harrison 座位旁的位置；Harrison 保持畫面右側坐姿。保留兩人的五官、髮型、服裝、頭頂留白，以及會議桌、皮椅、落地窗、窗外大樓與日照方向。

這是平板交接完成後的下一個瞬間。只調整雙方手臂、手部、頭部俯角、視線與表情，並在桌面加入一本攤開的報告書。不要將 Sandy 移回投影幕旁，不改成過肩鏡頭。

報告書外觀依照圖 2，保留深藍書脊、白色紙張與淡藍綠設計元素；此刻呈現攤開的內頁，可見整齊的數據表與圖表，不要求封面朝向鏡頭。只生成一本報告，不帶入參考圖的多視角排版。

畫面描述：
眼高、略帶側面的雙人中景，構圖沿用圖 1。Sandy 站在左側，Harrison 坐在右側，兩人頭頂完整入鏡。木質桌面位於畫面下方，保留足夠空間呈現報告與指向內頁的手指。

Harrison 已接過原有的橫向平板，以靠近 Sandy 的那隻手穩妥握住平板側邊及下緣，平板稍微降低至桌面上方，螢幕仍朝向他，鏡頭主要看見機背與薄側邊。平板不遮住報告或 Sandy 的指示手勢。他另一隻手仍自然放在桌上，頭部略微低下，視線落在 Sandy 指出的報告位置，神情沉穩專注，尚未露出批准的笑容。

Sandy 已放開平板，仍站在 Harrison 身旁，身體輕微向桌面前傾。一本攤開的永續報告放在兩人之間、靠近 Harrison 的桌面上，頁面朝向 Harrison，位於 Sandy 自然伸手可及的位置。

Sandy 用靠近 Harrison 的那隻手伸出食指，指尖輕觸報告內頁的一處數據圖表；另一隻手自然放在自己身側。她的頭部略朝 Harrison 轉動，目光看向他，眉眼舒展、神情自信而專業，嘴唇微張，正在解釋驗證數據。笑意克制，重點是清楚、有把握地說明證據。

畫面只呈現「Sandy 指出報告數據、Harrison 專注查看」的一個瞬間，不同時指向平板，不重演遞交動作。只有 Sandy 與 Harrison 兩人、一台平板及一本攤開的報告。

保留圖 1 明亮柔和的日間暖陽、木質與玻璃材質，以及略微柔化的背景。除上述表演與道具調整外，其餘沿用圖 1。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```



## 2026-10-21 shot_3.9.5a GPT v1（待評鑑）
- 工具：內建 image_gen；供應商：OpenAI；確切模型與費用：工具未提供。
- 輸出：assets/images/shot_3.9.5a_gpt_v1.png；1672×941 RGB。
- 參考圖（依輸入順序）：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 驗證：PNG完整解碼、來源與複本SHA256一致。坐姿、右食指抵下巴、左手托肘、抬頭上望成立；下緣多露少量桌面、人物比例與肩位偏離白模。 未重試、未改採用。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_ms_15deg_empty_gpt_v3.png：夜間辦公室外觀參考，提供材質、色彩與光影。
圖2 cam_amy_ms_15deg_block_blender.png：坐姿構圖底圖，提供相機方向、透視、人物位置、比例與裁切。
圖3 char_amy.jpeg：Amy 人物外觀與服裝參考，對應圖2的紅色定位人物。

生圖指引：
以圖2為編輯底圖，保留取景、透視、人物佔位、頭部大小、頭頂留白及前景遮擋。將紅色定位人物替換為圖3的 Amy，使用自然人體比例，保留棕色微捲短髮、淡雀斑、灰色西裝與米白色襯衫，不保留白模的方塊身體或紅色服裝。

依思考姿態調整雙臂、雙手、頭部與視線，其餘沿用坐姿構圖。Amy 的右手食指輕抵下巴側下緣，其餘手指自然微彎，不遮住嘴唇；左前臂橫放於胸腹前，左手掌從下方托住右手肘，形成自然的托肘思考姿勢。雙手各司其位，不交纏、不合十，不增加手臂。

場景材質與光影採用圖1的夜間外觀，保留圖2的窗戶、百葉、隔板、書櫃、盆栽、螢幕及椅背配置，不新增道具。

畫面描述：
這是一張從 Amy 工位前方偏側15度拍攝的50mm單人中景。Amy 坐在既有網布辦公椅上，上半身挺直而放鬆，右手食指抵著下巴，左手托住右手肘，雙手接觸關係清楚可辨。她的頭微微抬起，下巴略揚，雙眼輕微看向鏡頭上方的遠處，不直視觀眾，也不誇張翻白眼。眉毛略抬、眉心放鬆，嘴唇輕輕微張，呈現正在推敲新點子、逐漸找到方向的專注神情，尚未露出大笑或握拳慶祝。手機已放到畫外，雙手不持道具。暖色室內光柔和照亮面部，窗外保持深藍夜色，背景稍微柔化但保留空間辨識度。只有 Amy 一人，其他工位與走廊無人。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、對話框、思考泡泡、燈泡圖示或浮水印。
```


## 2026-10-21 shot_3.9.5b GPT v1（待評鑑）
- 工具：內建 image_gen；供應商：OpenAI；確切模型與費用：工具未提供。
- 輸出：assets/images/shot_3.9.5b_gpt_v1.png；1672×941 RGB。
- 參考圖（依輸入順序）：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 驗證：PNG完整解碼、來源與複本SHA256一致。站姿、胸前雙拳分開且不遮臉成立；頭頂留白偏少，視線略偏上、頭部側傾，背景取景未明顯上移。 未重試、未改採用。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_ms_15deg_empty_gpt_v3.png：夜間辦公室外觀參考，提供場景材質、色彩與光影。
圖2 cam_amy_ms_15deg_block_blender.png：工位空間與15度微側拍攝方向參考；人物為坐姿定位，本張須改為站姿，不沿用坐姿頭部高度及裁切。
圖3 char_amy.jpeg：Amy 人物外觀與服裝參考。

生圖指引：
沿用圖2的工位空間與拍攝方向，將紅色定位人物替換為圖3的 Amy。保留棕色微捲短髮、淡雀斑、灰色西裝與米白色襯衫，使用自然人體比例，不保留白模的方塊外形。

將 Amy 改為從原座位起身後的站姿，站在原工位桌後、辦公椅前方。雙手空手握拳，抬至胸前，拳頭自然分開，彼此不相碰，不遮住臉部。雙肘彎曲、肩膀自然下沉，拳頭位於下巴以下，呈現振奮與決心。

依站姿向上重新取景，必要時適度放寬畫面，保持50mm中景的自然透視，讓頭髮頂端、完整臉部及雙拳都清楚入鏡，頭頂保留適量留白。不要把人物壓縮回坐姿高度，也不要藉由縮短軀幹讓站姿塞入原坐姿裁切。保留椅子在身後較低處的合理位置，不新增第二張椅子。

場景外觀採用圖1，保留既有家具與窗戶的空間關係，背景隨重新取景自然改變可見範圍，不把家具搬動到新位置。

畫面描述：
這是一張從 Amy 工位前方偏側15度拍攝的單人站姿中景。Amy 已從椅子站起，上身挺直、胸口自然打開，雙拳在胸前分開，兩隻拳頭都不受前景螢幕遮擋。她抬頭望向鏡頭，雙眼明亮而堅定，眉心舒展，嘴角上揚、嘴唇微張，像正要說出「對！」，呈現終於想通方向的喜悅與自信。姿態有精神但不聳肩、不後仰、不擺出搏擊架勢。手機不在手中。深藍窗外夜景與柔和暖色室內光延續前鏡，臉部和雙拳清楚，其他工位與走廊無人。情緒的提升由表情與站姿表現，不加入誇張光效。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入字幕、「ESG 尋寶獵人」字卡、對話框或浮水印。
```



## 2026-10-21 shot_3.9.6 GPT v1（待評鑑）
- 工具：內建 image_gen；供應商：OpenAI；確切模型與費用：工具未提供。
- 參考圖／編輯底圖：assets/images/shot_3.9.1_gpt_v1.png。
- 輸出：assets/images/shot_3.9.6_gpt_v1.png；1672×941 RGB。
- 驗證：PNG完整解碼、來源與複本SHA256一致。新標題目視為《Amy 的 ESG 大尋寶：全體員工升級計畫》，單行、正文空白、結尾游標成立；游標較長，原介面尺規數字不規則仍在。未重試、未改採用。

完整 prompt：
```text
請局部編輯這張夜間辦公室電腦螢幕特寫，只修改文件中的標題文字與文字游標位置。

保留原圖的相機角度、透視、取景、螢幕大小與位置、黑色邊框、底座、桌面、薄荷綠隔板、百葉窗及窗外夜景。保持原有文書軟體介面、工具列、白色文件頁面與夜間光影，不拉近、不拉遠、不改變螢幕造型。

將文件上方的舊標題「《ESG 推動管理辦法與獎懲細則草案》」完整移除，替換為以下繁體中文新標題，文字必須完全一致：

《Amy 的 ESG 大尋寶：全體員工升級計畫》

新標題沿用原本黑色粗體標題風格與置中位置，適度縮小字級，使整段標題完整呈現在同一行，左右保留頁面邊距，不裁切、不擠壓字形。保留英文 Amy、ESG 的大小寫、中文全形冒號與前後書名號，不加入驚嘆號或其他文字。

將原本位於下一行左側的文字游標移除，改在新標題最後一個「》」的右側顯示一條細直文字游標，呈現剛完成輸入的瞬間。文件正文維持空白，不新增段落、清單、圖片或裝飾。

畫面聚焦於清楚可讀的新企劃名稱，以相同辦公室與文書介面呈現 Amy 思路的轉變。保持螢幕自然發光與室內暖光，不增加光暈、閃光或熱血特效。

畫面不出現人物、手部、人物倒影或額外鍵盤特寫。不將刪除與打字的多個階段拼貼在同一張圖，不保留舊標題殘字。

輸出一張16:9彩色分鏡圖，不加入螢幕以外的字幕、疊字、對話框或浮水印。
```



## 2026-10-21 shot_5.2.3 GPT v1（待評鑑）
- 圖片：`assets/images/shot_5.2.3_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；模型與費用未知；依確認prompt逐字生成1次。
- 驗證：1672×941 RGB PNG，完整解碼及來源SHA256相符。
- 目視：平板右、攤開報告左，無真人或手部，螢幕群像與綠樹清楚，平板四角完整；報告左側裁切且內頁重繪，樹上群像較像員工坐在枝葉間，不完全是員工組成樹形。螢幕圖為本次生成插畫，非既有Vlog截圖。未改正式採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_table_insert_iso_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_table_insert_iso_empty_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/prop_ipad_landscape.png`
4. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_5.2.2_gpt_v2.png`

```text
參考圖說明：
圖 1 cam_table_insert_iso_empty_gpt.png：會議桌材質與場景外觀參考。
圖 2 cam_table_insert_iso_empty_blender.png：桌面取景與透視底圖。
圖 3 prop_ipad_landscape.png：平板外觀參考，不採用其投資儀表板內容。
圖 4 shot_5.2.2_gpt_v2.png：上一鏡連戲參考，提供攤開報告的外觀、內頁與日間光線，不帶入人物或雙人構圖。

生圖指引：
以圖 2 為編輯底圖，保留高角度斜俯視的桌面透視、木紋方向、桌緣與背景皮椅的可見範圍。桌面材質採用圖 1，光線延續圖 4 明亮柔和的日間暖陽。

在桌面加入一台橫向平板及一本攤開的報告。平板外觀採用圖 3；報告沿用圖 4 的深藍封皮、白色內頁與藍綠色數據圖表。只有一台平板、一本報告，不加入人物、手部或其他道具。

畫面描述：
這是一張 60mm、高角度斜俯視的桌面特寫插鏡。橫向平板平放在木質桌面中央偏右，螢幕朝上，四角與薄邊框完整可見。攤開的報告位於平板左側，兩件物品靠近但不重疊，閱讀方向一致，像是 Harrison 剛將平板放在正在閱讀的報告旁。

平板為主要視覺焦點，螢幕有足夠面積辨識影片內容。報告作為次要資訊，可見圖表與整齊版面，不要求閱讀小字。兩件物品自然貼合桌面透視，接觸陰影清楚，不懸浮。

平板螢幕正在全螢幕顯示 Amy 的 ESG Vlog 結尾動畫：一群笑容明亮、穿著辦公室服裝、工作服與實驗室白袍的員工，以簡潔、溫暖的彩色動畫插畫呈現；員工群像沿著樹幹與向外伸展的枝條排列，共同組成一棵枝葉茂密的綠色大樹。畫面定格於大樹形態已完整形成、仍能辨認員工笑臉與團隊群像的瞬間，傳達全體員工共同投入永續的意義。

大樹與員工只出現在平板螢幕內，不延伸到真實桌面，不變成立體模型、全息投影或浮空圖示。螢幕內容遵循平板表面的透視，不生成正對鏡頭的獨立海報。不要顯示投資儀表板、播放按鈕或剪輯軟體介面。

暖陽在木質桌面留下柔和光澤，螢幕保持清楚，不被窗戶反光遮住。淺景深聚焦於平板螢幕，報告仍可辨識，遠處桌面與皮椅自然柔化。維持安靜、溫暖而專業的會議室氛圍。

輸出一張 16:9 彩色分鏡圖，單一連貫畫面，不加入字幕、對話框或額外疊字。
```



## 2026-10-21 shot_3.9.7 GPT v1（待評鑑）
- 工具：內建 image_gen；供應商：OpenAI；確切模型與費用：工具未提供。
- 輸出：assets/images/shot_3.9.7_gpt_v1.png；1672×941 RGB。
- 參考圖（依輸入順序）：
  1. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_ms_15deg_empty_gpt_v3.png
  2. D:/kj-openMontage/projects/course-51-esg/references/scenes/staff_office/cameras/cam_amy_mcu_selfie_block_blender.png
  3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
- 驗證：PNG完整解碼、來源與複本SHA256一致。夜間單人自拍、右臂前伸、左手整理瀏海、手機不入鏡成立；頭部側傾、肩胸裁切偏離白模，伸出前臂佔前景較大。未重試、未改採用。

完整 prompt：
```text
參考圖說明：
圖1 cam_amy_ms_15deg_empty_gpt_v3.png：同一辦公室的夜景外觀參考，只提供材質、色彩、夜間亮度與光影，不採用其機位和裁切。
圖2 cam_amy_mcu_selfie_block_blender.png：自拍構圖底圖，提供微俯視角度、透視、人物佔位、頭部尺度、頭頂留白及背景配置。
圖3 char_amy.jpeg：Amy 人物外觀與服裝參考，對應圖2的紅色定位人物。

生圖指引：
以圖2為編輯底圖，保留自拍微俯視角度、取景、透視、人物比例、頭頂留白、可見身體範圍及背景遮擋。不要改成旁觀者拍攝 Amy 拿手機的第三人稱視角，不拉遠補出全身。

將紅色定位人物替換為圖3的 Amy，保留棕色微捲短髮、淡雀斑、灰色西裝與米白色襯衫。使用自然人體比例，不保留白模的方塊身體、長方形脖子或紅色服裝，不採用人物設定圖的展示姿態。

調整 Amy 的右臂，使其自然向鏡頭方向伸出，呈現手持手機自拍的姿態。右前臂可在畫面左下緣局部出現，持手機的手與手機本體位於鏡頭所在位置之外，不必完整入鏡，不為展示手機而改變視角。

Amy 的左手抬至額側，以指尖輕觸瀏海，呈現剛開始整理髮絲的瞬間。手指自然分開，不遮擋雙眼、鼻子或嘴巴，不拉扯頭髮。除了指定的手臂動作，其餘身體位置沿用圖2。

以圖1的夜間材質與光影更新圖2的辦公室，保留圖2的窗戶、百葉、隔板、書櫃、盆栽、螢幕、桌角與椅背位置。窗外改為深藍夜色與零星建築燈光，移除白天日照及陽光條紋，不新增檯燈或其他道具。

畫面描述：
這是一張28mm手機前鏡頭視角的橫向自拍中特寫，鏡頭略高於 Amy 的雙眼，向下輕微俯拍。Amy 坐在原有網布辦公椅上，頭部完整入鏡，肩胸以上可見，保持圖2的頭頂留白。她右臂向鏡頭方向伸出持機，左手指尖輕觸額側瀏海，正準備將髮絲整理妥當。她的視線看向靠近鏡頭的自拍螢幕，雙眼明亮、眉心舒展，嘴角帶著克制而自信的俏皮微笑，嘴唇輕輕微張，像準備低聲說出「好戲……要上場囉！」。此刻尚未伸指按下錄影鍵，為後續放下整理瀏海的手、說話與按鍵動作保留起點。面部以柔和暖色室內光照亮，搭配微弱手機螢幕補光，背景維持安靜的深夜辦公室。景深讓 Amy 的眼睛、臉部與整理瀏海的手清楚可辨，背景略柔化。畫面只有 Amy 一人，其他工位與走廊無人。

輸出一張16:9彩色分鏡圖，單一連貫畫面，不加入手機邊框、相機操作介面、錄影紅點、字幕、對話框或浮水印。
```



## 2026-10-21 shot_5.2.4 GPT v1（待評鑑）
- 圖片：`assets/images/shot_5.2.4_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；模型與費用未知；依確認prompt逐字生成1次。
- 驗證：1672×941 RGB PNG，完整解碼與來源SHA256相符。
- 目視：Harrison單人特寫、低頭下視、閉嘴、頭頂完整、雙手及道具畫外、日間暖光呈現；眉心仍明顯緊繃，未充分柔化，頭臉比例及肩膀可見範圍偏離blocks，背景右側新增樓體。待評鑑，未改正式採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_harrison_cu_emotion_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_harrison_cu_emotion_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_harrison.jpeg`

```text
參考圖說明：
圖 1 cam_harrison_cu_emotion_empty_gpt.png：場景外觀參考圖。
圖 2 cam_harrison_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_harrison.jpeg：Harrison 人物外觀與服裝參考，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部大小、頭頂留白、肩膀裁切與椅背遮擋關係。不要拉遠成中景，不放大臉部，也不補出畫外的手、平板或報告。

將定位人物替換為圖 3 的 Harrison，保留銀灰色後梳髮型、濃眉、長鼻、方長下巴與深藍細條紋西裝。人物參考只提供外觀與服裝，不沿用其緊繃怒視的表情或展示姿態。

場景材質採用圖 1，保留棕色真皮高背椅、窗框與窗外大樓的位置。依本鏡劇情將陰冷光線改為晴朗明亮的日間暖光，延續前兩鏡的自然日照；窗外建築明亮清晰，背景自然虛化，不改動窗框與建築結構。

畫面描述：
這是一張 85mm、平視固定機位的 Harrison 單人臉部特寫。完整頭部、頸部及肩膀上緣入鏡，胸口以下自然裁切，人物比例與留白沿用圖 2。棕色皮椅位於頭部與肩膀後方，窗外金融大樓形成柔和背景。

Harrison 剛看完平板上的影片，仍安靜坐在原位。下巴稍微內收，頭部輕微低俯，雙眼看向畫面下方、桌上平板所在的位置，呈現沉默思考後、尚未完全抬頭的瞬間。不要低頭到遮住眼睛，雙眼與細微表情仍須清楚可辨。

眉心原本的緊繃稍微鬆開，眼神由嚴厲轉為沉穩、若有所思；嘴唇輕合，嘴角僅有幾乎察覺不到的柔化，尚未形成明顯笑容。不露齒、不挑眉、不做誇張讚許表情，保留即將說出「Risk is not attractive.」之前的懸念。

Sandy 仍站在 Harrison 身旁，但完全位於本鏡取景範圍外，不加入她的臉、肩膀或倒影。畫面只有 Harrison 一人；雙手、平板、報告與桌面均不入鏡。

自然暖光柔和照亮臉部，保留額頭、眼周與嘴角的細節。淺景深聚焦雙眼與面部表情，皮椅及窗景自然柔化，不使用誇張光暈。

除上述頭部俯角、視線、表情與日照調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```



## 2026-10-21 shot_5.2.5 GPT v1（待評鑑）
- 圖片：`assets/images/shot_5.2.5_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；模型與費用未知；依確認prompt逐字生成1次。
- 驗證：1672×941 RGB PNG，完整解碼與來源SHA256相符。
- 目視：右手指報告、左手低放、單人完整頭頂及桌面道具呈現；視線朝畫左上，眉心仍緊，笑意較明顯並略露齒，報告下緣裁切。平板螢幕內容偏向觀眾而非Harrison閱讀方向，與prompt有偏差。人物及背景重繪，待評鑑，未改正式採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_harrison_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_harrison_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_harrison.jpeg`
4. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_5.2.3_gpt_v1.png`

```text
參考圖說明：
圖 1 cam_harrison_mcu_45deg_empty_gpt.png：會議室場景外觀參考。
圖 2 cam_harrison_mcu_45deg_block_blender.png：Harrison 座位、人物與背景空間關係參考；本鏡需調整取景及手勢。
圖 3 char_harrison.jpeg：Harrison 人物外觀與服裝參考。
圖 4 shot_5.2.3_gpt_v1.png：桌上平板、攤開報告及平板螢幕內容的連戲參考，不採用其俯視機位。

生圖指引：
以圖 2 的座位與拍攝方向為基礎，略放寬取景並向下調整，使 Harrison 的完整頭部、胸腹、前臂及面前的桌面入鏡。保留人物坐在棕色皮椅上的位置，以及窗框、窗外大樓與座椅的空間關係。不強制沿用圖 2 的原裁切，不將桌面或道具懸浮到胸前。

人物外觀與服裝採用圖 3，保留銀灰後梳髮型、濃眉、長鼻、方長下巴及深藍細條紋西裝。不要沿用人物參考圖的怒視表情，也不要保留 blocks 的雙臂交叉姿勢。

場景材質採用圖 1，將陰冷窗景改為延續前鏡的晴朗日間暖光。棕色皮椅、玻璃與木質桌面保持自然質感，窗外建築明亮、柔和虛化。

平板與攤開報告的外觀採用圖 4。保留報告的深藍封皮、白色內頁與藍綠圖表；平板維持橫向平放、螢幕朝上，顯示員工與綠色大樹畫面。依本鏡機位呈現自然透視，不為了展示螢幕而將平板立起或轉向觀眾。

畫面描述：
這是一張坐姿眼高、固定機位的 Harrison 單人中近景。Harrison 坐於畫面中央的皮椅上，頭頂完整保留，胸腹與前臂清楚入鏡。面前木質桌面佔畫面下方，提供完整的手勢與報告閱讀空間。

Harrison 已從前鏡的沉思中抬起頭，身體稍微向前，保持沉穩而有權威的坐姿。他的右前臂向桌面伸出，右手食指輕觸攤開報告上的一處數據圖表；其餘手指自然彎曲，手腕與手臂連接清楚。左手放鬆地停在桌面，不握平板、不指向其他物件。

報告位於 Harrison 右手自然可及之處，平板並排放在報告旁，兩件物品不重疊。報告頁面與平板螢幕均朝向 Harrison 的閱讀方向。只呈現一本報告與一台平板，平板中的人物不出現在真實會議室。

Harrison 的頭部略轉向畫外、仍站在他身旁的 Sandy，視線看向她的臉，略微高於自己的坐姿眼線，不看鏡頭、不仰望天花板。眉心明顯放鬆，眼神專注而帶著認可，嘴角有克制、極淡的讚許笑意，嘴唇微張，正開始說明數據證明了公司的合規。保留他一貫的沉著，不露齒大笑、不誇張挑眉。

定格在「右手指出報告數據」這一個瞬間，不同時指向平板，也不提前演出最後強調結論的手勢。Sandy 完全位於取景範圍外，不加入她的肩膀、手部或倒影。

自然暖光照亮臉部與桌面，焦點落在 Harrison 的表情及指向報告的手勢。窗外大樓與皮椅背景柔和虛化，報告和平板仍可辨識，整體維持專業、沉穩、帶著由衷認可的氣氛。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字。
```



## 2026-10-21 cafe overview GPT v4（指定 loc_cafe_left_far 美術參考）
- 狀態：已生成，待使用者評鑑，未改採用。
- 工具：內建 image_gen／OpenAI；模型版本、預估與實際費用未知；單次生成1張。
- 圖1：references/scenes/cafe/cameras/cam_room_wide_overview_empty_blender_v2.png（唯一構圖底圖）
- 圖2：clp/loc_cafe_left_far.png（美術參考）
- 輸出：references/scenes/cafe/cameras/cam_room_wide_overview_empty_gpt_v4.png
- 驗證：PNG 1672×941 RGB，完整解碼及原生工具圖複本SHA256一致。
- 觀察：空景、四張完整椅＋右下裁切椅、兩桌與三垃圾桶保留；暖日光與布料材質成立。家具相對尺寸／位置略移，窗外建築與植葉重繪、地板紋理偏強，冰箱疑保留多餘右側把手，非精確幾何複製。未重試。

### 完整實際提示詞
```text
Use case: style-transfer.
請編輯圖1，將本機位 Blender 空景轉成與圖2同一套美術的高質感3D場景背景。
圖1 cam_room_wide_overview_empty_blender_v2.png 是唯一編輯底圖，唯一決定相機位置、觀看方向、透視、構圖、畫面裁切及物件配置。
圖2 loc_cafe_left_far.png 是同一場景的共用美術參考，只提供材質、色彩、光影與氣氛。不要採用圖2的拍攝角度、消失點、畫面排列或可見範圍，不要重新生成圖2。
匹配圖2的米灰細織布沙發、珊瑚橘布抱枕、淺木地板與層板、奶白霧面櫃體、拉絲金屬冰箱、陶瓷杯罐、自然綠葉；暖日光配合冷藍都市窗景與柔暖天花燈。不額外加強飽和度、暖色或泛光。依圖1朝向維持合理窗邊入光方向，不直接複製圖2光斑位置。
【保留本機位】
維持圖1的16:9畫幅、廣角俯視角度、消失點、主要結構與遮擋。保留窗框分格、立柱、門、天花燈與空調、地面邊界、家具設備及植物的位置、數量、尺度與主要輪廓。不旋轉相機、不鏡像、不拉遠拉近。不要為展示完整物件補出被裁切部分。
【材質與細節提升】
沿用圖1構造與物件種類，只提升微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與自然玻璃反射。布料紋理細緻且尺度合理，抱枕有柔軟皺褶；木紋淡雅，陶瓷與金屬質感區分。植物保留位置與主要枝幹，在原體積內細化薄葉、透光與自然葉片，不新增植物。保持乾燥霧面地板，不增加鏡面反光、髒污或強景深模糊。
【本鏡畫面】
本鏡為室內高位廣角全景：左側大面落地窗與冷藍都市建築，中景四張單人椅圍繞兩張圓桌；前桌杯子與書冊、後桌盆栽均保留。後牆茶水台含左側冰箱、水槽、微波爐、咖啡機、上下櫃與兩層木架、杯罐和垂葉植物，右方三個並排垃圾桶與畫框邊緣的木門。左下吧台和兩個凳子局部入鏡；右下另有被畫框裁切的椅子與橘抱枕，嚴格保留這些裁切關係。冰箱把手維持圖1靠窗左側的位置，杯子各自完整直立。所有物件依圖1位置，不套圖2家具位置。
【空景與輸出】
零人物，不得出現人體、肩膀、手臂、人影或人物倒影。只輸出一張16:9高解析度完整圖片，不拼貼、不加字幕、標誌或水印。
```




## 2026-10-21 cafe overview 人物重繪 GPT v1（待評鑑）
- 輸出：`references/scenes/cafe/cameras/cam_room_wide_overview_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；模型版本、預估與實際費用未知；單次生成。
- 有序輸入：
1. `D:/kj-openMontage/projects/course-51-esg/clp/loc_cafe_left_far.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_room_wide_overview_block_blender_v2.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`
4. `D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg`
- 觀察：George／Amy外觀與入座成立，但構圖偏向場景參考圖，未準確保留blocks；人物、桌椅畫面位置偏移，Amy雙手改交疊。未重試、未採用。
- 驗證：PNG完整解碼與輸出複本SHA256核對；尺寸1672×941 RGB。

完整實際 prompt：
```text
參考圖說明：
圖 1 loc_cafe_left_far.png：場景外觀參考圖。
圖 2 cam_room_wide_overview_block_blender_v2.png：唯一構圖與空間定位底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。銀灰頭髮、棕框眼鏡、短灰鬍鬚、米色襯衫、棕色背心與領帶、深棕褲及皮鞋。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。棕色短波浪髮、綠眼睛、灰色西裝與長褲、白襯衫、深色高跟鞋。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、家具與物件配置、人物佔位、身體朝向、比例、顯示範圍與遮擋關係。不要重新生成圖 1 的構圖。
將兩個定位人物替換為對應角色，直接坐入圖 2 的既有扶手椅，不另加椅子；人物外觀與服裝採用圖 3、4，不採用其站立展示姿態、拼圖構圖或背景。藍紅只是定位標記，不是最終服裝顏色。保留頭部與軀幹的位置及相對尺寸，不放大人物、不改為人物近景。
將場景的材質、風格與光影更新為圖 1 的外觀：細緻米灰布料扶手椅、珊瑚橘抱枕、淺木地板與桌面、白色陶瓷、霧面櫃體與金屬設備，窗外冷藍城市與室內暖光、柔和日照。光影依圖 2 的窗位合理落下。人物為與參考一致的精緻3D動畫角色，與室內光影自然融合、具有正確接觸陰影。
保持圖 2 門窗分格、天花燈帶、茶水台、冰箱、微波爐、咖啡機、層架、三個垃圾桶、所有椅子和兩張圓桌及植物的數量、位置、尺度和輪廓；在既有體積內細化材質、葉片與設備細節，不新增陳設，不將參考圖家具位置移植過來。保留前桌杯子、筆和紙本。保留近景資訊，不增加強烈散景。

畫面描述：
這是一張室內高位俯視廣角全景，左側大面積落地窗、後右側茶水台、右邊門牆與垃圾桶同框。George 位於畫面中央偏左的前排扶手椅，從其後側看見側後頭部及身體，面向右側；Amy 位於其右後方、靠茶水台前的扶手椅，身體朝向鏡頭偏George方向。兩人依定位模型維持自然坐姿，手臂與雙腿的位置沿用圖 2，不增加手勢或道具；不為了露出臉而旋轉George。前方圓桌遮擋部分Amy腿部；後排兩張空扶手椅與小圓桌維持原位。左下桌沿與高腳椅、右下局部扶手椅依底圖裁切。全圖只出現George與Amy兩位人物。

輸出一張16:9高解析度完整彩色圖片，不拼貼、不加文字、字幕、標誌或水印。
```



## 2026-10-21 cafe overview GPT v5（Cafe_2 指定美術參考）
- 狀態：待評鑑，未改採用；內建 image_gen／OpenAI，單次1張，模型版本及費用未知。
- 圖1（唯一底圖）：D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_room_wide_overview_empty_blender_v2.png
- 圖2（僅美術，不帶人物）：D:/Dropbox/_AI動畫製作_ESG/B0_MJ圖/cafe/Cafe_2.png
- 輸出：references/scenes/cafe/cameras/cam_room_wide_overview_empty_gpt_v5.png
- 驗證：PNG 1672×941 RGB，完整解碼／工具原圖複本SHA256一致。
- 觀察：零人物、四張完整椅＋右下裁切椅、兩桌、三垃圾桶保留；布料及木材質改善。構圖／家具投影略移、天花燈排列改變、窗外與植物細節重繪、冰箱多出右側把手；未完全遵守幾何保留，未重試。

### 完整實際提示詞
```text
Use case: style-transfer.
請編輯圖1，將這張Blender空景提升為圖2所呈現的精緻3D動畫電影環境質感，參考圖2的材質、色彩、光影與氣氛。
圖1 cam_room_wide_overview_empty_blender_v2.png 是唯一的取景、透視、物件配置與遮擋依據。
圖2 Cafe_2.png 僅供美術表現參考，不移植其構圖、家具排列、植物配置或人物。圖2的兩位女性絕不可出現在輸出中。
色彩與光影採用圖2的低飽和灰米色布料、珊瑚橘抱枕、奶油色桌面、柔和自然日光、略帶青藍的窗外光與克制溫暖的室內中間調。不要加成強烈金黃夕陽，不增加飽和度或泛光。保留圖1既有入光朝向，投影依本機位合理形成。
【保留本機位】
嚴格維持圖1的16:9畫幅、觀看方向、消失點、主要結構與遮擋。保留門窗分格、立柱、門把、地面邊界、家具、設備及植物的位置、數量、尺度與主要輪廓。
不旋轉相機、不鏡像、不拉遠或拉近，不移植參考圖中本鏡畫外的物件，不為展示完整物件補出被裁切部分。
【材質與細節提升】
沿用圖1構造與物件種類，改善微紋理、粗糙度、接縫、細微倒角高光、接觸陰影與反射。沙發布面呈現圖2精細而低對比的織紋，抱枕柔軟有自然接縫；淺木地板保留細緻木紋而不加花紋；奶白霧面櫥櫃、拉絲金屬冰箱、陶瓷杯罐各自有可信質感，不新增配件或重新設計家具。
植物保留位置與主要枝幹，在原有體積內細化薄葉及透光，不新增植物。避免球塊狀植物、平塗玻璃與塑膠質感。保持乾燥霧面表面，不加髒污或強鏡面反光。
作為後續加入人物的背景母圖，所有近中景資訊保持可用，不複製圖2的人像淺景深與背景虛化。
【本鏡畫面】
室內左前方高位廣角全景，左側大面落地窗，中間四張完整單人椅及兩張圓桌；另有右下角被裁切的第五張椅子與抱枕。前桌杯子與書冊、後桌小盆栽保持原位置。左下吧台與兩張凳子局部入鏡。後牆茶水台含冰箱、水槽、微波爐、咖啡機、上下櫃與兩層木層板、杯罐及垂葉；右側三個垃圾桶和門。保持圖1所有家具投影位置、大小與裁切，保持冰箱靠窗左側的上下兩把手，不新增右側手把。窗外建築維持圖1的主要輪廓與分格，提升材質即可。
【空景與輸出】
零人物，不得出現主角、路人、人體、肩膀、手臂、人物倒影或人形剪影。
只輸出一張16:9高解析度完整圖片，不製作拼貼，不加字幕、標誌或水印。
```




## 2026-10-21 shot_5.2.5 GPT v2（閱讀方向修正，待評鑑）
- 圖片：`assets/images/shot_5.2.5_gpt_v2.png`
- 工具：內建 image_gen／OpenAI；模型與費用未知；單圖編輯1次。
- 參考圖：`assets/images/shot_5.2.5_gpt_v1.png`（唯一底圖）。
- 驗證：1672×941 RGB PNG，完整解碼與來源SHA256相符。
- 目視：平板樹冠及人物倒向觀眾，企劃書照片／圖表方向亦改為Harrison閱讀方向。人物、手勢及主要背景大致保留；企劃書兩頁內容被重新編排／左右交換，非逐頁原樣旋轉，螢幕細節有重繪。保留v1，未改採用。

```text
以參考圖 shot_5.2.5_gpt_v1.png 為唯一編輯底圖，只修正平板螢幕內容與攤開企劃書內頁的閱讀方向。

Harrison 坐在桌子後方，攝影機位於桌子前方。現在平板與企劃書的內容都是朝攝影機正向，這是錯誤的。請將這兩處內容在各自表面平面內旋轉180度，使內容的頂端靠近攝影機、底端靠近Harrison。從目前鏡頭看，螢幕中的樹與人物、企劃書中的文字及圖表都應呈現倒向觀眾；Harrison 從自己的座位看則是正向可讀。

1. 平板：只將玻璃螢幕內的整幅員工與大樹畫面旋轉180度，維持原螢幕透視、邊界及亮度。員工頭部與樹冠朝向畫面下方靠近攝影機的一側，樹根朝向Harrison。不要鏡像，不改平板機身、外框、充電孔、大小、位置或角度。
2. 企劃書：保持書本原有位置、攤開狀態、書脊、封皮、頁面曲面及陰影，只將左右頁各自的印刷內容在其紙面內旋轉180度。兩頁所有文字、照片與圖表的頂端朝攝影機，讓Harrison能正向閱讀。右手食指仍觸碰原來相同的紙面位置，圖表仍在手指附近，不移動手指或書本。不鏡像，不左右交換紙張，不新增頁面。

除這兩處內容方向外，完整保留Harrison的臉、眼神、嘴部、髮型、服裝、姿態、雙手與手指，保留皮椅、桌面、窗框、大樓背景、光線、景別與裁切。不要重新構圖，不添加任何人物或物件，不加入字幕或額外疊字。輸出一張與原圖相同比例的彩色圖片。
```



## 2026-10-21 shot_5.2.6 GPT v1（待評鑑）
- 圖片：`assets/images/shot_5.2.6_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；模型與費用未知；依確認prompt逐字生成1次。
- 驗證：1672×941 RGB PNG，完整解碼與來源SHA256相符。
- 目視：單手綠色APPROVED實體章懸停、紅色ON HOLD紙面印記、暖陽呈現，紙面尚無綠章；紅印完整露出且部分壓住公司名稱，印章底面與紅印的落點對齊未能確認，未宣稱可精準覆蓋。封面主文字與原構圖大致保留。待評鑑，未改正式採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_1.1.11_gpt_v1.png`
2. `D:/kj-openMontage/projects/course-51-esg/clp/prop_stamp_approved.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/prop_stamp_onhold.png`

```text
參考圖說明：
圖 1 shot_1.1.11_gpt_v1.png：編輯底圖，提供桌面構圖、企劃書位置、Harrison 的手與袖口，以及印章懸停的姿態。
圖 2 prop_stamp_approved.png：綠色 APPROVED 印章外觀參考。
圖 3 prop_stamp_onhold.png：僅採用紅色 ON HOLD 印記樣式，不帶入紅色實體印章。

生圖指引：
以圖 1 為編輯底圖，保留原有斜俯視機位、桌面透視、木紋方向、企劃書大小、位置、封面設計與裁切，以及 Harrison 右手伸入畫面的方向。

將手中紅色 ON HOLD 實體印章替換為圖 2 的綠色 APPROVED 印章，保留自然握持關係。印章採用綠色圓潤握柄、銀色金屬長方形底座、黑色橡膠底面，正面綠底標籤清楚寫著白色「APPROVED」。只生成一枚印章，不帶入參考圖的多視角排列或獨立展示印記。

在企劃書封面加入圖 3 的紅色長方框「ON HOLD」舊印記，作為即將被核准章覆蓋的目標。本張圖片尚未完成蓋章，紙面上不可提前出現綠色 APPROVED 印記。

場景由第一幕的偏暗光線改為第五幕明亮、柔和的日間暖陽，保持相同木質桌面與企劃書材質，不改成其他房間。

畫面描述：
這是一張斜俯視的桌面蓋章特寫。合上的大成公司增資計畫書位於畫面中央偏下，沿用圖 1 的白色封面、深藍書脊、公司名稱、中文書名與淡藍綠圖形。封面閱讀方向沿用第一幕參考圖，不鏡像、不重排文字。

封面上方、公司名稱上方的留白處，已有一個清楚可辨的紅色「ON HOLD」印記，呈現略帶紙張紋理的印泥質感。印記直接附著於紙面，不是浮空字卡或貼紙。

Harrison 的右手從畫面上緣伸入，穿著原有深藍細條紋西裝，露出一小段白襯衫袖口。手指自然握緊綠色 APPROVED 印章握柄，印章底面與企劃書封面平行，停在紅色 ON HOLD 印記正上方、尚未接觸紙面的瞬間。

保持印章與紙面之間可辨識的空隙及柔和投影，紅色印記至少有部分從印章下方露出，讓觀眾看懂接下來將覆蓋的位置。不為了同時展示完整印記而將印章偏移到其他位置。

這一瞬間只呈現「準備果斷蓋下核准章」，不加入動態殘影、撞擊線、飛濺印泥或已完成的綠色紙面印記。手掌、手指與印章接觸自然，不增加手指，不讓印章懸浮於手掌之外。

焦點落在綠色印章、握持的手與封面上的紅色印記，桌面背景柔和退開。陽光在木紋與金屬底座上形成克制的暖色光澤，維持正式商務場合的質感。

畫面只有一隻手、一枚綠色實體印章與一本合上的企劃書，不加入 Harrison 的臉、其他人物、平板或紅色實體印章。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外疊字；封面原有文字、印章標籤與紅色 ON HOLD 印記保留。
```



## 2026-10-21 shot_5.2.7 GPT v1（待評鑑）
- 圖片：`assets/images/shot_5.2.7_gpt_v1.png`
- 工具：內建 image_gen／OpenAI；模型與費用未知；依確認prompt逐字生成1次。
- 驗證：1672×941 RGB PNG，完整解碼與來源SHA256相符。
- 目視：左側合上企劃書與右側平板完整入鏡，APPROVED拼字清楚、未遮主要書名，無手或實體印章、無額外片尾字卡。閱讀方向一致，員工大樹呈現；封面文字排版及螢幕細節有重繪，紅印殘痕不可見。待評鑑，未改正式採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_table_insert_iso_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/investment_office/cameras/cam_table_insert_iso_empty_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_5.2.6_gpt_v1.png`
4. `D:/kj-openMontage/projects/course-51-esg/clp/prop_stamp_approved.png`
5. `D:/kj-openMontage/projects/course-51-esg/assets/images/shot_5.2.3_gpt_v1.png`

```text
參考圖說明：
圖 1 cam_table_insert_iso_empty_gpt.png：桌面材質、場景外觀與光影參考。
圖 2 cam_table_insert_iso_empty_blender.png：桌面取景與透視底圖。
圖 3 shot_5.2.6_gpt_v1.png：合上企劃書的封面、裝訂及舊印記位置參考；不帶入手或實體印章。
圖 4 prop_stamp_approved.png：僅採用綠色 APPROVED 紙面印記樣式，不帶入實體印章。
圖 5 shot_5.2.3_gpt_v1.png：平板外觀與員工大樹螢幕畫面參考，不帶入攤開的報告。

生圖指引：
以圖 2 為編輯底圖，保留斜俯視的桌面透視、木紋方向、桌緣與背景皮椅的可見範圍。桌面材質採用圖 1，光線延續前鏡晴朗、溫暖的日間陽光，不改成夕陽或夜景。

桌面只放一本合上的增資計畫書與一台橫向平板。企劃書外觀採用圖 3；綠色核准印記採用圖 4；平板與螢幕內容採用圖 5。各參考圖僅提供指定素材，不帶入其他物件。

畫面描述：
這是一張 60mm、高角度斜俯視的桌面特寫插鏡。合上的大成公司增資計畫書位於畫面左側，橫向平板平放在畫面右側，兩件物品並排、靠近但不重疊，共同位於畫面中央。企劃書封面與平板四角完整入鏡，周圍保留少量木質桌面空間。

企劃書維持白色封面、深藍書脊、深藍公司名稱與「增資計畫書」書名，以及淡藍綠上升圖形。封面原本紅色 ON HOLD 所在的位置，現在已被一個醒目的翡翠綠長方框「APPROVED」核准印記覆蓋。綠色字母完整、清楚、拼寫正確，作為畫面的第一視覺焦點。

綠色印記自然附著於紙面，帶有細微印泥顆粒與紙張紋理，不是浮空字幕、發光字或立體牌。原紅色印記僅允許在邊緣留下極少量殘痕，不再形成另一個完整可讀的 ON HOLD，也不與 APPROVED 疊成難以辨識的混色文字。核准印記不要遮住主要書名。

平板螢幕停留在圖 5 的員工與茂密綠色大樹結尾畫面，保持人物群像、綠葉及樹幹的視覺內容，不重新設計成其他影片。畫面完全位於螢幕邊界內，遵循玻璃表面的透視，不顯示播放按鈕、進度列、通知或軟體介面。

企劃書封面與平板內容的閱讀方向一致，延續圖 5 桌面插鏡的觀看方向；這是道具特寫機位，不套用從 Harrison 對面拍攝人物時的倒向觀眾畫面。文字與螢幕內容不鏡像，兩件物品自然平貼桌面，有柔和接觸陰影。

溫暖日光在木紋、白色紙面與平板金屬邊緣留下柔和光澤，不產生遮住核准文字或螢幕的強烈反光。焦點落在 APPROVED 印記與平板畫面，遠處桌面及皮椅略微柔化，整體明亮、安定，呈現事情圓滿落定的餘韻。

畫面不出現人物、手、實體印章、電話或其他新增道具。Harrison 的台詞屬於畫外音，不以文字或人物呈現在圖片中。

輸出一張 16:9 彩色分鏡圖，維持完整亮度，不做淡出、不加黑色漸層，不加入 THE END、字幕、片尾標語或額外疊字；保留企劃書原有文字與綠色 APPROVED 印記。
```



## 2026-10-21 shot_3.8.13 GPT v1（待評鑑）
- 圖片：`assets/images/shot_3.8.13_gpt_v1.png`，1672×941 RGB PNG。
- 依使用者確認的 prompt 原文生成 1 次；內建 image_gen／OpenAI，模型版本與費用未知。
- 完整解碼及來源 SHA256 比對通過。目視：單人、雙掌向上與微笑呈現；視線偏左上，人物位置／比例及肩膀輪廓偏離 blocks，背景有重繪。待使用者評鑑，未改正式採用。
- 有序參考圖：
1. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_empty_gpt.png`
2. `D:/kj-openMontage/projects/course-51-esg/references/scenes/street/cameras/cam_george_mcu_45deg_block_blender.png`
3. `D:/kj-openMontage/projects/course-51-esg/clp/char_george.png`

### 完整 prompt
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：街道場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色定位人物。

生圖指引：
以圖 2 為編輯底圖，保留取景、透視、背景物件配置、人物位置與比例、頭頂留白、肩膀位置及畫面裁切。不拉近鏡頭，不放大人物。

將藍色定位人物替換為圖 3 的 George。人物五官、髮型、眼鏡、鬍鬚與服裝依圖 3，保留精緻 3D 動畫質感，不採用人物參考圖的展示姿態或多格構圖。只呈現本鏡取景內的身體部位。

將場景材質、風格與光影更新為圖 1 的外觀，空間配置與遮擋關係沿用圖 2。保留玻璃門、石材立柱與沿街花台的位置，以及溫暖自然日光。

畫面描述：
眼高平視、斜側約 45 度的 George 單人中特寫。頭部、肩膀與胸前區域入鏡，人物尺度與頭頂留白依圖 2，下半身位於畫外。畫面只有 George 一人，Amy 位於畫左鏡外。

George 正向 Amy 說明 ESG 能提升同事的競爭力，讓工作更有價值。他眉頭舒展，眼神明亮而專注，嘴角帶著自信、溫和的微笑，嘴唇自然微張，呈現真誠鼓勵對方的神情。

頭部略朝畫左，下巴自然水平，雙眼看向畫左鏡外、與自己眼睛高度相近的 Amy。視線保持水平，不看天空，也不看鏡頭。

雙肘彎曲，雙手在胸前偏下的位置自然分開，掌心朝上，手指放鬆微彎，呈現即將向上托舉的起始姿態。手掌空著，手勢自然開闊，不遮住臉部。允許為此調整手臂與手掌，其餘肩膀、軀幹位置及人物尺度沿用圖 2；不為了展示手肘而改變取景。

焦點落在 George 的眼睛與表情，背景玻璃門、石柱及綠植柔和失焦。只呈現這個同時成立的瞬間，不加入動作殘影、上升箭頭或概念圖示。

輸出一張 16:9 彩色分鏡圖，不加入字幕、字卡、對話框或浮水印。
```



### 2026-10-21 cafe table action 空景重繪（待評鑑）
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_twoshot_table_action_empty_gpt.png
- 工具：內建 image_gen／OpenAI；模型版本與費用未知；一次生成。
- 有序輸入：1. references/scenes/cafe/cameras/cam_twoshot_table_action_empty_blender.png；2. clp/loc_cafe_left_far.png
- 格式／尺寸：PNG (1672, 941)；完整解碼及來源複本SHA256通過。
- 觀察：四椅兩桌與零人物保留；布料與暖光貼近參考。椅子輪廓及窗外建築細節變動、日照較強；前杯疑似出現雙杯耳，未完全符合單耳要求。未重試、未改採用。
- 完整實際提示詞：

請編輯圖1，將本機位Blender空景轉成與圖2同一套精緻3D動畫電影美術的場景背景。
圖1 cam_twoshot_table_action_empty_blender.png 唯一決定相機位置、觀看方向、透視、構圖、畫面裁切及物件配置。
圖2 loc_cafe_left_far.png 是美術參考，只提供材質、色彩、光影與氣氛。不要採用圖2的拍攝角度、消失點、畫面排列或可見範圍，不要重新生成圖2。
匹配圖2的米灰色細織布沙發、珊瑚橘柔軟布抱枕、象牙白圓桌與陶瓷花盆、淺色木地板及木桌柱、自然綠植、冷藍玻璃城市背景，日光溫暖柔和而不過度橙黃。依圖1朝向與投影維持合理光源方向，不把圖2光斑直接貼上。
【保留本機位】
維持圖1的16:9畫幅、觀看方向、消失點、主要結構與遮擋。保留可見窗分格、立柱、家具及植物的位置、數量、尺度和主要輪廓。不旋轉相機、不鏡像、不拉遠或拉近。不移植圖2畫外的茶水台、冰箱、廚櫃、門、垃圾桶或天花板。不要為展示完整物件而補出被畫框裁切部分。
【材質與細節提升】
沿用圖1構造和物件種類，改善細織布紋理、柔軟抱枕皺褶、接縫、細微倒角高光、接觸陰影與玻璃反射。保持霧面、乾燥、潔淨質感與合理紋理尺度。植物保留既有種類、盆器位置、主要枝幹與體積，只細化葉片透光和葉緣。窗外建築保持原有主要輪廓與位置，改善玻璃材質與細節。保持近中景清楚，作為後續加入人物的背景，不額外強化散景。
【本鏡畫面】
從稍高位置朝向落地窗拍攝四張米灰單人沙發，每張一個珊瑚橘靠枕。前方左右兩椅較大、後方左右兩椅較小，兩組座椅各配一張象牙白圓茶几，必須保持這個前後透視與椅子朝向。前茶几居中偏下、底座在下緣裁切，桌面保留左側一只咖啡杯（僅一個杯耳）、右側一本閉合淺色筆記本及其上方一支黑筆；後茶几保留小盆栽和疊放書冊。左邊低矮綠植與細長多枝高植栽、右邊低矮綠植均依圖1位置及裁切。前景沙發扶手、坐墊及桌邊界不得移位，不加椅子或桌子。
【空景輸出】
零人物，無人體、肩膀、手臂、人物倒影或人形剪影。只輸出一張16:9高解析度完整圖片，不拼貼、不加字幕、標誌或水印。


### 2026-10-21 cafe batch restyle: cam_amy_cu_emotion_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_amy_cu_emotion_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_amy_cu_emotion_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：空景與緊裁切保留；窗外建築細格與亮度改變，暖光偏強，冰箱輪廓略移；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：緊裁切窗景與冰箱，冰箱在右半並被上方及下方畫框裁切，左邊是窗框和藍色建築；下緣只有少量珊瑚靠枕、沙發局部及綠葉。維持狹窄取景，不加入完整座椅、茶几或地板。


### 2026-10-21 cafe batch restyle: cam_amy_gesture_ms_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_amy_gesture_ms_empty_blender_v1.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_amy_gesture_ms_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：零人物、前後兩椅及左桌右冰箱關係保留；布紋較強、日照較亮，椅輪廓與窗外細格略變；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：主沙發在中央偏右前景，左後另一椅，左下小圓桌有盆栽與兩本書，右邊冰箱和局部茶水櫃，背景落地窗。保持前椅底部裁切、後椅遮擋及桌邊裁切，不擴展視野。


### 2026-10-21 cafe batch restyle: cam_amy_mcu_45deg_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_amy_mcu_45deg_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_amy_mcu_45deg_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：零人物、近景裁切及兩椅局部保留；抱枕變軟、日光加強、窗外新增遠處建築細節；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：中近景底部被裁切的前椅珊瑚抱枕與左後椅，中央綠葉、左側大片米色柱牆，中間窗格，右上冰箱兩門局部與靠窗把手，最右檯面一角。不得補出完整沙發、桌面或地板；維持原裁切。


### 2026-10-21 cafe batch restyle: cam_amy_ms_15deg_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_amy_ms_15deg_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_amy_ms_15deg_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：零人物與兩椅近景保留；靠枕比例和布紋略變、窗景細節及日照較強，白圓筒被細化為紙巾捲；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：中央偏右前椅珊瑚靠枕與左後椅形成前後遮擋，底部裁切坐墊；左半米色柱和落地窗，右上冰箱及右側局部上下櫃，檯上只有原有白色圓筒，椅後少量綠葉。不得補完整椅腳、茶几或增加桌上道具。


### 2026-10-21 cafe batch restyle: cam_amy_ots_george_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_amy_ots_george_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_amy_ots_george_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：空景與茶水台配置保留，紙杯兩柱清楚；暖燈及斜向日光加強，沙發輪廓與設備比例略變；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：向茶水台拍攝的空景中景，前方中央沙發與珊瑚抱枕、左下另一抱枕裁切。背景上櫃、左冰箱、檯上白圓筒和水龍頭、中央偏右微波爐、兩柱紙杯堆及最右裁切咖啡機。上右層板盆栽及杯依底圖數量位置，保留器具完整形狀。無人物肩膀，不補出咖啡機右側畫外部分。


### 2026-10-21 cafe batch restyle: cam_amy_ots_george_mcu_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_amy_ots_george_mcu_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_amy_ots_george_mcu_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：空景緊裁切、微波爐與單柱紙杯保留；白筒新增紙巾架細節、檯面光影更強，抱枕布紋偏密；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：茶水台緊近景，上櫃在頂部裁切、微波爐中央偏右、水龍頭偏左，左白色圓筒，右緣僅一柱紙杯，極左只有冰箱窄邊；底部只露前椅靠枕和椅背。保留此緊裁切，不能增加咖啡機、第二柱紙杯或完整沙發。

### 2026-10-21 cafe batch restyle: cam_amy_writing_ms_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_amy_writing_ms_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_amy_writing_ms_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：四椅兩桌、單耳杯與空景保留；布紋增強、椅輪廓略變、窗外和地板日照細節變化；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：略高斜俯拍四張單人沙發，左前椅在左邊和下方裁切，右前椅完整坐墊可見，後排兩椅之間小圓桌上盆栽與書，前茶几在下緣被裁切，含一只單耳咖啡杯、黑筆及閉合筆記本。右上植物與冰箱一角，背後落地窗。保持四椅兩桌的座標和裁切，不改成參考圖的全室廣角。

### 2026-10-21 shot_3.2.5 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.2.5_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；1 次生成。
- 有序參考圖：
  1. references/scenes/cafe/cameras/cam_amy_mcu_45deg_empty_gpt.png
  2. references/scenes/cafe/cameras/cam_amy_mcu_45deg_block_blender.png
  3. clp/char_amy.jpeg
- 驗證：1672×941 RGB PNG，完整解碼及來源副本 SHA256 通過。
- 觀察：雙手抓髮、皺眉張嘴與單人構圖呈現；視線偏左上，人物縮小且雙肘入鏡，肩膀位置及背景遮擋偏離 blocks。未重試、未改正式採用。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：cafe 場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy（char_amy）人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將紅色定位人物替換為 Amy，人物外觀與服裝採用圖 3，不採用其展示姿態、微笑或構圖。保留圖 2 的頭部大小、肩膀位置與頭頂留白；雙手依下述抱頭動作調整，不為容納手臂而縮小人物或拉遠鏡頭。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置，不採用 blocks 的方塊材質與簡化人物外觀。

畫面描述：
這是一張坐姿近眼高、65mm 固定鏡位的 Amy 單人頭肩近景。Amy 位於畫面中央，頭部、雙肩與部分上胸入鏡，下半身及桌面在畫外。背景保留同機位的落地玻璃、窗外高樓、右側冰箱、局部茶水台與座椅靠墊，使用淺景深突出人物。

Amy 剛聽完繁雜的 ESG 盤點項目，呈現倒抽一口涼氣、焦慮得頭皮發麻的瞬間。雙手抬至頭部兩側，手指張開並微彎，抓住兩側髮絲，掌心靠近頭側；手掌不遮住眼睛與臉部，前臂由畫面下緣進入，手肘可留在畫外。眉心緊皺、內側眉頭抬起，雙眼略睜大，嘴唇張開吸氣，嘴角不帶笑，表情是難以負荷又無可奈何。

Amy 的視線投向畫面左側、與她坐姿高度相近的畫外 George，不仰望上方。George 完全不入鏡，畫面只呈現 Amy 一人，不加入其他人物。除上述手臂、手部與表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外文字。
```




### 2026-10-21 cafe batch restyle: cam_coffee_handoff_insert_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_coffee_handoff_insert_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_coffee_handoff_insert_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：單杯單耳與裁切保留、零人物；沙發布紋較粗、日光陰影強於底圖，桌緣及杯比例略變；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：近距離斜俯拍茶几咖啡杯，杯在中央偏下只有一個朝鏡頭杯耳，圓桌下右出畫，右側黑筆和筆記本僅部分入鏡。左上沙發坐墊與扶手局部，後方只有另一茶几木柱及白底座。保留緊裁切，不補人物、不加第二個杯耳、不補窗景或完整沙發。

### 2026-10-21 shot_3.2.5 GPT v2（待評鑑）
- 輸出：assets/images/shot_3.2.5_gpt_v2.png
- 工具：內建 image_gen／OpenAI；模型與費用未知；1次 I2I。
- 有序參考圖：1. assets/images/shot_3.2.5_gpt_v1.png；2. references/scenes/cafe/cameras/cam_amy_mcu_45deg_block_blender.png
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過。
- 觀察：已拉近，雙肘畫外，雙手抓髮與焦慮保留；視線仍偏左上，未達水平看左要求；頭頂略裁切、較原 blocks 更緊。未重試、未改正式採用。
- 完整 prompt：
```text
請編輯圖 1（shot_3.2.5_gpt_v1.png），圖 2（cam_amy_mcu_45deg_block_blender.png）只提供目標頭肩近景的取景尺度與頭頂留白，不採用圖 2 的人物造型、材質或手勢。
僅做以下兩項修改：
1. 將 Amy 的視線從左上方降到畫面左側同高度的畫外 George。雙眼虹膜和瞳孔向左平移、垂直位置回到眼裂中央，視線水平向左，不抬眼、不看左上方。頭部維持自然平視，必要時略收下巴以消除仰望感；George 不入鏡。保留皺眉、內眉抬起、焦慮無奈與張嘴倒抽氣的表情。
2. 拉近成圖 2 的頭肩近景：Amy 的頭與臉明顯放大，頭頂保留少量空間，下緣裁到肩膀及少量上胸，雙肘完全留在畫面下方之外。雙手仍在頭的兩側抓髮抱頭，手指和手掌完整可見、不遮臉，前臂從畫面下緣進入，不為容納雙肘而縮小人物。不要裁掉頭頂。
保留圖 1 的 Amy 身分、五官、髮色、灰色西裝與白襯衫、雙手抱頭抓髮的動作、焦慮表情，以及咖啡館的色彩、材質與日光；背景只隨拉近取景合理裁切，不重新設計家具或增加物件。畫面只有 Amy 一人。
輸出一張 16:9 彩色圖片，不加字幕、文字或水印。
```




### 2026-10-21 cafe batch restyle: cam_george_cu_emotion_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_george_cu_emotion_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_george_cu_emotion_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：柱窗與枝幹緊裁切成立、無新增家具人物；牆面亮度提升、窗外細格與葉形改變；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：純窗戶及立柱緊裁切：中央偏右一大片米色立柱，左半冷藍近樓立面，右緣細長金棕植物枝幹與少量葉片，底緣綠葉局部。沒有沙發、桌子或地板入鏡，絕對不要新增。保留柱寬、窗框位置、枝幹數與裁切。


### 2026-10-21 cafe batch restyle: cam_george_gesture_ms_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_george_gesture_ms_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_george_gesture_ms_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：兩椅及植物主配置、零人物保留；遠處新增建築細節、抱枕輪廓與光照改變；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：窗邊兩張前後排列單人沙發，前椅居左中、後椅居右中，珊瑚色靠枕；前椅底部被裁切，最右小圓桌與盆栽只露一角。中央後方三枝細長植物，上方葉片裁切；米色柱及藍色窗景按圖1保持。不加入茶水台或更多椅子。


### 2026-10-21 cafe batch restyle: cam_george_mcu_45deg_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_george_mcu_45deg_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_george_mcu_45deg_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：近景裁切與零人物保留；植物葉形較自然但分布變化、柱面光影增強，窗外細格不同；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：窗景緊中近景：米色柱在中央偏左，右半三枝細長植栽與裁切葉片，左下低矮植物；底邊僅露前椅珊瑚靠枕頂部，右下後椅局部。保持這些裁切，不補坐墊、地板、桌子或人物。


### 2026-10-21 cafe batch restyle: cam_george_ms_15deg_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_george_ms_15deg_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_george_ms_15deg_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：前後椅與植栽位置大致保留、零人物；抱枕高度形狀略變、窗外細節與日照增加；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：窗邊兩椅中景：前椅在左中且底部裁切、後椅在右邊裁切，各有珊瑚靠枕。中央偏右有三枝高植物與底盆一部分，中央米色柱，左側藍樓窗景。保留椅背高度和左右比例，不增加完整茶几、人物或茶水台。


### 2026-10-21 cafe batch restyle: cam_george_ots_amy_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_george_ots_amy_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_george_ots_amy_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：空景、吧台兩凳與前椅保留；白杯杯耳轉可見、黑色扁物變書冊外觀、窗外樓群細節與抱枕輪廓變化；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：窗邊吧台方向：底部中央前椅珊瑚抱枕及椅背，右下大盆綠植、最右下少量另一抱枕；左中木吧台，檯上原有一白杯和一扁平黑物，下面兩張圓坐墊高腳凳。窗外樓群維持配置，無人物肩膀，不補畫外家具。

### 2026-10-21 shot_3.2.6 GPT v1（待評鑑）
- 輸出：assets/images/shot_3.2.6_gpt_v1.png
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；1次 W2I。
- 有序參考圖：1. references/scenes/cafe/cameras/cam_george_cu_emotion_empty_gpt.png；2. references/scenes/cafe/cameras/cam_george_cu_emotion_block_blender.png；3. clp/char_george.png
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過。
- 觀察：單人、閉嘴微笑、眼鏡與雙手畫外呈現；視線略偏右上，人物較blocks縮小、肩胸露出較多，頭頂留白及背景遮擋偏離blocks。未重試、未改採用。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：cafe 場景外觀參考圖。
圖 2 cam_george_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_george.png：George（char_george）人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將藍色定位人物替換為 George，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態、嚴肅表情或構圖。保留他的銀灰頭髮、深棕方框眼鏡與白色短鬍鬚。維持圖 2 的頭部尺度、頭頂留白與肩膀裁切，不縮小人物或拉遠鏡頭。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置，不採用 blocks 的方塊材質與簡化人物外觀。

畫面描述：
這是一張坐姿近眼高、100mm 固定鏡位的 George 單人臉部特寫。George 位於畫面中央，頭部與臉佔據主要畫面，頭頂完整保留，只在畫面底部露出頸部、衣領與少量肩膀，肩膀下緣裁切；胸口、雙臂及雙手都在畫外。背景為同機位的落地玻璃、窗外高樓、米色立柱及局部盆栽，以淺景深突出臉部與眼神。

George 聽完 Amy 對人力不足的擔憂，呈現準備輕輕點頭回應的起始瞬間。頭部自然端正，下巴放鬆，嘴唇輕合、嘴角微微上揚，眉心舒展，眼神溫暖而篤定，流露「我理解妳的擔心」的同理與安撫，不露齒大笑。

George 看向畫面右側、坐姿眼睛高度相近的畫外 Amy；雙眼自然朝右平視，不往右上方看，也不直視鏡頭。眼鏡鏡片保持通透，清楚看見眼神。Amy 完全不入鏡，畫面只有 George 一人，不加入背景顧客或咖啡師。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外文字。
```




### 2026-10-21 cafe batch restyle: cam_george_ots_amy_mcu_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_george_ots_amy_mcu_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_george_ots_amy_mcu_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：吧台、單杯與底緣座椅裁切保留，零人物；窗外玻璃細節增加，木紋及日照更強；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：窗邊吧台緊近景：藍色樓群充滿背景，木吧台從左延至中央偏右，上面只一只白杯，底邊只露兩凳坐墊局部和前椅珊瑚靠枕頂部。不得補出整椅、桌腿全貌或新增書冊，保持窗框與吧台高度。

## 2026-10-21 shot_3.1.2 GPT v1（待評鑑）
- 圖片：assets/images/shot_3.1.2_gpt_v1.png
- 工具：內建 image_gen／OpenAI；1 次生成，模型與費用未知。
- 觀察：雙人過肩與胸前交疊握拳呈現；Amy 視線略偏左上，人物比例與 George 前景遮擋偏離 blocks，背景細節重繪。未改正式採用。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_amy_ots_george_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_amy_ots_george_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
4. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整 prompt（使用者原文）：
```text
參考圖說明：
圖 1 cam_amy_ots_george_empty_gpt.png：新潮咖啡館 cafe 場景外觀參考圖。
圖 2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 中央偏右的紅色人物。
圖 4 char_george.png：George 人物參考圖，對應圖 2 左前景的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、家具配置、人物佔位、整體大小、可見範圍與遮擋關係。保持 George 左前景頭肩的裁切及 Amy 的位置，不移動前景人物來增加 Amy 的可見面積，不推近鏡頭。

將定位人物替換為對應角色。Amy 外觀與服裝採用圖 3，George 採用圖 4，不採用人物參考圖的展示姿態或排版。George 只呈現原本入鏡的後腦、頸部與肩背，不轉向鏡頭露出正臉。

場景材質、色彩與光影依圖 1，保留茶水台、吊櫃、開放層架、微波爐及咖啡機的原有配置。維持日間柔和自然光，淺景深聚焦 Amy，背景與前景 George 適度柔化。

畫面描述：
這是一張 60mm、坐姿平視、越過 George 肩膀拍 Amy 的過肩畫面。George 頭肩佔據左前景，Amy 坐在中央偏右的扶手椅上，保持圖 2 的身體尺度與遮擋關係。畫面共兩人。

Amy 帶著被看穿心思後不好意思的苦笑，眉毛內側輕微抬起，嘴角略帶羞赧地上揚。她看向左前景 George 的臉，視線維持對坐交流的高度，不仰望或看鏡頭。

她雙手在胸前交疊握拳，一手握成拳，另一手包覆拳頭，呈現拜票式拱手拜託的姿態，誠懇拜託顧問指點的姿態。允許前臂與手掌從原本低放位置抬起，其餘坐姿與軀幹位置沿用圖 2。手部被 George 遮住的部分保持遮擋，不將雙手移到臉旁或改變鏡位來展示完整手勢。

George 保持面向 Amy 聆聽的姿態。除上述表情、視線與合十手勢外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或分格。
```


### 2026-10-21 cafe batch restyle: cam_hands_insert_iso_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_hands_insert_iso_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_hands_insert_iso_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：四椅局部與兩桌、單杯黑筆保留、零人物；地板日照加強、織紋密度偏高、窗外細節增加；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：低位斜俯拍四椅坐墊及扶手局部，上方椅背被裁切；後方中央小圓桌有盆栽和兩本書。前茶几在底部只露上緣及一只部分裁切咖啡杯、黑筆、筆記本一角。保留四椅兩桌關係與緊裁切，不補椅背、窗景或人體手臂。


### 2026-10-21 cafe batch restyle: cam_notebook_writing_insert_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_notebook_writing_insert_empty_blender_v1.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_notebook_writing_insert_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：俯拍閉合筆記本與黑筆、上緣杯裁切保留，零人物；桌面／地板紋理和斜向日照明顯增強；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：高位斜俯拍近距離圓桌，閉合淺色筆記本在右下中央，黑筆在其右上，桌圓弧及底座保持原透視；咖啡杯僅在最上緣露底部裁切。右邊沙發局部、周圍淺木地板。不得打開筆記本、加文字、加手、補整杯或改俯拍角度。


## 2026-10-21 shot_3.1.4 GPT v1（待評鑑）
- 圖片：assets/images/shot_3.1.4_gpt_v1.png
- 工具：內建 image_gen／OpenAI；1 次生成，模型與費用未知。
- 觀察：微張嘴微笑、單人與雙手畫外呈現；視線略偏右上，人物較 blocks 縮小、肩胸露出較多，背景細節重繪。未改正式採用。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_george_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_george_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整 prompt（使用者原文）：
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：新潮咖啡館 cafe 場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、整體大小、頭頂留白、肩膀位置及畫面下緣裁切。保持原有頭肩近景，不拉遠展示手臂或桌面，不放大頭部。

將藍色定位人物替換為 George，五官、髮型、眼鏡、鬍鬚與服裝採用圖 3，不採用其展示姿態或參考圖排版。只呈現圖 2 中可見的身體範圍。

場景材質、色彩與光影依圖 1，保留落地玻璃、窗外高樓、竹節盆栽與原可見椅背的配置。維持日間柔和自然光，淺景深聚焦 George 的眼神與表情，背景適度柔化。

畫面描述：
這是一張 65mm、坐姿近眼高的 George 單人頭肩近景。頭部與肩膀依圖 2 的位置及比例呈現，身體下部與雙手保持在畫外。畫面只出現 George，Amy 位於畫外右側。

George 面帶溫和、從容的微笑，雙頰自然微抬，嘴唇輕微張開，呈現輕笑一聲、準備開始說明的瞬間。他的頭部略朝畫外右側 Amy，雙眼看向與自己坐姿眼高相近的對話者，不看鏡頭、不向上望。表情親切而沉穩，帶著有把握引導對方理解的神情。

此刻雙手仍低放在畫外，尚未抬手比出五指，保留後續講到五個步驟時抬手的動作空間。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或分格。
```



### 2026-10-21 cafe batch restyle: cam_pantry_ambience_front_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_pantry_ambience_front_empty_blender_refined_v1.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_pantry_ambience_front_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：設備排列、兩柱紙杯與空景保留；檯面陰影與燈光更強，藤蔓延長，水槽／杯器細節略變；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：正面茶水台設備近景：左水槽與龍頭、白筒，中央微波爐，右咖啡機與滴水盤，兩者之間兩柱紙杯堆，右邊另有白杯裁切。上櫃與木層板依圖1數量；層板五只杯各僅一耳、左小盆栽、右垂藤保持位置。頂部罐子只露部分，底櫃裁切。沒有冰箱、沙發、窗戶入鏡，不得添加。設備比例、杯數與層板高度依圖1。


### 2026-10-21 cafe batch restyle: cam_room_wide_overview_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_room_wide_overview_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_room_wide_overview_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：主要家具數量及廣角空景保留；家具輪廓／尺度略移、窗外細節與日照增強，紙杯堆疊細節不清。；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：房間全景，必須依圖1更高更廣的相機，切勿照搬圖2視角。左側落地窗與三盆落地植物、中央四椅兩圓桌，前左吧台及兩凳局部、右下額外沙發一角。後右茶水台、靠窗冰箱、上下櫃與兩層板、三只分類桶與最右門框；天花四段線燈及通風口保持圖1位置，不套用圖2天花燈。保留地面大留白、所有家具尺寸位置、四椅朝向；前桌單耳杯、筆記本黑筆，後桌盆栽書冊。


### 2026-10-21 cafe batch restyle: cam_table_insert_top_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_table_insert_top_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_table_insert_top_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：俯拍構圖、單耳杯、黑筆與閉合無字筆記本保留；桌面及地板日光陰影增強，沙發布紋較粗。；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：垂直俯拍圓桌，圓形桌面幾乎填滿畫面且上下裁切。左側只有一個單杯耳咖啡杯、杯耳朝下；右上斜放一支黑筆，右下閉合無字筆記本。沙發只在左上、右緣局部入鏡，周圍淺木地板；維持各物件角度、尺寸、位置與裁切，不加杯碟、文字、手或其他物件。

### 2026-10-21 cafe batch restyle: cam_twoshot_ms_level_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_twoshot_ms_level_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_twoshot_ms_level_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：四椅與前桌底緣裁切保留，杯子單杯耳；窗外新增遠處樓群、日照與布料紋理增強，椅背輪廓略變。；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：水平雙人中景空景，前景左右兩張沙發大幅裁切，後方左右另兩張沙發與中央小圓桌，桌上小盆栽和兩本書。前桌只在畫面底緣局部露出，單耳咖啡杯左下、黑筆右下，勿補出整張桌或筆記本。左緣高植物、後方冷藍窗與右立柱；保留圖1窗戶大留白及四張椅子遮擋，不放人物。

### 2026-10-21 shot_3.3.2 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；本鏡1次。
- 輸出：assets/images/shot_3.3.2_gpt_v1.png
- 有序參考圖：1. references/scenes/cafe/cameras/cam_george_ots_amy_empty_gpt.png；2. references/scenes/cafe/cameras/cam_george_ots_amy_block_blender.png；3. clp/char_george.png；4. clp/char_amy.jpeg
- 結果：雙手掌心相對呈現；George 偏左且人物尺度、頭部傾斜與 Amy 前景遮擋偏離 blocks。
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過；未重試、未改採用。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_george_ots_amy_empty_gpt.png：cafe 場景外觀參考圖。
圖 2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖 3 char_george.png：George（char_george）人物參考圖，對應圖 2 的藍色人物。
圖 4 char_amy.jpeg：Amy（char_amy）人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將藍色定位人物替換為 George，紅色定位人物替換為 Amy。人物外觀與服裝分別採用圖 3、圖 4，不採用人物參考圖的展示姿態或構圖。只呈現圖 2 中可見的身體範圍，不補出被遮擋或畫外的部位。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置，不採用 blocks 的方塊材質與簡化人物外觀。

畫面描述：
這是一張 60mm 固定鏡位、坐姿略帶俯角的過肩對談畫面，從 Amy 身後拍攝 George。Amy 的後腦、頸部與肩背佔據右側前景，頭頂及身體依圖 2 裁切；George 坐在對面、居中偏左，上身與原本可見的手部入鏡，部分身體被 Amy 遮擋。保留兩人原有大小差、座位距離與遮擋，不將 Amy 縮成畫面邊緣的一小片肩膀。

George 神情誠懇而務實，眉眼專注、嘴唇微張，視線朝畫面右側的 Amy，維持坐姿同高度的對視。呈現收攏聚焦手勢的起始瞬間：雙手在身前低處稍微抬起，掌心相對、手指自然放鬆，兩掌仍有間距，準備向內收攏；手部只在原構圖允許的範圍內呈現，被前景遮擋的部分保持遮擋，不刻意伸到 Amy 前方。

Amy 保持面向 George 的聆聽姿態，只呈現原本可見的後腦與肩背，不轉頭向鏡頭展示正臉。焦點落在 George，前景 Amy 柔和失焦。背景保留落地玻璃、窗外高樓、窗邊吧檯與高腳椅，畫面僅有這兩人。除上述 George 手部與表情調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外文字。
```

### 2026-10-21 shot_3.3.3 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；本鏡1次。
- 輸出：assets/images/shot_3.3.3_gpt_v1.png
- 有序參考圖：1. references/scenes/cafe/cameras/cam_amy_cu_emotion_empty_gpt.png；2. references/scenes/cafe/cameras/cam_amy_cu_emotion_block_blender.png；3. clp/char_amy.jpeg
- 結果：好奇微張嘴呈現；視線偏左上，人物較 blocks 縮小，胸肩露出過多。
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過；未重試、未改採用。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_cu_emotion_empty_gpt.png：cafe 場景外觀參考圖。
圖 2 cam_amy_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy（char_amy）人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將紅色定位人物替換為 Amy，人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。保持圖 2 的臉部特寫尺度、頭頂留白與肩膀裁切，不縮小人物，不補出胸口、雙臂或雙手。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置，不採用 blocks 的方塊材質與簡化人物外觀。

畫面描述：
這是一張坐姿眼高、100mm 固定鏡位的 Amy 單人臉部特寫。Amy 位於畫面中央，頭部與臉佔據主要畫面，完整保留頭頂，下緣只露出頸部、衣領及少量肩膀，雙手完全在畫外。

Amy 聽到可以優先處理關鍵議題，眼睛一亮，呈現剛開始微微前傾、準備追問的瞬間。前傾幅度輕微，不使頭頂越出畫框；眉毛自然略抬，眉心放鬆，雙眼專注而明亮，嘴唇微微張開，表情是好奇、期待與積極求知，不延續上一場抱頭崩潰的神情，也不誇張大笑。

Amy 看向畫面左側、與她坐姿眼睛高度相近的畫外 George，視線水平朝左，不往左上方看、不直視鏡頭。George 完全不入鏡，畫面只有 Amy 一人。背景保留落地玻璃、窗外高樓、冰箱及茶水台邊緣，淺景深聚焦 Amy 的眼神。除上述輕微前傾、表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外文字。
```

### 2026-10-21 shot_3.3.4 GPT 生成失敗
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；本鏡1次。
- 輸出：無
- 有序參考圖：1. references/scenes/cafe/cameras/cam_george_mcu_45deg_empty_gpt.png；2. references/scenes/cafe/cameras/cam_george_mcu_45deg_block_blender.png；3. clp/char_george.png
- 結果：生成失敗：http 400 moderation_blocked，moderation_stage=output，categories=[other]；request ID 4468022c-a444-4986-bf41-b0dec5b6458c。無輸出，未重試。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：cafe 場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George（char_george）人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將藍色定位人物替換為 George，人物外觀與服裝採用圖 3，不採用其展示姿態、嚴肅表情或構圖。保留銀灰頭髮、深棕方框眼鏡與白色短鬍鬚。維持圖 2 的頭部尺度、肩膀位置及頭頂留白，只呈現原本可見的身體部位。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置，不採用 blocks 的方塊材質與簡化人物外觀。

畫面描述：
這是一張坐姿眼高、65mm 固定鏡位的 George 單人頭肩近景。George 位於畫面中央略偏左，頭頂完整入鏡，下緣呈現雙肩及部分上胸；雙手留在畫外，不增加手勢，也不拉遠鏡頭。

George 準備向 Amy 解釋專業的篩選方法，姿態從容端正，嘴角帶著克制的微笑，嘴唇輕合，眉心放鬆，眼神清晰而自信，呈現沉穩、可信賴的導師神情。視線朝畫面右側、與他坐姿眼睛高度相近的畫外 Amy，自然平視，不看右上方、不直視鏡頭。眼鏡鏡片通透，眼神清楚可見。

Amy 完全在畫外，畫面只呈現 George 一人。背景保留落地玻璃、窗外高樓、立柱與竹節盆栽，淺景深聚焦 George。除上述表情與視線調整外，其餘沿用圖 2，不為字卡重新安排人物位置或增加留白。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或文字；「重大性分析 (Materiality Analysis)」字卡由後製疊加，不生成在圖片內。
```

### 2026-10-21 shot_3.3.10 GPT v1（待評鑑）
- 工具／供應商：內建 image_gen／OpenAI；模型與費用未知；本鏡1次。
- 輸出：assets/images/shot_3.3.10_gpt_v1.png
- 有序參考圖：1. references/scenes/cafe/cameras/cam_amy_ots_george_empty_gpt.png；2. references/scenes/cafe/cameras/cam_amy_ots_george_block_blender.png；3. clp/char_amy.jpeg；4. clp/char_george.png
- 結果：拍手前雙掌分開與開心表情呈現；Amy 視線偏左上、人物與雙手露出範圍增加，George 遮擋偏離 blocks。
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過；未重試、未改採用。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_ots_george_empty_gpt.png：cafe 場景外觀參考圖。
圖 2 cam_amy_ots_george_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy（char_amy）人物參考圖，對應圖 2 的紅色人物。
圖 4 char_george.png：George（char_george）人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將紅色定位人物替換為 Amy，藍色定位人物替換為 George。人物外觀與服裝分別採用圖 3、圖 4，不採用人物參考圖的展示姿態或構圖。只呈現圖 2 中可見的身體範圍，不補出被遮擋或畫外的部位。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置，不採用 blocks 的方塊材質與簡化人物外觀。

畫面描述：
這是一張坐姿平視、60mm 固定鏡位的過肩對談畫面，從 George 身後拍攝 Amy。George 的後腦、頸部與肩背佔據左側前景，頭頂與身體依圖 2 裁切；Amy 坐在對面、居中偏右，上身入鏡，部分身體被 George 遮擋。保留兩人的原有尺度、座位距離與遮擋，不縮小或移開 George 來讓 Amy 全身露出。

Amy 聽懂重大性分析後豁然開朗，雙眼明亮、眉毛略抬，嘴角上揚、嘴唇微張，神情開心而充滿幹勁。視線朝畫面左側、坐姿同高度的 George，不仰望上方。呈現第一次拍手之前的準備瞬間：雙手已抬至胸前、掌心相對，兩掌尚未接觸，手指自然伸展，準備合掌拍一下；頭部保持自然，為後續點頭動作保留起始姿態。

允許 Amy 的前臂與手部為拍手準備姿態調整，其餘頭部位置與軀幹佔位沿用圖 2。雙手被 George 肩背遮住的部分保持遮擋，不將手移到 George 前方，也不橫移人物或擴張取景來露出雙手。

George 維持面向 Amy 的聆聽姿態，只呈現原本可見的後腦與肩背，不轉頭展示正臉。焦點落在 Amy，前景 George 柔和失焦。背景保留茶水台吊櫃、開放層架、微波爐及咖啡機，畫面只有 Amy 與 George 兩人。除上述 Amy 手部、表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框、矩陣圖表或額外文字。
```



### 2026-10-21 cafe batch restyle: cam_twoshot_wide_high_bird_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_twoshot_wide_high_bird_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_twoshot_wide_high_bird_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：高斜俯角、四椅兩桌三落地盆栽與桌面物件保留；日照、窗外城市與布料細節增強，椅子輪廓和尺度略有偏差。；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：高處斜俯拍四張單人沙發、兩張圓桌的空景。前兩椅及大圓桌，桌上單耳咖啡杯在左、黑筆在右上、閉合無字筆記本在右下；後兩椅中間小圓桌上小盆栽與兩本書。窗邊三個落地花盆，左一矮一高，右一矮，葉片依圖1裁切。嚴格維持俯角、家具間距與尺度、圖1的窗格與地板留白，勿變成水平視角，不加人物。


### 2026-10-21 cafe batch restyle: cam_twoshot_wide_level_empty_gpt.png（待評鑑）
- 工具：內建image_gen／OpenAI；模型版本／費用未知；本機位一次。
- 有序輸入：1. references/scenes/cafe/cameras/cam_twoshot_wide_level_empty_blender.png；2. clp/loc_cafe_left_far.png
- 輸出：D:\kj-openMontage\projects\course-51-esg\references\scenes\cafe\cameras\cam_twoshot_wide_level_empty_gpt.png；PNG (1672, 941)；解碼／來源複本SHA256通過。
- 觀察：四椅兩桌及三盆落地植物、桌面單耳杯黑筆閉合本保留；冰箱局部形狀與門把位置略變，家具輪廓略變，日照及遠景樓群增強。；未重試／未改採用。
- 完整prompt：
請編輯圖1，轉成圖2 loc_cafe_left_far.png 同一套精緻3D動畫電影美術的空景背景。圖1是唯一相機、透視、取景、裁切、物件位置與遮擋依據；圖2只提供美術，不移植它的構圖或畫外物件，不重新生成圖2。
匹配米灰細織布沙發、珊瑚橘柔軟布抱枕、象牙白霧面桌與陶瓷、淺木、自然綠植、冷藍玻璃城市、柔暖日光，不逐張加強飽和度／泛光。維持圖1光源方向，反射隨視角合理變化。
嚴格保持圖1窗格、立柱、家具設備、植物的位置、數量、尺度、主要輪廓及裁切。不可旋轉、鏡像、拉近拉遠或補出裁切物件。近景沒有地板、天花板或全椅時不得自行補全。只細化已有物件的微紋理、接縫、倒角、接觸陰影、反射及原體積內葉片。保留乾淨霧面表面，不加雜物，不重設計家具。玻璃外建築保留位置與輪廓。不額外強化散景。
如果有冰箱，只保留靠窗側既有上下各一支把手，不加另一側把手。杯子各只有一個杯耳，器皿規整無扭曲。
零人物：無人物、手臂、肩膀、人形倒影。只輸出一張16:9高解析度完整圖片，無拼圖、字幕、商標、水印。
本鏡畫面：水平雙人廣角空景，前方兩張完整單人沙發與前圓桌，杯子在左、黑筆和閉合無字筆記本在右；後方另兩張椅及小桌盆栽兩本書。四個珊瑚橘抱枕，窗邊左矮植栽、左高植栽及右矮植栽共三盆；最右邊冰箱只露局部。保持圖1四椅朝向、位置、家具尺度、窗格與地板留白，不補出冰箱全貌，不改成參考圖視角、不加入人物。

### 2026-10-21 shot_3.3.4 GPT v1（待評鑑）
- 使用者確認新版 prompt 後生成；工具：內建 image_gen／OpenAI，模型與費用未知，本輪1次。
- 輸出：assets/images/shot_3.3.4_gpt_v1.png
- 有序參考圖：1. references/scenes/cafe/cameras/cam_george_mcu_45deg_empty_gpt.png；2. references/scenes/cafe/cameras/cam_george_mcu_45deg_block_blender.png；3. clp/char_george.png
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過。
- 觀察：閉嘴微笑、向右視線與雙手畫外呈現；人物較blocks縮小且偏左，胸肩露出更多，頭部朝向與背景遮擋有變化。待評鑑，未追加生成或改採用。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：cafe 場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George（char_george）人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、比例、顯示範圍與遮擋關係。

將藍色定位人物替換為 George，人物外觀與服裝採用圖 3，不採用其展示姿態、嚴肅表情或構圖。保留銀灰頭髮、深棕方框眼鏡、白色短鬍鬚、棕色背心、米色襯衫與深棕領帶。

維持圖 2 的頭部尺度、肩膀位置與頭頂留白。只呈現原本可見的部位，不縮小人物、不拉遠鏡頭，也不補出畫外身體。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置，不採用 blocks 的方塊材質與簡化人物外觀。

畫面描述：
這是一張坐姿眼高、65mm 固定鏡位的 George 單人頭肩近景。George 位於畫面中央略偏左，頭頂完整入鏡，臉部與頭部佔據主要畫面，下緣只呈現雙肩及部分上胸。雙手完全留在畫外，不增加手勢。

George 正準備向 Amy 介紹篩選關鍵 ESG 議題的專業方法。身體自然端正，頭部保持平穩，下巴放鬆；嘴唇輕合、嘴角微微上揚，眉心舒展，呈現從容、自信而親切的導師神情，不露齒大笑。

George 看向畫面右側、與他坐姿眼睛高度相近的畫外 Amy。雙眼自然水平朝右，虹膜位於眼裂垂直中央附近，不往右上方看，不抬下巴，也不直視鏡頭。眼鏡鏡片通透，能清楚看見雙眼。

背景保留同機位的落地玻璃、窗外高樓、立柱與竹節盆栽，使用自然日光與淺景深突出 George。畫面只有 George 一人，Amy 完全在畫外，不加入其他人物。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對話框或額外文字。「重大性分析 (Materiality Analysis)」字卡由後製疊加，不生成在圖片內，也不為字卡移動人物或改變取景。
```




## 2026-10-21 shot_3.4.2 GPT v1（待評鑑）
- 圖片：`assets/images/shot_3.4.2_gpt_v1.png`
- 工具：內建 image_gen；供應商：OpenAI；模型／費用：未知；本鏡呼叫 1 次。
- 驗證：1672x941 RGB PNG，完整解碼及來源 SHA256 一致。
- 看圖：攤掌與微張嘴呈現；George 左移、頭身比例及 Amy 前景遮擋偏離 blocks，視線略偏上。
- 未重試，未改正式採用。

參考圖順序：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_george_ots_amy_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_george_ots_amy_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

完整 prompt：
```text
參考圖說明：
圖 1 cam_george_ots_amy_empty_gpt.png：場景外觀參考圖。
圖 2 cam_george_ots_amy_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 外觀與服裝採用圖 3，Amy 外觀與服裝採用圖 4，不採用人物參考圖的展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。人物坐入原有座椅，不另加座椅。

畫面描述：
這是一張從 Amy 身後過肩拍攝 George 的畫面。George 位於中景中央偏左，頭部、上身及原有可見手部入鏡；Amy 的後腦、肩背佔據右前景，維持圖 2 的大小、裁切及對 George 的遮擋。George 看向面前的 Amy，視線維持對坐交談的高度，眉眼溫和而專注，嘴巴微張，呈現正在清楚解說的神情；右手在原有可見範圍內輕輕攤開、掌心斜向上，作為逐項說明的起始姿態，另一手自然放鬆。Amy 面向 George 安靜聆聽。焦點落在 George，前景 Amy 略微柔焦。畫面只有這兩位人物。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、數字或資訊圖表。
```


## 2026-10-21 shot_3.4.3 GPT v1（待評鑑）
- 圖片：`assets/images/shot_3.4.3_gpt_v1.png`
- 工具：內建 image_gen；供應商：OpenAI；模型／費用：未知；本鏡呼叫 1 次。
- 驗證：1672x941 RGB PNG，完整解碼及來源 SHA256 一致。
- 看圖：食指相觸與微張嘴呈現；視線偏右上，頭部縮小、上身露出增加，偏離 blocks。
- 未重試，未改正式採用。

參考圖順序：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_george_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_george_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png

完整 prompt：
```text
參考圖說明：
圖 1 cam_george_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖 2 cam_george_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、頭部比例、肩膀位置與遮擋關係。

將定位人物替換為 George，外觀與服裝採用圖 3，不採用其展示姿態或構圖。除本鏡指定抬手動作外，身體可見範圍沿用圖 2，不拉遠鏡頭或縮小人物以容納手勢。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張坐姿近眼高的 George 單人頭肩近景，保留圖 2 的頭頂留白、頭部大小與肩膀裁切。George 眼神朝畫面右側、畫外與他對坐的 Amy，視線保持接近水平，表情從容、有條理，嘴巴微張，正在開始列舉減碳對策。雙手抬到下巴下方、畫面下緣的可見區域，左手食指伸出，其餘手指自然彎曲，右手食指輕觸左手食指，呈現開始數第一項對策的單一瞬間；手勢不遮住嘴巴或臉，雙肘留在畫外。臉部與數手指的動作清楚可辨，背景略微柔焦。畫面只有 George，Amy 完全在畫外。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、項目文字或圖示。
```


## 2026-10-21 shot_3.4.5 GPT v1（待評鑑）
- 圖片：`assets/images/shot_3.4.5_gpt_v1.png`
- 工具：內建 image_gen；供應商：OpenAI；模型／費用：未知；本鏡呼叫 1 次。
- 驗證：1672x941 RGB PNG，完整解碼及來源 SHA256 一致。
- 看圖：低頭下視、閉嘴微笑及雙手畫外呈現；肩胸露出增加，人物比例與背景遮擋偏離 blocks。
- 未重試，未改正式採用。

參考圖順序：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_amy_mcu_45deg_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_amy_mcu_45deg_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg

完整 prompt：
```text
參考圖說明：
圖 1 cam_amy_mcu_45deg_empty_gpt.png：場景外觀參考圖。
圖 2 cam_amy_mcu_45deg_block_blender.png：構圖底圖。
圖 3 char_amy.jpeg：Amy 人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為 Amy，只呈現圖 2 中可見的頭部、肩膀與上胸，不補出畫外身體。人物外觀與服裝採用圖 3，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張坐姿近眼高的 Amy 單人頭肩近景，保留圖 2 的人物大小、頭頂留白及肩胸裁切。Amy 下巴微收、頭部稍微低下，雙眼看向畫面下方、畫外桌面上的筆記；眉心舒展，肩膀自然放鬆，嘴唇輕合、嘴角微微上揚，呈現看見具體計畫後開始安心的神情，作為接續輕嘆一口氣並開口說話的起始瞬間。筆記本、桌面及雙手全部留在畫外，不為了展示筆記而拉遠鏡頭。焦點落在 Amy 的表情，背景略微柔焦。畫面只有 Amy，George 完全在畫外。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```


## 2026-10-21 shot_3.1.1 GPT v1（待評鑑）
- 圖片：assets/images/shot_3.1.1_gpt_v1.png
- 工具：內建 image_gen／OpenAI；1 次生成，模型與費用未知。
- 觀察：Amy 雙手奉杯、George 雙手低放未接杯，桌面無重複咖啡杯；人物位置、比例、腿腳與圓几遮擋偏離 blocks，Amy 視線略偏左上，杯子疑似多出另一側杯柄。背景依 GPT 場景重繪。未改正式採用。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_twoshot_wide_level_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_twoshot_wide_level_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png

完整 prompt（使用者原文）：
```text
參考圖說明：
圖 1 cam_twoshot_wide_level_empty_gpt.png：新潮咖啡館 cafe 的場景外觀參考圖。
圖 2 cam_twoshot_wide_level_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側紅色人物。
圖 5 prop_coffee_set.png：白色陶瓷咖啡杯與杯碟的外觀參考；不使用同圖中的糖罐。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、家具配置、人物佔位、整體大小、可見範圍與遮擋關係。保持頭頂留白、兩人之間的距離及圓几在前景的位置，不推近鏡頭或放大人物。

將左側藍色定位人物替換為 George，右側紅色定位人物替換為 Amy。人物外觀、五官、髮型與服裝分別採用圖 3、圖 4，不採用其展示姿態或參考圖排版。兩人自然坐入原有扶手椅，身體與坐墊接觸，只呈現圖 2 中可見的部位。

場景材質、色彩與光影依圖 1，保留米白色扶手椅、橘色靠枕、淺色圓几、盆栽、落地玻璃及窗外高樓。維持日間柔和自然光與清晰背景，不改變圖 2 的空間配置。

Amy 奉上的咖啡杯碟採用圖 5 的外觀，只取一組白色杯碟，不複製多視角展示或糖罐。以這組杯碟取代圖 2 原本放在前方圓几上的咖啡杯；原杯位置留空，不另外增加咖啡杯。筆記本與筆保持原位。

畫面描述：
這是一張 26mm、坐姿平視的雙人全景。George 坐在畫面左側扶手椅，Amy 坐在右側扶手椅，兩人身體略朝向彼此，前方為低矮圓几。頭部、軀幹與原本可見的腿腳保留在畫面內，維持圓几遮擋下半身的關係。畫面只有 George 與 Amy 兩人。

Amy 臉上帶著熱情、略帶討好與期待的微笑，頭部轉向 George，視線落在他的臉上。她雙手托住同一只杯碟的兩側，盛著咖啡的杯子直立放在碟上；雙臂朝 George 方向伸出，杯碟停在兩人之間、圓几上方，呈現正在奉上咖啡的瞬間。為完成端杯動作，允許肩膀、手臂及上身輕微向前調整，臀部仍坐在原椅墊上，腿腳位置沿用圖 2。

George 面向 Amy，眼神溫和，嘴角帶著會心的淺笑。他的雙手仍自然低放在身前，尚未接觸杯碟，咖啡杯尚未送到嘴邊。呈現他準備接受 Amy 好意的起始狀態。

除上述表情、視線、端杯姿態及咖啡杯位置調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或分格。
```


## 2026-10-21 shot_3.5.1 GPT v1
- 路徑：assets/images/shot_3.5.1_gpt_v1.png
- 工具：內建 image_gen／OpenAI；確切模型與費用未知；單次生成，待評鑑，未改採用。
- 有序參考圖：1. references/scenes/cafe/cameras/cam_twoshot_ms_level_empty_gpt.png；2. references/scenes/cafe/cameras/cam_twoshot_ms_level_block_blender.png；3. clp/char_george.png；4. clp/char_amy.jpeg
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過。
- 觀察：兩人互看、George 微笑及扶手附近手勢成立；人物尺度、坐姿與背景配置偏移，Amy 額外交腿。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左側的藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、身體比例、顯示範圍與遮擋關係。維持人物頭頂留白、兩人間距及畫面下緣裁切，不放大人物頭部。

將藍色定位人物替換為 George，紅色定位人物替換為 Amy，直接坐入各自既有扶手椅，不額外增加座椅。只呈現圖 2 中可見的身體部位，不補出畫外身體。人物外觀與服裝採用圖 3、圖 4，不採用其展示姿態或多視圖構圖，不保留定位人物的藍紅色衣服與方塊外觀。

將場景的材質、風格與日間自然光更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張坐姿平視、40mm 雙人中景的畫面。George 坐在左側，Amy 坐在右側，兩人的上半身、手部與部分腿部依圖 2 入鏡；前方主圓几只在畫面下緣局部可見，兩人之間保留後方小圓几及盆栽。George 頭部略朝 Amy，眼神溫和，嘴角帶著會心的微笑，呈現準備提醒她計畫必須落實的瞬間；雙手仍自然停在扶手附近，尚未抬手指向牆面。Amy 看向 George，神情專注，保持聆聽的坐姿。人物臉部清楚，中等景深保留咖啡館與窗外高樓的辨識度。畫面只有 George 與 Amy 兩人，不加入背景顧客或咖啡師。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、字卡或浮水印。
```

## 2026-10-21 shot_3.5.2 GPT v1
- 路徑：assets/images/shot_3.5.2_gpt_v1.png
- 工具：內建 image_gen／OpenAI；確切模型與費用未知；單次生成，待評鑑，未改採用。
- 有序參考圖：1. references/scenes/cafe/cameras/cam_george_cu_emotion_empty_gpt.png；2. references/scenes/cafe/cameras/cam_george_cu_emotion_block_blender.png；3. clp/char_george.png
- 驗證：1672×941 RGB PNG，完整解碼與來源副本 SHA256 通過。
- 觀察：George 單人閉嘴認真特寫成立；頭頂留白減少、胸肩露出增加，視線略上偏，眉眼略顯擔憂。
- 完整 prompt：
```text
參考圖說明：
圖 1 cam_george_cu_emotion_empty_gpt.png：咖啡館同機位場景外觀參考圖。
圖 2 cam_george_cu_emotion_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、人物佔位、頭部比例、顯示範圍與遮擋關係。維持頭頂留白及肩部裁切，不放大頭部、不拉遠鏡頭，也不增加胸口的可見範圍。

將定位人物替換為 George，只呈現圖 2 中可見的頭部、頸部及肩部，不補出畫外身體。人物外觀與服裝採用圖 3，保留銀灰髮型、深棕方框眼鏡與白色短鬍鬚，不採用其展示姿態或多視圖構圖，不保留定位人物的棕色塊狀頭髮與藍色衣服。

將場景的材質、風格與日間自然光更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張坐姿近眼高、100mm 的 George 單人臉部特寫。頭部佔據畫面主要範圍，肩膀僅在下緣局部入鏡，Amy 與 George 的雙手都在畫外。George 已收起上一鏡的笑意，嘴唇自然輕合，眉眼專注而篤定，呈現即將鄭重說出「貫徹執行」的瞬間；視線朝向鏡外 Amy 所在方向，保持圖 2 的頭部基本朝向，不大幅轉頭。表情認真有力量，但不憤怒、不誇張瞪眼。焦點落在眼睛與面部，背景窗框、窗外高樓及植物呈柔和淺景深。畫面只出現 George 一人，不加入 Amy、其他人物或前景肩膀。除上述表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、字卡或浮水印。
```

## 2026-10-21 shot_3.6.2 GPT v1

- 圖片：`assets/images/shot_3.6.2_gpt_v1.png`
- 工具：內建 image_gen；供應商 OpenAI；確切模型及費用未知；單次生成，待評鑑，未改採用。
- 驗證：PNG 完整解碼通過，1672×941 RGB。Amy低頭書寫與George微笑注視成立；George也向前傾、手勢改為交握，桌面露出增加，未精準保留blocks姿態與裁切。
- 有序參考圖：
1. `references/scenes/cafe/cameras/cam_twoshot_ms_level_empty_gpt.png`
2. `references/scenes/cafe/cameras/cam_twoshot_ms_level_block_blender.png`
3. `clp/char_george.png`
4. `clp/char_amy.jpeg`
5. `clp/prop_coffee_set.png`

完整 prompt：
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：咖啡館場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左側的藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側的紅色人物。
圖 5 prop_coffee_set.png：桌面咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、家具配置、人物佔位、比例、顯示範圍與遮擋關係。

將左側藍色定位人物替換為圖 3 的 George，右側紅色定位人物替換為圖 4 的 Amy。人物外觀與服裝採用各自參考圖，不採用其展示姿態或構圖，不保留定位人物的紅藍色服裝及方塊外觀。只呈現本鏡取景內可見的身體部位，不補出畫外身體。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。桌面咖啡杯碟的外觀採用圖 5，只替換本鏡可見的咖啡杯碟，不加入該圖中的收納罐或其他展示物件。

畫面描述：
這是一張 40mm、坐姿平視的雙人中景。George 坐在畫面左側，Amy 坐在畫面右側；人物大小與裁切沿用圖 2，前方主圓几僅在畫面下緣局部入鏡。背景保留落地玻璃、窗外高樓及後方小圓几上的盆栽。

Amy 正在前方主圓几靠自己一側的攤開筆記本上做筆記：上身略微前傾，一手持筆、筆尖接觸紙面，另一手扶住筆記本，低頭看著正在書寫的位置，嘴角帶著得意而自信的微笑。筆記本與手部依原取景自然裁切，不為完整展示書寫動作而拉遠鏡頭或抬高桌面。

George 保持坐姿，頭部略朝向 Amy，以溫暖、欣慰的微笑看著她。畫面只有 George 與 Amy 兩人，不加入背景顧客或咖啡師。

日間自然光，溫暖柔和，中等景深。除 Amy 書寫所需的上身、手臂、手部姿態、筆記本，以及兩人的表情與視線調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、標題或 ESG 步驟疊字。
```




## 2026-10-21 shot_3.1.3 GPT v1（待評鑑）
- 圖片：assets/images/shot_3.1.3_gpt_v1.png
- 工具：內建 image_gen／OpenAI；1 次生成，模型與費用未知。
- 觀察：George 右手握杯柄、杯底懸於杯碟上方，Amy 雙手低放及雙人微笑呈現；人物位置／比例與軀幹朝向偏離 blocks，Amy 視線偏左上，背景依 GPT 空景重繪。未改正式採用。
- 有序參考圖：
1. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_twoshot_ms_level_empty_gpt.png
2. D:/kj-openMontage/projects/course-51-esg/references/scenes/cafe/cameras/cam_twoshot_ms_level_block_blender.png
3. D:/kj-openMontage/projects/course-51-esg/clp/char_george.png
4. D:/kj-openMontage/projects/course-51-esg/clp/char_amy.jpeg
5. D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png

完整 prompt（使用者原文）：
```text
參考圖說明：
圖 1 cam_twoshot_ms_level_empty_gpt.png：新潮咖啡館 cafe 場景外觀參考圖。
圖 2 cam_twoshot_ms_level_block_blender.png：構圖底圖。
圖 3 char_george.png：George 人物參考圖，對應圖 2 左側藍色人物。
圖 4 char_amy.jpeg：Amy 人物參考圖，對應圖 2 右側紅色人物。
圖 5 prop_coffee_set.png：白色陶瓷咖啡杯與杯碟外觀參考；不使用同圖中的糖罐。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、家具配置、人物佔位、整體大小、可見範圍與遮擋關係。保持 George 在左、Amy 在右及兩人之間的距離；前方圓几只保留原本在畫面下緣可見的範圍，不拉遠鏡頭展示整張桌子。

將定位人物替換為對應角色，George 外觀與服裝採用圖 3，Amy 採用圖 4，不採用人物參考圖的展示姿態或排版。兩人自然坐入原有扶手椅，保持與椅墊的接觸。

場景材質、色彩與光影依圖 1，保留落地玻璃、窗外高樓、扶手椅、後方小圓几及盆栽配置。日間柔和自然光，中等景深，兩位主角清楚可辨。

咖啡杯與杯碟外觀採用圖 5。以一組杯碟取代底圖原本的桌面咖啡杯，不保留重複杯子，不增加糖罐。筆與其他原有物件保持原位。

畫面描述：
這是一張 40mm、坐姿平視的雙人中景。George 坐在左側，Amy 坐在右側，兩人上身、原可見手部及腿部局部依圖 2 呈現，圓几在下緣局部入鏡。畫面只有兩人。

George 帶著溫和、略帶調侃的笑意，眼睛看向 Amy。他右手握住白色咖啡杯的杯柄，杯子已離開嘴邊，停在自己這側圓几上的杯碟正上方，杯底尚未接觸杯碟，呈現準備將杯子放回去的瞬間。杯碟位於底圖原咖啡杯附近，維持實際手掌可握持的尺寸；畫面下緣以外的部分保持裁切。左手自然低放，身體只為放杯稍微前傾。

Amy 看著 George 的臉，帶著期待、準備回應的微笑，雙手自然低放，維持原有坐姿。此刻尚未開始連續點頭或做出請客的額外手勢。

除上述表情、視線、George 放杯所需的局部姿態及杯碟狀態外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕、對白文字、角色標籤、浮水印或分格。
```



## 2026-10-21 shot_3.1.1b GPT v1（待評鑑）
- 圖片：assets/images/shot_3.1.1b_gpt_v1.png
- 工具：內建 image_gen／OpenAI；1 次編輯生成，模型與費用未知。
- 參考圖：D:/kj-openMontage/projects/course-51-esg/assets/images/shot_3.1.1_gpt_v1.png
- 觀察：George 雙手前伸承接杯碟，Amy 仍輕托，交接動作呈現；主背景與坐姿大致保留，George 頭身略有變動，杯碟與後方小圓几視覺重疊。未改正式採用或 scene_plan。

完整 prompt：
```text
以提供的 shot_3.1.1_gpt_v1.png 為編輯底圖，生成同一場景的下一個交接瞬間 shot_3.1.1b。

保留原圖的鏡位、取景、人物大小與座位位置、服裝、臉部辨識特徵、背景、光線、家具、筆記本與筆的位置及畫面裁切。

只調整交接咖啡所需的手臂與手部姿態：左側 George 將雙手從膝前抬起，向右側 Amy 伸出，雙手分別承托同一只白色杯碟靠近自己這側的左右邊緣與底部，已實際接觸並承接杯碟的重量。右側 Amy 雙手仍輕托杯碟靠近自己這側的兩邊，正把咖啡交到 George 雙手中。四隻手接觸同一只杯碟，位置清楚分開，不重疊融合；George 不握咖啡杯杯身或杯柄。

杯子直立放在杯碟中央，只有一杯咖啡與一只杯碟；杯子是單一杯柄的白色陶瓷咖啡杯。杯碟位於兩人之間、前景圓几上方。George 上身可因接杯輕微前傾，兩人臀部與腿腳維持原圖坐姿。兩人保留溫和微笑，視線朝彼此，呈現 George 雙手接過 Amy 端來咖啡的自然交接瞬間。

輸出一張 16:9 彩色分鏡圖，不加入字幕、文字、浮水印或分格。
```


## 2026-10-21 shot_1.3.1 — GPT v4（閃亮秀場服裝，待評鑑）

- 工具／供應商：內建 image_gen／OpenAI，I2I 1次；確切模型及費用未知。
- 有序參考圖：1. D:/kj-openMontage/projects/course-51-esg/assets/images/shot_1.3.1_gpt_v3.png（唯一編輯底圖）。
- 輸出：assets/images/shot_1.3.1_gpt_v4.png。
- 目視：金色亮片外套與長褲、黑緞領口／領結、黑亮面鞋成立；全身、商品、表情與舞台構圖保留。未改採用版本。
- 完整實際 prompt：
```text
以輸入圖1（shot_1.3.1_gpt_v3.png，唯一編輯底圖）為基礎，只修改中央主管的服裝與鞋子，將辦公室藍襯衫、棕領帶與棕長褲改成華麗、閃亮亮的秀場表演服裝：剪裁合身的金色亮片西裝外套，黑色緞面戧駁領，白襯衫與黑色蝴蝶領結，搭配金色亮片長褲與黑色亮面皮鞋。金色亮片密集細緻，在既有舞台燈光下呈現明亮閃耀的反射與少量精緻星芒，明確像秀場主持人或表演明星的華麗造型。保留原有3D動畫電影畫風。嚴格保留主管的臉、髮型、表情、身材比例、站位、雙手托扶商品的姿勢；保留原本的單一白罐綠蓋商品、標籤文字、大小與位置。保留原圖完整全身構圖，頭頂、完整雙腿、兩隻鞋與下方地板全部入鏡，人物比例與相機距離不變。背景舞台、ESG文字、裝飾、燈光、展示台與畫面邊界均維持原圖。只有服裝與鞋子改變，不新增人物、頭飾、手持物、字幕或浮水印。輸出同原圖比例的單張橫幅圖片。
```
