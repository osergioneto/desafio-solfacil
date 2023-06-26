from fastapi import FastAPI
from app.api.endpoints import partners
from app.crud.db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(partners.router)