# 4.6.2 GPT 雙人海報模板樣圖 v1

- 日期：2026-10-16（Asia/Taipei）
- Pipeline／階段：course-51-esg／kj-cinematic／assets 的 W2I 局部生成。
- 工具／供應商：內建 image_gen／OpenAI；確切模型、用量與實際費用未提供，事前已告知無法報價。
- 呼叫：一次、一張；使用本輪核准的 4.6.2 prompt 原文與四張參考圖，transparent_background=false，未追加修正條件。
- 圖 1：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/cameras/empty_gpt_s02_medium_two_shot.png
- 圖 2：D:/kj-openMontage/projects/course-51-esg/references/scenes/marketing_department/renders/blocks_blender_s02_medium_two_shot.png
- 圖 3：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg
- 圖 4：D:/kj-openMontage/projects/course-51-esg/clp/char_esg_li.jpeg
- 輸出：../assets/images/shot_4_6_2_gpt_template_v1.png
- 原生來源：C:/Users/servi/.codex/generated_images/01a14365-4ddb-7872-9254-b032d636e172/exec-bd8816b5-1e7d-4e5f-9f5d-93011cc189dd.png
- 尺寸：1672×941 RGB PNG，接近但非精確 16:9；未放大或裁切。
- 檢視：兩個定位人物已完整替換，無殘留白模；Amy 灰西裝、小李花襯衫與無眼鏡符合實圖，小李雙手舉彩色海報、興奮說話與看向 Amy，Amy 看海報／閉嘴聆聽、海報空白標語區及無字幕成立。人物較 blocks 靠近中央，兩人間距縮小、頭頂留白減少；Amy 改成托下巴與橫臂，未沿用 blocks 手勢。構圖與姿勢未完全通過。
- 驗證：已看圖、Pillow 完整解碼及來源／目的地 SHA256 核對；未製作海報文字後製或驗證後續影片效果。
- 狀態：保留本次樣圖，不追加生成、未替換正式素材、未更新 asset_manifest 或推進整體 assets 核准。

## 實際送出 prompt

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

