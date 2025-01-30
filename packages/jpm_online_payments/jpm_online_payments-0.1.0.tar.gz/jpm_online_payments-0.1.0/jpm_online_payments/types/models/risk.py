import typing
import pydantic


class Risk(pydantic.BaseModel):
    """
    Response information for transactions
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    request_fraud_score: typing.Optional[bool] = pydantic.Field(
        alias="requestFraudScore", default=None
    )
    """
    Indicates the true/false value of whether or not the transaction need to be assessed for fraud check.
    """
    risk_reason_code: typing.Optional[str] = pydantic.Field(
        alias="riskReasonCode", default=None
    )
    """
    Codifies adverse action reason associated with the Risk Index Score for the transaction. This reason can be given with a adverse decision made using the Risk Index Score.
    """
    token_risk_score: typing.Optional[int] = pydantic.Field(
        alias="tokenRiskScore", default=None
    )
    """
    Risk score for token
    """
    transaction_risk_score: typing.Optional[int] = pydantic.Field(
        alias="transactionRiskScore", default=None
    )
    """
    Risk score for transaction
    """
