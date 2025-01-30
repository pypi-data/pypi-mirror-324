import httpx
import typing

from jpm_online_payments.core import (
    AsyncBaseClient,
    AuthBearer,
    GrantType,
    OAuth2,
    OAuth2ClientCredentialsForm,
    SyncBaseClient,
)
from jpm_online_payments.environment import Environment
from jpm_online_payments.resources.captures import (
    AsyncCapturesClient,
    CapturesClient,
)
from jpm_online_payments.resources.fraudcheck import (
    AsyncFraudcheckClient,
    FraudcheckClient,
)
from jpm_online_payments.resources.healthcheck import (
    AsyncHealthcheckClient,
    HealthcheckClient,
)
from jpm_online_payments.resources.payments import (
    AsyncPaymentsClient,
    PaymentsClient,
)
from jpm_online_payments.resources.refunds import AsyncRefundsClient, RefundsClient
from jpm_online_payments.resources.verifications import (
    AsyncVerificationsClient,
    VerificationsClient,
)


class Client:
    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None,
        environment: Environment = Environment.PROD,
        auth: typing.Optional[OAuth2ClientCredentialsForm] = None,
    ):
        self._base_client = SyncBaseClient(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            httpx_client=(
                httpx.Client(timeout=timeout) if httpx_client is None else httpx_client
            ),
        )

        self.captures = CapturesClient(base_client=self._base_client)

        self.fraudcheck = FraudcheckClient(base_client=self._base_client)

        self.healthcheck = HealthcheckClient(base_client=self._base_client)

        self.payments = PaymentsClient(base_client=self._base_client)

        self.refunds = RefundsClient(base_client=self._base_client)

        self.verifications = VerificationsClient(base_client=self._base_client)
        self._base_client.register_auth(
            "auth",
            OAuth2(
                token_url="https://id.payments.jpmorgan.com/am/oauth2/alpha/access_token",
                access_token_pointer="/access_token",
                expires_in_pointer="/expires_in",
                credentials_location="basic_authorization_header",
                body_content="form",
                grant_type=typing.cast(
                    GrantType,
                    auth.get("grant_type", "client_credentials")
                    if auth
                    else "client_credentials",
                ),
                client_id=None if not auth else auth.get("client_id"),
                client_secret=None if not auth else auth.get("client_secret"),
                scope=None if not auth else auth.get("scope"),
                request_mutator=AuthBearer(val=None),
            ),
        )


class AsyncClient:
    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        environment: Environment = Environment.PROD,
        auth: typing.Optional[OAuth2ClientCredentialsForm] = None,
    ):
        self._base_client = AsyncBaseClient(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            httpx_client=(
                httpx.AsyncClient(timeout=timeout)
                if httpx_client is None
                else httpx_client
            ),
        )

        self.captures = AsyncCapturesClient(base_client=self._base_client)

        self.fraudcheck = AsyncFraudcheckClient(base_client=self._base_client)

        self.healthcheck = AsyncHealthcheckClient(base_client=self._base_client)

        self.payments = AsyncPaymentsClient(base_client=self._base_client)

        self.refunds = AsyncRefundsClient(base_client=self._base_client)

        self.verifications = AsyncVerificationsClient(base_client=self._base_client)
        self._base_client.register_auth(
            "auth",
            OAuth2(
                token_url="https://id.payments.jpmorgan.com/am/oauth2/alpha/access_token",
                access_token_pointer="/access_token",
                expires_in_pointer="/expires_in",
                credentials_location="basic_authorization_header",
                body_content="form",
                grant_type=typing.cast(
                    GrantType,
                    auth.get("grant_type", "client_credentials")
                    if auth
                    else "client_credentials",
                ),
                client_id=None if not auth else auth.get("client_id"),
                client_secret=None if not auth else auth.get("client_secret"),
                scope=None if not auth else auth.get("scope"),
                request_mutator=AuthBearer(val=None),
            ),
        )


def _get_base_url(
    *, base_url: typing.Optional[str] = None, environment: Environment
) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Must include a base_url or environment arguments")
