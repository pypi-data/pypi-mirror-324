from datetime import datetime

from .base import MutableSendPulseObjectObject


__all__ = ["MailingList", "MailingListId"]


class MailingListId(MutableSendPulseObjectObject):
    id: int


class MailingList(MailingListId):
    name: str
    all_email_qty: int
    active_email_qty: int
    inactive_email_qty: int
    active_phones_quantity: int
    exc_phones_quantity: int
    creationdate: datetime
    status: int
    status_explain: str
