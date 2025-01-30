import typing
import typing_extensions
import pydantic


class PaymentThreeDsPurchaseInfo(pydantic.BaseModel):
    """
    Three DS Purchase Information for the payment request
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication_amount: typing.Optional[int] = pydantic.Field(
        alias="authenticationAmount", default=None
    )
    """
    Specifies the monetary value of a mobile or online transaction associated with an authentication event.
    """
    consumer_installment_authorization_count: typing.Optional[int] = pydantic.Field(
        alias="consumerInstallmentAuthorizationCount", default=None
    )
    """
    Indicates the maximum number of authorizations permitted for instalment payments.
    """
    purchase_date: typing.Optional[str] = pydantic.Field(
        alias="purchaseDate", default=None
    )
    """
    Designates the hour, minute and second  of the of the purchase which occurred on the Cardholder account
    """
    recurring_authorization_day_count: typing.Optional[int] = pydantic.Field(
        alias="recurringAuthorizationDayCount", default=None
    )
    """
    Indicates the minimum number of days between authorizations. The field is limited to maximum 4 characters.
    """
    recurring_authorization_expiration_date: typing.Optional[str] = pydantic.Field(
        alias="recurringAuthorizationExpirationDate", default=None
    )
    """
    Date after which no further authorizations shall be performed. This field is limited to 8 characters, and the accepted format is YYYYMMDD.
    """
    three_domain_secure_transaction_type: typing.Optional[
        typing_extensions.Literal[
            "ACCOUNT_FUNDING", "CHECK", "GOODS_SERVICES", "PREPAID", "QUASI_CASH"
        ]
    ] = pydantic.Field(alias="threeDomainSecureTransactionType", default=None)
    """
    Identifies the type of transaction being authenticated. The values are derived from ISO 8583.
    """
