# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le dossier de travail
WORKDIR /app

# Copier le fichier requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer PyTorch CPU (léger) + Transformers
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir transformers

# Copier tout le projet (app/, test.html, etc.)
COPY . .

# Exposer le port
EXPOSE 7860

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Lancer l'app FastAPI (main.py est dans app/)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
