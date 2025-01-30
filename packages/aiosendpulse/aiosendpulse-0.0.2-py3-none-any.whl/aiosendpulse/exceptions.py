from __future__ import annotations


class ExceptionDispatcher:
    exceptions: dict[int, SendPulseException] = {}

    def __init_subclass__(cls, **kwargs):
        cls.exceptions[cls.error_code] = cls  # noqa

    @classmethod
    def get(cls, error_code: int, **kwargs) -> SendPulseException:
        exc_class = cls.exceptions.get(error_code, SendPulseException)
        exc = exc_class()
        exc.message = exc.message.format_map(kwargs)
        return exc


class SendPulseException(Exception):
    error_code: int

    def __init__(self) -> None:
        self.message: str = "Something went wrong"

    def __str__(self) -> str:
        return f"{self.message}"


class NoDataError(ExceptionDispatcher, SendPulseException):
    error_code = 8

    def __init__(self) -> None:
        self.message = "No data"


class SenderEmailAddressMissingError(ExceptionDispatcher, SendPulseException):
    error_code = 10

    def __init__(self) -> None:
        self.message = "Sender email address is missing"


class RecipientsAddressesNotFoundError(ExceptionDispatcher, SendPulseException):
    error_code = 11

    def __init__(self) -> None:
        self.message = "Recipients addresses not found"


class EmailNotFoundError(ExceptionDispatcher, SendPulseException):
    error_code = 17

    def __init__(self) -> None:
        self.message = "Email not found"


class MailingListNotFoundError(ExceptionDispatcher, SendPulseException):
    error_code = 213

    def __init__(self) -> None:
        self.message = "Mailing list {mailing_list_id} not found"
