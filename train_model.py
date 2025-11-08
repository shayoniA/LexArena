import pandas as pd
import pickle
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["legal_quiz_game"]
classifier_collection = db["next_question_classifier"]
data = list(classifier_collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [3])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sc = StandardScaler()
X_train[:, 2:] = sc.fit_transform(X_train[:, 2:])
X_test[:, 2:] = sc.transform(X_test[:, 2:])

classifier = RandomForestClassifier(n_estimators=10, criterion='entropy')
classifier.fit(X_train, y_train)

with open('ml/model.pkl', 'wb') as f:
    pickle.dump(classifier, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(sc, f)
