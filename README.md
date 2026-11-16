# Study Journal｜我的大學學習知識庫

本專案為生成式 AI 第九週作業，參考 LLM Wiki 的原始資料→整理筆記→索引與網頁方式。首批內容取自使用者提供的普通物理學及統計學講義，共五篇筆記。原始 35 份 PDF 保留於使用者自己的資料夾，不隨公開專案發布；其中一份歸類在統計學的數論作業標為待確認。

## 使用方式
直接開啟 `index.html` 即可瀏覽，也可部署到 GitHub Pages。不需要安裝前端套件。若新增筆記，需要 Python 3：先讀 `AGENTS.md`，依 `templates/note-template.md` 寫 Markdown、更新 `wiki/catalog.json`，再執行 `python scripts/build.py`。生成器僅用標準函式庫。

## 專案架構
- AGENTS.md：AI 員工手冊
- wiki/：筆記 Markdown、來源清冊、索引與 catalog
- templates/：筆記模板
- scripts/build.py：靜態網站生成程式
- index.html、notes/、assets/：可部署的網頁、樣式及搜尋功能

## 部署
建立公開 GitHub repository，將本專案內容放在根目錄（index.html 直接位於根目錄）。Settings → Pages → Deploy from a branch → main → /(root) → Save。完成部署後以 GitHub 提供的網址測試網站。

## 擴充示範
新增「常態分配」筆記：使用講義、複製模板到 `wiki/statistics/normal-distribution.md`、更新 catalog，再執行生成器。首頁、索引及筆記網頁將自動更新，不必重新設計網頁。
