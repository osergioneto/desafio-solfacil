from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
def read_partners():
    return {"message": "parceiros"}