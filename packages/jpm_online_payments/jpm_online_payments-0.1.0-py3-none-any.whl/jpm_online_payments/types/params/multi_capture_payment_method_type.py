import typing
import typing_extensions
import pydantic

from .card import Card, _SerializerCard


class MultiCapturePaymentMethodType(typing_extensions.TypedDict):
    """
    Multi Capture Payment Method Type contains all the payment method code supported for multi capture payment processing capability
    """

    card: typing_extensions.NotRequired[Card]
    """
    Card payment instrument
    """


class _SerializerMultiCapturePaymentMethodType(pydantic.BaseModel):
    """
    Serializer for MultiCapturePaymentMethodType handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    card: typing.Optional[_SerializerCard] = pydantic.Field(alias="card", default=None)
