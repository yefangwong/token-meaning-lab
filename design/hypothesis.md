# 實驗假說（Pre-Registered Hypothesis）

**Pre-Registration 日期**: 2026-09-26  
**狀態**: LOCKED — 鎖定後不得修改

---

## 研究背景

HowNet（知網）明確區分兩種語義關係：
- **相似性（Similarity）**：基於義原（Sememe）交集，度量概念間的本體類別重疊程度。
- **連結性（Relatedness）**：基於語義角色網路（ARN/CRN），度量概念間的事件結構關聯程度。

現代 LLM 使用 BPE 分詞後進行 Self-Supervised Next Token Prediction，其 Embedding 向量透過分佈假說（Distributional Hypothesis）同時習得兩者，但在同一個幾何空間中無法拆分。

---

## 虛無假說 H₀

> LLM Embedding 的餘弦相似度（Cosine Similarity）能**有效區分**語義相似性與語義連結性。
> 
> 預測：「高相似、低連結」詞對的 cosine score ≫ 「低相似、高連結」詞對的 cosine score。

## 對立假說 H₁（我們預期成立）

> LLM Embedding 的餘弦相似度**無法區分**語義相似性與語義連結性。
> 
> 預測：「低相似、高連結（Q2）」詞對的 cosine score ≈「高相似、低連結（Q1）」詞對的 cosine score，兩者無顯著差異。

---

## 關鍵評量指標

1. **Q1 vs Q2 cosine score 差異**：若 H₁ 成立，兩者均值應無統計顯著差異（t-test p > 0.05）。
2. **Pearson r（LLM cosine vs. Human Similarity Judgment）**：LLM 分數與純相似性人工評分的相關係數，預期 < 與混合連結性評分的相關係數。
3. **SimLex-999 效應複製**：LLM 在 SimLex-999（純相似性）上的表現，應顯著低於在 WordSim-353（混合連結性）上的表現。

---

## 實驗操控變數（Independent Variables）

| 變數 | 水平 |
|:---|:---|
| 語義關係類型 | Q1（高相似低連結）/ Q2（低相似高連結）/ Q3（高相似高連結）/ Q4（低相似低連結） |
| 測量工具 | LLM Cosine Similarity / HowNet Similarity Score |

## 依變數（Dependent Variable）

- 語義相關度分數（0–1）

## 控制變數

- 詞對頻率：選取訓練語料中出現頻率相近的詞對
- 字符長度：避免極端短詞（單字）或極端長詞（>4字）的干擾
- 領域：主要選用醫療、自然、音樂、日常生活跨領域詞彙

---

## 預期結果圖示

```
        LLM Cosine Score
   1.0 │
       │   ●Q1           ●Q2    ← Q2 不當地高！這就是混沌的證據
   0.7 │
       │
   0.4 │                              ●Q4
       │
   0.1 │
       └──────────────────────────────────
         高相似低連結  低相似高連結  低相似低連結

        HowNet Similarity Score（預期正確區分）
   1.0 │   ●Q1
       │
   0.5 │
       │                              ●Q4
   0.1 │              ●Q2  ← Q2 應該要低！HowNet 正確！
       └──────────────────────────────────
         高相似低連結  低相似高連結  低相似低連結
```
