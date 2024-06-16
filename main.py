from datetime import datetime, timedelta
from fastapi import FastAPI
import ssl
import nltk
from tensorflow.keras.models import load_model
from utils import preprocess_text, download_stopwords,send_mail
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from google.cloud import firestore
import os

ssl._create_default_https_context = ssl._create_unverified_context
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./kidlink-e61e421c3176.json"


db = firestore.Client()
nltk.download("punkt")
nltk.download("stopwords")
app = FastAPI()

def scheduled_job():
    send_email_parents()
    print(f"Job executed at {datetime.now()}")

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, CronTrigger(hour=8, minute=0)) 
scheduler.start()

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
    
@app.get("/send")
def send_email_parents():
    current_time = datetime.now()
    previous_day_8am = current_time - timedelta(days=1)
    users = db.collection("users").stream()
    chat_rooms = db.collection("chatRooms").stream()
    data = []
    for chat in chat_rooms:
        data.append(chat)

    for user in users:
        parent_email = user._data['parentEmail']
        username = user._data['name']
        child_email = user._data['email']
        unsafe_count = 0

        for chat in data:
            if(child_email in chat._data['participants']):
                messages = chat.reference.collection("messages").stream()
                for message in messages:
                    if message._data['censor'] == "UNSAFE" and message._data['senderId'] == user.id and message._data['timestamp'] < previous_day_8am:
                        unsafe_count+=1

        if unsafe_count > 0:
            send_mail(parent_email, unsafe_count, username, child_email)
        

    return "Sended all email successfully"






