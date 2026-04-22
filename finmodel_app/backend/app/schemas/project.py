from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import date


class PropertyBase(BaseModel):
    property_type: str
    total_area: float = Field(..., gt=0)
    total_units: int = Field(..., gt=0)
    price_per_sqm: float = Field(..., gt=0)
    sales_start_date: date


class SeasonalityBase(BaseModel):
    month_number: int = Field(..., ge=1, le=12)
    coefficient: float = Field(..., ge=0.1, le=2.0)


class PaymentMethodBase(BaseModel):
    method_type: str
    share_percentage: float = Field(..., gt=0, le=100)
    installment_months: Optional[int] = None


class ProjectCreate(BaseModel):
    real_estate_class: str
    location_link: Optional[HttpUrl] = None
    construction_period_months: int = Field(..., gt=0)
    sales_period_months: int = Field(..., gt=0)
    properties: List[PropertyBase]
    seasonalities: List[SeasonalityBase]
    payment_methods: List[PaymentMethodBase]


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True