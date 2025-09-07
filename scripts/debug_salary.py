from src.calc.totals import calc_total

answers = {...}  # тот же словарь
result = calc_total(answers)
print("Базовый оклад:", result["base_oklad"])
print("Итоговая сумма:", result["total_salary"])
