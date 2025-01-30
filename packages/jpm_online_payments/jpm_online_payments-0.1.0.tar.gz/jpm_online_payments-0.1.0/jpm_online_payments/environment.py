import enum


class Environment(enum.Enum):
    PROD = "https://api-ms.payments.jpmorgan.com/api/v2"
    MOCK = "https://api-mock.payments.jpmorgan.com/api/v2"
    MOCK_SERVER = (
        "https://api.sideko-staging.dev/v1/mock/sideko-octa/jpm-online-payments/0.1.0"
    )
