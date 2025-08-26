# coding: utf-8
from typing import Optional
import pandas as pd

from src.config import load_settings
from src.data_loaders import zones_df, risk_df

S = load_settings()
BDO = float(S["BDO"])
MRP = float(S["MRP"])

def _role_key(role: str) -> str:
    r = (role or "").strip().lower()
    return "врач" if r.startswith("врач") else "сестра"

# --- K1: эко/радиация/льготные зоны ---
def k1_amount(zone_code: Optional[str], base_oklad: Optional[float] = None) -> float:
    """
    Эко-зоны с calc_base=DO считаются от ДО (base_oklad),
    радиация/льготные с calc_base=MRP — от МРП.
    """
    if not zone_code:
        return 0.0
    z: pd.DataFrame = zones_df()
    m = z["code"].str.lower() == str(zone_code).strip().lower()
    if not m.any():
        return 0.0

    row = z.loc[m].iloc[0]
    calc_base = str(row["calc_base"]).strip().upper()
    val = float(str(row["value"]).replace(",", "."))  # на случай "1,75"

    if calc_base == "MRP":
        return val * MRP
    # calc_base == "DO" → от должностного оклада
    if base_oklad is None:
        # на всякий случай fallback (но в итоговом расчёте мы передаём base_oklad)
        return val * BDO
    return val * float(base_oklad)

# --- K2: сельская местность ---
def k2_amount(location: str, base_oklad: Optional[float] = None) -> float:
    """
    Должна считаться от ДО (base_oklad).
    Если base_oklad не передан — аккуратный fallback на БДО для обратной совместимости.
    """
    if not str(location).strip().lower().startswith("село"):
        return 0.0
    mult = float(S.get("k2_rural", 0.25))
    if base_oklad is None:
        return mult * BDO
    return mult * float(base_oklad)

# --- K3 ---
def k3_amount(is_head: bool) -> float:
    return float(S.get("k3_head", 0.05)) * BDO if is_head else 0.0

# --- K4: вредные условия ---
def k4_amount(profile_key: Optional[str]) -> float:
    if not profile_key:
        return 0.0
    r: pd.DataFrame = risk_df()
    key = str(profile_key).strip().lower()
    m = (r["key"].str.lower() == key) | (r["label"].str.lower() == key)
    if not m.any():
        return 0.0
    row = r.loc[m].iloc[0]
    return float(row["value"]) * BDO  # k4 остаётся от БДО

# --- K5: стационар ---
def k5_amount(facility: str, role: str, is_surgery: bool) -> float:
    if not str(facility).strip().lower().startswith("стац"):
        return 0.0
    branch = "хирургия" if is_surgery else "терапия"
    role_k = _role_key(role)
    mult = float(S["k5_inpatient"][role_k][branch])
    return mult * BDO

# --- K6: участковость ---
def k6_amount(is_district: bool, role: str) -> float:
    if not is_district:
        return 0.0
    role_k = _role_key(role)
    mult = float(S["k6_district"][role_k])
    return mult * BDO

# --- Special: 10% от ДО (базового оклада) ---
def special_amount(base_salary: float) -> float:
    return 0.1 * float(base_salary)

# Алиасы (совместимость со старым API)
def calc_k1(eco_code: Optional[str], base_salary: Optional[float] = None, _settings: Optional[dict] = None) -> float:
    return k1_amount(eco_code, base_salary)

def calc_k2(location: str, base_salary: Optional[float] = None, _settings: Optional[dict] = None) -> float:
    return k2_amount(location, base_salary)

def calc_k3(is_head: bool, _settings: Optional[dict] = None) -> float:
    return k3_amount(is_head)

def calc_k4(profile: Optional[str], _settings: Optional[dict] = None) -> float:
    return k4_amount(profile)

def calc_k5(facility: str, role: str, is_surgery: bool, _settings: Optional[dict] = None) -> float:
    return k5_amount(facility, role, is_surgery)

def calc_k6(is_district: bool, role: str, _settings: Optional[dict] = None) -> float:
    return k6_amount(is_district, role)

def special_conditions(base_salary: float, _settings: Optional[dict] = None) -> float:
    return special_amount(base_salary)
