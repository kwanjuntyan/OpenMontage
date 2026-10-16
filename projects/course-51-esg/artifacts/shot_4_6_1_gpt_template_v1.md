# 4.6.1 GPT 非自拍模板樣圖 v1

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成；以使用者最新「不要自拍」與確認的 prompt 為準。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：一次、生成一張；transparent_background=false；prompt 原文送出，未追加創意條件。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s06_amy_medium_close_up.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s06_amy_medium_close_up.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 輸出：../assets/images/shot_4_6_1_gpt_template_v1.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-0b9d39b0-7077-4abf-b9fd-8054a2c6b2f2.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：非自拍、無手機、無字幕、Amy 開朗說話表情與暖色場景成立；灰色白模軀幹、手臂及手部仍殘留，Amy 部分上身出現在白模軀幹後方，人物替換未完成，未通過驗收。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未驗證後續影片效果。
- 狀態：保留本次未通過樣圖，未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准；script.json／scene_plan 仍保留舊自拍規劃，後續以使用者最新指示為準。

## 實際送出 prompt

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

