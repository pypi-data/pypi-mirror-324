from .base import MutableSendPulseObjectObject


__all__ = ["Result", "CreateTemplateResult"]


class Result(MutableSendPulseObjectObject):
    result: bool


class CreateTemplateResult(Result):
    real_id: int
