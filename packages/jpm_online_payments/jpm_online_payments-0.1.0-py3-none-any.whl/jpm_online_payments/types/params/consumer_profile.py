import typing
import typing_extensions
import pydantic

from .authentication import Authentication, _SerializerAuthentication
from .payment_authentication_request import (
    PaymentAuthenticationRequest,
    _SerializerPaymentAuthenticationRequest,
)


class ConsumerProfile(typing_extensions.TypedDict):
    """
    Consumer Profile Payment method and attributes needed to process a transaction.
    """

    account_type: typing_extensions.NotRequired[
        typing_extensions.Literal["CHECKING", "CORPORATE_CHECKING", "SAVING"]
    ]
    """
    Type of banking account.
    """

    authentication: typing_extensions.NotRequired[Authentication]
    """
    The authentication object allows you to opt in to additional security features like 3-D Secure
    """

    card_type_funding: typing_extensions.NotRequired[
        typing_extensions.Literal["CREDIT", "DEBIT"]
    ]
    """
    Codifies the funding source for a card payment transaction. This will support debit enablement to merchant during processing transaction. Sample values are CREDIT_CARD and DEBIT_CARD
    """

    consumer_profile_id: typing_extensions.Required[str]
    """
    Identifies a unique occurrence of a consumer maintained in the firm as requested by merchant. Consumer profile contains information relevant to processing transactions such as name, address, account and payment methods information.
    """

    cvv: typing_extensions.NotRequired[str]
    """
    Card verification value (CVV/CV2)
    """

    is_bill_payment: typing_extensions.NotRequired[bool]
    """
    Indicates whether or not the transaction is identified as a bill payment, prearranged between the cardholder and the merchant.
    """

    is_transaction_micro_entry: typing_extensions.NotRequired[bool]
    """
    Indicates If a Micro-Entry  is used for account validation purposes. *Micro-Entries are defined as ACH credits of less than $1 and any offsetting ACH debits to verify a Receiver?s account.
    """

    merchant_preferred_routing: typing_extensions.NotRequired[
        typing_extensions.Literal["CREDIT", "PINLESS"]
    ]
    """
    Indicates the routing model used to route the transaction as preferred by merchant.
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

    payment_authentication_request: typing_extensions.NotRequired[
        PaymentAuthenticationRequest
    ]
    """
    Request Authentication during payment process
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

    preferred_payment_network_name_list: typing_extensions.NotRequired[
        typing.List[
            typing_extensions.Literal[
                "ACCEL_PINLESS",
                "EFTPOS_PINLESS",
                "NYCE_PINLESS",
                "PULSE_PINLESS",
                "STAR_PINLESS",
            ]
        ]
    ]
    """
    Define the list of Payment Network Name preferred by merchant.  Payment Network Name is the label for primary transactions processing network through which card's (Debit or credit) account transactions are processed.
    """


class _SerializerConsumerProfile(pydantic.BaseModel):
    """
    Serializer for ConsumerProfile handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    account_type: typing.Optional[
        typing_extensions.Literal["CHECKING", "CORPORATE_CHECKING", "SAVING"]
    ] = pydantic.Field(alias="accountType", default=None)
    authentication: typing.Optional[_SerializerAuthentication] = pydantic.Field(
        alias="authentication", default=None
    )
    card_type_funding: typing.Optional[typing_extensions.Literal["CREDIT", "DEBIT"]] = (
        pydantic.Field(alias="cardTypeFunding", default=None)
    )
    consumer_profile_id: str = pydantic.Field(
        alias="consumerProfileId",
    )
    cvv: typing.Optional[str] = pydantic.Field(alias="cvv", default=None)
    is_bill_payment: typing.Optional[bool] = pydantic.Field(
        alias="isBillPayment", default=None
    )
    is_transaction_micro_entry: typing.Optional[bool] = pydantic.Field(
        alias="isTransactionMicroEntry", default=None
    )
    merchant_preferred_routing: typing.Optional[
        typing_extensions.Literal["CREDIT", "PINLESS"]
    ] = pydantic.Field(alias="merchantPreferredRouting", default=None)
    merchant_sales_channel_name: typing.Optional[
        typing_extensions.Literal[
            "INTERACTIVE_VOICE_RESPONSE", "INTERNET", "MAIL_ORDER_TELEPHONE_ORDER"
        ]
    ] = pydantic.Field(alias="merchantSalesChannelName", default=None)
    original_network_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalNetworkTransactionId", default=None
    )
    payment_authentication_request: typing.Optional[
        _SerializerPaymentAuthenticationRequest
    ] = pydantic.Field(alias="paymentAuthenticationRequest", default=None)
    payment_method_id: typing.Optional[str] = pydantic.Field(
        alias="paymentMethodId", default=None
    )
    payment_type: typing.Optional[
        typing_extensions.Literal["RECURRING", "TEL", "WEB"]
    ] = pydantic.Field(alias="paymentType", default=None)
    preferred_payment_network_name_list: typing.Optional[
        typing.List[
            typing_extensions.Literal[
                "ACCEL_PINLESS",
                "EFTPOS_PINLESS",
                "NYCE_PINLESS",
                "PULSE_PINLESS",
                "STAR_PINLESS",
            ]
        ]
    ] = pydantic.Field(alias="preferredPaymentNetworkNameList", default=None)
