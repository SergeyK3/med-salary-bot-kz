# src/calc/base_oklad.py
from __future__ import annotations
from typing import Literal
from ..utils.data_loader import load_ets_table

Role = Literal["врач", "сестра"]

__all__ = ["get_ets_coeff", "get_ets_coeff_by_role", "role_to_group", "category_to_num"]


def role_to_group(role: Role, education: str | None = None) -> str:
    """
    'врач'  -> B2
    'сестра' + высшее   -> B3
    'сестра' + среднее  -> B4
    """
    r = (role or "").strip().lower()
    if r.startswith("врач"):
        return "B2"
    if r.startswith("сест"):
        e = (education or "").strip().lower()
        return "B3" if e.startswith("выс") else "B4"
    raise ValueError("role должен быть 'врач' или 'сестра'")


def category_to_num(category: int | str | None) -> int:
    """
    'высшая' -> 1, 'первая' -> 2, 'вторая' -> 3, 'нет' -> 4.
    Поддерживает варианты: '1', '1-я', 'без категории', 'none' и т.п.
    """
    if isinstance(category, int) and 1 <= category <= 4:
        return category
    c = (str(category or "")).strip().lower()
    mapping = {
        "высшая": 1, "высш.": 1, "высшая категория": 1, "highest": 1,
        "первая": 2, "1": 2, "1-я": 2, "1я": 2,
        "вторая": 3, "2": 3, "2-я": 3, "2я": 3,
        "нет": 4, "без категории": 4, "0": 4, "none": 4, "н/к": 4,
        "третья": 4,  # на всякий случай маппим в 'нет'
    }
    return mapping.get(c, 4)


def get_ets_coeff(group: str, category: int, years: float) -> float:
    """
    Коэффициент ЕТС по группе (B2/B3/B4), категории (1..4) и стажу (годы).
    Интервал: band_from <= years < band_to (для '>25' band_to=999).
    """
    g = str(group).upper().strip()
    cat = int(category)
    y = max(0.0, float(years))

    df = load_ets_table()  # DataFrame
    d = df[(df["group"] == g) & (df["category"] == cat)]
    if d.empty:
        raise ValueError(f"Не найдена группа/категория: {g}/{cat}")

    hit = d[(d["band_from"] <= y) & (y < d["band_to"])]
    if hit.empty:
        # подстраховка для граничных/аномальных значений
        hit = d[d["band_from"] == d["band_from"].max()]
    if hit.empty:
        raise ValueError(f"Не найден коридор стажа для {g}/{cat}, years={y}")

    return float(hit.iloc[0]["coeff"])


def get_ets_coeff_by_role(
    role: Role,
    education: str | None,
    category: str | int | None,   # ← добавили None
    years: float
) -> float:
    g = role_to_group(role, education)
    c = category_to_num(category)
    return get_ets_coeff(g, c, years)

