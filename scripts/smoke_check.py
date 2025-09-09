# scripts/smoke_test.py
from src.calc.base_oklad import get_ets_coeff
from src.main import calc_salary
import json

# ЕТС — три эталонные проверки
assert round(get_ets_coeff("врач", None, "первая", 11), 2) == 5.21
assert round(get_ets_coeff("сестра", "высшее", "первая", 3.5), 2) == 4.39
assert round(get_ets_coeff("сестра", "среднее", "нет", 8.5), 2) == 3.53

# Пробный полный расчёт
answers = {
  "role": "врач", "education": None, "experience_years": 11, "category": "первая",
  "eco_zone": "eco_crisis", "location": "село", "facility": "стационар",
  "senior_nurse": False, "hazard_profile": "xray", "is_surgery": True, "is_district": False
}
result = calc_salary(answers)
print(json.dumps(result, ensure_ascii=False, indent=2))
print("SMOKE TEST: OK")
