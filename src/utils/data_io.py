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

def read_ets(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        path = ROOT / "data" / "ets_coefficients.csv"
    cols = {"group", "category", "band_label", "band_from", "band_to", "coeff"}
    return _read_robust(Path(path), cols)

def read_zones(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        path = ROOT / "data" / "zones.csv"
    cols = {"code", "name", "calc_base", "value", "notes"}
    return _read_robust(Path(path), cols)
