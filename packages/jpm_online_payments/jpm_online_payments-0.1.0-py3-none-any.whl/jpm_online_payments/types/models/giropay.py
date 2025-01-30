import typing
import pydantic

from .redirected_payment import RedirectedPayment


class Giropay(pydantic.BaseModel):
    """
    Giropay is German based payment method that allows customers to complete transactions online using their online banking environment, with funds debited from their bank account.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    completion_time: typing.Optional[str] = pydantic.Field(
        alias="completionTime", default=None
    )
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """
    creation_time: typing.Optional[str] = pydantic.Field(
        alias="creationTime", default=None
    )
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """
    preferred_language: typing.Optional[str] = pydantic.Field(
        alias="preferredLanguage", default=None
    )
    """
    Language preference indicated by consumer for pages displayed. Using language tags indicated in RFC5646.
    """
    redirected_payment: typing.Optional[RedirectedPayment] = pydantic.Field(
        alias="redirectedPayment", default=None
    )
    """
    Redirected Payment attributes
    """
