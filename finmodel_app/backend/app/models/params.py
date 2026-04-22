from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Seasonality(Base):
    __tablename__ = 'seasonality'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    month_number = Column(Integer, nullable=False)
    coefficient = Column(Float, nullable=False)

    project = relationship("Project", back_populates="seasonalities")


class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    method_type = Column(String, nullable=False)  # '100_percent', 'mortgage', 'installment'
    share_percentage = Column(Float, nullable=False)
    installment_months = Column(Integer, nullable=True)

    project = relationship("Project", back_populates="payment_methods")