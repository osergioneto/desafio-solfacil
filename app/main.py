from fastapi import FastAPI
from api.endpoints import partners

app = FastAPI()

app.include_router(partners.router)