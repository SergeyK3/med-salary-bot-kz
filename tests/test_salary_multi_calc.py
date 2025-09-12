import pytest
from copy import deepcopy
from src.calc.totals import calc_total


def _print_result(title: str, result: dict, answers: dict) -> None:
    print("\n===", title, "===")
    print("Входные данные:", {
        k: answers.get(k) for k in [
            "role", "education", "experience_years", "category",
            "eco_zone", "location", "facility", "senior_nurse",
            "hazard_profile", "is_surgery", "is_uchastok"
        ]
    })
    print("Базовый оклад:", f"{result['base_oklad']:.2f}")
    alw = result.get("allowances", {})
    print("Надбавки:")
    print(f"  k1 (эко-зона): {alw.get('k1', 0):.2f}")
    print(f"  k2 (город/село): {alw.get('k2', 0):.2f}")
    print(f"  k3 (рук. должность): {alw.get('k3', 0):.2f}")
    print(f"  k4 (вредность): {alw.get('k4', 0):.2f} ({alw.get('k4_label', '')}, {alw.get('k4_value', 0)})")
    print(f"  k5 (психоэмоц напряжение): {alw.get('k5', 0):.2f}")
    print("Итоговая сумма (total):", f"{result['total_salary']:.2f}")

@pytest.mark.parametrize(
    "scenario",
    [
        {"name": "База/город/врач/стационар", "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False, "is_uchastok": False},
        {"name": "Село", "location": "село", "eco_zone": None, "hazard_profile": None, "senior_nurse": False, "is_uchastok": False},
        {"name": "Эко-зона (radiation_high)", "location": "город", "eco_zone": "radiation_high", "hazard_profile": None, "senior_nurse": False, "is_uchastok": False},
        {"name": "Вредность: рентген", "location": "город", "eco_zone": None, "hazard_profile": "xray", "senior_nurse": False, "is_uchastok": False},
        {"name": "Вредность: УЗИ", "location": "город", "eco_zone": None, "hazard_profile": "ultrasound", "senior_nurse": False, "is_uchastok": False},
        {"name": "Вредность: инфекционное отделение", "location": "город", "eco_zone": None, "hazard_profile": "infectious", "senior_nurse": False, "is_uchastok": False},        
        {"name": "Ст. медсестра", "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": True, "is_uchastok": False, "role": "медсестра", "education": "среднее"},
        {"name": "Комбо: село+эко+вредность+рук", "location": "село", "eco_zone": "radiation_high", "hazard_profile": "xray", "senior_nurse": True, "is_uchastok": False, "role": "медсестра", "education": "среднее"},
                
        {"name": "База/город/врач/участковый", "location": "город", "facility": "поликлиника", "eco_zone": None, "hazard_profile": None, "senior_nurse": False, "is_uchastok": True},
        {"name": "Село", "location": "село", "facility": "поликлиника", "eco_zone": None, "hazard_profile": None, "senior_nurse": False, "is_uchastok": True},
        {"name": "Эко-зона (radiation_high)", "location": "город", "facility": "поликлиника", "eco_zone": "radiation_high", "hazard_profile": None, "senior_nurse": False, "is_uchastok": True},
        {"name": "Вредность: рентген", "location": "город", "facility": "поликлиника", "eco_zone": None, "hazard_profile": "xray", "senior_nurse": False, "is_uchastok": True},
        {"name": "Вредность: УЗИ", "location": "город", "facility": "поликлиника", "eco_zone": None, "hazard_profile": "ultrasound", "senior_nurse": False, "is_uchastok": True},
        {"name": "Вредность: инфекционное отделение", "location": "город", "facility": "поликлиника", "eco_zone": None, "hazard_profile": "infectious", "senior_nurse": False, "is_uchastok": True},        
        {"name": "Ст. медсестра", "location": "город", "facility": "поликлиника", "eco_zone": None, "hazard_profile": None, "senior_nurse": True, "is_uchastok": True, "role": "медсестра", "education": "среднее"},
        {"name": "Комбо: село+эко+вредность+рук", "location": "село", "facility": "поликлиника", "eco_zone": "radiation_high", "hazard_profile": "xray", "senior_nurse": True, "is_uchastok": True, "role": "медсестра", "education": "среднее"},
        
        # Медсестра со средним образованием
{"name": "Медсестра/стационар/среднее/хирургия", "role": "медсестра", "education": "среднее", "facility": "стационар", "is_surgery": True, "is_uchastok": False, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},
{"name": "Медсестра/стационар/среднее/терапия", "role": "медсестра", "education": "среднее", "facility": "стационар", "is_surgery": False, "is_uchastok": False, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},
{"name": "Медсестра/поликлиника/среднее/участковая", "role": "медсестра", "education": "среднее", "facility": "поликлиника", "is_surgery": False, "is_uchastok": True, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},
{"name": "Медсестра/поликлиника/среднее/не участковая", "role": "медсестра", "education": "среднее", "facility": "поликлиника", "is_surgery": False, "is_uchastok": False, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},

# Медсестра с высшим образованием
{"name": "Медсестра/стационар/высшее/хирургия", "role": "медсестра", "education": "высшее", "facility": "стационар", "is_surgery": True, "is_uchastok": False, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},
{"name": "Медсестра/стационар/высшее/терапия", "role": "медсестра", "education": "высшее", "facility": "стационар", "is_surgery": False, "is_uchastok": False, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},
{"name": "Медсестра/поликлиника/высшее/участковая", "role": "медсестра", "education": "высшее", "facility": "поликлиника", "is_surgery": False, "is_uchastok": True, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},
{"name": "Медсестра/поликлиника/высшее/не участковая", "role": "медсестра", "education": "высшее", "facility": "поликлиника", "is_surgery": False, "is_uchastok": False, "location": "город", "eco_zone": None, "hazard_profile": None, "senior_nurse": False},
    
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
        "senior_nurse": False,
        "hazard_profile": None,
        "is_surgery": True,
        "is_uchastok": False,
    }

    answers = deepcopy(base_answers)
    answers.update({
        "location": scenario["location"],
        "eco_zone": scenario["eco_zone"],
        "hazard_profile": scenario["hazard_profile"],
        "senior_nurse": scenario["senior_nurse"],
        "is_uchastok": scenario.get("is_uchastok", False),
        "facility": scenario.get("facility", answers["facility"]),
    })

    # Добавлено: обработка role и education для сценариев старшей медсестры
    if "role" in scenario:
        answers["role"] = scenario["role"]
    if "education" in scenario:
        answers["education"] = scenario["education"]

    result = calc_total(answers)

    # Печать (видно при запуске с -s)
    _print_result(scenario["name"], result, answers)

    # Инварианты
    assert isinstance(result["base_oklad"], (float, int)), f"base_oklad должен быть float или int, получено {type(result['base_oklad'])}"
    assert isinstance(result["total_salary"], (float, int)), f"total_salary должен быть float или int, получено {type(result['total_salary'])}"
    assert round(result["base_oklad"], 2) > round(0, 2), "base_oklad должен быть > 0"
    assert round(result["total_salary"], 2) > round(0, 2), "total_salary должен быть > 0"


if __name__ == "__main__":
    # Позволяет запускать файл как обычный скрипт:
    #   python tests/test_salary_multi_calc.py
    import sys
    # добавляем -s для отображения print, остальные аргументы пробрасываем
    sys.exit(pytest.main([__file__, "-s", *sys.argv[1:]]))