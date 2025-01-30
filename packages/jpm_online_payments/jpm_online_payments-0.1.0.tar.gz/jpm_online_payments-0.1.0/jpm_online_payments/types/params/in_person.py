import typing
import typing_extensions
import pydantic

from .emv_information import EmvInformation, _SerializerEmvInformation
from .pin_processing import PinProcessing, _SerializerPinProcessing
from .storeand_forward import StoreandForward, _SerializerStoreandForward


class InPerson(typing_extensions.TypedDict):
    """
    Card present information
    """

    batch_julian_day_number: typing_extensions.NotRequired[int]
    """
    Batch Julian day number returned on responses.
    """

    batch_transaction_classification_code: typing_extensions.NotRequired[
        typing_extensions.Literal["1", "2", "3", "4"]
    ]
    """
    Codifies the generalized merchant classification for a transaction. 1=Captured, approved EFT transaction; 2=Captured, authorization only transaction; 3=Declined, error transaction; 4=Batch control transaction
    """

    cardholder_authentication_method: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "ELECTRONIC_SIGNATURE",
            "MANUAL_SIGNATURE",
            "NOT_AUTHENTICATED",
            "OTHER",
            "OTHER_SYSTEMIC",
            "PIN",
            "UNKNOWN",
        ]
    ]
    """
    Codifies how the merchant authenticated the cardholder before or during the point of sale card present transaction.
    """

    emv_information: typing_extensions.NotRequired[EmvInformation]
    """
    Europay Mastercard Visa (EMV) chip transactions information
    """

    entry_method: typing_extensions.NotRequired[
        typing_extensions.Literal[
            "BARCODE",
            "CREDENTIAL_ON_FILE",
            "EMV_CONTACT",
            "EMV_CONTACTLESS",
            "EMV_FALLBACK",
            "KEYED",
            "SWIPE",
        ]
    ]
    """
    Codifies the condition under which the card number and expiration date were captured during the transaction (e.g., 90 = Full track read, 03 = bar code read).
    """

    is_cardholder_present: typing_extensions.NotRequired[bool]
    """
    Indicate the cardholder was in person at the point of sale.
    """

    pin_processing: typing_extensions.NotRequired[PinProcessing]
    """
    PIN processing information
    """

    storeand_forward: typing_extensions.NotRequired[StoreandForward]
    """
    Store and Forward transaction information.
    """

    terminal_batch_number: typing_extensions.NotRequired[str]
    """
    The number assigned to a batch
    """

    transaction_sequence_number: typing_extensions.NotRequired[str]
    """
    Identifies the number indicating the location of this record in the sorting sequence of the specified data. In this context, this is the sequence number of this transaction within the current batch.
    """


class _SerializerInPerson(pydantic.BaseModel):
    """
    Serializer for InPerson handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    batch_julian_day_number: typing.Optional[int] = pydantic.Field(
        alias="batchJulianDayNumber", default=None
    )
    batch_transaction_classification_code: typing.Optional[
        typing_extensions.Literal["1", "2", "3", "4"]
    ] = pydantic.Field(alias="batchTransactionClassificationCode", default=None)
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
    emv_information: typing.Optional[_SerializerEmvInformation] = pydantic.Field(
        alias="emvInformation", default=None
    )
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
    is_cardholder_present: typing.Optional[bool] = pydantic.Field(
        alias="isCardholderPresent", default=None
    )
    pin_processing: typing.Optional[_SerializerPinProcessing] = pydantic.Field(
        alias="pinProcessing", default=None
    )
    storeand_forward: typing.Optional[_SerializerStoreandForward] = pydantic.Field(
        alias="storeandForward", default=None
    )
    terminal_batch_number: typing.Optional[str] = pydantic.Field(
        alias="terminalBatchNumber", default=None
    )
    transaction_sequence_number: typing.Optional[str] = pydantic.Field(
        alias="transactionSequenceNumber", default=None
    )
