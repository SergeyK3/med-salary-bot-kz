from src.calc.allowances import k1_amount, k4_amount, k5_amount, k6_amount, special_amount
from src.utils.data_loader import load_settings

def test_k1_eco_catastrophe_uses_bdo():
    S = load_settings()
    assert k1_amount("eco_catastrophe") == float(S["BDO"]) * 0.5

def test_k4_xray_from_bdo():
    S = load_settings()
    assert k4_amount("xray") == float(S["BDO"]) * 1.0  # рентген = 1.0 ДО

def test_k5_inpatient_surgery_doctor():
    S = load_settings()
    # стационар + хирургия → врач 1.5 БДО
    assert k5_amount("стационар", "врач", True) == float(S["BDO"]) * 1.5

def test_k6_district_nurse():
    S = load_settings()
    # участковая сестра 1.5 БДО
    assert k6_amount(True, "сестра") == float(S["BDO"]) * 1.5

def test_special_amount_is_0_1_base_salary():
    base_salary = 123456
    assert special_amount(base_salary) == base_salary * 0.1
