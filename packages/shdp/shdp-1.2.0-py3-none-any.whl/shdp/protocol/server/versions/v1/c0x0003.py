import logging

from .....lib import Result
from .....utils.bitvec import Lsb
from ....errors import Error
from ....managers.bits.encoder import BitEncoder
from ....managers.event import EventEncoder


class ComponentNeedsResponse(EventEncoder[Lsb]):
    """Component needs response encoder for SHDP protocol.

    Handles encoding of component requirements, including:
    - Component name
    - Optional title
    - List of required files

    Attributes:
        encoder (BitEncoder): Bit encoder for the response
        component_name (str): Name of the component
        title (str | None): Optional component title
        files (list[str]): List of required file paths

    Example:
        >>> files = ["style.css", "script.js"]
        >>> response = ComponentNeedsResponse("MyComponent", "My Title", files)
        >>> response.encode()
    """

    def __init__(self, component_name: str, title: str | None, files: list[str]):
        """Initialize component needs response.

        Args:
            component_name: Name of the component
            title: Optional title for the component
            files: List of required file paths
        """
        logging.debug(
            f"[\x1b[38;5;227mSHDP\x1b[0m] \x1b[38;5;192m0x0003\x1b[0m created ({component_name})"
        )

        self.encoder = BitEncoder[Lsb]()
        self.component_name = component_name
        self.title = "" if title is None else title
        self.files = files

    def encode(self) -> Result[None, Error]:
        Result.hide()

        self.encoder.add_bytes(self.component_name.encode("utf-8"))

        if self.title is not None:
            self.encoder.add_data(1, 8)
            self.encoder.add_bytes(self.title.encode("utf-8"))

        if len(self.files) > 0:
            for file in self.files:
                self.encoder.add_data(0, 8)
                self.encoder.add_bytes(file.encode("utf-8"))

        return Result.reveal()

    def get_encoder(self) -> BitEncoder[Lsb]:
        return self.encoder

    def get_event(self) -> int:
        return 0x0003
