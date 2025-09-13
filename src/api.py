# coding: utf-8
from typing import Optional
import os
from importlib.metadata import version as _pkg_version, PackageNotFoundError

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.main import calc_salary
from src.config import load_settings
from src.data_loaders import ets_df, zones_df, risk_df

app = FastAPI(title="med-salary-bot-kz", version="0.1.0")


class Answers(BaseModel):
    role: str
    education: Optional[str] = None
    experience_years: float = Field(0, ge=0)
    category: Optional[str] = None
    eco_zone: Optional[str] = None
    location: Optional[str] = "город"
    facility: Optional[str] = None
    senior_nurse: bool = False
    hazard_profile: Optional[str] = None
    is_surgery: bool = False
    is_uchastok: bool = False


@app.get("/")
def root():
    return {"ok": True, "service": "med-salary-bot-kz"}


# --- Service endpoints: healthz / readyz / version ---

@app.get("/healthz")
def healthz():
    """Лёгкая проверка «жив ли процесс» (быстрый 200)."""
    return {"ok": True}


@app.get("/readyz")
def readyz():
    """
    Готов ли сервис принимать трафик:
    - читаются settings.yml
    - читаются CSV (ETS / zones / risk)
    """
    try:
        _ = load_settings()
        _ = ets_df().head(1)
        _ = zones_df().head(1)
        _ = risk_df().head(1)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/version")
def version():
    """Версия приложения и окружения (для отладки/деплоя)."""
    app_version = os.getenv("APP_VERSION", "dev")
    git_sha = os.getenv("GIT_SHA", "unknown")
    try:
        fastapi_ver = _pkg_version("fastapi")
    except PackageNotFoundError:
        fastapi_ver = None
    return {
        "service": "med-salary-bot-kz",
        "app": app_version,
        "commit": git_sha,
        "fastapi": fastapi_ver,
    }


@app.post("/calc")
def calc(a: Answers):
    """Рассчитать зарплату по входным данным."""
    return calc_salary(a.model_dump())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
