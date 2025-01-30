import typing
import typing_extensions
import pydantic


class LineItemTax(typing_extensions.TypedDict):
    """
    Tax information in the Line Item data within the Level 3.
    """

    line_item_tax_amount: typing_extensions.NotRequired[int]
    """
    The amount added to the transaction for taxes.
    """

    tax_percent: typing_extensions.NotRequired[str]
    """
    Specifies the ratio of the tax levied by a governmental authority on a product or service.
    """

    tax_type_code: typing_extensions.NotRequired[str]
    """
    Identifies the form of tax applied to a transaction. Valid values are  01= Federal/National Sales Tax; 02 = State Sales Tax; 03 = City Sales Tax; 04 = Local Sales Tax; 05 = Municipal Sales Tax; 06 = Other Tax; 10 = Value Added Tax (VAT); 11 = Goods and Services (GST); 12 = Provincial Sales Tax (PST); 13 = Harmonized Sales Tax (HST); 14 = Quebec Sales Tax (QST); 22 = Energy Tax
    """


class _SerializerLineItemTax(pydantic.BaseModel):
    """
    Serializer for LineItemTax handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    line_item_tax_amount: typing.Optional[int] = pydantic.Field(
        alias="lineItemTaxAmount", default=None
    )
    tax_percent: typing.Optional[str] = pydantic.Field(alias="taxPercent", default=None)
    tax_type_code: typing.Optional[str] = pydantic.Field(
        alias="taxTypeCode", default=None
    )
