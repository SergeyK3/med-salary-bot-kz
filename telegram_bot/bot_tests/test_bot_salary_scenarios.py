from src.calc.totals import calc_total

scenarios = [
    {
        "name": "Врач, город, стационар, хирург",
        "role": "врач",
        "education": "высшее",
        "experience_years": 11,
        "category": "первая",
        "eco_zone": None,
        "location": "город",
        "facility": "стационар",
        "senior_nurse": False,
        "hazard_profile": None,
        "is_uchastok": False,
        "is_surgery": True,
    },
    {
        "name": "Врач, город, стационар, не хирург",
        "role": "врач",
        "education": "высшее",
        "experience_years": 11,
        "category": "первая",
        "eco_zone": None,
        "location": "город",
        "facility": "стационар",
        "senior_nurse": False,
        "hazard_profile": None,
        "is_uchastok": False,
        "is_surgery": False,
    },
    {
        "name": "Врач, город, поликлиника, участковый",
        "role": "врач",
        "education": "высшее",
        "experience_years": 11,
        "category": "первая",
        "eco_zone": None,
        "location": "город",
        "facility": "поликлиника",
        "senior_nurse": False,
        "hazard_profile": None,
        "is_uchastok": False,
        "is_surgery": None,
    },
]

for scenario in scenarios:
    print(f"\n--- {scenario['name']} ---")
    result = calc_total(scenario)
    print("Базовый оклад:", result["base_oklad"])
    print("Надбавки:", {k: round(v,2) for k,v in result["allowances"].items() if isinstance(v, (int, float))})
    print("Итоговая сумма:", result["total_salary"])
