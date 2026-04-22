from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.database import Base


class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    property_type = Column(String, nullable=False)  # 'residential', 'commercial', 'storage', 'parking'
    total_area = Column(Float, nullable=False)
    total_units = Column(Integer, nullable=False)
    price_per_sqm = Column(Float, nullable=False)
    sales_start_date = Column(Date, nullable=False)

    project = relationship("Project", back_populates="properties")