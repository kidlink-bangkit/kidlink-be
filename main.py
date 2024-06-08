from fastapi import FastAPI
import pandas as pd
from utils import preprocess_text, download_stopwords
import ssl
import nltk

ssl._create_default_https_context = ssl._create_unverified_context

download_stopwords()
app = FastAPI()


@app.get("/predict")
def predict():
    # add model in here
    model = None
    prediction = model.predict(preprocess_text("hai"))[0][0]
    class_label = "badword" if prediction >= 0.56 else "goodword"

    # integrate with firestore

    return {"Hello": "World"}








