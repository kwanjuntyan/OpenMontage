# 六鏡短指令｜Nano Banana 2.1

2026-10-13：依已接受的六鏡短指令轉寫；第四鏡採身體朝向修正版。OpenAI 成品保留，本組另存。

工具：image_selector → google_imagen；Vertex AI／服務帳戶 JSON／global；gemini-nano-banana-2.1；edit；2K；16:9；每鏡一張，依序生成。
每鏡下方為完整實際 prompt；圖片按清單順序附入。費用先依歷史用量估六張 US$0.36～0.50，非帳單。

## 2.1.1

- 圖 1 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s02_medium_two_shot.png)
- 圖 2 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s02_medium_two_shot.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)
- 圖 5 [prop_coffee_cup.png](D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png)

```text
圖 1 是本鏡空景，也是唯一的背景編輯底圖。圖 2 是人物定位 blocks。圖 3 提供 George 外觀與服裝；圖 4 提供 Amy 外觀與服裝；圖 5 提供白色咖啡杯碟外觀。

直接在圖 1 中置入人物，保留其原取景、透視、家具位置、牆面掛畫、自然藤葉形狀與分布、材質及光影；不要重建背景。圖 2 只提供藍色 George、紅色 Amy 的人物佔位、整體大小、對坐朝向與遮擋，不採用圖 2 的背景、葉片或方塊材質。兩人坐入圖 1 既有椅子，人物頭頂高度、頭肩所在範圍與入座位置對齊圖 2；在這個佔位內依人物參考圖還原自然頭身比例，不放大人物或頭部、不改變鏡位與裁切。

Amy 愁眉微皺，一手握小匙、匙端仍在拿鐵中，抬眼望向 George 求助；George 沉著聆聽。肩膀與軀幹保持原本對坐朝向。只為這個表演調整表情、視線、手臂與原杯中飲品。維持雙人中景、既有 3D 動畫風格，輸出一張 16:9 彩色分鏡圖；不呈現方塊、展示排版或字幕。
```

v1：已生成，使用者指出背景與 blocks 不符，保留不採用。
v2：[成品](../assets/images/shot_2.1.1_banana21_v2.png)；已生成，構圖／背景核對未通過：仍混入 blocks 多角形藤葉，人物頭部偏大、頭頂位置未對齊 blocks；攪拌求助與對坐成立。
生成紀錄：2752×1536，35.11 秒；輸入 5908 tokens、圖片輸出 1680 tokens。按歷史費率估 US$0.059262，未核帳；請求與用量保存在 `.tmp/banana21_first_v2_result.json`。原 v1 請求保存在 `.tmp/banana21_six_short_1_result.json`。只重生本鏡一次，未追加。

v3：[成品](../assets/images/shot_2.1.1_banana21_v3.png)；依使用者要求將場景改為圖 1、blocks 改為圖 2，實際附件順序同步調換，其餘表演要求不變。自然藤葉恢復，未再見 v1／v2 多角形藤葉；人物頭部仍偏大、頭頂位置未對齊 blocks，不能列為完全符合，待使用者檢視。2752×1536，37.62 秒；輸入 5908、圖片輸出 1680、文字輸出 220、思考 724 tokens；按歷史費率估 US$0.066342，未核帳。實際請求與用量：`.tmp/banana21_first_v3_result.json`。

GPT 新模板 v1：[成品](../assets/images/shot_2.1.1_gpt_template_v1.png)。使用者確認原文與場景／blocks／George／Amy／杯碟五圖依序送至內建 image_gen，1672×941，確切模型／費用未知。Amy 攪拌拿鐵、抬眼求助及 George 聆聽成立；人物頭部比例較 blocks 大，George 新增握杯動作，未完全對齊 blocks。 實際請求 `.tmp/gpt_first_template_v1_result.json`；舊圖保留，共用模板未更新，未追加生成。

本次實際 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s02_medium_two_shot.png]：場景外觀參考圖。
圖 2 [blocks_blender_s02_medium_two_shot.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應紅色人物。
圖 5 [prop_coffee_cup.png]：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3、圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟外觀採用圖 5；圖 5 的其他物件不參與生成。

畫面描述：
這是一張接近人物眼高、略微俯拍的雙人中景。George 位於畫面左側，Amy 位於右側，兩人坐在木椅上隔桌相向。畫面呈現兩人的完整頭部、上半身、伸向桌面的前臂與手部，以及下緣被裁切的局部腿部。Amy 眉心微皺，一手握著小匙，匙端留在面前杯中的拿鐵裡，呈現攪拌時抬眼望向 George 求助的瞬間；George 神情沉著，注視 Amy 聆聽。兩人的肩膀與軀幹維持圖 2 的對坐朝向，除上述表情、視線、攪拌手勢及杯中飲品調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

Banana 2.1 v4（新模板）：[成品](../assets/images/shot_2.1.1_banana21_v4.png)。與本節 GPT 新模板 v1 相同 prompt 原文及五圖順序，Vertex JSON／global／gemini-nano-banana-2.1，2K／16:9。成功生成 2752×1536，55.84 秒；輸入 6068、圖片輸出 1680 tokens，按歷史費率估 US$0.059502，未核帳。Amy 攪拌拿鐵、望向 George 求助及 George 對坐聆聽成立，背景自然葉片保留；人物頭頂位置仍高於 blocks，非精確對齊。請求與回應 `.tmp/banana21_first_v4_result.json`／`.tmp/banana21_first_v4_response.json`；舊圖保留，共用模板未更新，未重試。

GPT 本對話模板 v2（2026-10-13）：[成品](../assets/images/shot_2.1.1_gpt_template_v2.png)。依本對話使用者確認的 prompt 原文與圖 1～5 順序（場景／blocks／George／Amy／杯碟），使用內建 image_gen／OpenAI 生成一張 1672×941 RGB 圖；確切模型與費用未提供。原生檔：`C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-d48ea4db-8896-4d26-a99a-e9eeaf7d5c73.png`。
已看圖並完整解碼：Amy 攪拌拿鐵、望向 George 求助及對坐聆聽成立；人物頭部較 blocks 大、頭頂位置偏高，George 新增握杯動作，尚未完全符合底圖。舊圖保留，未重試、未替換正式 asset 或推進整體 assets 核准。

本次實際 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s02_medium_two_shot.png]：場景外觀參考圖。
圖 2 [blocks_blender_s02_medium_two_shot.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_cup.png]：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。

畫面描述：
這是一張接近坐姿眼高、略微俯拍的雙人中景。George 位於畫面左側，Amy 位於右側，兩人坐在木椅上隔桌相向。畫面呈現兩人的完整頭部、上半身、伸向桌面的前臂與手部；腿部只呈現圖 2 中露出的範圍，沿用桌面的遮擋與畫面下緣的裁切。Amy 愁眉微皺，一手握著小匙，匙端仍在面前杯中的拿鐵裡，呈現攪拌時抬眼望向 George 求助的瞬間；George 神情沉著，注視 Amy 聆聽。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

Banana 2.1 v5（2026-10-13，六圖含糖罐）：[成品](../assets/images/shot_2.1.1_banana21_v5.png)。使用者指定六圖 prompt 原文，順序為場景／blocks／George／Amy／杯碟／[糖罐](../clp/prop_sugar_jar.png)。image_selector → google_imagen，Vertex JSON／global／gemini-nano-banana-2.1，edit／2K／16:9，生成一張；2752×1536 RGB，33.62 秒。工具未回傳 token 用量，cost_usd=null、cost_status=unquoted；事前估 US$0.06～0.08，實際費用未核帳。
已看圖並完整解碼：Amy 求助／攪拌與 George 聆聽成立，糖罐採白瓷木蓋外觀；前景桌上原一個糖罐變成兩個，背景仍留 blocks 多角形藤葉，人物頭頂偏高，未完全符合底圖。未追加生成、未替換正式 asset 或推進整體 assets 核准。

本次實際 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s02_medium_two_shot.png]：場景外觀參考圖。
圖 2 [blocks_blender_s02_medium_two_shot.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_cup.png]：咖啡杯碟外觀參考圖。
圖 6 [prop_sugar_jar.png]：糖罐外觀參考圖

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
咖啡杯碟的外觀採用圖 5；糖罐的外觀採用圖 6；該圖的其他物件不參與生成。

畫面描述：
這是一張接近坐姿眼高、略微俯拍的雙人中景。George 位於畫面左側，Amy 位於右側，兩人坐在木椅上隔桌相向。畫面呈現兩人的完整頭部、上半身、伸向桌面的前臂與手部；腿部只呈現圖 2 中露出的範圍，沿用桌面的遮擋與畫面下緣的裁切。Amy 愁眉微皺，一手握著小匙，匙端仍在面前杯中的拿鐵裡，呈現攪拌時抬眼望向 George 求助的瞬間；George 神情沉著，注視 Amy 聆聽。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

GPT 新流程 v3：[成品](../assets/images/shot_2.1.1_gpt_template_v3.png)。使用者確認的新 W2I prompt 原文與場景／blocks／George／Amy／杯碟五圖送出；內建 image_gen，1672×941，模型／費用未知。Amy 攪拌拿鐵抬眼求助與 George 聆聽成立；人物頭部比例較 blocks 大，George 手臂姿態改變，並非精確對齊。 請求 `.tmp/gpt_first_newflow_v3_result.json`；舊圖保留，未追加。

本次實際 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s02_medium_two_shot.png]：場景外觀參考圖。
圖 2 [blocks_blender_s02_medium_two_shot.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_cup.png]：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。人物外觀與服裝採用圖 3、圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。咖啡杯碟外觀採用圖 5；圖 5 的其他物件不參與生成。

畫面描述：
這是一張接近人物眼高、略微俯拍的雙人中景。George 位於畫面左側，Amy 位於右側，兩人坐在木椅上隔桌相向。畫面呈現兩人的完整頭部、上半身、伸向桌面的前臂與手部，以及下緣被裁切的局部腿部。Amy 眉心微皺，一手握著小匙，匙端留在面前杯中的拿鐵裡，呈現攪拌時抬眼望向 George 求助的瞬間；George 神情沉著，注視 Amy 聆聽。兩人的肩膀與軀幹維持圖 2 的對坐朝向，除上述表情、視線、攪拌手勢及杯中飲品調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

Banana 2.1 v6（新流程）：[成品](../assets/images/shot_2.1.1_banana21_v6.png)。與 GPT 新流程 v3 相同 prompt／五圖順序，Vertex JSON／global／gemini-nano-banana-2.1、2K／16:9。2752×1536，34.8 秒；輸入 6076、圖片輸出 1680 tokens，按歷史費率估 US$0.059514，未核帳。攪拌求助與對坐聆聽成立，人物頭頂仍高於 blocks；Amy 杯柄改朝右。請求及回應 `.tmp/banana21_first_v6_result.json`／`.tmp/banana21_first_v6_response.json`；保留既有 v5 與其他舊圖，未追加。

## 2.1.2

- 圖 1 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s06_amy_medium_close_up.png)
- 圖 2 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s06_amy_medium_close_up.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)

```text
圖 1 是場景，物件與光影的絕對參考來源；圖 2 僅提供人物位置、比例、朝向與遮擋；圖 3、圖 4 分別提供 George、Amy 的外觀與服裝。

Amy 已停止攪拌，眉心皺起、嘴角下垂，輕輕歪頭，向 George 訴說 KPI 要 GG 的無奈，並小幅攤手。歪頭只調整頭部，身體朝向沿用圖 2；手勢若在取景外，不必呈現。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

v1：`assets/images/shot_2.1.2_banana21_v1.png` 已生成，保留。
v2：[成品](../assets/images/shot_2.1.2_banana21_v2.png)；依使用者提供原文送出，場景／blocks／George／Amy 四圖依序附入。Amy 無奈表情與攤手成立；George 放大成頭肩過肩前景、Amy 佔位偏右且身體較小，未符合 blocks；咖啡機顯示及桌面杯具仍有差異，待使用者檢視。2752×1536，60.19 秒；輸入 4618、圖片輸出 1680、思考 2013 tokens；按歷史費率估 US$0.0724245，未核帳。實際請求與用量 `.tmp/banana21_second_v2_result.json`；v1 請求 `.tmp/banana21_six_short_2_result.json`。

GPT 模板 v1（2026-10-13，使用者同意拼接道具）：[成品](../assets/images/shot_2.1.2_gpt_template_v1.png)。使用內建 image_gen／OpenAI，以本對話 2.1.2 prompt 原文生成一張；確切模型／費用未提供。實際五個附件依序為本節場景／blocks／George／Amy／`D:/kj-openMontage/.tmp/shot_2.1.2_props_5_6.png`；最後一張以本機原尺寸拼接杯碟與糖罐，分別標示圖 5、圖 6（3416×1085），未裁切或改繪原道具。原生輸出：`C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-33323da2-e30e-41ff-a539-bb91ff9e5c90.png`。
已看圖：Amy 訴苦、攤手及白瓷木蓋糖罐成立，George 未露頭臉；但 George 左側前景擴大、Amy 頭頂留白減少，手部入鏡範圍亦增加，未完全對齊 blocks。舊圖保留，未追加生成、未替換正式 asset 或推進整體 assets 核准。

本次實際 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s06_amy_medium_close_up.png]：場景外觀參考圖。
圖 2 [blocks_blender_s06_amy_medium_close_up.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_cup.png]：咖啡杯碟外觀參考圖。
圖 6 [prop_sugar_jar.png]：糖罐外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
咖啡杯碟的外觀採用圖 5；糖罐的外觀採用圖 6；各道具參考圖的其他物件不參與生成。

畫面描述：
這是一張接近坐姿眼高、微側拍攝的 Amy 中特寫。Amy 位於畫面中右側，完整頭部、肩膀與胸部可見，手臂及手部僅呈現圖 2 下緣可見的部分，下半身在畫外。George 只在左下角露出局部身體，頭部與臉部不入鏡。前景杯碟與糖罐沿用圖 2 的位置及下緣裁切。Amy 已停止攪拌，眉心皺起、嘴角下垂，頭部微偏，望向畫面左側的 George 訴苦，呈現焦慮與無奈；小幅攤手僅在原取景容納的範圍內呈現，肩膀與軀幹維持圖 2 的朝向。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

Banana 2.1 v3（2026-10-13，六張獨立參考圖）：[成品](../assets/images/shot_2.1.2_banana21_v3.png)。沿用下方 2.1.2 prompt 原文，附件依序為場景／blocks／George／Amy／`clp/prop_coffee_cup.png`／`clp/prop_sugar_jar.png`，未使用 GPT 拼接圖。image_selector → google_imagen，Vertex JSON／global／gemini-nano-banana-2.1，edit／2K／16:9；一張 2752×1536 RGB，55.53 秒。工具未回傳 token 用量，cost_usd=null、cost_status=unquoted；事前估 US$0.06～0.08，實際費用未核帳。
已看圖並完整解碼：Amy 無奈表情與攤手可辨識，但 George 被擴大成左側過肩人物並露出側臉；背景吧台、層架及咖啡機配置重建，Amy 佔位／人物比例與桌面裁切也偏離 blocks；木蓋糖罐變寬矮且失去蓋頂把手。構圖與參考一致性未通過。舊圖保留，未追加生成、未替換正式 asset 或推進整體 assets 核准。

本次實際 prompt：

```text
參考圖說明：
圖 1 [empty_banana_s06_amy_medium_close_up.png]：場景外觀參考圖。
圖 2 [blocks_blender_s06_amy_medium_close_up.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_cup.png]：咖啡杯碟外觀參考圖。
圖 6 [prop_sugar_jar.png]：糖罐外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
咖啡杯碟的外觀採用圖 5；糖罐的外觀採用圖 6；各道具參考圖的其他物件不參與生成。

畫面描述：
這是一張接近坐姿眼高、微側拍攝的 Amy 中特寫。Amy 位於畫面中右側，完整頭部、肩膀與胸部可見，手臂及手部僅呈現圖 2 下緣可見的部分，下半身在畫外。George 只在左下角露出局部身體，頭部與臉部不入鏡。前景杯碟與糖罐沿用圖 2 的位置及下緣裁切。Amy 已停止攪拌，眉心皺起、嘴角下垂，頭部微偏，望向畫面左側的 George 訴苦，呈現焦慮與無奈；小幅攤手僅在原取景容納的範圍內呈現，肩膀與軀幹維持圖 2 的朝向。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

Banana 2.1 v4（2026-10-13，依使用者要求重新生成）：[成品](../assets/images/shot_2.1.2_banana21_v4.png)。沿用上方 v3 所列 2.1.2 prompt 原文與場景／blocks／George／Amy／杯碟／糖罐六張獨立參考，未使用 GPT 拼接圖。image_selector → google_imagen，Vertex JSON／global／gemini-nano-banana-2.1，edit／2K／16:9；一張 2752×1536 RGB，35.77 秒。工具未回傳 token 用量，cost_usd=null、cost_status=unquoted；事前估 US$0.06～0.08，實際費用未核帳。
已看圖並完整解碼：Amy 訴苦與攤手可辨識，但 Amy 佔位偏右、頭頂上移、手部入鏡範圍增加；George 左側前景擴大，左緣出現局部眼鏡；糖罐保留金屬蓋，未採圖 6 木蓋外觀。人物構圖與糖罐參考未完全符合。v3 與舊圖保留，本輪僅生成一次，未替換正式 asset 或推進整體 assets 核准。

## 2.1.3

- 圖 1 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png)
- 圖 2 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)
- 圖 5 [prop_coffee_cup.png](D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png)

```text
圖 1 是場景，物件，風格，與光影的絕對參考來源；圖 2 僅提供人物位置、人物朝向、人物比例與遮擋；圖 3、圖 4 分別提供 George、Amy 的外觀與服裝；圖 5 提供咖啡杯碟外觀。

George 溫和微笑看向 Amy，一手握住原有咖啡杯的杯柄，準備放回杯碟；杯底尚未接觸碟面，保留清楚空隙，碟上不留重複杯。Amy 安靜聆聽。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

v1：已生成，保留於 `.tmp/shot_2.1.3_banana21_v1.png`；請求 `.tmp/banana21_six_short_3_result.json`。
v2：[成品](../assets/images/shot_2.1.3_banana21_v2.png)；已依確認原文送出，場景／blocks／George／Amy／杯碟五圖依序附入。George 微笑握杯、杯底離碟且碟上無重複杯成立；背景主要構件保留，但 George 佔位偏左、頭頂較高，Amy 前景露出較多側臉，未完全符合 blocks，待使用者檢視。2752×1536，40.14 秒；輸入 5732、圖片輸出 1680、思考 1145 tokens；按歷史費率估 US$0.0675855，未核帳。實際請求與用量 `.tmp/banana21_third_v2_result.json`；未追加重生。

v3：[成品](../assets/images/shot_2.1.3_banana21_v3.png)；依使用者新版將圖 1 明列為場景、物件、風格、氣氛與光影的絕對參考來源（氣圍訂正為氣氛），其餘表演與五圖順序不變。握杯／杯底離碟成立，但變為雙人側面對坐，Amy 不再是 blocks 指定過肩前景，人物佔位及朝向不符合原鏡位，待使用者檢視。2752×1536，33.8 秒；輸入 5738、圖片輸出 1680、文字輸出 34、思考 548 tokens；按歷史費率估 US$0.063372，未核帳。實際請求與用量 `.tmp/banana21_third_v3_result.json`；僅生成一次，舊圖保留。

v4：[成品](../assets/images/shot_2.1.3_banana21_v4.png)；使用者新版原文送出，移除氣氛、圖 2 明列人物位置／人物朝向／人物比例與遮擋，五圖順序不變。恢復 Amy 右側過肩前景，George 微笑握杯／杯底離碟成立；人物佔位仍未完全對齊 blocks，Amy 仍露部分側臉，待使用者檢視。2752×1536，35.83 秒；輸入 5737、圖片輸出 1680 tokens；按歷史費率估 US$0.0590055，未核帳。實際請求與用量 `.tmp/banana21_third_v4_result.json`；僅生成一次，舊圖保留。


### 2.1.3 GPT 模板 v1（2026-10-13）

```text
參考圖說明：
圖 1 [empty_banana_s03_ots_to_george.png]：場景外觀參考圖。
圖 2 [blocks_blender_s03_ots_to_george.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_cup.png]：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。

畫面描述：
這是一張接近坐姿眼高、略微俯拍，從 Amy 肩後望向 George 的過肩中景。George 位於畫面中左側，坐在桌子對面的木椅上，完整頭部、上半身及桌面附近的部分前臂與手部可見。Amy 位於右側近景，以後腦、肩背及局部手臂入鏡，沿用圖 2 的右緣與下緣裁切，以及對 George 和桌面的遮擋。兩人的下半身不入鏡。George 溫和微笑，望向 Amy，一手握著原有咖啡杯的杯柄，呈現正要將杯子放回面前杯碟的瞬間；杯底尚未接觸碟面，兩者之間保留清楚空隙，杯碟維持圖 2 的位置，碟上不留重複杯。Amy 維持圖 2 的頭部與軀幹朝向，安靜聆聽。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

生成紀錄：id=shot_2.1.3_gpt_template_v1；type=image；scene_id=shot_2.1.3；source_tool=image_gen（內建）；供應商 OpenAI，確切模型與費用未提供。原 prompt 與場景／blocks／George／Amy／杯碟五張獨立參考依序送出，僅生成一張。[成品](../assets/images/shot_2.1.3_gpt_template_v1.png)；原生來源：C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-03b52f12-6235-406a-a5d1-2210039f8ad2.png。
檢視：George 微笑看向 Amy、握杯柄、杯底離碟及碟上無重複杯成立，Amy 為頭肩背影；George 頭部偏大／偏左、頭頂留白減少，Amy 頭頂也上移，桌面顯露範圍增加，原本被遮住的糖罐及 Amy 杯子露出，構圖未完全符合 blocks。已看圖、Pillow 完整解碼（1672×941 RGB）及複製 SHA256 核對；未替換正式 asset、未追加生成、未推進整體 assets 核准。


### 2.1.3 Banana 模板 v5（2026-10-13）

沿用上方 GPT 模板 v1 的完整 prompt 原文與五張獨立參考圖（場景／blocks／George／Amy／杯碟），無文字改寫。[成品](../assets/images/shot_2.1.3_banana21_v5.png)；id=shot_2.1.3_banana21_v5；type=image；scene_id=shot_2.1.3；source_tool=image_selector → google_imagen；Vertex AI／服務帳戶 JSON／global／gemini-nano-banana-2.1；generation_mode=edit；resolution=2K；aspect_ratio=16:9；number_of_images=1。工具成功，37.5 秒，2752×1536 RGB；工具未回傳用量或實際費用（cost_usd=null、cost_status=unquoted），事前依歷史用量估 US$0.06～0.08，未核帳。
檢視：George 微笑看向 Amy、握杯柄、杯底離碟及碟上無重複杯成立；George 頭部偏大／偏左／頭頂上移，Amy 頭頂上移並露出部分側臉，前景遮擋縮小而露出原被擋住的糖罐及 Amy 杯子，構圖未完全符合 blocks。已看圖及 Pillow 完整解碼；僅生成一張，保留 GPT 與 Banana 舊版，未追加生成、未替換正式 asset 或推進整體 assets 核准。

## 2.1.4

- 圖 1 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s08_amy_close_up.png)
- 圖 2 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s08_amy_close_up.png)
- 圖 3 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)

```text
圖 1 是場景，物件，風格，與光影的絕對參考來源；圖 2 是取景範圍、人物位置、人物朝向、人物顯示範圍與比例，遮擋的絕對參考來源；圖 3 僅提供 Amy 的外觀與服裝，不採用其展示姿態與取景。

將圖 2 的紅色人物原位替換為 Amy，維持人物在畫面中的佔位與裁切，呈現頭肩特寫，不縮小人物以展示更多身體。

Amy 睜大眼睛、微抬眉，輕輕歪頭，嘴唇微張。只調整頭部傾斜與表情，肩膀與軀幹朝向沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

v1：已生成，保留於 `.tmp/shot_2.1.4_banana21_v1.png`；請求 `.tmp/banana21_six_short_4_result.json`。
v2：[成品](../assets/images/shot_2.1.4_banana21_v2.png)；使用者原文 prompt，場景／blocks／Amy 三圖依序附入。睜眼、抬眉、微張嘴與輕微歪頭成立；人物偏右、頭頂上移，身體變為較寬半身取景，未符合 blocks 特寫比例。2752×1536，35.87 秒；輸入 3469、圖片輸出 1680 tokens；按歷史費率估 US$0.0556035，未核帳。實際請求與用量 `.tmp/banana21_fourth_v2_result.json`；未追加生成。

v3 嘗試：使用者新版原文，明列圖2取景範圍／人物顯示範圍及原位替換。Vertex OAuth `oauth2.googleapis.com/token` 連線逾時（ConnectTimeoutError）；無新圖、無用量回傳，費用未核帳。首次請求與錯誤 `.tmp/banana21_fourth_v3_oauth_timeout.json`；未重試、未改模型或認證。

v3 第二次嘗試：使用者要求重生後，相同 prompt／三圖／模型重送一次。認證成功且收到模型回應，但 adapter 未取得非 thought 的 inline 圖片，報 `No image data returned (text-only response)`；此錯誤字串不能證明所有回應都只有文字，因用量含 IMAGE 1120 tokens。無新圖；輸入 3533、輸出圖片 1120／文字 170、思考 1028 tokens，按歷史費率估 US$0.0478845，未核帳。紀錄 `.tmp/banana21_fourth_v3_result.json`；未再次重送，未更改 prompt／模型／認證。


### 2.1.4 GPT 模板 v1（2026-10-13）

```text
參考圖說明：
圖 1 [empty_banana_s08_amy_close_up.png]：場景外觀參考圖。
圖 2 [blocks_blender_s08_amy_close_up.png]：構圖底圖。
圖 3 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為 Amy，只呈現圖 2 中可見的部位，不補出畫外身體。Amy 的外觀與服裝採用圖 3，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張接近坐姿眼高、微側拍攝的 Amy 頭肩特寫。Amy 位於畫面中右側，完整頭部、頸部、肩膀與上胸部可見，上半身及上臂沿用圖 2 下緣的裁切；雙手與下半身在畫外，George 不入鏡。Amy 眼睛因驚奇而睜大，眉毛微抬，頭部輕輕歪向一側，嘴唇微張，望向畫面左側的畫外 George，呈現聽到「企業健康指標」這個比喻後，好奇反問的瞬間。只調整表情、視線與頭部輕微傾斜，肩膀及軀幹維持圖 2 的朝向。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

生成紀錄：id=shot_2.1.4_gpt_template_v1；type=image；scene_id=shot_2.1.4；source_tool=image_gen（內建）；供應商 OpenAI，確切模型與費用未提供。原 prompt 與場景／blocks／Amy 三張獨立參考依序送出，僅生成一張。[成品](../assets/images/shot_2.1.4_gpt_template_v1.png)；原生來源：C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-af206609-a9ef-4335-84cc-baf38ceba975.png。
檢視：Amy 睜眼、抬眉、歪頭、微張嘴及單人頭肩畫面成立，George／雙手／下半身未入鏡；人物偏右、頭部上移且頭頂留白減少，視線偏左上，構圖未完全符合 blocks。已看圖、Pillow 完整解碼（1672×941 RGB）及複製 SHA256 核對；未替換正式 asset、未追加生成、未推進整體 assets 核准。


### 2.1.4 GPT 模板 v2（2026-10-13）

```text
參考圖說明：
圖 1 [empty_banana_s08_amy_close_up.png]：場景外觀參考圖。
圖 2 [blocks_blender_s08_amy_close_up.png]：構圖底圖。
圖 3 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為 Amy，只呈現圖 2 中可見的部位，不補出畫外身體。Amy 的外觀與服裝採用圖 3，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張接近坐姿眼高、微側拍攝的 Amy 頭肩特寫。Amy 位於畫面中右側，完整頭部、頸部、肩膀與上胸部可見，上半身及上臂沿用圖 2 下緣的裁切；雙手與下半身在畫外，George 不入鏡。Amy 眼睛因驚奇而睜大，眉毛微抬，頭部輕輕歪向一側，嘴唇微張，望向畫面左側的畫外 George，呈現聽到「企業健康指標」這個比喻後，好奇反問的瞬間。只調整表情、視線與頭部輕微傾斜，肩膀及軀幹維持圖 2 的朝向，即George的方向。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

生成紀錄：id=shot_2.1.4_gpt_template_v2；type=image；scene_id=shot_2.1.4；source_tool=image_gen（內建）；供應商 OpenAI，確切模型與費用未提供。使用者新版原文（三圖同 v1，加入「即George的方向」）生成一張。[成品](../assets/images/shot_2.1.4_gpt_template_v2.png)；原生來源：C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-2f6a0310-e144-4140-8618-c4f208d86964.png。
檢視：驚奇／歪頭／微張嘴成立；人物仍偏右、頭頂留白減少、胸部露出增加。使用者指出身體應轉向左前方，本版身體朝向未接受。已看圖、Pillow 完整解碼（1672×941 RGB）及複製 SHA256 核對；保留前版、未替換正式 asset 或推進整體 assets 核准。


### 2.1.4 GPT 身體朝向修正 v3（2026-10-13）

使用者指出「身體要轉向左前方才對」，兩次均以 v2 圖片為唯一編輯底圖。工具 image_gen（內建）／OpenAI，確切模型與費用未提供。第一次肩線改變但胸口仍朝相反方向，未採用；原生檔保留於 C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-14593896-6b08-49d4-ba29-51194578b02d.png。

第一次送出原文：
```text
以這張 2.1.4 圖片為編輯底圖，修正 Amy 的身體朝向。

Amy 的肩膀、胸口與軀幹必須一起轉向畫面左前方，也就是畫外 George 所在的方向。讓西裝正面與胸口明確朝左前方，呈自然的三分之四側身，不再正對鏡頭；不是只轉頭或只移動視線。保留原本坐姿，肩膀、上臂與西裝衣褶隨軀幹轉向自然調整。

保留 Amy 的人物外觀、服裝、驚奇睜眼、微抬眉、微張嘴、輕微歪頭及朝畫面左側的視線。維持人物目前在畫面中的位置、頭部大小與頭頂位置，不平移人物。攝影機位置、取景、透視、背景物件、材質、光影與色彩沿用底圖；維持頭肩與上胸部的裁切，雙手及下半身不入鏡，George 不入鏡。

只進行上述身體朝向及必要的衣服、肩臂連動調整。
輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

第二次補充以畫面左右辨識的肩膀遠近關係，所用原文：
```text
編輯這張圖片，僅修正 Amy 胸口與肩膀的朝向。畫面中的左、右一律指觀眾看到的畫面左、右。

Amy 保持坐姿，整個上半身轉向畫面左前方的畫外 George，呈三分之四側身：
- 畫面右側的肩膀是靠近鏡頭的肩膀，較大、較近。
- 畫面左側的肩膀退向遠處，較小、較遠。
- 胸口、西裝的前襟與白襯衫的正面一起朝畫面左前方。
- 上半身的转向与她望向畫面左側的頭臉方向一致，不能出現頭朝左而胸口朝右的扭身。
這次真正需要改的是軀幹的左右轉向，並相應調整肩膀、上臂及衣服摺痕。

保留 Amy 的臉、髮型、服裝款式、驚奇睜眼、微張嘴和頭部輕微傾斜。保留原人物在畫面中的位置、頭部大小及頭頂位置，保留原攝影機取景與16:9比例，維持雙手及下半身不入鏡。背景咖啡機、磨豆機、木牆、櫃台、椅子與原光影沿用底圖。
輸出一張彩色分鏡圖，不加入字幕。
```

採用的修正樣圖：[v3](../assets/images/shot_2.1.4_gpt_template_v3.png)；id=shot_2.1.4_gpt_template_v3；type=image；scene_id=shot_2.1.4；source_tool=image_gen；原生來源：C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-df5300f5-7ddc-4c36-9d98-49ea0bbd882f.png。胸口／衣襟轉向畫面左前方，畫面右肩較近，頭部位置、驚奇表情與主要背景保留；承襲 v2 原有偏右／頭頂留白較少的構圖，不宣稱完全對齊 blocks。已看圖、Pillow 完整解碼（1672×941 RGB）及複製 SHA256 核對。本輪身體修正共生成兩次；未替換正式 asset 或推進整體 assets 核准。


### 2.1.4 Banana 身體朝向對照 v4（2026-10-13）

使用上方「GPT 身體朝向修正 v3」第二次編輯 prompt 原文，唯一底圖為 `assets/images/shot_2.1.4_gpt_template_v2.png`；本次為 I2I 身體轉向對照，未重送場景／blocks／Amy 三圖模板。[成品](../assets/images/shot_2.1.4_banana21_v4.png)；id=shot_2.1.4_banana21_v4；type=image；scene_id=shot_2.1.4；source_tool=image_selector → google_imagen；Vertex AI／服務帳戶 JSON／global／gemini-nano-banana-2.1；generation_mode=edit；resolution=2K；aspect_ratio=16:9；number_of_images=1。工具成功，26.8 秒，2752×1536 RGB；未回傳用量或實際費用（cost_usd=null、cost_status=unquoted），事前估 US$0.06～0.08，未核帳。
檢視：Amy 驚奇睜眼／微張嘴及頭臉朝左保留，但肩胸仍未明確轉向左前方，未達指定身體朝向；人物及背景主要位置保留，機器顯示數字等局部細節改變。已看圖及 Pillow 完整解碼；僅生成一張，保留 GPT／Banana 舊版，未追加重生、未替換正式 asset 或推進整體 assets 核准。

## 2.1.5

- 圖 1 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s07_george_close_up.png)
- 圖 2 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s07_george_close_up.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)

```text
參考圖說明：
圖 1 [empty_banana_s07_george_close_up.png]：場景參考圖。
圖 2 [blocks_blender_s07_george_close_up.png]：人物定位圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
場景、物件、材質、風格與光影以圖 1 為準。
最終構圖以圖 2 為準，包括取景、人物位置、朝向、畫面佔比，以及人物與場景物件的遮擋關係。
將圖 2 的藍色人物原位替換為 George；人物外觀與服裝採用圖 3，不採用其展示姿態與取景。
參考圖之間有差異時，依上述分工處理。

畫面人物動作描述：
George 下巴略收，帶著肯定的神情與溫和微笑，嘴唇自然微張。只調整頭部姿態與表情，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

v1：[成品](../assets/images/shot_2.1.5_banana21_v1.png)；已依使用者確認的參考圖說明／生圖指引／畫面人物動作描述格式送出，SH07 場景／blocks／George 三圖依序附入。單人微笑與微張嘴成立；頭頂較高、肩身佔位較窄，前景椅背遮住身體下緣，未完全符合 blocks，待使用者檢視。2752×1536，31.17 秒；輸入 3607、圖片輸出 1680 tokens；按歷史費率估 US$0.0558105，未核帳。實際請求與用量 `.tmp/banana21_fifth_v1_result.json`，原始模型回應 `.tmp/banana21_fifth_v1_response.json`；未追加生成。

v2：[成品](../assets/images/shot_2.1.5_banana21_v2.png)；使用者確認的通用模板原文送出，素材用途集中於生圖指引，三圖順序不變。微笑微張嘴成立，但人物偏左、頭頂上移、肩身比例未對齊 blocks，前景椅背仍遮在人物前方，未解決入座遮擋問題，待使用者檢視。2752×1536，36.32 秒；輸入 3629、圖片輸出 1680、思考 1273 tokens；按歷史費率估 US$0.065391，未核帳。實際請求與用量 `.tmp/banana21_fifth_v2_result.json`，原始模型回應 `.tmp/banana21_fifth_v2_response.json`；未追加生成。

GPT 同指令比較：[成品](../assets/images/shot_2.1.5_gpt_compare_v1.png)。依使用者要求使用內建 image_gen，與 Banana 第五鏡 v2 完全相同 prompt／三圖／順序，未加椅子補句。1672×941，確切模型／費用未知；人物遮住前景椅背、未橫擋身體，遮擋較符合 blocks，但頭頂偏高與人物比例仍未完全對齊，不能據單次結果宣稱穩定優於 Banana。紀錄 `.tmp/gpt_fifth_compare_v1_result.json`；未追加生成。

第五鏡 GPT 判讀訂正：使用者確認 George 坐在自己的椅子，後方是另一張窗台邊椅子；入座與椅子關係成立。撤回後續對 GPT 座椅關係的錯誤判斷，不因兩段椅背判錯。


### 2.1.5 GPT 模板 v1（2026-10-13）

```text
參考圖說明：
圖 1 [empty_banana_s07_george_close_up.png]：場景外觀參考圖。
圖 2 [blocks_blender_s07_george_close_up.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為 George，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。

畫面描述：
這是一張接近坐姿眼高、微側拍攝的 George 頭肩特寫。George 位於畫面中左側，完整頭部、頸部、肩膀與上胸部可見，上半身及上臂沿用圖 2 下緣的裁切；雙手、桌面與下半身在畫外，Amy 不入鏡。George 下巴略收，帶著肯定的神情與溫和微笑，嘴唇自然微張，望向畫面右側的畫外 Amy，呈現輕輕點頭回應並開始解釋 EPS 的瞬間。只調整表情、視線與頭部輕微姿態，肩膀及軀幹維持圖 2 的朝向，胸口朝向畫面右前方的 Amy。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

生成紀錄：id=shot_2.1.5_gpt_template_v1；type=image；scene_id=shot_2.1.5；source_tool=image_gen（內建）；供應商 OpenAI，確切模型與費用未提供。原 prompt 與場景／blocks／George 三張獨立參考依序送出，僅生成一張。[成品](../assets/images/shot_2.1.5_gpt_template_v1.png)；原生來源：C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-e3592221-3a1e-48ce-856d-dac562f45aa5.png。
檢視：George 溫和微笑、微張嘴及單人頭肩畫面成立，Amy／雙手／桌面／下半身未入鏡；頭部偏大且偏左、頭頂上移，視線偏右上，肩胸朝右前方的轉向不明顯，構圖及表演未完全符合原 prompt／blocks。已看圖、Pillow 完整解碼（1672×941 RGB）及複製 SHA256 核對；未替換正式 asset、未追加生成、未推進整體 assets 核准。

## 2.1.6

- 圖 1 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s09_table_insert.png)
- 圖 2 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s09_table_insert.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)
- 圖 5 [prop_coffee_set.png](D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png)

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

畫面描述：
這是一張由上往下斜俯拍的桌面插入特寫（insert）。木桌面佔滿畫面，George 位於畫面左側，Amy 位於右側，兩人隔桌對坐。畫面僅呈現兩人伸入桌面的前臂與手部，以及左右邊緣被裁切的局部身體；頭部與臉部均在畫面外。George 的咖啡杯已放回杯碟，兩只咖啡杯均置於各自杯碟上；兩人的前臂與手部位置、姿態沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

GPT 通用模板 v1：[成品](../assets/images/shot_2.1.6_gpt_template_v1.png)。依確認 prompt 原文與場景／blocks／George／Amy／杯碟五圖，使用內建 image_gen 生成；1672×941，確切模型／費用未知。雙杯在碟上、雙手停在桌邊成立；取景擴大露出兩人頭部，金屬蓋罐變木蓋，未完全遵守 blocks 及背景圖，待使用者檢視。實際請求紀錄 `.tmp/gpt_sixth_template_v1_result.json`；第六鏡 Banana 仍未生成，舊 OpenAI 圖保留，未追加生成。

GPT 通用模板 v2：[成品](../assets/images/shot_2.1.6_gpt_template_v2.png)。依確認新版原文，以图2為編輯底圖、只替換可見部位；五圖與順序不變。1672×941，確切模型／費用未知。金屬罐蓋恢復、雙杯在碟與手停桌邊成立；仍露出兩人頭部、杯子改為並排，未遵守 blocks 的取景與配置，George 兩腕均出現錶狀飾物，待檢視。紀錄 `.tmp/gpt_sixth_template_v2_result.json`；舊圖保留，未追加。

GPT 通用模板 v3：[成品](../assets/images/shot_2.1.6_gpt_template_v3.png)。使用者確認將取景與動作合併為單段畫面描述，原文與五張參考圖依序送至內建 image_gen。1672×941，確切模型／費用未知。頭部與臉部在畫外、雙杯左下右上錯位及金屬蓋成立；手部呈握拳姿態，局部佔位並非精確對齊 blocks，待使用者檢視。請求紀錄 `.tmp/gpt_sixth_template_v3_result.json`；舊圖保留，未追加生成。

Banana 2.1 v1：[成品](../assets/images/shot_2.1.6_banana21_v1.png)。與 GPT v3 相同 prompt 原文及五圖順序，Vertex JSON／global／gemini-nano-banana-2.1，2K／16:9。成功生成 2752×1536，33.11 秒；輸入 6013、圖片輸出 1680 tokens，按歷史費率估 US$0.0594195，未核帳。雙杯錯位及金屬蓋成立，但上緣仍露出 George 下巴／鬍鬚及 Amy 部分臉部，人物軀幹比 blocks 顯露更多，未完全符合取景。實際請求與回應 `.tmp/banana21_sixth_v1_result.json`／`.tmp/banana21_sixth_v1_response.json`；未重試。

### 2.1.6 GPT 模板 v4（2026-10-13）

```text
參考圖說明：
圖 1 [empty_banana_s09_table_insert.png]：場景外觀參考圖。
圖 2 [blocks_blender_s09_table_insert.png]：構圖底圖。
圖 3 [char_esg_george.png]：George 人物參考圖，對應圖 2 的藍色人物。
圖 4 [char_esg_amy.jpeg]：Amy 人物參考圖，對應圖 2 的紅色人物。
圖 5 [prop_coffee_set.png]：咖啡杯碟外觀參考圖。

生圖指引：
以圖 2 為編輯底圖，保留其取景、透視、物件配置、人物佔位、顯示範圍與遮擋關係。

將定位人物替換為對應角色，只呈現圖 2 中可見的部位，不補出畫外身體。George 的外觀與服裝採用圖 3，Amy 的外觀與服裝採用圖 4，不採用其展示姿態或構圖。

將場景的材質、風格與光影更新為圖 1 的外觀，不改變圖 2 的空間配置。
咖啡杯碟的外觀採用圖 5；該圖的其他物件不參與生成。糖罐的外觀沿用圖 1 的白色罐身與金色金屬蓋。

畫面描述：
這是一張由高位向下斜俯拍的桌面插入特寫。畫面以木桌面為主體，George 位於左側，Amy 位於右側，兩人隔桌對坐。只呈現兩人伸入桌面的前臂、手部，以及左右邊緣被裁切的局部身體；頭部與臉部均在畫外。George 的杯碟位於畫面左下方，Amy 的杯碟位於右上方，糖罐位於上方中央，沿用圖 2 的位置與裁切。兩只咖啡杯均已放在各自杯碟上，兩人的前臂與手部維持圖 2 的位置及姿態，呈現 George 畫外講述、Amy 聆聽時的桌面瞬間。除上述指定調整外，其餘沿用圖 2。

輸出一張 16:9 彩色分鏡圖，不加入字幕。
```

生成紀錄：id=shot_2.1.6_gpt_template_v4；type=image；scene_id=shot_2.1.6；source_tool=image_gen（內建）；供應商 OpenAI，確切模型與實際費用未提供。原 prompt 與場景／blocks／George／Amy／杯碟五張獨立參考依序送出，僅生成一張，工具耗時 48 秒。[成品](../assets/images/shot_2.1.6_gpt_template_v4.png)；原生來源：C:/Users/servi/.codex/generated_images/01a133fe-9f94-7881-8661-889a33653287/exec-60c63bb7-9d5e-4688-9e79-68c781179a98.png。
檢視：雙杯在碟、左下／右上錯位與白色罐身／金色金屬蓋成立；George 改成雙手攤開比劃、Amy 改成雙手交握，手部位置與姿態未沿用 blocks，人物邊緣裁切亦未完全符合。已看圖、Pillow 完整解碼（1672×941 RGB）及複製 SHA256 核對；未追加生成、未替換正式 asset、未推進整體 assets 核准。
