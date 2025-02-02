# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:22:43 2025

@author: oem
"""

filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width', 200)
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from textblob import Word, TextBlob
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from nltk.sentiment import SentimentIntensityAnalyzer
from warnings import filterwarnings
from textblob import Word
! pip install nltk
! pip install textblob
! pip install wordcloud
import nltk
nltk.download('stopwords')
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
import nltk
nltk.download('vader_lexicon')
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
df = pd.read_excel("C:\\Users\\oem\\Desktop\\amazon\\amazon.xlsx")
df["Review"] = df["Review"].str.lower()
df["Review"] = df["Review"].replace("[^\w\s]", " ", regex = True)
sw = stopwords.words("english")
df["Review"] = df["Review"].apply(lambda x: " ".join(x for x in str(x).split()
                                                     if x not in sw))
df["Review"] = df["Review"].replace("\d" , " " , regex = True)
drops = pd.Series(" ".join(df["Review"]).split()).value_counts()[-1000:]
df["Review"] = df["Review"].apply(lambda x: " ".join(x for x in x.split() if x not in drops))
df['Review'] = df['Review'].apply(lambda x: " ".join([Word(word).lemmatize() 
                                                      for word in str(x).split()]))
df['Review'] = df['Review'].apply(lambda x: " ".join([Word(word).lemmatize() 
                                                      for word in str(x).split()]))
tf = df['Review'].apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
tf.columns = ["words", "tf"]
tf[tf["tf"] > 500].plot.bar(x = "words", y = "tf")
plt.show()
text = " ".join(i for i in df.Review)
wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud, interpolation= "bilinear")
plt.axis("off")
plt.show()
sia = SentimentIntensityAnalyzer()
df["Review"][0:10].apply(lambda x: sia.polarity_scores(x))
df["Review"][0:10].apply(lambda x: sia.polarity_scores(x)["compound"])
df["Review"][0:10].apply(lambda x: "pos" if sia.polarity_scores(x)["compound"] > 0 else "neg")
df["Sentiment_Label"] = df["Review"].apply(lambda x: "pos" if sia.polarity_scores(x)["compound"] > 0 else "neg")
df.groupby("Sentiment_Label")["Star"].mean()
train_x, test_x, train_y, test_y = train_test_split(df["Review"],
                                                    df["Sentiment_Label"],
                                                    random_state=42)

tf_idf_word_vectorizer = TfidfVectorizer().fit(train_x)
x_train_tf_idf_word = tf_idf_word_vectorizer.transform(train_x)
x_test_tf_idf_word = tf_idf_word_vectorizer.transform(test_x)
log_model = LogisticRegression().fit(x_train_tf_idf_word, train_y)
y_pred = log_model.predict(x_test_tf_idf_word)
print(classification_report(y_pred, test_y))
cross_val_score(log_model, x_test_tf_idf_word, test_y, cv = 5).mean()
random_review = pd.Series(df["Review"].sample(1).values)
yeni_yorum = CountVectorizer().fit(train_x).transform(random_review)
pred = log_model.predict(yeni_yorum)
print(f'Review:  {random_review[0]} \n Prediction: {pred}')
rf_model = RandomForestClassifier().fit(x_train_tf_idf_word, train_y)
cross_val_score(rf_model, x_test_tf_idf_word, test_y, cv=5, n_jobs=-1).mean()


