"""
Модуль для подсчёта итоговой зарплаты.
"""

BDO = 17697  # базовый должностной оклад (2025)
MRP = 3932   # минимальный расчётный показатель (2025)

def get_role_coeff(role: str) -> float:
    if role == "врач":
        return 3.42
    elif role == "сестра":
        return 2.34
    else:
        return 2.0  # по умолчанию младший персонал

def calc_total(ets_coeff: float, role: str, **kwargs) -> float:
    """
    ets_coeff: коэффициент ЕТС
    role: 'врач' | 'сестра'
    kwargs: значения k1..k6 и special
    """
    base = BDO * ets_coeff * get_role_coeff(role)
    total = base

    # Складываем надбавки
    for k in kwargs.values():
        total += k * BDO if k < 5 else k * MRP  # ДО vs МРП

    return total
