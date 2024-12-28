# Create modbus to influx compose
Create the following compose file on the RPI;
- Login on the RPI  
- Install Golang on the RPI (I used go1.23.3.linux-arm64)
- Install Python on the RPI

### Create 'edgexfoundry/app-influxdb:2.3.0' docker image
- `cd edgex-app-influxdb-export`  
    - doc: https://www.yiqisoft.cn/blogs/edgex/519.html  
    - repo: https://github.com/yiqisoft/edgex-app-influxdb-export
- `make build`
- `docker build . -t edgexfoundry/app-influxdb:2.3.0`
- `cd ..`

### Define custom configurations
- `cd custom-config`
- `python update_configurations.py` Fill in your credentials been used on influx db
- `cd ..`

### Run prebuilt compose file
- `docker compose up -d`

### Setup Device and Device Profile
- `cd modbus`
- Update [modbus_data.txt](./modbus/modbus_data.txt) file with modbus data we want to read out. 
- `python modbus_create_device_profile.py`
- `pip install pyyaml`
- Define in the modbus_create_device.py the 
    - `deviceResourcesNames` with the values you want to read 
    - `PROTOCOLS` with the modbus information
- `python modbus_create_device.py`

### When not receiving data in your influx bucket check logs on:
- `docker logs telegraf`
- `docker logs edgex-mqtt-broker`
- `docker logs edgex-app-influxdb-export`

### References
- https://docs.edgexfoundry.org/3.1/microservices/application/ApplicationServices/

### (Optional) Create Docker compose file manually
We want to send the incomming data to influxDB in this case over MQTT (faster protocol then HTTP)    
- Set following compose file with https://github.com/edgexfoundry/edgex-compose  
    - `make gen no-secty arm64 ds-modbus` and update it with following services.
    - Set missing services on compose file like [this](./docker-compose.yml)

- Telegraf configure file is readed from the location `/home/pi/repo/edgex-compose/compose-builder/config/telegraf.conf` edit this location if needed and create the `telegraf.conf` with following content
```
[[inputs.mqtt_consumer]]
  servers = ["tcp://edgex-mqtt-broker:1883"]
  topics = [
    "telegraf/host01/cpu",
    "telegraf/+/mem",
    "sensors/#",
    "edgex/EdgeXEvents"
  ]
  data_format = "influx"

[[outputs.influxdb_v2]]
  urls = ["https://eu-central-1-1.aws.cloud2.influxdata.com"]
  token = "v72jtcinkYwKe1lL_VZuv5Eqs7E5kk4RkwL6gNg-l7rPNpQLtWn-eZK23Idf6H-sQkoKlKmHBoSY3sPqZBB0mw=="
  organization = "GateMate"
  bucket = "Machinova_Test"
  timeout = "10s"
```
