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
