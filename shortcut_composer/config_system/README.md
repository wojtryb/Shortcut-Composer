### Config system
Package `config_system` consists of `Field` and `FieldGroup` which grant object-oriented API to control kritarc configuration file easier, than with API of krita.

---

`Field` represents a single value in kritarc file. Once initialized with its group name, name and default value, it allows to:
- write a given value to kritarc.
- read current value from kritarc, parsing it to correct python type.
- reset the value to default.
- register a callback run on each value change.

Type of default value passed on initialization is remembered, and used to parse values both on read and write. Supported types are:
- `int`, `list[int]`,
- `float`, `list[float]`,
- `str`, `list[str]`,
- `bool`, `list[bool]`,
- `Enum`, `list[Enum]`

For empty, homogeneous lists, `parser_type` argument must be used to determine type of list elements. Default values are not saved when until the field does not exist in kritarc. Repeated saves of the same value are filtered, so that callbacks are not called when the same value is written multiple times one after the other.

---

`FieldGroup` represents a section of fields in kritarc file. It simplifies the field creation by auto-completing the group name.

FieldGroup holds and aggregates fields created with it. It allows to reset all the fields at once, and register a callback to all its fields: both existing and future ones.

---

Example usage:
```python
from enum import Enum
from config_system import FieldGroup


class EnumMock(Enum):
    MODE_A = 0
    MODE_B = 1

# Create a config group
group = FieldGroup("MyGroup")
# Register a callback on all three fields
group.register_callback(lambda: print("any field changed"))

# Create three fields inside a group - for string and two enum lists
str_field = group.field(name="my_str", default="Sketch")
enums_field_1 = group.field("my_enums_1", [], parser_type=EnumMock)
enums_field_2 = group.field("my_enums_2", [EnumMock.MODE_A])

# Register a different callback on each field
str_field.register_callback(lambda: print("string changed"))
enums_field_1.register_callback(lambda: print("enum 1 changed"))
enums_field_2.register_callback(lambda: print("enum 2 changed"))

# Change the value from default "Sketch" to "Digital"
str_field.write("Digital")
# Change the value from empty list to one with two values
enums_field_1.write([EnumMock.MODE_A, EnumMock.MODE_B])
# Repeat the default value. Will be filtered
enums_field_2.write([EnumMock.MODE_A])

# The program will not break, as red values are the same as written ones
assert str_field.read() == "Digital"
assert enums_field_1.read() == [EnumMock.MODE_A, EnumMock.MODE_B]
assert enums_field_2.read() == [EnumMock.MODE_A]
```

The code above produces "MyGroup" section in kritarc file. my_enums_2 is missing, as the default value was not changed:
```
[MyGroup]
my_str=Digital
my_enums_1=MODE_A\tMODE_B
```

Registered callbacks outputs on the terminal:
```
any field changed
string changed
any field changed
enum 1 changed
```

Calling `group.reset_defaults()` would change both values back to their defaults, and produce the same output on the terminal, as resetting changes the fields.
