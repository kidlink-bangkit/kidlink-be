
import re
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd
import requests
import json
import csv
from io import StringIO
import pickle
import os
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def get_html(unsafe_words, username, child_email):
    unsafe_words_text = "unsafe word" if unsafe_words == 1 else "unsafe words"

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pemberitahuan: Kata-kata Tidak Aman Terdeteksi</title>
    <style>
        .highlight {{ color: red; }}
    </style>
</head>
<body>
    <p>Kami berharap anda mendapatkan pesan ini dengan baik. Kami ingin memberitahukan bahwa sistem pemantauan kami telah mendeteksi penggunaan kata-kata tidak aman oleh anak Anda dengan username {username} dan email {child_email}. Ada { "satu" if unsafe_words == 1 else ""} <span class="highlight">{unsafe_words} {unsafe_words_text}</span>.</p>
</body>
</html>
"""



def preprocess_sentence(data):
    data = re.sub(r"(?:\@|https?\://)\S+", "", data)
    data = re.sub(r"http\S+", "", data)
    data = re.sub(r"<[^>]+>", "", data, flags=re.IGNORECASE)
    data = re.sub('\n', '', data)
    data = re.sub('RT', '', data)
    data = re.sub("[^a-zA-Z^']", " ", data)
    data = re.sub(" {2,}", " ", data)
    data = data.strip()
    data = re.sub(r'\s+', ' ', data)
    data = data.lower()
    return data

# Remove slang words
def remove_slang(data):
    slang_dict = get_slang_dict()
    words = data.split()  # Split string into list of words
    for i, word in enumerate(words):
        words[i] = slang_dict.get(word, word)  # Replace slang with actual word if exists
    return ' '.join(words)  # Join words back into string

def remove_stop_words(data):
    stop_words = set(stopwords.words('indonesian'))
    words = data.split()  # Split string into list of words
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)  # Join words back into string

def preprocess_text(sentence):
    max_len = 100
    tokenizer = load_pickle("tokenizer_2.pickle")
    processed_sentence = preprocess_sentence(sentence)
    tokenized_sentence = nltk.word_tokenize(processed_sentence)
    stemmed_sentence = ' '.join(stemming(tokenized_sentence))
    rmvSlang_sentence = remove_slang(stemmed_sentence)
    rmvStopWords_sentence = remove_stop_words(rmvSlang_sentence)
    sequence = tokenizer.texts_to_sequences([rmvStopWords_sentence])
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
    return padded_sequence



def stemming(data):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    return [stemmer.stem(sentence) for sentence in data]

def load_pickle(pickle_file):
    try:
        with open(pickle_file, 'rb') as f:
            return pickle.load(f)      
    except Exception as error:
        print(error)


def get_slang_dict():
    pickle_file = 'slang_words.pkl'
    
    if os.path.exists(pickle_file):
        slang_dict = load_pickle(pickle_file)
    else:
        slang_word = requests.get('https://raw.githubusercontent.com/louisowen6/NLP_bahasa_resources/master/combined_slang_words.txt').text
        slang_word2 = requests.get('https://raw.githubusercontent.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection/master/new_kamusalay.csv').text
        
        slang_word_dict = json.loads(slang_word)
        
        slang_word2_dict = {}
        csv_reader = csv.reader(StringIO(slang_word2))
        for row in csv_reader:
            if row:
                slang, standard = row
                slang_word2_dict[slang] = standard
        
        slang_word_merge = {**slang_word_dict, **slang_word2_dict}

        slang_df = pd.DataFrame(slang_word_merge.items(), columns=['Old', 'New'])
        slang_df['Old'] = slang_df['Old'].apply(lambda x: x.strip())
        slang_df['New'] = slang_df['New'].apply(lambda x: x.strip())
        slang_dict = {}
        for _, row in slang_df.iterrows():
            slang_dict.update({row['Old']: row['New']})

        with open(pickle_file, 'wb') as f:
            pickle.dump(slang_dict, f)
    
    return slang_dict


def download_stopwords():
    if not os.path.exists(os.path.join(nltk.data.find('corpora'), 'stopwords')):
        print("Stopwords resource not found. Downloading...")
        nltk.download('stopwords')


def send_mail(receiver,unsafe_count, username, child_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "elbertmarcellinus@gmail.com"
    password = "ydyb qmmh wksl qdex" 

    # Create the email
    msg = MIMEMultipart("alternative")
    msg['From'] = sender_email
    msg['To'] = receiver
    msg["Subject"] = "Notification: Unsafe Words Detected"
    html_content = get_html(unsafe_count, username, child_email)
    part = MIMEText(html_content, "html")
    msg.attach(part)


    try:
        # Connect to the server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Login to the email account

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        # Close the connection
        server.quit()


