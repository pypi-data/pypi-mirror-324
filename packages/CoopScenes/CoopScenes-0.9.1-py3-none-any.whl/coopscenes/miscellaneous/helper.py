"""
This module provides utility functions and mixins for various tasks such as time conversion,
data serialization, and checksum computation. The functions include time conversion from Unix
timestamps to UTC strings, serialization and deserialization of objects, checksum calculation,
and handling byte streams.

Classes:
    TimestampMixin: A mixin class providing a method for timestamp conversion.
    ReprFormaterMixin: A mixin class providing methods for formatting numpy arrays and nested objects.

Functions:
    unix_to_utc(unix_time, precision='ns', timezone='Europe/Berlin'): Converts a Unix timestamp to a formatted UTC time string.
    compute_checksum(data): Computes the SHA-256 checksum for a given data block.
    read_checksum(data): Reads and separates the SHA-256 checksum from a data stream.
    read_data_block(data, dtype_length=INT_LENGTH): Reads a block of data from a byte stream, using a length prefix.
    obj_to_bytes(obj): Serializes an object to bytes using the Dill library.
    obj_from_bytes(data): Deserializes an object from bytes using the Dill library.
    serialize(obj): Serializes an object to bytes with a length prefix.
    deserialize(data, cls, *args): Deserializes a byte stream into an object using the class's `from_bytes()` method.
"""
from typing import Optional, Tuple
from coopscenes.miscellaneous import INT_LENGTH, SHA256_CHECKSUM_LENGTH
from decimal import Decimal
from datetime import datetime, timedelta
import numpy as np
import hashlib
import dill
import pytz


class TimestampMixin:
    """Mixin class to provide a method for timestamp conversion."""

    def get_timestamp(self, precision='ns', timezone: str = 'Europe/Berlin') -> str:
        """Convert the timestamp to a formatted string using a specific timezone.

        Args:
            precision (str): Desired precision for the timestamp ('ns' for nanoseconds or 's' for seconds).
                             Defaults to 'ns'.
            timezone (str): The timezone for the conversion (e.g., 'Europe/Berlin'). Defaults to 'Europe/Berlin'.

        Returns:
            str: The formatted timestamp as a string.

        Raises:
            ValueError: If the precision is not 'ns' or 's'.
        """
        if not hasattr(self, 'timestamp') or self.timestamp is None:
            return 'None'
        return unix_to_utc(self.timestamp, precision=precision, timezone=timezone)


class ReprFormaterMixin:
    """Mixin class to provide methods for formatting numpy arrays and other objects."""

    @staticmethod
    def _format_array(array: Optional[np.ndarray], precision: int = 3, indent: int = 0) -> str:
        """Format a numpy array for display with indentation and specified precision."""
        if array is None:
            return 'None'
        # Format array with specified precision and line breaks
        array_str = np.array2string(
            array,
            precision=precision,
            separator=', ',
            suppress_small=True,
            threshold=np.inf
        )
        # Indent all lines, including the first
        lines = array_str.split('\n')
        formatted_string = '\n'.join([f"{' ' * indent}{line}" for line in lines])
        return formatted_string

    @staticmethod
    def _format_height(height_matrix: Optional[np.ndarray]) -> str:
        """Format the height value from a 4x4 transformation matrix."""
        if height_matrix is None:
            return 'None'
        # Extract z-translation component from the matrix
        height_value = height_matrix[2, 3]
        return f"{height_value:.1f}m"


def unix_to_utc(unix_time: Decimal, precision='ns', timezone: str = 'Europe/Berlin') -> str:
    """Convert a Unix timestamp to a formatted local time string with dynamic timezone handling.

    Args:
        unix_time (Decimal): The Unix timestamp as a `Decimal`, representing time since epoch.
        precision (str): The desired precision of the output ('ns' for nanoseconds, 's' for seconds). Defaults to 'ns'.
        timezone (str): The timezone to compute local time. Defaults to 'Europe/Berlin'.

    Returns:
        str: The local time formatted as a string, with the specified precision.

    Raises:
        ValueError: If an unsupported precision is provided.
    """
    # Convert Decimal to nanoseconds
    unix_time_ns = Decimal(str(unix_time).replace('.', ''))
    seconds = int(unix_time_ns) // 1000000000
    nanoseconds = int(unix_time_ns) % 1000000000

    utc_time = datetime.utcfromtimestamp(seconds).replace(tzinfo=pytz.utc) + timedelta(seconds=nanoseconds / 1e9)

    try:
        local_tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Invalid timezone '{timezone}' provided.")

    local_time = utc_time.astimezone(local_tz)

    if precision == 'ns':
        local_time_str = local_time.strftime('%Y-%m-%d_%H-%M-%S') + f'.{nanoseconds:09d}'
    elif precision == 's':
        local_time_str = local_time.strftime('%Y-%m-%d_%H-%M-%S')
    else:
        raise ValueError("Precision must be 'ns' or 's'")

    return local_time_str


def compute_checksum(data: bytes) -> bytes:
    """Compute the SHA-256 checksum for a given data block.

    This function takes a byte sequence and returns the SHA-256 hash.

    Args:
        data (bytes): The data for which the checksum is to be computed.

    Returns:
        bytes: The computed SHA-256 checksum.
    """
    return hashlib.sha256(data).digest()


def read_checksum(data: bytes) -> Tuple[bytes, bytes]:
    """Read and separate the SHA-256 checksum from the data.

    This function extracts the SHA-256 checksum from the start of a byte stream,
    and returns the checksum along with the remaining data.

    Args:
        data (bytes): The byte stream that contains the checksum at the beginning.

    Returns:
        tuple[bytes, bytes]: A tuple where the first element is the extracted SHA-256 checksum,
                             and the second element is the remaining data after the checksum.
    """
    return data[0:SHA256_CHECKSUM_LENGTH], data[SHA256_CHECKSUM_LENGTH:]


def read_data_block(data: bytes, dtype_length: int = INT_LENGTH) -> Tuple[bytes, bytes]:
    """Read a block of data from the given byte stream.

    This function reads the first part of the byte stream that indicates the
    length of the following data block. It then extracts that block of bytes.

    Args:
        data (bytes): The input byte stream.
        dtype_length (int): The length of the size header in bytes. Defaults to INT_LENGTH.

    Returns:
        tuple[bytes, bytes]: The extracted data block and the remaining byte stream.
    """
    data_len = int.from_bytes(data[0:dtype_length], 'big')
    data_block_bytes = data[dtype_length:dtype_length + data_len]
    return data_block_bytes, data[dtype_length + data_len:]


def obj_to_bytes(obj) -> bytes:
    """Serialize an object to bytes using Dill.

    This function serializes an object into a byte stream using Dill. The
    length of the serialized data is prepended as a header.

    Args:
        obj: The object to be serialized.

    Returns:
        bytes: The serialized byte representation of the object.
    """
    obj_bytes = dill.dumps(obj)
    obj_bytes_len = len(obj_bytes).to_bytes(INT_LENGTH, 'big')
    return obj_bytes_len + obj_bytes


def obj_from_bytes(data: bytes):
    """Deserialize an object from bytes using Dill.

    This function deserializes a byte stream into an object using Dill.

    Args:
        data (bytes): The byte data to be deserialized.

    Returns:
        object: The deserialized object.
    """
    return dill.loads(data)


def serialize(obj) -> bytes:
    """Serialize an object to bytes with a length prefix.

    This function serializes an object by calling its `to_bytes()` method
    and prepends the length of the serialized byte data.

    Args:
        obj: The object to be serialized.

    Returns:
        bytes: The serialized byte representation of the object, or a placeholder
               if the object is `None`.
    """
    if obj is None:
        return b'\x00\x00\x00\x00'
    obj_bytes = obj.to_bytes()
    obj_bytes_len = len(obj_bytes).to_bytes(INT_LENGTH, 'big')
    return obj_bytes_len + obj_bytes


def deserialize(data: bytes, cls, *args) -> Tuple[Optional[object], bytes]:
    """Deserialize a byte stream into an object.

    This function deserializes a byte stream into an object of the specified class
    by calling the class's `from_bytes()` method. The length of the serialized data
    is used to extract the object, and the remaining data is returned.

    Args:
        data (bytes): The byte stream to be deserialized.
        cls (class): The class type that has a `from_bytes()` method for deserialization.
        *args: Additional arguments passed to the class's `from_bytes()` method.

    Returns:
        tuple[Optional[object], bytes]: The deserialized object and the remaining byte stream.
    """
    obj_len = int.from_bytes(data[:INT_LENGTH], 'big')
    if obj_len == 0:
        return None, data[INT_LENGTH:]
    obj_data = data[INT_LENGTH:INT_LENGTH + obj_len]
    return cls.from_bytes(obj_data, *args), data[INT_LENGTH + obj_len:]
