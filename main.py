"""
IoTIncubator Sensor Array Emulator.

This program generates random values for temperature and humidity within a specified range and outputs them as a JSON object every 10 seconds. The generated values gradually rise or fall over time to create a more natural representation of temperature and humidity changes.

Dependencies:
- Flask: A micro web framework used to create a simple HTTP server for hosting the application.

Usage:
1. Ensure Flask is installed (`pip install flask`).
2. Run the script.
3. Access the root URL (`http://localhost:5000/`) to view the program status.

Code Organization:
- `generate_data()`: Generates temperature and humidity data and output as JSON.
- `sensor_data()`: Route handler for sensor data from the DHT11 temperature and humidity sensor.
- `__name__ == '__main__'` block: Starts data generation and runs the Flask application.

"""
from random import uniform, gauss, choice
from datetime import datetime

from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incubator.db'
db = SQLAlchemy(app=app)
CORS(app=app, origins='*')


class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    motion_detected = db.Column(db.Boolean)
    water_refill = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)


class EggTurnSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)


# Initial temperature and humidity values
temperature = uniform(25, 35)
humidity = uniform(50, 85)
# motionSensorState = choice([True, False])
# waterLevelSensorState = choice([True, False])

# Range for variation
range_variation = (-0.15, 0.15)


def generate_data() -> dict:
    """
    Generates temperature and humidity data and output as JSON.
    """

    global temperature, humidity

    water_level = choice([True, False])
    motion_detected = choice([True, False])
    incubator_status = choice(['active', 'paused', 'completed'])

    # Calculate  temperature growth or decay with randomness
    new_temperature = gauss(0, range_variation[1])
    new_temperature = max(range_variation[0], new_temperature)
    new_temperature = min(range_variation[1], new_temperature)

    # Calculate humidity growth or decay with randomness
    new_humidity = gauss(0, range_variation[1])
    new_humidity = max(range_variation[0], new_humidity)
    new_humidity = min(range_variation[1], new_humidity)

    temperature += new_temperature
    humidity += new_humidity

    return temperature, humidity, water_level, motion_detected, incubator_status


@app.route('/')
def index():
    """
    Default route handler for the flask application.
    """
    html = f"""
    <html>
        <head>
            <title>IoTIncubator Sensor Array Simulator</title>
        </head>
        <body>
            <p>Navigate '<a href='{request.base_url}sensor/data'>HERE</a>' to get JSON response from the sensor array.</p>
        </body>
    </html>
    """
    return html


@app.route('/sensor/data')
def sensor_data() -> Response:
    """
    Route handler for sensor data from the DHT11 temperature and humidity sensor.
    """
    temperature, humidity, water_level, motion_detected, incubator_status = generate_data()
    # timestamp = datetime.now().isoformat()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check for null values
    if temperature is None or humidity is None:
        return jsonify(error='Null values received')

    return jsonify(temperature=temperature, humidity=humidity, motionSensorState=motion_detected, waterLevelSensorState=water_level, incubatorStatus=incubator_status,timestamp=timestamp)


if __name__ == '__main__':
    # Start the Flask application
    app.run(debug=True, port=5001)
