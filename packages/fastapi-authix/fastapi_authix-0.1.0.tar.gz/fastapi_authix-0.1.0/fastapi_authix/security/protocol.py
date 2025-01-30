from typing import Any, Protocol


class SecureLayer(Protocol):
    @property
    def ttl(self) -> int:
        ...

    def create_access_token(self, payload: dict[str, Any]) -> str:
        ...

    def decode_access_token(self, value: str) -> dict[str, Any]:
        ...
