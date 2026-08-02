import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense # type: ignore

# Constants
CSV_PATH = 'emotion_dataset.csv'
MODEL_DIR = 'model'
MODEL_PATH = os.path.join(MODEL_DIR, 'emotion_model.h5')
TOKENIZER_PATH = os.path.join(MODEL_DIR, 'tokenizer.pkl')
ENCODER_PATH = os.path.join(MODEL_DIR, 'encoder.pkl')
MAX_LENGTH = 50
VOCAB_SIZE = 5000
EMBEDDING_DIM = 16

def train():
    print(f"Loading data from {CSV_PATH}...")
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f"Error: Could not find {CSV_PATH}.")
        return

    if 'text' not in df.columns or 'emotion' not in df.columns:
        print("Error: CSV must contain 'text' and 'emotion' columns.")
        return

    texts = df['text'].astype(str).tolist()
    labels = df['emotion'].tolist()

    # Encode labels
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels)
    num_classes = len(encoder.classes_)
    print(f"Detected classes: {encoder.classes_}")

    # Tokenize text
    print("Tokenizing text...")
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post')

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, encoded_labels, test_size=0.2, random_state=42)

    # Build model
    print("Building model...")
    model = Sequential([
        Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_LENGTH),
        GlobalAveragePooling1D(),
        Dense(24, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    # Train model
    print("Training model...")
    # For a real dataset, epochs should be higher. We use 100 for dummy data.
    model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), verbose=1)

    # Evaluate
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {accuracy:.4f}")

    # Save artifacts
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print("Saving model and tokenizer...")
    model.save(MODEL_PATH)
    
    with open(TOKENIZER_PATH, 'wb') as f:
        pickle.dump(tokenizer, f)

    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(encoder, f)
        
    print("Training complete!")

if __name__ == '__main__':
    train()
