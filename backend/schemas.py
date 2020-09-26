from datetime import datetime
from pydantic import BaseModel, validator


class HouseholdBase(BaseModel):
    serial_number: str
    brand: str = ''
    model: str = ''

    status: str = 'new'
    date_bought: datetime = datetime.now()

    @validator('serial_number', pre=True, always=True)
    def serial_number_not_empty(cls, val):
        if not val:
            raise ValueError('serial_number must contain a value')
        return val

    @validator('brand', pre=True, always=True)
    def brand_not_empty(cls, val):
        if not val:
            raise ValueError('brand must contain a value')
        return val

    @validator('model', pre=True, always=True)
    def model_not_empty(cls, val):
        if not val:
            raise ValueError('model must contain a value')
        return val

    @validator('status', pre=True, always=True)
    def status_is_allowed(cls, val):
        if val.lower() in ['new', 'rent']:  # TODO what should be there?
            return val

    @validator('date_bought', pre=True, always=True)
    def default_date_bought(cls, val, values):
        return val or values['created_at']


class HouseholdCreate(HouseholdBase):
    pass


class Household(HouseholdBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @validator('created_at', pre=True, always=True)
    def default_created_at(cls, val):
        return val or datetime.now()

    @validator('updated_at', pre=True, always=True)
    def default_updated_at(cls, val, values):
        return val or values['created_at']

    class Config:
        orm_mode = True
