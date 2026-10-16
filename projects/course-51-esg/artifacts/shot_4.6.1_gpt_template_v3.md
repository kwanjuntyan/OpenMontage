# 4.6.1 GPT 完整人物替換樣圖 v3

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

## 實際送出 prompt

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

