from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from typing import List

from .database import (
    get_db,
    BaseObservations,
    BasePredictions,
    Observations,
    Predictions,
)

router = APIRouter()


@router.get("/series/{series_id}", response_model=List[BaseObservations])
async def get_observations(series_id: str) -> List[BaseObservations]:
    with get_db() as session:
        try:
            series = (
                session.query(Observations)
                .filter(Observations.series_id == series_id)
                .all()
            )
            if series:
                return series
            else:
                raise HTTPException(status_code=404, detail="Series not found")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error") from e


@router.get("/predictions/{series_id}/{model}", response_model=List[BasePredictions])
async def get_predictions(series_id: str, model: str) -> List[BasePredictions]:
    with get_db() as session:
        try:
            series = (
                session.query(Predictions)
                .filter(Predictions.series_id == series_id, Predictions.model == model)
                .all()
            )
            if series:
                return series
            else:
                raise HTTPException(status_code=404, detail="Series not found")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error") from e
