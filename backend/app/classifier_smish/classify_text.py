from joblib import load

# Load the trained model from disk
loaded_model = load('trained_model.joblib')

# Define a function to clean the text
def clean_text(text):
    # Implement your text cleaning logic here
    return text

# Define a function to classify a single text
def classify_text(text):
    # Preprocess the single text
    cleaned_text = clean_text(text)
    
    # Use the trained model for prediction
    prediction = loaded_model.predict([cleaned_text])
    
    return prediction[0]

# Example text to classify
text_to_classify = "La entregas se intento 2/2 veces, confirme sus datoso su articulo sera devuelto: qrco.de/bf3lxx"
print("Text to classify:", text_to_classify)

# Classify the text
prediction = classify_text(text_to_classify)
print("Prediction:", prediction)
