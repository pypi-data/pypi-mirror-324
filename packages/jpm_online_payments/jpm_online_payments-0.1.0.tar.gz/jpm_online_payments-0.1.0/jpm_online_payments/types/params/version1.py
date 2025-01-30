import typing
import typing_extensions
import pydantic


class Version1(typing_extensions.TypedDict):
    """
    Contains information about payer authentication using 3-D Secure authentication version 1
    """

    three_dspa_res_status: typing_extensions.NotRequired[
        typing_extensions.Literal["A", "N", "U", "Y"]
    ]
    """
    Contains value returned in the transaction status field of the Payer Authentication Response (PARes) message from the card Issuer's Access Control Server (ACS). Y=Authentication successful ; N=Authentication failed ; U=Authentication unavailable ; A=Attempted authentication
    """

    three_dsve_res_enrolled: typing_extensions.NotRequired[
        typing_extensions.Literal["A", "N", "U", "Y"]
    ]
    """
    Contains value returned in the 'enrolled' field of the Verify Enrollment Response (VERes) message from the card scheme's Directory Server. Y=Authentication successful;  N=Authentication failed; U=Authentication unavailable;  A=Attempted authentication
    """


class _SerializerVersion1(pydantic.BaseModel):
    """
    Serializer for Version1 handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    three_dspa_res_status: typing.Optional[
        typing_extensions.Literal["A", "N", "U", "Y"]
    ] = pydantic.Field(alias="threeDSPAResStatus", default=None)
    three_dsve_res_enrolled: typing.Optional[
        typing_extensions.Literal["A", "N", "U", "Y"]
    ] = pydantic.Field(alias="threeDSVEResEnrolled", default=None)
