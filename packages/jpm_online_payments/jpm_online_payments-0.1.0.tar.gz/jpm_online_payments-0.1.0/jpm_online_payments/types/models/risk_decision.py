import typing
import pydantic


class RiskDecision(pydantic.BaseModel):
    """
    Object containing Risk Decision information.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    digital_alert_rule_name: typing.Optional[str] = pydantic.Field(
        alias="digitalAlertRuleName", default=None
    )
    """
    The moniker given to the alert rule used to identify potential fraud online. (e.g. 200Billpay, 300ACH, QPRT Quickpay V005)
    """
    fraud_risk_response: typing.Optional[str] = pydantic.Field(
        alias="fraudRiskResponse", default=None
    )
    """
    Codifies the success or failure of a request to the fraud engine to assign a risk score to a payment transaction. This request is done prior to the authorization.
    """
    fraud_risk_score: typing.Optional[str] = pydantic.Field(
        alias="fraudRiskScore", default=None
    )
    """
    industryType
    """
    fraud_rule_action: typing.Optional[str] = pydantic.Field(
        alias="fraudRuleAction", default=None
    )
    """
    Codifies the next step of the fraud analysis based on the risk rule result as defined by the merchant.
    """
    fraud_status: typing.Optional[str] = pydantic.Field(
        alias="fraudStatus", default=None
    )
    """
    Codifies the status of card at time of suspected fraud. Note: Used in conjunction with the Fraud Method Code field. Contains the first character the 2-character alphanumeric Fraud Type entered in the Code1 field of the Work Suspect Fraud screen. Code used to further define an account status. Specifically, the fraud type codes defined by credit card associations. Commonly known as Fraud Type 1 Code.
    """
    fraud_status_description: typing.Optional[str] = pydantic.Field(
        alias="fraudStatusDescription", default=None
    )
    """
    The label for the status of card at time of suspected fraud. Note: Used in conjunction with the Fraud Method Code field. Contains the first character the 2-character alphanumeric Fraud Type entered in the Code1 field of the Work Suspect Fraud screen. Code used to further define an account status. Specifically, the fraud type codes defined by credit card associations. Commonly known as Fraud Type 1 Code.
    """
