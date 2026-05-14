const express = require('express');
const app = express();

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: "Notify service running" });
});

app.post('/send', (req, res) => {
  const { message } = req.body;

  console.log("Notification:", message);

  res.json({ status: "sent", message });
});

app.listen(3006, () => {
  console.log("Notify service running on 3006");
});