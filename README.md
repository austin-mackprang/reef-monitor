# Neptune Apex TIG Stack Monitoring

This setup provides a complete monitoring solution for your Neptune Apex reef controller using Telegraf, InfluxDB, and Grafana.

## Prerequisites

- Docker Desktop for Mac (installed and running)
- Neptune Apex controller accessible at `http://192.168.1.59/cgi-bin/datalog.json`

## Quick Start

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Start the stack:**
   ```bash
   docker-compose up -d
   ```

3. **Access Grafana:**
   - URL: http://localhost:3000
   - Username: `admin`
   - Password: `admin`
   - You'll be prompted to change the password on first login

4. **View your dashboard:**
   - The "Neptune Apex Overview" dashboard should be automatically provisioned
   - You'll see graphs for Temperature, pH, Power Consumption, and Salinity

## What Gets Monitored

The system monitors all data from your Apex controller including:

- **Temperature** (Tmp)
- **pH levels** (pH)
- **ORP** (Oxidation-Reduction Potential)
- **Salinity** (Salt/Cond)
- **Water Level** (Level)
- **Current Draw** (Amps) for all outlets
- **Power Consumption** (Watts) for all outlets
- **Voltage** readings

## Architecture

- **Telegraf**: Scrapes data from Apex every 60 seconds
- **InfluxDB**: Time-series database storing all metrics
- **Grafana**: Visualization and alerting dashboard

## File Structure

```
.
├── docker-compose.yml          # Docker stack definition
├── telegraf.conf              # Telegraf configuration
├── apex-parser.py             # JSON parser (optional)
├── setup.sh                   # Setup automation script
├── grafana-provisioning/      # Auto-provision Grafana
│   ├── datasources/
│   │   └── influxdb.yml
│   └── dashboards/
│       ├── dashboard.yml
│       └── apex-overview.json
└── README.md                  # This file
```

## Customization

### Change Apex Controller IP

Edit `telegraf.conf` and update the URL:
```toml
urls = ["http://YOUR_APEX_IP/cgi-bin/datalog.json"]
```

### Change Data Collection Interval

Edit `telegraf.conf` and modify:
```toml
interval = "60s"  # Change to desired interval
```

### Add Custom Dashboards

1. Create dashboards in Grafana UI
2. Export as JSON
3. Save to `grafana-provisioning/dashboards/`
4. Restart Grafana: `docker-compose restart grafana`

## Troubleshooting

### Check if containers are running:
```bash
docker-compose ps
```

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f telegraf
docker-compose logs -f influxdb
docker-compose logs -f grafana
```

### Test Apex connectivity:
```bash
curl http://192.168.1.59/cgi-bin/datalog.json
```

### Restart a service:
```bash
docker-compose restart telegraf
```

### Reset everything:
```bash
docker-compose down -v  # WARNING: This deletes all data!
docker-compose up -d
```

## InfluxDB Direct Access

If you want to query data directly:

1. Access InfluxDB UI: http://localhost:8086
2. Login with:
   - Username: `admin`
   - Password: `adminpassword123`
3. Organization: `reef`
4. Bucket: `apex`

Example Flux query:
```flux
from(bucket: "apex")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "apex")
  |> filter(fn: (r) => r["type"] == "Temp")
```

## Security Notes

⚠️ **Important for Production Use:**

1. **Change default passwords** in `docker-compose.yml`:
   - InfluxDB admin password
   - InfluxDB token
   - Grafana admin password

2. **Secure network access**:
   - Don't expose ports to the internet
   - Use a reverse proxy with SSL/TLS
   - Enable Grafana authentication

3. **Backup your data**:
   ```bash
   # Backup InfluxDB
   docker exec apex-influxdb influx backup /tmp/backup
   docker cp apex-influxdb:/tmp/backup ./backup
   ```

## Advanced Configuration

### Email Alerts in Grafana

1. Go to Grafana → Alerting → Contact points
2. Add your email configuration
3. Create alert rules on dashboard panels

### Retention Policies

Edit in InfluxDB UI or via CLI to automatically delete old data:
```bash
docker exec -it apex-influxdb influx bucket update \
  --name apex \
  --retention 30d \
  --org reef
```

## Stopping the Stack

```bash
# Stop but keep data
docker-compose stop

# Stop and remove containers (data persists in volumes)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

## Getting Help

Common issues:

1. **"Connection refused" errors**: Check that Apex is accessible from your Mac
2. **No data in Grafana**: Wait 60 seconds for first scrape, check Telegraf logs
3. **Permission denied**: Make sure setup.sh is executable: `chmod +x setup.sh`

## Resources

- [Telegraf Documentation](https://docs.influxdata.com/telegraf/)
- [InfluxDB Documentation](https://docs.influxdata.com/influxdb/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Neptune Apex API](https://www.neptunesystems.com/)

## License

This configuration is provided as-is for personal use with Neptune Apex controllers.