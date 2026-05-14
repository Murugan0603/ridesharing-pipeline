const express = require('express');
const app = express();

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: "Payment service running" });
});

app.post('/charge', (req, res) => {
  const { amount } = req.body;

  // Mock payment
  res.json({
    status: "success",
    amount,
    transaction_id: "txn_" + Date.now()
  });
});

app.listen(3007, () => {
  console.log("Payment service running on 3007");
});