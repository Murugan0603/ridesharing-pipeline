const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 3005 });

wss.on('connection', (ws) => {
  console.log("Client connected");

  ws.on('message', (msg) => {
    console.log("Received:", msg.toString());

    // Broadcast to all clients
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(msg.toString());
      }
    });
  });
});

console.log("WebSocket running on 3005");