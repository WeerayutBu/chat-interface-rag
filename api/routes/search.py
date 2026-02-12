from fastapi import APIRouter, Depends
# from core.retriever import Retriever

router = APIRouter()

@router.get("/search")
def search(q: str):
    return {"Search": True, "q": q}