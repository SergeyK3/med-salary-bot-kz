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
        "senior_nurse": False,
        "hazard_profile": None,
        "is_surgery": True,
        "is_district": False,
    }
    res = calc_total(answers)
    assert abs(res["ets_coeff"] - 5.21) < 1e-9
    assert round(res["base_oklad"], 2) == round(315329, 2)
    assert round(abs(res["allowances"]["k5"] - 26_545.5), 2) < round(0.01, 2)
    assert round(abs(res["allowances"]["special"] - 1_769.7), 2) < round(0.01, 2)
    assert round(res["total_salary"], 2) == round(343644, 2)  # исправлено: сравнение с округлённым значением