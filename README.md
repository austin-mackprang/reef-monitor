# apex

## Overview

This project provides a monitoring stack for Neptune Apex aquarium controllers using Telegraf, InfluxDB, and Grafana. It collects data from your Apex device, stores it in InfluxDB, and visualizes it with Grafana.

## Features
- Collects real-time data from Neptune Apex via HTTP
- Stores metrics in InfluxDB 2.x
- Visualizes data with Grafana dashboards

## Stack Components
- **Telegraf**: Collects and parses data from the Apex controller
- **InfluxDB**: Time-series database for storing metrics
- **Grafana**: Visualization and dashboarding

## Quick Start
1. Clone this repository:
	```sh
	git clone https://github.com/austin-mac/apex.git
	cd apex/apex-stack/telegraf
	```
2. Update `telegraf.conf` with your Apex device IP if needed.
3. (Optional) Edit `docker-compose.yml` to change credentials or ports.
4. Start the stack:
	```sh
	docker-compose up -d
	```
5. Access:
	- InfluxDB: http://localhost:8086
	- Grafana: http://localhost:3000

## Security Note
For production, do not hardcode sensitive credentials in config files. Use environment variables or Docker secrets.

## License
MIT

