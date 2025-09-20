from __future__ import annotations
from .data_io import read_zones, read_ets

from pathlib import Path
from typing import Iterable
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]  # корень репо: …/med-salary-bot-kz


def _read_csv_robust(path: Path, expected_cols: Iterable[str]) -> pd.DataFrame:
    """
    Пытается прочитать CSV разными способами:
    - разделитель: ',' или ';' или таб
    - десятичный: '.' или ','
    Возвращает DataFrame, в котором есть все expected_cols.
    """
    expected = set(expected_cols)
    for sep in (",", ";", "\t"):
        for dec in (".", ","):
            try:
                df = pd.read_csv(path, sep=sep, decimal=dec)
            except Exception:
                continue
            if expected.issubset(df.columns):
                return df
    raise ValueError(f"Не удалось прочитать {path} с колонками {expected_cols}")


# ---------- settings.yml ----------
def load_settings(path: str | Path | None = None) -> dict:
    if path is None:
        path = ROOT / "data" / "settings.yml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_zones(path: str | Path | None = None, table: str = "zones") -> list[dict]:
    import sqlite3
    if path is None:
        path = ROOT / "data" / "zones.sqlite"
    with sqlite3.connect(path) as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df["calc_base"] = df["calc_base"].astype(str).str.strip().str.upper()
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0.0)
    return df.to_dict(orient="records")


def load_risk_allowances(path: str | Path | None = None, table: str = "risk_allowances") -> list[dict]:
    import sqlite3
    if path is None:
        path = ROOT / "data" / "risk_allowances.sqlite"
    with sqlite3.connect(path) as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df["calc_base"] = df["calc_base"].astype(str).str.strip().str.upper()
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0.0)
    return df.to_dict(orient="records")

# Совместимость со старым кодом: таблица ЕТС
def load_ets_table(path: str | Path | None = None):
    # используем уже надёжный ридер
    return read_ets(path)
