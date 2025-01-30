import typing
import pydantic


class RedirectedPayment(pydantic.BaseModel):
    """
    Redirected Payment attributes
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    merchant_return_url: typing.Optional[str] = pydantic.Field(
        alias="merchantReturnUrl", default=None
    )
    """
    Information on where consumer needs to be redirected after payment process completion. Ensure that the URL begins with 'https'.
    """
    redirect_url: typing.Optional[str] = pydantic.Field(
        alias="redirectUrl", default=None
    )
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with 'https'
    """
    secret_key: typing.Optional[str] = pydantic.Field(alias="secretKey", default=None)
    """
    Provides textual information about a cipher key using random string returned by payment processor for session validity
    """
    timestamp_returned: typing.Optional[str] = pydantic.Field(
        alias="timestampReturned", default=None
    )
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """
