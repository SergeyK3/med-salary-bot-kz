# src/calc/base_oklad.py
from __future__ import annotations
from typing import Literal
from ..utils.data_loader import load_ets_table

Role = Literal["врач", "сестра"]

__all__ = ["get_ets_coeff", "role_to_group", "category_to_num"]

def get_ets_coeff(group: str, category: int, years: float) -> float:
    """
    Возвращает коэффициент ЕТС по группе (B2/B3/B4), категории (1..4) и стажу (годы).
    Правило интервала: band_from <= years < band_to; для '>25' у нас band_to=999.
    """
    g = str(group).upper().strip()
    try:
        cat = int(category)
    except Exception as e:
        raise ValueError(f"Некорректная категория: {category}") from e

    df = load_ets_table()
    # фильтр по группе и категории
    d = df[(df["group"] == g) & (df["category"] == cat)]
    if d.empty:
        raise ValueError(f"Не найдена группа/категория: {g}/{cat}")

    # фильтр по стажу (включая нижнюю, исключая верхнюю границу)
    m = d[(d["band_from"] <= years) & (years < d["band_to"])]
    if m.empty:
        # на всякий случай для граничных значений берём максимальный коридор
        m = d[d["band_from"] == d["band_from"].max()]
    if m.empty:
        raise ValueError(f"Не найден коридор стажа для {g}/{cat}, years={years}")

    return float(m.iloc[0]["coeff"])

def role_to_group(role: str, education: str | None) -> str:
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

def category_to_num(category: str) -> int:
    """
    'высшая' -> 1, 'первая' -> 2, 'вторая' -> 3, 'нет' -> 4.
    Поддерживает варианты: '1', '1-я', 'без категории', 'none' и т.п.
    """
    c = (category or "").strip().lower()
    mapping = {
        "высшая": 1, "высш.": 1, "высшая категория": 1, "highest": 1,
        "первая": 2, "1": 2, "1-я": 2, "1я": 2,
        "вторая": 3, "2": 3, "2-я": 3, "2я": 3,
        "нет": 4, "без категории": 4, "0": 4, "none": 4, "н/к": 4,
        "третья": 4,  # на всякий случай маппим в 'нет'
    }
    return mapping.get(c, 4)

def _band_match(years: float, frm: float, to: float) -> bool:
    """
    Интервал считается [from, to); для '>25' в таблице to=999.
    Отрицательный стаж приравниваем к 0.
    """
    y = max(0.0, float(years))
    return (y >= float(frm)) and (y < float(to))

def get_ets_coeff(
    role: Role,
    education: str | None,
    category: str,
    years: float,
) -> float:
    """
    Вернёт коэффициент ЕТС из data/ets_coefficients.csv.

    Пример:
        >>> get_ets_coeff("врач", None, "первая", 11)
        5.21
        >>> get_ets_coeff("сестра", "высшее", "первая", 3.5)
        4.39
        >>> get_ets_coeff("сестра", "среднее", "нет", 8.5)
        3.53
    """
    group = role_to_group(role, education)
    cat = category_to_num(category)

    for row in load_ets_table():
        if row["group"] == group and row["category"] == cat:
            if _band_match(years, row["band_from"], row["band_to"]):
                return float(row["coeff"])

    raise ValueError(
        f"Не найден коэффициент ЕТС для group={group}, category={cat}, years={years}"
    )
