import typing
import typing_extensions
import pydantic

from .authentication import Authentication, _SerializerAuthentication


class RefundConsumerProfile(typing_extensions.TypedDict):
    """
    Consumer Profile Payment method and attributes needed to process a refund transaction.
    """

    authentication: typing_extensions.NotRequired[Authentication]
    """
    The authentication object allows you to opt in to additional security features like 3-D Secure
    """

    consumer_profile_id: typing_extensions.Required[str]
    """
    Identifies a unique occurrence of a consumer maintained in the firm as requested by merchant. Consumer profile contains information relevant to processing transactions such as name, address, account and payment methods information.
    """

    is_bill_payment: typing_extensions.NotRequired[bool]
    """
    Indicates whether or not the transaction is identified as a bill payment, prearranged between the cardholder and the merchant.
    """

    is_transaction_micro_entry: typing_extensions.NotRequired[bool]
    """
    Indicates If a Micro-Entry  is used for account validation purposes. *Micro-Entries are defined as ACH credits of less than $1 and any offsetting ACH debits to verify a Receiver?s account.
    """

    merchant_sales_channel_name: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "INTERACTIVE_VOICE_RESPONSE", "INTERNET", "MAIL_ORDER_TELEPHONE_ORDER"
        ]
    ]
    """
    Label given to a merchant client of the Firm's medium for reaching its customers and facilitating and/or performing sales of its merchandise or services.
    """

    original_network_transaction_id: typing_extensions.NotRequired[str]
    """
    When submitting a merchant-initiated payment, submit the networkTransactionId received from the first payment in this field.
    """

    payment_method_id: typing_extensions.NotRequired[str]
    """
    Identifies a unique occurrence of the type of payment accepted by a level of the hierarchy of the merchant acquiring account.
    """

    payment_type: typing_extensions.NotRequired[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ]
    """
    Identifies how accountholders  initiated debits to their accounts .
    """


class _SerializerRefundConsumerProfile(pydantic.BaseModel):
    """
    Serializer for RefundConsumerProfile handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    authentication: typing.Optional[_SerializerAuthentication] = pydantic.Field(
        alias="authentication", default=None
    )
    consumer_profile_id: str = pydantic.Field(
        alias="consumerProfileId",
    )
    is_bill_payment: typing.Optional[bool] = pydantic.Field(
        alias="isBillPayment", default=None
    )
    is_transaction_micro_entry: typing.Optional[bool] = pydantic.Field(
        alias="isTransactionMicroEntry", default=None
    )
    merchant_sales_channel_name: typing.Optional[
        typing_extensions.Literal[
            "INTERACTIVE_VOICE_RESPONSE", "INTERNET", "MAIL_ORDER_TELEPHONE_ORDER"
        ]
    ] = pydantic.Field(alias="merchantSalesChannelName", default=None)
    original_network_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalNetworkTransactionId", default=None
    )
    payment_method_id: typing.Optional[str] = pydantic.Field(
        alias="paymentMethodId", default=None
    )
    payment_type: typing.Optional[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ] = pydantic.Field(alias="paymentType", default=None)
