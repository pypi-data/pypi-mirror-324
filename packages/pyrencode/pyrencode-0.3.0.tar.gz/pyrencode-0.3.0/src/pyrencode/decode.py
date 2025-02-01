from __future__ import annotations

import struct
from string import digits
from typing import Any

from pyutilkit.classes import Singleton

from pyrencode import constants

string_bytes = {digit.encode() for digit in digits}


class Decoder(metaclass=Singleton):
    __slots__ = ()

    @classmethod
    def decode(  # type: ignore[misc]
        cls, bytes_obj: bytes, *, decode_utf8: bool = constants.DECODE_UTF8
    ) -> Any:  # noqa: ANN401
        try:
            obj, end_position = cls._decode(bytes_obj, decode_utf8=decode_utf8)
        except (IndexError, TypeError, KeyError, OverflowError) as exc:
            # We've tried to decode bytes that weren't properly encoded
            raise ValueError(str(exc)) from exc
        if end_position != len(bytes_obj):
            msg = f"extra data: {bytes_obj[end_position:]!r}"
            raise ValueError(msg)
        return obj

    @classmethod
    def _decode(  # type: ignore[misc]
        cls, bytes_obj: bytes, cursor: int = 0, *, decode_utf8: bool
    ) -> tuple[Any, int]:
        type_byte = bytes_obj[cursor : cursor + 1]
        if type_byte == constants.CHR_NONE:
            return None, cursor + 1
        if type_byte == constants.CHR_TRUE:
            return True, cursor + 1
        if type_byte == constants.CHR_FALSE:
            return False, cursor + 1
        if type_byte == constants.CHR_INT:
            return cls.decode_int(bytes_obj, cursor)
        if type_byte == constants.CHR_INT1:
            return cls.decode_int1(bytes_obj, cursor)
        if type_byte == constants.CHR_INT2:
            return cls.decode_int2(bytes_obj, cursor)
        if type_byte == constants.CHR_INT4:
            return cls.decode_int3(bytes_obj, cursor)
        if type_byte == constants.CHR_INT8:
            return cls.decode_int4(bytes_obj, cursor)
        if type_byte == constants.CHR_FLOAT32:
            return cls.decode_float32(bytes_obj, cursor)
        if type_byte == constants.CHR_FLOAT64:
            return cls.decode_float64(bytes_obj, cursor)
        if type_byte in string_bytes:
            return cls.decode_string(bytes_obj, cursor, decode_utf8=decode_utf8)
        if type_byte == constants.CHR_LIST:
            return cls.decode_list(bytes_obj, cursor, decode_utf8=decode_utf8)
        if type_byte == constants.CHR_DICT:
            return cls.decode_dict(bytes_obj, cursor, decode_utf8=decode_utf8)

        order = ord(type_byte)
        if constants.INT_POS_FIXED_START <= order <= constants.INT_POS_FIXED_END:
            return cls.decode_fixed_length_positive_integer(bytes_obj, cursor)
        if constants.INT_NEG_FIXED_START <= order <= constants.INT_NEG_FIXED_END:
            return cls.decode_fixed_length_negative_integer(bytes_obj, cursor)
        if constants.STR_FIXED_START <= order <= constants.STR_FIXED_END:
            return cls.decode_fixed_length_string(
                bytes_obj, cursor, decode_utf8=decode_utf8
            )
        if constants.LIST_FIXED_START <= order <= constants.LIST_FIXED_END:
            return cls.decode_fixed_length_list(
                bytes_obj, cursor, decode_utf8=decode_utf8
            )
        if constants.DICT_FIXED_START <= order <= constants.DICT_FIXED_END:
            return cls.decode_fixed_length_dict(
                bytes_obj, cursor, decode_utf8=decode_utf8
            )

        msg = f"unknown type byte: {type_byte!r}"
        raise ValueError(msg)

    @staticmethod
    def _decode_string(
        bytes_obj: bytes, cursor: int, length: int, *, decode_utf8: bool
    ) -> tuple[str | bytes, int]:
        new_cursor = cursor + length
        string = bytes_obj[cursor:new_cursor]
        if decode_utf8:
            return string.decode("utf8"), new_cursor

        return string, new_cursor

    @staticmethod
    def decode_int(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = bytes_obj.index(constants.CHR_TERM, cursor)
        if new_cursor - cursor >= constants.MAX_INT_LENGTH:
            msg = "int exceeds maximum length"
            raise OverflowError(msg)
        n = int(bytes_obj[cursor:new_cursor])
        if bytes_obj[cursor : cursor + 1] == b"-":
            if bytes_obj[cursor + 1 : cursor + 2] == b"0":
                msg = "negative zero in int"
                raise ValueError(msg)
        elif bytes_obj[cursor : cursor + 1] == b"0" and new_cursor != cursor + 1:
            msg = "leading zero in int"
            raise ValueError(msg)

        return n, new_cursor + 1

    @staticmethod
    def decode_int1(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 1
        return struct.unpack("!b", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_int2(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 2
        return struct.unpack("!h", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_int3(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 4
        return struct.unpack("!l", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_int4(bytes_obj: bytes, cursor: int) -> tuple[int, int]:
        cursor += 1
        new_cursor = cursor + 8
        return struct.unpack("!q", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_float32(bytes_obj: bytes, cursor: int) -> tuple[float, int]:
        cursor += 1
        new_cursor = cursor + 4
        return struct.unpack("!f", bytes_obj[cursor:new_cursor])[0], new_cursor

    @staticmethod
    def decode_float64(bytes_obj: bytes, cursor: int) -> tuple[float, int]:
        cursor += 1
        new_cursor = cursor + 8
        return struct.unpack("!d", bytes_obj[cursor:new_cursor])[0], new_cursor

    @classmethod
    def decode_string(
        cls, bytes_obj: bytes, cursor: int, *, decode_utf8: bool
    ) -> tuple[str | bytes, int]:
        colon = bytes_obj.index(b":", cursor)
        if bytes_obj[cursor : cursor + 1] == b"0" and colon != cursor + 1:
            msg = "leading zero in string length"
            raise ValueError(msg)

        length = int(bytes_obj[cursor:colon])
        return cls._decode_string(bytes_obj, colon + 1, length, decode_utf8=decode_utf8)

    @classmethod
    def decode_list(  # type: ignore[misc]
        cls, bytes_obj: bytes, cursor: int, *, decode_utf8: bool
    ) -> tuple[tuple[Any, ...], int]:
        output = []
        cursor += 1
        while bytes_obj[cursor : cursor + 1] != constants.CHR_TERM:
            value, cursor = cls._decode(bytes_obj, cursor, decode_utf8=decode_utf8)
            output.append(value)
        return tuple(output), cursor + 1

    @classmethod
    def decode_dict(  # type: ignore[misc]
        cls, bytes_obj: bytes, cursor: int, *, decode_utf8: bool
    ) -> tuple[dict[Any, Any], int]:
        output = {}
        cursor += 1
        while bytes_obj[cursor : cursor + 1] != constants.CHR_TERM:
            key, cursor = cls._decode(bytes_obj, cursor, decode_utf8=decode_utf8)
            output[key], cursor = cls._decode(
                bytes_obj, cursor, decode_utf8=decode_utf8
            )
        return output, cursor + 1

    @staticmethod
    def decode_fixed_length_positive_integer(
        bytes_obj: bytes, cursor: int
    ) -> tuple[int, int]:
        return bytes_obj[cursor], cursor + 1

    @staticmethod
    def decode_fixed_length_negative_integer(
        bytes_obj: bytes, cursor: int
    ) -> tuple[int, int]:
        return constants.INT_NEG_FIXED_START - bytes_obj[cursor] - 1, cursor + 1

    @classmethod
    def decode_fixed_length_string(
        cls, bytes_obj: bytes, cursor: int, *, decode_utf8: bool
    ) -> tuple[str | bytes, int]:
        length = bytes_obj[cursor] - constants.STR_FIXED_START
        return cls._decode_string(
            bytes_obj, cursor + 1, length, decode_utf8=decode_utf8
        )

    @classmethod
    def decode_fixed_length_list(
        cls, bytes_obj: bytes, cursor: int, *, decode_utf8: bool
    ) -> tuple[tuple[object, ...], int]:
        length = bytes_obj[cursor] - constants.LIST_FIXED_START
        output = []
        cursor += 1
        for _ in range(length):
            value, cursor = cls._decode(bytes_obj, cursor, decode_utf8=decode_utf8)
            output.append(value)
        return tuple(output), cursor

    @classmethod
    def decode_fixed_length_dict(
        cls, bytes_obj: bytes, cursor: int, *, decode_utf8: bool
    ) -> tuple[dict[object, object], int]:
        length = bytes_obj[cursor] - constants.DICT_FIXED_START
        output = {}
        cursor += 1
        for _ in range(length):
            key, cursor = cls._decode(bytes_obj, cursor, decode_utf8=decode_utf8)
            output[key], cursor = cls._decode(
                bytes_obj, cursor, decode_utf8=decode_utf8
            )
        return output, cursor


def loads(  # type: ignore[misc]
    bytes_obj: bytes, *, decode_utf8: bool = False
) -> Any:  # noqa: ANN401
    return Decoder.decode(bytes_obj, decode_utf8=decode_utf8)
