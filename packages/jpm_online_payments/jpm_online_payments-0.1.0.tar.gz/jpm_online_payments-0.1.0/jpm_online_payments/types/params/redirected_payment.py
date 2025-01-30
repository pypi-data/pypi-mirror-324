import typing
import typing_extensions
import pydantic


class RedirectedPayment(typing_extensions.TypedDict):
    """
    Redirected Payment attributes
    """

    merchant_return_url: typing_extensions.NotRequired[str]
    """
    Information on where consumer needs to be redirected after payment process completion. Ensure that the URL begins with 'https'.
    """

    redirect_url: typing_extensions.NotRequired[str]
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with 'https'
    """

    secret_key: typing_extensions.NotRequired[str]
    """
    Provides textual information about a cipher key using random string returned by payment processor for session validity
    """

    timestamp_returned: typing_extensions.NotRequired[str]
    """
    Provides a timestamp (UTC). Designates the hour (hh), minute (mm), seconds (ss) and date (if timestamp) or year (YYYY), month (MM), and day (DD) (if date)
    """


class _SerializerRedirectedPayment(pydantic.BaseModel):
    """
    Serializer for RedirectedPayment handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    merchant_return_url: typing.Optional[str] = pydantic.Field(
        alias="merchantReturnUrl", default=None
    )
    redirect_url: typing.Optional[str] = pydantic.Field(
        alias="redirectUrl", default=None
    )
    secret_key: typing.Optional[str] = pydantic.Field(alias="secretKey", default=None)
    timestamp_returned: typing.Optional[str] = pydantic.Field(
        alias="timestampReturned", default=None
    )
