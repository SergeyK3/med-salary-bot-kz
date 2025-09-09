# coding: utf-8
from src.config import load_settings
from src.calc.base_oklad import get_ets_coeff
from src.calc.allowances import (
    calc_k1, calc_k2, calc_k3, calc_k4, calc_k5, calc_k6, special_conditions
)


def role_coeff(role: str, settings: dict) -> float:
    r = role.strip().lower()
    if r.startswith("врач"):
        return float(settings["role_coefficients"]["врач"])
    if r.startswith("сест"):
        return float(settings["role_coefficients"]["сестра"])
    return float(settings["role_coefficients"]["младший"])


def calc_total(answers: dict) -> dict:
    settings = load_settings()
    ets = get_ets_coeff(
        answers["role"],
        answers.get("education"),
        answers["category"],
        float(answers["experience_years"]),
    )

    # должностной оклад округляем до целого
    base_oklad_raw = float(settings["BDO"]) * ets * role_coeff(answers["role"], settings)
    base_oklad = round(base_oklad_raw)

    k1 = calc_k1(answers.get("eco_zone"), settings)
    k2 = calc_k2(answers.get("location", ""), settings)
    k3 = calc_k3(bool(answers.get("senior_nurse")), settings)
    k4 = calc_k4(answers.get("hazard_profile"), settings)
    k5 = calc_k5(
        answers.get("facility", ""),
        answers["role"],
        bool(answers.get("is_surgery")),
        settings,
    )
    k6 = calc_k6(bool(answers.get("is_district")), answers["role"], settings)
    k_spec = special_conditions(settings)

    # итоговую сумму тоже округляем до целого
    total_raw = base_oklad + k1 + k2 + k3 + k4 + k5 + k6 + k_spec
    total = round(total_raw)

    return {
        "ets_coeff": ets,
        "base_oklad": base_oklad,
        "allowances": {
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "k4": k4,
            "k5": k5,
            "k6": k6,
            "special": k_spec,
        },
        "total_salary": total,
    }


# Совместимость со старым API (если где-то используется)
def total_amount(
    ets_coeff: float,
    role: str,
    k1: float,
    k2: float,
    k3: float,
    k4: float,
    k5: float,
    k6: float,
    kspec: float,
) -> float:
    settings = load_settings()
    # должностной оклад округляем до целого
    base_oklad_raw = float(settings["BDO"]) * ets_coeff * role_coeff(role, settings)
    base_oklad = round(base_oklad_raw)
    # итоговая сумма тоже округляется до целого
    total_raw = base_oklad + k1 + k2 + k3 + k4 + k5 + k6 + kspec
    return round(total_raw)
