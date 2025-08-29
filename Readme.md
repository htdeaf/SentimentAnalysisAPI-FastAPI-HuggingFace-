
---

# 📊 Sentiment Analysis API

## 📖 Description

Ce projet propose une **API REST de détection de sentiment** basée sur les modèles **Hugging Face Transformers**.
Elle expose un endpoint permettant d’analyser un texte et de retourner :

* le **sentiment** prédit
* le **score de confiance** associé

L’application est conçue pour être :
✔️ **Exécutable localement** avec Uvicorn
✔️ **Conteneurisée avec Docker**
✔️ **Déployable sur Hugging Face Spaces**
✔️ Fournie avec une **mini interface HTML** et une **UI Gradio** en option

---

## 📂 Arborescence du projet

```
.
├── app/
│   ├── main.py          # Application FastAPI
├── static/
│   └── test.html       # Mini interface HTML
├── tests/
│   └── test_api.py      # Tests unitaires
├── requirements.txt     # Dépendances Python
├── Dockerfile           # Conteneurisation
├── gradio_app.py        # Interface Gradio (optionnelle)
└── README.md            # Documentation
```

---

## ⚙️ Installation & Lancement

### 🔹 Exécution locale (sans Docker)

```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

➡️ Accéder à l’API : [http://localhost:7860](http://localhost:7860)
➡️ Documentation interactive : [http://localhost:7860/docs](http://localhost:7860/docs)

---

### 🔹 Exécution avec Docker

Un `Dockerfile` est fourni pour faciliter le déploiement.

#### Construire l’image :

```bash
docker build -t sentiment-api .
```

#### Lancer le conteneur :

```bash
docker run -p 7860:7860 sentiment-api
```

➡️ L’API sera accessible sur [http://localhost:7860](http://localhost:7860).

---

## 🚀 Utilisation de l’API

### Endpoint principal

**POST /predict**

#### Exemple de requête :

```bash
curl -X POST "http://localhost:7860/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this project!"}'
```

#### Exemple de réponse :

```json
{
  "input": "I love this project!",
  "sentiment": "POSITIVE",
  "score": 0.999
}
```

#### Gestion des erreurs :

* Texte vide → `{"error": "Texte vide ou invalide"}`
* Format JSON incorrect → `{"error": "Format JSON invalide"}`

---

## 🖥️ Interfaces de test

### 🔹 Interface HTML (statique)

Accessible via [http://localhost:7860/static/index.html](http://localhost:7860/static/index.html)

* Champ texte
* Bouton d’envoi
* Résultat affiché en JSON

### 🔹 Interface Gradio (optionnelle)

Lancer :

```bash
python gradio_app.py
```

➡️ Une interface interactive sera disponible sur [http://localhost:7860](http://localhost:7860).

---

## 🧪 Tests & Benchmark

### 🔹 Tests unitaires

Exécuter avec **pytest** :

```bash
pytest tests/test_api.py
```

Exemple de résultats :

```
collected 3 items

tests/test_api.py ...      [100%]
```

### 🔹 Mini-benchmark (latence + justesse)

Deux modèles testés :

* **DistilBERT** : `distilbert-base-uncased-finetuned-sst-2-english`
* **BERT Multilingue** : `nlptown/bert-base-multilingual-uncased-sentiment`

| Texte        | Modèle           | Prédiction | Score | Latence (s) |
| ------------ | ---------------- | ---------- | ----- | ----------- |
| I love this! | DistilBERT       | POSITIVE   | 1.0   | 0.28        |
| I hate this! | DistilBERT       | NEGATIVE   | 1.0   | 0.03        |
| I love this! | BERT Multilingue | 5 stars    | 0.92  | 0.08        |
| I hate this! | BERT Multilingue | 1 star     | 0.88  | 0.05        |

---

## 🌍 Déploiement

### 🔹 Hugging Face Spaces (avec Docker)

* Compatible avec **Docker Spaces**
* Port exposé : **7860** (modifiable via `$PORT`)
* Premier chargement gère automatiquement le **téléchargement du modèle**

Exemple :

```dockerfile
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
```

---

## ✅ Checklist des fonctionnalités

* [x] API REST avec FastAPI
* [x] Endpoint `/predict` (POST)
* [x] Documentation Swagger `/docs`
* [x] Gestion des erreurs explicites
* [x] Mini-interface HTML
* [x] Interface Gradio optionnelle
* [x] Dockerfile fonctionnel
* [x] Tests unitaires (≥ 3 cas)
* [x] Mini-benchmark comparatif

---

✍️ **Auteur :** Salma Rehmi

---

