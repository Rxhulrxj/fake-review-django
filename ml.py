from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import sklearn as sk
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import train_test_split
def fake_analysis(text):
    nltk.download('stopwords')
    set(stopwords.words('english'))
    stop_words = stopwords.words('english')
    text1 = "BAD ONE"
    #convert to lowercase
    text1 = text1.lower()
    text_final = ''.join(c for c in text1 if not c.isdigit())
    #remove stopwords    
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])
    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    compound = round((1 + dd['compound'])/2, 2)
    compound = int(compound * 100)
    print(compound)
    if compound < 50:
       model=pickle.load(open('model.pkl','rb'))
       df = pd.read_csv('deceptive-opinion.csv')
       df1 = df[['deceptive', 'text']]
       df1.loc[df1['deceptive'] == 'deceptive', 'deceptive'] = 0
       df1.loc[df1['deceptive'] == 'truthful', 'deceptive'] = 1
       X = df1['text']
       Y = np.asarray(df1['deceptive'], dtype = int)
       X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,random_state=109)
       cv = CountVectorizer()
       x = cv.fit_transform(X_train)
       y = cv.transform(X_test)
       data = [text_final]
       vect = cv.transform(data).toarray()
       pred = model.predict(vect)
       if pred == 0:
            print("fake")
       else:
            print("true")
    else:
        print("Positive")