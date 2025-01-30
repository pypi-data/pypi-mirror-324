import typing
import pydantic


class LineItemTax(pydantic.BaseModel):
    """
    Tax information in the Line Item data within the Level 3.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    line_item_tax_amount: typing.Optional[int] = pydantic.Field(
        alias="lineItemTaxAmount", default=None
    )
    """
    The amount added to the transaction for taxes.
    """
    tax_percent: typing.Optional[str] = pydantic.Field(alias="taxPercent", default=None)
    """
    Specifies the ratio of the tax levied by a governmental authority on a product or service.
    """
    tax_type_code: typing.Optional[str] = pydantic.Field(
        alias="taxTypeCode", default=None
    )
    """
    Identifies the form of tax applied to a transaction. Valid values are  01= Federal/National Sales Tax; 02 = State Sales Tax; 03 = City Sales Tax; 04 = Local Sales Tax; 05 = Municipal Sales Tax; 06 = Other Tax; 10 = Value Added Tax (VAT); 11 = Goods and Services (GST); 12 = Provincial Sales Tax (PST); 13 = Harmonized Sales Tax (HST); 14 = Quebec Sales Tax (QST); 22 = Energy Tax
    """
