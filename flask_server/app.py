from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b"
api_token = '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'
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid response from API"}

@app.route('/receive_data', methods=['POST'])
def receive_data():
    sentence_sets = request.json
    print(f"Received data: {sentence_sets}")

    results = []
    for sentence_set in sentence_sets:
        # Prepare the payload with the sentences formatted as sentence1 and sentence2
        payload = {
            "inputs": {
                "source_sentence": sentence_set["source_sentence"],
                "sentences": [sentence_set["user_sentences"]]
            }
        }
        response_data = query(payload)
        print(f"API response: {response_data}")

        # Retry logic for when the model is loading
        if isinstance(response_data, dict) and "error" in response_data and "currently loading" in response_data["error"]:
            print("Model is currently loading, waiting before retrying...")
            time.sleep(20)  # Wait for 20 seconds before retrying
            response_data = query(payload)
            print(f"API response after retrying: {response_data}")

        # Check if the response_data is a list and contains similarity scores as floats
        if isinstance(response_data, list) and len(response_data) > 0:
            similarity_score = response_data[0]  # Extract the similarity score (first item in the list)
        else:
            similarity_score = 0  # Default to 0 if the response format is unexpected

        accuracy = f"{similarity_score * 100:.2f}%"  # Convert to percentage and format to two decimal places

        result_set = {
            "your_answer": sentence_set["source_sentence"],
            "right_answer": sentence_set["user_sentences"],
            "accuracy": accuracy
        }
        results.append(result_set)

    response_data = {'message': 'Data received successfully', 'results': results}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
