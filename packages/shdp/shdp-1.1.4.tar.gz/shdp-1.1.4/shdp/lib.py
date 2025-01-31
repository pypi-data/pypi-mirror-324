from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, Optional, TypeVar

from .protocol.errors import Error
from .protocol.managers.event import EventEncoder
from .utils.result import Result

CT = TypeVar("CT")
RT = TypeVar("RT")


class IShdpServer(Generic[CT, RT], ABC):
    """Abstract base class for SHDP protocol servers.

    This class defines the interface for SHDP servers that can handle
    connections from multiple clients of type CT.

    Examples:
        >>> class MyServer(IShdpServer[MyClient]):
        ...     @staticmethod
        ...     def listen(port=15150):
        ...         # Implementation
        ...         return Result.Ok(client)
    """

    @staticmethod
    @abstractmethod
    async def listen(
        port: int = 15150,
        *,
        cert_path: Optional[Path] = None,
        key_path: Optional[Path] = None,
    ) -> "Result[IShdpServer[CT, RT], Error]":
        """Start listening for client connections on the specified port.

        Args:
            port: Port number to listen on, defaults to 15150
            cert_path: Path to the certificate file
            key_path: Path to the private key file

        Returns:
            Result containing the connected server if successful, Error if failed

        Example:
            >>> result = server.listen(8080)
            >>> if result.is_ok():
            ...     server = result.unwrap()
        """
        pass

    @abstractmethod
    async def _accept(self, connection: CT) -> RT:
        """Internal method to accept incoming connections.

        Returns:
            Result indicating success or failure of accepting connection
        """
        pass

    @abstractmethod
    async def stop(self) -> Result[None, Error]:
        """Stop the server and close all client connections.

        Returns:
            Result indicating success or failure of stopping server

        Example:
            >>> server.stop()
        """
        pass

    @abstractmethod
    def get_clients(self) -> Result[dict[str, CT], Error]:
        """Get a dictionary of all connected clients.

        Returns:
            Result containing dict mapping 'IP:PORT' strings to client objects

        Example:
            >>> clients = server.get_clients().unwrap()
            >>> for addr, client in clients.items():
            ...     print(f"Client at {addr}")
        """
        pass


class IShdpClient(Generic[CT], ABC):
    """Abstract base class for SHDP protocol clients.

    This class defines the interface for SHDP clients that can connect
    to servers and send events.

    Examples:
        >>> class MyClient(IShdpClient[MyClientType]):
        ...     @staticmethod
        ...     def connect(addr: tuple[str, int]):
        ...         # Implementation
        ...         return Result.Ok(client)
    """

    @abstractmethod
    async def send(self, event: EventEncoder) -> Result[None, Error]:
        """Send an encoded event to the server.

        Args:
            event: The encoded event to send

        Returns:
            Result indicating success or failure of sending

        Example:
            >>> event = MyEvent()
            >>> client.send(event)
        """
        pass

    @staticmethod
    @abstractmethod
    async def connect(to: tuple[str, int]) -> "Result[IShdpClient[CT], Error]":
        """Connect to a server at the specified address.

        Args:
            to: Tuple of (host, port) to connect to

        Returns:
            Result containing connected client if successful

        Example:
            >>> result = Client.connect(('localhost', 8080))
            >>> if result.is_ok():
            ...     client = result.unwrap()
        """
        pass

    @abstractmethod
    async def disconnect(self) -> Result[None, Error]:
        """Disconnect from the server.

        Returns:
            Result indicating success or failure of disconnecting

        Example:
            >>> client.disconnect()
        """
        pass

    @abstractmethod
    def get_address(self) -> Result[tuple[str, int], Error]:
        """Get this client's address.

        Returns:
            Result containing (host, port) tuple if successful

        Example:
            >>> addr = client.get_address().unwrap()
            >>> host, port = addr
        """
        pass

    @abstractmethod
    async def _accept(self) -> Result[None, Error]:
        """Internal method to accept the connection.

        Returns:
            Result indicating success or failure of accepting
        """
        pass
