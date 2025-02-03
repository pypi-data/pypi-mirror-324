from aiosendpulse.types.base import MutableSendPulseObjectObject


__all__ = ["TotalEmails"]


class TotalEmails(MutableSendPulseObjectObject):
    total: int
