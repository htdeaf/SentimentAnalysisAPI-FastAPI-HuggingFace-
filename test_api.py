import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ✅ 1. Health check (GET /)
def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "Analyse de sentiment" in response.text

# ✅ 2. API JSON succès
def test_predict_success():
    payload = {"text": "I love this!"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["text"] == payload["text"]
    assert json_data["sentiment"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= json_data["confiance"] <= 1

# ✅ 3. API JSON erreur (texte vide)
def test_predict_empty_text():
    payload = {"text": ""}
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Texte vide ou invalide."
