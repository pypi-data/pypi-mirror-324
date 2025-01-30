import typing
import pydantic


class BusinessInformation(pydantic.BaseModel):
    """
    Partner's Customer Business information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    client_business_description_text: typing.Optional[str] = pydantic.Field(
        alias="clientBusinessDescriptionText", default=None
    )
    """
    Provides textual information for a company, which may include information about its history, its products and services, and its influence on a particular industry.
    """
    organization_dba_name: typing.Optional[str] = pydantic.Field(
        alias="organizationDBAName", default=None
    )
    """
    The label given to an alias name for an Organization labeled as D.B.A. that is different from the legal name.
    """
    organization_legal_name: typing.Optional[str] = pydantic.Field(
        alias="organizationLegalName", default=None
    )
    """
    Labels an entity as identified in its formation documents and, where applicable, as registered with a state, local, or federal government, or other chartering, or licensing authority.
    """
