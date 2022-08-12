import typing
from base64 import b64decode, b64encode

from app.service.starsessions.backends.base import SessionBackend
from app.service.starsessions.serializers import JsonSerializer, Serializer
from itsdangerous import BadSignature, TimestampSigner
from starlette.datastructures import Secret


class CookieBackend(SessionBackend):
    """Stores session data in the browser's cookie as a signed string."""

    def __init__(
        self,
        secret_key: typing.Union[str, Secret],
        max_age: int,
        serializer: typing.Optional[Serializer] = None,
    ):
        self._signer = TimestampSigner(str(secret_key))
        self._max_age = max_age
        self._serializer = serializer or JsonSerializer()

    async def read(self, session_id: str) -> typing.Dict[str, typing.Any]:
        """A session_id is a signed session value."""
        try:
            data = self._signer.unsign(session_id, max_age=self._max_age)
            return self._serializer.deserialize(b64decode(data).decode())
        except BadSignature:
            return {}

    async def write(
        self,
        data: typing.Dict[str, typing.Any],
        session_id: typing.Optional[str] = None,
    ) -> str:
        """The data is a session id in this backend."""
        encoded_data = b64encode(self._serializer.serialize(data).encode("utf-8"))
        return self._signer.sign(encoded_data).decode("utf-8")

    async def remove(self, session_id: str) -> None:
        """Session data stored on client side - no way to remove it."""

    async def exists(self, session_id: str) -> bool:
        return False
