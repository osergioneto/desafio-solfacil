from sqlalchemy import Column, DateTime, UUID, String
from sqlalchemy.sql import func
from ..crud.db.base import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(UUID, primary_key=True, index=True)
    cnpj = Column(String, index=True, unique=True)
    company_name = Column(String)
    trading_name = Column(String)
    telephone = Column(String)
    email = Column(String, unique=True)
    zip_code = Column(String)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None)