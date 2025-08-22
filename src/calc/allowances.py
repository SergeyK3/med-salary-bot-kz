"""
Модуль для расчёта надбавок К1–К6 и "особые условия труда".
"""

def calc_k1(eco_zone: str | None) -> float:
    # TODO: реализовать по таблице data/zones.csv
    return 0.0

def calc_k2(location: str) -> float:
    return 0.25 if location == "село" else 0.0

def calc_k3(is_head: bool) -> float:
    return 0.05 if is_head else 0.0

def calc_k4(profile: str | None) -> float:
    # TODO: реализовать по таблице data/risk_allowances.csv
    return 0.0

def calc_k5(facility: str, role: str, is_surgery: bool) -> float:
    # TODO: реализовать (стационар / хирургия / терапия)
    return 0.0

def calc_k6(is_district: bool, role: str) -> float:
    # TODO: реализовать (участковый врач / сестра)
    return 0.0

def special_conditions() -> float:
    return 0.1
