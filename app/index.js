const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

HOST = 'http://127.0.0.1'
PORT = 8000

// API to call /api/transactions/analyze
app.post('/api/transactions/analyze', async (req, res) => {
  try {
    const response = await axios.post(`${HOST}:${PORT}/api/transactions/analyze`, req.body);
    res.send(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error');
  }
});

// API to call /api/transactions/summary/interpret
app.post('/api/transactions/summary/interpret', async (req, res) => {
  try {
    const response = await axios.post(`${HOST}:${PORT}/api/transactions/summary/interpret`, req.body);
    res.send(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error');
  }
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});