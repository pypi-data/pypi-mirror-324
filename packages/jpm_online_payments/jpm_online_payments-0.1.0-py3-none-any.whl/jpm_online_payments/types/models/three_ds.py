import typing
import pydantic

from .version1 import Version1
from .version2 import Version2


class ThreeDs(pydantic.BaseModel):
    """
    Contains information about payer authentication using 3-D Secure authentication
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authentication_transaction_id: typing.Optional[str] = pydantic.Field(
        alias="authenticationTransactionId", default=None
    )
    """
    Identifier provided by the merchant plug in system (MPI) or scheme directory server during payer authentication using 3-D Secure authentication.
    """
    authentication_value: typing.Optional[str] = pydantic.Field(
        alias="authenticationValue", default=None
    )
    """
    3DS Base 64 cryptogram obtained prior to payment request.
    """
    three_ds_program_protocol: typing.Optional[str] = pydantic.Field(
        alias="threeDSProgramProtocol", default=None
    )
    """
    Indicates 3-D Secure program protocol used in the transaction.
    """
    version1: typing.Optional[Version1] = pydantic.Field(alias="version1", default=None)
    """
    Contains information about payer authentication using 3-D Secure authentication version 1
    """
    version2: typing.Optional[Version2] = pydantic.Field(alias="version2", default=None)
    """
    Contains information about payer authentication using 3-D Secure authentication version 2
    """
