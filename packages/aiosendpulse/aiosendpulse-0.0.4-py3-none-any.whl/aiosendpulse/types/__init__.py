from .addressbook import Addressbook, AddressbookId
from .addressbook_variable import AddressbookVariable
from .email import EmailDetail
from .recipient import Recipient
from .result import CreateTemplateResult, Result
from .sender import Sender
from .template import Template, TemplateMeta
from .template_category import TemplateCategory
from .token import Token


Template.model_rebuild()


__all__ = [
    "Addressbook",
    "AddressbookId",
    "AddressbookVariable",
    "EmailDetail",
    "Recipient",
    "CreateTemplateResult",
    "Result",
    "Sender",
    "Template",
    "TemplateMeta",
    "TemplateCategory",
    "Token",
]
