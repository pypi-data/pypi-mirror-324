"""
Fast Communication Interface.

FastCI is a lightweight, efficient and developer-friendly communication
interface, enabling seamless communication between distributed systems.
By leveraging MQTT [1]_ for messaging and Protocol Buffers [2]_ for data
serialization, this interface ensures fast, reliable, and bandwidth-efficient
communication. Its simplicity in setup and development makes it ideal for
both small-scale and enterprise-level applications.

To enable the "request-response" pattern, the use of MQTT v5 is mandatory.

References
----------
.. [1] https://mqtt.org
.. [2] https://protobuf.dev/
"""

__all__ = ["OS_NAME", "OS_NAME_WINDOWS", "CIRouter", "FastCI", "QoS"]

from .application import CIRouter, FastCI
from .utilities.constants import OS_NAME, OS_NAME_WINDOWS
from .utilities.mqtt import QoS
