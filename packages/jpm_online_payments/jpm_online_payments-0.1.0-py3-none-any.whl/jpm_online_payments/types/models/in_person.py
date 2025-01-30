import typing
import typing_extensions
import pydantic

from .emv_information import EmvInformation
from .pin_processing import PinProcessing
from .storeand_forward import StoreandForward


class InPerson(pydantic.BaseModel):
    """
    Card present information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    batch_julian_day_number: typing.Optional[int] = pydantic.Field(
        alias="batchJulianDayNumber", default=None
    )
    """
    Batch Julian day number returned on responses.
    """
    batch_transaction_classification_code: typing.Optional[
        typing_extensions.Literal["1", "2", "3", "4"]
    ] = pydantic.Field(alias="batchTransactionClassificationCode", default=None)
    """
    Codifies the generalized merchant classification for a transaction. 1=Captured, approved EFT transaction; 2=Captured, authorization only transaction; 3=Declined, error transaction; 4=Batch control transaction
    """
    cardholder_authentication_method: typing.Optional[
        typing_extensions.Literal[
            "ELECTRONIC_SIGNATURE",
            "MANUAL_SIGNATURE",
            "NOT_AUTHENTICATED",
            "OTHER",
            "OTHER_SYSTEMIC",
            "PIN",
            "UNKNOWN",
        ]
    ] = pydantic.Field(alias="cardholderAuthenticationMethod", default=None)
    """
    Codifies how the merchant authenticated the cardholder before or during the point of sale card present transaction.
    """
    emv_information: typing.Optional[EmvInformation] = pydantic.Field(
        alias="emvInformation", default=None
    )
    """
    Europay Mastercard Visa (EMV) chip transactions information
    """
    entry_method: typing.Optional[
        typing_extensions.Literal[
            "BARCODE",
            "CREDENTIAL_ON_FILE",
            "EMV_CONTACT",
            "EMV_CONTACTLESS",
            "EMV_FALLBACK",
            "KEYED",
            "SWIPE",
        ]
    ] = pydantic.Field(alias="entryMethod", default=None)
    """
    Codifies the condition under which the card number and expiration date were captured during the transaction (e.g., 90 = Full track read, 03 = bar code read).
    """
    is_cardholder_present: typing.Optional[bool] = pydantic.Field(
        alias="isCardholderPresent", default=None
    )
    """
    Indicate the cardholder was in person at the point of sale.
    """
    pin_processing: typing.Optional[PinProcessing] = pydantic.Field(
        alias="pinProcessing", default=None
    )
    """
    PIN processing information
    """
    storeand_forward: typing.Optional[StoreandForward] = pydantic.Field(
        alias="storeandForward", default=None
    )
    """
    Store and Forward transaction information.
    """
    terminal_batch_number: typing.Optional[str] = pydantic.Field(
        alias="terminalBatchNumber", default=None
    )
    """
    The number assigned to a batch
    """
    transaction_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="transactionSequenceNumber", default=None
    )
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data. In this context, this is the sequence number of this transaction within the current batch.
    """
