from src.calc.base_oklad import get_ets_coeff

def test_b3_cat1_years_4():
    assert abs(get_ets_coeff("сестра", "высшее", "первая", 4) - 4.39) < 1e-9

def test_b4_no_cat_years_8_5():
    assert abs(get_ets_coeff("сестра", "среднее", "нет", 8.5) - 3.53) < 1e-9

def test_b2_cat2_years_11():
    assert abs(get_ets_coeff("врач", None, "первая", 11) - 5.21) < 1e-9
