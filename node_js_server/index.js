const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

app.post('/sendToFlask', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:5000/receive_data', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/getFromFlask', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/send_data');
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Node.js server is running on port 3000');
});
