#!/usr/bin/env python3
"""
Neptune Apex JSON Parser for Telegraf
Converts Apex datalog.json format to InfluxDB line protocol
"""

import json
import sys
from datetime import datetime

def parse_apex_json(data):
    """Parse Apex JSON and output InfluxDB line protocol"""
    try:
        ilog = data.get('ilog', {})
        hostname = ilog.get('hostname', 'unknown')
        software = ilog.get('software', 'unknown')
        hardware = ilog.get('hardware', 'unknown')
        controller_type = ilog.get('type', 'unknown')
        
        records = ilog.get('record', [])
        
        for record in records:
            timestamp = record.get('date')
            if not timestamp:
                continue
            
            # Convert to nanoseconds for InfluxDB
            timestamp_ns = int(timestamp) * 1000000000
            
            data_points = record.get('data', [])
            
            for point in data_points:
                name = point.get('name', '').replace(' ', '_')
                did = point.get('did', '').replace(' ', '_')
                point_type = point.get('type', '').replace(' ', '_')
                value = point.get('value', '')
                
                if not name or not value:
                    continue
                
                # Try to convert value to float
                try:
                    float_value = float(value)
                except ValueError:
                    continue
                
                # Build tags
                tags = f"hostname={hostname},name={name},did={did},type={point_type}"
                tags += f",software={software},hardware={hardware},controller={controller_type}"
                
                # Output line protocol
                print(f"apex,{tags} value={float_value} {timestamp_ns}")
    
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
        parse_apex_json(data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)