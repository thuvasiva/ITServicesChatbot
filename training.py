import pandas as pd
import sklearn.model_selection as ms
import sklearn.linear_model as sk
import sklearn.naive_bayes as nb
import sklearn.preprocessing as pp
import sklearn.metrics as metrics
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pickle

df = pd.read_csv("intent_recognition_dataset.csv") #read file
print(df['Tag'].unique()) #print all unique tags
oe = pp.OrdinalEncoder() #create ordinal encoder
encodedTags = oe.fit_transform(df['Tag'].values.reshape(-1,1)) #encode tags
df['Tag'] = encodedTags
print(df['Tag'].unique()) #print the encoded (numeric) tags associated with each unencoded tag

vectorizer = CountVectorizer(stop_words = 'english', strip_accents = 'ascii') #create count vectoriser instance
transformed = vectorizer.fit_transform(df['Text'].values).toarray() #transform corpus of text to bag of words model

for i in range(len(transformed)):
  df['Text'][i] = transformed[i]

train, test = ms.train_test_split(df) #split into train and test datasets

X = np.array(train['Text'].values.tolist()) 
y = train['Tag'].values

model = sk.LogisticRegression() #create logistic regression model
model.fit(X,y) #fit the model
predictions = model.predict(np.array(test['Text'].values.tolist()))

model2 = nb.MultinomialNB() #create Multinomial Naive Bayes model
model2.fit(X,y)
predictions2 = model2.predict(np.array(test['Text'].values.tolist()))

print(metrics.f1_score(test['Tag'].values,predictions, average=None)) #compute f1 scores for LR model 
print(metrics.f1_score(test['Tag'].values,predictions2, average=None)) #compute f1 scores for NB model

pickle.dump( model, open( "model.p", "wb" ) ) #serialize model to file
pickle.dump( vectorizer, open( "vectorizer.p", "wb")) #serialize vectorizer to file
