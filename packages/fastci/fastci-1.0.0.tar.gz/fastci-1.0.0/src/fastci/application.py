"""Module implementing a communication interface on top `MQTT` [1]_.

References
----------
.. [1] https://mqtt.org
"""

from __future__ import annotations

import inspect
import logging
import types
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from fastci.utilities.type_aliases import Routable

import aiomqtt
from google.protobuf.message import Message

from fastci.utilities.annotations import find_parameter_by_type_annotation
from fastci.utilities.mqtt import QoS
from fastci.utilities.parsing import bytes_to_packet
from fastci.utilities.type_definitions import Packet

_logger = logging.getLogger(__name__)


class CIRouter:
    """Router for communication interface endpoints.

    Parameters
    ----------
    prefix
        Prefix for all endpoints.
    """

    def __init__(self, *, prefix: str | None = None) -> None:
        self._prefix = prefix
        self._routes: dict[str, dict[int, list[Routable]]] = {}
        self._injectors: dict[str, typing.Any] = {}

    @property
    def routes(self) -> dict[str, dict[int, list[Routable]]]:
        """Return all registered routes.

        Returns
        -------
        dict[str, dict[int, list[Routable]]]
            All registered routes.
        """
        return self._routes

    @property
    def injectors(self) -> dict[str, typing.Any]:
        """Return all registered injectors.

        Returns
        -------
        dict[str, Any]
            All registered injectors.
        """
        return self._injectors

    def route(
        self,
        topic: str,
        *,
        qos: QoS = QoS.AT_MOST_ONCE,
    ) -> Callable[[Routable], Routable]:
        """Register a (MQTT-) route.

        Parameters
        ----------
        topic
            MQTT topic to subscribe and assign the function to.
        qos
            Quality of Service level for the subscription.

        Returns
        -------
        Callable[[Routable], Routable]
            Decorated callable.
        """

        def decorator(routable: Routable) -> Routable:
            self.__validate_routable(routable)

            if topic not in self._routes:
                self._routes[topic] = {}

            if qos not in self._routes[topic]:
                self._routes[topic][qos] = []

            self._routes[topic][qos].append(routable)

            return routable

        return decorator

    def include_router(self, router: CIRouter) -> None:
        """Include routes and injectors from another router.

        Parameters
        ----------
        router
            Router to include routes from.
        """
        self._routes.update(router.routes)
        self.add_injectors(**router.injectors)

    def add_injectors(self, **kwargs: typing.Any) -> None:  # noqa: ANN401
        """Add an injector to the router.

        Injectors are passed to the decorated routes as keyword arguments.

        Parameters
        ----------
        kwargs
            Key-value pairs of injectors.
        """
        self._injectors.update(kwargs)

    def __validate_routable(self, routable: Routable) -> None:
        self.__validate_routable_payload_parameter(routable)
        self.__validate_routable_keyword_parameters(routable)
        self.__validate_routable_return_type(routable)

    @staticmethod
    def __validate_routable_payload_parameter(routable: Routable) -> None:  # noqa: C901
        signature = inspect.signature(routable, eval_str=True)

        parameters = list(signature.parameters.values())
        if not parameters:
            return

        p = parameters.pop(0)

        # If it is not a `POSITIONAL_OR_KEYWORD` parameter, it is not
        # the payload - ignore.
        if p.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD:
            return

        if p.annotation is inspect.Parameter.empty:
            details = (
                "Routable's payload parameter must have an type annotation"
            )
            _logger.error(details)
            raise TypeError(details)

        if type(p.annotation) is types.UnionType:
            p_types = p.annotation.__args__
            if len(p_types) != 2:
                details = (
                    f"Routable's payload parameter with {types.UnionType} "
                    f"annotation must have exactly two arguments, got "
                    f"{len(p_types)}"
                )
                _logger.error(details)
                raise TypeError(details)

            if not issubclass(p_types[1], types.NoneType):
                details = (
                    f"Routable's payload parameter with {types.UnionType} "
                    f"annotation must have {types.NoneType} as last "
                    f"argument, got {p_types[1]}"
                )
                _logger.error(details)
                raise TypeError(details)

            p_type = p_types[0]
        else:
            p_type = p.annotation

        if p_type is None:
            return

        if not issubclass(p_type, Packet):
            details = (
                f"Routable's payload parameter must be of type {Packet}, "
                f"got {p.annotation!r}"
            )
            _logger.error(details)
            raise TypeError(details)

    @staticmethod
    def __validate_routable_keyword_parameters(routable: Routable) -> None:
        signature = inspect.signature(routable, eval_str=True)

        parameters = list(signature.parameters.values())
        if not parameters:
            return

        if parameters[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            parameters.pop(0)

        for p in parameters:
            if p.kind != inspect.Parameter.KEYWORD_ONLY:
                details = (
                    f"Routable's parameters after the first one must be "
                    f"keyword-only, got {p.kind!r}"
                )
                _logger.error(details)
                raise TypeError(details)

    @staticmethod
    def __validate_routable_return_type(routable: Routable) -> None:
        signature = inspect.signature(routable, eval_str=True)

        r_type = signature.return_annotation
        if r_type is inspect.Signature.empty:
            details = "Routable's return type must have an type annotation"
            _logger.error(details)
            raise TypeError(details)

        if r_type is None:
            return

        if not issubclass(r_type, Packet):
            details = (
                f"Routable's return type must be of type {Packet}, "
                f"got {r_type!r}"
            )
            _logger.error(details)
            raise TypeError(details)


class FastCI:
    """Fast communication interface on top of `MQTT` [1]_.

    Parameters
    ----------
    client
        MQTT client instance.

    Raises
    ------
    ValueError
        If the client protocol is not MQTT v5.

    References
    ----------
    .. [1] https://mqtt.org
    """

    def __init__(
        self,
        client: aiomqtt.Client,
        *,
        prefix: str | None = None,
    ) -> None:
        if client._client.protocol != aiomqtt.ProtocolVersion.V5.value:  # noqa: SLF001
            details = "FastCI only supports MQTT v5"
            _logger.error(details)
            raise ValueError(details)

        self._client = client
        self._router = CIRouter(prefix=prefix)

    def include_router(self, router: CIRouter) -> None:
        """Include routes from another router.

        Parameters
        ----------
        router
            Router to include routes from.
        """
        self._router.include_router(router)

    def add_injectors(self, **kwargs: typing.Any) -> None:  # noqa: ANN401
        """Add an injector to the application.

        Injectors are passed to the decorated routes as keyword arguments.

        Parameters
        ----------
        kwargs
            Key-value pairs of injectors.
        """
        self._router.add_injectors(**kwargs)

    async def run(self) -> None:
        """Start communication.

        Subscribes to all routes and listens for incoming messages.

        Raises
        ------
        ValueError
            If the client is not connected.
        """
        if not self._client._connected.done():  # noqa: SLF001
            details = "Client is not connected"
            _logger.error(details)
            raise ValueError(details)

        for topic, data in self._router.routes.items():
            for qos in data:
                _logger.info("Subscribing to topic %s with QoS %s", topic, qos)
                await self._client.subscribe(topic, qos)

        await self.__listen()

    async def __listen(self) -> None:
        async for message in self._client.messages:
            await self.__handle(message)

    async def __handle(self, message: aiomqtt.Message) -> None:  # noqa: C901
        if not isinstance(message.payload, bytes):
            details = "Message payload is not of type bytes"
            _logger.error(details)
            raise TypeError(details)

        if (routings := self._router.routes.get(message.topic.value)) is None:
            return

        if (callbacks := routings.get(QoS(message.qos))) is None:
            return

        for callback in callbacks:
            signature = inspect.signature(callback, eval_str=True)
            kwargs = {
                key: value
                for key, value in self._router.injectors.items()
                if key in signature.parameters
            }

            payload_parameter = find_parameter_by_type_annotation(
                callback,
                Packet,
            )

            if payload_parameter is not None:
                kwargs[payload_parameter.name] = bytes_to_packet(
                    message.payload,
                    payload_parameter.annotation,
                )

            try:
                result = await callback(**kwargs)
            except Exception:
                _logger.exception("An error occurred while handling a message")
                raise

            response_topic: str | None = getattr(
                message.properties,
                "ResponseTopic",
                None,
            )

            if response_topic is None and result is None:
                return

            if response_topic is None and result is not None:
                details = (
                    f"{callback} returned a result but no response topic "
                    f"was set"
                )
                _logger.warning(details)
                return

            if response_topic is not None and result is None:
                details = (
                    f"{callback} returned no result but a response topic "
                    f"was set"
                )
                _logger.warning(details)
                return

            if response_topic is not None and result is not None:
                await self.__respond(result, response_topic)

    async def __respond(self, result: Packet, topic: str) -> None:
        if isinstance(result, Message):
            result = result.SerializeToString()

        await self._client.publish(topic, result, qos=QoS.AT_LEAST_ONCE)
