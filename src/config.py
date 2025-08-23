from __future__ import annotations
from pathlib import Path
import os
import yaml

# Кэш, чтобы не читать файл при каждом вызове
_settings_cache: dict | None = None

def project_root() -> Path:
    """
    Корень репозитория (папка, где лежат README.md/LICENSE).
    Берём из расположения текущего файла: <root>/src/config.py → <root>
    """
    return Path(__file__).resolve().parent.parent

def settings_path() -> Path:
    """
    Путь к settings.yml. Можно переопределить через переменную окружения
    SETTINGS_PATH, иначе берём <root>/data/settings.yml
    """
    env = os.getenv("SETTINGS_PATH")
    return Path(env) if env else project_root() / "data" / "settings.yml"

def load_settings(force_reload: bool = False) -> dict:
    """
    Читает YAML с параметрами (БДО, МРП, коэффициенты и т.д.).
    Использует кэш до перезагрузки (force_reload=True).
    """
    global _settings_cache
    if _settings_cache is not None and not force_reload:
        return _settings_cache

    sp = settings_path()
    if not sp.exists():
        raise FileNotFoundError(
            f"Не найден файл настроек: {sp}. "
            "Создайте data/settings.yml (или укажите SETTINGS_PATH)."
        )
    with open(sp, "r", encoding="utf-8") as f:
        _settings_cache = yaml.safe_load(f) or {}
    return _settings_cache
