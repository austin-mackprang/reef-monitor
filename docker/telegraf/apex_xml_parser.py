#!/usr/bin/env python3
"""
Neptune Apex XML Parser for Telegraf
Fetches status.xml and outputs InfluxDB line protocol
"""

import sys
import os
import xml.etree.ElementTree as ET
import urllib.request
import time

def fetch_and_parse():
    apex_url = os.environ.get('APEX_ENDPOINT', 'http://192.168.1.59/cgi-bin/status.xml')

    try:
        # Fetch XML from Apex
        with urllib.request.urlopen(apex_url, timeout=10) as response:
            xml_data = response.read()

        # Parse XML
        root = ET.fromstring(xml_data)

        # Get timestamp (use current time)
        timestamp = int(time.time() * 1000000000)  # nanoseconds

        # Get system info
        hostname = root.find('hostname').text if root.find('hostname') is not None else 'unknown'
        serial = root.find('serial').text if root.find('serial') is not None else 'unknown'
        software = root.get('software', 'unknown')
        hardware = root.get('hardware', 'unknown')

        # Parse probes
        probes = root.find('probes')
        if probes is not None:
            for probe in probes.findall('probe'):
                probe_name = probe.find('name').text.strip() if probe.find('name') is not None else 'unknown'
                probe_value_text = probe.find('value').text.strip() if probe.find('value') is not None else '0'
                probe_type_elem = probe.find('type')
                probe_type = probe_type_elem.text.strip() if probe_type_elem is not None else ''

                # Try to convert value to float
                try:
                    probe_value = float(probe_value_text)
                except ValueError:
                    probe_value = 0.0

                # Output in line protocol format
                # apex_probe,probe_name=Tmp,probe_type=Temp,hostname=Austins_Reef value=79.3 timestamp
                tags = f'probe_name={probe_name},hostname={hostname}'
                if probe_type:
                    tags += f',probe_type={probe_type}'

                print(f'apex_probe,{tags} value={probe_value} {timestamp}')

        # Parse outlets
        outlets = root.find('outlets')
        if outlets is not None:
            for outlet in outlets.findall('outlet'):
                outlet_name = outlet.find('name').text.strip() if outlet.find('name') is not None else 'unknown'
                outlet_state = outlet.find('state').text.strip() if outlet.find('state') is not None else 'unknown'
                device_id = outlet.find('deviceID').text.strip() if outlet.find('deviceID') is not None else 'unknown'
                output_id_text = outlet.find('outputID').text.strip() if outlet.find('outputID') is not None else '0'

                try:
                    output_id = int(output_id_text)
                except ValueError:
                    output_id = 0

                # Output outlet status
                tags = f'outlet_name={outlet_name},device_id={device_id},state={outlet_state},hostname={hostname}'
                print(f'apex_outlet,{tags} output_id={output_id}i {timestamp}')

        # Output system info
        tags = f'hostname={hostname},serial={serial},software={software},hardware={hardware}'
        print(f'apex_system,{tags} status=1i {timestamp}')

    except Exception as e:
        print(f'# Error fetching/parsing Apex data: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    fetch_and_parse()
