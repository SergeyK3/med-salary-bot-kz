# coding: utf-8
from src.config import load_settings
from src.calc.base_oklad import get_ets_coeff
from src.calc.allowances import (
    calc_k1, calc_k2, calc_k3, calc_k4, calc_k5, calc_k6, calc_senior_nurse, special_conditions
)

def role_coeff(role: str, settings: dict) -> float:
    r = role.strip().lower()
    if r.startswith("врач"):
        return float(settings["role_coefficients"]["врач"])
    # распознаём медсестру по подстроке, чтобы охватить 'медсестра', 'старшая медсестра' и т.п.
    if "сест" in r:
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
    role_mult = role_coeff(answers["role"], settings)
    print("ETS coeff:", ets, "Role multiplier:", role_mult)  # Для отладки

    # должностной оклад с учетом дополнительного коэффициента
    job_oklad_raw = float(settings["BDO"]) * ets * role_mult
    job_oklad = round(job_oklad_raw, 2)

    k1 = calc_k1(answers.get("eco_zone"), job_oklad)
    k2 = calc_k2(answers["location"], job_oklad)
    
    k3 = calc_k3(answers.get("senior_nurse", False), job_oklad)

    k4, k4_label, k4_value = calc_k4(answers.get("hazard_profile"), float(settings["BDO"]))
    k5 = calc_k5(
        answers["role"],
        answers.get("facility", ""),
        bool(answers.get("is_surgery")),
        bool(answers.get("is_uchastok")),
        float(settings["BDO"])
    )

    # k6 перенесён в k5 для участковых (чтобы не дублировать начисление)
    k6 = 0.0

    k_spec = special_conditions(job_oklad)

    # итоговую сумму тоже округляем до двух знаков после запятой
    total_raw = job_oklad + k1 + k2 + k3 + k4 + k5 + k6 + k_spec
    total = round(total_raw, 2)

    return {
        "ets_coeff": ets,
        # Новый ключ с более ясным названием и алиас для совместимости
        "job_oklad": job_oklad,
        "base_oklad": job_oklad,
        "allowances": {
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "k4": k4,
            "k4_label": k4_label,
            "k4_value": k4_value,
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
    kspec: float,
) -> float:
    settings = load_settings()
    # должностной оклад округляем до двух знаков после запятой
    job_oklad_raw = float(settings["BDO"]) * ets_coeff * role_coeff(role, settings)
    job_oklad = round(job_oklad_raw, 2)
    # итоговая сумма тоже округляется до двух знаков после запятой
    total_raw = job_oklad + k1 + k2 + k3 + k4 + k5 + kspec
    return round(total_raw, 2)