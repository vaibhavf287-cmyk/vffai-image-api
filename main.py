import os
import requests
import time
from flask import Flask, request, send_file, jsonify
import io

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": "Bearer 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"}

@app.route('/generate', methods=['GET'])
def generate():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt missing!"}), 400

    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}  # Ye line AI ko wait karne bolegi
    }

    # Retry logic agar AI busy ho
    for i in range(3):
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return send_file(io.BytesIO(response.content), mimetype='image/jpeg')
        elif response.status_code == 503: # Model loading error
            time.sleep(5) # 5 second ruko phir try karo
            continue
        else:
            break

    return jsonify({"error": "AI is taking too long, please refresh in 10 seconds"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
