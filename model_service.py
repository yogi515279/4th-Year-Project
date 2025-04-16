import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os

class CyberBullyingDetector:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
            
        # Initialize the lemmatizer
        self.lemmatizer = WordNetLemmatizer()
        
        # Load the model and vectorizer
        try:
            model_path = r'D:\cyber_bulling33\cyber_bulling\ann_model.h5'
            vectorizer_path = r'D:\cyber_bulling33\cyber_bulling\tfidf_vectorizer.pkl'
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            if not os.path.exists(vectorizer_path):
                raise FileNotFoundError(f"Vectorizer file not found at {vectorizer_path}")
                
            self.model = load_model(model_path)
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
        except Exception as e:
            print(f"Error loading model or vectorizer: {e}")
            raise

    def preprocess_text(self, text: str) -> str:
        """Preprocess the input text."""
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove special characters and numbers
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            tokens = [word for word in tokens if word not in stop_words]
            
            # Lemmatize
            tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
            
            # Join tokens back into a string
            return ' '.join(tokens)
        except Exception as e:
            print(f"Error in text preprocessing: {e}")
            raise

    def analyze_text(self, text: str) -> dict:
        """Analyze text for cyberbullying content."""
        try:
            # Preprocess the text
            processed_text = self.preprocess_text(text)
            
            # Vectorize the text
            text_vector = self.vectorizer.transform([processed_text])
            
            # Make prediction
            prediction = self.model.predict(text_vector.toarray())[0][0]
            
            # Prepare result
            result = {
                'is_cyberbullying': bool(prediction > 0.5),
                'confidence': float(prediction * 100),
                'severity': self._get_severity(prediction),
                'original_text': text,
                'processed_text': processed_text
            }
            
            return result
        except Exception as e:
            print(f"Error in analyze_text: {e}")
            raise

    def _get_severity(self, probability: float) -> str:
        """Determine severity level based on probability."""
        if probability < 0.5:
            return "none"
        elif probability < 0.7:
            return "low"
        elif probability < 0.85:
            return "medium"
        else:
            return "high"

    def get_bullying_categories(self, text: str) -> list:
        """
        Get potential categories of cyberbullying.
        This is a simplified version that looks for specific keywords.
        """
        text = text.lower()
        categories = []
        
        # Define simple keyword-based categories
        category_keywords = {
            'hate_speech': ['hate', 'racist', 'discrimination'],
            'harassment': ['harass', 'stalking', 'threatening'],
            'personal_attack': ['stupid', 'ugly', 'loser', 'idiot'],
            'sexual': ['sexual', 'inappropriate'],
            'threat': ['threat', 'kill', 'hurt', 'die']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ['general'] 