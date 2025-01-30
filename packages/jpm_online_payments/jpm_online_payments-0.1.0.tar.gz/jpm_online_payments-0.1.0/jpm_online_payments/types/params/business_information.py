import typing
import typing_extensions
import pydantic


class BusinessInformation(typing_extensions.TypedDict):
    """
    Partner's Customer Business information
    """

    client_business_description_text: typing_extensions.NotRequired[str]
    """
    Provides textual information for a company, which may include information about its history, its products and services, and its influence on a particular industry.
    """

    organization_dba_name: typing_extensions.NotRequired[str]
    """
    The label given to an alias name for an Organization labeled as D.B.A. that is different from the legal name.
    """

    organization_legal_name: typing_extensions.NotRequired[str]
    """
    Labels an entity as identified in its formation documents and, where applicable, as registered with a state, local, or federal government, or other chartering, or licensing authority.
    """


class _SerializerBusinessInformation(pydantic.BaseModel):
    """
    Serializer for BusinessInformation handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    client_business_description_text: typing.Optional[str] = pydantic.Field(
        alias="clientBusinessDescriptionText", default=None
    )
    organization_dba_name: typing.Optional[str] = pydantic.Field(
        alias="organizationDBAName", default=None
    )
    organization_legal_name: typing.Optional[str] = pydantic.Field(
        alias="organizationLegalName", default=None
    )
