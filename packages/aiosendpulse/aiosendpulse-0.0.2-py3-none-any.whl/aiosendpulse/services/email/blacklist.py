from aiosendpulse.methods.email.blacklist import AddEmailsToBlacklist, DeleteEmailsFromBlacklist
from aiosendpulse.services.base import BaseService
from aiosendpulse.types import Result


__all__ = ["BlacklistService"]


class BlacklistService(BaseService):
    async def add_emails_to_blacklist(self, emails: list[str], comment: str = None) -> Result:
        return await AddEmailsToBlacklist(
            emails=emails,
            comment=comment,
        )(client=self.http_client, auth=self.auth)

    async def delete_emails_from_blacklist(self, emails: list[str]) -> Result:
        return await DeleteEmailsFromBlacklist(emails=emails)(client=self.http_client, auth=self.auth)
