from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # allow all origins for testing

app = Flask(__name__)

# Your n8n webhook URL
N8N_WEBHOOK_URL = "https://anuptg.app.n8n.cloud/webhook/GKG"

@app.route("/api/prompt", methods=["POST"])
def proxy_to_n8n():
    try:
        # Get JSON body from tester
        user_data = request.get_json(force=True)

        # Forward it to n8n webhook
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=user_data,
            timeout=300  # 5 min max wait (to match your n8n workflow)
        )

        # Try to return n8n JSON response
        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            # If not JSON, return raw text
            return response.text, response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return {"message": "Flask Proxy API for n8n is running!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
