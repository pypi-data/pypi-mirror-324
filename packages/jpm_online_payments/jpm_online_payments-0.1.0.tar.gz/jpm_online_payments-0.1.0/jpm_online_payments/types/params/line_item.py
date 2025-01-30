import typing
import typing_extensions
import pydantic

from .line_item_tax import LineItemTax, _SerializerLineItemTax


class LineItem(typing_extensions.TypedDict):
    """
    Line Item data within the Level 3
    """

    item_comodity_code: typing_extensions.NotRequired[str]
    """
    Commodity code used to classify the item purchased.
    """

    line_item_description_text: typing_extensions.NotRequired[str]
    """
    Description of the item purchased.
    """

    line_item_detail_code: typing_extensions.NotRequired[str]
    """
    Indicates type of line item detail record. Valid values: 0 ? Normal line item detail record; 1 ? Normal last line item detail record; 2 ? Credit line item detail record; 3 ? Credit last line item detail record; 4 ? Payment line item detail record; 5 ? Payment last line item detail record; Note: If this field is not populated, 0 will be sent to Visa
    """

    line_item_discount_indicator: typing_extensions.NotRequired[bool]
    """
    Indicates whether the amount is discounted.
    """

    line_item_discount_treatment_code: typing_extensions.NotRequired[str]
    """
    Indicates how the merchant is managing discounts on the item. Valid values: Y ? Amount is discounted N ? Amount is not discounted
    """

    line_item_tax_indicator: typing_extensions.NotRequired[bool]
    """
    Indicates whether tax amount is included in item amount.
    """

    line_item_taxes: typing_extensions.NotRequired[typing.List[LineItemTax]]
    """
    List Of line Items Tax Information
    """

    line_item_unit_quantity: typing_extensions.NotRequired[str]
    """
    Number of units purchased.
    """

    line_item_unitof_measure_code: typing_extensions.NotRequired[str]
    """
    Item Bulk/Unit of measure code. (example: LBR = pound, MIN = minute, Acre=ACR)
    """

    merchant_product_identifier: typing_extensions.NotRequired[str]
    """
    Product code assigned by merchant of the item purchased.
    """

    purchase_transaction_discount_percent: typing_extensions.NotRequired[str]
    """
    Specifies the ratio of the reduction amount applied by the merchant (e.g., based on a percentage or fixed amount) to the purchase amount on a transaction. Discount percentages could be calculated at individual line item, or total transaction levels.
    """

    tax_inclusive_line_item_total_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value (inclusive of tax) for the price of the product or service multiplied by the quantity of the items purchased recorded in the transaction addendum data.
    """

    transaction_discount_amount: typing_extensions.NotRequired[int]
    """
    Monetary value of total discount amount applied to order.
    """

    unit_price_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value of the per-item cost of a good or service.
    """


class _SerializerLineItem(pydantic.BaseModel):
    """
    Serializer for LineItem handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    item_comodity_code: typing.Optional[str] = pydantic.Field(
        alias="itemComodityCode", default=None
    )
    line_item_description_text: typing.Optional[str] = pydantic.Field(
        alias="lineItemDescriptionText", default=None
    )
    line_item_detail_code: typing.Optional[str] = pydantic.Field(
        alias="lineItemDetailCode", default=None
    )
    line_item_discount_indicator: typing.Optional[bool] = pydantic.Field(
        alias="lineItemDiscountIndicator", default=None
    )
    line_item_discount_treatment_code: typing.Optional[str] = pydantic.Field(
        alias="lineItemDiscountTreatmentCode", default=None
    )
    line_item_tax_indicator: typing.Optional[bool] = pydantic.Field(
        alias="lineItemTaxIndicator", default=None
    )
    line_item_taxes: typing.Optional[typing.List[_SerializerLineItemTax]] = (
        pydantic.Field(alias="lineItemTaxes", default=None)
    )
    line_item_unit_quantity: typing.Optional[str] = pydantic.Field(
        alias="lineItemUnitQuantity", default=None
    )
    line_item_unitof_measure_code: typing.Optional[str] = pydantic.Field(
        alias="lineItemUnitofMeasureCode", default=None
    )
    merchant_product_identifier: typing.Optional[str] = pydantic.Field(
        alias="merchantProductIdentifier", default=None
    )
    purchase_transaction_discount_percent: typing.Optional[str] = pydantic.Field(
        alias="purchaseTransactionDiscountPercent", default=None
    )
    tax_inclusive_line_item_total_amount: typing.Optional[int] = pydantic.Field(
        alias="taxInclusiveLineItemTotalAmount", default=None
    )
    transaction_discount_amount: typing.Optional[int] = pydantic.Field(
        alias="transactionDiscountAmount", default=None
    )
    unit_price_amount: typing.Optional[int] = pydantic.Field(
        alias="unitPriceAmount", default=None
    )
