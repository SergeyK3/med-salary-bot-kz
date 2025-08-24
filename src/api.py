# coding: utf-8
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.main import calc_salary

app = FastAPI(title="med-salary-bot-kz", version="0.1.0")

class Answers(BaseModel):
    role: str
    education: Optional[str] = None
    experience_years: float = Field(0, ge=0)
    category: Optional[str] = None
    eco_zone: Optional[str] = None
    location: Optional[str] = "город"
    facility: Optional[str] = None
    is_head: bool = False
    hazard_profile: Optional[str] = None
    is_surgery: bool = False
    is_district: bool = False

@app.get("/")
def root():
    return {"ok": True, "service": "med-salary-bot-kz"}

@app.post("/calc")
def calc(a: Answers):
    """Рассчитать зарплату по входным данным."""
    return calc_salary(a.model_dump())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
