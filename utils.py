
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



def preprocess_sentence(sentence):
    sentence = re.sub(r"(?:\@|https?\://)\S+", "", sentence)
    sentence = re.sub(r"http\S+", "", sentence)
    sentence = re.sub(r"<[^>]+>", "", sentence, flags=re.IGNORECASE)
    sentence = re.sub('\n', '', sentence)
    sentence = re.sub('RT', '', sentence)
    sentence = re.sub("[^a-zA-Z^']", " ", sentence)
    sentence = re.sub(" {2,}", " ", sentence)
    sentence = sentence.strip()
    sentence = re.sub(r'\s+', ' ', sentence)
    sentence = sentence.lower()
    return sentence

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
    tokenizer = load_pickle("tokenizer.pkl")
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
