"""
Главная точка входа для расчёта зарплаты.

Функция calc_salary принимает словарь с ответами пользователя,
а возвращает итоговый расчёт (оклад и все доплаты).
"""

from calc.base_oklad import get_ets_coeff
from calc.allowances import (
    calc_k1, calc_k2, calc_k3, calc_k4, calc_k5, calc_k6, special_conditions
)
from calc.totals import calc_total

def calc_salary(answers: dict) -> dict:
    """
    answers: {
        "role": "врач" | "сестра",
        "education": "высшее" | "среднее",
        "experience_years": int,
        "category": "высшая" | "первая" | "вторая" | "нет",
        "eco_zone": str | None,
        "location": "город" | "село",
        "facility": "стационар" | "поликлиника",
        "is_head": bool,
        "hazard_profile": str | None,
        "is_surgery": bool,
        "is_district": bool
    }
    """
    # 1. Определяем коэффициент ЕТС
    ets_coeff = get_ets_coeff(
        answers["role"],
        answers["education"],
        answers["category"],
        answers["experience_years"]
    )

    # 2. Считаем надбавки
    k1 = calc_k1(answers.get("eco_zone"))
    k2 = calc_k2(answers["location"])
    k3 = calc_k3(answers["is_head"])
    k4 = calc_k4(answers.get("hazard_profile"))
    k5 = calc_k5(answers["facility"], answers["role"], answers["is_surgery"])
    k6 = calc_k6(answers["is_district"], answers["role"])
    k_spec = special_conditions()

    # 3. Считаем итог
    total = calc_total(
        ets_coeff=ets_coeff,
        role=answers["role"],
        k1=k1, k2=k2, k3=k3, k4=k4, k5=k5, k6=k6,
        k_spec=k_spec
    )

    return {
        "ets_coeff": ets_coeff,
        "total_salary": total,
        "breakdown": {
            "k1": k1, "k2": k2, "k3": k3, "k4": k4, "k5": k5, "k6": k6,
            "special": k_spec
        }
    }
