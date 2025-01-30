import pytest
from datetime import datetime, timedelta, timezone
import json
from dataclasses import dataclass
from typing import Any

from dogpile_breaker.api import CachedEntry
from dogpile_breaker.exceptions import CantDeserializeError


# Example serializer and deserializer for testing
def example_serializer(payload: Any) -> bytes:
    return json.dumps(payload).encode("utf-8")


def example_deserializer(data: bytes) -> Any:
    return json.loads(data.decode("utf-8"))


@pytest.fixture
def valid_payload():
    return {"key": "value", "timestamp": datetime.now(tz=timezone.utc).isoformat()}


@pytest.fixture
def expired_timestamp():
    return (datetime.now(tz=timezone.utc) - timedelta(hours=1)).timestamp()


@pytest.fixture
def future_timestamp():
    return (datetime.now(tz=timezone.utc) + timedelta(hours=1)).timestamp()


@pytest.fixture
def valid_cached_entry(valid_payload, future_timestamp):
    return CachedEntry(payload=valid_payload, expiration_timestamp=future_timestamp)


def test_to_bytes(valid_cached_entry):
    serialized_data = valid_cached_entry.to_bytes(serializer=example_serializer)
    assert isinstance(serialized_data, bytes)
    assert b"key" in serialized_data
    assert b"expiration_timestamp" in serialized_data


def test_from_bytes(valid_cached_entry, valid_payload, future_timestamp):
    serialized_data = valid_cached_entry.to_bytes(serializer=example_serializer)
    deserialized_entry = CachedEntry.from_bytes(serialized_data, deserializer=example_deserializer)
    assert deserialized_entry is not None
    assert deserialized_entry.payload == valid_payload
    assert deserialized_entry.expiration_timestamp == future_timestamp


def test_from_bytes_invalid_meta_data():
    invalid_data = b'{"value": "42"}|data'
    CachedEntry.from_bytes(invalid_data, deserializer=example_deserializer)


def test_from_bytes_invalid_payload():
    invalid_data = b'invalid|{"expiration_timestamp": 1738012598.794059}'
    CachedEntry.from_bytes(invalid_data, deserializer=example_deserializer)


def test_deserialization_error_handling():
    def failing_deserializer(data: bytes) -> Any:
        raise CantDeserializeError("Cannot deserialize")

    serialized_data = b'{"key":"value"}|{"expiration_timestamp":1234567890}'
    deserialized_entry = CachedEntry.from_bytes(serialized_data, deserializer=failing_deserializer)
    assert deserialized_entry is None


def test_to_bytes_empty_payload():
    empty_entry = CachedEntry(payload=None, expiration_timestamp=1234567890)
    serialized_data = empty_entry.to_bytes(serializer=example_serializer)
    assert isinstance(serialized_data, bytes)
    assert b"expiration_timestamp" in serialized_data
