import time
from transformers import pipeline

# Chargement modèle Hugging Face
models = {
    "distilbert": "distilbert-base-uncased-finetuned-sst-2-english",
    "bert": "nlptown/bert-base-multilingual-uncased-sentiment"
}

texts = ["I love this!", "I hate this!"]

for name, model_id in models.items():
    print(f"\n🔹 Modèle: {name} ({model_id})")
    sentiment_model = pipeline("sentiment-analysis", model=model_id)
    
    for text in texts:
        start_time = time.time()
        result = sentiment_model(text)[0]
        end_time = time.time()
        print(f"Texte: '{text}' -> Sentiment: {result['label']} | Score: {round(result['score'],3)} | Temps: {end_time-start_time:.3f}s")
