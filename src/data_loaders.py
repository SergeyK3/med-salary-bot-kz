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

def ets_df(path: str | Path = "data/ets_coefficients.sqlite", table: str = "ets_coefficients") -> pd.DataFrame:
    import sqlite3
    p = _abs(path)
    with sqlite3.connect(p) as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    # Приведение типов для числовых столбцов
    for col in ["band_from", "band_to", "coeff"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # Явно привести band_from и band_to к float
    if "band_from" in df.columns:
        df["band_from"] = df["band_from"].astype(float)
    if "band_to" in df.columns:
        df["band_to"] = df["band_to"].astype(float)
    # Очистить band_label от пробелов
    if "band_label" in df.columns:
        df["band_label"] = df["band_label"].astype(str).str.strip()
    # Привести category к int для совместимости с тестами
    if "category" in df.columns:
        df["category"] = pd.to_numeric(df["category"], errors="coerce", downcast="integer")
    # Отладочный вывод типов и примеров значений
    print("band_from dtype:", df["band_from"].dtype)
    print("band_to dtype:", df["band_to"].dtype)
    print("band_from sample:", df["band_from"].head(5).tolist())
    print("band_to sample:", df["band_to"].head(5).tolist())
    return df

def zones_df(path: str | Path = "data/zones.sqlite", table: str = "zones") -> pd.DataFrame:
    import sqlite3
    p = _abs(path)
    with sqlite3.connect(p) as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"calcbase": "calc_base", "base": "calc_base", "val": "value"})
    df["calc_base"] = df["calc_base"].astype(str).str.strip().str.upper()
    if "value" in df.columns:
        # Заменяем запятые на точки и приводим к float
        df["value"] = df["value"].astype(str).str.replace(",", ".").astype(float)
    required = {"code", "name", "calc_base", "value"}
    if not required.issubset(df.columns):
        raise ValueError(f"zones.sqlite must have columns {sorted(required)}; got {list(df.columns)}")
    return df

def risk_df(path: str | Path = "data/risk_allowances.sqlite", table: str = "risk_allowances") -> pd.DataFrame:
    import sqlite3
    p = _abs(path)
    with sqlite3.connect(p) as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    # Приведение типов для числовых столбцов
    for col in ["value"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df
