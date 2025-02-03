from typing import Annotated

from httpx import URL, Request
from pydantic import Field

from aiosendpulse.methods.base import SendPulseMethod
from aiosendpulse.types import EmailDetail


__all__ = ["SearchEmails"]


class SearchEmails(SendPulseMethod[list[EmailDetail]]):
    id: int
    variable_name: Annotated[str, Field(serialization_alias="variableName")]
    search_value: Annotated[str, Field(serialization_alias="searchValue")]

    __http_method__ = "GET"
    __api_endpoint__ = "/addressbooks/{id}/variables/{variable_name}/emails/{search_value}"
    __returning__ = list[EmailDetail]
    __path_params__ = {"id", "variable_name", "search_value"}

    def build_request(self, base_url: URL) -> Request:
        data = {}
        if self.__body_params__:
            data = {
                "json" if self.__content_type__ == "application/json" else "body": self.model_dump(
                    include=self.__body_params__,
                    exclude_none=True,
                    exclude_unset=True,
                    by_alias=True,
                ),
            }
        return Request(
            method=self.__http_method__,
            url=base_url.join(
                url=self.__api_endpoint__.format_map(
                    self.model_dump(include=self.__path_params__) if self.__path_params__ else {}
                ),
            ),
            params=self.model_dump(include=self.__query_parameters__) if self.__query_parameters__ else {},
            headers={"content-type": self.__content_type__},
            **data,
        )
