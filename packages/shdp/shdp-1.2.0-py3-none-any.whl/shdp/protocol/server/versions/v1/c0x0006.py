import json
import logging
from typing import Optional

from .....lib import Result
from .....utils.bitvec import Lsb
from ....errors import Error
from ....managers.bits.encoder import BitEncoder
from ....managers.event import EventEncoder


class InteractionResponse(EventEncoder[Lsb]):
    """Interaction response encoder for SHDP protocol.

    Handles encoding of interaction responses, including:
    - 64-bit request ID
    - Optional JSON response data

    Attributes:
        encoder (BitEncoder): Bit encoder for the response
        request_id (int): ID of the original request
        response (Optional[dict[str, Any]]): Optional response data

    Example:
        >>> data = {"status": "success", "value": 42}
        >>> response = InteractionResponse(123, data)
        >>> response.encode()
    """

    def __init__(self, request_id: int, response: Optional[dict | list]):
        logging.debug("[\x1b[38;5;227mSHDP\x1b[0m] \x1b[38;5;163m0x0006\x1b[0m created")

        self.encoder = BitEncoder[Lsb]()
        self.request_id = request_id
        self.response = response

    def encode(self) -> Result[None, Error]:
        self.encoder.add_data(self.request_id, 64)

        if self.response is not None:
            self.encoder.add_bytes(json.dumps(self.response).encode("utf-8"))

        return Result.Ok(None)

    def get_encoder(self) -> BitEncoder[Lsb]:
        return self.encoder

    def get_event(self) -> int:
        return 0x0006
