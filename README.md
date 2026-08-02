# Emotion Detection System

An end-to-end Text Emotion Detection System using Deep Learning (TensorFlow/Keras) and a Flask web interface.

## Project Structure

- `app.py`: Flask web application.
- `train_model.py`: Script to train the Keras NLP model.
- `predict.py`: Helper script for loading the model and making predictions.
- `emotion_dataset.csv`: Dataset used for training.
- `model/`: Directory storing the trained model (`emotion_model.h5`) and tokenizer (`tokenizer.pkl`).
- `templates/` & `static/`: Frontend web interface files.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Model**
   Run the training script to generate the `.h5` model and `.pkl` tokenizer in the `model/` directory.
   ```bash
   python train_model.py
   ```

3. **Run the Application**
   Start the Flask web server.
   ```bash
   python app.py
   ```

4. **Access the Web UI**
   Open your browser and navigate to `http://localhost:5000`.

## Dataset Format
The dataset (`emotion_dataset.csv`) should be a CSV file with at least two columns: `text` and `emotion`.
