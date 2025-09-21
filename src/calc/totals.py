# coding: utf-8
from src.config import load_settings
from src.calc.base_oklad import get_ets_coeff
from src.calc.allowances import k3_amount
from src.calc.allowances import (
    calc_k1, calc_k2, calc_k3, calc_k4, calc_k5, calc_senior_nurse, special_conditions
)

def role_coeff(role: str, settings: dict) -> float:
    r = role.strip().lower()
    if r.startswith("врач"):
        return float(settings["role_coefficients"]["врач"])
    if r.startswith("сест") or r.startswith("медсестра"):
        return float(settings["role_coefficients"]["медсестра"])
    return float(settings["role_coefficients"]["младший"])


def calc_total(answers: dict) -> dict:
    settings = load_settings()
    exp = answers.get("experience_years")
    if exp is None:
        exp = 0
    elif isinstance(exp, dict):
        exp = exp.get("value", 0)
    ets = get_ets_coeff(
        answers["role"],
        answers.get("education"),
        answers["category"],
        float(exp),
    )
    role_mult = role_coeff(answers["role"], settings)
    BDO_val = float(settings["BDO"])

    # должностной оклад с учетом дополнительного коэффициента
    base_oklad_raw = BDO_val * ets * role_mult
    base_oklad = round(base_oklad_raw, 2)


    eco_zone = answers.get("eco_zone")
    if eco_zone is None:
        eco_zone = ""
    elif isinstance(eco_zone, dict):
        while isinstance(eco_zone, dict):
            eco_zone = eco_zone.get("value", "")
    if not isinstance(eco_zone, str):
        eco_zone = str(eco_zone)
    k1 = calc_k1(eco_zone, base_oklad)

    location = answers.get("location")
    if location is None:
        location = ""
    elif isinstance(location, dict):
        location = location.get("value", "")
    k2 = calc_k2(location, base_oklad)
    
    k3 = k3_amount(base_oklad)

    hazard_profile = answers.get("hazard_profile")
    if hazard_profile is None:
        hazard_profile = None
    elif isinstance(hazard_profile, dict):
        hazard_profile = hazard_profile.get("value", None)
    # Вредность (k4) считается от БДО (settings.yml)
    k4, k4_label, k4_value = calc_k4(hazard_profile, BDO_val)
    # Fallback: если ключ вредности не распознан (k4==0), но передано явное значение вредности
    try:
        hazard_value_param = answers.get("hazard_value")
        if (k4 is None or float(k4) == 0.0) and hazard_value_param is not None:
            hv = float(hazard_value_param)
            if hv > 0:
                # fallback тоже от БДО
                k4 = hv * BDO_val
                # Метка — используем то, что пришло как hazard_profile (скорее всего русское название отделения)
                k4_label = str(answers.get("hazard_profile") or "")
                k4_value = hv
    except Exception:
        pass

    facility = answers.get("facility", "")
    if facility is None:
        facility = ""
    elif isinstance(facility, dict):
        facility = facility.get("value", "")
    k5 = calc_k5(
        answers["role"],
        facility,
        bool(answers.get("is_surgery")),
        bool(answers.get("is_uchastok")),
        float(settings["BDO"])
    )
    # Неклиническое отделение стационара: доплата за психоэмоциональное напряжение не применяется
    clinical_dept = answers.get("clinical_dept")
    if str(facility).strip().lower() == "стационар" and str(clinical_dept or "").strip().lower() == "неклиническое":
        k5 = 0.0

    k_spec = special_conditions(base_oklad)

    # Округляем k4 до двух знаков для стабильного отображения
    try:
        k4 = round(float(k4), 2)
    except Exception:
        pass
    # итоговую сумму тоже округляем до двух знаков после запятой
    total_raw = base_oklad + k1 + k2 + k3 + k4 + k5 + k_spec
    total = round(total_raw, 2)

    # Маппинг для отображения категории
    category_map = {
        1: "высшая",
        2: "первая",
        3: "вторая",
        4: "без категории"
    }
    display_category = answers["category"]
    if isinstance(display_category, int):
        display_category = category_map.get(display_category, str(display_category))
    elif isinstance(display_category, str):
        # если вдруг строка-цифра
        try:
            display_category = category_map.get(int(display_category), display_category)
        except Exception:
            pass
    return {
        "ets_coeff": ets,
        "base_oklad": base_oklad,
        "allowances": {
            "k1": k1,
            "k2": k2,
            "k4": k4,
            "k4_label": k4_label,
            "k4_value": k4_value,
            "k5": k5,            
            "special": k_spec,
        },
        "total_salary": total,
        "display_category": display_category,
    }


# Совместимость со старым API (если где-то используется)
def total_amount(
    ets_coeff: float,
    role: str,
    k1: float,
    k2: float,
    k3: float,
    k4: float,
    k5: float,    
    kspec: float,
) -> float:
    settings = load_settings()
    # должностной оклад округляем до двух знаков после запятой
    base_oklad_raw = float(settings["BDO"]) * ets_coeff * role_coeff(role, settings)
    base_oklad = round(base_oklad_raw, 2)
    # итоговая сумма тоже округляется до двух знаков после запятой
    total_raw = base_oklad + k1 + k2 + k3 + k4 + k5 + kspec
    return round(total_raw, 2)