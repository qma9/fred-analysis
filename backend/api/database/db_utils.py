from sqlalchemy.orm import sessionmaker, Session as _Session
from sqlalchemy import create_engine

from contextlib import contextmanager
from typing import Generator, Dict, List, Union

import os
import sys

# Add the root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from . import (
    Base,
    BaseSeries,
    BaseObservations,
    Series,
    Observations,
)

# Create the database engine, log SQL statements to console
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

# Create a session factory class
SessionFactory = sessionmaker(bind=engine, autocommit=False)


@contextmanager
def get_db() -> Generator[_Session, None, None]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    Base.metadata.create_all(engine)


def populate_series(series_data: List[Dict[str, str | int | float]]) -> None:
    with get_db() as session:
        for data in series_data:
            series_model = BaseSeries.model_validate(data)
            series = Series(**series_model.model_dump())
            session.add(series)
        session.commit()


def generate_observations(
    observation_data: List[Dict[str, str | int | float]]
) -> Generator[Observations, None, None]:
    for data in observation_data:
        observation_model = BaseObservations.model_validate(data)
        yield Observations(**observation_model.model_dump())


def populate_observations(observation_data: List[Dict[str, str | int | float]]) -> None:
    with get_db() as session:
        for observation in generate_observations(observation_data):
            session.add(observation)
        session.commit()


def get_gdp_per_capita() -> None:
    with get_db() as session:
        gdp = (
            session.query(Observations).filter(Observations.series_id == "GDPC1").all()
        )
        pop = session.query(Observations).filter(Observations.series_id == "POP").all()

        # Assuming series1 and series2 have the same dates and are sorted by date
        gdp_per_capita_series = []
        for gdp_obs, pop_obs in zip(gdp, pop):
            # Perform the division operation
            gdp_per_capita = (
                gdp_obs.value / pop_obs.value if pop_obs.value != 0 else None
            )

            # Create a new observation with the new series_id and value
            new_observation = Observations(
                series_id="GDPPERCAP",
                realtime_start=gdp_obs.realtime_start,
                realtime_end=gdp_obs.realtime_end,
                date=gdp_obs.date,
                value=gdp_per_capita,
            )

            # Add the new observation to the new series
            gdp_per_capita_series.append(new_observation)

        # Add the new series to the session
        session.add_all(gdp_per_capita_series)

        # Commit the session to save the changes to the database
        session.commit()
