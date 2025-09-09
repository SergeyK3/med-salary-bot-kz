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

def test_special_amount_is_0_1_bdo():
    S = load_settings()
    assert special_amount() == float(S["BDO"]) * 0.1

def test_k5_inpatient_therapy_doctor():
    """Test therapy doctor in inpatient setting"""
    S = load_settings()
    assert k5_amount("стационар", "врач", False) == float(S["BDO"]) * 0.8

def test_k5_inpatient_surgery_nurse():
    """Test surgery nurse in inpatient setting"""
    S = load_settings()
    assert k5_amount("стационар", "сестра", True) == float(S["BDO"]) * 0.8

def test_k5_inpatient_therapy_nurse():
    """Test therapy nurse in inpatient setting"""
    S = load_settings()
    assert k5_amount("стационар", "сестра", False) == float(S["BDO"]) * 0.4

def test_k6_district_doctor():
    """Test district doctor allowance"""
    S = load_settings()
    assert k6_amount(True, "врач") == float(S["BDO"]) * 2.0

def test_k6_non_district():
    """Test non-district worker has no allowance"""
    assert k6_amount(False, "врач") == 0
    assert k6_amount(False, "сестра") == 0
