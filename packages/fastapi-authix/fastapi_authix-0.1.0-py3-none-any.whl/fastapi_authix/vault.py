from datetime import datetime, timedelta
from typing import Any

from starlette.responses import Response
from starlette.requests import Request

from fastapi_authix.exceptions import AccessDenied
from fastapi_authix.security.fernet import Fernet
from fastapi_authix.security.protocol import SecureLayer
from fastapi_authix.serializers import Serializer
from fastapi_authix.typing import SerializeMode


class Vault:
    def __init__(
        self,
        *,
        cipher: SecureLayer = Fernet(),
        serializer: SerializeMode = "auto",
        cookie_key: str = "access-token",
        header_key: str = "X-API-Key",
        use_cookie: bool = True,
        use_header: bool = False,
    ) -> None:
        self._cipher: SecureLayer = cipher
        self._serialize_mode: SerializeMode = serializer
        self._cookie_key: str = cookie_key
        self._header_key: str = header_key
        self._use_cookie: bool = use_cookie
        self._use_header: bool = use_header

        self._logged_out: dict[str, datetime] = {}
        self._serializer: Serializer | None = None

    def create_access_token(self, payload: Any) -> str:
        if self._serializer is None:
            self._serializer = Serializer(payload, mode=self._serialize_mode)

        return self._cipher.create_access_token(self._serializer.serialize())

    def decode_access_token(self, value: str) -> Any:
        payload = self._cipher.decode_access_token(value)
        return self._serializer.deserialize(payload)

    def disable_access_token(self, value: str) -> None:
        """
        Adds access token to the list of disabled tokens and marks it with the current date.
        """
        self._logged_out[value] = datetime.now()

    def set_access_token(self, response: Response, *, payload: Any) -> None:
        """
        Serializes the provided ``payload`` into JSON and encrypts its data into an access token.
        This allows the token to be decrypted later, restoring the original object.
        Finally, it sets a cookie containing this access token for the provided response object.

        The ``payload`` can be any object that supports serialization
        (e.g., Pydantic models, SQLAlchemy models, etc.).
        For a full list of supported serializable objects, refer to the documentation here:
        """
        response.set_cookie(self._cookie_key, self.create_access_token(payload), httponly=True)

    def remove_access_token(self, response: Response) -> None:
        """
        Removes the access token cookie from the provided ``response`` object.
        """
        response.delete_cookie(self._cookie_key, httponly=True)

    def extract_access_token(self, request: Request) -> str | None:
        """
        Extracts the access token from either cookies or headers,
        depending on the configured settings.
        If both ``use_cookie`` and ``use_header`` are enabled,
        the method first attempts to retrieve the token from cookies,
        and only if unsuccessful, proceeds to check the headers.

        Returns ``None`` if the access token cannot be retrieved.
        """
        if self._use_cookie:
            if (access_token := request.cookies.get(self._cookie_key)) is not None:
                return access_token
        if self._use_header:
            return request.headers.get(self._header_key)

    def is_token_disabled(self, value: str, *, auto_remove: bool = False) -> bool:
        """
        Checks for the presence of an access token in the list of disabled tokens.
        The ``auto_remove`` flag determines whether the token should be
        automatically removed from this list when its TTL expires.

        If ``auto_remove`` is enabled, it returns actual info at the time of the call.
        Otherwise, it only checks for the token's presence in the list.
        """
        if disabled_at := self._logged_out.get(value):
            # Calculates the time when the token was supposed to expire.
            expiration_time = disabled_at + timedelta(seconds=self._cipher.ttl)
            # Checks whether this expiration date has passed and determines if removal is necessary.
            if need_remove := (auto_remove and expiration_time < datetime.now()):
                del self._logged_out[value]
            # `need_remove = True` -> token was removed -> token NOT disabled.
            # `need_remove = False` -> token suspended -> token DISABLED.
            return not need_remove

        # Token is not in the list.
        return False

    def require_data(self, request: Request) -> Any:
        """
        Retrieves an object containing data serialized during access token generation.
        It returns the original object with fields populated from the decoded access token information.

        The method can be used either as a FastAPI dependency or called directly as a standalone function.
        It checks for the presence of the access token in either cookies or headers
        (depending on configuration settings), attempts to decode it, and then deserializes the data.

        If any issue occurs during the process (e.g., missing token or decoding failure),
        ``AccessDenied`` exception is raised, accompanied by a descriptive error message.
        """
        if not (access_token := self.extract_access_token(request)):
            raise AccessDenied("Missing access token")
        elif self.is_token_disabled(access_token, auto_remove=True):
            # This token was recently used to log out. It's blocked until it expires.
            raise AccessDenied("Access token is no longer valid")

        return self.decode_access_token(access_token)
