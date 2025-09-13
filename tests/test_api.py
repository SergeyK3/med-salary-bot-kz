import pytest
pytestmark = pytest.mark.asyncio
from httpx import AsyncClient, ASGITransport
from src.api import app

@pytest.mark.asyncio
async def test_calc_endpoint_ok():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "role": "врач",
            "education": None,
            "experience_years": 11,
            "category": "первая",
            "eco_zone": None,
            "location": "город",
            "facility": "стационар",
            "senior_nurse": False,
            "hazard_profile": None,
            "is_surgery": True,
            "is_uchastok": False,
        }
        r = await client.post("/calc", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert abs(data["ets_coeff"] - 5.21) < 1e-9
        assert round(data["total_salary"], 2) > round(0, 2)
