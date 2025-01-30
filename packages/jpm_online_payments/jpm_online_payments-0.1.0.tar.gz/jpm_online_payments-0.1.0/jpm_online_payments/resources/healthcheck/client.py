import typing

from jpm_online_payments.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
)
from jpm_online_payments.types import models


class HealthcheckClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def payments_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.HealthCheckResource:
        """
        Health check for payments

        Health check for payments

        GET /healthcheck/payments

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.healthcheck.payments_status()
        ```

        """
        return self._base_client.request(
            method="GET",
            path="/healthcheck/payments",
            auth_names=["auth"],
            cast_to=models.HealthCheckResource,
            request_options=request_options or default_request_options(),
        )

    def refunds_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.HealthCheckResource:
        """
        Health check for refunds

        Health check for refunds

        GET /healthcheck/refunds

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.healthcheck.refunds_status()
        ```

        """
        return self._base_client.request(
            method="GET",
            path="/healthcheck/refunds",
            auth_names=["auth"],
            cast_to=models.HealthCheckResource,
            request_options=request_options or default_request_options(),
        )

    def verifications_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.HealthCheckResource:
        """
        Health check for verifications

        Health check for verifications

        GET /healthcheck/verifications

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.healthcheck.verifications_status()
        ```

        """
        return self._base_client.request(
            method="GET",
            path="/healthcheck/verifications",
            auth_names=["auth"],
            cast_to=models.HealthCheckResource,
            request_options=request_options or default_request_options(),
        )


class AsyncHealthcheckClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def payments_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.HealthCheckResource:
        """
        Health check for payments

        Health check for payments

        GET /healthcheck/payments

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.healthcheck.payments_status()
        ```

        """
        return await self._base_client.request(
            method="GET",
            path="/healthcheck/payments",
            auth_names=["auth"],
            cast_to=models.HealthCheckResource,
            request_options=request_options or default_request_options(),
        )

    async def refunds_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.HealthCheckResource:
        """
        Health check for refunds

        Health check for refunds

        GET /healthcheck/refunds

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.healthcheck.refunds_status()
        ```

        """
        return await self._base_client.request(
            method="GET",
            path="/healthcheck/refunds",
            auth_names=["auth"],
            cast_to=models.HealthCheckResource,
            request_options=request_options or default_request_options(),
        )

    async def verifications_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.HealthCheckResource:
        """
        Health check for verifications

        Health check for verifications

        GET /healthcheck/verifications

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.healthcheck.verifications_status()
        ```

        """
        return await self._base_client.request(
            method="GET",
            path="/healthcheck/verifications",
            auth_names=["auth"],
            cast_to=models.HealthCheckResource,
            request_options=request_options or default_request_options(),
        )
