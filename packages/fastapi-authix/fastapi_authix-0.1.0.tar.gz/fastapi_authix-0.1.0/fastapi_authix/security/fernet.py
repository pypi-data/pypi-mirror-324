from typing import Any

from cryptography import fernet
from orjson import orjson

from fastapi_authix.security.protocol import SecureLayer


class Fernet(SecureLayer):
    def __init__(
        self,
        *,
        secret_key: bytes | str | None = None,
        time_to_live: int = 3600,
    ) -> None:
        self._cipher = fernet.Fernet(secret_key or fernet.Fernet.generate_key())
        self._ttl = time_to_live

    @property
    def ttl(self) -> int:
        return self._ttl

    def _encrypt_data(self, payload: Any) -> bytes:
        """
        Converts payload data into a JSON object and encrypts it
        into a byte sequence that can be converted to string.
        """
        return self._cipher.encrypt(orjson.dumps(payload))

    def _decrypt_data(self, value: str) -> dict[str, Any]:
        """
        Decrypts the payload from given access token.

        :param value: Access token string.
        :return: Raw payload.
        :raises InvalidToken: If the token has expired or is invalid.
        """
        return orjson.loads(self._cipher.decrypt(value, ttl=self._ttl))

    def create_access_token(self, payload: dict[str, Any]) -> str:
        return self._encrypt_data(payload).decode()

    def decode_access_token(self, value: str) -> dict[str, Any]:
        return self._decrypt_data(value)
