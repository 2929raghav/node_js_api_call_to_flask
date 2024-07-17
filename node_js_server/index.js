const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

const data = [
    {
        "source_sentence": "TCP/IP is the most commonly used protocol suite in computer networks",
        "user_sentences": "UDP is an alternative protocol to TCP for certain applications"
    },
    {
        "source_sentence": "Routing algorithms are used to determine the best path for data packets in a network",
        "user_sentences": "Distance vector routing is a type of routing algorithm"
    }
];

app.post('/sendToFlask', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:5000/receive_data', data, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const score_data = response.data;  // Store the response data in a variable
        console.log(score_data);  // Log the response data for debugging purposes
        res.json(score_data);  // Send the response data back to the client
    } catch (error) {
        console.error('Error sending data to Flask:', error.message);
        res.status(500).json({ error: error.message });
    }
});

app.listen(8000, () => {
    console.log('Node.js server is running on port 8000');
});
