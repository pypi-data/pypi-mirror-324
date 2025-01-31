from typing import Callable, Generic

from ...utils.bitvec import Lsb, Msb, R
from ..args import Arg
from .bits.decoder import BitDecoder
from .event import EventDecoder

# Type alias for event identifiers as (major, minor) version tuples
EventId = tuple[int, int]

# Type alias for event handler functions
EventFn = Callable[[BitDecoder[R]], EventDecoder[R]]
# Type alias for event listener functions
ListenerFn = Callable[[EventDecoder[R]], list[Arg]]


class EventRegistry(Generic[R]):
    """Registry for managing protocol events and their listeners.

    This class maintains two registries:
    - events: Maps event IDs to their handler functions
    - listeners: Maps event IDs to their listener functions

    Examples:
        >>> registry = EventRegistry()
        >>> event_id = (1, 0)  # v1.0

        # Register an event handler
        >>> def handle_login(decoder: BitDecoder) -> LoginEvent:
        ...     return LoginEvent
        >>> registry.add_event(event_id, handle_login)

        # Register an event listener
        >>> def on_login(event: LoginEvent) -> list[Arg]:
        ...     return [Arg(Arg.TEXT, "user123")]
        >>> registry.add_listener(event_id, on_login)
    """

    events: dict[EventId, list[EventFn]] = {}
    listeners: dict[EventId, list[ListenerFn]] = {}

    def __init__(self) -> None:
        """Initialize a new event registry."""
        super().__init__()

    def get_event(self, event_id: EventId) -> list[EventFn] | None:
        """Get all event handlers for a specific event ID.

        Args:
            event_id (EventId): The event identifier (major, minor)

        Returns:
            list[EventFn] | None: List of event handlers or None if not found

        Example:
            >>> handlers = registry.get_event((1, 0))
            >>> if handlers:
            ...     for handler in handlers:
            ...         event = handler(decoder)
        """
        return self.events.get(event_id)

    def get_listeners(self, event_id: EventId) -> list[ListenerFn] | None:
        """Get all listeners for a specific event ID.

        Args:
            event_id (EventId): The event identifier (major, minor)

        Returns:
            list[ListenerFn] | None: List of event listeners or None if not found

        Example:
            >>> listeners = registry.get_listeners((1, 0))
            >>> if listeners:
            ...     for listener in listeners:
            ...         args = listener(event)
        """
        return self.listeners.get(event_id)

    def add_event(self, event_id: EventId, event_fn: EventFn) -> None:
        """Register a new event handler for a specific event ID.

        Args:
            event_id (EventId): The event identifier (major, minor)
            event_fn (EventFn): The event handler function

        Example:
            >>> def handle_message(decoder: BitDecoder) -> MessageEvent:
            ...     return MessageEvent
            >>> registry.add_event((1, 0), handle_message)
        """
        self.events.setdefault(event_id, []).append(event_fn)

    def add_listener(self, event_id: EventId, listener_fn: ListenerFn) -> None:
        """Register a new event listener for a specific event ID.

        Args:
            event_id (EventId): The event identifier (major, minor)
            listener_fn (ListenerFn): The listener function

        Example:
            >>> def on_message(event: MessageEvent) -> list[Arg]:
            ...     return [Arg(Arg.TEXT, "Hello!")]
            >>> registry.add_listener((1, 0), on_message)
        """
        self.listeners.setdefault(event_id, []).append(listener_fn)


EVENT_REGISTRY_MSB: EventRegistry[Msb] = EventRegistry[Msb]()
EVENT_REGISTRY_LSB: EventRegistry[Lsb] = EventRegistry[Lsb]()
