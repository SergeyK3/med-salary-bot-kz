from src.main import calc_salary

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
    "is_district": False,
}

res = calc_salary(answers)
print("ETS:", res["ets_coeff"])
print("Base:", round(res["base_oklad"], 2))
print("Allowances:", {k: round(v,2) for k,v in res["allowances"].items()})
print("TOTAL:", round(res["total_salary"], 2))
