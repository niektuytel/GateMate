import json
import yaml

# Function to read the device profile name from the YAML file
def get_device_profile_name(file_name):
    try:
        with open(file_name, 'r') as file:
            data = yaml.safe_load(file)
            return data.get('name', None)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None
    
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
    print(f"{curl_command}")

    return curl_command

# Example Usage
if __name__ == "__main__":
    deviceResourcesNames = ["Status_Homing"]
    PROTOCOLS = {
        "modbus-tcp": {
            "Address": "192.168.8.237",
            "IdleTimeout": "5",
            "Port": "502",
            "Timeout": "5",
            "UnitID": "1"
        }
    }

    # Parameters for device creation
    file_name = "ModBusDeviceProfile.yml"
    deviceProfileName = get_device_profile_name(file_name)
    DEVICE_NAME = f"{deviceProfileName}_Device"
    DESCRIPTION = f"Modbus connection with data from profile {deviceProfileName}"
    PROFILE_NAME = deviceProfileName
    LABELS = ["modbus", "automation"]

    AUTO_EVENTS = [
        {
            "interval": "2s",
            "onChange": True,
            "sourceName": sourceName
        } for sourceName in deviceResourcesNames
    ]


    generate_device_creation_curl(
        device_name=DEVICE_NAME,
        description=DESCRIPTION,
        labels=LABELS,
        profile_name=PROFILE_NAME,
        auto_events=AUTO_EVENTS,
        protocols=PROTOCOLS
    )
