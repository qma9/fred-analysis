from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List

from .database import get_db, BaseObservations, Observations

router = APIRouter()


@router.get("/series/{series_id}", response_model=List[BaseObservations])
async def get_data(series_id: str) -> List[BaseObservations]:
    with get_db() as db:
        series = (
            db.query(Observations).filter(Observations.series_id == series_id).all()
        )
        if series is not None:
            return series
        else:
            raise HTTPException(status_code=404, detail="Series not found")
