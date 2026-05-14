from flask import Flask, request, jsonify

app = Flask(__name__)

trip_db = {}

@app.route('/health')
def health():
    return jsonify({"status": "Trip service running"})

@app.route('/create-trip', methods=['POST'])
def create_trip():
    data = request.json
    trip_id = str(len(trip_db) + 1)

    trip_db[trip_id] = {
        "rider": data.get("rider"),
        "driver": data.get("driver"),
        "status": "requested"
    }

    return jsonify({"trip_id": trip_id, "status": "created"})

@app.route('/update-trip/<trip_id>', methods=['POST'])
def update_trip(trip_id):
    status = request.json.get("status")

    if trip_id in trip_db:
        trip_db[trip_id]["status"] = status
        return jsonify({"message": "updated"})

    return jsonify({"error": "trip not found"}), 404

app.run(host="0.0.0.0", port=3004)