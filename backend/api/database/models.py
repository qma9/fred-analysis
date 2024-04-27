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
    predictions = relationship("Predictions", back_populates="series")

    def __repr__(self):
        return f"<Series(id={self.id}, title={self.title})>"


class Observations(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True)
    series_id = Column(String, ForeignKey("series.id"))
    realtime_start = Column(Date)
    realtime_end = Column(Date)
    date = Column(Date)
    value = Column(Float, nullable=True)
    series = relationship("Series", back_populates="observations")

    def __repr__(self):
        return f"<Observations(series_id={self.series_id}, date={self.date}, value={self.value})>"
    

class Predictions(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True)
    series_id = Column(String, ForeignKey("series.id"))
    model = Column(String)
    date = Column(Date)
    value = Column(Float)
    series = relationship("Series", back_populates="predictions")
    
    def __repr__(self):
        return f"<Predictions(series_id={self.series_id}, model={self.model}, date={self.date}, value={self.value})>"
