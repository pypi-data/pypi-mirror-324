import typing
import typing_extensions

from jpm_online_payments.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_param,
    to_encodable,
    type_utils,
)
from jpm_online_payments.types import models, params


class CapturesClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def create(
        self,
        *,
        id: str,
        merchant_id: str,
        request_id: str,
        account_holder: typing.Union[
            typing.Optional[params.AccountHolder], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        account_on_file: typing.Union[
            typing.Optional[
                typing_extensions.Literal["NOT_STORED", "STORED", "TO_BE_STORED"]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        capture_method: typing.Union[
            typing.Optional[typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        currency: typing.Union[
            typing.Optional[
                typing_extensions.Literal[
                    "AED",
                    "AFN",
                    "ALL",
                    "AMD",
                    "ANG",
                    "AOA",
                    "ARS",
                    "AUD",
                    "AWG",
                    "AZN",
                    "BAM",
                    "BBD",
                    "BDT",
                    "BGN",
                    "BIF",
                    "BMD",
                    "BND",
                    "BOB",
                    "BRL",
                    "BSD",
                    "BTN",
                    "BWP",
                    "BYN",
                    "BZD",
                    "CAD",
                    "CDF",
                    "CHF",
                    "CLP",
                    "CNY",
                    "COP",
                    "CRC",
                    "CVE",
                    "CZK",
                    "DJF",
                    "DKK",
                    "DOP",
                    "DZD",
                    "EGP",
                    "ETB",
                    "EUR",
                    "FJD",
                    "FKP",
                    "GBP",
                    "GEL",
                    "GHS",
                    "GIP",
                    "GMD",
                    "GTQ",
                    "GYD",
                    "HKD",
                    "HNL",
                    "HRK",
                    "HTG",
                    "HUF",
                    "IDR",
                    "ILS",
                    "INR",
                    "ISK",
                    "JMD",
                    "JPY",
                    "KES",
                    "KHR",
                    "KMF",
                    "KRW",
                    "KYD",
                    "KZT",
                    "LAK",
                    "LBP",
                    "LKR",
                    "LRD",
                    "LSL",
                    "MAD",
                    "MDL",
                    "MGA",
                    "MKD",
                    "MMK",
                    "MNT",
                    "MOP",
                    "MRU",
                    "MUR",
                    "MVR",
                    "MWK",
                    "MXN",
                    "MYR",
                    "MZN",
                    "NAD",
                    "NGN",
                    "NIO",
                    "NOK",
                    "NPR",
                    "NZD",
                    "PAB",
                    "PEN",
                    "PGK",
                    "PHP",
                    "PKR",
                    "PLN",
                    "PYG",
                    "QAR",
                    "RON",
                    "RSD",
                    "RWF",
                    "SAR",
                    "SBD",
                    "SCR",
                    "SEK",
                    "SGD",
                    "SHP",
                    "SLL",
                    "SOS",
                    "SRD",
                    "STN",
                    "SZL",
                    "THB",
                    "TJS",
                    "TOP",
                    "TRY",
                    "TTD",
                    "TWD",
                    "TZS",
                    "UAH",
                    "UGX",
                    "USD",
                    "UYU",
                    "UZS",
                    "VND",
                    "VUV",
                    "WST",
                    "XAF",
                    "XCD",
                    "XOF",
                    "XPF",
                    "YER",
                    "ZAR",
                    "ZMW",
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        initiator_type: typing.Union[
            typing.Optional[typing_extensions.Literal["CARDHOLDER", "MERCHANT"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        installment: typing.Union[
            typing.Optional[params.Installment], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_amount_final: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant: typing.Union[
            typing.Optional[params.Merchant], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_order_number: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        multi_capture: typing.Union[
            typing.Optional[params.MultiCapture], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        original_transaction_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        partial_authorization_support: typing.Union[
            typing.Optional[typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        payment_method_type: typing.Union[
            typing.Optional[params.MultiCapturePaymentMethodType], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        payment_request_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        recurring: typing.Union[
            typing.Optional[params.Recurring], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        retail_addenda: typing.Union[
            typing.Optional[params.RetailAddenda], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        risk: typing.Union[
            typing.Optional[params.Risk], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        ship_to: typing.Union[
            typing.Optional[params.ShipTo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        statement_descriptor: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        sub_merchant_supplemental_data: typing.Union[
            typing.Optional[params.SubMerchantSupplementalData], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Capture a payment

        Capture a payment request for existing authorized transaction

        POST /payments/{id}/captures

        Args:
            accountHolder: Card owner properties
            accountOnFile: Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
            amount: Total monetary value of the payment including all taxes and fees.
            captureMethod: To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
            currency: Describes the currency type of the transaction
            initiatorType: Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
            installment: Object containing information in the file
            isAmountFinal: Indicates if the amount is final and will not change
            merchant: Information about the merchant
            merchantOrderNumber: A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
            multiCapture: Split Shipment Information
            originalTransactionId: Identifies a unique occurrence of a transaction.
            partialAuthorizationSupport: Indicates ability to support a partial approval amount on payments including prompting consumer for another method of payment for the balance.
            paymentMethodType: Multi Capture Payment Method Type contains all the payment method code supported for multi capture payment processing capability
            paymentRequestId: Identifies a unique occurrence of an payment processing request from merchant that is associated with a purchase of goods and/or services. A payment request consist of authorization, captures and refunds.
            recurring: Recurring Payment Object
            retailAddenda: Industry-specific attributes.
            risk: Response information for transactions
            shipTo: Object containing information about the recipients
            statementDescriptor: Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            id: Identifies a unique occurrence of a transaction.
            merchant-id: Identifier for the merchant account
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.payments.captures.create(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6",
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        _header["request-id"] = str(encode_param(request_id, False))
        _json = to_encodable(
            item={
                "account_holder": account_holder,
                "account_on_file": account_on_file,
                "amount": amount,
                "capture_method": capture_method,
                "currency": currency,
                "initiator_type": initiator_type,
                "installment": installment,
                "is_amount_final": is_amount_final,
                "merchant": merchant,
                "merchant_order_number": merchant_order_number,
                "multi_capture": multi_capture,
                "original_transaction_id": original_transaction_id,
                "partial_authorization_support": partial_authorization_support,
                "payment_method_type": payment_method_type,
                "payment_request_id": payment_request_id,
                "recurring": recurring,
                "retail_addenda": retail_addenda,
                "risk": risk,
                "ship_to": ship_to,
                "statement_descriptor": statement_descriptor,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
            },
            dump_with=params._SerializerCaptureRequest,
        )
        return self._base_client.request(
            method="POST",
            path=f"/payments/{id}/captures",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncCapturesClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def create(
        self,
        *,
        id: str,
        merchant_id: str,
        request_id: str,
        account_holder: typing.Union[
            typing.Optional[params.AccountHolder], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        account_on_file: typing.Union[
            typing.Optional[
                typing_extensions.Literal["NOT_STORED", "STORED", "TO_BE_STORED"]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        capture_method: typing.Union[
            typing.Optional[typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        currency: typing.Union[
            typing.Optional[
                typing_extensions.Literal[
                    "AED",
                    "AFN",
                    "ALL",
                    "AMD",
                    "ANG",
                    "AOA",
                    "ARS",
                    "AUD",
                    "AWG",
                    "AZN",
                    "BAM",
                    "BBD",
                    "BDT",
                    "BGN",
                    "BIF",
                    "BMD",
                    "BND",
                    "BOB",
                    "BRL",
                    "BSD",
                    "BTN",
                    "BWP",
                    "BYN",
                    "BZD",
                    "CAD",
                    "CDF",
                    "CHF",
                    "CLP",
                    "CNY",
                    "COP",
                    "CRC",
                    "CVE",
                    "CZK",
                    "DJF",
                    "DKK",
                    "DOP",
                    "DZD",
                    "EGP",
                    "ETB",
                    "EUR",
                    "FJD",
                    "FKP",
                    "GBP",
                    "GEL",
                    "GHS",
                    "GIP",
                    "GMD",
                    "GTQ",
                    "GYD",
                    "HKD",
                    "HNL",
                    "HRK",
                    "HTG",
                    "HUF",
                    "IDR",
                    "ILS",
                    "INR",
                    "ISK",
                    "JMD",
                    "JPY",
                    "KES",
                    "KHR",
                    "KMF",
                    "KRW",
                    "KYD",
                    "KZT",
                    "LAK",
                    "LBP",
                    "LKR",
                    "LRD",
                    "LSL",
                    "MAD",
                    "MDL",
                    "MGA",
                    "MKD",
                    "MMK",
                    "MNT",
                    "MOP",
                    "MRU",
                    "MUR",
                    "MVR",
                    "MWK",
                    "MXN",
                    "MYR",
                    "MZN",
                    "NAD",
                    "NGN",
                    "NIO",
                    "NOK",
                    "NPR",
                    "NZD",
                    "PAB",
                    "PEN",
                    "PGK",
                    "PHP",
                    "PKR",
                    "PLN",
                    "PYG",
                    "QAR",
                    "RON",
                    "RSD",
                    "RWF",
                    "SAR",
                    "SBD",
                    "SCR",
                    "SEK",
                    "SGD",
                    "SHP",
                    "SLL",
                    "SOS",
                    "SRD",
                    "STN",
                    "SZL",
                    "THB",
                    "TJS",
                    "TOP",
                    "TRY",
                    "TTD",
                    "TWD",
                    "TZS",
                    "UAH",
                    "UGX",
                    "USD",
                    "UYU",
                    "UZS",
                    "VND",
                    "VUV",
                    "WST",
                    "XAF",
                    "XCD",
                    "XOF",
                    "XPF",
                    "YER",
                    "ZAR",
                    "ZMW",
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        initiator_type: typing.Union[
            typing.Optional[typing_extensions.Literal["CARDHOLDER", "MERCHANT"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        installment: typing.Union[
            typing.Optional[params.Installment], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_amount_final: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant: typing.Union[
            typing.Optional[params.Merchant], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_order_number: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        multi_capture: typing.Union[
            typing.Optional[params.MultiCapture], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        original_transaction_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        partial_authorization_support: typing.Union[
            typing.Optional[typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        payment_method_type: typing.Union[
            typing.Optional[params.MultiCapturePaymentMethodType], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        payment_request_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        recurring: typing.Union[
            typing.Optional[params.Recurring], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        retail_addenda: typing.Union[
            typing.Optional[params.RetailAddenda], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        risk: typing.Union[
            typing.Optional[params.Risk], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        ship_to: typing.Union[
            typing.Optional[params.ShipTo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        statement_descriptor: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        sub_merchant_supplemental_data: typing.Union[
            typing.Optional[params.SubMerchantSupplementalData], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Capture a payment

        Capture a payment request for existing authorized transaction

        POST /payments/{id}/captures

        Args:
            accountHolder: Card owner properties
            accountOnFile: Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
            amount: Total monetary value of the payment including all taxes and fees.
            captureMethod: To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
            currency: Describes the currency type of the transaction
            initiatorType: Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
            installment: Object containing information in the file
            isAmountFinal: Indicates if the amount is final and will not change
            merchant: Information about the merchant
            merchantOrderNumber: A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
            multiCapture: Split Shipment Information
            originalTransactionId: Identifies a unique occurrence of a transaction.
            partialAuthorizationSupport: Indicates ability to support a partial approval amount on payments including prompting consumer for another method of payment for the balance.
            paymentMethodType: Multi Capture Payment Method Type contains all the payment method code supported for multi capture payment processing capability
            paymentRequestId: Identifies a unique occurrence of an payment processing request from merchant that is associated with a purchase of goods and/or services. A payment request consist of authorization, captures and refunds.
            recurring: Recurring Payment Object
            retailAddenda: Industry-specific attributes.
            risk: Response information for transactions
            shipTo: Object containing information about the recipients
            statementDescriptor: Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            id: Identifies a unique occurrence of a transaction.
            merchant-id: Identifier for the merchant account
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.payments.captures.create(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6",
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        _header["request-id"] = str(encode_param(request_id, False))
        _json = to_encodable(
            item={
                "account_holder": account_holder,
                "account_on_file": account_on_file,
                "amount": amount,
                "capture_method": capture_method,
                "currency": currency,
                "initiator_type": initiator_type,
                "installment": installment,
                "is_amount_final": is_amount_final,
                "merchant": merchant,
                "merchant_order_number": merchant_order_number,
                "multi_capture": multi_capture,
                "original_transaction_id": original_transaction_id,
                "partial_authorization_support": partial_authorization_support,
                "payment_method_type": payment_method_type,
                "payment_request_id": payment_request_id,
                "recurring": recurring,
                "retail_addenda": retail_addenda,
                "risk": risk,
                "ship_to": ship_to,
                "statement_descriptor": statement_descriptor,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
            },
            dump_with=params._SerializerCaptureRequest,
        )
        return await self._base_client.request(
            method="POST",
            path=f"/payments/{id}/captures",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )
