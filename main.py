from fastapi import FastAPI
import pandas as pd
import ssl
import nltk
from tensorflow.keras.models import load_model
from utils import preprocess_text, download_stopwords

ssl._create_default_https_context = ssl._create_unverified_context

download_stopwords()
app = FastAPI()


@app.get("/predict")
def predict(text):
    try:
        model = load_model("model.h5")
        prediction = model.predict(preprocess_text(text))[0][0]
        class_label = "badword" if prediction >= 0.56 else "goodword"
        return {"class_label": class_label}
    except:
        return {"class_label": "error"}







