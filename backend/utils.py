# utils.py
import pandas as pd
from sklearn.metrics import confusion_matrix

def compute_basic_fairness_metrics(df, pred_col="pred", label_col="label", group_col="employer"):
    # For each group compute FPR/FNR
    res = {}
    groups = df[group_col].unique()
    for g in groups:
        sub = df[df[group_col]==g]
        if len(sub)==0: continue
        tn, fp, fn, tp = confusion_matrix(sub[label_col], sub[pred_col], labels=[0,1]).ravel()
        fpr = fp / (fp + tn + 1e-9)
        fnr = fn / (fn + tp + 1e-9)
        res[g] = {"fpr": fpr, "fnr": fnr, "support": len(sub)}
    return res
