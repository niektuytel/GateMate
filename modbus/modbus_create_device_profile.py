import yaml
import re

# Group similar resources getting bulked
# curl -X GET http://localhost:59882/api/v3/device/name/<DEVICE_NAME>/command/Readfrei_group
GROUPS = {
    "frei_group": ["frei_9", "frei_10", "frei_11", "frei_12", "frei_13", "frei_14", "frei_15"]
}


def parse_modbus_data(file_path):
    modbus_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and "=>" in line:
                key, value = line.split("=>")
                modbus_data[key.strip()] = value.strip()
    return modbus_data

def sanitize_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '', name)

def clean_value(address):
    return address.replace("\xC2", "").replace("_", "").strip()

def determine_value_type(address):
    if address.startswith("w"):
        return "Uint16"  # "Word" typically means 16-bit unsigned integer
    elif address.startswith("lw"):
        return "Uint32"  # "Long Word" typically means 32-bit unsigned integer
    return "String"

def generate_device_profile(manufacturer, modbus_data):
    device_profile = {
        "name": f"{manufacturer}_DeviceProfile",
        "description": "Device profile generated from Modbus data",
        "manufacturer": manufacturer,
        "model": "ModbusModel",
        "labels": ["modbus", "automation"],
        "deviceResources": [],
        "deviceCommands": []
    }

    for name, address in modbus_data.items():
        sanitized_name = sanitize_name(name)
        cleaned_address = clean_value(address)
        resource = {
            "name": sanitized_name,
            "description": f"Modbus register {cleaned_address}",
            "isHidden": False,
            "attributes": {
                "address": cleaned_address
            },
            "properties": {
                "valueType": determine_value_type(cleaned_address),
                "readWrite": "RW",  # Ensure compatibility, probably we will only use Read just to be sure
                "units": "",  # Optional, but must be valid if provided
                "minimum": None,  # Use None for optional values
                "maximum": None,
                "defaultValue": "",
                "mask": None,
                "shift": None,
                "scale": None,
                "offset": None,
                "base": None,
                "assertion": "",
                "mediaType": ""
            }
        }
        device_profile["deviceResources"].append(resource)

    return device_profile

def try_add_device_commands(device_profile):
    for group_name, resource_names in GROUPS.items():
        sanitized_group_name = sanitize_name(group_name)
        command = {
            "name": f"Read{sanitized_group_name}",
            "isHidden": False,
            "readWrite": "R",
            "resourceOperations": [
                {"deviceResource": sanitize_name(resource_name), "defaultValue": "", "mappings": {}}
                for resource_name in resource_names
            ]
        }
        device_profile["deviceCommands"].append(command)

    return device_profile

# Main execution
if __name__ == "__main__":
    input_file = "modbus_data.txt"  # Input file containing Modbus data
    company = input("What is de bedrijfs naam waar het voor gemaakt wordt? ")
    company = sanitize_name(company.replace(" ", "_"))

    modbus_data = parse_modbus_data(input_file)
    
    device_profile = generate_device_profile(company, modbus_data)
    device_profile = try_add_device_commands(device_profile)

    # Output the YAML profile
    output_file = "ModbusDeviceProfile.yml"
    with open(output_file, "w") as yaml_file:
        yaml.dump(device_profile, yaml_file, default_flow_style=False, sort_keys=False)

    print(f"Device profile generated: {output_file}")
    print(f"Execute the following curl command in this location to set it on EdgeX Foundry: (or paste into Postman and define the file location)")
    print(f"curl -X POST -F 'file=@./{output_file}' http://192.168.8.128:59881/api/v3/deviceprofile/uploadfile")
