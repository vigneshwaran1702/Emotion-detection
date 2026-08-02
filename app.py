from flask import Flask, render_template, request, jsonify
from predict import predict_emotion
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_api():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data['text']
        result = predict_emotion(text)
        
        if isinstance(result, str):
            # Error string returned
            return jsonify({"error": result}), 500
            
        if result:
            return jsonify({
                "text": text,
                "emotion": result["emotion"],
                "confidence": result["confidence"]
            })
        else:
            return jsonify({"error": "Failed to predict emotion"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure model directory exists
    if not os.path.exists('model'):
        os.makedirs('model')
    app.run(debug=True, host='0.0.0.0', port=5000)
