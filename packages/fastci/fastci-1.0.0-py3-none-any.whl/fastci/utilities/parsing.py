"""Module implementing parsing functions."""

from __future__ import annotations

import struct
import typing

if typing.TYPE_CHECKING:
    from fastci.utilities.type_definitions import Packet

from google.protobuf.message import Message


def bytes_to_packet(payload: bytes, packet_type: type[Packet]) -> Packet:
    """Convert bytes to a packet.

    Parameters
    ----------
    payload
        Bytes to convert.

    Returns
    -------
    Packet
        Parsed packet.
    """
    if issubclass(packet_type, Message):
        packet = packet_type()
        packet.ParseFromString(payload)
        return packet

    if issubclass(packet_type, str):
        return payload.decode()

    if issubclass(packet_type, int):
        return int.from_bytes(payload)

    if issubclass(packet_type, float):
        return struct.unpack("f", payload)[0]  # type: ignore [no-any-return]

    return payload
