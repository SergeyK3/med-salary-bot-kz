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

def test_root_endpoint():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["service"] == "med-salary-bot-kz"

def test_healthz_endpoint():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True

def test_version_endpoint():
    client = TestClient(app)
    r = client.get("/version")
    assert r.status_code == 200
    data = r.json()
    assert data["service"] == "med-salary-bot-kz"
    assert "app" in data
    assert "commit" in data

def test_readyz_endpoint():
    client = TestClient(app)
    r = client.get("/readyz")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True

def test_calc_endpoint_nurse():
    client = TestClient(app)
    payload = {
        "role": "сестра",
        "education": None,
        "experience_years": 5,
        "category": "вторая",
        "eco_zone": None,
        "location": "село",
        "facility": "поликлиника",
        "is_head": False,
        "hazard_profile": None,
        "is_surgery": False,
        "is_district": True,
    }
    r = client.post("/calc", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total_salary"] > 0

def test_calc_endpoint_minimal():
    client = TestClient(app)
    payload = {
        "role": "врач",
        "category": "нет",  # Need valid category
    }
    r = client.post("/calc", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total_salary"] > 0

def test_calc_endpoint_invalid_role():
    client = TestClient(app)
    payload = {
        "role": "",
        "category": "нет",  # Need valid category
    }
    r = client.post("/calc", json=payload)
    # Should handle gracefully or return error
    assert r.status_code in [200, 400, 422]

def test_calc_endpoint_negative_experience():
    client = TestClient(app)
    payload = {
        "role": "врач",
        "experience_years": -1,
    }
    r = client.post("/calc", json=payload)
    # Should fail validation due to Field(ge=0) constraint
    assert r.status_code == 422

def test_calc_endpoint_large_experience():
    client = TestClient(app)
    payload = {
        "role": "врач",
        "experience_years": 50,
        "category": "высшая",
    }
    r = client.post("/calc", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total_salary"] > 0

def test_calc_endpoint_head_position():
    client = TestClient(app)
    payload = {
        "role": "врач",
        "experience_years": 15,
        "category": "высшая",
        "is_head": True,
        "facility": "стационар",
    }
    r = client.post("/calc", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total_salary"] > 0
    # Head position should add allowance
    assert "allowances" in data
    assert "k3" in data["allowances"]