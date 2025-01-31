import json
import logging
from typing import Any, Optional, cast

from .....utils.bitvec import Lsb, Msb, ReversedR
from .....utils.result import Result
from ....errors import Error, ErrorKind
from ....managers.bits.decoder import BitDecoder
from ....managers.event import EventDecoder, EventEncoder, Frame
from ....managers.registry import EVENT_REGISTRY_MSB
from .c0x0006 import InteractionResponse


class InteractionRequest(EventDecoder[Msb]):
    def __init__(self, decoder: BitDecoder[Msb]):
        logging.debug(
            "[\x1b[38;5;187mSHDP\x1b[0m] \x1b[38;5;125m0x0005\x1b[0m received"
        )

        self.decoder = decoder
        self.request_id = 0
        self.parent_name = ""
        self.function_name = ""
        self.object_id: Optional[int] = None
        self.params: Optional[dict[str, Any]] = None
        self.token: Optional[str] = None

    def decode(self, frame: Frame) -> Result[None, Error]:
        self.request_id = self.decoder.read_data(64).unwrap().to_int().unwrap()
        byte_length = (frame.data_size - 64) // 8
        data_bytes = []

        for _ in range(byte_length):
            byte = self.decoder.read_data(8).unwrap().to_byte_list()[0]
            data_bytes.append(byte)

        string = bytes(data_bytes).decode("utf-8")
        parts = string.split("\x00")

        self.function_name = parts[0]
        self.parent_name = parts[1]

        if self.parent_name == "":
            return Result.Err(Error.new(ErrorKind.BAD_REQUEST, "Parent name is empty"))

        if self.function_name == "":
            return Result.Err(
                Error.new(ErrorKind.BAD_REQUEST, "Function name is empty")
            )

        self.token = parts[2] if parts[2] != "" else None
        self.object_id = int(parts[3]) if parts[3] != "" else None
        self.params = json.loads(parts[4]) if parts[4] != "" else None

        logging.debug(
            f"[\x1b[38;5;187mSHDP\x1b[0m] \x1b[38;5;125m0x0005\x1b[0m: function_name: {self.function_name}, table: {self.parent_name}, object_id: {self.object_id}, params: {self.params}, token: {self.token}"
        )

        return Result.Ok(None)

    def get_responses(self) -> Result[list[EventEncoder[ReversedR]], Error]:
        listeners = EVENT_REGISTRY_MSB.get_listeners((1, 0x0005))

        if listeners is None:
            return Result.Ok([])

        all_args = [listener(self) for listener in listeners]
        responses: list[EventEncoder[Lsb]] = []

        for args_list in all_args:
            result_response = args_list[0].to_opt_value()

            if result_response.is_ok():
                response = result_response.unwrap()
            else:
                return Result.Err(result_response.unwrap_err())

            responses.append(InteractionResponse(self.request_id, response))

        return Result.Ok(cast(list[EventEncoder[ReversedR]], responses))


#
# REGISTRY
#

EVENT_REGISTRY_MSB.add_event((1, 0x0005), lambda decoder: InteractionRequest(decoder))
