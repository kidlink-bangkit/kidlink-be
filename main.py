from fastapi import FastAPI
import pandas as pd
import ssl
import nltk
from tensorflow.keras.models import load_model
from utils import preprocess_text, download_stopwords

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download("punkt")
nltk.download("stopwords")
app = FastAPI()

from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request:TextRequest):
    try:
        model = load_model("model_capstone_2.h5")
        prediction = model.predict(preprocess_text(request.text))[0][0]
        class_label = "badword" if prediction >= 0.982 else "goodword"
        return {"class_label": class_label}
    except Exception as e:
        print(e)
        return {"class_label": "error"}







