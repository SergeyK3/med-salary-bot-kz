from src.calc.totals import calc_total

def test_total_doctor_surgery_case():
    answers = {
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
    res = calc_total(answers)
    assert abs(res["ets_coeff"] - 5.21) < 1e-9
    assert abs(res["base_oklad"] - 315_328.6854) < 0.01
    assert abs(res["allowances"]["k5"] - 26_545.5) < 0.01
    assert abs(res["allowances"]["special"] - 1_769.7) < 0.01
    assert abs(res["total_salary"] - 343_643.8854) < 0.02
