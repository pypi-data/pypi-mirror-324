from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from pyrencode import constants
from pyrencode.utils import to_bytes

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping, Sequence


class Encoder:
    __slots__ = ()

    @classmethod
    def encode(
        cls, obj: object, *, float_bits: int = constants.DEFAULT_FLOAT_BITS
    ) -> bytes:
        if float_bits not in {32, 64}:
            msg = f"Float bits {float_bits} is not 32 or 64"
            raise ValueError(msg)
        return b"".join(cls._encode(obj, float_bits))

    @classmethod
    def _encode(cls, obj: object, float_bits: int) -> Iterator[bytes]:
        if obj is None:
            yield constants.CHR_NONE
        elif obj is True:
            yield constants.CHR_TRUE
        elif obj is False:
            yield constants.CHR_FALSE
        elif isinstance(obj, int):
            yield from cls.encode_int(obj)
        elif isinstance(obj, float):
            if float_bits == 32:  # noqa: PLR2004
                yield from cls.encode_float32(obj)
            else:
                yield from cls.encode_float64(obj)
        elif isinstance(obj, bytes):
            yield from cls.encode_bytes(obj)
        elif isinstance(obj, (list, tuple)):
            yield from cls.encode_list(obj, float_bits)
        elif isinstance(obj, dict):
            yield from cls.encode_dict(obj, float_bits)
        elif isinstance(obj, str):
            yield from cls.encode_string(obj)
        else:
            msg = f"Object {obj} cannot be rencoded."
            raise TypeError(msg)

    @staticmethod
    def encode_int(obj: int) -> Iterator[bytes]:
        if 0 <= obj < constants.INT_POS_FIXED_COUNT:
            yield to_bytes(constants.INT_POS_FIXED_START + obj)
        elif -constants.INT_NEG_FIXED_COUNT <= obj < 0:
            yield to_bytes(constants.INT_NEG_FIXED_START - 1 - obj)
        elif -constants.INT1_SIZE <= obj < constants.INT1_SIZE:
            yield constants.CHR_INT1
            yield struct.pack("!b", obj)
        elif -constants.INT2_SIZE <= obj < constants.INT2_SIZE:
            yield constants.CHR_INT2
            yield struct.pack("!h", obj)
        elif -constants.INT4_SIZE <= obj < constants.INT4_SIZE:
            yield constants.CHR_INT4
            yield struct.pack("!l", obj)
        elif -constants.INT8_SIZE <= obj < constants.INT8_SIZE:
            yield constants.CHR_INT8
            yield struct.pack("!q", obj)
        else:
            yield constants.CHR_INT

            int_as_bytes = bytes(str(obj), "ascii")
            yield int_as_bytes
            if len(int_as_bytes) >= constants.MAX_INT_LENGTH:
                msg = f"Integer {obj} is too big to be rencoded."
                raise OverflowError(msg)

            yield constants.CHR_TERM

    @staticmethod
    def encode_float32(obj: float) -> Iterator[bytes]:
        yield constants.CHR_FLOAT32
        yield struct.pack("!f", obj)

    @staticmethod
    def encode_float64(obj: float) -> Iterator[bytes]:
        yield constants.CHR_FLOAT64
        yield struct.pack("!d", obj)

    @staticmethod
    def encode_bytes(obj: bytes) -> Iterator[bytes]:
        if len(obj) < constants.STR_FIXED_COUNT:
            yield to_bytes(constants.STR_FIXED_START + len(obj))
        else:
            yield str(len(obj)).encode()
            yield b":"
        yield obj

    @classmethod
    def encode_string(cls, obj: str) -> Iterator[bytes]:
        yield from cls.encode_bytes(obj.encode())

    @classmethod
    def encode_list(cls, obj: Sequence[object], float_bits: int) -> Iterator[bytes]:
        if len(obj) < constants.LIST_FIXED_COUNT:
            yield to_bytes(constants.LIST_FIXED_START + len(obj))
            for item in obj:
                yield from cls._encode(item, float_bits)
        else:
            yield constants.CHR_LIST
            for item in obj:
                yield from cls._encode(item, float_bits)
            yield constants.CHR_TERM

    @classmethod
    def encode_dict(
        cls, obj: Mapping[object, object], float_bits: int
    ) -> Iterator[bytes]:
        if len(obj) < constants.DICT_FIXED_COUNT:
            yield to_bytes(constants.DICT_FIXED_START + len(obj))
            for key, value in obj.items():
                yield from cls._encode(key, float_bits)
                yield from cls._encode(value, float_bits)
        else:
            yield constants.CHR_DICT
            for key, value in obj.items():
                yield from cls._encode(key, float_bits)
                yield from cls._encode(value, float_bits)
            yield constants.CHR_TERM


def dumps(obj: object, float_bits: int = constants.DEFAULT_FLOAT_BITS) -> bytes:
    return Encoder.encode(obj, float_bits=float_bits)
