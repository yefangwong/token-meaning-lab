# token-meaning-lab

**LLM 語義空間「相似性 vs 連結性」混沌實驗室**

---

## 🎯 核心研究問題

> BPE + Self-Supervised Next Token Prediction 能同時學到語義「相似性（Similarity）」與「連結性（Relatedness）」，但無法在向量空間中區分兩者。

## 🧪 實驗設計

請見 [design/hypothesis.md](design/hypothesis.md) 與 [design/stimulus_set.csv](design/stimulus_set.csv)。

## 🚀 快速開始

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動 Jupyter
jupyter notebook
```

## 📓 Notebook 執行順序

1. `notebooks/01_embedding_cosine.ipynb` — LLM cosine similarity 量測
2. `notebooks/02_hownet_similarity.ipynb` — HowNet 義原相似度計算
3. `notebooks/03_analysis_and_plot.ipynb` — 四象限散布圖 + 統計分析
4. `notebooks/04_run_retrofitting.ipynb` — Faruqui Retrofitting 神經符號校準實驗

## 🔗 關聯知識庫

- [HowNet 計算語義學](../knowledge/facts/hownet_computation_of_meaning.md)
- [Outlines 受控生成](../knowledge/facts/willard_louf_2023_efficient_guided_generation_outlines.md)
- [神經符號知識編譯合成草稿](../knowledge/AI_Raw/drafts/neurosymbolic_knowledge_compilation_and_hownet.md)
