from fastapi import APIRouter, Request, HTTPException
import uuid
from typing import Dict, Any, Tuple, List

router = APIRouter()

# simple in-memory chat store (use Redis/DB in prod)
CHAT_STORE: Dict[Tuple[str, str], List[Dict[str, str]]] = {}

@router.post("/chat")
def chat(payload: Dict[str, Any], request: Request):

    model = payload.get("model")
    question = payload.get("question")
    session_id = payload.get("session_id") or str(uuid.uuid4())

    if model in request.app.state.llms:
        llm = request.app.state.llms[model]
    else: 
        raise TypeError(f"Not support {model}")

    # Load section chat history
    key = session_id
    history = CHAT_STORE.get(key, [])

    # Generate answer
    output = llm(question, history)
    facts = output['facts']
    answer = output['response']

    # Save history
    CHAT_STORE.setdefault(key, []).extend([
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ])

    return {
        "answer": answer,
        "session_id": session_id,
        "facts": facts,
        "model": model,
        "history": history,
    }
