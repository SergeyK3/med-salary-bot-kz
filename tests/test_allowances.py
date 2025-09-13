from src.calc.allowances import k1_amount
from src.utils.data_loader import load_settings

def test_k1_radiation_max_uses_mrp():
    S = load_settings()
    # Надбавка для radiation_max должна считаться от МРП
    assert k1_amount("radiation_max", float(S["MRP"])) == float(S["MRP"]) * 1.75