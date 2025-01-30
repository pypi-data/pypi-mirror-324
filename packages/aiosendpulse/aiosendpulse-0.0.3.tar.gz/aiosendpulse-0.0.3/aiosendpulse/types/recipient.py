from aiosendpulse.types.base import SendPulseObject


__all__ = ["Recipient"]


class Recipient(SendPulseObject):
    name: str
    email: str
