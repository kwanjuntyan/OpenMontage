# OpenMontage（lean 分支）

## 開發原則 — 優先於本 repo 其他所有規則

這是**兩人公司內部自用**的 script-to-video 工具。目標：**能跑、好改、好懂**。

1. **使用者可信任。** 不做身分驗證、權限、多租戶、稽核、輸入消毒。
2. **出錯就直接丟例外（fail loud）。** 不加層層檢查、fallback、重試包裝、防禦性驗證。
3. **最小改動。** 每個任務預設上限：3 個檔案、150 行**新增或修改**。超過要先說明原因並問我。**刪除程式碼、原封不動搬移既有檔案不計入。**
4. **不新增治理機制。** 不寫新的 schema、contract、gate、checkpoint、approval、governance 測試、git hook、CI 閘門，除非使用者明確要求。
5. **重複第 3 次才抽象化。** 寧可複製兩次，也不要提早設計 interface 或框架。
6. **檔案保持短小。** 單一檔案超過 400 行要先問。
7. **測試只要 smoke test。** 每條 pipeline 一個：跑完能產出 mp4 就算通過。不追求覆蓋率。
8. **驗證要快。** 只跑跟這次改動有關的測試，不要每次跑全套。測試暫存一律放 `.tmp/`，不要另外建立新的暫存資料夾或 worktree。
9. **不確定要不要加某個機制時，答案是「不加」。** 在回覆最後列出「我刻意沒做的事」，讓使用者決定。
10. **衝突時以本原則為準。** `AGENT_GUIDE.md` 和各 skill 的影片製作流程照常使用；但寫程式時，若它們的要求與本原則衝突，依本原則。

## 協作方式

- **用繁體中文，簡短回覆。** 不寫長篇計畫文件；動手前用一張「檔案／改什麼／約幾行」小表說明，使用者同意就做。
- **Google 模型固定預設 Vertex AI＋服務帳戶 JSON**（`GOOGLE_APPLICATION_CREDENTIALS`）；不再詢問認證方式，不自動改用 AI Studio API key 或第三方代管。憑證／模型不可用直接報錯。
- **OM 統一使用本專案 `.venv/Scripts/python.exe`**，依賴版本以 OM 需求為準（Gemini 3.8 TTS 需要 `google-genai >= 2.25.0`）；不為未使用的 `google-cloud-aiplatform`／`langchain-google-genai` 降版或維持相容性。
- Omni 預設 `gemini-omni-1.1-flash-preview`，Gemini TTS 預設 `gemini-3.8-flash-tts`，兩者使用 `global`。舊 Cloud TTS 仍是不同 API，但同樣用 JSON 認證。
- **需要使用者決定時**：編號列出選項，標出建議與預設，讓使用者能用「1① 2 可以」一行回覆。一次問完，不要一題一題來回。
- **先看再改。** 改之前先讀相關程式碼確認現況（不要憑記憶或推測 API）；改完立刻用 `.tmp/` 的小腳本或相關測試驗證，再回報。
- **錯誤先找根因再修**，修完記到 `docs/kj-lean-status.md` 的「踩過的坑」。
- **花錢前必報**：工具、供應商、模型、原因、預估費用。使用者選過的供應商可直接用，但換模型要先問。
- **commit／push**：使用者確認後再做；push 到 `team-fork lean`。`projects/` 測試資料預設不 commit。
- **不要動** `AGENT_GUIDE.md`（保持可和 upstream 合併）、其他 `codex/*` 分支與 worktree。
- 每次回覆結尾列「我刻意沒做的事」。

## 現況與交接

目前進度、已搬回的功能、踩過的坑、下一步：見 [`docs/kj-lean-status.md`](docs/kj-lean-status.md)。**開始工作前先讀。** 完成一段工作後更新它（保持 100 行內）。

## 影片製作操作手冊

**接著請閱讀 [`AGENT_GUIDE.md`](AGENT_GUIDE.md)**（原作者的操作手冊，含 pipeline 路由規則），再處理使用者的請求。
架構與重要檔案見 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)。
