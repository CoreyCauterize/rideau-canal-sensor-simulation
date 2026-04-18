# Rideau Canal Sensor Simulation

## Overview

This simulator generates synthetic Rideau Canal sensor telemetry and sends it to Azure IoT Hub using one of three device identities. It is used to feed test data into the Stream Analytics pipeline and dashboard.

### What The Simulator Does

- Selects one of three IoT devices from a command-line argument
- Maps each device to a location name
- Generates randomized telemetry fields every 10 seconds
- Sends telemetry to Azure IoT Hub continuously until stopped

### Technologies Used

- Python
- Azure IoT SDK for Python (azure-iot-device)

## Prerequisites

- Python 3.9+
- pip
- An Azure IoT Hub with at least three registered devices
- Device connection strings for those three devices

## Installation

1. Open a terminal in this folder.
2. Install dependencies.

```bash
pip install -r requirements.txt
```

## Configuration

Create a .env file (or export environment variables) with these keys:

- IOTHUB_DEVICE_CONNECTION_STRING_1
- IOTHUB_DEVICE_CONNECTION_STRING_2
- IOTHUB_DEVICE_CONNECTION_STRING_3

Example:

```env
IOTHUB_DEVICE_CONNECTION_STRING_1=HostName=<hub>.azure-devices.net;DeviceId=device1;SharedAccessKey=<key1>
IOTHUB_DEVICE_CONNECTION_STRING_2=HostName=<hub>.azure-devices.net;DeviceId=device2;SharedAccessKey=<key2>
IOTHUB_DEVICE_CONNECTION_STRING_3=HostName=<hub>.azure-devices.net;DeviceId=device3;SharedAccessKey=<key3>
```

Important:

- app.py expects variable names starting with IOTHUB_.
- If your sample env file contains CIOTHUB_ prefixes, rename them to IOTHUB_.

## Usage

Run the simulator and choose the device number:

```bash
python app.py 1
python app.py 2
python app.py 3
```

Device mapping:

- 1 -> DowsLake
- 2 -> FifthAvenue
- 3 -> NAC

Stop the simulator with Ctrl+C.

## Code Structure

Main files:

- app.py: simulator entry point and telemetry sender
- requirements.txt: Python dependencies
- env.example: sample environment variable names/values

### Main Components Explained

- Connection setup:
	- Loads connection strings from environment variables
	- Validates expected IoT Hub connection string format
- Telemetry generator:
	- Produces randomized values for ice, temperature, and snow fields
- Sender loop:
	- Creates IoT Hub client
	- Sends one message every 10 seconds

### Key Functions

- get_telemetry(): creates one telemetry payload
- get_connection_string(device_number): resolves and validates selected device connection string
- parse_args(): validates command-line device selection (1, 2, 3)
- main(device_number): connects to IoT Hub and sends messages in a loop

## Sensor Data Format

### JSON Schema (Logical)

```json
{
	"location": "string",
	"iceThickness": "number (meters)",
	"surfaceTemperature": "number (Celsius)",
	"externalTemperature": "number (Celsius)",
	"snowAccumulation": "number (centimeters)",
	"timestamp": "string (ISO 8601 UTC)"
}
```

### Example Output

```json
{
	"location": "DowsLake",
	"iceThickness": 0.742,
	"surfaceTemperature": -3.8,
	"externalTemperature": -9.4,
	"snowAccumulation": 4.6,
	"timestamp": "2026-04-18T20:55:30Z"
}
```

Note:

- The current code sends Message(str(telemetry)), which serializes a Python dict string.
- For strict JSON on the wire, use json.dumps(telemetry) when creating the message.

## Troubleshooting

### Common Issues And Fixes

1. Missing environment variable error

- Cause: one or more connection string variables are not set.
- Fix: define IOTHUB_DEVICE_CONNECTION_STRING_1, _2, and _3 in your environment or .env file.

2. Invalid connection string format error

- Cause: connection string is malformed or quoted incorrectly.
- Fix: ensure each value includes HostName=, DeviceId=, and SharedAccessKey=. Remove surrounding quotes if needed.

3. No data appears in downstream services

- Cause: wrong device connection string, wrong IoT Hub, or no active Stream Analytics cloud job.
- Fix: verify IoT Hub device IDs and confirm the deployed Stream Analytics job is running.

4. Unicode or dependency install issues on Windows

- Cause: environment differences or outdated pip.
- Fix: upgrade pip and reinstall dependencies.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Data format mismatch in Stream Analytics

- Cause: stream expects JSON but receives a Python-string payload.
- Fix: update message creation to use JSON serialization in app.py.