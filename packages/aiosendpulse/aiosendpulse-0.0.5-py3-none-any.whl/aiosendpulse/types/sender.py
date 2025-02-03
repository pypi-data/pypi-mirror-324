from aiosendpulse.types.base import SendPulseObject


__all__ = ["Sender"]


class Sender(SendPulseObject):
    name: str
    email: str
