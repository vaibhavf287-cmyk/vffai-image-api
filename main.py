import os
import requests
from flask import Flask, request, send_file, jsonify
import io

app = Flask(__name__)

# Aapka Hugging Face Token aur Model URL
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": "Bearer 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"}

@app.route('/generate', methods=['GET'])
def generate():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt missing!"}), 400

    # AI ko image banane ka request bhej rahe hain
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    
    if response.status_code == 200:
        # AI se image data mila, use bhej rahe hain
        return send_file(io.BytesIO(response.content), mimetype='image/jpeg')
    else:
        # Agar AI busy ho ya token error ho
        return jsonify({"error": "AI is busy, try again in 10 seconds"}), 500

if __name__ == "__main__":
    # Render ke liye port setup
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
