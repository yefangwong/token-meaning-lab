"""
discovery_tree.py — Dream-RSI 發現樹核心模組

靈感來源: Google DeepMind《Dream-RSI: Recursive Self-Improvement through Evolving Worlds》
          Tong Zheng et al., arXiv:2609.14858 (2026-09)

核心思想：
  每一次實驗跑完，不只留 CSV 結果，而是留下一個「發現節點（Discovery Node）」：
  - 完整的環境快照（模型版本、詞對版本、亂數種子）
  - 原始分數（可重播）
  - 統計結論（可比較）
  - 人類可讀的裁決書

  未來實驗可以在歷史節點上「做夢」：
  - What-if：「如果當時用 M3E 模型，結果會如何？」
  - 單調保證：新實驗結果必須 >= 歷史最佳節點，否則標記為 regression
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
import pandas as pd


TREE_DIR = Path(__file__).parent.parent / "discovery_tree"
TREE_INDEX = TREE_DIR / "tree_index.json"


@dataclass
class ExperimentConfig:
    """實驗配置快照 — 這是每個節點的 DNA"""
    embedding_model: str
    stimulus_version: str  # stimulus_set.csv 的 git hash 或版本號
    random_seed: int
    hownet_version: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))

    def node_id(self) -> str:
        """用配置內容生成唯一節點 ID"""
        content = f"{self.embedding_model}_{self.stimulus_version}_{self.random_seed}_{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


@dataclass
class StatResult:
    """統計結論快照"""
    q1_llm_mean: float
    q2_llm_mean: float
    q1_hownet_mean: float
    q2_hownet_mean: float
    llm_t_stat: float
    llm_p_value: float
    hownet_t_stat: float
    hownet_p_value: float
    h1_supported: bool  # True if p_llm > 0.05 AND p_hownet < 0.05


@dataclass
class DiscoveryNode:
    """
    發現樹的一個節點 — 對應 Dream-RSI 中的一次真實環境探索快照

    Dream-RSI 原文：
    「累積的發現歷史作為實現搜尋空間之重放模擬器」
    我們的版本：累積的實驗歷史作為可重放的知識節點
    """
    config: ExperimentConfig
    stats: StatResult
    verdict: str  # "H1_SUPPORTED" | "H1_REJECTED" | "INCONCLUSIVE"
    node_path: Optional[str] = None


def save_node(
    config: ExperimentConfig,
    scores_df: pd.DataFrame,
    stats: StatResult,
) -> DiscoveryNode:
    """
    將一次完整實驗存入發現樹。

    Returns:
        DiscoveryNode: 存入的節點物件
    """
    node_id = config.node_id()
    node_dir = TREE_DIR / f"run_{config.timestamp}_{node_id}"
    node_dir.mkdir(parents=True, exist_ok=True)

    # 1. 儲存配置快照
    with open(node_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(asdict(config), f, ensure_ascii=False, indent=2)

    # 2. 儲存原始分數（高保真軌跡，不壓縮）
    scores_df.to_csv(node_dir / "scores.csv", index=False)

    # 3. 儲存統計結論
    with open(node_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(asdict(stats), f, ensure_ascii=False, indent=2)

    # 4. 生成人類可讀裁決書
    if stats.h1_supported:
        verdict = "H1_SUPPORTED"
        verdict_text = "✅ 強力支持 H1：LLM Embedding 混淆相似性與連結性；HowNet 義原體系正確區分兩者。"
    elif not stats.h1_supported and stats.llm_p_value < 0.05:
        verdict = "H1_REJECTED"
        verdict_text = "❌ H1 被拒絕：LLM 在此配置下能區分兩類詞對。需重新審視刺激組設計。"
    else:
        verdict = "INCONCLUSIVE"
        verdict_text = "⚠️ 結果不確定：請增加刺激詞對數量或調整模型。"

    verdict_md = f"""# 實驗裁決書 — {config.timestamp}

## 配置
- 模型: `{config.embedding_model}`
- 刺激詞對版本: `{config.stimulus_version}`
- 隨機種子: `{config.random_seed}`

## 統計結果

| 測量工具 | Q1 均值 | Q2 均值 | t 統計量 | p 值 | 結論 |
|:---|:---|:---|:---|:---|:---|
| LLM Cosine | {stats.q1_llm_mean:.4f} | {stats.q2_llm_mean:.4f} | {stats.llm_t_stat:.4f} | {stats.llm_p_value:.4f} | {"無法區分 ✓" if stats.llm_p_value > 0.05 else "能區分 ✗"} |
| HowNet | {stats.q1_hownet_mean:.4f} | {stats.q2_hownet_mean:.4f} | {stats.hownet_t_stat:.4f} | {stats.hownet_p_value:.4f} | {"正確區分 ✓" if stats.hownet_p_value < 0.05 else "未能區分 ✗"} |

## 最終裁決

**{verdict}**

{verdict_text}

---
*由 token-meaning-lab Dream-RSI Discovery Tree 自動生成*
*節點 ID: {node_id}*
"""

    with open(node_dir / "verdict.md", "w", encoding="utf-8") as f:
        f.write(verdict_md)

    # 5. 更新樹索引（tree_index.json）
    node = DiscoveryNode(
        config=config,
        stats=stats,
        verdict=verdict,
        node_path=str(node_dir),
    )
    _update_index(node, node_id)

    print(f"✅ 發現節點已儲存: {node_dir.name}")
    print(f"   裁決: {verdict}")
    return node


def _update_index(node: DiscoveryNode, node_id: str):
    """更新全局樹索引"""
    if TREE_INDEX.exists():
        with open(TREE_INDEX, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {"nodes": [], "best_node_id": None, "created_at": datetime.now().isoformat()}

    node_summary = {
        "node_id": node_id,
        "timestamp": node.config.timestamp,
        "model": node.config.embedding_model,
        "verdict": node.verdict,
        "llm_p_value": node.stats.llm_p_value,
        "hownet_p_value": node.stats.hownet_p_value,
        "h1_supported": node.stats.h1_supported,
        "path": node.node_path,
    }
    index["nodes"].append(node_summary)

    # 單調保證：更新最佳節點（以 LLM p_value 最大為準，代表 LLM 最無法區分——最強混沌證據）
    best = max(index["nodes"], key=lambda n: n["llm_p_value"])
    index["best_node_id"] = best["node_id"]
    index["updated_at"] = datetime.now().isoformat()

    with open(TREE_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def load_tree() -> list[dict]:
    """載入發現樹所有節點摘要"""
    if not TREE_INDEX.exists():
        return []
    with open(TREE_INDEX, "r", encoding="utf-8") as f:
        return json.load(f)["nodes"]


def replay_node(node_id_prefix: str) -> pd.DataFrame:
    """
    重放歷史節點的原始分數——Dream-RSI「做夢」的基礎操作

    Args:
        node_id_prefix: 節點 ID 前綴（前 6 碼即可）

    Returns:
        歷史實驗的原始分數 DataFrame
    """
    for node_dir in TREE_DIR.iterdir():
        if node_dir.is_dir() and node_id_prefix in node_dir.name:
            scores_path = node_dir / "scores.csv"
            if scores_path.exists():
                print(f"🔄 重放節點: {node_dir.name}")
                return pd.read_csv(scores_path)
    raise FileNotFoundError(f"找不到節點: {node_id_prefix}")


def compare_nodes(node_id_a: str, node_id_b: str) -> dict:
    """
    比較兩個歷史節點——Dream-RSI What-if 推演的核心

    Returns:
        dict 包含兩節點的統計對比
    """
    nodes = {n["node_id"]: n for n in load_tree()}
    a = nodes.get(node_id_a) or next((n for n in nodes.values() if n["node_id"].startswith(node_id_a)), None)
    b = nodes.get(node_id_b) or next((n for n in nodes.values() if n["node_id"].startswith(node_id_b)), None)

    if not a or not b:
        raise ValueError(f"找不到節點 {node_id_a} 或 {node_id_b}")

    return {
        "node_a": a,
        "node_b": b,
        "regression": a["llm_p_value"] > b["llm_p_value"],  # True = B 比 A 更差（p 更小，LLM 更能區分）
        "improvement": b["llm_p_value"] > a["llm_p_value"],  # True = B 比 A 更好
    }
