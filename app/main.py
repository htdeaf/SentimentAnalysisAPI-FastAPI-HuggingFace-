from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")
templates = Jinja2Templates(directory=".")

# Charger le modèle Hugging Face
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# ✅ Modèle Pydantic pour valider l'entrée JSON
class TextInput(BaseModel):
    text: str


# --- Interface HTML ---
@app.get("/", response_class=HTMLResponse)
def lire_texte(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
def submit_text(request: Request, text: str = Form(...)):
    if not text.strip():
        return templates.TemplateResponse("test.html", {"request": request, "result": {"error": "Texte vide"}})

    result = sentiment_model(text)[0]
    return templates.TemplateResponse("test.html", {"request": request, "result": result})
# --- API JSON ---
@app.post("/predict")
def predict(input_data: TextInput):
    text = input_data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Texte vide ou invalide.")

    result = sentiment_model(text)[0]
    return {
        "text": text,
        "sentiment": result["label"],
        "confiance": round(result["score"], 3)
    }