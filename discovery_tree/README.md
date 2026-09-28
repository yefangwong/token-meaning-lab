# Discovery Tree — 發現樹

> **靈感來源**：Google DeepMind《Dream-RSI: Recursive Self-Improvement through Evolving Worlds》
> Tong Zheng et al., arXiv:2609.14858 (2026-09)

---

## 這不是普通的 logs 目錄

普通的 log：`[INFO] Experiment ran. p=0.032. Done.`  
→ 資訊被壓縮成幾個數字，上下文永遠消失。

**發現樹（Discovery Tree）**：每個節點保留完整的高保真快照：
- 實驗配置（模型版本、詞對版本、亂數種子）
- 所有 20 個詞對的原始分數（可重播！）
- 完整統計結論
- 人類可讀裁決書

→ 未來任何時候都能「回到」這個歷史節點，進行 What-if 推演。

---

## Dream-RSI 概念對應

| Dream-RSI 原文概念 | 在本實驗室的對應 |
|:---|:---|
| 真實環境探索 → 記錄進發現樹 | 跑完 Notebook → `save_node()` 自動存入此目錄 |
| 重放模擬器（Replay Simulator） | `replay_node(node_id)` 重載歷史原始分數，不需重跑模型 |
| 做夢（Dreaming）= 在歷史樹上 what-if 推演 | `compare_nodes(id_a, id_b)` 比較不同配置的結果 |
| 數學保證單調不退步 | `tree_index.json` 自動追蹤 `best_node_id`，新實驗若退步則標記 regression |

---

## 目錄結構

每次實驗在此目錄下建立一個子目錄：

```
discovery_tree/
├── README.md            ← 本文件
├── tree_index.json      ← 全部節點索引（自動維護）
└── run_20260926_120000_abc123def456/
    ├── config.json      ← 模型版本、詞對版本、亂數種子
    ├── scores.csv       ← 所有 20 詞對的原始分數（高保真）
    ├── stats.json       ← t-test 統計結論
    └── verdict.md       ← 人類可讀裁決書
```

---

## 人類審計原則（對應 Dream-RSI「顛覆常識」發現）

> Dream-RSI 最反直覺的發現：**高層經驗總結（Lossy Compression）反而拖後腿。**
> 未來 Agent 需要的是「高保真的行動軌跡快照」，而非抽象格言。

本目錄的設計完全體現此原則：
- **禁止**：在此目錄下寫 `lessons_learned.txt`（這是有損壓縮！）
- **鼓勵**：在 Notebook 的 Markdown Cell 中記錄每次實驗的完整觀察與推理過程
- **必須**：每次跑完實驗，呼叫 `src/discovery_tree.py` 的 `save_node()` 自動建立節點
