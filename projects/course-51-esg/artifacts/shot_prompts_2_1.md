# Scene 2.1.1～2.1.6｜逐鏡生圖短指令

更新：2026-10-13。依使用者決定，本組改用逐鏡短指令；狀態：六鏡均已有生成圖片：2.1.1～2.1.3、2.1.5～2.1.6 為 v1；2.1.4 為 v2，v1 保留。2.1.5 首次遭服務攔截，使用者要求後以原指令重試成功；各鏡差異見下方紀錄，未代表全部驗收通過。

依據：`script.json`、`master_script.md`、`scene_plan.json`（皆在本目錄），以及 `../references/scenes/coffee_shop/scene_camera_char_meta.json`。
本檔保存生圖指令與素材對應；故事、台詞和時間以 scene_plan 為準，相機與人物綁定以 meta 為準。

## 共用短指令

背景沿用本鏡空景；依 blocks 的人物位置、整體大小、朝向與遮擋置入 CLP 角色，藍色是 George、紅色是 Amy。角色外觀與自身頭身比例依 CLP，表演依逐鏡指令。人物坐入既有椅子。維持參考圖的既有 3D 動畫風格、取景與暖色日光，輸出一張 16:9 彩色分鏡圖；不呈現方塊、參考圖展示排版或新增字幕。

使用方式：每次將「共用短指令＋該鏡短指令」及該鏡所列圖片一起送入生圖工具。素材按列出順序附入；路徑清單本身不能代替圖片。

## 2.1.1｜Amy 求救｜s02_medium_two_shot／40mm

- 圖 1 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s02_medium_two_shot.png)
- 圖 2 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s02_medium_two_shot.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)
- 圖 5 [prop_coffee_cup.png](D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png)

短指令：Amy 愁眉微皺，一手握小匙、匙端仍在拿鐵中，抬眼望向 George 求助；George 沉著聆聽。保留雙人中景與桌面互動。

生成紀錄（2026-10-13）：`shot_2.1.1_short_v1`，image，scene_id=`shot_2.1.1`；[成品](../assets/images/shot_2.1.1_short_v1.png)。工具 `image_gen`，供應商 OpenAI，模型與費用未回報；新生成素材，沿用專案五張參考圖。
實際 prompt：先加「圖 1 是 blocks，圖 2 是同鏡空景，圖 3 是 George CLP，圖 4 是 Amy CLP，圖 5 是杯碟外觀。」，再接本檔共用短指令及 2.1.1 短指令。
檢視：求助／攪拌與聆聽可辨識；人物較 blocks 放大並向內靠、頭頂留白減少，另有托腮姿勢，背景細節非完全相同；待使用者檢視，未視為構圖完全通過。

## 2.1.2｜Amy 訴苦｜s06_amy_medium_close_up／65mm

- 圖 1 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s06_amy_medium_close_up.png)
- 圖 2 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s06_amy_medium_close_up.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)

短指令：Amy 已停止攪拌，眉心皺起、嘴角下垂、頭微偏，望向 George 訴說 KPI 要 GG 的無奈；小幅攤手僅在原取景容納處呈現。George 只保留 blocks 所示局部前景，不補出臉。

生成紀錄（2026-10-13）：`shot_2.1.2_short_v1`，image，scene_id=`shot_2.1.2`；[成品](../assets/images/shot_2.1.2_short_v1.png)。工具 `image_gen`，供應商 OpenAI，模型與費用未回報；新生成素材，沿用本鏡四張參考圖。
實際 prompt：先加「圖 1 是 blocks，圖 2 是同鏡空景，圖 3 是 George CLP，圖 4 是 Amy CLP。」，再接本檔共用短指令及 2.1.2 短指令。
檢視：Amy 無奈訴苦及攤手可辨識；George 被擴大成明顯過肩前景並露出部分側臉，不符合 blocks 局部入鏡及不補臉要求；Amy 頭頂留白也減少。構圖未通過，保留供使用者檢視，未追加生成。

## 2.1.3｜George 解惑｜s03_ots_to_george／60mm

- 圖 1 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s03_ots_to_george.png)
- 圖 2 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s03_ots_to_george.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)
- 圖 5 [prop_coffee_cup.png](D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_cup.png)

短指令：George 溫和微笑看向 Amy，一手握咖啡杯柄，準備放回原杯碟；杯底尚未接觸碟面，保留清楚空隙。Amy 以頭肩背影聆聽。握起原有杯子，碟上不留重複杯。

生成紀錄（2026-10-13）：`shot_2.1.3_short_v1`，image，scene_id=`shot_2.1.3`；[成品](../assets/images/shot_2.1.3_short_v1.png)。工具 `image_gen`，供應商 OpenAI，模型與費用未回報；新生成素材，沿用本鏡五張參考圖。
實際 prompt：先加「圖 1 是 blocks，圖 2 是同鏡空景，圖 3 是 George CLP，圖 4 是 Amy CLP，圖 5 是杯碟外觀。」，再接本檔共用短指令及 2.1.3 短指令。
檢視：George 微笑看向 Amy、握杯柄、杯底離碟空隙與空碟成立；Amy 頭肩背影成立。George 頭部佔比較 blocks 大、頭頂留白減少；背景主要窗牆關係保留，非逐像素一致。待使用者檢視，未追加生成。

## 2.1.4｜Amy 反問｜s08_amy_close_up／100mm

- 圖 1 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s08_amy_close_up.png)
- 圖 2 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s08_amy_close_up.png)
- 圖 3 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)

短指令：Amy 聽見「企業健康指標」而睜大眼睛、微抬眉、輕輕歪頭，嘴唇微張，望向畫外 George 驚奇反問。維持單人頭肩特寫。身體維持 blocks 中朝向對坐的 George，肩膀與軀幹不轉動，只輕輕歪頭；頭與胸口朝向同一位對坐者，不做側身回頭姿勢。

生成紀錄（2026-10-13）：`shot_2.1.4_short_v1`，image，scene_id=`shot_2.1.4`；[成品](../assets/images/shot_2.1.4_short_v1.png)。工具 `image_gen`，供應商 OpenAI，模型與費用未回報；新生成素材，沿用本鏡三張參考圖。
實際 prompt：先加「圖 1 是 blocks，圖 2 是同鏡空景，圖 3 是 Amy CLP。」，再接本檔共用短指令及當時的 2.1.4 短指令（僅至「維持單人頭肩特寫。」，不含後來新增的身體朝向限制）。
檢視：Amy 睜眼、抬眉、歪頭、嘴唇微張及望向畫外的驚奇反問成立，維持單人頭肩特寫；頭部較 blocks 放大、髮頂被上緣裁切，背景細節非逐像素一致。待使用者檢視，未追加生成。

修正與生成（2026-10-13）：使用者確認歪頭可保留，身體須維持對坐朝向；v1 驗收漏查軀幹朝向，不能把側面鏡位解釋為人物轉身要求。
`shot_2.1.4_short_v2`，image，scene_id=`shot_2.1.4`；[修正版](../assets/images/shot_2.1.4_short_v2.png)。工具 `image_gen`，OpenAI，模型／費用未回報；沿用相同三圖重生，v1 保留。
實際 prompt：圖 1 是 blocks，圖 2 是同鏡空景，圖 3 是 Amy CLP。再接共用短指令與本鏡修正後的完整短指令。
檢視：肩膀／胸口扭轉感較 v1 減少，保留歪頭及驚奇反問；頭部仍較 blocks 放大，頭頂留白較少，未宣稱幾何完全一致。待使用者檢視，未再追加生成。

## 2.1.5｜George 講解 EPS｜s07_george_close_up／100mm

- 圖 1 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s07_george_close_up.png)
- 圖 2 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s07_george_close_up.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)

短指令：George 下巴略收，帶著剛點頭後的肯定神情與溫和微笑，嘴唇自然微張，望向畫外 Amy 解釋 EPS。維持單人頭肩特寫，手部與杯子留在畫外。身體維持 blocks 中朝向對坐的 Amy，肩膀與軀幹不額外轉動，頭與胸口朝向同一位對坐者，不做側身回頭姿勢。

生成嘗試（2026-10-13）：2.1.5 使用 `image_gen`／OpenAI，沿用本鏡三張參考圖，模型與費用未回報；未產出圖片。
實際 prompt：先加「圖 1 是 blocks，圖 2 是同鏡空景，圖 3 是 George CLP。」，再接共用短指令與本鏡完整短指令（含對坐身體朝向限制）。
錯誤：HTTP 400，`image_generation_user_error`／`moderation_blocked`，moderation_stage=`output`，categories=`other`；request ID `15d78c48-19da-4b0f-a6a3-59acdc70914d`。服務訊息：Your request was rejected by the safety system. If you believe this is an error, contact us at help.openai.com and include the request ID 15d78c48-19da-4b0f-a6a3-59acdc70914d. 未改寫規避、未重試或更換工具。

重新生成（2026-10-13）：依使用者「再生第五圖」以相同三張參考圖、相同原 prompt 重新呼叫一次，成功產出 `shot_2.1.5_short_v1`，image，scene_id=`shot_2.1.5`；[成品](../assets/images/shot_2.1.5_short_v1.png)。工具 `image_gen`／OpenAI，模型與費用未回報。
實際 prompt 與上次嘗試完全相同：圖片角色說明＋共用短指令＋本鏡完整短指令，沒有改寫或更換工具；前次錯誤保留。
檢視：George 單人頭肩、溫和微笑與嘴唇微張成立，手部／杯子在畫外；未見明顯側身回頭。頭部較 blocks 放大、頭頂留白較少，背景主要窗牆關係保留，細節非完全一致。待使用者檢視，未追加生成。

## 2.1.6｜ESG 概念轉折｜s09_table_insert／50mm

- 圖 1 [blocks](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/renders/blocks_blender_s09_table_insert.png)
- 圖 2 [背景](D:/kj-openMontage/projects/course-51-esg/references/scenes/coffee_shop/cameras/empty_banana_s09_table_insert.png)
- 圖 3 [char_esg_george.png](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_george.png)
- 圖 4 [char_esg_amy.jpeg](D:/kj-openMontage/projects/course-51-esg/clp/char_esg_amy.jpeg)
- 圖 5 [prop_coffee_set.png](D:/kj-openMontage/projects/course-51-esg/clp/prop_coffee_set.png)

短指令：維持桌面斜俯拍：兩人的局部前臂與手自然停在桌邊，兩只咖啡杯均在各自杯碟上，保留背景的白色金色金屬蓋罐。只見 blocks 所示局部身體，不出現臉；George 為畫外音。E／S／G 留待後製，這張不生成字卡。咖啡組 CLP 僅取杯碟，不採用木蓋罐。

生成紀錄（2026-10-13）：`shot_2.1.6_short_v1`，image，scene_id=`shot_2.1.6`；[成品](../assets/images/shot_2.1.6_short_v1.png)。工具 `image_gen`，供應商 OpenAI，模型與費用未回報；新生成素材，沿用本鏡五張參考圖。
實際 prompt：先加「圖 1 是 blocks，圖 2 是同鏡空景，圖 3 是 George CLP，圖 4 是 Amy CLP，圖 5 是咖啡組 CLP。」，再接本檔共用短指令及 2.1.6 短指令。
檢視：桌面斜俯拍、兩組杯碟、白色金色金屬蓋罐、角色局部衣袖與無臉／無字卡成立；兩人各一手改成握杯柄，偏離原 blocks 手位與自然停在桌邊的指定動作。Amy 杯中沿用空景黑咖啡，與前鏡拿鐵不連戲；未判定整體通過，未追加生成。
