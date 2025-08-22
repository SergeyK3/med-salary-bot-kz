from __future__ import annotations
from pathlib import Path
import csv, yaml

ROOT = Path(__file__).resolve().parents[2]   # корень репозитория
DATA = ROOT / "data"

def _read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def load_settings() -> dict:
    with (DATA / "settings.yml").open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_ets_table() -> list[dict]:
    rows = _read_csv(DATA / "ets_coefficients.csv")
    # нормализуем типы
    for r in rows:
        r["category"] = int(r["category"])
        r["band_from"] = float(r["band_from"])
        r["band_to"] = float(r["band_to"])
        r["coeff"] = float(r["coeff"])
    return rows

def load_zones() -> list[dict]:
    rows = _read_csv(DATA / "zones.csv")
    for r in rows:
        r["value"] = float(r["value"])
    return rows

def load_risk_allowances() -> list[dict]:
    rows = _read_csv(DATA / "risk_allowances.csv")
    for r in rows:
        r["value"] = float(r["value"])
    return rows
