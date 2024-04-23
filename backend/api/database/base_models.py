# base_models.py
from pydantic import BaseModel, validator
from dateutil.parser import parse

from datetime import datetime, date
from typing import Optional


class BaseSeries(BaseModel):
    id: str
    realtime_start: date
    realtime_end: date
    title: str
    observation_start: date
    observation_end: date
    frequency: str
    frequency_short: str
    units: str
    units_short: str
    seasonal_adjustment: str
    seasonal_adjustment_short: str
    last_updated: datetime
    popularity: int
    notes: Optional[str] = None
    is_transformed: bool = False


class BaseObservations(BaseModel):
    series_id: str
    realtime_start: date
    realtime_end: date
    date: date
    value: Optional[float]
    is_prediction: Optional[bool] = False
