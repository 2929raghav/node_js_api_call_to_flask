
import json
import requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b"
api_token = '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'
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Define source sentences and their corresponding sentences
sentences_sets = [
    {
        "source_sentence": "TCP/IP is the most commonly used protocol suite in computer networks",
        "sentences": [
            "UDP is an alternative protocol to TCP for certain applications",
            "Ethernet is a widely used technology for local area networks",
            "IPv6 is the successor to IPv4 and provides a larger address space"
        ]
    },
    {
        "source_sentence": "Routing algorithms are used to determine the best path for data packets in a network",
        "sentences": [
            "Distance vector routing is a type of routing algorithm",
            "Link-state routing is another type of routing algorithm",
            "OSPF is a popular link-state routing protocol used in large networks"
        ]
    },
    {
        "source_sentence": "Firewalls are used to protect networks from unauthorized access",
        "sentences": [
            "Stateful inspection is a type of firewall technology",
            "Packet filtering is another technique used in firewalls",
            "Intrusion detection systems can complement firewalls for network security"
        ]
    },
    {
        "source_sentence": "Wireless networks use radio waves for communication",
        "sentences": [
            "Wi-Fi is a common wireless networking technology",
            "Bluetooth is another wireless technology used for short-range communication",
            "LTE is a mobile network technology used for high-speed data transmission"
        ]
    },
    {
        "source_sentence": "Network topologies define the layout of network components",
        "sentences": [
            "Star topology connects all devices to a central hub",
            "Mesh topology provides redundant paths for data transmission",
            "Bus topology connects devices along a single cable"
        ]
    }
]

# Iterate over the sets and query for similarity scores
for set_index, sentences_set in enumerate(sentences_sets):
    print(f"Set {set_index + 1}:")
    data = query({"inputs": sentences_set})
    for target_sentence, similarity_score in zip(sentences_set["sentences"], data):
        source_sentence = sentences_set["source_sentence"]
        similarity_score = float(similarity_score)  # Convert similarity score to float
        print(f"Source: {source_sentence} | Target: {target_sentence} | \n Similarity Score: {similarity_score:.4f}")

import numpy as np
import torch as T
from transformers import AutoModelForMaskedLM, AutoTokenizer

print("\nBegin fill-in-the-blank using TA ")

print("\nLoading (cached) DistilBERT language model into memory ")
toker = \
  AutoTokenizer.from_pretrained("distilbert-base-cased")
model = \
  AutoModelForMaskedLM.from_pretrained("distilbert-base-cased")

sentence = "Machine learning (ML) is the study of computer \
algorithms that can (BLANK) automatically through experience \
and by the use of data."

print("\nThe target fill-in-the-blank sentence is: ")
print(sentence)

print("\nThe actual (BLANK) word from Wikipedia is \"learn\" ")

sentence = f"Machine learning (ML) is the study of computer \
algorithms that can {toker.mask_token} automatically through \
experience and by the use of data."

print("\nConverting sentence to token IDs ")
inpts = toker(sentence, return_tensors="pt")
# inpts["input_ids"]
# tensor([[  101,  7792,  3776,   113,   150,
#           2162,   114,  1110,  1103,  2025,
#           1104,  2775, 14975,  1115,  1169,
#            103,  7743,  1194,  2541,  1105,
#           1118,  1103,  1329,  1104,  2233,
#            119,   102]])

# for i in range(27):
#   print(inpts["input_ids"][0][i])

print("\nComputing output for all 28,996 possibilities ")
blank_id = toker.mask_token_id             # ID of blank = 103
blank_id_idx = T.where(inpts["input_ids"] == blank_id)[1]  # 15
with T.no_grad():
  all_logits = model(**inpts).logits                 # 3D
pred_logits = all_logits[0, blank_id_idx, :]  # [1, 28996]

print("\nExtracting IDs of top five predicted words: ")
top_ids = T.topk(pred_logits, 5, dim=1).indices[0].tolist()
print(top_ids)

print("\nThe top five predicteds as words: ")
for id in top_ids:
  print(toker.decode([id]))

print("\nConverting raw logit outputs to probabilities ")
np.set_printoptions(precision=4, suppress=True)
pred_probs = T.softmax(pred_logits, dim=1).numpy()
pred_probs = np.sort(pred_probs[0])[::-1]  # high p to low p
top_probs = pred_probs[0:5]
print("\nThe top five corresponding probabilities: ")
print(top_probs)
# [0.3484 0.1901 0.0978 0.0247 0.0224]

print("\nEnd fill-in-the-blank demo ")