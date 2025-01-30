import typing
import pydantic


class EmvInformation(pydantic.BaseModel):
    """
    Europay Mastercard Visa (EMV) chip transactions information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    application_id: typing.Optional[str] = pydantic.Field(
        alias="applicationId", default=None
    )
    """
    A unique identifier stored on the chip card used to identify the cryptographic application used by the terminal and the card to process the transaction. This application identifier (AID) is printed on all chip card (Euro MasterCard Visa (EMV)) cardholder receipts.
    """
    emv_data: typing.Optional[str] = pydantic.Field(alias="emvData", default=None)
    """
    The encrypted cardholder information stored on a metallic chip
    """
    emv_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="emvSequenceNumber", default=None
    )
    """
    Contains a unique sequence counter for this transaction from this point of sale. This field comes from EMV Tag 9F41
    """
    host_returned_data: typing.Optional[str] = pydantic.Field(
        alias="hostReturnedData", default=None
    )
    """
    EMV tags returned to the terminal from the host.
    """
    pan_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="panSequenceNumber", default=None
    )
    """
    Identifies unique number for primary account number sent from the chip card.
    """
