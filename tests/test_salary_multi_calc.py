import pytest
from copy import deepcopy
from src.calc.totals import calc_total


def _print_result(title: str, result: dict, answers: dict) -> None:
    print("\n===", title, "===")
    print("Входные данные:", {
        k: answers.get(k) for k in [
            "role", "education", "experience_years", "category",
            "eco_zone", "location", "facility", "is_head",
            "hazard_profile", "is_surgery", "is_district"
        ]
    })
    print("Базовый оклад:", result["base_oklad"])
    alw = result.get("allowances", {})
    print("Надбавки:")
    print(f"  k1 (эко-зона): {alw.get('k1')}")
    print(f"  k2 (село/местность): {alw.get('k2')}")
    print(f"  k3 (рук. должность): {alw.get('k3')}")
    print(f"  k4 (вредность): {alw.get('k4')}")
    print(f"  k5 (профиль/операции): {alw.get('k5')}")
    print(f"  k6 (участковость): {alw.get('k6')}")
    print(f"  special (психоэмоц. напр.): {alw.get('special')}")
    print("Итоговая сумма (total):", result["total_salary"])


@pytest.mark.parametrize(
    "scenario",
    [
        {"name": "База/город", "location": "город", "eco_zone": None, "hazard_profile": None, "is_head": False, "is_district": False},
        {"name": "Село", "location": "село", "eco_zone": None, "hazard_profile": None, "is_head": False, "is_district": False},
        {"name": "Эко-зона (radiation_high)", "location": "город", "eco_zone": "radiation_high", "hazard_profile": None, "is_head": False, "is_district": False},
        {"name": "Вредность: радиация", "location": "город", "eco_zone": None, "hazard_profile": "radiation", "is_head": False, "is_district": False},
        {"name": "Вредность: химия", "location": "город", "eco_zone": None, "hazard_profile": "chemical", "is_head": False, "is_district": False},
        {"name": "Вредность: инфекция", "location": "город", "eco_zone": None, "hazard_profile": "infection", "is_head": False, "is_district": False},
        {"name": "Руководитель (зав. отделением)", "location": "город", "eco_zone": None, "hazard_profile": None, "is_head": True, "is_district": False},
        {"name": "Комбо: село+эко+вредность+рук", "location": "село", "eco_zone": "radiation_high", "hazard_profile": "radiation", "is_head": True, "is_district": False},
        {"name": "Участковость", "location": "город", "eco_zone": None, "hazard_profile": None, "is_head": False, "is_district": True},
    ],
)
def test_salary_scenarios_print_and_validate(scenario):
    base_answers = {
        "role": "врач",
        "education": None,
        "experience_years": 11,
        "category": "первая",
        "eco_zone": None,
        "location": "город",
        "facility": "стационар",
        "is_head": False,
        "hazard_profile": None,
        "is_surgery": True,
        "is_district": False,
    }

    answers = deepcopy(base_answers)
    answers.update({
        "location": scenario["location"],
        "eco_zone": scenario["eco_zone"],
        "hazard_profile": scenario["hazard_profile"],
        "is_head": scenario["is_head"],
        "is_district": scenario["is_district"],
    })

    result = calc_total(answers)

    # Печать (видно при запуске с -s)
    _print_result(scenario["name"], result, answers)

    # Инварианты
    assert isinstance(result["base_oklad"], int), f"base_oklad должен быть int, получено {type(result['base_oklad'])}"
    assert isinstance(result["total_salary"], int), f"total_salary должен быть int, получено {type(result['total_salary'])}"
    assert result["base_oklad"] > 0, "base_oklad должен быть > 0"
    assert result["total_salary"] > 0, "total_salary должен быть > 0"


if __name__ == "__main__":
    # Позволяет запускать файл как обычный скрипт:
    #   python tests/test_salary_multi_calc.py
    import sys
    # добавляем -s для отображения print, остальные аргументы пробрасываем
    sys.exit(pytest.main([__file__, "-s", *sys.argv[1:]]))
