import typing
import pydantic


class CustomData(pydantic.BaseModel):
    """
    Customized data provided by merchant for reference purposes.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    external_batch_id: typing.Optional[str] = pydantic.Field(
        alias="externalBatchId", default=None
    )
    """
    A merchant specified batch identifier that a merchant has for a collection of payment/refund transactions.
    """
    external_merchant_id: typing.Optional[str] = pydantic.Field(
        alias="externalMerchantId", default=None
    )
    """
    Identifies a merchant account maintained by an external party and is used as a reference identifier during transaction processing by the Firm.
    """
    external_transaction_reference_number: typing.Optional[str] = pydantic.Field(
        alias="externalTransactionReferenceNumber", default=None
    )
    """
    Identifies a transaction as assigned by a third-party such as the payment gateway, partner bank, facilitator, aggregator, etc.
    """
    external_transaction_type: typing.Optional[str] = pydantic.Field(
        alias="externalTransactionType", default=None
    )
    """
    Codifies a grouping of payment transactions with similar processing characteristics such as retails transactions, mail order transactions, etc.
    """
    merchant_expected_deposit_date: typing.Optional[str] = pydantic.Field(
        alias="merchantExpectedDepositDate", default=None
    )
    """
    A merchant specified date of when transaction is expected to be deposited and available for withdrawal.
    """
    merchant_order_reference_id: typing.Optional[str] = pydantic.Field(
        alias="merchantOrderReferenceId", default=None
    )
    """
    Identifies a unique reference provided and used by the merchant to track orders within their own internal system or in a third party application (such as FeDex or UPS).
    """
