const express = require('express');
const app = express();
app.use(express.json());

// ✅ Change this: உங்க app name போடுங்க
const APP_NAME = "RideShare Auth Service";

app.get('/health', (req, res) => {
  res.json({ status: 'running', service: APP_NAME });
});

app.post('/login', (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'email and password required' });
  }
  // ✅ Change this: Real JWT logic later add பண்ணலாம்
  res.json({
    token: 'mock-jwt-' + Date.now(),
    user: { id: 1, email: email, role: 'rider' }
  });
});

app.post('/register', (req, res) => {
  const { name, email, password, role } = req.body;
  // ✅ Change this: role = 'rider' or 'driver'
  res.json({
    message: 'User registered successfully',
    user: { name, email, role: role || 'rider' }
  });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`${APP_NAME} running on port ${PORT}`);
});