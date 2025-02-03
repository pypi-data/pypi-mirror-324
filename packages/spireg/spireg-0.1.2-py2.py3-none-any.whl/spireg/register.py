""" Register class for SPI communication. """

from ctypes import c_uint8
from dataclasses import dataclass
from typing import List

from bitstring import BitArray


@dataclass
class Entry:
    """ A single entry within a register. Wraps one or more bits. """
    name: str
    length: int
    default: int = 0


class Register:
    """ Base class for registers """
    name: str
    register: c_uint8
    description: str
    _fields: List[Entry]
    _fieldnames: List[str]
    _data: BitArray

    def __init__(self, name, register, description, fields, value=0):
        self.name = name
        self.register = register
        self.description = description
        self._fields = fields
        self._fieldnames = [field.name for field in fields]
        self._data = BitArray(uint=value, length=8)

        # Dynamically add properties for each field
        for field in fields:
            self._add_property(field)
            start, length = self._getentry(field.name)
            if not 0 <= field.default < (1 << field.length):
                raise ValueError(
                    f"{field.name} must be between 0 and {1 << length - 1}.")
            self._data[start: start + length] = field.default

    def _getentry(self, name: str):
        if name in self._fieldnames:
            start = sum(
                field.length for field in self._fields[: self._fieldnames.index(name)]
            )
            length = next(field.length for field in self._fields if field.name == name)
            return start, length
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _add_property(self, field: Entry):
        def getter(self):
            start, length = self._getentry(field.name)
            return self._data[start: start + length].uint

        def setter(self, value):
            start, length = self._getentry(field.name)
            if not 0 <= value < (1 << length):  # Ensure value fits in the field
                raise ValueError(
                    f"{field.name} must be between 0 and {1 << length - 1}.")
            self._data[start: start + length] = value

        setattr(self.__class__, field.name, property(getter, setter))

    def __int__(self):
        return self._data.uint

    def __str__(self):
        return f"Bits: {self._data.bin}, " + ", ".join(
            f"{name}: {getattr(self, name)}" for name in self._fieldnames
        )
