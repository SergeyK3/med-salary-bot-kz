from src.calc.allowances import k1_amount, k4_amount, k5_amount, k6_amount, special_amount
from src.utils.data_loader import load_settings

def test_k1_eco_catastrophe_uses_bdo():
    S = load_settings()
    assert k1_amount("eco_catastrophe", float(S["BDO"])) == float(S["BDO"]) * 0.5

def test_k4_xray_from_bdo():
    S = load_settings()
    assert k4_amount("xray", float(S["BDO"])) == float(S["BDO"]) * 1.0  # рентген = 1.0 ДО

def test_k5_inpatient_surgery_doctor():
    S = load_settings()
    # Врач, стационар, хирургия → 1.5 БДО
    assert k5_amount("стационар", "врач", True, False, float(S["BDO"])) == float(S["BDO"]) * 1.5

def test_k5_inpatient_non_surgery_doctor():
    S = load_settings()
    # Врач, стационар, не хирургия → 0.8 БДО
    assert k5_amount("стационар", "врач", False, False, float(S["BDO"])) == float(S["BDO"]) * 0.8

def test_k5_outpatient_district_doctor():
    S = load_settings()
    # Врач, не стационар, участковый → 2.0 БДО
    assert k5_amount("поликлиника", "врач", False, True, float(S["BDO"])) == float(S["BDO"]) * 2.0

def test_k5_outpatient_non_district_doctor():
    S = load_settings()
    # Врач, не стационар, не участковый → 0 БДО
    assert k5_amount("поликлиника", "врач", False, False, float(S["BDO"])) == 0.0

def test_k5_inpatient_surgery_nurse():
    S = load_settings()
    # Медсестра, стационар, хирургия → 0.8 БДО
    assert k5_amount("стационар", "сестра", True, False, float(S["BDO"])) == float(S["BDO"]) * 0.8

def test_k5_inpatient_non_surgery_nurse():
    S = load_settings()
    # Медсестра, стационар, не хирургия → 0.4 БДО
    assert k5_amount("стационар", "сестра", False, False, float(S["BDO"])) == float(S["BDO"]) * 0.4

def test_k5_outpatient_district_nurse():
    S = load_settings()
    # Медсестра, не стационар, участковая → 1.5 БДО
    assert k5_amount("поликлиника", "сестра", False, True, float(S["BDO"])) == float(S["BDO"]) * 1.5

def test_k5_outpatient_non_district_nurse():
    S = load_settings()
    # Медсестра, не стационар, не участковая → 0 БДО
    assert k5_amount("поликлиника", "сестра", False, False, float(S["BDO"])) == 0.0

def test_special_amount_is_0_1_bdo():
    S = load_settings()
    assert special_amount(float(S["BDO"])) == float(S["BDO"]) * 0.1