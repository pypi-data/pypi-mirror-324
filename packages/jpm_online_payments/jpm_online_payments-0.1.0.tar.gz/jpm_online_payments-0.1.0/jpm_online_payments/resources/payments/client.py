import typing
import typing_extensions

from jpm_online_payments.core import (
    AsyncBaseClient,
    QueryParams,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_param,
    to_encodable,
    type_utils,
)
from jpm_online_payments.resources.payments.captures import (
    AsyncCapturesClient,
    CapturesClient,
)
from jpm_online_payments.types import models, params


class PaymentsClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

        self.captures = CapturesClient(base_client=self._base_client)

    def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_identifier: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Get a specific payment transaction by request Id

        Request Original Authorization Transaction details

        GET /payments

        Args:
            merchant-id: Identifier for the merchant account
            request-id: Merchant identifier for the request. The value must be unique.
            requestIdentifier: The request identifier for the previous attempted transaction to query by.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.payments.get(
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
            request_identifier="12cc0270-7bed-11e9-a188-1763956dd7f6",
        )
        ```

        """
        _query: QueryParams = {}
        _query["requestIdentifier"] = encode_param(request_identifier, False)
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        _header["request-id"] = str(encode_param(request_id, False))
        return self._base_client.request(
            method="GET",
            path="/payments",
            auth_names=["auth"],
            query_params=_query,
            headers=_header,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )

    def get_by_id(
        self,
        *,
        id: str,
        merchant_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Get a specific payment transaction by transaction Id

        Get a specific payment transaction by transaction Id

        GET /payments/{id}

        Args:
            id: Identifier for the transaction
            merchant-id: Identifier for the merchant account
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.payments.get_by_id(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        return self._base_client.request(
            method="GET",
            path=f"/payments/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        id: str,
        merchant_id: str,
        request_id: str,
        amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        capture_method: typing.Union[
            typing.Optional[typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        gratuity_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_capture: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_taxable: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_void: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        reversal_reason: typing.Union[
            typing.Optional[
                typing_extensions.Literal[
                    "CARD_DECLINED",
                    "LATE_RESPONSE",
                    "MAC_NOT_VERIFIED",
                    "MAC_SYNC_ERROR",
                    "NO_RESPONSE",
                    "SUSPECTED_FRAUD",
                    "SYSTEM_MALFUNCTION",
                    "UNABLE_TO_DELIVER",
                    "ZEK_SYNC_ERROR",
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        statement_descriptor: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        sub_merchant_supplemental_data: typing.Union[
            typing.Optional[params.SubMerchantSupplementalData], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        surcharge_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        tax_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Update payment transaction by transaction Id

        Update an existing payment 1.Capture a payment for settlement. 2. Void a payment and authorization. The transaction will not settle. 3. Update a payment.

        PATCH /payments/{id}

        Args:
            amount: Total monetary value of the payment including all taxes and fees.
            captureMethod: To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
            gratuityAmount: Specifies the monetary value paid by the consumer over and above the payment due for service.
            isCapture: (Deprecated) For auth only, send isCapture=false. For sale or update an authorized payment to capture, send isCapture=true.
            isTaxable: Indicates whether tax has been added to the payment.
            isVoid: Void a payment
            reversalReason: Codifies the explanation for an authorization of funds for a sales transaction to have an offsetting (reversal) authorization transaction before settlement occurs. The offset will release the hold of funds placed from the original authorization transaction.
            statementDescriptor: Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            surchargeAmount: Specifies the monetary value of an additional charge by a United States (US) merchant for the customer's usage of the credit card on a domestic US purchase. Surcharging is prohibited outside the US and in several US states and territories. The no-surcharge list currently includes California, Colorado, Connecticut, Florida, Kansas, Maine, Massachusetts, New York, Oklahoma, Texas and Puerto Rico.
            taxAmount: Monetary value of the tax amount assessed to the payment.
            id: Identifier for the transaction
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
        client.payments.patch(
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
                "amount": amount,
                "capture_method": capture_method,
                "gratuity_amount": gratuity_amount,
                "is_capture": is_capture,
                "is_taxable": is_taxable,
                "is_void": is_void,
                "reversal_reason": reversal_reason,
                "statement_descriptor": statement_descriptor,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
                "surcharge_amount": surcharge_amount,
                "tax_amount": tax_amount,
            },
            dump_with=params._SerializerPaymentPatch,
        )
        return self._base_client.request(
            method="PATCH",
            path=f"/payments/{id}",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        amount: int,
        currency: typing_extensions.Literal[
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
        ],
        merchant: params.Merchant,
        merchant_id: str,
        payment_method_type: params.PaymentMethodType,
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
        authorization_purpose: typing.Union[
            typing.Optional[
                typing_extensions.Literal[
                    "DELAYED_CHARGE", "NO_SHOW", "REAUTHORIZATION", "RESUBMISSION"
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        browser_info: typing.Union[
            typing.Optional[params.BrowserInfo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        capture_method: typing.Union[
            typing.Optional[typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        cash_back_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        direct_pay: typing.Union[
            typing.Optional[params.DirectPay], type_utils.NotGiven
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
        is_capture: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mandate: typing.Union[
            typing.Optional[params.Mandate], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_defined: typing.Union[
            typing.Optional[params.MerchantDefined], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_order_number: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        original_transaction_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        partial_authorization_support: typing.Union[
            typing.Optional[typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        payment_metadata_list: typing.Union[
            typing.Optional[typing.List[params.PaymentMetadata]], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        point_of_interaction: typing.Union[
            typing.Optional[params.PointOfInteraction], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        recurring: typing.Union[
            typing.Optional[params.Recurring], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        restaurant_addenda: typing.Union[
            typing.Optional[params.RestaurantAddenda], type_utils.NotGiven
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
        transaction_routing_override_list: typing.Union[
            typing.Optional[
                typing.List[
                    typing_extensions.Literal["CIELO", "GETNET", "REDECARD", "STONE"]
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Create a payment

        Create a payment request with a specified payment instrument. Authorization and Sale (Authorization and capture).

        POST /payments

        Args:
            accountHolder: Card owner properties
            accountOnFile: Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
            authorizationPurpose: This field should be populated when there is a specific authorization purpose such as delayed authorizations, reauthorizations, resubmissions and no shows.
            browserInfo: Browser Information of the consumer
            captureMethod: To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
            cashBackAmount: The monetary value of a cash withdrawal using a debit or credit card during checkout at a physical terminal in a merchant location. Cash back is equivalent to withdrawing cash from an Automated Teller Machine (ATM).
            directPay: Direct Pay
            initiatorType: Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
            installment: Object containing information in the file
            isAmountFinal: Indicates if the amount is final and will not change
            isCapture: (Deprecated) For auth only, send isCapture=false. For sale or update an authorized payment to capture, send isCapture=true.
            mandate: Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
            merchantDefined: merchant defined data field that it will pass through to reporting.
            merchantOrderNumber: A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
            originalTransactionId: Identifies a unique occurrence of a transaction.
            partialAuthorizationSupport: Indicates ability to support a partial approval amount on payments including prompting consumer for another method of payment for the balance.
            paymentMetadataList: Payment Metadata List
            pointOfInteraction: In store payment Information
            recurring: Recurring Payment Object
            restaurantAddenda: Restaurant Addenda
            retailAddenda: Industry-specific attributes.
            risk: Response information for transactions
            shipTo: Object containing information about the recipients
            statementDescriptor: Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            transactionRoutingOverrideList: List of transaction routing providers where the transaction be routed preferred by the merchant .
            amount: Total monetary value of the payment including all taxes and fees.
            currency: Describes the currency type of the transaction
            merchant: Information about the merchant
            merchant-id: Identifier for the merchant account
            paymentMethodType: paymentType
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.payments.create(
            amount=1234,
            currency="AED",
            merchant={
                "merchant_software": {
                    "company_name": "Payment Company",
                    "product_name": "Application Name",
                }
            },
            merchant_id="991234567890",
            payment_method_type={},
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
                "authorization_purpose": authorization_purpose,
                "browser_info": browser_info,
                "capture_method": capture_method,
                "cash_back_amount": cash_back_amount,
                "direct_pay": direct_pay,
                "initiator_type": initiator_type,
                "installment": installment,
                "is_amount_final": is_amount_final,
                "is_capture": is_capture,
                "mandate": mandate,
                "merchant_defined": merchant_defined,
                "merchant_order_number": merchant_order_number,
                "original_transaction_id": original_transaction_id,
                "partial_authorization_support": partial_authorization_support,
                "payment_metadata_list": payment_metadata_list,
                "point_of_interaction": point_of_interaction,
                "recurring": recurring,
                "restaurant_addenda": restaurant_addenda,
                "retail_addenda": retail_addenda,
                "risk": risk,
                "ship_to": ship_to,
                "statement_descriptor": statement_descriptor,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
                "transaction_routing_override_list": transaction_routing_override_list,
                "amount": amount,
                "currency": currency,
                "merchant": merchant,
                "payment_method_type": payment_method_type,
            },
            dump_with=params._SerializerPayment,
        )
        return self._base_client.request(
            method="POST",
            path="/payments",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncPaymentsClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

        self.captures = AsyncCapturesClient(base_client=self._base_client)

    async def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_identifier: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Get a specific payment transaction by request Id

        Request Original Authorization Transaction details

        GET /payments

        Args:
            merchant-id: Identifier for the merchant account
            request-id: Merchant identifier for the request. The value must be unique.
            requestIdentifier: The request identifier for the previous attempted transaction to query by.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.payments.get(
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
            request_identifier="12cc0270-7bed-11e9-a188-1763956dd7f6",
        )
        ```

        """
        _query: QueryParams = {}
        _query["requestIdentifier"] = encode_param(request_identifier, False)
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        _header["request-id"] = str(encode_param(request_id, False))
        return await self._base_client.request(
            method="GET",
            path="/payments",
            auth_names=["auth"],
            query_params=_query,
            headers=_header,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )

    async def get_by_id(
        self,
        *,
        id: str,
        merchant_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Get a specific payment transaction by transaction Id

        Get a specific payment transaction by transaction Id

        GET /payments/{id}

        Args:
            id: Identifier for the transaction
            merchant-id: Identifier for the merchant account
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.payments.get_by_id(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        return await self._base_client.request(
            method="GET",
            path=f"/payments/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        id: str,
        merchant_id: str,
        request_id: str,
        amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        capture_method: typing.Union[
            typing.Optional[typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        gratuity_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_capture: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_taxable: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        is_void: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        reversal_reason: typing.Union[
            typing.Optional[
                typing_extensions.Literal[
                    "CARD_DECLINED",
                    "LATE_RESPONSE",
                    "MAC_NOT_VERIFIED",
                    "MAC_SYNC_ERROR",
                    "NO_RESPONSE",
                    "SUSPECTED_FRAUD",
                    "SYSTEM_MALFUNCTION",
                    "UNABLE_TO_DELIVER",
                    "ZEK_SYNC_ERROR",
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        statement_descriptor: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        sub_merchant_supplemental_data: typing.Union[
            typing.Optional[params.SubMerchantSupplementalData], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        surcharge_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        tax_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Update payment transaction by transaction Id

        Update an existing payment 1.Capture a payment for settlement. 2. Void a payment and authorization. The transaction will not settle. 3. Update a payment.

        PATCH /payments/{id}

        Args:
            amount: Total monetary value of the payment including all taxes and fees.
            captureMethod: To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
            gratuityAmount: Specifies the monetary value paid by the consumer over and above the payment due for service.
            isCapture: (Deprecated) For auth only, send isCapture=false. For sale or update an authorized payment to capture, send isCapture=true.
            isTaxable: Indicates whether tax has been added to the payment.
            isVoid: Void a payment
            reversalReason: Codifies the explanation for an authorization of funds for a sales transaction to have an offsetting (reversal) authorization transaction before settlement occurs. The offset will release the hold of funds placed from the original authorization transaction.
            statementDescriptor: Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            surchargeAmount: Specifies the monetary value of an additional charge by a United States (US) merchant for the customer's usage of the credit card on a domestic US purchase. Surcharging is prohibited outside the US and in several US states and territories. The no-surcharge list currently includes California, Colorado, Connecticut, Florida, Kansas, Maine, Massachusetts, New York, Oklahoma, Texas and Puerto Rico.
            taxAmount: Monetary value of the tax amount assessed to the payment.
            id: Identifier for the transaction
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
        await client.payments.patch(
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
                "amount": amount,
                "capture_method": capture_method,
                "gratuity_amount": gratuity_amount,
                "is_capture": is_capture,
                "is_taxable": is_taxable,
                "is_void": is_void,
                "reversal_reason": reversal_reason,
                "statement_descriptor": statement_descriptor,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
                "surcharge_amount": surcharge_amount,
                "tax_amount": tax_amount,
            },
            dump_with=params._SerializerPaymentPatch,
        )
        return await self._base_client.request(
            method="PATCH",
            path=f"/payments/{id}",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        amount: int,
        currency: typing_extensions.Literal[
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
        ],
        merchant: params.Merchant,
        merchant_id: str,
        payment_method_type: params.PaymentMethodType,
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
        authorization_purpose: typing.Union[
            typing.Optional[
                typing_extensions.Literal[
                    "DELAYED_CHARGE", "NO_SHOW", "REAUTHORIZATION", "RESUBMISSION"
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        browser_info: typing.Union[
            typing.Optional[params.BrowserInfo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        capture_method: typing.Union[
            typing.Optional[typing_extensions.Literal["DELAYED", "MANUAL", "NOW"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        cash_back_amount: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        direct_pay: typing.Union[
            typing.Optional[params.DirectPay], type_utils.NotGiven
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
        is_capture: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mandate: typing.Union[
            typing.Optional[params.Mandate], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_defined: typing.Union[
            typing.Optional[params.MerchantDefined], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_order_number: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        original_transaction_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        partial_authorization_support: typing.Union[
            typing.Optional[typing_extensions.Literal["NOT_SUPPORTED", "SUPPORTED"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        payment_metadata_list: typing.Union[
            typing.Optional[typing.List[params.PaymentMetadata]], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        point_of_interaction: typing.Union[
            typing.Optional[params.PointOfInteraction], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        recurring: typing.Union[
            typing.Optional[params.Recurring], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        restaurant_addenda: typing.Union[
            typing.Optional[params.RestaurantAddenda], type_utils.NotGiven
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
        transaction_routing_override_list: typing.Union[
            typing.Optional[
                typing.List[
                    typing_extensions.Literal["CIELO", "GETNET", "REDECARD", "STONE"]
                ]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Create a payment

        Create a payment request with a specified payment instrument. Authorization and Sale (Authorization and capture).

        POST /payments

        Args:
            accountHolder: Card owner properties
            accountOnFile: Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
            authorizationPurpose: This field should be populated when there is a specific authorization purpose such as delayed authorizations, reauthorizations, resubmissions and no shows.
            browserInfo: Browser Information of the consumer
            captureMethod: To capture via separate API call, send captureMethod= ?Manual.? For immediate capture, send captureMethod= ?Now.? For automated delayed capture based on merchant profile setting (default is 120 minutes), send captureMethod= ?Delayed.?
            cashBackAmount: The monetary value of a cash withdrawal using a debit or credit card during checkout at a physical terminal in a merchant location. Cash back is equivalent to withdrawing cash from an Automated Teller Machine (ATM).
            directPay: Direct Pay
            initiatorType: Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
            installment: Object containing information in the file
            isAmountFinal: Indicates if the amount is final and will not change
            isCapture: (Deprecated) For auth only, send isCapture=false. For sale or update an authorized payment to capture, send isCapture=true.
            mandate: Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
            merchantDefined: merchant defined data field that it will pass through to reporting.
            merchantOrderNumber: A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
            originalTransactionId: Identifies a unique occurrence of a transaction.
            partialAuthorizationSupport: Indicates ability to support a partial approval amount on payments including prompting consumer for another method of payment for the balance.
            paymentMetadataList: Payment Metadata List
            pointOfInteraction: In store payment Information
            recurring: Recurring Payment Object
            restaurantAddenda: Restaurant Addenda
            retailAddenda: Industry-specific attributes.
            risk: Response information for transactions
            shipTo: Object containing information about the recipients
            statementDescriptor: Merchant name to appear on account holder statement. If not provided, defaults to merchant profile descriptor value.  To send both company identifier and transaction-specific information, use one of these formats: Option 1 ? 3-byte company identifier * 18-byte descriptor (example: XYZ*PAYMENT1OF3) Option 2 ? 7-byte company identifier * 14-byte descriptor (example: XYZCOMP*PAYMENT1OF3) Option 3 ? 12-byte company identifier * 9-byte descriptor (example: XYZCOMPANY1*PAYMT1OF3)
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            transactionRoutingOverrideList: List of transaction routing providers where the transaction be routed preferred by the merchant .
            amount: Total monetary value of the payment including all taxes and fees.
            currency: Describes the currency type of the transaction
            merchant: Information about the merchant
            merchant-id: Identifier for the merchant account
            paymentMethodType: paymentType
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.payments.create(
            amount=1234,
            currency="AED",
            merchant={
                "merchant_software": {
                    "company_name": "Payment Company",
                    "product_name": "Application Name",
                }
            },
            merchant_id="991234567890",
            payment_method_type={},
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
                "authorization_purpose": authorization_purpose,
                "browser_info": browser_info,
                "capture_method": capture_method,
                "cash_back_amount": cash_back_amount,
                "direct_pay": direct_pay,
                "initiator_type": initiator_type,
                "installment": installment,
                "is_amount_final": is_amount_final,
                "is_capture": is_capture,
                "mandate": mandate,
                "merchant_defined": merchant_defined,
                "merchant_order_number": merchant_order_number,
                "original_transaction_id": original_transaction_id,
                "partial_authorization_support": partial_authorization_support,
                "payment_metadata_list": payment_metadata_list,
                "point_of_interaction": point_of_interaction,
                "recurring": recurring,
                "restaurant_addenda": restaurant_addenda,
                "retail_addenda": retail_addenda,
                "risk": risk,
                "ship_to": ship_to,
                "statement_descriptor": statement_descriptor,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
                "transaction_routing_override_list": transaction_routing_override_list,
                "amount": amount,
                "currency": currency,
                "merchant": merchant,
                "payment_method_type": payment_method_type,
            },
            dump_with=params._SerializerPayment,
        )
        return await self._base_client.request(
            method="POST",
            path="/payments",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )
