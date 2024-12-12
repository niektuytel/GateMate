import yaml
import re

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

def determine_value_type(address):
    if address.startswith("w"):
        return "Uint16"  # "Word" typically means 16-bit unsigned integer
    elif address.startswith("lw"):
        return "Uint32"  # "Long Word" typically means 32-bit unsigned integer
    return "String"

# Create device profile structure
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
        resource = {
            "name": sanitized_name,
            "description": f"Modbus register {address}",
            "isHidden": False,
            "tag": "",
            "attributes": {
                "address": address
            },
            "properties": {
                "valueType": determine_value_type(address),
                "readWrite": "RW",
                "units": "",
                "minimum": "",
                "maximum": "",
                "defaultValue": "",
                "mask": "",
                "shift": "",
                "scale": "",
                "offset": "",
                "base": "",
                "assertion": "",
                "mediaType": ""
            }
        }
        device_profile["deviceResources"].append(resource)

    # Example of adding device commands for each resource
    for name in modbus_data.keys():
        sanitized_name = sanitize_name(name)
        command = {
            "name": f"ReadWrite{sanitized_name}Value",
            "isHidden": False,
            "readWrite": "RW",
            "resourceOperations": [
                {
                    "deviceResource": sanitized_name,
                    "defaultValue": "",
                    "mappings": {}
                }
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

    # Output the YAML profile
    output_file = "ModbusDeviceProfile.yml"
    with open(output_file, "w") as yaml_file:
        yaml.dump(device_profile, yaml_file, default_flow_style=False, sort_keys=False)

    print(f"Device profile generated: {output_file}")
    print(f"Execute the following curl command in this location to set it on EdgeX Foundry: (or paste into Postman and define the file location)")
    print(f"curl -X POST -F 'file=@./{output_file}' http://192.168.8.128:59881/api/v2/deviceprofile/uploadfile")
