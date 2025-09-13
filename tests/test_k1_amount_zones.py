from src.calc.allowances import k1_amount, zones_df

answers = {
    'role': 'врач',
    'education': None,
    'experience_years': 11,
    'category': 'первая',
    'eco_zone': None,
    'location': 'город',
    'facility': 'стационар',
    'senior_nurse': False,
    'hazard_profile': None,
    'is_surgery': True,
    'is_uchastok': False
}

BASE_OKLAD = 315328.69  # пример оклада
MRP = 3932  # актуальное значение из settings.yml

eco_zones = [
    "eco_catastrophe",
    "eco_crisis",
    "eco_precrisis",
    "radiation_extreme",
    "radiation_max",
    "radiation_high",
    "radiation_min",
    "social_benefit",
    None  # благополучная зона
]

print(f"Входные данные: {answers}")
print(f"Базовый оклад: {BASE_OKLAD}")
print("Надбавки:")

zdf = zones_df()
for zone_code in eco_zones:
    if zone_code is None:
        print("  k1 (eco_zone=None): 0.00 {нет надбавки}")
        continue
    row = zdf[zdf["code"] == zone_code].iloc[0]
    value = float(row["value"])
    calc_base = str(row["calc_base"]).upper()
    if calc_base == "DO":
        base_descr = f"{value} от должностного оклада"
        amount = value * BASE_OKLAD
    else:
        base_descr = f"{value} * MRP"
        amount = value * MRP
    print(f"  k1 ({zone_code}): {amount:.2f} {{{base_descr}}}")