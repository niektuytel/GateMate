# GateMate
With gate mate you can connect any connection and pass it trough other configured connections to parse data through

## Setup export for app influx db:

### Build 'edgexfoundry/app-influxdb:2.3.0'
- `git clone https://github.com/yiqisoft/edgex-app-influxdb-export` (doc: https://www.yiqisoft.cn/blogs/edgex/519.html)
- `make build`
- `docker build . -t edgexfoundry/app-influxdb:2.3.0`

### Define application that van export data to influxDB
We want to send the incomming data to influxDB in this case over MQTT (faster protocol then HTTP)    
- Set following compose file with https://github.com/edgexfoundry/edgex-compose  
i.e. `make gen no-secty arm64 ds-modbus ds-virtual mqtt-broker` and update it with following services. (NOTE: remove/edit generated mqtt-broker)
```
name: edgex
services:
  app-service-influxdb-export:
    image: edgexfoundry/app-influxdb:2.3.0
    ports:
      - 127.0.0.1:59780:59780/tcp
    container_name: edgex-app-influxdb-export
    hostname: edgex-app-influxdb-export
    depends_on:
      consul:
        condition: service_started
      core-data:
        condition: service_started
    environment:
      CLIENTS_CORE_COMMAND_HOST: edgex-core-command
      CLIENTS_CORE_DATA_HOST: edgex-core-data
      CLIENTS_CORE_METADATA_HOST: edgex-core-metadata
      CLIENTS_SUPPORT_NOTIFICATIONS_HOST: edgex-support-notifications
      CLIENTS_SUPPORT_SCHEDULER_HOST: edgex-support-scheduler
      DATABASES_PRIMARY_HOST: edgex-redis
      EDGEX_SECURITY_SECRET_STORE: "false"
      MESSAGEQUEUE_HOST: edgex-redis
      REGISTRY_HOST: edgex-core-consul
      SERVICE_HOST: edgex-app-influxdb-export
      TRIGGER_EDGEXMESSAGEBUS_PUBLISHHOST_HOST: edgex-redis
      TRIGGER_EDGEXMESSAGEBUS_SUBSCRIBEHOST_HOST: edgex-redis
      MQTTCONFIG_BROKERADDRESS: edgex-mqtt-broker:1883
    read_only: true
    restart: always
    networks:
      - edgex-network
    security_opt:
      - no-new-privileges:true
    user: 2002:2001
  mqtt-broker:
    command:
      - /usr/sbin/mosquitto
      - -v
      - -c
      - /mosquitto-no-auth.conf
    container_name: edgex-mqtt-broker
    hostname: edgex-mqtt-broker
    image: eclipse-mosquitto:2.0.18
    ports:
      - "1884:1884"
    networks:
      - edgex-network
    read_only: true
    restart: always
    security_opt:
      - no-new-privileges:true
    user: 2002:2001

  telegraf:
    image: telegraf:latest
    container_name: telegraf
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /home/pi/repo/edgex-compose/compose-builder/config/telegraf.conf:/etc/telegraf/telegraf.conf:ro
    restart: unless-stopped
    depends_on:
      mqtt-broker:
        condition: service_started
    networks:
      - edgex-network

``` 
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

### When not receiving data in your influx bucket check logs on:
- `docker logs telegraf`
- `docker logs mqtt-broker`
- `docker logs app-service-influxdb-export`

If there are exceptions try to remove it.

### References
- https://docs.edgexfoundry.org/3.1/microservices/application/ApplicationServices/

## Setup device service for reading modbus data
- Check if the modbus ip is public and try to bind to it
- When the plc/device is been binded on the modbus device see if you receive some data:  
  `docker logs edgex-device-modbus`
- Create a device profile, this explains how the data is been structured that will been received through the `edgex-device-modbus`. [see scipt for auto generating device profile file](./modbus/modbus_create_device_profile.py)
- Connect device service with device profile (provision if needed)
  Open the dashboard of edgex foundry on port 4000 and set this connection manually. 

  Hard to say which values are important we can accept all properties then we should create a script that will bind them on the profile.


## TODO: Set received Influx data on grafana