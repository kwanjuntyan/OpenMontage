# Asset Director - kj-cinematic Pipeline

本檔是 kj-cinematic 的完整素材工序，不繼承 cinematic/asset-director。音訊與視覺由此調度；工具、供應商 adapter、artifact 格式與既有製作 checkpoint 繼續共用。
本檔是素材工序的入口，維護共通原則、模態調度與交付；視覺素材順序、權責宣告及各模態 Prompt 寫法由 [配方手冊](prompt-recipes.md) 維護。

## 輸入與責任

- 讀取 `state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["clp"]["clp_manifest"]`，以及已有的 script、proposal_packet、brief；以已核准分鏡與製作選擇為準。
- 讀取選定 style playbook；視覺 prompt 使用 `asset_generation.image_prompt_prefix`，但風格文字不得覆蓋本鏡的構圖與 CLP 特徵。
- 輸出 `asset_manifest`，沿用 `schemas/artifacts/asset_manifest.schema.json`；只準備素材，剪接及混音交給 edit／compose。
- 進場與續作遵循 `skills/meta/checkpoint-protocol.md`：先載入已有成果與 partial_progress，再更新 assets 的 `in_progress`，避免重做已核准資產。
- 先盤點可重用的錄音、圖片、影片、音樂與 CLP；有現成素材就依規劃使用，生成鏡頭也可以是主要素材。
- 花費前報工具、供應商、模型、模式、用途與預估費用；沿用已核准選擇，換模型須先問。失敗保留原始錯誤，不自行換供應商或模式。

## 1. 音訊先行

1. 有台詞／旁白時，先把 script 段落與鏡頭對上；優先沿用已核准錄音。沒有語音需求的鏡頭略過 TTS。
2. 缺少錄音才使用 `tts_selector`；保留角色 Voice ID、已核准 baseline、語速與 delivery_cues。動作括號是表演指令，不讀成台詞；provider_text 依相應工具格式傳入。
3. Google TTS 使用 Vertex AI＋`GOOGLE_APPLICATION_CREDENTIALS` 服務帳戶 JSON／global；其他聲音依既有工具及專案選擇，不在本檔重建音訊 adapter。
4. 用 ffprobe 取得實際秒數，記入音訊 asset 的 `duration_seconds`；先對齊台詞、停頓、動作，再安排影片時長。超出核准鏡頭時回報並調整 scene_plan，不偷偷加速或刪台詞。
5. BGM 優先既有音軌／`music_library`，需要檢索時用 `pixabay_music`／`freesound_music`；付費生成依核准選擇使用 `music_gen`。SFX 同樣先找已有素材。
6. 在 manifest 的 `metadata.music_plan`／`metadata.ambience_plan` 記錄音軌用途、對應鏡頭、進出點與來源授權；混音留給 compose。需要字幕才使用 `subtitle_gen`。
7. 影片原生音訊不得默默取代已核准台詞；有對嘴需求時明確交代採用方法，首幀或參考圖本身不保證對嘴。

## 2. 視覺裝配與分流

1. 先按 scene 的 `render_stages` 盤點整鏡所需素材與步驟，再依序執行當前模態；八個代號是 Agent 配方，不是直接傳入 API 的 generation_mode。缺省或空陣列沿用原分鏡與素材意圖，不強制改成白模流程。
2. 從 `required_assets` 解析本鏡所需素材。CLP 的 `reference_images` 相對於專案根目錄；送工具前解析成實際路徑。先看圖；本鏡使用白模影片時，檢視起訖及關鍵動作。
3. 確定當前模態後，在 repo 根目錄執行 `.venv/Scripts/python.exe scripts/read_prompt_recipe.py <本步模態>`，以實際代號替換佔位；只讀命令回傳的配方與適用共通規則，不先讀八類全文。按範本組裝素材與 prompt，不混套其他模態寫法；完成後依本檔呼叫工具、驗收及交接。只附本鏡需要的參考圖，數量依用途及選定工具限制，不固定限三張。
   - 工具只縮小本次讀取內容，不清除先前對話上下文；切換步驟時重新讀取當前模態，避免沿用前一模態的範本。
4. **CLP 共用描述與逐鏡摘錄**：人物／場景／道具以實圖為依據；參考圖說明寫名稱／CLP id、圖片編號及從 `clp_manifest.description` 直接摘錄的本鏡相關短句，不逐鏡另編外觀或佈景描述。
   - 按特徵短句摘錄，保留原有特徵用詞、顏色及物件關係；同一特徵跨鏡重用相同文字。動作、表情、視線與攝影指示另寫，不混入共用描述。
   - 依本鏡取景與表演省略「不會呈現且不影響本鏡」的描述；白模未建出、但 CLP 確認存在且本鏡可見或有影響的特徵仍需保留，例如眼鏡、鬍鬚或窗框；範例不是每個實體的必備特徵。畫外物件若影響光線或互動也需保留相關依據。
   - 刪減只作用於本鏡 Prompt，不回寫刪除 CLP 原文。
   - manifest 與實圖不符時，排除衝突文字並回報待修項目，以圖片為準；不能為了文字一致而沿用錯誤描述，也不在本工序另編或自動改寫共用設定。
5. **表演來源**：動作、表情、視線、手勢及道具互動依使用者最新明確指示，其次依核准分鏡的 `character_actions`／描述；素材在各模態中的姿態／運動用途依配方。
6. 生成前依各素材職責核對主體、動作、場景、構圖、相機，排除互相衝突的指令；本鏡指定表演與白模／CLP 展示姿態不同，不視為素材衝突。
7. 查選定 provider 的 skill／現有 adapter，將配方語意與媒體引用綁定工具欄位，再交給 `image_selector`／`video_selector`。實際欄位、素材上限、秒數及支援模式以工具實作為準，不把所有供應商都假設成 `image_urls`。
8. 同一製作選擇批量生成前，先呈現代表樣本；已有適用核准樣本就重用。`motion_required` 的動態樣本及最終素材必須有真正影片，W2I 首幀不能代替。

## 3. 多步素材交接與 W2V 條件

本節適用於多步 `render_stages`，或沿用既有輸出續作。單步完成後依第 4 節交付；獨立 W2I 不要求白模影片或自動追加 W2V。執行 W2V 時另套第 3.2 節。

### 3.1 共通交接

1. 本步完成後依第 4 節的驗收項目檢視輸出；有後續步驟時，確認輸出適合作為下一步的原圖、首幀或參考素材，例如 R2I → I2V 的圖片需適合作為影片起點。
2. 將實際輸出路徑、所屬鏡頭、已完成步驟、核准情形及下一步保存在 assets checkpoint 的既有 `metadata.partial_progress`，不把中間產出當成整個 assets 已完成。
3. 核准安排沿用第 2 節的代表樣本與既有 checkpoint protocol；需要等待人工核准時，呈現首幀／樣本，assets 維持 `in_progress` 並結束本輪，不新增逐步核准關卡。
4. 繼續時重用適用的同一路徑，依下一模態的配方組裝請求；從 partial_progress 的下一步續作，檢視既有輸出是否仍適用，不重生已核准素材、不覆寫核准檔。
5. 下一步缺件就回報並停在該鏡；工具無法接受所需條件時，先交代差異並取得改方案的決定，不靜默丟棄素材或切換模態。
6. 影片時長依核准規劃，有錄音／預演時一併對齊；超過模型單段限制時先修訂切段／運鏡安排，不自行截短、延長或降格。這些步驟仍在 assets 內，不新增 pipeline stage。

### 3.2 W2V 特殊條件

- W2V 必須有適合作為後續動作起點的核准首幀；首幀可來自本鏡 W2I 或既有適用素材，按共通交接核對後重用。
- 同時需要可用白模影片。缺白模影片就回報缺件並停在該鏡；只有首幀屬 I2V，不得冒稱 W2V，也不自行改成 I2V。

## 4. 所有模態的驗收與交付

本節適用於八類視覺模態，以及音訊、標題／疊圖等素材；單步完成與多步的最終產出均依本節交付。

- 標題／疊圖依 `skills/meta/animation-runtime-selector.md` 與已選 renderer；不因視覺配方改變 runtime。
- 若交付本身是可自由取景的 3D 世界，讀 `skills/creative/3d-world-generation.md` 與相應工具 skill，沿用已核准 renderer 及品質要求；只用於幾何引導的白模不套成品材質標準。
- 每件素材記錄既有欄位：`id`、`type`、`path`、`source_tool`、`scene_id`，以及適用的 `prompt`、`model`、`duration_seconds`、來源／授權／實際費用。未知費用不填成零。
- `generation_summary` 開頭用 `clp: <CLP ids> | <本步配方> | ...` 記實際配方與參考用途；沒有 CLP 就寫 `clp: none`。不新增 asset 欄位；檔案未生成前不冒填成已完成素材。
- 所有視覺素材檢視角色／場景連戲與本鏡需求，記錄具體未過項目；不能只因檔案存在就宣告品質通過。
- 圖片驗收構圖、可見人數、外觀及指定瞬間的表演；用作影片首幀時，另確認是否適合後續動作起點，不要求圖片本身有影片時長或運鏡。
- 影片除上述外觀與構圖外，另驗實際時長、動作起訖、時間節點與運鏡；有錄音時確認對齊，有白模預演時檢視運動引導效果，不當成逐幀精度保證。
- assets 規劃的全部素材完成後，依既有 reviewer 與 checkpoint protocol 提交 schema-valid manifest，assets 寫 `awaiting_human`，呈現逐鏡素材、音訊、費用與限制並結束本輪；核准後才進 edit／compose。
