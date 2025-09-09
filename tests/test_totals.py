from src.calc.totals import calc_total
from conftest import assertround

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

def test_total_nurse_therapy_case():
    """Test nurse in therapy department"""
    answers = {
        "role": "сестра",
        "education": "высшее",
        "experience_years": 4,
        "category": "первая",
        "eco_zone": None,
        "location": "город",
        "facility": "стационар",
        "is_head": False,
        "hazard_profile": None,
        "is_surgery": False,
        "is_district": False,
    }
    res = calc_total(answers)
    assert abs(res["ets_coeff"] - 4.39) < 1e-9
    assert res["base_oklad"] > 0
    assert res["total_salary"] > res["base_oklad"]

def test_total_district_doctor():
    """Test district doctor with special allowances"""
    answers = {
        "role": "врач",
        "education": None,
        "experience_years": 8.5,
        "category": "нет",
        "eco_zone": None,
        "location": "село",
        "facility": None,
        "is_head": False,
        "hazard_profile": None,
        "is_surgery": False,
        "is_district": True,
    }
    res = calc_total(answers)
    assert res["ets_coeff"] > 0
    assert res["allowances"]["k6"] > 0  # District allowance
    assert res["allowances"]["k2"] > 0  # Rural allowance
    assert res["total_salary"] > res["base_oklad"]

def test_total_head_doctor():
    """Test head doctor with management allowance"""
    answers = {
        "role": "врач",
        "education": None,
        "experience_years": 15,
        "category": "высшая",
        "eco_zone": None,
        "location": "город",
        "facility": "поликлиника",
        "is_head": True,
        "hazard_profile": None,
        "is_surgery": False,
        "is_district": False,
    }
    res = calc_total(answers)
    assert res["allowances"]["k3"] > 0  # Head allowance
    assert res["total_salary"] > res["base_oklad"]

def test_total_xray_specialist():
    """Test specialist with X-ray hazard"""
    answers = {
        "role": "врач",
        "education": None,
        "experience_years": 5,
        "category": "вторая",
        "eco_zone": None,
        "location": "город",
        "facility": "поликлиника",
        "is_head": False,
        "hazard_profile": "xray",
        "is_surgery": False,
        "is_district": False,
    }
    res = calc_total(answers)
    assert res["allowances"]["k4"] > 0  # Hazard allowance
    assert res["total_salary"] > res["base_oklad"]

def test_total_eco_zone_specialist():
    """Test specialist in ecological crisis zone"""
    answers = {
        "role": "сестра",
        "education": "среднее",
        "experience_years": 3,
        "category": "нет",
        "eco_zone": "eco_crisis",
        "location": "город",
        "facility": "стационар",
        "is_head": False,
        "hazard_profile": None,
        "is_surgery": False,
        "is_district": False,
    }
    res = calc_total(answers)
    assert res["allowances"]["k1"] > 0  # Eco zone allowance
    assert res["total_salary"] > res["base_oklad"]

def test_total_using_assertround():
    """Test using the new assertround utility function"""
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
    # Test using the new assertround function
    assertround(res["ets_coeff"], 5.21, 2)
    assertround(res["base_oklad"], 315328.69, 2)
    assertround(res["total_salary"], 343643.89, 2)
