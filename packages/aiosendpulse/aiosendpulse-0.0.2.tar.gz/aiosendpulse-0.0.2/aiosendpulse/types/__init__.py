from .email import EmailDetail
from .mailing_list import MailingList, MailingListId
from .mailing_list_variable import MailingListVariable
from .result import CreateTemplateResult, Result
from .template import Template
from .template_category import TemplateCategory
from .token import Token


Template.model_rebuild()


__all__ = [
    "EmailDetail",
    "MailingList",
    "MailingListId",
    "MailingListVariable",
    "CreateTemplateResult",
    "Result",
    "Template",
    "TemplateCategory",
    "Token",
]
