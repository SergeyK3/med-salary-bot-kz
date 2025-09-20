import sys
from src.calc.totals import calc_total

def print_stage(stage, inputs, outputs):
    print(f"\n=== {stage} ===")
    print("Входные данные:")
    category_map = {
        1: "высшая",
        2: "первая",
        3: "вторая",
        4: "без категории"
    }
    for k, v in inputs.items():
        if k == "clinical_dept" and answers.get("facility") == "поликлиника":
            continue
        if k == "category" or k == "категория":
            try:
                v = category_map.get(int(v), v)
            except Exception:
                pass
        print(f"  {k}: {v}")
    print("Выходные данные:")
    for k, v in outputs.items():
        if k == "special":
            v = round(v, 2)
        print(f"  {k}: {v}")

# Пример параметров (можно заменить на любые)
answers = {
    "role": "медсестра",
    "education": "среднее",
    "category": 2,  # первая категория
    "experience_years": 11,
    "eco_zone": "нет",
    "location": "город",
    "facility": "поликлиника",
    "clinical_dept": "неклиническое",
    "hazard_profile": None,
    "is_surgery": False,
    "is_uchastok": True,
}

print_stage("Исходные параметры", answers, {})

result = calc_total(answers)


print(f"\nДолжностной оклад: {result['base_oklad']} KZT (ETS coeff: {result['ets_coeff']} Role multiplier: 2.34)")

allowances = result["allowances"]
allowance_names = {
    "k1": "Экологическая зона",
    "k2": "Сельская местность",
    "k4": "Вредные условия",
    "k4_label": "k4_label",
    "k4_value": "k4_value",
}
for k in ["k1", "k2", "k4", "k4_label", "k4_value"]:
    if k in allowances:
        print(f"{allowance_names.get(k, k)}: {allowances[k]}")
print(f"Психоэмоц напряжение: {allowances.get('k5', 0.0)}")
print(f"Особые условия труда: {round(allowances.get('special', 0.0), 2)}")

print(f"\nИтоговая зарплата: {result['total_salary']}")
print("\n--- Протокол завершён ---")
