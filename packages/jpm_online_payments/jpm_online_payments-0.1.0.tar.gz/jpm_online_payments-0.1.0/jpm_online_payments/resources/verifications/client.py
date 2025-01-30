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
from jpm_online_payments.types import models, params


class VerificationsClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_identifier: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.VerificationResponse:
        """
        Get a specific verification transaction by request Id

        Get a specific verification transaction by request Id.

        GET /verifications

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
        client.verifications.get(
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
            path="/verifications",
            auth_names=["auth"],
            query_params=_query,
            headers=_header,
            cast_to=models.VerificationResponse,
            request_options=request_options or default_request_options(),
        )

    def get_by_id(
        self,
        *,
        id: str,
        merchant_id: str,
        request_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.VerificationResponse:
        """
        Get a specific verification transaction by transaction Id

        Get a specific verification transaction by transaction Id.

        GET /verifications/{id}

        Args:
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
        client.verifications.get_by_id(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6",
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        _header["request-id"] = str(encode_param(request_id, False))
        return self._base_client.request(
            method="GET",
            path=f"/verifications/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.VerificationResponse,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
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
        payment_method_type: params.VerificationPaymentMethodType,
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
        browser_info: typing.Union[
            typing.Optional[params.BrowserInfo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        initiator_type: typing.Union[
            typing.Optional[typing_extensions.Literal["CARDHOLDER", "MERCHANT"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        installment: typing.Union[
            typing.Optional[params.Installment], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mandate: typing.Union[
            typing.Optional[params.Mandate], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_order_number: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        payment_metadata_list: typing.Union[
            typing.Optional[typing.List[params.PaymentMetadata]], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        recurring_sequence: typing.Union[
            typing.Optional[typing_extensions.Literal["FIRST", "SUBSEQUENT"]],
            type_utils.NotGiven,
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
        website_short_merchant_universal_resource_locator_text: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.VerificationResponse:
        """
        Verify a payment instrument

        Validate a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        POST /verifications

        Args:
            accountHolder: Card owner properties
            accountOnFile: Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
            browserInfo: Browser Information of the consumer
            initiatorType: Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
            installment: Object containing information in the file
            mandate: Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
            merchantOrderNumber: A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
            paymentMetadataList: Payment Metadata List
            recurringSequence: Identifies whether payment is the first in a series of recurring payments or a subsequent payment. Required for recurring billing.
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            transactionRoutingOverrideList: List of transaction routing providers where the transaction be routed preferred by the merchant .
            websiteShortMerchantUniversalResourceLocatorText: Provides textual information about data for the protocol for specifying addresses on the Internet (Universal Resource Locator - URL) for the merchant's organization.
            currency: Describes the currency type of the transaction
            merchant: Information about the merchant
            merchant-id: Identifier for the merchant account
            paymentMethodType: Object with one of the payment method type applicable for verification processing
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.verifications.create(
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
                "browser_info": browser_info,
                "initiator_type": initiator_type,
                "installment": installment,
                "mandate": mandate,
                "merchant_order_number": merchant_order_number,
                "payment_metadata_list": payment_metadata_list,
                "recurring_sequence": recurring_sequence,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
                "transaction_routing_override_list": transaction_routing_override_list,
                "website_short_merchant_universal_resource_locator_text": website_short_merchant_universal_resource_locator_text,
                "currency": currency,
                "merchant": merchant,
                "payment_method_type": payment_method_type,
            },
            dump_with=params._SerializerVerification,
        )
        return self._base_client.request(
            method="POST",
            path="/verifications",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.VerificationResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncVerificationsClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_identifier: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.VerificationResponse:
        """
        Get a specific verification transaction by request Id

        Get a specific verification transaction by request Id.

        GET /verifications

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
        await client.verifications.get(
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
            path="/verifications",
            auth_names=["auth"],
            query_params=_query,
            headers=_header,
            cast_to=models.VerificationResponse,
            request_options=request_options or default_request_options(),
        )

    async def get_by_id(
        self,
        *,
        id: str,
        merchant_id: str,
        request_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.VerificationResponse:
        """
        Get a specific verification transaction by transaction Id

        Get a specific verification transaction by transaction Id.

        GET /verifications/{id}

        Args:
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
        await client.verifications.get_by_id(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6",
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        _header["request-id"] = str(encode_param(request_id, False))
        return await self._base_client.request(
            method="GET",
            path=f"/verifications/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.VerificationResponse,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
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
        payment_method_type: params.VerificationPaymentMethodType,
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
        browser_info: typing.Union[
            typing.Optional[params.BrowserInfo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        initiator_type: typing.Union[
            typing.Optional[typing_extensions.Literal["CARDHOLDER", "MERCHANT"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        installment: typing.Union[
            typing.Optional[params.Installment], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mandate: typing.Union[
            typing.Optional[params.Mandate], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant_order_number: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        payment_metadata_list: typing.Union[
            typing.Optional[typing.List[params.PaymentMetadata]], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        recurring_sequence: typing.Union[
            typing.Optional[typing_extensions.Literal["FIRST", "SUBSEQUENT"]],
            type_utils.NotGiven,
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
        website_short_merchant_universal_resource_locator_text: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.VerificationResponse:
        """
        Verify a payment instrument

        Validate a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        POST /verifications

        Args:
            accountHolder: Card owner properties
            accountOnFile: Indicates whether payment method is stored by merchant. Possible values:STORED - Use if already stored and current payment is either cardholder-initiated stored payment or subsequent recurring or installment transaction. NOT_STORED - Use when payment method obtained for purpose of single payment. TO_BE_STORED - Use when consumer is intentionally storing their payment method after this payment for subsequent recurring or stored payments.
            browserInfo: Browser Information of the consumer
            initiatorType: Describes the initiator of the transaction for the stored credential framework (MIT/CIT)
            installment: Object containing information in the file
            mandate: Agreement information between the consumer, debtor bank (checking account of the consumer) and the merchant for debit funds.
            merchantOrderNumber: A unique merchant assigned identifier for the confirmation of goods and/or services purchased. The merchant order provides the merchant a reference to the prices, quantity and description of goods and/or services to be delivered for all transactions included in the sale.
            paymentMetadataList: Payment Metadata List
            recurringSequence: Identifies whether payment is the first in a series of recurring payments or a subsequent payment. Required for recurring billing.
            subMerchantSupplementalData: Additional data provided by merchant for reference purposes.
            transactionRoutingOverrideList: List of transaction routing providers where the transaction be routed preferred by the merchant .
            websiteShortMerchantUniversalResourceLocatorText: Provides textual information about data for the protocol for specifying addresses on the Internet (Universal Resource Locator - URL) for the merchant's organization.
            currency: Describes the currency type of the transaction
            merchant: Information about the merchant
            merchant-id: Identifier for the merchant account
            paymentMethodType: Object with one of the payment method type applicable for verification processing
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.verifications.create(
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
                "browser_info": browser_info,
                "initiator_type": initiator_type,
                "installment": installment,
                "mandate": mandate,
                "merchant_order_number": merchant_order_number,
                "payment_metadata_list": payment_metadata_list,
                "recurring_sequence": recurring_sequence,
                "sub_merchant_supplemental_data": sub_merchant_supplemental_data,
                "transaction_routing_override_list": transaction_routing_override_list,
                "website_short_merchant_universal_resource_locator_text": website_short_merchant_universal_resource_locator_text,
                "currency": currency,
                "merchant": merchant,
                "payment_method_type": payment_method_type,
            },
            dump_with=params._SerializerVerification,
        )
        return await self._base_client.request(
            method="POST",
            path="/verifications",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.VerificationResponse,
            request_options=request_options or default_request_options(),
        )
