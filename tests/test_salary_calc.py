import pytest
from src.calc.totals import calc_total

def test_salary_is_integer():
    answers = {
        "role": "врач",
        "education": None,
        "experience_years": 11,
        "category": "первая",
        "eco_zone": None,
        "location": "город",
        "facility": "стационар",
        "senior_nurse": False,
        "hazard_profile": None,
        "is_surgery": True,
        "is_uchastok": False,
    }

    result = calc_total(answers)

    # Печать для отладки (видно только с флагом -s)
    print("\n=== Расчёт зарплаты ===")
    print("Базовый оклад:", result["base_oklad"])
    print("Итоговая сумма:", result["total_salary"])

    # Проверки
    assert isinstance(result["base_oklad"], int)
    assert isinstance(result["total_salary"], int)
    assert round(result["base_oklad"], 2) > round(0, 2)
    assert round(result["total_salary"], 2) > round(0, 2)
