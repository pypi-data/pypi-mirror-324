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


class FraudcheckClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.FraudCheckResponse:
        """
        Retrieve fraud response

        Retrieve fraud score of a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        GET /fraudcheck

        Args:
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
        client.fraudcheck.get(
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
            path="/fraudcheck",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.FraudCheckResponse,
            request_options=request_options or default_request_options(),
        )

    def get_by_id(
        self,
        *,
        id: str,
        merchant_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.FraudCheckResponse:
        """
        Retrieve fraud response

        Retrieve fraud score of a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        GET /fraudcheck/{id}

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
        client.fraudcheck.get_by_id(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        return self._base_client.request(
            method="GET",
            path=f"/fraudcheck/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.FraudCheckResponse,
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
        merchant_id: str,
        payment_method_type: params.FraudCheckPaymentMethodType,
        request_id: str,
        account_holder: typing.Union[
            typing.Optional[params.AccountHolderInformation], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        fraud_score: typing.Union[
            typing.Optional[params.FraudScore], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant: typing.Union[
            typing.Optional[params.Merchant], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        ship_to: typing.Union[
            typing.Optional[params.FraudShipTo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.FraudCheckResponse:
        """
        Fraud check

        Validate a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        POST /fraudcheck

        Args:
            accountHolder: Information about the card Account Holder for which fraud checking is performed.
            fraudScore: Object for Fraud Score Information
            merchant: Information about the merchant
            shipTo: Ship To Information used for fraud checking services.
            amount: Total monetary value of the payment including all taxes and fees.
            currency: Describes the currency type of the transaction
            merchant-id: Identifier for the merchant account
            paymentMethodType: Object with information for Payment Method Type for  Fraud Check
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.fraudcheck.create(
            amount=1234,
            currency="AED",
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
                "fraud_score": fraud_score,
                "merchant": merchant,
                "ship_to": ship_to,
                "amount": amount,
                "currency": currency,
                "payment_method_type": payment_method_type,
            },
            dump_with=params._SerializerFraudCheckRequest,
        )
        return self._base_client.request(
            method="POST",
            path="/fraudcheck",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.FraudCheckResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncFraudcheckClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.FraudCheckResponse:
        """
        Retrieve fraud response

        Retrieve fraud score of a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        GET /fraudcheck

        Args:
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
        await client.fraudcheck.get(
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
            path="/fraudcheck",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.FraudCheckResponse,
            request_options=request_options or default_request_options(),
        )

    async def get_by_id(
        self,
        *,
        id: str,
        merchant_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.FraudCheckResponse:
        """
        Retrieve fraud response

        Retrieve fraud score of a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        GET /fraudcheck/{id}

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
        await client.fraudcheck.get_by_id(
            id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
        )
        ```

        """
        _header: typing.Dict[str, str] = {}
        _header["merchant-id"] = str(encode_param(merchant_id, False))
        return await self._base_client.request(
            method="GET",
            path=f"/fraudcheck/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.FraudCheckResponse,
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
        merchant_id: str,
        payment_method_type: params.FraudCheckPaymentMethodType,
        request_id: str,
        account_holder: typing.Union[
            typing.Optional[params.AccountHolderInformation], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        fraud_score: typing.Union[
            typing.Optional[params.FraudScore], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        merchant: typing.Union[
            typing.Optional[params.Merchant], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        ship_to: typing.Union[
            typing.Optional[params.FraudShipTo], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.FraudCheckResponse:
        """
        Fraud check

        Validate a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

        POST /fraudcheck

        Args:
            accountHolder: Information about the card Account Holder for which fraud checking is performed.
            fraudScore: Object for Fraud Score Information
            merchant: Information about the merchant
            shipTo: Ship To Information used for fraud checking services.
            amount: Total monetary value of the payment including all taxes and fees.
            currency: Describes the currency type of the transaction
            merchant-id: Identifier for the merchant account
            paymentMethodType: Object with information for Payment Method Type for  Fraud Check
            request-id: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.fraudcheck.create(
            amount=1234,
            currency="AED",
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
                "fraud_score": fraud_score,
                "merchant": merchant,
                "ship_to": ship_to,
                "amount": amount,
                "currency": currency,
                "payment_method_type": payment_method_type,
            },
            dump_with=params._SerializerFraudCheckRequest,
        )
        return await self._base_client.request(
            method="POST",
            path="/fraudcheck",
            auth_names=["auth"],
            headers=_header,
            json=_json,
            cast_to=models.FraudCheckResponse,
            request_options=request_options or default_request_options(),
        )
