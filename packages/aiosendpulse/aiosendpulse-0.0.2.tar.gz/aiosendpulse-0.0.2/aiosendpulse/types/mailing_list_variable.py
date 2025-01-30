from typing import Literal

from .base import MutableSendPulseObjectObject


__all__ = ["MailingListVariable"]


class MailingListVariable(MutableSendPulseObjectObject):
    name: str
    type: Literal["string", "date", "number"]
