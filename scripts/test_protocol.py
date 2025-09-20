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
    "category": 4,
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

print_stage("Расчёт ETS, role_mult, base_oklad", {
    "role": answers["role"],
    "education": answers["education"],
    "категория": result.get("display_category"),
    "experience_years": answers["experience_years"]
}, {
    "ETS coeff": result["ets_coeff"],
    "Role multiplier": result["base_oklad"] / (17697 * result["ets_coeff"])
})

print_stage("Надбавки", {}, result["allowances"])

print_stage("Итоговая зарплата", {}, {"total_salary": result["total_salary"]})

print("\n--- Протокол завершён ---")
