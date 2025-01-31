import typing

from httpx import Auth, Request, Response


__all__ = ["BearerTokenAuth"]


class BearerTokenAuth(Auth):
    def __init__(self, token: str, header: str = "Authorization") -> None:
        self.__token = token
        self.header = header

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        request.headers[self.header] = f"Bearer {self.__token}"
        yield request

    @property
    def token(self) -> str:
        return self.__token
