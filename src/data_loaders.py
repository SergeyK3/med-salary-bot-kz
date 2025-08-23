# src/data_loaders.py
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
_CACHE: dict[str, pd.DataFrame] = {}

def _abs(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else (ROOT / p)

def _read_csv_resilient(p: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(p, encoding="utf-8-sig")  # обычный CSV (запятая, точка)
    except Exception:
        try:
            # CSV с ; и десятичной запятой
            return pd.read_csv(p, sep=";", decimal=",", encoding="utf-8-sig")
        except Exception:
            # авто-определение
            return pd.read_csv(p, sep=None, engine="python", encoding="utf-8-sig")

def _load_csv(key: str, path: str | Path) -> pd.DataFrame:
    p = _abs(path)
    if key not in _CACHE:
        _CACHE[key] = _read_csv_resilient(p)
    return _CACHE[key]

def ets_df(path: str | Path = "data/ets_coefficients.csv") -> pd.DataFrame:
    return _load_csv("ets", path)

def zones_df(path: str | Path = "data/zones.csv") -> pd.DataFrame:
    df = _load_csv("zones", path).copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"calcbase": "calc_base", "base": "calc_base", "val": "value"})
    # приведение типов/формата
    df["calc_base"] = df["calc_base"].astype(str).str.strip().str.upper()
    df["value"] = (
        df["value"].astype(str)
        .str.replace("\u00A0", "", regex=False)  # NBSP
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["value"] = pd.to_numeric(df["value"], errors="raise")
    required = {"code", "name", "calc_base", "value"}
    if not required.issubset(df.columns):
        raise ValueError(f"zones.csv must have columns {sorted(required)}; got {list(df.columns)}")
    return df

def risk_df(path: str | Path = "data/risk_allowances.csv") -> pd.DataFrame:
    return _load_csv("risk", path)
