from cheshirecat_python_sdk.clients import HttpClient, WSClient, AsyncHttpClient
from cheshirecat_python_sdk.configuration import Configuration
from cheshirecat_python_sdk.endpoints import (
    AdminsEndpoint,
    AuthHandlerEndpoint,
    EmbedderEndpoint,
    FileManagerEndpoint,
    LargeLanguageModelEndpoint,
    MemoryEndpoint,
    MessageEndpoint,
    PluginsEndpoint,
    RabbitHoleEndpoint,
    SettingsEndpoint,
    UsersEndpoint,
)


class CheshireCatClient:
    def __init__(self, configuration: Configuration, token: str | None = None):
        self.__http_client = HttpClient(
            host=configuration.host,
            port=configuration.port,
            apikey=configuration.auth_key,
            is_https=configuration.secure_connection
        )
        self.__async_http_client = AsyncHttpClient(
            host=configuration.host,
            port=configuration.port,
            apikey=configuration.auth_key,
            is_https=configuration.secure_connection
        )
        self.__ws_client = WSClient(
            host=configuration.host,
            port=configuration.port,
            apikey=configuration.auth_key,
            is_wss=configuration.secure_connection
        )

        if token:
            self.add_token(token)

        self.admins = AdminsEndpoint(self)
        self.auth_handler = AuthHandlerEndpoint(self)
        self.embedder = EmbedderEndpoint(self)
        self.file_manager = FileManagerEndpoint(self)
        self.large_language_model = LargeLanguageModelEndpoint(self)
        self.memory = MemoryEndpoint(self)
        self.message = MessageEndpoint(self)
        self.plugins = PluginsEndpoint(self)
        self.rabbit_hole = RabbitHoleEndpoint(self)
        self.settings = SettingsEndpoint(self)
        self.users = UsersEndpoint(self)

    def add_token(self, token: str) -> 'CheshireCatClient':
        self.__ws_client.set_token(token)
        self.__http_client.set_token(token)
        return self

    @property
    def http_client(self) -> HttpClient:
        return self.__http_client

    @property
    def async_http_client(self) -> AsyncHttpClient:
        return self.__async_http_client

    @property
    def ws_client(self) -> WSClient:
        return self.__ws_client
