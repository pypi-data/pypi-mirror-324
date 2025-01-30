import typing
import typing_extensions
import pydantic


class PaymentThreeDsAccountAdditionalInfo(pydantic.BaseModel):
    """
    Additional account  Information used for authentication processing.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    consumer_account24_hours_add_card_count: typing.Optional[int] = pydantic.Field(
        alias="consumerAccount24HoursAddCardCount", default=None
    )
    """
    Number of Card addition attempts to  the consumer account during last 24 hours.
    """
    consumer_account_address_identical_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="consumerAccountAddressIdenticalIndicator", default=None)
    )
    """
    Indicates if the Cardholder billing address and shipping address are identical for this transaction.
    """
    consumer_account_create_length: typing.Optional[
        typing_extensions.Literal[
            "BETWEEN_THIRTY_AND_SIXTY",
            "GREATER_THAN_SIXTY",
            "LESS_THAN_THIRTY",
            "NEW_ACCOUNT",
            "NO_ACCOUNT",
        ]
    ] = pydantic.Field(alias="consumerAccountCreateLength", default=None)
    """
    Indicates how long the cardholder  has had the account with the merchant or authentication requestor in days.
    """
    consumer_account_create_timestamp: typing.Optional[str] = pydantic.Field(
        alias="consumerAccountCreateTimestamp", default=None
    )
    """
    The create date of the consumer account with merchant.
    """
    consumer_account_first_shipping_date: typing.Optional[str] = pydantic.Field(
        alias="consumerAccountFirstShippingDate", default=None
    )
    """
    Indicates when the shipping address used for this transaction was first used with the 3DS Requestor.
    """
    consumer_account_password_change_length: typing.Optional[
        typing_extensions.Literal[
            "BETWEEN_THIRTY_AND_SIXTY",
            "CURRENT_TXN_CHANGE",
            "GREATER_THAN_SIXTY",
            "LESS_THAN_THIRTY",
            "NO_CHANGE",
        ]
    ] = pydantic.Field(alias="consumerAccountPasswordChangeLength", default=None)
    """
    Indicates  the length of time since the consumer account password was last updated in days.
    """
    consumer_account_password_update_timestamp: typing.Optional[str] = pydantic.Field(
        alias="consumerAccountPasswordUpdateTimestamp", default=None
    )
    """
    Indicates  when consumer account password was last updated.
    """
    consumer_account_ship_name_identical_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="consumerAccountShipNameIdenticalIndicator", default=None)
    )
    """
    Indicates if the Cardholder Name on the account is identical to the shipping Name used for this transaction.
    """
    consumer_account_shipping_address_length: typing.Optional[
        typing_extensions.Literal[
            "BETWEEN_THIRTY_AND_SIXTY",
            "CURRENT_TXN_CHANGE",
            "GREATER_THAN_SIXTY",
            "LESS_THAN_THIRTY",
        ]
    ] = pydantic.Field(alias="consumerAccountShippingAddressLength", default=None)
    """
    Indicates when the shipping address used for this transaction was first used with the 3DS Requestor in days.
    """
    consumer_account_suspicious_activity_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="consumerAccountSuspiciousActivityIndicator", default=None)
    )
    """
    Indicates whether the 3DS Requestor has experienced suspicious activity (including previous fraud) on the cardholder account.
    """
    consumer_account_update_length: typing.Optional[
        typing_extensions.Literal[
            "BETWEEN_THIRTY_AND_SIXTY",
            "CURRENT_TXN",
            "GREATER_THAN_SIXTY",
            "LESS_THAN_THIRTY",
        ]
    ] = pydantic.Field(alias="consumerAccountUpdateLength", default=None)
    """
    Length of time since the cardholder?s account information with the 3DS Requestor was last changed. Includes Billing or Shipping address, new payment account, or new user(s) added.
    """
    consumer_account_update_timestamp: typing.Optional[str] = pydantic.Field(
        alias="consumerAccountUpdateTimestamp", default=None
    )
    """
    Indicates  when consumer account with merchant was last modified.
    """
    consumer_payment_account_enrollment_date: typing.Optional[str] = pydantic.Field(
        alias="consumerPaymentAccountEnrollmentDate", default=None
    )
    """
    Indicates the date  the  payment method  was enrolled in the consumer account with the 3DS Requestor.
    """
    consumer_payment_account_length: typing.Optional[
        typing_extensions.Literal[
            "BETWEEN_THIRTY_AND_SIXTY",
            "CURRENT_TXN_CHANGE",
            "GREATER_THAN_SIXTY",
            "LESS_THAN_THIRTY",
            "NO_ACCOUNT",
        ]
    ] = pydantic.Field(alias="consumerPaymentAccountLength", default=None)
    """
    Indicates how long the payment method has been stored in the consumer account in days.
    """
    previous_year_transaction_count: typing.Optional[int] = pydantic.Field(
        alias="previousYearTransactionCount", default=None
    )
    """
    Number of transactions with the 3DS Requestor across all payment methods for this consumer account in the previous year.
    """
    six_month_transaction_count: typing.Optional[int] = pydantic.Field(
        alias="sixMonthTransactionCount", default=None
    )
    """
    Merchant reported number of purchases with this consumer account during the previous six months.
    """
    twenty_four_hours_transaction_count: typing.Optional[int] = pydantic.Field(
        alias="twentyFourHoursTransactionCount", default=None
    )
    """
    Number of transactions with the 3DS Requestor across all payment methods for this consumer account in the previous 24 hours.
    """
