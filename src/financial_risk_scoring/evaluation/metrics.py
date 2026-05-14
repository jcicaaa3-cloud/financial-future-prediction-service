from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, brier_score_loss, f1_score, roc_auc_score


def classification_metrics(y_true, probability, *, threshold: float = 0.5) -> dict[str, float | None]:
    y_true_arr = np.asarray(y_true)
    prob_arr = np.asarray(probability)
    pred_arr = (prob_arr >= threshold).astype(int)
    metrics: dict[str, float | None] = {
        "positive_rate": float(y_true_arr.mean()) if len(y_true_arr) else None,
        "f1_at_0_5": float(f1_score(y_true_arr, pred_arr, zero_division=0)) if len(y_true_arr) else None,
        "brier": float(brier_score_loss(y_true_arr, prob_arr)) if len(np.unique(y_true_arr)) > 1 else None,
    }
    if len(np.unique(y_true_arr)) > 1:
        metrics["roc_auc"] = float(roc_auc_score(y_true_arr, prob_arr))
        metrics["average_precision"] = float(average_precision_score(y_true_arr, prob_arr))
    else:
        metrics["roc_auc"] = None
        metrics["average_precision"] = None
    return metrics
