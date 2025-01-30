import typing
import typing_extensions
import pydantic

from .version1 import Version1, _SerializerVersion1
from .version2 import Version2, _SerializerVersion2


class ThreeDs(typing_extensions.TypedDict):
    """
    Contains information about payer authentication using 3-D Secure authentication
    """

    authentication_transaction_id: typing_extensions.NotRequired[str]
    """
    Identifier provided by the merchant plug in system (MPI) or scheme directory server during payer authentication using 3-D Secure authentication.
    """

    authentication_value: typing_extensions.NotRequired[str]
    """
    3DS Base 64 cryptogram obtained prior to payment request.
    """

    three_ds_program_protocol: typing_extensions.NotRequired[str]
    """
    Indicates 3-D Secure program protocol used in the transaction.
    """

    version1: typing_extensions.NotRequired[Version1]
    """
    Contains information about payer authentication using 3-D Secure authentication version 1
    """

    version2: typing_extensions.NotRequired[Version2]
    """
    Contains information about payer authentication using 3-D Secure authentication version 2
    """


class _SerializerThreeDs(pydantic.BaseModel):
    """
    Serializer for ThreeDs handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    authentication_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="authenticationTransactionId", default=None
    )
    authentication_value: typing.Optional[str] = pydantic.Field(
        alias="authenticationValue", default=None
    )
    three_ds_program_protocol: typing.Optional[str] = pydantic.Field(
        alias="threeDSProgramProtocol", default=None
    )
    version1: typing.Optional[_SerializerVersion1] = pydantic.Field(
        alias="version1", default=None
    )
    version2: typing.Optional[_SerializerVersion2] = pydantic.Field(
        alias="version2", default=None
    )
