from azure.iot.device import IoTHubDeviceClient, Message
import time 
import dotenv
import os
import random
import argparse

dotenv.load_dotenv()

# use three different connection strings for three different devices
CONNECTION_STRING_1 = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING_1")
CONNECTION_STRING_2 = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING_2")
CONNECTION_STRING_3 = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING_3")

location_mapping = {
    1: "DowsLake",
    2: "FifthAvenue",
    3: "NAC"
}


def get_telemetry():
    return {
        "location": location_mapping.get(number, "Unknown Location"),
        "iceThickness": random.uniform(0.5, 1.0),  # Simulated ice thickness in meters
        "surfaceTemperature": random.uniform(-10, 10),    # Simulated surface temperature in °C
        "externalTemperature": random.uniform(-15, 5),  # Simulated external temperature in °C
        "snowAccumulation": random.uniform(0, 10),  # Simulated snow accumulation in cm
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def get_connection_string(device_number):
    connection_strings = {
        1: CONNECTION_STRING_1,
        2: CONNECTION_STRING_2,
        3: CONNECTION_STRING_3,
    }

    connection_string = connection_strings.get(device_number)
    print(f"Using connection string for device {device_number}")
    if not connection_string:
        raise ValueError(
            f"Missing environment variable for device {device_number}. "
            f"Expected IOTHUB_DEVICE_CONNECTION_STRING_{device_number}."
        )

    # dotenv values are sometimes wrapped in quotes; remove only outer quotes.
    connection_string = connection_string.strip().strip('"').strip("'")

    required_parts = ["HostName=", "DeviceId=", "SharedAccessKey="]
    if not all(part in connection_string for part in required_parts):
        raise ValueError(
            f"Invalid connection string format for device {device_number}. "
            "Expected HostName, DeviceId, and SharedAccessKey segments."
        )

    return connection_string


def parse_args():
    parser = argparse.ArgumentParser(
        description="Rideau Canal Sensor Simulation"
    )
    parser.add_argument(
        "device_number",
        type=int,
        choices=[1, 2, 3],
        help="Device connection string selector (1, 2, or 3)",
    )
    return parser.parse_args()


def main(device_number):
    connection_string = get_connection_string(device_number)
    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    print("Connecting to IoT Hub...")
    current_location = location_mapping.get(device_number, "Unknown Location")
    device_client.connect()
    print(f"Connected to IoT Hub. Current location: {current_location}")

    try:
        while True:
            telemetry = get_telemetry()

            # Send message to IoT Hub
            message = Message(str(telemetry))
            device_client.send_message(message)
            print(f"Sent message: {telemetry}")

            # Wait for a few seconds before sending the next message
            time.sleep(10)

    except KeyboardInterrupt:
        print("Simulation stopped by user.")
    finally:
        device_client.disconnect()    

if __name__ == "__main__":
    print("Starting Rideau Canal Sensor Simulation...")
    args = parse_args()
    number = args.device_number
    main(number)