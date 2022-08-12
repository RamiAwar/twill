import typing
from datetime import datetime

from app.service.starsessions.backends import CookieBackend, SessionBackend
from app.service.starsessions.exceptions import ImproperlyConfigured
from app.service.starsessions.session import Session
from starlette.datastructures import MutableHeaders, Secret
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class SessionMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        session_cookie: str = "session",
        max_age: int = 14 * 24 * 60 * 60,  # 14 days, in seconds
        same_site: str = "lax",
        https_only: bool = False,
        autoload: bool = False,
        domain: typing.Optional[str] = None,
        path: typing.Optional[str] = None,
        secret_key: typing.Optional[typing.Union[str, Secret]] = None,
        backend: typing.Optional[SessionBackend] = None,
    ) -> None:
        self.app = app
        if backend is None:
            if secret_key is None:
                raise ImproperlyConfigured(
                    "CookieBackend requires secret_key argument."
                )
            backend = CookieBackend(secret_key, max_age)

        self.backend = backend
        self.session_cookie = session_cookie
        self.max_age = max_age
        self.autoload = autoload
        self.domain = domain
        self.path = path
        self.security_flags = "httponly; samesite=" + same_site
        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        session_id = connection.cookies.get(self.session_cookie, None)

        session = Session(self.backend, session_id)
        scope["session"] = session
        if self.autoload:
            await session.load()

        async def send_wrapper(message: Message) -> None:
            if message["type"] != "http.response.start":
                await send(message)
                return

            nonlocal session
            if not session.is_loaded:  # session was not accessed, do nothing
                await send(message)
                return

            path = self.path or scope.get("root_path", "") or "/"

            if session.is_empty:
                # session data loaded but empty, no matter whether it was initially empty or cleared
                # we have to remove the cookie and clear the storage
                if not self.path or self.path and scope["path"].startswith(self.path):
                    headers = MutableHeaders(scope=message)
                    header_value = "{}={}; {}".format(
                        self.session_cookie,
                        f"null; path={path}; expires=Thu, 01 Jan 1970 00:00:00 GMT;",
                        self.security_flags,
                    )
                    headers.append("Set-Cookie", header_value)
                    await self.backend.remove(scope["session"].session_id)
                await send(message)
                return

            # persist session data
            nonlocal session_id
            session_id = await session.persist()

            headers = MutableHeaders(scope=message)
            header_parts = [
                f"{self.session_cookie}={session_id}",
                f"path={path}",
            ]

            # Enforce correct frontend cookie expiry
            if self.max_age and session.data["_created"]:
                age = (
                    int(session.data["_created"])
                    + self.max_age
                    - int(datetime.utcnow().timestamp())
                )
                if age < 0:
                    session.clear()

                header_parts.append(f"Max-Age={age}")

            if self.domain:
                header_parts.append(f"Domain={self.domain}")

            header_parts.append(self.security_flags)
            header_value = "; ".join(header_parts)
            headers.append("Set-Cookie", header_value)

            await send(message)

        await self.app(scope, receive, send_wrapper)
