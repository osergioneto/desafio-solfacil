from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class Partner(BaseModel):
    id: UUID
    cnpj: str
    company_name: str
    trading_name: str
    telephone: str
    email: str
    zip_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True