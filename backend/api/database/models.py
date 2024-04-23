# models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
    Date,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


# Create the base class for the declarative class
Base = declarative_base()


class Series(Base):
    __tablename__ = "series"

    id = Column(String, primary_key=True)
    realtime_start = Column(Date)
    realtime_end = Column(Date)
    title = Column(String)
    observation_start = Column(Date)
    observation_end = Column(Date)
    frequency = Column(String)
    frequency_short = Column(String)
    units = Column(String)
    units_short = Column(String)
    seasonal_adjustment = Column(String)
    seasonal_adjustment_short = Column(String)
    last_updated = Column(DateTime)
    popularity = Column(Integer)
    notes = Column(String, nullable=True)
    is_transformed = Column(Boolean, default=False)
    observations = relationship("Observations", back_populates="series")

    def __repr__(self):
        return f"<Series(id={self.id}, title={self.title})>"


class Observations(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True)
    series_id = Column(String, ForeignKey("series.id"))
    realtime_start = Column(Date)
    realtime_end = Column(Date)
    date = Column(Date)
    value = Column(Float)
    is_prediction = Column(Boolean, default=False)
    series = relationship("Series", back_populates="observations")

    def __repr__(self):
        return f"<Observations(series_id={self.series_id}, date={self.date}, value={self.value})>"
