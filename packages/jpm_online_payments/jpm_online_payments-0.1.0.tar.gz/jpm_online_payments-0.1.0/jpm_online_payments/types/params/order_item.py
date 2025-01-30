import typing
import typing_extensions
import pydantic


class OrderItem(typing_extensions.TypedDict):
    """
    Partner's customer order line level information
    """

    chosen_shipping_option: typing_extensions.NotRequired[str]
    """
    Provides textual information about the method of the delivery of an item(s) to the customer.
    """

    item_comodity_code: typing_extensions.NotRequired[str]
    """
    Codifies the category the item being purchased belongs in a standardized commodity group as defined by the card acceptor.
    """

    line_item_description_text: typing_extensions.NotRequired[str]
    """
    Provides detailed information regarding specific goods or services that have been procured and for which payment has been requested.
    """

    line_item_unit_quantity: typing_extensions.NotRequired[str]
    """
    Enumerates the volume (quantity) of each individual product type included in the transaction. The quantity, unit of measure and the line item price is used to calculate the aggregated purchase amount for each line item. In some cases, quantity can include a fraction or decimal places to allow for items such as hours of service provided, or a pound portion of goods.
    """

    merchant_campaign_name: typing_extensions.NotRequired[str]
    """
    The moniker given to the merchant initiative that is in place to pursue an opportunity for business expansion for potential new and existing clients.
    """

    merchant_product_identifier: typing_extensions.NotRequired[str]
    """
    A unique merchant assigned identifier for an item or service offered for sale by the Merch
    """

    unit_price_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value of the per-item cost of a good or service.
    """


class _SerializerOrderItem(pydantic.BaseModel):
    """
    Serializer for OrderItem handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    chosen_shipping_option: typing.Optional[str] = pydantic.Field(
        alias="chosenShippingOption", default=None
    )
    item_comodity_code: typing.Optional[str] = pydantic.Field(
        alias="itemComodityCode", default=None
    )
    line_item_description_text: typing.Optional[str] = pydantic.Field(
        alias="lineItemDescriptionText", default=None
    )
    line_item_unit_quantity: typing.Optional[str] = pydantic.Field(
        alias="lineItemUnitQuantity", default=None
    )
    merchant_campaign_name: typing.Optional[str] = pydantic.Field(
        alias="merchantCampaignName", default=None
    )
    merchant_product_identifier: typing.Optional[str] = pydantic.Field(
        alias="merchantProductIdentifier", default=None
    )
    unit_price_amount: typing.Optional[int] = pydantic.Field(
        alias="unitPriceAmount", default=None
    )
