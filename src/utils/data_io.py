from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def _read_robust(path: Path, expected_cols: set[str]) -> pd.DataFrame:
    # пробуем разные пары разделителей/десятичных
    for sep in (",", ";", "\t"):
        for dec in (".", ","):
            try:
                df = pd.read_csv(path, sep=sep, decimal=dec)
                if expected_cols.issubset(set(df.columns)):
                    return df
            except Exception:
                continue
    raise ValueError(f"Не удалось прочитать {path} с ожидаемыми колонками {expected_cols}")

def read_ets(path: str | Path | None = None, table: str = "ets_coefficients") -> pd.DataFrame:
    import sqlite3
    if path is None:
        path = ROOT / "data" / "ets_coefficients.sqlite"
    with sqlite3.connect(path) as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        for col in ["band_from", "band_to", "coeff"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        # Привести category к int для корректной фильтрации
        if "category" in df.columns:
            df["category"] = pd.to_numeric(df["category"], errors="coerce", downcast="integer")
        # Очистить band_label от пробелов
        if "band_label" in df.columns:
            df["band_label"] = df["band_label"].astype(str).str.strip()
        return df

def read_zones(path: str | Path | None = None, table: str = "zones") -> pd.DataFrame:
    import sqlite3
    if path is None:
        path = ROOT / "data" / "zones.sqlite"
    with sqlite3.connect(path) as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df
