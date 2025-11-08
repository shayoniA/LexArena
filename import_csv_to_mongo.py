import pandas as pd
from db import questions_collection, descriptions_collection, classifier_collection

# Load and insert QuestionAnswer.csv
questions_df = pd.read_csv("data/QuestionAnswer.csv")
questions_data = questions_df.to_dict(orient="records")
questions_collection.insert_many(questions_data)

# Load and insert Descriptions.csv
desc_df = pd.read_csv("data/Descriptions.csv")
desc_data = desc_df.to_dict(orient="records")
descriptions_collection.insert_many(desc_data)

# Load and insert NextQuestionClassifier.csv
clf_df = pd.read_csv("data/NextQuestionClassifier.csv")
clf_data = clf_df.to_dict(orient="records")
classifier_collection.insert_many(clf_data)

print("✅ All CSV files successfully imported to MongoDB.")
