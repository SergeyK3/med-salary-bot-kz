# coding: utf-8
from src.config import load_settings
from src.calc.base_oklad import get_ets_coeff
from src.calc.allowances import (
    calc_k1, calc_k2, calc_k3, calc_k4, calc_k5, calc_k6, special_conditions
)

def role_coeff(role: str, settings: dict) -> float:
    r = (role or "").strip().lower()
    if r.startswith("врач"):
        return float(settings["role_coefficients"]["врач"])
    if r.startswith("сест"):
        return float(settings["role_coefficients"]["сестра"])
    return float(settings["role_coefficients"]["младший"])

def calc_total(answers: dict) -> dict:
    settings = load_settings()
    ets = get_ets_coeff(
        answers["role"], answers.get("education"), answers.get("category"),
        float(answers.get("experience_years", 0.0))
    )
    base_oklad = float(settings["BDO"]) * ets * role_coeff(answers["role"], settings)

    # передаём base_oklad в k1 и k2 (см. новые сигнатуры)
    k1 = calc_k1(answers.get("eco_zone"), base_oklad, settings)
    k2 = calc_k2(answers.get("location", ""), base_oklad, settings)

    k3 = calc_k3(bool(answers.get("is_head")), settings)
    k4 = calc_k4(answers.get("hazard_profile"), settings)
    k5 = calc_k5(answers.get("facility", ""), answers["role"], bool(answers.get("is_surgery")), settings)
    k6 = calc_k6(bool(answers.get("is_district")), answers["role"], settings)

    k_spec = special_conditions(base_oklad, settings)  # 10% от ДО

    total = base_oklad + k1 + k2 + k3 + k4 + k5 + k6 + k_spec
    return {
        "ets_coeff": ets,
        "base_oklad": base_oklad,
        "allowances": {"k1": k1, "k2": k2, "k3": k3, "k4": k4, "k5": k5, "k6": k6, "special": k_spec},
        "total_salary": total
    }

# совместимость со старым API
def total_amount(ets_coeff: float, role: str, k1: float, k2: float, k3: float, k4: float, k5: float, k6: float, kspec: float) -> float:
    settings = load_settings()
    base_oklad = float(settings["BDO"]) * ets_coeff * role_coeff(role, settings)
    return base_oklad + k1 + k2 + k3 + k4 + k5 + k6 + kspec
