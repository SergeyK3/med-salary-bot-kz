"""
Поиск коэффициента ЕТС по группе (B2/B3/B4), категории и стажу.
Поддерживает два стиля вызова:
- get_ets_coeff(role, education, category, years)
- get_ets_coeff(group, category, years)
"""

from typing import Optional, Literal
import pandas as pd
from src.data_loaders import ets_df
from src.config import load_settings

CatName = Literal["высшая", "первая", "вторая", "нет", "без категории"]

def _group_by_role(role: str, education: Optional[str]) -> str:
    r = (role or "").strip().lower()
    if r.startswith("врач"):
        return "B2"
    # сестринская
    e = (education or "").strip().lower()
    if e.startswith("высш"):
        return "B3"
    return "B4"

def _cat_to_num(cat: str) -> int:
    c = (str(cat) or "").strip().lower()
    match c:
        case "1" | "высшая": return 1
        case "2" | "первая": return 2
        case "3" | "вторая": return 3
        case "4" | "нет" | "без категории": return 4
    raise ValueError(f"Неизвестная категория: {cat}")

def get_ets_coeff(a, b, c, d=None) -> float:
    """
    Вариант 1 (4 аргумента): (role, education, category, years)
    Вариант 2 (3 аргумента): (group, category, years)
    """
    if d is None:
        # старый стиль (group, category, years)
        group = str(a).strip().upper()   # ожидаем 'B2'/'B3'/'B4'
        category = _cat_to_num(b)
        years = float(c)
        role = None
    else:
        # новый стиль (role, education, category, years)
        role = a
        education = b
        category = _cat_to_num(c)
        years = float(d)
        group = _group_by_role(role, education)

    df: pd.DataFrame = ets_df()
    m = (
        (df["group"] == group) &
        (df["category"] == category) &
        (df["band_from"] <= years) &
        (years < df["band_to"])
    )
    hit = df.loc[m]
    if hit.empty:
        raise LookupError(f"Коэфф. ЕТС не найден: group={group}, cat={category}, years={years}")
    ets_coeff = float(hit.iloc[0]["coeff"])

    # --- ДОБАВЛЕНА ЛОГИКА ДОПОЛНИТЕЛЬНОГО КОЭФФИЦИЕНТА ---
    settings = load_settings()
    role_coeffs = settings.get("role_coefficients", {})
    # Для врача и медсестры берём коэффициент из settings.yml
    if role is not None:
        r = str(role).strip().lower()
        if r.startswith("врач"):
            extra_coeff = float(role_coeffs.get("врач", 1.0))
        elif r.startswith("медсестра"):
            extra_coeff = float(role_coeffs.get("медсестра", role_coeffs.get("сестра", 1.0)))
        else:
            extra_coeff = float(role_coeffs.get(r, 1.0))
        return ets_coeff * extra_coeff
    else:
        return ets_coeff

def get_ets_coeff_by_role(role, education, category, years) -> float:
    # обёртка старого имени на новую функцию
    return get_ets_coeff(role, education, category, years)