from typing import Union

from aiosendpulse.methods.email.mailing_list import (
    AddEmailsToMailingList,
    CreateMailingList,
    EditMailingList,
    GetEmailsList,
    GetListMailingListVariables,
    GetListOfMailingLists,
    GetMailingList,
)
from aiosendpulse.services.base import BaseService
from aiosendpulse.types import EmailDetail, MailingList, MailingListId, MailingListVariable, Result


__all__ = ["MailingListService"]


class MailingListService(BaseService):
    async def create(self, name: str) -> MailingListId:
        return await CreateMailingList(
            book_name=name,
        )(client=self.http_client, auth=self.auth)

    async def edit(self, mailing_list_id: int, name: str) -> Result:
        return await EditMailingList(id=mailing_list_id, name=name)(client=self.http_client, auth=self.auth)

    async def all(self, limit: int = None, offset: int = None) -> list[MailingList]:
        return await GetListOfMailingLists(
            limit=limit,
            offset=offset,
        )(client=self.http_client, auth=self.auth)

    async def get(self, mailing_list_id: int) -> MailingList:
        method = GetMailingList(id=mailing_list_id)
        response = await method(client=self.http_client, auth=self.auth)
        if response:
            return response[0]

    async def variables(self, mailing_list_id: int) -> list[MailingListVariable]:
        return await GetListMailingListVariables(
            id=mailing_list_id,
        )(client=self.http_client, auth=self.auth)

    async def add_emails(self, mailing_list_id: int, emails: list[Union[EmailDetail, dict]]) -> Result:
        return await AddEmailsToMailingList(
            mailing_list_id=mailing_list_id,
            emails=emails,
        )(client=self.http_client, auth=self.auth)

    async def get_emails(
        self, mailing_list_id: int, limit: int = None, offset: int = None, active: bool = None, not_active: bool = None
    ) -> list[EmailDetail]:
        return await GetEmailsList(
            id=mailing_list_id,
            limit=limit,
            offset=offset,
            active=active,
            not_active=not_active,
        )(client=self.http_client, auth=self.auth)
