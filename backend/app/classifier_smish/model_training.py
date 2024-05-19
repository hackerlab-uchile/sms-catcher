import re
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from joblib import dump, load
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words(['english','spanish']))

# Define a function to clean the text
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^0-9a-zA-Z]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove stopwords
    text = " ".join(word for word in text.split() if word not in STOPWORDS)
    return text

# Load the dataset
file_path = '/path/to/dataset.csv'
df = pd.read_csv(file_path, delimiter=';')

# Preprocess the text data
df['clean_text'] = df['messages'].apply(clean_text)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['label'], test_size=0.25, random_state=42)

# Initialize the model
model = RandomForestClassifier()

# Create a pipeline
pipeline_model = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', model)
])

# Train the model
pipeline_model.fit(X_train, y_train)

# Evaluate the model
accuracy = pipeline_model.score(X_test, y_test)
print("Accuracy:", accuracy)

y_pred = pipeline_model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the trained model to disk
dump(pipeline_model, 'trained_model.joblib')

# Load the trained model from disk
loaded_model = load('trained_model.joblib')

# Now you can use loaded_model to make predictions
