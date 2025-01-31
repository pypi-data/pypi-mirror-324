from typing import Union

from aiosendpulse.methods.email.addressbook import (
    AddEmailsToAddressbook,
    CreateAddressbook,
    EditAddressbook,
    GetAddressbook,
    GetEmailsFromAddressbook,
    GetListOfAddressbook,
    GetListOfAddressbookVariables,
)
from aiosendpulse.services.base import BaseService
from aiosendpulse.types import Addressbook, AddressbookId, AddressbookVariable, EmailDetail, Result


__all__ = ["AddressbookService"]


class AddressbookService(BaseService):
    async def create(self, name: str) -> AddressbookId:
        return await CreateAddressbook(
            book_name=name,
        )(client=self.http_client, auth=self.auth)

    async def edit(self, addressbook_id: int, name: str) -> Result:
        return await EditAddressbook(id=addressbook_id, name=name)(client=self.http_client, auth=self.auth)

    async def get_list(self, limit: int = None, offset: int = None) -> list[Addressbook]:
        return await GetListOfAddressbook(
            limit=limit,
            offset=offset,
        )(client=self.http_client, auth=self.auth)

    async def get(self, addressbook_id: int) -> Addressbook:
        method = GetAddressbook(id=addressbook_id)
        response = await method(client=self.http_client, auth=self.auth)
        if response:
            return response[0]

    async def variables(self, addressbook_id: int) -> list[AddressbookVariable]:
        return await GetListOfAddressbookVariables(
            id=addressbook_id,
        )(client=self.http_client, auth=self.auth)

    async def add_emails(self, addressbook_id: int, emails: list[Union[EmailDetail, dict]]) -> Result:
        return await AddEmailsToAddressbook(
            addressbook_id=addressbook_id,
            emails=emails,
        )(client=self.http_client, auth=self.auth)

    async def get_emails(
        self, addressbook_id: int, limit: int = None, offset: int = None, active: bool = None, not_active: bool = None
    ) -> list[EmailDetail]:
        return await GetEmailsFromAddressbook(
            id=addressbook_id,
            limit=limit,
            offset=offset,
            active=active,
            not_active=not_active,
        )(client=self.http_client, auth=self.auth)
