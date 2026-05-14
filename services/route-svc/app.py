from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "Route service running"})

@app.route('/eta', methods=['POST'])
def eta():
    data = request.json

    # Mock ETA calculation
    return jsonify({
        "eta_minutes": 10,
        "distance_km": 5
    })

app.run(host="0.0.0.0", port=3008)