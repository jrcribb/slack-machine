from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any


class MachineBaseStorage(ABC):
    """Base class for storage backends

    Extending classes should implement the five methods in this base class. Slack Machine takes
    care of a lot of details regarding the persistent storage of data. So storage backends
    **do not** have to deal with the following, because Slack Machine takes care of these:

    - Serialization/Deserialization of data
    - Namespacing of keys (so data stored by different plugins doesn't clash)
    """

    settings: Mapping[str, Any]

    def __init__(self, settings: Mapping[str, Any]):
        self.settings = settings

    async def init(self) -> None:  # noqa: B027 (no-op by design)
        """Initialize the storage backend

        To be implemented by subclasses if initialization is required. This method is called once after instantiation.
        """
        pass

    @abstractmethod
    async def get(self, key: str) -> bytes | None:
        """Retrieve data by key

        Args:
            key: key for which to retrieve data

        Returns:
            the raw data for the provided key, as (byte)string. Should return `None` when
                the key is unknown or the data has expired.
        """
        ...

    @abstractmethod
    async def set(self, key: str, value: bytes, expires: int | None = None) -> None:
        """Store data by key

        Args:
            key: the key under which to store the data
            value: data as (byte)string
            expires: optional expiration time in seconds, after which the data should not be
                returned any more.
        """
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete data by key

        :param key: key for which to delete the data
        """
        ...

    @abstractmethod
    async def has(self, key: str) -> bool:
        """Check if the key exists

        Args:
            key: key to check

        Returns:
            `True/False` wether the key exists
        """
        ...

    @abstractmethod
    async def size(self) -> int:
        """Calculate the total size of the storage

        Returns:
            total size of storage in bytes (integer)
        """
        ...

    @abstractmethod
    async def close(self) -> None:
        """Close the storage backend"""
        ...
