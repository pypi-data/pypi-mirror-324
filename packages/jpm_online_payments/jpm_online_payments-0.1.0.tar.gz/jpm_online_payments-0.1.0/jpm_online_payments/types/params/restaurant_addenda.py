import typing
import typing_extensions
import pydantic


class RestaurantAddenda(typing_extensions.TypedDict):
    """
    Restaurant Addenda
    """

    gratuity_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value paid by the consumer over and above the payment due for service.
    """

    restaurant_server_number: typing_extensions.NotRequired[str]
    """
    Uniuque Identifier of a restaurant server assigned by the merchant.
    """

    surcharge_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value of an additional charge by a United States (US) merchant for the customer's usage of the credit card on a domestic US purchase. Surcharging is prohibited outside the US and in several US states and territories. The no-surcharge list currently includes California, Colorado, Connecticut, Florida, Kansas, Maine, Massachusetts, New York, Oklahoma, Texas and Puerto Rico.
    """

    tax_amount: typing_extensions.NotRequired[int]
    """
    Monetary value of the tax amount assessed to the payment.
    """


class _SerializerRestaurantAddenda(pydantic.BaseModel):
    """
    Serializer for RestaurantAddenda handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    gratuity_amount: typing.Optional[int] = pydantic.Field(
        alias="gratuityAmount", default=None
    )
    restaurant_server_number: typing.Optional[str] = pydantic.Field(
        alias="restaurantServerNumber", default=None
    )
    surcharge_amount: typing.Optional[int] = pydantic.Field(
        alias="surchargeAmount", default=None
    )
    tax_amount: typing.Optional[int] = pydantic.Field(alias="taxAmount", default=None)
