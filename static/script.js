document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('textInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    
    const resultSection = document.getElementById('resultSection');
    const emotionEmoji = document.getElementById('emotionEmoji');
    const emotionLabel = document.getElementById('emotionLabel');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceValue = document.getElementById('confidenceValue');
    
    const errorToast = document.getElementById('errorToast');
    const errorMessage = document.getElementById('errorMessage');

    const emojiMap = {
        'joy': '😊',
        'sadness': '😢',
        'anger': '😠',
        'fear': '😨',
        'surprise': '😲',
        'neutral': '😐',
        'love': '🥰',
        'default': '🤔'
    };

    function showError(msg) {
        errorMessage.textContent = msg;
        errorToast.classList.remove('hidden');
        setTimeout(() => {
            errorToast.classList.add('hidden');
        }, 3000);
    }

    function setLoading(isLoading) {
        if (isLoading) {
            btnText.classList.add('hidden');
            loader.classList.remove('hidden');
            analyzeBtn.disabled = true;
            analyzeBtn.style.opacity = '0.8';
        } else {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            analyzeBtn.disabled = false;
            analyzeBtn.style.opacity = '1';
        }
    }

    analyzeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        
        if (!text) {
            showError('Please enter some text to analyze.');
            return;
        }

        setLoading(true);
        resultSection.classList.add('hidden');
        
        // Reset progress bar
        confidenceBar.style.width = '0%';
        confidenceValue.textContent = '0%';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred');
            }

            // Update UI with results
            const emotion = data.emotion.toLowerCase();
            const confidence = Math.round(data.confidence * 100);

            emotionEmoji.textContent = emojiMap[emotion] || emojiMap['default'];
            emotionLabel.textContent = data.emotion;
            
            // Re-trigger animations
            emotionEmoji.style.animation = 'none';
            emotionEmoji.offsetHeight; /* trigger reflow */
            emotionEmoji.style.animation = 'popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';

            resultSection.classList.remove('hidden');
            
            // Animate progress bar slightly after showing
            setTimeout(() => {
                confidenceBar.style.width = `${confidence}%`;
                confidenceValue.textContent = `${confidence}%`;
            }, 100);

        } catch (error) {
            console.error('Error:', error);
            showError(error.message);
        } finally {
            setLoading(false);
        }
    });

    // Handle Enter key to submit
    textInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            analyzeBtn.click();
        }
    });
});
