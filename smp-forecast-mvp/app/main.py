"""SMP 예측 MVP API.

실행:  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
문서:  http://localhost:8000/docs
"""
from __future__ import annotations

import datetime as dt
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query

from .forecaster import BaselineForecaster, load_history

_state: dict = {"model": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    _state["model"] = BaselineForecaster().fit(load_history())
    yield


app = FastAPI(title="SMP Forecast MVP", version="0.1.0", lifespan=lifespan)


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "smp-forecast-mvp"}


@app.post("/train")
def train() -> dict:
    df = load_history()
    _state["model"] = BaselineForecaster().fit(df)
    return {"trained": True, "rows": int(len(df))}


@app.get("/forecast")
def forecast(
    date: str | None = Query(default=None, description="YYYY-MM-DD (기본: 내일)"),
) -> dict:
    target = (
        dt.date.fromisoformat(date) if date else dt.date.today() + dt.timedelta(days=1)
    )
    model = _state["model"] or BaselineForecaster().fit(load_history())
    _state["model"] = model
    return {
        "date": target.isoformat(),
        "resolution": "1h",
        "unit": "KRW/kWh",
        "forecast": model.predict_day(target),
    }
