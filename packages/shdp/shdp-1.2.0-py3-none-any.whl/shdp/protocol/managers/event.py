from abc import ABC, abstractmethod
from typing import Generic

from ...utils.bitvec import R, ReversedR
from ...utils.result import Result
from ..errors import Error
from .bits.decoder import Frame
from .bits.encoder import BitEncoder


class EventEncoder(Generic[R], ABC):
    """Abstract base class for encoding protocol events.

    This class defines the interface for encoding events in the protocol.
    Each event type should implement this interface to specify how it should
    be encoded into bits.

    Example:
        >>> class LoginEvent(EventEncoder[R]):
        ...     def encode(self):
        ...         self.encoder.add_data(0x01, 8)  # Add event data
        ...
        ...     def get_encoder(self) -> BitEncoder[R]:
        ...         return self.encoder
        ...
        ...     def get_event(self) -> int:
        ...         return 0x0001  # Event ID for login
    """

    @abstractmethod
    def encode(self) -> Result[None, Error]:
        """Encode the event data into bits.

        This method should use the encoder to add the event's data
        to the bit frame.
        """
        pass

    @abstractmethod
    def get_encoder(self) -> BitEncoder[R]:
        """Get the bit encoder used by this event.

        Returns:
            BitEncoder[R]: The encoder instance for this event
        """
        pass

    @abstractmethod
    def get_event(self) -> int:
        """Get the event identifier.

        Returns:
            int: The unique 16-bit identifier for this event type
        """
        pass


class EventDecoder(Generic[R], ABC):
    """Abstract base class for decoding protocol events.

    This class defines the interface for decoding events in the protocol.
    Each event type should implement this interface to specify how it should
    be decoded from bits and what responses it can generate.

    Example:
        >>> class LoginDecoder(EventDecoder[R]):
        ...     def decode(self, frame: Frame[R]) -> Result[None, Error]:
        ...         user_id = frame.read_int(8)  # Read event data
        ...         return Result.Ok(None)
        ...
        ...     def get_responses(self) -> Result[list[EventEncoder[ReversedR]], Error]:
        ...         return Result.Ok([LoginSuccessEvent, LoginFailedEvent])
    """

    @abstractmethod
    def decode(self, frame: Frame[R]) -> Result[None, Error]:
        """Decode event data from a frame.

        Args:
            frame (Frame): The frame containing the event data
        """
        pass

    @abstractmethod
    def get_responses(self) -> Result[list[EventEncoder[ReversedR]], Error]:
        """Get list of possible response types for this event.

        Returns:
            Result containing list of event encoder types that can respond to this event
        """
        pass
