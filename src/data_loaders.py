# src/data_loaders.py
from __future__ import annotations
from pathlib import Path
import pandas as pd

# Корень репозитория: <root>/src/data_loaders.py → <root>
ROOT = Path(__file__).resolve().parents[1]
_CACHE: dict[str, pd.DataFrame] = {}

def _abs(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else (ROOT / p)

def _load_csv(key: str, path: str | Path) -> pd.DataFrame:
    p = _abs(path)
    if key not in _CACHE:
        _CACHE[key] = pd.read_csv(p)
    return _CACHE[key]

def ets_df(path: str | Path = "data/ets_coefficients.csv") -> pd.DataFrame:
    return _load_csv("ets", path)

def zones_df(path: str | Path = "data/zones.csv") -> pd.DataFrame:
    return _load_csv("zones", path)

def risk_df(path: str | Path = "data/risk_allowances.csv") -> pd.DataFrame:
    return _load_csv("risk", path)
