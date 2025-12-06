# data_preprocessing.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_jsonl_to_df(jsonl_path: str) -> pd.DataFrame:
    import json
    rows = []
    with open(jsonl_path, "r", encoding="utf8") as f:
        for line in f:
            rows.append(json.loads(line))
    # Flatten a few fields
    flat = []
    for r in rows:
        s = r.get("structured") or {}
        summary = r.get("summary") or {}
        # create feature row
        fr = {
            "claim_id": r.get("claim_id"),
            "hospital": s.get("hospital"),
            "claim_amount": s.get("claim_amount") or 0.0,
            "previous_claim_count": s.get("previous_claim_count") or 0,
            "prev_risk_flags": s.get("previous_risk_flags") or 0,
            "billing_total": s.get("billing_total") or 0.0,
            "behavior_anomaly_score": s.get("behavior_anomaly_score") or 0.0,
            "risk_score": summary.get("risk_score") or 0.0,
            "fraud_label": r.get("fraud_label") or 0
        }
        flat.append(fr)
    return pd.DataFrame(flat)

def featurize(df: pd.DataFrame) -> pd.DataFrame:
    # Simple features: ratios, logs, encode hospital domain via frequency
    df = df.copy()
    df["claim_amount_log"] = np.log1p(df["claim_amount"])
    df["billing_ratio"] = df["billing_total"] / (df["claim_amount"] + 1e-6)
    # hospital frequency encoding
    freq = df["hospital"].fillna("UNK").value_counts().to_dict()
    df["hospital_freq"] = df["hospital"].fillna("UNK").map(freq)
    # fill nan
    df = df.fillna(0)
    return df

def train_test_split_features(df, target_col="fraud_label", test_size=0.2, random_state=42):
    X = df.drop(columns=[target_col, "claim_id", "hospital"])
    y = df[target_col].astype(int)
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
