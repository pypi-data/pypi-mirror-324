import typing
import typing_extensions
import pydantic


class PaymentThreeDsPurchaseInfo(typing_extensions.TypedDict):
    """
    Three DS Purchase Information for the payment request
    """

    authentication_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value of a mobile or online transaction associated with an authentication event.
    """

    consumer_installment_authorization_count: typing_extensions.NotRequired[int]
    """
    Indicates the maximum number of authorizations permitted for instalment payments.
    """

    purchase_date: typing_extensions.NotRequired[str]
    """
    Designates the hour, minute and second  of the of the purchase which occurred on the Cardholder account
    """

    recurring_authorization_day_count: typing_extensions.NotRequired[int]
    """
    Indicates the minimum number of days between authorizations. The field is limited to maximum 4 characters.
    """

    recurring_authorization_expiration_date: typing_extensions.NotRequired[str]
    """
    Date after which no further authorizations shall be performed. This field is limited to 8 characters, and the accepted format is YYYYMMDD.
    """

    three_domain_secure_transaction_type: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ACCOUNT_FUNDING", "CHECK", "GOODS_SERVICES", "PREPAID", "QUASI_CASH"
        ]
    ]
    """
    Identifies the type of transaction being authenticated. The values are derived from ISO 8583.
    """


class _SerializerPaymentThreeDsPurchaseInfo(pydantic.BaseModel):
    """
    Serializer for PaymentThreeDsPurchaseInfo handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    authentication_amount: typing.Optional[int] = pydantic.Field(
        alias="authenticationAmount", default=None
    )
    consumer_installment_authorization_count: typing.Optional[int] = pydantic.Field(
        alias="consumerInstallmentAuthorizationCount", default=None
    )
    purchase_date: typing.Optional[str] = pydantic.Field(
        alias="purchaseDate", default=None
    )
    recurring_authorization_day_count: typing.Optional[int] = pydantic.Field(
        alias="recurringAuthorizationDayCount", default=None
    )
    recurring_authorization_expiration_date: typing.Optional[str] = pydantic.Field(
        alias="recurringAuthorizationExpirationDate", default=None
    )
    three_domain_secure_transaction_type: typing.Optional[
        typing_extensions.Literal[
            "ACCOUNT_FUNDING", "CHECK", "GOODS_SERVICES", "PREPAID", "QUASI_CASH"
        ]
    ] = pydantic.Field(alias="threeDomainSecureTransactionType", default=None)
