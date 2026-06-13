"""SMP 데이터 로딩 + 베이스라인 예측기.

MVP 목적: '바로 실행되는' 최소 동작.
- data/smp_history.csv 가 있으면 사용, 없으면 합성 데이터로 대체.
- 베이스라인 = 요일×시간대 평균. (TODO: XGBoost/LightGBM 으로 교체)
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "smp_history.csv"


def load_history() -> pd.DataFrame:
    """SMP 이력 로드. CSV 스키마: datetime(ISO), smp(float)."""
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH, parse_dates=["datetime"])
    return _synthetic_history()


def _synthetic_history(days: int = 365) -> pd.DataFrame:
    """KPX 실데이터 연동 전, 실행 확인용 합성 SMP(원/kWh)."""
    end = pd.Timestamp.now().normalize()
    start = end - pd.Timedelta(days=days)
    idx = pd.date_range(start, end, freq="h", inclusive="left")
    hour = idx.hour.to_numpy()
    dow = idx.dayofweek.to_numpy()
    daily = 30 * np.sin((hour - 6) / 24 * 2 * np.pi) + 110  # 낮 고가 / 새벽 저가
    weekly = np.where(dow >= 5, -10, 0)                     # 주말 소폭 하락
    noise = np.random.default_rng(42).normal(0, 6, len(idx))
    smp = np.clip(daily + weekly + noise, 40, None)
    return pd.DataFrame({"datetime": idx, "smp": smp})


class BaselineForecaster:
    """요일×시간대 평균 기반 베이스라인 예측기."""

    def __init__(self) -> None:
        self.table: pd.Series | None = None
        self.global_mean: float | None = None

    def fit(self, df: pd.DataFrame) -> "BaselineForecaster":
        d = df.copy()
        d["hour"] = d["datetime"].dt.hour
        d["dow"] = d["datetime"].dt.dayofweek
        self.table = d.groupby(["dow", "hour"])["smp"].mean()
        self.global_mean = float(d["smp"].mean())
        return self

    def predict_day(self, target: dt.date) -> list[dict]:
        out: list[dict] = []
        for h in range(24):
            try:
                val = float(self.table.loc[(target.weekday(), h)])  # type: ignore[union-attr]
            except (KeyError, AttributeError, TypeError):
                val = self.global_mean or 0.0
            out.append(
                {
                    "datetime": f"{target.isoformat()}T{h:02d}:00:00",
                    "hour": h,
                    "smp_forecast": round(val, 2),
                }
            )
        return out
