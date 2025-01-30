import typing
import typing_extensions
import pydantic


class Risk(typing_extensions.TypedDict):
    """
    Response information for transactions
    """

    request_fraud_score: typing_extensions.NotRequired[bool]
    """
    Indicates the true/false value of whether or not the transaction need to be assessed for fraud check.
    """

    risk_reason_code: typing_extensions.NotRequired[str]
    """
    Codifies adverse action reason associated with the Risk Index Score for the transaction. This reason can be given with a adverse decision made using the Risk Index Score.
    """

    token_risk_score: typing_extensions.NotRequired[int]
    """
    Risk score for token
    """

    transaction_risk_score: typing_extensions.NotRequired[int]
    """
    Risk score for transaction
    """


class _SerializerRisk(pydantic.BaseModel):
    """
    Serializer for Risk handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    request_fraud_score: typing.Optional[bool] = pydantic.Field(
        alias="requestFraudScore", default=None
    )
    risk_reason_code: typing.Optional[str] = pydantic.Field(
        alias="riskReasonCode", default=None
    )
    token_risk_score: typing.Optional[int] = pydantic.Field(
        alias="tokenRiskScore", default=None
    )
    transaction_risk_score: typing.Optional[int] = pydantic.Field(
        alias="transactionRiskScore", default=None
    )
