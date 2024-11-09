# GateMate
With gate mate you can connect any connection and pass it trough other configured connections to parse data through

## Data models:
- Connections -> Represents connections to Modbus, OPC-UA, or other systems.
  - Id (Unique INT)
  - Name (VARCHAR 50 e.g. "Modbus_Sensor_1")
  - Description (VARCHAR 1000: Optional description about the connection)
  - Status (INT Enum: Active, Inactive, Error)
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
    - Database: ```
      {
        "ConnectionString": "Server=.;Database=TestDB;",
        "Authentication": "Integrated"
      }```
  - LastUpdated (DATETIME UTC: Timestamp of the last update)
    
- DataStreams -> Manages data transfer between connections
  - Id (Unique INT)
  - Name (VARCHAR 150 e.g. "Parse data from Modbus_Sensor_1 to Modbus_Server_2")
  - Status (INT Enum: Active, Paused, Error)
  - ReadConnectionId (INT FK)
  - WriteConnectionId (INT FK)
  - PollingIntervalMs (INT, Default=0): How often data is read (in milliseconds).
  - ErrorRetries (INT, Default=0): Number of retries before marking the stream as errored.
  - ErrorRetryDelayInSeconds (INT): Time to wait between retries (default = 5).
  - IsSpecificTagTransfer (BOOLEAN): When ReadTag/WriteTag is null or empty
  - ReadTag (VARCHAR 100, Nullable): Optional tag or identifier for reading.
  - WriteTag (VARCHAR 100, Nullable): Optional tag or identifier for writing.
  - LastUpdated (DATETIME UTC)
    
- Logs -> Use this for tracking issues ower system diagnostics.
  - Id (Unique INT)
  - LogType (INT Enum: Info, Warning, Error)
  - Timestamp (DATETIME UTC): When the event occurred.
  - DataStreamId (INT FK, Nullable): Optional link to a data stream.
  - ConnectionId (INT FK, Nullable): Optional link to a connection.
  - Message (VARCHAR 1000): Description of the event.

## Storage
We use a embedded database SQLite for storing data.

## Logging Keep limited
Before the logging goes into a WildGrowing table in rows we set a Maximum row.
Use for now a SQLite Triggers see the example: 
```
CREATE TRIGGER MaintainLogLimit
AFTER INSERT ON Logs
BEGIN
    DELETE FROM Logs
    WHERE Id IN (
        SELECT Id FROM Logs ORDER BY Timestamp ASC LIMIT (SELECT COUNT(*) - 1000 FROM Logs)
    );
END;
```

## The Hybride caching approach
The hybrid approach caching data in memory and writing to a database only when persistence is required.

### Data Buffering in Gateways:
Use memory for short-term data retention before sending it to the cloud.
Persist critical data (e.g., alarms or trends) locally in a database if the cloud is temporarily unreachable.

### Selective Persistence:
Not all data is stored—only selected metrics or events are logged, reducing overhead.

