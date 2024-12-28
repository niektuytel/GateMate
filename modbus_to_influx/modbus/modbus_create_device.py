import pyperclip
import json

def generate_device_creation_curl(
    device_name,
    description,
    labels,
    profile_name,
    auto_events,
    protocols
):
    """
    Generate a curl command to create a device in EdgeX Foundry.

    Parameters:
        device_name (str): Name of the device.
        description (str): Description of the device.
        labels (list): List of labels for the device.
        profile_name (str): Profile name of the device.
        auto_events (list): List of auto events for the device.
        protocols (dict): Protocols and their configurations.
    Returns:
        str: Generated curl command.
    """

    url = "http://localhost:59881/api/v3/device"

    payload = [
        {
            "apiVersion": "v3",
            "device": {
                "name": device_name,
                "description": description,
                "adminState": "UNLOCKED",
                "operatingState": "UP",
                "labels": labels,
                "serviceName": "device-modbus",
                "profileName": profile_name,
                "autoEvents": auto_events,
                "protocols": protocols,
            }
        }
    ]

    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    # Generate curl command
    curl_command = f"curl -X POST -H \"Content-Type: application/json\" -d '{payload_json}' {url}"
    print(f"{curl_command}\n\n\n")

    # Copy to clipboard
    pyperclip.copy(curl_command)
    print("Curl command copied to clipboard. You can now paste and execute it in your terminal.")

    return curl_command

# Example Usage
if __name__ == "__main__":
    deviceResourcesNames = ["Status_Homing"]

    # Parameters for device creation
    DEVICE_NAME = "Machinova_Test_2"
    DESCRIPTION = "Testing modbus connection with data"
    PROFILE_NAME = "Machinova_Test1_DeviceProfile"
    LABELS = ["modbus", "automation"]

    AUTO_EVENTS = [
        {
            "interval": "2s",
            "onChange": True,
            "sourceName": sourceName
        } for sourceName in deviceResourcesNames
    ]

    PROTOCOLS = {
        "modbus-tcp": {
            "Address": "192.168.8.237",
            "IdleTimeout": "5",
            "Port": "502",
            "Timeout": "5",
            "UnitID": "1"
        }
    }

    generate_device_creation_curl(
        device_name=DEVICE_NAME,
        description=DESCRIPTION,
        labels=LABELS,
        profile_name=PROFILE_NAME,
        auto_events=AUTO_EVENTS,
        protocols=PROTOCOLS
    )
