import requests
import json

# EdgeX Foundry API URL
BASE_URL = "http://192.168.8.128:59881/api/v3"

# Define the device setup function
def configure_device(device_name, profile_name, labels, keys):
    device_data = {
        "name": device_name,
        "description": "Device configured from Modbus data",
        "labels": labels,  # e.g., ["modbus", "automation"]
        "profileName": profile_name,
        "protocols": {
            "modbus-tcp": {
                "address": "192.168.1.100",  # Replace with your device IP
                "port": "502",               # Default Modbus TCP port
                "unitID": "1"                # Modbus Unit ID
            }
        },
        "autoEvents": [
            {
                "sourceName": key,
                "interval": "5s",
                "onChange": True
            }
            for key in keys
        ]
    }

    # API endpoint to create the device
    endpoint = f"{BASE_URL}/device"

    # Send the POST request to EdgeX Foundry
    headers = {"Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=device_data)

    if response.status_code == 201:
        print(f"Device '{device_name}' successfully created.")
    else:
        print(f"Failed to create device '{device_name}'.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

# Main execution
if __name__ == "__main__":
    device_service_name = "device-modbus" # input('Wat is de "device service name"?')
    auto_event_interval_in_seconds = 5 # input('Wat is de interval van lezen in seconden?')

    device_name = "Machinova_Test_Device"  # Unique name for your device
    profile_name = "Machinova_Test_DeviceProfile"  # Uploaded profile name
    labels = ["modbus", "automation"]
    keys = [
        "Status_Homing",
        "Status_Pick_and_Place",
        "Status_CanBus",
        "Status_Pick",
        "Status_Place",
        "Status_TrayChange",
        "Status_Matrix",
        "Status_Pusher",
        "frei_1",
        "frei_2"
    ]

    configure_device(device_name, profile_name, labels, keys)

# Make this working with so least as possbile information from the user, maybe use straight the edgex api

#AND get following working:
# dEventRequest.Event.Readings[0].DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;="
# level=ERROR ts=2024-12-20T00:17:02.355774445Z app=app-influx-export source=runtime.go:427 msg="unable to process payload AddEventRequest.Event.DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;=; AddEventRequest.Event.Readings[0].DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;=. X-Correlation-ID=a3bb3a07-ca15-426e-9d6b-48079db82a7a"
# level=ERROR ts=2024-12-20T00:17:02.355981203Z app=app-influx-export source=messaging.go:199 msg="MessageBus Trigger: Failed to process message on pipeline(s): unable to decode message: unable to process payload AddEventRequest.Event.DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;=; AddEventRequest.Event.Readings[0].DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;="
# level=ERROR ts=2024-12-20T00:18:12.898996953Z app=app-influx-export source=runtime.go:427 msg="unable to process payload AddEventRequest.Event.DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;=; AddEventRequest.Event.Readings[0].DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;=. X-Correlation-ID=d3468e32-c530-4011-9cf6-09d7ac9ab39f"
# level=ERROR ts=2024-12-20T00:18:12.899217375Z app=app-influx-export source=messaging.go:199 msg="MessageBus Trigger: Failed to process message on pipeline(s): unable to decode message: unable to process payload AddEventRequest.Event.DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;=; AddEventRequest.Event.Readings[0].DeviceName field only allows unreserved characters which are ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~:;="
# pi@gatemate:~$ docker logs edgex-app-influxdb-export