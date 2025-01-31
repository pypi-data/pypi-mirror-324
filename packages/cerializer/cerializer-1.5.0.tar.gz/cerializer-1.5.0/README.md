# Cerializer

![PyPI](https://img.shields.io/pypi/v/Cerializer)

Cerializer is an Avro de/serialization library that aims at providing an even faster alternative to FastAvro and Avro standard library.

This speed increase does not come without a cost. Cerializer will work only with predefined set of schemata for which it will generate tailor made Cython code. This way, the overhead caused by the universality of other serialization libraries will be avoided.

Special credit needs to be given to [FastAvro](https://github.com/fastavro/fastavro) library, by which is this project heavily inspired.

## Example of a schema and the corresponding code

SCHEMA
```python
{
    'name': 'array_schema',
    'doc': 'Array schema',
    'namespace': 'cerializer',
    'type': 'record',
    'fields': [
        {
            'name': 'order_id',
            'doc': 'Id of order',
            'type': 'string'
        },
        {
            'name': 'trades',
            'type': {
                'type': 'array',
                'items': ['string', 'int']
            }
        }
    ]
}
```

CORRESPONDING CODE
```python
def serialize(data, output):
    cdef bytearray buffer = bytearray()
    cdef dict datum
    cdef str type_0
    write.write_string(buffer, data['order_id'])
    if len(data['trades']) > 0:
        write.write_long(buffer, len(data['trades']))
        for val_0 in data['trades']:
            if type(val_0) is tuple:
                type_0, val_1 = val_0

                if type_0 == 'string':
                    write.write_long(buffer, 0)
                    write.write_string(buffer, val_1)

                elif type_0 == 'int':
                    write.write_long(buffer, 1)
                    write.write_int(buffer, val_1)

            else:
                if type(val_0) is str:
                    write.write_long(buffer, 0)
                    write.write_string(buffer, val_0)
                elif type(val_0) is int:
                    write.write_long(buffer, 1)
                    write.write_int(buffer, val_0)
    write.write_long(buffer, 0)
    output.write(buffer)



def deserialize(fo):
    cdef long long i_0
    cdef long long i_1
    cdef long i_2
    data = {}
    data['order_id'] = read.read_string(fo)
    data['trades'] = []

    i_1 = read.read_long(fo)
    while i_1 != 0:
        if i_1 < 0:
            i_1 = -i_1
            read.read_long(fo)
        for i_0 in range(i_1):
            i_2 = read.read_int(fo)
            if i_2 == 0:
                val_2 = read.read_string(fo)
            if i_2 == 1:
                val_2 = read.read_int(fo)
            data['trades'].append(val_2)
        i_1 = read.read_long(fo)
    return data
```


## Usage Example
1. Create an instance of CerializerSchemata
For initializing CerializerSchemata it is necessary to supply a list of tuples in form of (schema_identifier, schema)
where schema_identifier is a string and schema is a dict representing the Avro schema.
schema tuple = (namespace.schema_name, schema). eg.:
    ```python
    import cerializer.schema_handler
    import os
    import yaml
    
    def list_schemata():
        # iterates through all your schemata and yields schema_identifier and path to schema folder
        raise NotImplemented
    
    def schemata() -> cerializer.schema_handler.CerializerSchemata:
        schemata = []
        for schema_identifier, schema_root in list_schemata():
            schema_tuple = schema_identifier, yaml.unsafe_load( # type: ignore
                open(os.path.join(schema_root, 'schema.yaml'))
            )
            schemata.append(schema_tuple)
        return cerializer.schema_handler.CerializerSchemata(schemata)
    ```

2. Create an instance of Cerializer for each of your schemata by calling `cerializer_handler.Cerializer`.
eg. `cerializer_instance = cerializer_handler.Cerializer(cerializer_schemata, schema_namespace, schema_name)`
This will create an instance of Cerializer that can serialize and deserialize data in the particular schema format.

3. Use the instance accordingly.
    eg.:
    ```python
    data_record = {
        'order_id': 'aaaa',
        'trades': [123, 456, 765]
    }
    
    cerializer_instance = cerializer.cerializer_handler.Cerializer(cerializer_schemata, 'school', 'student')
    serialized_data = cerializer_instance.serialize(data_record)
    print(serialized_data)
    ```

Serialized data
```
b'\x08aaaa\x06\x02\xf6\x01\x02\x90\x07\x02\xfa\x0b\x00'
```

You can also use `serialize_into` if you already have an IO buffer:

```python
output = io.BytesIO()
cerializer_instance.serialize_into(output, data_record)
print(output.getvalue())
```

## Benchmark
```
cerializer.default_schema:3            2.5661 times faster,   0.0209s : 0.0082s
cerializer.fixed_decimal_schema:1      1.2795 times faster,   0.1588s : 0.1241s
cerializer.int_date_schema:1           2.8285 times faster,   0.0273s : 0.0097s
cerializer.plain_int:1                 2.2334 times faster,   0.0146s : 0.0065s
cerializer.timestamp_schema_micros:1   2.3759 times faster,   0.0577s : 0.0243s
cerializer.default_schema:2            2.8129 times faster,   0.0240s : 0.0085s
cerializer.array_schema:3              1.2177 times faster,   0.3088s : 0.2536s
cerializer.timestamp_schema:1          2.5928 times faster,   0.0577s : 0.0223s
cerializer.array_schema:2              1.4756 times faster,   0.6542s : 0.4434s
cerializer.union_schema:1              3.0796 times faster,   0.0284s : 0.0092s
cerializer.bytes_decimal_schema:1      1.8449 times faster,   0.0490s : 0.0266s
cerializer.array_schema:1              2.1771 times faster,   0.0344s : 0.0158s
cerializer.string_uuid_schema:1        1.8887 times faster,   0.0494s : 0.0262s
cerializer.map_schema:2                2.0896 times faster,   0.0331s : 0.0158s
cerializer.fixed_schema:1              3.4042 times faster,   0.0213s : 0.0062s
cerializer.long_time_micros_schema:1   2.3747 times faster,   0.0352s : 0.0148s
cerializer.array_schema:4              2.8779 times faster,   0.0591s : 0.0205s
cerializer.default_schema:1            2.0182 times faster,   0.0393s : 0.0195s
cerializer.map_schema:1                3.4610 times faster,   0.0597s : 0.0172s
cerializer.string_schema:1             2.2048 times faster,   0.0352s : 0.0159s
cerializer.reference_schema:1          2.9309 times faster,   0.1525s : 0.0520s
cerializer.enum_schema:1               3.0065 times faster,   0.0217s : 0.0072s
cerializer.tree_schema:1               4.0494 times faster,   0.0869s : 0.0215s
cerializer.huge_schema:1               2.8161 times faster,   0.1453s : 0.0516s
AVERAGE: 1.7814 times faster
```

Measured against Fastavro using the benchmark in Cerializer/tests.

Device: ASUS ZenBook 14 UM425QA, AMD Ryzen 7 5800H, 16 GB 2133 MHz LPDDR4X
