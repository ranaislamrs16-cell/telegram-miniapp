const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// সার্ভার ঠিকঠাক চলছে কিনা চেক করার রুট
app.get('/', (req, res) => {
  res.send('Telegram Mini App Backend is running!');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
