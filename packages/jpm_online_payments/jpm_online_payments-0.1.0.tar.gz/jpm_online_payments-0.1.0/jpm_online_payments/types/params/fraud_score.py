import typing
import typing_extensions
import pydantic


class FraudScore(typing_extensions.TypedDict):
    """
    Object for Fraud Score Information
    """

    a_ni_telephone_number: typing_extensions.NotRequired[str]
    """
    A locator whose value identifies the formatted numeric address for routing voice or data communications via telephony, to reach a party. NOTE: Telephone number formats may vary; this field can include domestic and international telephone numbers.
    """

    cardholder_browser_information: typing_extensions.NotRequired[str]
    """
    The label for a web browser which is used to access and view websites for the merchant's products and services by consumer who is making a purchase.
    """

    fencible_item_amount: typing_extensions.NotRequired[int]
    """
    The monetary value of items that are typically locked or stored behind the counter and aren't available for general selection on store shelves by customers.
    """

    fraud_check_shopping_cart: typing_extensions.NotRequired[str]
    """
    Provides textual information about the purchase of a product or service via an online retailer that is stored via a digital basket that enables consumers to select products, review what they selected and make modifications before finalizing the purchase.  Supplemental: In this context, User (merchant) defined information may be included such as fraud rule values. Examples of fraud rules value may be a maximum basket value, a maximum product quantity, etc.
    """

    is_fraud_rule_return: typing_extensions.NotRequired[bool]
    """
    Indicates the fraud checking rules that flagged the payment transaction as potentially fraudulent are returned to the merchant.
    """

    session_id: typing_extensions.NotRequired[str]
    """
    Identifies an interaction between a customer and a representative with the Firm within a given application tool.
    """

    website_root_domain_name: typing_extensions.NotRequired[str]
    """
    The label given to combination of the Web Address Top Level and the Web Address Second Level domain identifiers. This is commonly referred to as the website name.
    """


class _SerializerFraudScore(pydantic.BaseModel):
    """
    Serializer for FraudScore handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    a_ni_telephone_number: typing.Optional[str] = pydantic.Field(
        alias="aNITelephoneNumber", default=None
    )
    cardholder_browser_information: typing.Optional[str] = pydantic.Field(
        alias="cardholderBrowserInformation", default=None
    )
    fencible_item_amount: typing.Optional[int] = pydantic.Field(
        alias="fencibleItemAmount", default=None
    )
    fraud_check_shopping_cart: typing.Optional[str] = pydantic.Field(
        alias="fraudCheckShoppingCart", default=None
    )
    is_fraud_rule_return: typing.Optional[bool] = pydantic.Field(
        alias="isFraudRuleReturn", default=None
    )
    session_id: typing.Optional[str] = pydantic.Field(alias="sessionId", default=None)
    website_root_domain_name: typing.Optional[str] = pydantic.Field(
        alias="websiteRootDomainName", default=None
    )
