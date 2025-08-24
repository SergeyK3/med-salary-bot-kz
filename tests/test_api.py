from fastapi.testclient import TestClient
from src.api import app

def test_calc_endpoint_ok():
    client = TestClient(app)
    payload = {
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
    r = client.post("/calc", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert abs(data["ets_coeff"] - 5.21) < 1e-9
    assert data["total_salary"] > 0
