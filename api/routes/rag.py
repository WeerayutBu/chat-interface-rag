from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/retrieve")
def search(q: str, request: Request):
    retriever = request.app.state.retriever
    answer = retriever(q)
    return {"a": answer}
