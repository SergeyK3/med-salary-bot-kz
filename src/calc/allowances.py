from __future__ import annotations
from ..utils.data_loader import load_settings, load_zones, load_risk_allowances

S = load_settings()
BDO = float(S["BDO"])
MRP = float(S["MRP"])

# К1 — экозоны (часть от ДО или МРП, возвращаем сумму в тенге)
def k1_amount(zone_code: str | None) -> float:
    if not zone_code:
        return 0.0
    for z in load_zones():
        if z["code"] == zone_code:
            return (z["value"] * (BDO if z["calc_base"].upper() == "DO" else MRP))
    return 0.0

# К2 — сельская местность (от ДО)
def k2_amount(location: str) -> float:
    return (S.get("k2_rural", 0.25) * BDO) if str(location).lower().startswith("село") else 0.0

# К3 — заведование/старшая (от ДО)
def k3_amount(is_head: bool) -> float:
    return (S.get("k3_head", 0.05) * BDO) if is_head else 0.0

# К4 — вредность (все от ДО, по ключам из data/risk_allowances.csv)
def k4_amount(profile_key: str | None) -> float:
    if not profile_key:
        return 0.0
    for r in load_risk_allowances():
        if r["key"] == profile_key:
            return r["value"] * BDO
    return 0.0

# К5 — стационар (от БДО)
def k5_amount(facility: str, role: str, is_surgery: bool) -> float:
    if not str(facility).lower().startswith("стац"):
        return 0.0
    branch = "хирургия" if is_surgery else "терапия"
    mult = float(S["k5_inpatient"].get(role, {}).get(branch, 0.0))
    return mult * BDO

# К6 — участковый (от БДО)
def k6_amount(is_district: bool, role: str) -> float:
    if not is_district:
        return 0.0
    mult = float(S["k6_district"].get(role, 0.0))
    return mult * BDO

# Особые условия — 0.1 ДО
def special_amount() -> float:
    return float(S.get("special_conditions", 0.1)) * BDO
