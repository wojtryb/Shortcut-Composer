from typing import Any, Dict, Set, Iterable, Tuple, Type, Generic, TypeVar
from enum import Enum
T = TypeVar("T", bound=Enum)


class EnumGroupMeta(type, Generic[T]):
    """
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

    def __init__(
        self,
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, Any]
    ) -> None:
        super().__init__(name, bases, attrs)

        self._grouped_enums_ = MetaInit.get_enum_types(attrs)
        """Dictionary mapping grouped enum types to their names."""
        MetaInit.ensure_common_base(self._grouped_enums_.values())

        self._member_map_ = MetaInit.init_member_map(self._grouped_enums_)
        """Dictionary mapping enum members to their names."""

        self._value2member_map_ = MetaInit.init_reverse_map(self._member_map_)
        """Dictionary mapping enum members to their values."""

    def __getattr__(self, name: str) -> T:
        """Return enum member as attribute of the composite."""
        return self._member_map_[name]

    def __getitem__(self, name: str) -> T:
        """Return enum member by its name."""
        return self._member_map_[name]

    def __call__(self, value: str) -> T:
        """Return enum member by its value."""
        return self._value2member_map_[value]


class MetaInit:
    """Organizes methods used by EnumGroupMeta."""

    @staticmethod
    def get_enum_types(attrs: Dict[str, Any]) -> Dict[str, Type[Enum]]:
        """Filter attribute dict leaving only enum types."""
        def is_enum_type(value: Any) -> bool:
            """Return True when value is a class and inherits Enum."""
            return isinstance(value, type) and issubclass(value, Enum)

        return {name: val for name, val in attrs.items() if is_enum_type(val)}

    @classmethod
    def init_member_map(cls, enum_types: Dict[str, Type[Enum]]):
        """Return dict mapping enum members to their names."""
        # maps enum values to their names from all the passed types
        member_map = {}
        for enum in enum_types.values():

            # raise an error when two enum types define the same name
            if common := cls.common_keys(member_map, enum._member_map_):
                raise RuntimeError(f"Enums have repeated keys: {common}")

            # update dictionary
            args = {name: val for name, val in enum._member_map_.items()}
            member_map.update(args)

        return member_map

    @staticmethod
    def init_reverse_map(member_map: dict):
        """Return dict mapping enum members to their values."""
        reverse_map = {}
        for value in member_map.values():
            if value not in reverse_map.values():
                reverse_map[value.value] = value
        return reverse_map

    @staticmethod
    def common_keys(dict_1: dict, dict_2: dict) -> Set:
        """Return the set of common keys of two dictionaries."""
        keys_1 = set(dict_1.keys())
        keys_2 = set(dict_2.keys())
        return keys_1.intersection(keys_2)

    @staticmethod
    def ensure_common_base(enum_types: Iterable[Type[Enum]]) -> None:
        """
        Return common base class of given enum types.

        Raise exception when their bases are not exactly the same.
        """
        enum_bases = [enum.__base__ for enum in enum_types]
        if not enum_bases[:-1] == enum_bases[1:]:
            raise RuntimeError("All enums must have the same base.")
