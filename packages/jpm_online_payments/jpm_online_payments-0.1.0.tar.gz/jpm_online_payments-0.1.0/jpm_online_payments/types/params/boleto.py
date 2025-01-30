import typing
import typing_extensions
import pydantic


class Boleto(typing_extensions.TypedDict):
    """
    Boleto payment information
    """

    bank_code: typing_extensions.Required[typing_extensions.Literal["JPM"]]
    """
    Indicates the bank issuing the Boleto
    """

    barcode_url: typing_extensions.NotRequired[str]
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.  In this context, this is the URL provided by merchant for the barcode. Customer can complete the transaction by paying the transaction amount using barcode from the link.
    """

    document_number: typing_extensions.Required[str]
    """
    Ticket identifier
    """

    due_date: typing_extensions.Required[str]
    """
    Date payment is due by
    """

    expiry_date: typing_extensions.NotRequired[str]
    """
    Designates the year, month, and day in which the Convenience Store Payment document will no longer be recognized as a valid payment document to be utilized at the convenience store.
    """

    paid_amount: typing_extensions.Required[str]
    """
    Actual amount paid.
    """

    paid_date: typing_extensions.Required[str]
    """
    Date and time in which the voucher or ticket was paid.
    """

    pdf_url: typing_extensions.NotRequired[str]
    """
    A reference to a web resource on the internet specifying its location on a computer network and a mechanism for retrieving.  In this context, this is the URL provided by merchant for the payment document in PDF format. The document contain payment instruction to pay at store to complete the transaction.
    """

    qr_code_url: typing_extensions.NotRequired[str]
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with either 'http' or 'https'
    """

    redirect_url: typing_extensions.NotRequired[str]
    """
    Information on where consumer needs to be redirected for payment process completion. Ensure that the URL begins with 'https'
    """

    status: typing_extensions.NotRequired[
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
    ]
    """
    Indicates the payment status from the processor. Examples include COMPLETED ,PAID, OVERPAID,ERRORED. Brazil only.
    """

    ticket_instructions: typing_extensions.Required[str]
    """
    Ticket instructions
    """

    type_field: typing_extensions.Required[typing_extensions.Literal["BDP", "DM"]]
    """
    Boleto type of Duplicata Mercantil or Boleto de Proposta
    """

    unique_number: typing_extensions.Required[str]
    """
    Number that uniquely identifies a Boleto for an account
    """


class _SerializerBoleto(pydantic.BaseModel):
    """
    Serializer for Boleto handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    bank_code: typing_extensions.Literal["JPM"] = pydantic.Field(
        alias="bankCode",
    )
    barcode_url: typing.Optional[str] = pydantic.Field(alias="barcodeUrl", default=None)
    document_number: str = pydantic.Field(
        alias="documentNumber",
    )
    due_date: str = pydantic.Field(
        alias="dueDate",
    )
    expiry_date: typing.Optional[str] = pydantic.Field(alias="expiryDate", default=None)
    paid_amount: str = pydantic.Field(
        alias="paidAmount",
    )
    paid_date: str = pydantic.Field(
        alias="paidDate",
    )
    pdf_url: typing.Optional[str] = pydantic.Field(alias="pdfUrl", default=None)
    qr_code_url: typing.Optional[str] = pydantic.Field(alias="qrCodeUrl", default=None)
    redirect_url: typing.Optional[str] = pydantic.Field(
        alias="redirectUrl", default=None
    )
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
    ticket_instructions: str = pydantic.Field(
        alias="ticketInstructions",
    )
    type_field: typing_extensions.Literal["BDP", "DM"] = pydantic.Field(
        alias="type",
    )
    unique_number: str = pydantic.Field(
        alias="uniqueNumber",
    )
