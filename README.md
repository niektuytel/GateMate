# GateMate

Data models:
- Connections -> Represents connections to Modbus, OPC-UA, or other systems.
  - Id (Unique INT)
  - Name (VARCHAR 50 e.g. "Modbus_Sensor_1")
  - Description (VARCHAR 1000: Optional description about the connection)
  - Status (INT Enum: Active, Inactive, Error)
  - StatusMessage (VARCHAR 1000: Optional feedback on the status)
  - ProtocolType (INT Enum: ModbusRTU, ModbusTCP, OPC_UA, Database)
  - ProtocolSettings (TEXT)
    - ModbusRTU: ```
      {
        "BaudRate": 9600,
        "DataBits": 8,
        "StopBits": 1,
        "Parity": "None",
        "SlaveAddress": 1
      }```
    - OPC-UA: ```
      {
        "EndpointURL": "opc.tcp://127.0.0.1",
        "NodeID": "ns=2;s=MotorSpeed",
        "SecurityPolicy": "Basic256"
      }```
    - Database: ```{
        "ConnectionString": "Server=.;Database=TestDB;",
        "Authentication": "Integrated"
      }```
  - LastUpdated (DATETIME UTC: Timestamp of the last update)
- Devices -> Represents a physical device in the system. Is this really been needed?






