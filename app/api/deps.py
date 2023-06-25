from app.crud.db.session import Base, engine, SessionLocal

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()