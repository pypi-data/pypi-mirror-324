from aiosendpulse.services.base import BaseService
from aiosendpulse.services.email.blacklist import BlacklistService
from aiosendpulse.services.email.mailing_list import MailingListService


__all__ = ["EmailService"]


class EmailService(BaseService):
    @property
    def mailing_lists(self) -> MailingListService:
        return MailingListService(client=self.client)

    @property
    def blacklist(self) -> BlacklistService:
        return BlacklistService(client=self.client)
