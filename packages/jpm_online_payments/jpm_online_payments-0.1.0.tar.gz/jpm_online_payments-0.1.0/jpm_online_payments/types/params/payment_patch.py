import typing
import typing_extensions
import pydantic

from .sub_merchant_supplemental_data import (
    SubMerchantSupplementalData,
    _SerializerSubMerchantSupplementalData,
)


class PaymentPatch(typing_extensions.TypedDict):
    """
    Payment Update
    """

    amount: typing_extensions.NotRequired[int]
    """
    Total monetary value of the payment including all taxes and fees.
    """

    capture_method: typing_extensions.NotRequired[
        typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]
    ]
    """
    To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
    """

    gratuity_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value paid by the consumer over and above the payment due for service.
    """

    is_capture: typing_extensions.NotRequired[bool]
    """
    (Deprecated) For auth only, send isCapture=false. For sale or update an authorized payment to capture, send isCapture=true.
    """

    is_taxable: typing_extensions.NotRequired[bool]
    """
    Indicates whether tax has been added to the payment.
    """

    is_void: typing_extensions.NotRequired[bool]
    """
    Void a payment
    """

    reversal_reason: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "CARD_DECLINED",
            "LATE_RESPONSE",
            "MAC_NOT_VERIFIED",
            "MAC_SYNC_ERROR",
            "NO_RESPONSE",
            "SUSPECTED_FRAUD",
            "SYSTEM_MALFUNCTION",
            "UNABLE_TO_DELIVER",
            "ZEK_SYNC_ERROR",
        ]
    ]
    """
    Codifies the explanation for an authorization of funds for a sales transaction to have an offsetting (reversal) authorization transaction before settlement occurs. The offset will release the hold of funds placed from the original authorization transaction.
    """

    statement_descriptor: typing_extensions.NotRequired[str]
    """
    Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
    """

    sub_merchant_supplemental_data: typing_extensions.NotRequired[
        SubMerchantSupplementalData
    ]
    """
    Additional data provided by merchant for reference purposes.
    """

    surcharge_amount: typing_extensions.NotRequired[int]
    """
    Specifies the monetary value of an additional charge by a United States (US) merchant for the customer's usage of the credit card on a domestic US purchase. Surcharging is prohibited outside the US and in several US states and territories. The no-surcharge list currently includes California, Colorado, Connecticut, Florida, Kansas, Maine, Massachusetts, New York, Oklahoma, Texas and Puerto Rico.
    """

    tax_amount: typing_extensions.NotRequired[int]
    """
    Monetary value of the tax amount assessed to the payment.
    """


class _SerializerPaymentPatch(pydantic.BaseModel):
    """
    Serializer for PaymentPatch handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    amount: typing.Optional[int] = pydantic.Field(alias="amount", default=None)
    capture_method: typing.Optional[
        typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]
    ] = pydantic.Field(alias="captureMethod", default=None)
    gratuity_amount: typing.Optional[int] = pydantic.Field(
        alias="gratuityAmount", default=None
    )
    is_capture: typing.Optional[bool] = pydantic.Field(alias="isCapture", default=None)
    is_taxable: typing.Optional[bool] = pydantic.Field(alias="isTaxable", default=None)
    is_void: typing.Optional[bool] = pydantic.Field(alias="isVoid", default=None)
    reversal_reason: typing.Optional[
        typing_extensions.Literal[
            "CARD_DECLINED",
            "LATE_RESPONSE",
            "MAC_NOT_VERIFIED",
            "MAC_SYNC_ERROR",
            "NO_RESPONSE",
            "SUSPECTED_FRAUD",
            "SYSTEM_MALFUNCTION",
            "UNABLE_TO_DELIVER",
            "ZEK_SYNC_ERROR",
        ]
    ] = pydantic.Field(alias="reversalReason", default=None)
    statement_descriptor: typing.Optional[str] = pydantic.Field(
        alias="statementDescriptor", default=None
    )
    sub_merchant_supplemental_data: typing.Optional[
        _SerializerSubMerchantSupplementalData
    ] = pydantic.Field(alias="subMerchantSupplementalData", default=None)
    surcharge_amount: typing.Optional[int] = pydantic.Field(
        alias="surchargeAmount", default=None
    )
    tax_amount: typing.Optional[int] = pydantic.Field(alias="taxAmount", default=None)
