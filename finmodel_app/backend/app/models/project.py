from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    real_estate_class = Column(String, nullable=False)
    location_link = Column(String)
    construction_period_months = Column(Integer, nullable=False)
    sales_period_months = Column(Integer, nullable=False)

    properties = relationship("Property", back_populates="project", cascade="all, delete-orphan")
    seasonalities = relationship("Seasonality", back_populates="project", cascade="all, delete-orphan")
    payment_methods = relationship("PaymentMethod", back_populates="project", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="project", cascade="all, delete-orphan")


class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    expense_category = Column(String, nullable=False)  # 'land_acquisition', 'construction', 'marketing', 'taxes'
    total_amount = Column(Float, nullable=False)
    distribution_type = Column(String, nullable=False)  # 'even', 'front_loaded', 'back_loaded', 'custom'
    start_month = Column(Integer, nullable=False)  # Месяц начала трат от старта проекта
    duration_months = Column(Integer, nullable=False)

    project = relationship("Project", back_populates="expenses")