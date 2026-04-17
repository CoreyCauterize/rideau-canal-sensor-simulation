from azure.iot.device import IoTHubDeviceClient, Message
import time 
import dotenv
import os
import random

dotenv.load_dotenv()

CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")


def get_telemetry():
    return {
        "iceThickness": random.uniform(0.5, 1.0),  # Simulated ice thickness in meters
        "temperature": random.uniform(-10, 10),    # Simulated temperature in °C
        "snowAccumulation": random.uniform(0, 10),  # Simulated snow accumulation in cm
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def main():
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    print("Connecting to IoT Hub...")
    device_client.connect()
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
    main()