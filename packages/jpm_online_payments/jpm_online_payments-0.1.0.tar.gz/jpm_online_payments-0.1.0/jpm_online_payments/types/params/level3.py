import typing
import typing_extensions
import pydantic

from .line_item import LineItem, _SerializerLineItem
from .transaction_advice import TransactionAdvice, _SerializerTransactionAdvice


class Level3(typing_extensions.TypedDict):
    """
    Level 3 data provides commercial shoppers with additional information about purchases on their card statements.
    """

    alternate_tax_amount: typing_extensions.NotRequired[int]
    """
    Total monetary value of alternate tax associated with this payment.
    """

    duty_amount: typing_extensions.NotRequired[int]
    """
    The monetary value for an additional tax levied or tariff charged against the purchase of goods or services imported from another country.
    """

    line_items: typing_extensions.NotRequired[typing.List[LineItem]]
    """
    List Of line Items
    """

    order_discount_treatment_code: typing_extensions.NotRequired[str]
    """
    Indicates how the merchant is managing discounts for the order. Valid values: 0 ? No invoice level discount provided 1 ? Tax calculated on the post-discount invoice total 2 ? Tax calculated on the pre-discount invoice total
    """

    party_tax_government_issued_identifier: typing_extensions.NotRequired[str]
    """
    Tax ID number assigned by a government agency for the alternate tax associated with this payment.
    """

    ship_from_address_postal_code: typing_extensions.NotRequired[str]
    """
    The postal code from which the goods were shipped.
    """

    ship_to_address_country_code: typing_extensions.NotRequired[str]
    """
    The country code of the shipping address based on Alpha 3 ISO standards.
    """

    ship_to_address_postal_code: typing_extensions.NotRequired[str]
    """
    The postal code of the shipping address.
    """

    shipping_value_added_tax_amount: typing_extensions.NotRequired[int]
    """
    Monetary value of value added tax (VAT) amount on shipping or freight.
    """

    shipping_value_added_tax_percent: typing_extensions.NotRequired[str]
    """
    The percentage of Value added tax (VAT) for shipping or freight added to the payment. Two decimals implied, e.g. 250 = 2.5%.
    """

    tax_treatment_code: typing_extensions.NotRequired[str]
    """
    Identifies the type of processing that will be applied to the invoice, such as whether gross or net pricing is used, if tax will be calculated at the line item or invoice level, or if zero tax is applied.  Valid values:  0- Net prices with tax calculated at line item level  1 ? Net prices with tax calculated at invoice level  2 ? Gross prices given with tax information provided at line item level  3 ? Gross prices given with tax information provided at invoice level  4 ? No tax applies.
    """

    total_shipping_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value to be paid for the postage and related transportation to get a package from the shipping carrier to the consumer for all items purchased.
    """

    total_transaction_discount_amount: typing_extensions.NotRequired[int]
    """
    Monetary value of total discount amount applied to the payment.
    """

    transaction_advices: typing_extensions.NotRequired[typing.List[TransactionAdvice]]
    """
    List of transaction advices from American Express
    """

    value_added_tax_amount: typing_extensions.NotRequired[int]
    """
    Monetary value of the value added tax (VAT) included on the payment.
    """

    value_added_tax_invoice_reference_number: typing_extensions.NotRequired[str]
    """
    Identifies the additional sub-element used to identify the value-added tax (VAT) invoice or tax receipt.
    """

    value_added_tax_percent: typing_extensions.NotRequired[str]
    """
    The percentage of value added tax (VAT) added to the payment. Two decimals implied, e.g. 250 = 2.5%.
    """


class _SerializerLevel3(pydantic.BaseModel):
    """
    Serializer for Level3 handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    alternate_tax_amount: typing.Optional[int] = pydantic.Field(
        alias="alternateTaxAmount", default=None
    )
    duty_amount: typing.Optional[int] = pydantic.Field(alias="dutyAmount", default=None)
    line_items: typing.Optional[typing.List[_SerializerLineItem]] = pydantic.Field(
        alias="lineItems", default=None
    )
    order_discount_treatment_code: typing.Optional[str] = pydantic.Field(
        alias="orderDiscountTreatmentCode", default=None
    )
    party_tax_government_issued_identifier: typing.Optional[str] = pydantic.Field(
        alias="partyTaxGovernmentIssuedIdentifier", default=None
    )
    ship_from_address_postal_code: typing.Optional[str] = pydantic.Field(
        alias="shipFromAddressPostalCode", default=None
    )
    ship_to_address_country_code: typing.Optional[str] = pydantic.Field(
        alias="shipToAddressCountryCode", default=None
    )
    ship_to_address_postal_code: typing.Optional[str] = pydantic.Field(
        alias="shipToAddressPostalCode", default=None
    )
    shipping_value_added_tax_amount: typing.Optional[int] = pydantic.Field(
        alias="shippingValueAddedTaxAmount", default=None
    )
    shipping_value_added_tax_percent: typing.Optional[str] = pydantic.Field(
        alias="shippingValueAddedTaxPercent", default=None
    )
    tax_treatment_code: typing.Optional[str] = pydantic.Field(
        alias="taxTreatmentCode", default=None
    )
    total_shipping_amount: typing.Optional[int] = pydantic.Field(
        alias="totalShippingAmount", default=None
    )
    total_transaction_discount_amount: typing.Optional[int] = pydantic.Field(
        alias="totalTransactionDiscountAmount", default=None
    )
    transaction_advices: typing.Optional[typing.List[_SerializerTransactionAdvice]] = (
        pydantic.Field(alias="transactionAdvices", default=None)
    )
    value_added_tax_amount: typing.Optional[int] = pydantic.Field(
        alias="valueAddedTaxAmount", default=None
    )
    value_added_tax_invoice_reference_number: typing.Optional[str] = pydantic.Field(
        alias="valueAddedTaxInvoiceReferenceNumber", default=None
    )
    value_added_tax_percent: typing.Optional[str] = pydantic.Field(
        alias="valueAddedTaxPercent", default=None
    )
