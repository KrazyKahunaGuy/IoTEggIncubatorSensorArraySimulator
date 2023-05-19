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

from flask import Flask, Response, request
from random import uniform, gauss

app = Flask(__name__)

# Initial temperature and humidity values
temperature = uniform(25, 35)
humidity = uniform(50, 85)

# Range for variation
range_variation = (-0.15, 0.15)


def generate_data() -> dict:
    """
    Generates temperature and humidity data and output as JSON.
    """

    global temperature, humidity

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

    data = {'temperature': temperature, 'humidity': humidity}
    return data


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
    return generate_data()


if __name__ == '__main__':
    # Start the Flask application
    app.run(debug=True, port=os.getenv("PORT", default=5000))
