import typing

from jpm_online_payments.core import (
    AsyncBaseClient,
    QueryParams,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_param,
)
from jpm_online_payments.types import models


class CapturesClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_identifier: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Retrieve Payment Details

        Request capture details for a specific capture request

        GET /captures

        Args:
            merchant-id: Identifier for the merchant account
            request-id: Merchant identifier for the request. The value must be unique.
            requestIdentifier: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.captures.get(
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
            request_identifier="10cc0270-7bed-11e9-a188-1763956dd7f6",
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
            path="/captures",
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
        request_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Retrieve Payment Details by transaction Id

        Request capture details for a specific capture request by captureId

        GET /captures/{id}

        Args:
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
        client.captures.get_by_id(
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
            path=f"/captures/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncCapturesClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def get(
        self,
        *,
        merchant_id: str,
        request_id: str,
        request_identifier: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Retrieve Payment Details

        Request capture details for a specific capture request

        GET /captures

        Args:
            merchant-id: Identifier for the merchant account
            request-id: Merchant identifier for the request. The value must be unique.
            requestIdentifier: Merchant identifier for the request. The value must be unique.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.captures.get(
            merchant_id="991234567890",
            request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
            request_identifier="10cc0270-7bed-11e9-a188-1763956dd7f6",
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
            path="/captures",
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
        request_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.PaymentResponse:
        """
        Retrieve Payment Details by transaction Id

        Request capture details for a specific capture request by captureId

        GET /captures/{id}

        Args:
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
        await client.captures.get_by_id(
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
            path=f"/captures/{id}",
            auth_names=["auth"],
            headers=_header,
            cast_to=models.PaymentResponse,
            request_options=request_options or default_request_options(),
        )
