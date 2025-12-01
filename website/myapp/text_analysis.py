import csv
import pandas as pd
import string
#pip install spacy
#pip install gensim

import spacy
import gensim
from gensim.models.phrases import Phrases


nlp = spacy.load("fr_core_news_md")
string.punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'

def analyze(df):

    df.fillna('', inplace=True)
    df.drop_duplicates(subset=['Username', 'Text'], keep='last', inplace = True)

    df["Text"] = df["Text"].str.replace('é','e')
    df["Text"] = df["Text"].str.replace('ô','o')
    df["Text"] = df["Text"].str.replace('è','e')
    df["Text"] = df["Text"].str.replace('ê','e')


    cleanDataLemmatized = Clean_listofText(df['Text'])
    df["lemmatized_text"]=cleanDataLemmatized
    df["lemmatized_text"]

def Clean_listofText(textData):
    stop_word_autre = ["\\n"]
    stopwords = list(fr_stop) + stop_word_autre
    cleanDataLemmatize = []
    
    for text in textData :
        
        text=[i.replace("\'"," ") for i in text]
        
        text_w_punct = "".join([i.lower() for i in text if i not in string.punctuation])
        
        #text_w_punct = " ".join([i for i in text_w_punct if not "\'"])
        
        #text_w_num = "".join(i for i in text_w_punct if not i.isdigit())

        tokenize_text = nlp(text_w_punct)

        words_w_3ch = [i for i in tokenize_text if len(i)>3]
        
        words_w_25ch = [i for i in words_w_3ch if len(i)<25]
        
        words_w_stopwords = [i for i in words_w_25ch if i.text not in stopwords]

        words_lemmatize = [word.lemma_ for word in words_w_stopwords]

        #cleanDataLemmatize.append(" ".join([i for i in words_lemmatize]))
        cleanDataLemmatize.append(words_lemmatize)
    
    return cleanDataLemmatize



