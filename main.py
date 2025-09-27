from fastapi import FastAPI
from pydantic import BaseModel
import spacy

nlp = spacy.load("x5-ner")

app = FastAPI()

class PredictRequest(BaseModel):
    input: str

@app.post("/api/predict")
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
