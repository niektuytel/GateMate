Refered on documentation: https://docs.edgexfoundry.org/2.1/microservices/device/profile/Ch-DeviceProfileRef/
Create json schema file for automating for the device profile:
```
{
  "DeviceProfile": {
    "fields": [
      {
        "name": "name",
        "type": "String",
        "required": true,
        "notes": "Must be unique in the EdgeX deployment. Only allow unreserved characters as defined in https://tools.ietf.org/html/rfc3986#section-2.3."
      },
      {
        "name": "description",
        "type": "String",
        "required": false,
        "notes": "Optional description of the device profile"
      },
      {
        "name": "manufacturer",
        "type": "String",
        "required": false,
        "notes": "Optional manufacturer information"
      },
      {
        "name": "model",
        "type": "String",
        "required": false,
        "notes": "Optional model information"
      },
      {
        "name": "labels",
        "type": "Array of String",
        "required": false,
        "notes": "Optional labels for categorization"
      },
      {
        "name": "deviceResources",
        "type": "Array of DeviceResource",
        "required": true,
        "notes": "Defines resources available on the device"
      },
      {
        "name": "deviceCommands",
        "type": "Array of DeviceCommand",
        "required": false,
        "notes": "Defines commands that operate on device resources"
      }
    ]
  },
  "DeviceResource": {
    "fields": [
      {
        "name": "name",
        "type": "String",
        "required": true,
        "notes": "Must be unique in the EdgeX deployment. Only allow unreserved characters as defined in https://tools.ietf.org/html/rfc3986#section-2.3."
      },
      {
        "name": "description",
        "type": "String",
        "required": false,
        "notes": "Optional description of the resource"
      },
      {
        "name": "isHidden",
        "type": "Bool",
        "required": false,
        "default": false,
        "notes": "Expose the DeviceResource to Command Service or not, default false"
      },
      {
        "name": "tag",
        "type": "String",
        "required": false,
        "notes": "Optional tag for additional metadata"
      },
      {
        "name": "attributes",
        "type": "String-Interface Map",
        "required": false,
        "notes": "Each Device Service should define required and optional keys"
      },
      {
        "name": "properties",
        "type": "ResourceProperties",
        "required": true,
        "notes": "Defines properties of the resource"
      }
    ]
  },
  "ResourceProperties": {
    "fields": [
      {
        "name": "valueType",
        "type": "Enum",
        "required": true,
        "notes": "Allowed values: Uint8, Uint16, Uint32, Uint64, Int8, Int16, Int32, Int64, Float32, Float64, Bool, String, Binary, Object, Uint8Array, Uint16Array, Uint32Array, Uint64Array, Int8Array, Int16Array, Int32Array, Int64Array, Float32Array, Float64Array, BoolArray"
      },
      {
        "name": "readWrite",
        "type": "Enum",
        "required": true,
        "notes": "Allowed values: R (read), W (write), RW (read-write)"
      },
      {
        "name": "units",
        "type": "String",
        "required": false,
        "notes": "Optional units of the value (e.g., Celsius, meters)"
      },
      {
        "name": "minimum",
        "type": "String",
        "required": false,
        "notes": "Error if SET command value is below this range"
      },
      {
        "name": "maximum",
        "type": "String",
        "required": false,
        "notes": "Error if SET command value exceeds this range"
      },
      {
        "name": "defaultValue",
        "type": "String",
        "required": false,
        "notes": "Default value compatible with the valueType"
      },
      {
        "name": "mask",
        "type": "String",
        "required": false,
        "notes": "Valid only for unsigned integer types"
      },
      {
        "name": "shift",
        "type": "String",
        "required": false,
        "notes": "Valid only for unsigned integer types"
      },
      {
        "name": "scale",
        "type": "String",
        "required": false,
        "notes": "Valid only for integer or float types"
      },
      {
        "name": "offset",
        "type": "String",
        "required": false,
        "notes": "Valid only for integer or float types"
      },
      {
        "name": "base",
        "type": "String",
        "required": false,
        "notes": "Valid only for integer or float types"
      },
      {
        "name": "assertion",
        "type": "String",
        "required": false,
        "notes": "Value to which the reading is compared"
      },
      {
        "name": "mediaType",
        "type": "String",
        "required": false,
        "notes": "Required when valueType is Binary"
      }
    ]
  },
  "DeviceCommand": {
    "fields": [
      {
        "name": "name",
        "type": "String",
        "required": true,
        "notes": "Must be unique in this profile. Only allow unreserved characters as defined in https://tools.ietf.org/html/rfc3986#section-2.3."
      },
      {
        "name": "isHidden",
        "type": "Bool",
        "required": false,
        "default": false,
        "notes": "Expose the DeviceCommand to Command Service or not, default false"
      },
      {
        "name": "readWrite",
        "type": "Enum",
        "required": true,
        "notes": "Allowed values: R (read), W (write), RW (read-write)"
      },
      {
        "name": "resourceOperations",
        "type": "Array of ResourceOperation",
        "required": true,
        "notes": "Defines operations on associated resources"
      }
    ]
  },
  "ResourceOperation": {
    "fields": [
      {
        "name": "deviceResource",
        "type": "String",
        "required": true,
        "notes": "Name of the associated DeviceResource"
      },
      {
        "name": "defaultValue",
        "type": "String",
        "required": false,
        "notes": "Default value compatible with the associated DeviceResource"
      },
      {
        "name": "mappings",
        "type": "String-String Map",
        "required": false,
        "notes": "Maps GET resourceOperation values to other strings"
      }
    ]
  }
}
```
