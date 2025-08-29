import logging
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from transformers import pipeline

# --- Configuration logging ---
logging.basicConfig(
    level=logging.INFO,  # Niveau : DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# --- Application FastAPI ---
app = FastAPI(title="Sentiment Analysis API", version="1.0.0")
templates = Jinja2Templates(directory=".")

# Charger le modèle Hugging Face
logger.info("Chargement du modèle Hugging Face...")
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
logger.info("Modèle chargé avec succès ✅")

# ✅ Modèle Pydantic pour valider l'entrée JSON
class TextInput(BaseModel):
    text: str


# --- Interface HTML ---
@app.get("/", response_class=HTMLResponse)
def lire_texte(request: Request):
    logger.info("Page d'accueil appelée (GET /)")
    return templates.TemplateResponse(request, "test.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
def submit_text(request: Request, text: str = Form(...)):
    if not text.strip():
        logger.warning("Texte vide soumis via formulaire HTML.")
        return templates.TemplateResponse(
            request, "test.html", {"request": request, "result": {"error": "Texte vide"}}
        )

    result = sentiment_model(text)[0]

    # On enrichit le résultat avec le texte soumis
    final_result = {
        "text": text,
        "sentiment": result["label"],
        "confiance": round(result["score"], 3)
    }

    logger.info(f"Prédiction réussie via formulaire HTML: {final_result}")
    return templates.TemplateResponse(
        request, "test.html", {"request": request, "result": final_result}
    )



# --- API JSON ---
@app.post("/predict")
def predict(input_data: TextInput):
    text = input_data.text.strip()
    if not text:
        logger.error("Requête API reçue avec texte vide ❌")
        raise HTTPException(status_code=400, detail="Texte vide ou invalide.")

    result = sentiment_model(text)[0]
    logger.info(f"Prédiction réussie via API JSON: {result}")
    return {
        "text": text,
        "sentiment": result["label"],
        "confiance": round(result["score"], 3),
    }
