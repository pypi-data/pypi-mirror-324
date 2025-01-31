import logging

from .....lib import Result
from .....utils.bitvec import Lsb
from ....errors import Error
from ....managers.bits.encoder import BitEncoder
from ....managers.event import EventEncoder


class ErrorResponse(EventEncoder[Lsb]):
    """Error response encoder for SHDP protocol.

    Handles encoding of error responses including:
    - 16-bit error code
    - UTF-8 encoded error message
    - 8-bit padding

    Attributes:
        encoder (BitEncoder): Bit encoder for the response
        error (Error): Error details to encode

    Example:
        >>> error = Error(404, ErrorKind.NOT_FOUND, "Page not found")
        >>> response = ErrorResponse(error)
        >>> response.encode()
    """

    def __init__(self, error: Error):
        logging.debug(
            f"[\x1b[38;5;227mSHDP\x1b[0m] \x1b[38;5;160m0x0002\x1b[0m created (\x1b[38;5;160m{error.code}\x1b[0m): [{error.kind}] {error.message}"
        )
        self.encoder = BitEncoder[Lsb]()
        self.error = error

    def encode(self) -> Result[None, Error]:
        Result.hide()

        self.encoder.add_data(self.error.code, 16)
        self.encoder.add_data(0, 8)
        self.encoder.add_bytes(self.error.message.encode("utf-8"))

        return Result.reveal()

    def get_encoder(self) -> BitEncoder[Lsb]:
        return self.encoder

    def get_event(self) -> int:
        return 0x0002
