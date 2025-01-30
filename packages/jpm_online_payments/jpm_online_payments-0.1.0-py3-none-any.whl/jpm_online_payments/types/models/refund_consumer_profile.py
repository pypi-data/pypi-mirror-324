import typing
import typing_extensions
import pydantic

from .authentication import Authentication


class RefundConsumerProfile(pydantic.BaseModel):
    """
    Consumer Profile Payment method and attributes needed to process a refund transaction.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication: typing.Optional[Authentication] = pydantic.Field(
        alias="authentication", default=None
    )
    """
    The authentication object allows you to opt in to additional security features like 3-D Secure
    """
    consumer_profile_id: str = pydantic.Field(
        alias="consumerProfileId",
    )
    """
    Identifies a unique occurrence of a consumer maintained in the firm as requested by merchant. Consumer profile contains information relevant to processing transactions such as name, address, account and payment methods information.
    """
    is_bill_payment: typing.Optional[bool] = pydantic.Field(
        alias="isBillPayment", default=None
    )
    """
    Indicates whether or not the transaction is identified as a bill payment, prearranged between the cardholder and the merchant.
    """
    is_transaction_micro_entry: typing.Optional[bool] = pydantic.Field(
        alias="isTransactionMicroEntry", default=None
    )
    """
    Indicates If a Micro-Entry  is used for account validation purposes. *Micro-Entries are defined as ACH credits of less than $1 and any offsetting ACH debits to verify a Receiver?s account.
    """
    merchant_sales_channel_name: typing.Optional[
        typing_extensions.Literal[
            "INTERACTIVE_VOICE_RESPONSE", "INTERNET", "MAIL_ORDER_TELEPHONE_ORDER"
        ]
    ] = pydantic.Field(alias="merchantSalesChannelName", default=None)
    """
    Label given to a merchant client of the Firm's medium for reaching its customers and facilitating and/or performing sales of its merchandise or services.
    """
    original_network_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalNetworkTransactionId", default=None
    )
    """
    When submitting a merchant-initiated payment, submit the networkTransactionId received from the first payment in this field.
    """
    payment_method_id: typing.Optional[str] = pydantic.Field(
        alias="paymentMethodId", default=None
    )
    """
    Identifies a unique occurrence of the type of payment accepted by a level of the hierarchy of the merchant acquiring account.
    """
    payment_type: typing.Optional[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ] = pydantic.Field(alias="paymentType", default=None)
    """
    Identifies how accountholders  initiated debits to their accounts .
    """
