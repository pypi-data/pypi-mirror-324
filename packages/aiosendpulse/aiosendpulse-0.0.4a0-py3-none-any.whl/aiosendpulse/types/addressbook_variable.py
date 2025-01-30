from typing import Literal

from .base import MutableSendPulseObjectObject


__all__ = ["AddressbookVariable"]


class AddressbookVariable(MutableSendPulseObjectObject):
    name: str
    type: Literal["string", "date", "number"]
