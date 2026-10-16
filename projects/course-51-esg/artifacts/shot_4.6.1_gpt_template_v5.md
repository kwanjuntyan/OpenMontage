# 4.6.1 GPT SH01 雙人中景與白板內容樣圖 v5

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

## 實際送出 prompt

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

