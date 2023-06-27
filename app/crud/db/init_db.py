from sqlalchemy.orm import Session

from app import crud, schemas
from .session import engine
from app.crud.db.base import Base

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
