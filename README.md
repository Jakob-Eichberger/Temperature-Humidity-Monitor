# Temperature-Humidity-Monitor

Software stack that monitors the temperature and humidity in different rooms using esp3286s and sht31 sensors and then displays the data on a grafana dashboard. 

# Prometheus Exporter

## Install

## Build

Open the terminal in `Temperature-Humidity-Monitor\src\Exporter` and run the following commands:

```
docker build -t temperature-humidity-exporter .
docker run -p 5000:5000 --name temperature-humidity-exporter -d  temperature-humidity-exporter
```
OR 

Create a buildkit... 

```docker buildx create --name multiplatformbuilder --driver docker-container --bootstrap ```

...switch to the buildkit...

```docker buildx use multiplatformbuilder```

...build the container and push them to hub.docker.com.

```docker buildx build --platform linux/amd64,linux/arm64 -t <REPOSITORY> --push .```









