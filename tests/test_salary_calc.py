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
    assert isinstance(result["base_oklad"], (int, float))
    assert round(result["base_oklad"], 2) == result["base_oklad"]
    assert isinstance(result["total_salary"], float)
    # Проверяем, что ровно два знака после запятой
    total_str = f"{result['total_salary']:.2f}"
    assert "." in total_str and len(total_str.split(".")[1]) == 2
    assert round(result["total_salary"], 2) == result["total_salary"]