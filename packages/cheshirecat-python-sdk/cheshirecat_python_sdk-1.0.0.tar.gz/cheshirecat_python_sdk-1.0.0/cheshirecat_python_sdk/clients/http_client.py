import asyncio
from abc import ABC, abstractmethod
from aiohttp import ClientSession
from requests_toolbelt.sessions import BaseUrlSession
from urllib.parse import urlunparse
from typing import Callable, List, Any
from requests.adapters import BaseAdapter


class MiddlewareAdapter(BaseAdapter):
    def __init__(self, middleware: Callable):
        super().__init__()
        self.middleware = middleware

    def send(self, request, **kwargs):
        request = self.middleware(request, **kwargs)
        return super().send(request, **kwargs)


class HttpClientMixin(ABC):
    def __init__(
        self,
        host: str,
        port: int | None = None,
        apikey: str | None = None,
        is_https: bool = False
    ):
        self.apikey = apikey
        self.token = None
        self.user_id = None
        self.agent_id = None
        self.headers = {}

        self.middlewares: List[Callable] = [
            self.before_secure_request,
            self.before_jwt_request,
        ]

        scheme = "https" if is_https else "http"
        netloc = f"{host}:{port}" if port else host
        self.http_uri = urlunparse((scheme, netloc, "", "", "", ""))

    def set_token(self, token: str):
        self.token = token
        return self

    def get_http_uri(self) -> str:
        return self.http_uri

    def before_secure_request(self):
        if self.apikey:
            self.headers["Authorization"] = f"Bearer {self.apikey}"
        if self.user_id:
            self.headers["user_id"] = self.user_id
        if self.agent_id:
            self.headers["agent_id"] = self.agent_id

    def before_jwt_request(self):
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        if self.agent_id:
            self.headers["agent_id"] = self.agent_id

    def get_client(self, agent_id: str | None = None, user_id: str | None = None) -> BaseUrlSession:
        if not self.apikey and not self.token:
            raise ValueError("You must provide an apikey or a token")

        self.agent_id = agent_id or "agent"
        self.user_id = user_id

        for middleware in self.middlewares:
            middleware()

        return self.get_session()

    @abstractmethod
    def get_session(self) -> Any:
        pass


class HttpClient(HttpClientMixin):
    def get_session(self) -> BaseUrlSession:
        session = BaseUrlSession(base_url=self.http_uri)
        session.headers = self.headers

        return session


class AsyncHttpClient(HttpClientMixin):
    def get_session(self) -> ClientSession:
        loop = asyncio.get_event_loop()
        return ClientSession(base_url=self.http_uri, headers=self.headers, loop=loop)
