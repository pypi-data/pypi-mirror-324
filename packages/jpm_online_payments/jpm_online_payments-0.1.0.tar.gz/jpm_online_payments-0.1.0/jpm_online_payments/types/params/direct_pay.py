import typing
import typing_extensions
import pydantic

from .direct_pay_sender import DirectPaySender, _SerializerDirectPaySender


class DirectPay(typing_extensions.TypedDict):
    """
    Direct Pay
    """

    currency_conversion_fee_amount: typing_extensions.NotRequired[int]
    """
    Optional currency conversion fee charged by merchant.  Only applicable to AFT transactions.
    """

    direct_payment_type: typing_extensions.NotRequired[
        typing_extensions.Literal["PULL_FUNDS", "PUSH_FUNDS"]
    ]
    """
    Indicator that specifies whether you want to pull funds from a funding source or push funds to a receiving target.
    """

    funds_transfer_type: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ACCOUNT_TO_ACCOUNT",
            "FUNDS_DISBURSEMENT",
            "FUNDS_TRANSFER",
            "GAMBLING_PAY",
            "GOVERNMENT_DISBURSEMENT",
            "LOYALTY_PAY",
            "MERCHANT_DISBURSEMENT",
            "ONLINE_GAMBLING_PAY",
            "PAYROLL_DISBURSEMENT",
            "PERSON_TO_PERSON",
            "PREPAID_CARD",
            "WALLET_TRANSFER",
        ]
    ]
    """
    Codifies the intended use of a payment using direct pay by the merchant. It determines the data carried in the message, the limits and economics that may apply to the transaction, and may be used by the sending and/or receiving issuer to make an authorization decision.
    """

    sender: typing_extensions.NotRequired[DirectPaySender]
    """
    Direct Pay Sender
    """

    service_fee_amount: typing_extensions.NotRequired[int]
    """
    Optional Service Fee charged by merchant for use of service.  Only applicable to AFT transactions.
    """

    transaction_reason: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ACCOUNT_MANAGEMENT",
            "BONUS_PAYMENT",
            "BUSINESS_EXPENSE",
            "BUS_TRANSPORT",
            "CAR_INSURANCE",
            "CASH_MANAGEMENT_TRANSFER",
            "CC_REIMBURSEMENT",
            "CHARITY",
            "COLLECTION",
            "COMMISSION",
            "COMPENSATION",
            "COPYRIGHT",
            "CREDIT_CARD_PAYMENT",
            "DEBIT_CARD",
            "DEBIT_REIMBURSEMENT",
            "DEPOSIT",
            "DIVIDENT",
            "ELECTRICITY_BILL",
            "ENERGIES",
            "FERRY",
            "FOREIGN_EXCHANGE",
            "GAS_BILL",
            "GENERAL_FEE",
            "GOVERNMENT_CASH_COMP",
            "GOVORNMENT_PAYMENT",
            "HEALTH_INSURANCE",
            "INSOLVENCY",
            "INSTALLMENT",
            "INSURANCE_CLAIM",
            "INSURANCE_PREMIUM",
            "INTEREST",
            "INTRA_COMPANY",
            "INVESTMENT",
            "LABOR_INSURANCE",
            "LICENCE_FEE",
            "LIFE_INSURANCE",
            "LOAN",
            "MEDICAL_SERVICE",
            "MOBILE_P2B",
            "MOBILE_P2P",
            "MOBILE_TOPUP",
            "MUTUAL_FUND_INVESTMENT",
            "NOT_OTHERWISE",
            "OTHERS",
            "OTHER_TEL_BILL",
            "PAYMENT_ALLOWANCE",
            "PAYROLL",
            "PENSION_FUND",
            "PENSION_PAYMENT",
            "PROPERTY_INSURANCE",
            "RAIL_TRANSPORT",
            "REFUND_TAX",
            "RENT",
            "RENTAL_LEASE",
            "ROYALTY",
            "SALARY",
            "SAVING_RETIREMENT",
            "SECURITIES",
            "SETTLEMENT_ANNUITY",
            "SOCIAL_SECURITY",
            "STUDY",
            "STUDY_TUITION",
            "SUBSCRIPTION",
            "SUPPLIER",
            "TAX",
            "TAX_INCOME",
            "TELEPHONE_BILL",
            "TEL_BILL",
            "TRADE_SERVICE",
            "TRAVEL",
            "TREASURY",
            "UNEMPLOYMEMNT_DISABILITY_BENEFIT",
            "UTILITY_BILL",
            "VAT",
            "WATER_BILL",
            "WITH_HOLD",
        ]
    ]
    """
    Codifies the purpose of the payment based on the standard values defined for respective market.
    """


class _SerializerDirectPay(pydantic.BaseModel):
    """
    Serializer for DirectPay handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    currency_conversion_fee_amount: typing.Optional[int] = pydantic.Field(
        alias="currencyConversionFeeAmount", default=None
    )
    direct_payment_type: typing.Optional[
        typing_extensions.Literal["PULL_FUNDS", "PUSH_FUNDS"]
    ] = pydantic.Field(alias="directPaymentType", default=None)
    funds_transfer_type: typing.Optional[
        typing_extensions.Literal[
            "ACCOUNT_TO_ACCOUNT",
            "FUNDS_DISBURSEMENT",
            "FUNDS_TRANSFER",
            "GAMBLING_PAY",
            "GOVERNMENT_DISBURSEMENT",
            "LOYALTY_PAY",
            "MERCHANT_DISBURSEMENT",
            "ONLINE_GAMBLING_PAY",
            "PAYROLL_DISBURSEMENT",
            "PERSON_TO_PERSON",
            "PREPAID_CARD",
            "WALLET_TRANSFER",
        ]
    ] = pydantic.Field(alias="fundsTransferType", default=None)
    sender: typing.Optional[_SerializerDirectPaySender] = pydantic.Field(
        alias="sender", default=None
    )
    service_fee_amount: typing.Optional[int] = pydantic.Field(
        alias="serviceFeeAmount", default=None
    )
    transaction_reason: typing.Optional[
        typing_extensions.Literal[
            "ACCOUNT_MANAGEMENT",
            "BONUS_PAYMENT",
            "BUSINESS_EXPENSE",
            "BUS_TRANSPORT",
            "CAR_INSURANCE",
            "CASH_MANAGEMENT_TRANSFER",
            "CC_REIMBURSEMENT",
            "CHARITY",
            "COLLECTION",
            "COMMISSION",
            "COMPENSATION",
            "COPYRIGHT",
            "CREDIT_CARD_PAYMENT",
            "DEBIT_CARD",
            "DEBIT_REIMBURSEMENT",
            "DEPOSIT",
            "DIVIDENT",
            "ELECTRICITY_BILL",
            "ENERGIES",
            "FERRY",
            "FOREIGN_EXCHANGE",
            "GAS_BILL",
            "GENERAL_FEE",
            "GOVERNMENT_CASH_COMP",
            "GOVORNMENT_PAYMENT",
            "HEALTH_INSURANCE",
            "INSOLVENCY",
            "INSTALLMENT",
            "INSURANCE_CLAIM",
            "INSURANCE_PREMIUM",
            "INTEREST",
            "INTRA_COMPANY",
            "INVESTMENT",
            "LABOR_INSURANCE",
            "LICENCE_FEE",
            "LIFE_INSURANCE",
            "LOAN",
            "MEDICAL_SERVICE",
            "MOBILE_P2B",
            "MOBILE_P2P",
            "MOBILE_TOPUP",
            "MUTUAL_FUND_INVESTMENT",
            "NOT_OTHERWISE",
            "OTHERS",
            "OTHER_TEL_BILL",
            "PAYMENT_ALLOWANCE",
            "PAYROLL",
            "PENSION_FUND",
            "PENSION_PAYMENT",
            "PROPERTY_INSURANCE",
            "RAIL_TRANSPORT",
            "REFUND_TAX",
            "RENT",
            "RENTAL_LEASE",
            "ROYALTY",
            "SALARY",
            "SAVING_RETIREMENT",
            "SECURITIES",
            "SETTLEMENT_ANNUITY",
            "SOCIAL_SECURITY",
            "STUDY",
            "STUDY_TUITION",
            "SUBSCRIPTION",
            "SUPPLIER",
            "TAX",
            "TAX_INCOME",
            "TELEPHONE_BILL",
            "TEL_BILL",
            "TRADE_SERVICE",
            "TRAVEL",
            "TREASURY",
            "UNEMPLOYMEMNT_DISABILITY_BENEFIT",
            "UTILITY_BILL",
            "VAT",
            "WATER_BILL",
            "WITH_HOLD",
        ]
    ] = pydantic.Field(alias="transactionReason", default=None)
