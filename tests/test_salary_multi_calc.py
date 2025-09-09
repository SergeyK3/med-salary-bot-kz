import pytest
import sqlite3
import pandas as pd
from copy import deepcopy
from src.calc.totals import calc_total

def load_eco_zone_names():
    conn = sqlite3.connect("data/zones.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT code, name FROM zones")
    eco_zone_names = {row[0]: row[1] for row in cur.fetchall()}
    conn.close()
    return eco_zone_names

def load_risk_labels():
    conn = sqlite3.connect("data/risk_allowances.sqlite")
    df = pd.read_sql("SELECT key, label, value FROM risk_allowances", conn)
    conn.close()
    # value приводим к float для корректного форматирования
    return {row["key"]: (row["label"], float(row["value"])) for _, row in df.iterrows()}

ECO_ZONE_NAMES = load_eco_zone_names()
RISK_LABELS = load_risk_labels()

def _print_result(title: str, result: dict, answers: dict) -> None:
    hazard_code = answers.get("hazard_profile")
    hazard_label = None
    hazard_value = None
    # Меняем заголовок, если есть вредность
    if hazard_code and hazard_code in RISK_LABELS:
        hazard_label, hazard_value = RISK_LABELS[hazard_code]
        title = f"Вредные условия: {hazard_label}"
    print("\n===", title, "===")
    # Входные данные: заменяем hazard_profile на label
    inputs = deepcopy(answers)
    if hazard_code and hazard_code in RISK_LABELS:
        inputs["hazard_profile"] = hazard_label
    print("Входные данные:", inputs)
    print("Базовый оклад:", result["base_oklad"])
    alw = result.get("allowances", {})
    eco_code = answers.get("eco_zone")
    eco_label = ECO_ZONE_NAMES.get(eco_code) if eco_code else ECO_ZONE_NAMES.get('none')
    if alw.get('k1') and eco_label:
        print(f"  k1 (эко-зона): {alw.get('k1')} ({eco_label})")
    print(f"  k2 (село/местность): {alw.get('k2')}")
    print(f"  k3 (рук. должность): {alw.get('k3')}")
    # k4: вредные условия с label и %
    if hazard_label is not None and hazard_value is not None:
        percent = hazard_value * 100
        k4_value = round(alw.get('k4', 0.0), 2)
        print(f"  k4 (вредные условия, {hazard_label}, {percent:.0f}%): {k4_value}")
    else:
        print(f"  k4 (вредные условия): {alw.get('k4')}")
    print(f"  k5 (профиль/операции): {alw.get('k5')}")
    print(f"  k6 (участковость): {alw.get('k6')}")
    print(f"  Особые условия (10%): {alw.get('special')}")
    print("Итоговая сумма (total):", result["total_salary"])

@pytest.mark.parametrize(
    "scenario",
    [
        {"name": "База/город", "location": "город", "eco_zone": None, "hazard_profile": None, "is_head": False, "is_district": False},
        {"name": "Село", "location": "село", "eco_zone": None, "hazard_profile": None, "is_head": False, "is_district": False},
        {"name": "Эко-зона (radiation_high)", "location": "город", "eco_zone": "radiation_high", "hazard_profile": None, "is_head": False, "is_district": False},
        {"name": "Вредность: рентген", "location": "город", "eco_zone": None, "hazard_profile": "xray", "is_head": False, "is_district": False},
        {"name": "Вредность: УЗИ", "location": "город", "eco_zone": None, "hazard_profile": "ultrasound", "is_head": False, "is_district": False},
        {"name": "Вредность: инфекционное", "location": "город", "eco_zone": None, "hazard_profile": "infectious", "is_head": False, "is_district": False},
        {"name": "Руководитель (ст. медсестра)", "location": "город", "eco_zone": None, "hazard_profile": None, "is_head": True, "is_district": False},
        {"name": "Комбо: село+эко+вредность+рук", "location": "село", "eco_zone": "radiation_high", "hazard_profile": "xray", "is_head": True, "is_district": False},
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
    assert isinstance(result["base_oklad"], (int, float)), f"base_oklad получено {type(result['base_oklad'])}"
    assert isinstance(result["total_salary"], (int, float)), f"total_salary должен быть int или float, получено {type(result['total_salary'])}"
    assert result["base_oklad"] > 0, "base_oklad должен быть > 0"
    assert result["total_salary"] > 0, "total_salary должен быть > 0"

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-s", *sys.argv[1:]]))