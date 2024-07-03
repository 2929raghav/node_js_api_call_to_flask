# app.py
from flask import Flask, request, jsonify
import json
app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    print(f"Received data: {data}")
    with open('sentence_sets.json', 'w') as f:
       json.dump(data, f, indent=4)
    response_data = {'message': 'Data received successfully', 'received_data': data}

    return jsonify(response_data)



@app.route('/send_data', methods=['GET'])
def send_data():
    
    with open('similarity_scores.json', 'r') as f:
        similarity_scores = json.load(f)

    return jsonify(similarity_scores)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
