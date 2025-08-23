from src.utils.data_io import read_ets, read_zones
import math

def test_ets_has_known_coeff():
    df = read_ets()
    row = df[(df["group"]=="B2") & (df["category"]==2) & (df["band_label"]=="10-13")].iloc[0]
    assert math.isclose(row["coeff"], 5.21, rel_tol=1e-6)

def test_zones_columns():
    z = read_zones()
    assert {"code","name","calc_base","value","notes"}.issubset(z.columns)
