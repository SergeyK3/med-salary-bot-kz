# src/main.py
from __future__ import annotations
from .calc.base_oklad import get_ets_coeff
from .calc.allowances import (
    k1_amount, k2_amount, k3_amount, k4_amount, k5_amount, k6_amount, special_amount
)
from .calc.totals import total_amount

def calc_salary(answers: dict) -> dict:
    ets = get_ets_coeff(
        role=answers["role"],
        education=answers.get("education"),
        category=answers["category"],
        years=float(answers["experience_years"]),
    )

    k1 = k1_amount(answers.get("eco_zone"))
    k2 = k2_amount(answers.get("location", "город"))
    k3 = k3_amount(bool(answers.get("is_head")))
    k4 = k4_amount(answers.get("hazard_profile"))
    k5 = k5_amount(answers.get("facility", ""), answers["role"], bool(answers.get("is_surgery")))
    k6 = k6_amount(bool(answers.get("is_district")), answers["role"])
    kspec = special_amount()

    total = total_amount(ets, answers["role"], k1, k2, k3, k4, k5, k6, kspec)

    return {
        "ets_coeff": ets,
        "total_salary": round(total, 2),
        "breakdown": {"k1": k1, "k2": k2, "k3": k3, "k4": k4, "k5": k5, "k6": k6, "special": kspec},
    }
