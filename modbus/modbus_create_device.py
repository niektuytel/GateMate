import yaml
import re

# TODO: create scripts so the device can read all Events inplace of 1

# on edge-compose compose-builder: "make gen no-secty arm64 ds-modbus asc-metrics ds-virtual asc-sample"


# https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?org=GateMate&bucket=Machinova_Test&precision=ns


# Leer meer op: https://docs.edgexfoundry.org/3.1/microservices/application/ApplicationServices/


# app service influx 
# go mod tidy
# docker build --platform linux/arm64 -t app-influx-mqtt:3.1_arm64 .
#  
# Define on docker compose the image 
# version: '3.8'
# services:
#   app-influx-mqtt:
#     image: app-influx-mqtt:3.1_arm64  # Use the locally built image
#     ports:
#       - "59798:59798"             # Map container's port to host
#     environment:
#       - EDGEX_SECURITY_SECRET_STORE=false
#     depends_on:
#       - edgex-core-consul          # Ensure dependent services start first
#     volumes:
#       - ./res:/res                 # Mount configuration files
# 
# 
# 
# 
#  

