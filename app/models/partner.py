from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql import func
from app.crud.db.session import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String, index=True, unique=True)
    company_name = Column(String)
    trading_name = Column(String)
    telephone = Column(String)
    email = Column(String, unique=True)
    zip_code = Column(String)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None)