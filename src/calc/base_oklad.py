"""
Модуль для поиска коэффициента ЕТС по группе (B2/B3/B4),
категории и стажу.
"""

def get_ets_coeff(role: str, education: str, category: str, years: int) -> float:
    """
    role: 'врач' | 'сестра'
    education: 'высшее' | 'среднее' (для сестер)
    category: 'высшая' | 'первая' | 'вторая' | 'нет'
    years: стаж в годах

    Возвращает коэффициент из таблицы ЕТС (будет загружаться из data/ets_coefficients.csv).
    """
    # TODO: реализовать загрузку CSV и поиск значения
    raise NotImplementedError
