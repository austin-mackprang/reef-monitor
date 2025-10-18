#!/bin/bash
# Fix script for Telegraf mount issue

set -e

echo "🔧 Fixing Telegraf configuration..."

# Stop all containers
echo "Stopping containers..."
docker-compose down

# Create telegraf directory if it doesn't exist
mkdir -p telegraf

# Create telegraf.conf in the telegraf directory
echo "Creating telegraf.conf..."
cat > telegraf/telegraf.conf <<'EOF'
[agent]
  interval = "60s"
  round_interval = true
  metric_batch_size = 1000
  metric_buffer_limit = 10000
  collection_jitter = "0s"
  flush_interval = "10s"
  flush_jitter = "0s"
  precision = "0s"
  hostname = "apex-telegraf"
  omit_hostname = false

[[outputs.influxdb_v2]]
  urls = ["http://influxdb:8086"]
  token = "${INFLUX_TOKEN}"
  organization = "reef"
  bucket = "apex"

[[inputs.http]]
  urls = ["http://192.168.1.59/cgi-bin/datalog.json"]
  interval = "60s"
  timeout = "30s"
  method = "GET"
  data_format = "json_v2"
  
  [[inputs.http.json_v2]]
    measurement_name = "apex"
    timestamp_path = "ilog.record.#.date"
    timestamp_format = "unix"
    
    [[inputs.http.json_v2.object]]
      path = "ilog.record.#.data.#"
      tags = ["name", "did", "type"]
      
      [[inputs.http.json_v2.object.field]]
        path = "value"
        type = "float"

    [[inputs.http.json_v2.tag]]
      path = "ilog.hostname"
      rename = "hostname"
    
    [[inputs.http.json_v2.tag]]
      path = "ilog.software"
      rename = "software_version"
    
    [[inputs.http.json_v2.tag]]
      path = "ilog.hardware"
      rename = "hardware_version"
    
    [[inputs.http.json_v2.tag]]
      path = "ilog.type"
      rename = "controller_type"
EOF

# Verify the file was created
if [ -f "telegraf/telegraf.conf" ]; then
    echo "✅ telegraf.conf created successfully"
    echo "📍 File location: $(pwd)/telegraf/telegraf.conf"
else
    echo "❌ Failed to create telegraf.conf"
    exit 1
fi

# Start the stack again
echo ""
echo "Starting containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for containers to start..."
sleep 5

echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "✅ Fix applied! Checking Telegraf logs..."
echo ""
docker-compose logs --tail=20 telegraf

echo ""
echo "To monitor logs in real-time, run:"
echo "  docker-compose logs -f telegraf"