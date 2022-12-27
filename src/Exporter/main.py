import json
import time
import requests
import logging
from flask import Flask
from prometheus_client import Gauge, make_wsgi_app

# Set the path to the configuration file
config_file = "/etc/TemperatureHumidityMonitor/App.config"

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Reading the IP addresses from the configuration file until it exists
while True:
    try:
        with open(config_file) as f:
            ip_addresses = f.read().strip().split("\n")
        break
    except FileNotFoundError:
        logging.debug(f"{config_file} not found")
        time.sleep(1)

# Create Prometheus metrics to store the values we want to expose
temperature_metric = Gauge("temperature_metric", "The temperature from the REST API", ["ip_address", "room_name"])
humidity_metric = Gauge("humidity_metric", "The humidity from the REST API", ["ip_address", "room_name"])

@app.route("/metrics")
def metrics():
    for ip_address in ip_addresses:
        try:
            # Make a GET request to the REST API
            response = requests.get(f"http://{ip_address}/")
            # Parse the response data
            data = json.loads(response.text)
            # Extract the values we want to expose
            temperature = data["Temperature"]
            humidity = data["Humidity"]
            room_name = data["Room"]
            # Set the values of the metrics
            temperature_metric.labels(ip_address=ip_address, room_name=room_name).set(temperature)
            humidity_metric.labels(ip_address=ip_address, room_name=room_name).set(humidity)
        except requests.exceptions.RequestException:
            # Set the value of the metrics to nan if the REST API is not reachable
            temperature_metric.labels(ip_address=ip_address, room_name=room_name).set(float('nan'))
            humidity_metric.labels(ip_address=ip_address, room_name=room_name).set(float('nan'))
    # Create a WSGI app that exposes the metrics
    return make_wsgi_app()

if __name__ == "__main__":
    app.run()