from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    serial_number = Column(String(255))
    brand = Column(String(255))
    model = Column(String(255))
    status = Column(String(255))
    date_bought = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint('serial_number', 'brand', 'model', name='_unique_household'),
    )
