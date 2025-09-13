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
def k1_amount(zone_code: Optional[str], base_oklad: float) -> float:
    z: pd.DataFrame = zones_df()
    # Проверяем, что zone_code указан и есть в таблице
    m = z["code"].str.lower() == str(zone_code or "").strip().lower()
    if not m.any():
        return 0.0
    row = z.loc[m].iloc[0]
    base = base_oklad if str(row["calc_base"]).upper() == "DO" else MRP
    return float(row["value"]) * float(base)

# --- K2 ---
def k2_amount(location: str, base_oklad: float) -> float:
    # Надбавка 25% от должностного оклада только для села
    if location.strip().lower() == "село":
        return 0.25 * base_oklad
    return 0.0

# --- K3 ---
def k3_amount(senior_nurse: bool, base_oklad: float) -> float:
    # Надбавка 5% только для старшей медсестры
    if senior_nurse:
        return 0.05 * base_oklad
    return 0.0

def calc_k3(is_head: bool, _settings: Optional[dict] = None) -> float:
    return k3_amount(is_head)

# --- Senior Nurse ---
def senior_nurse_amount(is_senior_nurse: bool) -> float:
    return 0.25 * BDO if is_senior_nurse else 0.0

def calc_senior_nurse(is_senior_nurse: bool, _settings: Optional[dict] = None) -> float:
    return senior_nurse_amount(is_senior_nurse)

def k4_amount(hazard_profile: Optional[str], base_oklad: float) -> tuple[float, str, float]:
    if hazard_profile is None:
        return 0.0, "", 0.0
    df = risk_df()
    filtered = df[df['key'] == hazard_profile]
    if filtered.empty:
        return 0.0, "", 0.0
    row = filtered.iloc[0]
    value = float(row['value'])
    label = row.get('label', '') if 'label' in row else ''
    return value * base_oklad, label, value

def calc_k4(hazard_profile: Optional[str], base_oklad: float, _settings: Optional[dict] = None) -> tuple[float, str, float]:
    return k4_amount(hazard_profile, base_oklad)

# --- K5 ---
def k5_amount(location, role, is_surgery, is_district, base_oklad):
    if role == "врач":
        if location == "стационар":
            if is_surgery:
                return base_oklad * 1.5
            else:
                return base_oklad * 0.8
        elif is_district:
            return base_oklad * 2.0
        else:
            return 0.0
    elif role == "сестра":
        if location == "стационар":
            if is_surgery:
                return base_oklad * 0.8
            else:
                return base_oklad * 0.4
        elif is_district:
            return base_oklad * 1.5
        else:
            return 0.0
    return 0.0

# --- K6 ---
def k6_amount(is_uchastok: bool, role: str) -> float:
    if not is_uchastok:
        return 0.0
    role_k = _role_key(role)
    mult = float(S["k6_district"][role_k])
    return mult * BDO

# --- Special ---
def special_amount(base_oklad: float) -> float:
    return float(S.get("special_conditions", 0.1)) * base_oklad

# Алиасы (совместимость)
def calc_k1(eco_code: Optional[str], base_oklad: float, _settings: Optional[dict] = None) -> float:
    return k1_amount(eco_code, base_oklad)
def calc_k2(location: str, base_oklad: float, _settings: Optional[dict] = None) -> float:        return k2_amount(location, base_oklad)
def calc_k4(hazard_profile: Optional[str], base_oklad: float, _settings: Optional[dict] = None) -> tuple[float, str, float]:
    return k4_amount(hazard_profile, base_oklad)
def calc_k5(role: str, facility: str, is_surgery: bool, is_uchastok: bool, BDO: float) -> float:
    return k5_amount(role, facility, is_surgery, is_uchastok, BDO)
def calc_k6(is_uchastok: bool, role: str, _settings: Optional[dict] = None) -> float:
    return k6_amount(is_uchastok, role)
def special_conditions(base_oklad: float, _settings: Optional[dict] = None) -> float:
    return special_amount(base_oklad)