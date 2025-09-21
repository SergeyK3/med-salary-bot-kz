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
    "is_uchastok": False,
}

res = calc_salary(answers)
print("ETS:", res["ets_coeff"])
print("Base:", round(res["base_oklad"], 2))
def _fmt_allowances(dct):
    out = {}
    for k, v in dct.items():
        if isinstance(v, (int, float)):
            out[k] = round(float(v), 2)
        else:
            out[k] = v
    return out

print("Allowances:", _fmt_allowances(res["allowances"]))
print("TOTAL:", round(res["total_salary"], 2))
