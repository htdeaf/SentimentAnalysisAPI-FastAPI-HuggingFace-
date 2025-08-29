# gradio_app.py
import gradio as gr
from main import sentiment_model # tu importes ton pipeline depuis FastAPI
def analyze_text(text):
    if not text.strip():
        return {"error": "Le texte est vide"}
    result = sentiment_model(text)[0]   # <- ATTENTION: sentiment_model(text) renvoie une liste
    return {
        "input": text,
        "sentiment": result["label"],
        "score": round(result["score"], 3)
    }

iface = gr.Interface(
    fn=analyze_text,
    inputs=gr.Textbox(lines=6, placeholder="Écris ton texte ici..."),
    outputs="json",
    title="Analyse de Sentiment",
    description="Saisis un texte et obtiens le sentiment et le score de confiance"
)

if __name__ == "__main__":
    # ⚠️ NE PAS forcer port ni server_name sous Windows
    iface.launch(share=True)  
