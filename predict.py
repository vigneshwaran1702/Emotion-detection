import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

MODEL_DIR = 'model'
MODEL_PATH = os.path.join(MODEL_DIR, 'emotion_model.h5')
TOKENIZER_PATH = os.path.join(MODEL_DIR, 'tokenizer.pkl')
ENCODER_PATH = os.path.join(MODEL_DIR, 'encoder.pkl')
MAX_LENGTH = 50

# Global variables to cache model/tokenizer
_model = None
_tokenizer = None
_encoder = None

def load_artifacts():
    global _model, _tokenizer, _encoder
    if _model is None:
        try:
            _model = load_model(MODEL_PATH)
            with open(TOKENIZER_PATH, 'rb') as f:
                _tokenizer = pickle.load(f)
            with open(ENCODER_PATH, 'rb') as f:
                _encoder = pickle.load(f)
        except Exception as e:
            print(f"Error loading model artifacts: {e}")
            raise

def predict_emotion(text):
    if not text or not text.strip():
        return None

    try:
        load_artifacts()
    except Exception:
        return "Error: Model not trained yet."

    # Preprocess text
    sequence = _tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')

    # Predict
    prediction = _model.predict(padded)
    predicted_class_index = np.argmax(prediction[0])
    
    # Decode
    emotion = _encoder.inverse_transform([predicted_class_index])[0]
    
    # Get confidence
    confidence = float(prediction[0][predicted_class_index])
    
    return {
        "emotion": emotion,
        "confidence": confidence
    }
