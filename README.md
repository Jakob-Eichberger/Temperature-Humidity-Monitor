# Temperature-Humidity-Monitor

Software stack that monitors the temperature and humidity in different rooms using esp3286s and sht31 sensors and then displays the data on a grafana dashboard. 

# Install

## Run Exporter

Open the terminal in `Temperature-Humidity-Monitor\src\Exporter` and run the following commands:

```
docker build -t temperature-humidity-exporter .
docker run -p 5000:5000 --name temperature-humidity-exporter -d  temperature-humidity-exporter
```
