import typing
import typing_extensions
import pydantic

from .refund_authentication import RefundAuthentication, _SerializerRefundAuthentication
from .card_type_indicators import CardTypeIndicators, _SerializerCardTypeIndicators
from .expiry import Expiry, _SerializerExpiry
from .network_response import NetworkResponse, _SerializerNetworkResponse
from .payment_token import PaymentToken, _SerializerPaymentToken


class RefundCard(typing_extensions.TypedDict):
    """
    Card payment instrument for refund
    """

    account_number: typing_extensions.Required[str]
    """
    The card or token number.
    """

    authentication: typing_extensions.NotRequired[RefundAuthentication]
    """
    The authentication object allows you to opt in to additional security features specific for refund
    """

    card_type: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "AP",
            "AX",
            "CC",
            "CR",
            "CZ",
            "DC",
            "DI",
            "EP",
            "IM",
            "JC",
            "MC",
            "MR",
            "NP",
            "PP",
            "SP",
            "VI",
            "VR",
        ]
    ]
    """
    Abbreviation of card name
    """

    card_type_indicators: typing_extensions.NotRequired[CardTypeIndicators]
    """
    The card type indicators provide additional information about the card. For example, if the card is a prepaid card and thus less likely to         support recurring payments or if the card is a healthcare or commercial  card.
    """

    card_type_name: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ACCEL_PINLESS",
            "AMERICAN_EXPRESS",
            "CHASENET_CREDIT",
            "CHASENET_SIGNATURE_DEBIT",
            "CHINA_UNION_PAY",
            "DINERS_CLUB",
            "DISCOVER",
            "EFTPOS_PINLESS",
            "INTERNATIONAL_MAESTRO",
            "JCB",
            "MASTERCARD",
            "MASTERCARD_RESTRICTED_DEBIT",
            "NYCE_PINLESS",
            "PULSE_PINLESS",
            "STAR_PINLESS",
            "VISA",
            "VISA_RESTRICTED_DEBIT",
        ]
    ]
    """
    Name of the payment network.
    """

    encrypted_payload: typing_extensions.NotRequired[str]
    """
    Encrypted message details have been rendered unreadable by general means through the application of a given set of instructions and a key.
    """

    expiry: typing_extensions.NotRequired[Expiry]
    """
    Expiration date
    """

    is_bill_payment: typing_extensions.NotRequired[bool]
    """
    Indicates whether or not the transaction is identified as a bill payment, prearranged between the cardholder and the merchant.
    """

    masked_account_number: typing_extensions.NotRequired[str]
    """
    Identifies a concealed number associated with the card number recognized by various payment systems. This is typically concealed by storing only the first 6 and/or last 4 digits of the payment account number or some variation.
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

    network_response: typing_extensions.NotRequired[NetworkResponse]
    """
    Response information from payment network
    """

    original_network_transaction_id: typing_extensions.NotRequired[str]
    """
    When submitting a merchant-initiated payment, submit the networkTransactionId received from the first payment in this field.
    """

    payment_tokens: typing_extensions.NotRequired[typing.List[PaymentToken]]
    """
    List of payment tokens for the transaction
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

    wallet_provider: typing_extensions.NotRequired[
        typing_extensions.Literal["APPLE_PAY", "GOOGLE_PAY", "PAZE"]
    ]
    """
    Name of wallet provider.
    """


class _SerializerRefundCard(pydantic.BaseModel):
    """
    Serializer for RefundCard handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    account_number: str = pydantic.Field(
        alias="accountNumber",
    )
    authentication: typing.Optional[_SerializerRefundAuthentication] = pydantic.Field(
        alias="authentication", default=None
    )
    card_type: typing.Optional[
        typing_extensions.Literal[
            "AP",
            "AX",
            "CC",
            "CR",
            "CZ",
            "DC",
            "DI",
            "EP",
            "IM",
            "JC",
            "MC",
            "MR",
            "NP",
            "PP",
            "SP",
            "VI",
            "VR",
        ]
    ] = pydantic.Field(alias="cardType", default=None)
    card_type_indicators: typing.Optional[_SerializerCardTypeIndicators] = (
        pydantic.Field(alias="cardTypeIndicators", default=None)
    )
    card_type_name: typing.Optional[
        typing_extensions.Literal[
            "ACCEL_PINLESS",
            "AMERICAN_EXPRESS",
            "CHASENET_CREDIT",
            "CHASENET_SIGNATURE_DEBIT",
            "CHINA_UNION_PAY",
            "DINERS_CLUB",
            "DISCOVER",
            "EFTPOS_PINLESS",
            "INTERNATIONAL_MAESTRO",
            "JCB",
            "MASTERCARD",
            "MASTERCARD_RESTRICTED_DEBIT",
            "NYCE_PINLESS",
            "PULSE_PINLESS",
            "STAR_PINLESS",
            "VISA",
            "VISA_RESTRICTED_DEBIT",
        ]
    ] = pydantic.Field(alias="cardTypeName", default=None)
    encrypted_payload: typing.Optional[str] = pydantic.Field(
        alias="encryptedPayload", default=None
    )
    expiry: typing.Optional[_SerializerExpiry] = pydantic.Field(
        alias="expiry", default=None
    )
    is_bill_payment: typing.Optional[bool] = pydantic.Field(
        alias="isBillPayment", default=None
    )
    masked_account_number: typing.Optional[str] = pydantic.Field(
        alias="maskedAccountNumber", default=None
    )
    merchant_preferred_routing: typing.Optional[
        typing_extensions.Literal["CREDIT", "PINLESS"]
    ] = pydantic.Field(alias="merchantPreferredRouting", default=None)
    merchant_sales_channel_name: typing.Optional[
        typing_extensions.Literal[
            "INTERACTIVE_VOICE_RESPONSE", "INTERNET", "MAIL_ORDER_TELEPHONE_ORDER"
        ]
    ] = pydantic.Field(alias="merchantSalesChannelName", default=None)
    network_response: typing.Optional[_SerializerNetworkResponse] = pydantic.Field(
        alias="networkResponse", default=None
    )
    original_network_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="originalNetworkTransactionId", default=None
    )
    payment_tokens: typing.Optional[typing.List[_SerializerPaymentToken]] = (
        pydantic.Field(alias="paymentTokens", default=None)
    )
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
    wallet_provider: typing.Optional[
        typing_extensions.Literal["APPLE_PAY", "GOOGLE_PAY", "PAZE"]
    ] = pydantic.Field(alias="walletProvider", default=None)
