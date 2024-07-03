import json
import requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b"
api_token = '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'
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Load sentence sets from the file
with open('sentence_sets.json', 'r') as f:
    sentence_sets = json.load(f)

# Iterate over the sets and query for similarity scores
results = []
for set_index, sentence_set in enumerate(sentence_sets):
    data = query({"inputs": sentence_set})
    result_set = {
        "source_sentence": sentence_set["source_sentence"],
        "results": []
    }
    for target_sentence, similarity_score in zip(sentence_set["sentences"], data):
        try:
            similarity_score = float(similarity_score)  # Convert similarity score to float
        except ValueError:
            similarity_score = None  # Handle the error case
        result_set["results"].append({
            "target_sentence": target_sentence,
            "similarity_score": similarity_score
        })
    results.append(result_set)

# Save the results to a file
with open('similarity_scores.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Similarity scores saved to similarity_scores.json")
