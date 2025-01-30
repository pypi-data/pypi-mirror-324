import typing
import typing_extensions
import pydantic


class Version1(pydantic.BaseModel):
    """
    Contains information about payer authentication using 3-D Secure authentication version 1
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    three_dspa_res_status: typing.Optional[
        typing_extensions.Literal["A", "N", "U", "Y"]
    ] = pydantic.Field(alias="threeDSPAResStatus", default=None)
    """
    Contains value returned in the transaction status field of the Payer Authentication Response (PARes) message from the card Issuer's Access Control Server (ACS). Y=Authentication successful ; N=Authentication failed ; U=Authentication unavailable ; A=Attempted authentication
    """
    three_dsve_res_enrolled: typing.Optional[
        typing_extensions.Literal["A", "N", "U", "Y"]
    ] = pydantic.Field(alias="threeDSVEResEnrolled", default=None)
    """
    Contains value returned in the 'enrolled' field of the Verify Enrollment Response (VERes) message from the card scheme's Directory Server. Y=Authentication successful;  N=Authentication failed; U=Authentication unavailable;  A=Attempted authentication
    """
