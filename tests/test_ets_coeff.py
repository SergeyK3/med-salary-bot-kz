from src.calc.base_oklad import get_ets_coeff
import math

def test_b2_cat2_11years():
    assert math.isclose(get_ets_coeff("B2", 2, 11), 5.21, rel_tol=1e-6)

def test_b3_cat2_4years():
    assert math.isclose(get_ets_coeff("B3", 2, 4), 4.39, rel_tol=1e-6)

def test_b4_cat4_8_5years():
    assert math.isclose(get_ets_coeff("B4", 4, 8.5), 3.53, rel_tol=1e-6)
