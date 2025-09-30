from fastapi import FastAPI
from pydantic import BaseModel
import spacy
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import streamlit


nlp = spacy.load("x5-ner")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class PredictRequest(BaseModel):
    input: str

class Render(BaseModel):
    pass

@app.get("/")
def render(request: Render):
    return streamlit hello

@app.post("/api/predict")
@limiter.limit("25/minute")
async def predict(request: PredictRequest):
    doc = nlp(request.input)
    entities = []
    for ent in doc.ents:
        entities.append({
            "start_index": ent.start_char,
            "end_index": ent.end_char,
            "entity": ent.label_
        })
    return entities
