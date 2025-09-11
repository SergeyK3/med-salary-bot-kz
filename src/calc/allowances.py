# coding: utf-8
from typing import Optional
import pandas as pd

from src.config import load_settings
from src.data_loaders import zones_df, risk_df

# Загружаем настройки один раз (внутри load_settings есть кэш)
S = load_settings()
BDO = float(S["BDO"])
MRP = float(S["MRP"])

def _role_key(role: str) -> str:
    r = (role or "").strip().lower()
    return "врач" if r.startswith("врач") else "сестра"

# --- K1 ---
def k1_amount(zone_code: Optional[str]) -> float:
    if not zone_code:
        return 0.0
    z: pd.DataFrame = zones_df()
    m = z["code"].str.lower() == str(zone_code).strip().lower()
    if not m.any():
        return 0.0
    row = z.loc[m].iloc[0]
    base = BDO if str(row["calc_base"]).upper() == "DO" else MRP
    return float(row["value"]) * float(base)

# --- K2 ---
def k2_amount(location: str, base_oklad: float) -> float:
    # Надбавка 25% от должностного оклада для города или села
    if location in ("город", "село"):
        return 0.25 * base_oklad
    return 0.0

# --- K3 ---
def k3_amount(is_head: bool) -> float:
    return float(S.get("k3_head", 0.05)) * BDO if is_head else 0.0

def calc_k3(is_head: bool, _settings: Optional[dict] = None) -> float:
    return k3_amount(is_head)

# --- Senior Nurse ---
def senior_nurse_amount(is_senior_nurse: bool) -> float:
    return 0.25 * BDO if is_senior_nurse else 0.0

def calc_senior_nurse(is_senior_nurse: bool, _settings: Optional[dict] = None) -> float:
    return senior_nurse_amount(is_senior_nurse)

# --- K4 ---
def k4_amount(hazard_profile: str, base_oklad: float) -> tuple[float, str, float]:
    if hazard_profile is None:
        return 0.0, "", 0.0
    df = risk_df()
    filtered = df[df['key'] == hazard_profile]
    if filtered.empty:
        return 0.0, "", 0.0
    row = filtered.iloc[0]
    value = float(row['value'])
    label = row['label']
    return value * base_oklad, label, value

# --- K5 ---
def k5_amount(facility: str, role: str, is_surgery: bool) -> float:
    if not str(facility).strip().lower().startswith("стац"):
        return 0.0
    branch = "хирургия" if is_surgery else "терапия"
    role_k = _role_key(role)
    mult = float(S["k5_inpatient"][role_k][branch])
    return mult * BDO

# --- K6 ---
def k6_amount(is_district: bool, role: str) -> float:
    if not is_district:
        return 0.0
    role_k = _role_key(role)
    mult = float(S["k6_district"][role_k])
    return mult * BDO

# --- Special ---
def special_amount(base_oklad: float) -> float:
    return float(S.get("special_conditions", 0.1)) * base_oklad

# Алиасы (совместимость)
def calc_k1(eco_code: Optional[str], _settings: Optional[dict] = None) -> float: return k1_amount(eco_code)
def calc_k2(location: str, base_oklad: float, _settings: Optional[dict] = None) -> float:        return k2_amount(location, base_oklad)
def calc_k4(profile: Optional[str], base_oklad: float, _settings: Optional[dict] = None) -> tuple[float, str, float]:
    return k4_amount(profile, base_oklad)
def calc_k5(facility: str, role: str, is_surgery: bool, _settings: Optional[dict] = None) -> float:
    return k5_amount(facility, role, is_surgery)
def calc_k6(is_district: bool, role: str, _settings: Optional[dict] = None) -> float:
    return k6_amount(is_district, role)
def special_conditions(base_oklad: float, _settings: Optional[dict] = None) -> float:
    return special_amount(base_oklad)