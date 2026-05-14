from flask import Flask, jsonify, request
import redis

app = Flask(__name__)

# ✅ Change this: Redis host name - docker-compose-ல "redis" யே name
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/health')
def health():
    return jsonify({'status': 'running', 'service': 'Matching Service'})

@app.route('/find-driver', methods=['POST'])
def find_driver():
    data = request.json

    # ✅ Change this: இங்க rider-ஓட location வருது
    rider_lat = data.get('lat', 12.9716)   # Chennai default
    rider_lon = data.get('lon', 77.5946)

    # Redis GEO - 5km radius-ல driver தேடுது
    drivers = r.georadius(
        'drivers',
        rider_lon, rider_lat,
        5, 'km',
        withcoord=True,
        withdist=True,
        sort='ASC',
        count=1
    )

    if drivers:
        driver = drivers[0]
        return jsonify({
            'found': True,
            'driver_id': driver[0],
            'distance_km': round(float(driver[1]), 2),
            'driver_location': driver[2]
        })

    return jsonify({'found': False, 'error': 'No drivers nearby'}), 404

if __name__ == '__main__':
    # ✅ host='0.0.0.0' - இது மாத்தாதீங்க! Docker-க்கு இது வேணும்
    app.run(host='0.0.0.0', port=3002, debug=True)