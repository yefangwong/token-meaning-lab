# CORNELIUS.md — token-meaning-lab 開發規範

> **Cornelius** 是本實驗室的開發守護代理。本文件定義 Antigravity IDE 在此 Jupyter 實驗室中的開發行為規範。

---

## 🧪 專案定位

**token-meaning-lab** 是一個語義空間科學實驗室，目的是用可執行的 Python 實驗，驗證：

> *LLM Embedding（BPE + Next Token Prediction）無法區分語義「相似性（Similarity）」與「連結性（Relatedness）」，而 HowNet 義原體系能精確拆分兩者。*

---

## 📏 開發規範

### 1. 語言規範
- **Notebook 說明文字（Markdown Cell）**：繁體中文
- **程式碼變數與函數命名**：英文 snake_case
- **提交訊息（git commit）**：英文，遵從 Conventional Commits

### 2. 科學誠信（Scientific Integrity）
- **可再現性第一（Reproducibility First）**：所有實驗必須設定 `random_seed`，結果可由第三方完整重現。
- **禁止 P-hacking**：嚴禁在跑出結果後回頭調整刺激詞組選取以符合預期。詞對組必須在跑模型**之前**鎖定並記錄在 `design/stimulus_set.csv`。
- **負面結果記錄**：若實驗結果拒絕 H₁，必須誠實記錄並分析原因，不得隱藏。
- **Fidelity First**：所有數字引用必須附來源（embedding 模型名稱 + 版本 + huggingface model ID）。

### 3. 目錄結構規範
```
token-meaning-lab/
├── AGENTS.md             ← 複製自 Knowledge base，Antigravity 治理規範
├── CORNELIUS.md          ← 本文件，開發規範
├── README.md             ← 實驗概述與執行指引
├── design/               ← 實驗設計（在跑模型前鎖定）
│   ├── hypothesis.md     ← 假說陳述
│   └── stimulus_set.csv  ← 刺激詞對組（Pre-registered）
├── notebooks/            ← Jupyter Notebooks
│   ├── 01_embedding_cosine.ipynb   ← LLM 向量空間量測
│   ├── 02_hownet_similarity.ipynb  ← HowNet 義原相似度計算
│   └── 03_analysis_and_plot.ipynb  ← 統計分析與視覺化
├── src/                  ← 可重用 Python 模組
│   ├── embeddings.py     ← Embedding 計算工具
│   ├── hownet_utils.py   ← HowNet API 查詢工具
│   └── stats.py          ← 統計分析工具（Pearson r, Spearman rho）
├── data/
│   └── results/          ← 實驗結果（自動生成，不手動編輯）
├── requirements.txt
└── pyproject.toml
```

### 4. Pre-Registration 原則
> 在運行任何 Embedding 計算前，design/stimulus_set.csv 必須先被 commit 並標記 [PRE-REGISTERED]。
> 這是確保實驗不被「後驗調整」的核心機制。

---

## 🎯 第一個里程碑（Milestone 1）

- [ ] 完成刺激詞對組 pre-registration（design/stimulus_set.csv）
- [ ] 完成 01_embedding_cosine.ipynb（LLM cosine similarity 量測）
- [ ] 完成 02_hownet_similarity.ipynb（HowNet 分數量測）
- [ ] 完成 03_analysis_and_plot.ipynb（四象限散布圖 + Pearson r）
- [ ] 生成實驗報告，回饋至 Knowledge Base 知識庫

---

*規範版本 v1.0 — 2026-09-26*
*由 Antigravity IDE 與藝芳共同制定*
