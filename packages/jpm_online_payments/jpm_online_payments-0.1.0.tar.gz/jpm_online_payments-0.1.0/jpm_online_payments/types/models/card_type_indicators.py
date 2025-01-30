import typing
import typing_extensions
import pydantic


class CardTypeIndicators(pydantic.BaseModel):
    """
    The card type indicators provide additional information about the card. For example, if the card is a prepaid card and thus less likely to         support recurring payments or if the card is a healthcare or commercial  card.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    card_issuer_name: typing.Optional[str] = pydantic.Field(
        alias="cardIssuerName", default=None
    )
    """
    The label given to the issuer of a card-based payment account. The term "issuer" may refer to either the payment brand itself, as for the American Express and Discover payment brands, or the issuer will be a financial institution authorized to issue cards with the payment brand logo, as is the case for Visa and MasterCard.
    """
    card_product_name: typing.Optional[str] = pydantic.Field(
        alias="cardProductName", default=None
    )
    """
    Card product name as defined by payment networks. e.g. Signature Premium Debit.
    """
    card_product_types: typing.Optional[
        typing.List[
            typing_extensions.Literal[
                "AFFLUENT_CATEGORY",
                "COMMERCIAL",
                "HEALTHCARE",
                "PAYROLL",
                "PINLESS_DEBIT",
                "PREPAID_RELOADABLE",
                "SIGNATURE_DEBIT",
            ]
        ]
    ] = pydantic.Field(alias="cardProductTypes", default=None)
    """
    List of card products applicable for the account number.
    """
    card_type_category: typing.Optional[
        typing_extensions.Literal[
            "CHARGE_CARD",
            "CREDIT_CARD",
            "DEBIT_CARD",
            "DEFERRED_DEBIT",
            "NON_MASTERCARD",
            "PREPAID_CARD",
        ]
    ] = pydantic.Field(alias="cardTypeCategory", default=None)
    """
    Indicates how the issuer account is funded or used, e.g. Debit, Credit, Prepaid, Single Use..
    """
    combination_card_code: typing.Optional[
        typing_extensions.Literal[
            "CREDIT_AND_DEBIT", "CREDIT_AND_PREPAID", "NOT_A_COMBOCARD"
        ]
    ] = pydantic.Field(alias="combinationCardCode", default=None)
    """
    Codifies the card's ability to support both CREDIT and DEBIT payment transactions under the same Primary Account Number (PAN) as chosen by the consumer. Some subscription merchants can also decide to route transactions on one modality and retrial on the second one, upon consumer acknowledge/approval.
    """
    is_durbin_regulated: typing.Optional[bool] = pydantic.Field(
        alias="isDurbinRegulated", default=None
    )
    """
    Whether the card is regulated as per the Durbin Amendment
    """
    is_level3_eligible: typing.Optional[bool] = pydantic.Field(
        alias="isLevel3Eligible", default=None
    )
    """
    Whether the card is eligible for Level 3 fields
    """
    issuance_country_code: typing.Optional[str] = pydantic.Field(
        alias="issuanceCountryCode", default=None
    )
    """
    Identifies country of card issuing bank, using ISO Alpha 3 standards.
    """
    money_transfer_fast_funds_cross_border_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="moneyTransferFastFundsCrossBorderIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for money transfer and Fast Fund service and cross border transaction .
    """
    money_transfer_fast_funds_domestic_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="moneyTransferFastFundsDomesticIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for money transfer and Fast Fund service and domestic transaction .
    """
    money_transfer_push_funds_cross_border_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="moneyTransferPushFundsCrossBorderIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for money transfer and Push Fund service and cross border transaction .
    """
    money_transfer_push_funds_domestic_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="moneyTransferPushFundsDomesticIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for money transfer and Push Fund service and domestic transaction .
    """
    non_money_transfer_fast_funds_cross_border_indicator: typing.Optional[bool] = (
        pydantic.Field(
            alias="nonMoneyTransferFastFundsCrossBorderIndicator", default=None
        )
    )
    """
    Indicates whether the payment card is used for Non-Money Transfer and Fast Fund service and cross border transaction .
    """
    non_money_transfer_fast_funds_domestic_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="nonMoneyTransferFastFundsDomesticIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for Non-Money Transfer and Fast Fund service and domestic transaction .
    """
    non_money_transfer_push_funds_cross_border_indicator: typing.Optional[bool] = (
        pydantic.Field(
            alias="nonMoneyTransferPushFundsCrossBorderIndicator", default=None
        )
    )
    """
    Indicates whether the payment card is used for Non-Money Transfer and Push Fund service and cross border transaction .
    """
    non_money_transfer_push_funds_domestic_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="nonMoneyTransferPushFundsDomesticIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for Non-Money Transfer and Push Fund service and domestic transaction .
    """
    online_gambling_fast_funds_cross_border_indicator: typing.Optional[bool] = (
        pydantic.Field(
            alias="onlineGamblingFastFundsCrossBorderIndicator", default=None
        )
    )
    """
    Indicates whether the payment card is used for online gambling and Fast Fund service and cross border transaction .
    """
    online_gambling_fast_funds_domestic_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="onlineGamblingFastFundsDomesticIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for online gambling and Fast Fund service and domestic transaction .
    """
    online_gambling_push_funds_cross_border_indicator: typing.Optional[bool] = (
        pydantic.Field(
            alias="onlineGamblingPushFundsCrossBorderIndicator", default=None
        )
    )
    """
    Indicates whether the payment card is used for online gambling and Push Fund service and cross border transaction .
    """
    online_gambling_push_funds_domestic_indicator: typing.Optional[bool] = (
        pydantic.Field(alias="onlineGamblingPushFundsDomesticIndicator", default=None)
    )
    """
    Indicates whether the payment card is used for online gambling and Push Fund service and domestic transaction .
    """
    prepaid_card_category_code: typing.Optional[
        typing_extensions.Literal["NON_RELOADABLE", "NOT_PREPAID", "RELOADABLE"]
    ] = pydantic.Field(alias="prepaidCardCategoryCode", default=None)
    """
    Codifies the high level grouping of prepaid payment card supported by payment processing system.
    """
