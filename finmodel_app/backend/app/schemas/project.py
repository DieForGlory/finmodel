from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import date

class PropertyBase(BaseModel):
    property_type: str
    total_area: float = Field(..., ge=0)
    total_units: int = Field(..., ge=0)
    price_per_sqm: float = Field(..., ge=0)
    sales_start_date: date
    yearly_sales_paces: List[float] = [] # Массив процентов по годам (напр. [30, 60, 10])

class SeasonalityBase(BaseModel):
    month_number: int = Field(..., ge=1, le=12)
    coefficient: float = Field(..., ge=0.1, le=2.0)

class PaymentMethodBase(BaseModel):
    method_type: str
    share_percentage: float = Field(..., ge=0, le=100)
    installment_months: Optional[int] = None
    installment_type: Optional[str] = None

class ExpenseBase(BaseModel):
    expense_category: str
    total_amount: float = Field(..., ge=0)
    distribution_type: str
    start_month: int = Field(..., ge=0)
    duration_months: int = Field(..., gt=0)

class ProjectCreate(BaseModel):
    real_estate_class: str
    location_link: Optional[HttpUrl] = None
    construction_period_months: int = Field(..., gt=0)
    sales_period_months: int = Field(..., gt=0)
    properties: List[PropertyBase]
    seasonalities: List[SeasonalityBase]
    payment_methods: List[PaymentMethodBase]
    expenses: List[ExpenseBase] = []

class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True