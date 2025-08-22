# src/calc/totals.py
from __future__ import annotations
from ..utils.data_loader import load_settings

S = load_settings()
BDO = float(S["BDO"])

def role_coeff(role: str) -> float:
    return float(S["role_coefficients"].get(role, 2.0))

def base_amount(ets_coeff: float, role: str) -> float:
    return BDO * float(ets_coeff) * role_coeff(role)

def total_amount(ets_coeff: float, role: str, *allowances: float) -> float:
    # allowances — уже суммы в тенге (К1..К6 и «особые условия»)
    return base_amount(ets_coeff, role) + sum(float(x) for x in allowances)
