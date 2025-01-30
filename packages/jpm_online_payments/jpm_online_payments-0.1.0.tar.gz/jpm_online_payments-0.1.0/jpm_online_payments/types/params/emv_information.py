import typing
import typing_extensions
import pydantic


class EmvInformation(typing_extensions.TypedDict):
    """
    Europay Mastercard Visa (EMV) chip transactions information
    """

    application_id: typing_extensions.NotRequired[str]
    """
    A unique identifier stored on the chip card used to identify the cryptographic application used by the terminal and the card to process the transaction. This application identifier (AID) is printed on all chip card (Euro MasterCard Visa (EMV)) cardholder receipts.
    """

    emv_data: typing_extensions.NotRequired[str]
    """
    The encrypted cardholder information stored on a metallic chip
    """

    emv_sequence_number: typing_extensions.NotRequired[str]
    """
    Contains a unique sequence counter for this transaction from this point of sale. This field comes from EMV Tag 9F41
    """

    host_returned_data: typing_extensions.NotRequired[str]
    """
    EMV tags returned to the terminal from the host.
    """

    pan_sequence_number: typing_extensions.NotRequired[str]
    """
    Identifies unique number for primary account number sent from the chip card.
    """


class _SerializerEmvInformation(pydantic.BaseModel):
    """
    Serializer for EmvInformation handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    application_id: typing.Optional[str] = pydantic.Field(
        alias="applicationId", default=None
    )
    emv_data: typing.Optional[str] = pydantic.Field(alias="emvData", default=None)
    emv_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="emvSequenceNumber", default=None
    )
    host_returned_data: typing.Optional[str] = pydantic.Field(
        alias="hostReturnedData", default=None
    )
    pan_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="panSequenceNumber", default=None
    )
