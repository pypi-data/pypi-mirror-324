from typing import Generic, Iterator

from ....utils.bitvec import BitVec, R
from ....utils.result import Result
from ...errors import Error, ErrorKind


class BitDecoder(Generic[R]):
    """A generic decoder that processes bytes.

    This class implements a decoder that processes binary data. It provides iteration
    over its underlying bytes and methods for reading data at specific positions.

    Args:
        frame (BitVec[R]): The binary data to be decoded

    Examples:
        >>> decoder = BitDecoder(b'\\x0F\\x42')
        >>> list(decoder.frame)  # Access raw bytes
        [15, 66]
    """

    def __init__(self, frame: BitVec[R]):
        self.frame: BitVec[R] = frame
        self.position: int = 0

    def __iter__(self) -> Iterator[int]:
        """Allows iteration over the decoder's bytes.

        Returns:
            Iterator[int]: An iterator over the bytes in the decoder

        Examples:
            >>> decoder = BitDecoder(b'\\x0F\\x42')
            >>> list(decoder)
            [15, 66]
        """
        return iter(self.frame)

    def read_data(self, n: int) -> Result[BitVec[R], Error]:
        """Reads n bytes from the frame at the current position.

        Args:
            n (int): The number of bytes to read

        Returns:
            Result[BitVec, Error]: The bytes read from the frame
        """
        if self.position + n > len(self.frame):
            return Result.Err(
                Error.new(
                    ErrorKind.SIZE_CONSTRAINT_VIOLATION,
                    f"Out of bounds :: {self.position} + {n} > {len(self.frame)}",
                )
            )

        data = self.frame[self.position : self.position + n]
        self.position += n
        return Result.Ok(data)

    def __str__(self):
        return f"BitDecoder(frame={self.frame}, position={self.position})"

    def read_vec(self, fp: int, tp: int) -> Result[BitVec[R], Error]:
        """Reads a vector of bytes from the frame between two positions.

        Args:
            fp (int): The start position
            tp (int): The end position

        Returns:
            Result[BitVec, Error]: The bytes read from the frame
        """
        if fp >= len(self.frame):
            return Result.Err(
                Error.new(
                    ErrorKind.SIZE_CONSTRAINT_VIOLATION,
                    f"Out of bounds :: {fp} >= {len(self.frame)}",
                )
            )

        return Result.Ok(self.frame[fp:tp])


class Frame(Generic[R]):
    """A frame of decoded data.

    This class represents a frame of data that has been decoded.
    It contains the version, event, data size, and data fields.
    """

    def __init__(self, version: int, event: int, data_size: int, data: BitVec[R]):
        self.version = version
        self.event = event
        self.data_size = data_size
        self.data: BitVec[R] = data


class FrameDecoder(Generic[R]):
    """A decoder that processes frames of data.

    This class extends BitDecoder to provide additional functionality for processing
    frames of data. It handles decoding of protocol-specific frame structures including
    version, event ID, and data size headers.
    """

    def __init__(self, decoder: BitDecoder[R]):
        self.decoder: BitDecoder[R] = decoder

    def get_decoder(self) -> BitDecoder[R]:
        """Returns the underlying decoder.

        Returns:
            BitDecoder: The underlying decoder
        """
        return self.decoder

    def decode(self) -> Result[Frame[R], Error]:
        """Decodes the frame according to the specified bit order.

        Returns:
            Result[Frame, Error]: A Frame object containing the decoded version,
                                     event, data size, and data
        """

        result_version_data: Result[BitVec[R], Error] = self.decoder.read_data(8)
        if result_version_data.is_ok():
            version: int = result_version_data.unwrap().to_int().unwrap()
        else:
            return Result.Err(result_version_data.unwrap_err())

        result_event_data: Result[BitVec[R], Error] = self.decoder.read_data(16)
        if result_event_data.is_ok():
            event: int = result_event_data.unwrap().to_int().unwrap()
        else:
            return Result.Err(result_event_data.unwrap_err())

        result_data_size_data: Result[BitVec[R], Error] = self.decoder.read_data(32)
        if result_data_size_data.is_ok():
            data_size: int = result_data_size_data.unwrap().to_int().unwrap()
        else:
            return Result.Err(result_data_size_data.unwrap_err())

        result_data: Result[BitVec[R], Error] = self.decoder.read_vec(
            56, 56 + data_size
        )
        if result_data.is_err():
            return Result.Err(result_data.unwrap_err())

        return Result.Ok(Frame(version, event, data_size, result_data.unwrap()))
