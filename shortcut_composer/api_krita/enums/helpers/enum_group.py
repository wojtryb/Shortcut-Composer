from typing import Any, Dict, Set, Tuple, Type
from enum import Enum


class EnumGroupMetaclass(type):
    """Metaclass for creating enum groups. See EnumGroup documentation."""

    def __init__(
        self,
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, Any]
    ) -> None:
        super().__init__(name, bases, attrs)

        self._enums_ = MetaclassTools.get_enum_types(attrs)
        """Dictionary mapping enum types to their names."""

        self._compound_ = MetaclassTools.create_compound(self._enums_)
        """Enum containing elements of all grouped enums."""


class MetaclassTools:
    """Organizes methods used by EnumGroupMetaclass."""

    @staticmethod
    def get_enum_types(attrs: Dict[str, Any]) -> Dict[str, Type[Enum]]:
        """Filter attribute dict leaving only enum types."""
        def is_enum_type(value: Any) -> bool:
            """Return True when value is a class and inherits Enum."""
            return isinstance(value, type) and issubclass(value, Enum)

        return {name: val for name, val in attrs.items() if is_enum_type(val)}

    @classmethod
    def create_compound(cls, enum_types: Dict[str, Type[Enum]]) -> Type[Enum]:
        """Combine passed enums types into single enum."""
        # maps enum values to their names from all the passed types
        compound_attrs = {}
        for enum in enum_types.values():

            # raise an error when two enum types define the same name
            if common := cls.common_keys(compound_attrs, enum._member_map_):
                raise RuntimeError(f"Enums have repeated keys: {common}")

            # update dictionary
            args = {name: val.value for name, val in enum._member_map_.items()}
            compound_attrs.update(args)

        # dynamically create enum composite keeping the same base class
        enum_base = cls.get_enum_base(enum_types)
        return enum_base("Compound", compound_attrs)

    @staticmethod
    def common_keys(dict_1: dict, dict_2: dict) -> Set:
        """Return the set of common keys of two dictionaries."""
        keys_1 = set(dict_1.keys())
        keys_2 = set(dict_2.keys())
        return keys_1.intersection(keys_2)

    @staticmethod
    def get_enum_base(enum_types: Dict[str, Type[Enum]]) -> Type[Enum]:
        """
        Return common base class of given enum types.

        Raise exception when their bases are not exactly the same.
        """
        enum_bases = [enum.__base__ for enum in enum_types.values()]
        if not enum_bases[:-1] == enum_bases[1:]:
            raise RuntimeError("All enums must have the same base.")
        return enum_bases[0] if enum_bases else Enum


class EnumGroup(metaclass=EnumGroupMetaclass):
    """
    Base class for creating enum groups.

    Intended use is to place enum definitions inside a subclass:
    ```
    class CustomEnumGroup(EnumGroup):
        class EnumA(Enum):
            ASD = "asd"
            QWE = "qwe"

        class EnumB(Enum):
            Z = "z"
            X = "x"
    ```
    Child class automatically provides following class attributes:
    - `_compound_` - dynamically created enum containing elements of
      all grouped enums.
    - `_enums_` - dictionary mapping enum types to their names.

    Grouped enums do not need to directly inherit from Enum. If subclass
    of enum is used, the composite will also be based on the same class.

    Grouped enum types must follow those rules:
    - All passed enum types must inherit directly from the same class.
    - Enums cannot define the same names.

    Breaking those rules will result in exception during class creation.
    """
