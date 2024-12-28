import re

def update_telegraf_conf(file_path, updates):
    with open(file_path, 'r') as file:
        config_data = file.read()

    for key, value in updates.items():
        # Match the key and update its value using regex
        pattern = rf'({key}\s*=\s*)(.*)'
        replacement = rf'\1{value}'
        config_data = re.sub(pattern, replacement, config_data)

    with open(file_path, 'w') as file:
        file.write(config_data)

def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} (default: {default_value}): ").strip()
    return user_input if user_input else default_value

# Define default updates
default_updates = {
    'servers': '[\"tcp://edgex-mqtt-broker:1883\"]',
    'topics': '[\"telegraf/host01/cpu\",\"telegraf/+/mem\",\"sensors/#\",\"edgex/EdgeXEvents\"]',
    'urls': '[\"https://eu-central-1-1.aws.cloud2.influxdata.com\"]',
    'token': '\"v72jtcinkYwKe1lL_VZuv5Eqs7E5kk4RkwL6gNg-l7rPNpQLtWn-eZK23Idf6H-sQkoKlKmHBoSY3sPqZBB0mw==\"',
    'organization': '\"GateMate\"',
    'bucket': '\"Machinova_Test\"',
    'timeout': '\"10s\"'
}

# Get custom values from the user
updates = {}
for key, default_value in default_updates.items():
    updates[key] = get_user_input(f"Enter value for {key}", default_value)

# Path to the telegraf.conf file
file_path = 'telegraf.conf'

# Update the configuration
update_telegraf_conf(file_path, updates)

print("Configuration updated successfully.")
