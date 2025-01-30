import typing
import typing_extensions
import pydantic


class Boleto(pydantic.BaseModel):
    """
    Boleto payment information
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    bank_code: typing_extensions.Literal["JPM"] = pydantic.Field(
        alias="bankCode",
    )
    """
    Indicates the bank issuing the Boleto
    """
    barcode_url: typing.Optional[str] = pydantic.Field(alias="barcodeUrl", default=None)
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.  In this context, this is the URL provided by merchant for the barcode. Customer can complete the transaction by paying the transaction amount using barcode from the link.
    """
    document_number: str = pydantic.Field(
        alias="documentNumber",
    )
    """
    Ticket identifier
    """
    due_date: str = pydantic.Field(
        alias="dueDate",
    )
    """
    Date payment is due by
    """
    expiry_date: typing.Optional[str] = pydantic.Field(alias="expiryDate", default=None)
    """
    Designates the year, month, and day in which the Convenience Store Payment document will no longer be recognized as a valid payment document to be utilized at the convenience store.
    """
    paid_amount: str = pydantic.Field(
        alias="paidAmount",
    )
    """
    Actual amount paid.
    """
    paid_date: str = pydantic.Field(
        alias="paidDate",
    )
    """
    Date and time in which the voucher or ticket was paid.
    """
    pdf_url: typing.Optional[str] = pydantic.Field(alias="pdfUrl", default=None)
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.  In this context, this is the URL provided by merchant for the payment document in PDF format. The document contain payment instruction to pay at store to complete the transaction.
    """
    qr_code_url: typing.Optional[str] = pydantic.Field(alias="qrCodeUrl", default=None)
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with either 'http' or 'https'
    """
    redirect_url: typing.Optional[str] = pydantic.Field(
        alias="redirectUrl", default=None
    )
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with 'https'
    """
    status: typing.Optional[
        typing_extensions.Literal[
            "COMPLETED",
            "ERROR",
            "EXPIRED",
            "INITIATED",
            "OVERPAID",
            "PAID",
            "REDIRECTED",
            "RETURNED",
            "UNDERPAID",
            "VOIDED",
        ]
    ] = pydantic.Field(alias="status", default=None)
    """
    Indicates the payment status from the processor. Examples include COMPLETED ,PAID, OVERPAID,ERRORED. Brazil only.
    """
    ticket_instructions: str = pydantic.Field(
        alias="ticketInstructions",
    )
    """
    Ticket instructions
    """
    type_field: typing_extensions.Literal["BDP", "DM"] = pydantic.Field(
        alias="type",
    )
    """
    Boleto type of Duplicata Mercantil or Boleto de Proposta
    """
    unique_number: str = pydantic.Field(
        alias="uniqueNumber",
    )
    """
    Number that uniquely identifies a Boleto for an account
    """
