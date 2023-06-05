from typing import Dict, List, Tuple, TypeVar, Callable
from enum import Enum, EnumMeta
T = TypeVar("T", bound=Enum)


class EnumGroupMeta(EnumMeta):
    """
    TODO: rewrite documentation
    Metaclass for creating enum groups.

    Intended use is to place enum definitions inside a class definition:
    ```
    class EnumGroup(metaclass=EnumGroupMeta[Enum]):
        class EnumA(Enum):
            ASD = "asd"
            QWE = "qwe"

        class EnumB(Enum):
            Z = "z"
            X = "x"
    ```
    Metaclass makes its instance act as a composite of all the grouped
    enums. Although the instance technically is not an Enum subclass,
    it provides the following Enum class attributes:
    - `_member_map_`
    - `_value2member_map_`

    Enum members can be fetched in multiple ways:
        - Using the original, grouped Enum class:
            - EnumGroup.EnumA.ASD
            - EnumGroup.EnumA["ASD"]
            - EnumGroup.EnumA("asd")

        - Using the composite class directly:
            - EnumGroup.ASD
            - EnumGroup["ASD"]
            - EnumGroup("asd")

    Grouped enum types must follow those rules:
    - All passed enum types must inherit directly from the same Enum.
    - Grouped enums cannot define the same names.

    Breaking those rules will result in exception during class creation.

    Grouped enums do not need to directly inherit from Enum.
    Metaclass is a Generic - for typing purposes, base class of grouped
    enum types should also be passed to the metaclass.
    """

    _groups_: Dict[str, 'Group']

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs
    ) -> 'EnumGroupMeta':
        active_separator = None
        groups: Dict[str, Group] = {}
        for key, value in attrs.copy().items():
            if isinstance(value, Group):
                attrs._member_names.remove(key)
                active_separator = value
                groups[active_separator.name] = active_separator
            elif not isinstance(value, Callable):
                if active_separator is not None:
                    active_separator.keys.add(key)

        new_class = super().__new__(cls, name, bases, attrs)
        new_class._groups_ = groups
        for group in groups.values():
            setattr(new_class, group.name, group)
        return new_class

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for group in self._groups_.values():
            for key in group.keys:
                group.append(self[key])  # type: ignore


class Group(List[Enum]):
    def __init__(self, name: str) -> None:
        self.name = name
        self.keys = set()


class EnumGroup(Enum, metaclass=EnumGroupMeta):
    pass


# class MyEnum(EnumGroup):
#     _fruit = Group("Fruit")
#     QWE = 0
#     ASD = 1

#     _vegetable = Group("Vegetable")
#     Z = 2

#     _other = Group("Other")
#     X = 3

#     def foo(self):
#         return f"{self.name}_{self.value}"


# print(MyEnum.QWE)
# print(MyEnum.QWE.foo())
# print(MyEnum["QWE"])
# print(MyEnum(0))
# print(MyEnum._fruit)
# print(MyEnum._vegetable)
# print(MyEnum._other)
# print(MyEnum._member_map_)
# print(MyEnum._value2member_map_)
# print(MyEnum.QWE in MyEnum._fruit)  # type: ignore
# print()
# for name, group in MyEnum._groups_.items():
#     print(name, group)
