import typing
import typing_extensions
import pydantic

from .fraud_card import FraudCard, _SerializerFraudCard


class FraudCheckPaymentMethodType(typing_extensions.TypedDict):
    """
    Object with information for Payment Method Type for  Fraud Check
    """

    card: typing_extensions.NotRequired[FraudCard]
    """
    Card payment instrument for fraud checking
    """


class _SerializerFraudCheckPaymentMethodType(pydantic.BaseModel):
    """
    Serializer for FraudCheckPaymentMethodType handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    card: typing.Optional[_SerializerFraudCard] = pydantic.Field(
        alias="card", default=None
    )
