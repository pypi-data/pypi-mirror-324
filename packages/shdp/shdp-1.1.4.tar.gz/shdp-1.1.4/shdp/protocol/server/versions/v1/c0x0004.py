import logging
import os
import re

from .....utils.bitvec import Lsb
from .....utils.result import Result
from ....errors import Error
from ....managers.bits.encoder import BitEncoder
from ....managers.event import EventEncoder
from ...bits.utils import CHARS


class FullFyveResponse(EventEncoder[Lsb]):
    """Fyve file response encoder for SHDP protocol.

    Handles encoding of Fyve files, including:
    - File name encoding
    - Content encoding using CHARS mapping
    - Null byte separation

    Attributes:
        encoder (BitEncoder): Bit encoder for the response
        path (str): Path to the Fyve file

    Example:
        >>> response = FullFyveResponse("components/button.fyve")
        >>> response.encode()
        >>> encoder = response.get_encoder()
    """

    def __init__(self, path: str) -> None:
        """Initialize a full Fyve file response.

        Args:
            path: Path to the Fyve file to be sent

        Example:
            >>> response = FullFyveResponse("components/button.fyve")
        """
        logging.debug(
            f"[\x1b[38;5;227mSHDP\x1b[0m] \x1b[38;5;192m0x0004\x1b[0m created ({path})"
        )

        self.encoder = BitEncoder[Lsb]()
        self.path: str = path

    def encode(self) -> Result[None, Error]:
        """Encode the Fyve file content into binary format.

        Reads the file content and encodes both the filename and content
        using the CHARS encoding table.

        Returns:
            Result[None, Error]: Ok(None) if encoding succeeds,
                               Err(error) if any operation fails

        Example:
            >>> response = FullFyveResponse("button.fyve")
            >>> result = response.encode()
            >>> if result.is_ok():
            ...     print("File encoded successfully")
        """
        file_name: str = (
            self.path.split("/")[-1]
            if os.name == "posix"
            else self.path.split("\\")[-1]
        )

        Result.hide()

        self.encoder.add_bytes(file_name.encode("utf-8"))
        self.encoder.add_data(0, 8)

        with open(self.path, "rb") as file:
            content: str = file.read().decode("utf-8")
            content = re.sub(r"[\t\n\r]", "", content)

        for char in content:
            self.encoder.add_vec(CHARS[char])

        return Result.reveal()

    def get_encoder(self) -> BitEncoder[Lsb]:
        """Get the bit encoder containing the encoded file data.

        Returns:
            BitEncoder[Lsb]: The encoder containing the encoded filename and content

        Example:
            >>> response = FullFyveResponse("button.fyve")
            >>> response.encode()
            >>> encoder = response.get_encoder()
        """
        return self.encoder

    def get_event(self) -> int:
        """Get the event identifier for full Fyve file responses.

        Returns:
            int: The event ID (0x0004)

        Example:
            >>> response = FullFyveResponse("button.fyve")
            >>> response.get_event()
            0x0004
        """
        return 0x0004
