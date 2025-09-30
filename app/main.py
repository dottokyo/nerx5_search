from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel
import spacy
import asyncio
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded

model_path = 'models/x5-ner'
nlp = spacy.load(model_path)

# limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class PredictRequest(BaseModel):
    input: str

@app.get("/")
def read_root():
    return {"message": "Hello, Railway!"}

@app.post("/api/predict")
# @limiter.limit("25/minute")
async def predict(request: PredictRequest, req: Request):
    print(f"Received request from {req.client.host}")
    try:
        doc = await asyncio.to.thread(nlp, request.input)
    except Exception as e:
        return {"error": str(e)}
    entities = []
    for ent in doc.ents:
        entities.append({
            "start_index": ent.start_char,
            "end_index": ent.end_char,
            "entity": ent.label_
        })
    return entities
