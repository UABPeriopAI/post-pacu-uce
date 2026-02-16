from typing import Any, Dict, Iterable, List, Mapping

import pandas as pd


def _normalize_input(X: Any) -> pd.DataFrame:
    if isinstance(X, pd.DataFrame):
        return X
    if isinstance(X, Mapping):
        return pd.DataFrame([X])
    if isinstance(X, Iterable):
        return pd.DataFrame(X)
    raise TypeError("X must be a pandas.DataFrame, mapping, or iterable of mappings")


def predict(X: Any, artifacts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate risk predictions for new observations.

    Args:
        X: Input features as a pandas DataFrame, a mapping, or an iterable of mappings.
        artifacts: Dictionary containing a trained scorecard model under "model".

    Returns:
        List of records with input features and predicted risk scores.
    """
    model = artifacts.get("model")
    if model is None:
        raise ValueError("artifacts must include a 'model' entry")

    X_df = _normalize_input(X)
    proba = model.predict_proba(X_df)[:, 1]

    records: List[Dict[str, Any]] = []
    for row, score in zip(X_df.to_dict(orient="records"), proba):
        record = dict(row)
        record["risk_score"] = float(score)
        records.append(record)
    return records
