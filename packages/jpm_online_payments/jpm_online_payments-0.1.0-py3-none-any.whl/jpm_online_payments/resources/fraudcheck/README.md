
### get <a name="get"></a>
Retrieve fraud response

Retrieve fraud score of a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

**API Endpoint**: `GET /fraudcheck`

#### Synchronous Client

```python
from jpm_online_payments import Client
from os import getenv

client = Client(
    auth={
        "client_id": getenv("OAUTH_CLIENT_ID"),
        "client_secret": getenv("OAUTH_CLIENT_SECRET"),
    }
)
res = client.fraudcheck.get(
    merchant_id="991234567890", request_id="10cc0270-7bed-11e9-a188-1763956dd7f6"
)
```

#### Asynchronous Client

```python
from jpm_online_payments import AsyncClient
from os import getenv

client = AsyncClient(
    auth={
        "client_id": getenv("OAUTH_CLIENT_ID"),
        "client_secret": getenv("OAUTH_CLIENT_SECRET"),
    }
)
res = await client.fraudcheck.get(
    merchant_id="991234567890", request_id="10cc0270-7bed-11e9-a188-1763956dd7f6"
)
```

### get_by_id <a name="get_by_id"></a>
Retrieve fraud response

Retrieve fraud score of a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

**API Endpoint**: `GET /fraudcheck/{id}`

#### Synchronous Client

```python
from jpm_online_payments import Client
from os import getenv

client = Client(
    auth={
        "client_id": getenv("OAUTH_CLIENT_ID"),
        "client_secret": getenv("OAUTH_CLIENT_SECRET"),
    }
)
res = client.fraudcheck.get_by_id(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
)
```

#### Asynchronous Client

```python
from jpm_online_payments import AsyncClient
from os import getenv

client = AsyncClient(
    auth={
        "client_id": getenv("OAUTH_CLIENT_ID"),
        "client_secret": getenv("OAUTH_CLIENT_SECRET"),
    }
)
res = await client.fraudcheck.get_by_id(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
)
```

### create <a name="create"></a>
Fraud check

Validate a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

**API Endpoint**: `POST /fraudcheck`

#### Synchronous Client

```python
from jpm_online_payments import Client
from os import getenv

client = Client(
    auth={
        "client_id": getenv("OAUTH_CLIENT_ID"),
        "client_secret": getenv("OAUTH_CLIENT_SECRET"),
    }
)
res = client.fraudcheck.create(
    amount=10000,
    currency="USD",
    merchant_id="991234567890",
    payment_method_type={
        "card": {
            "account_number": "401200cpGlDovRz0026",
            "account_number_type": "SAFETECH_PAGE_ENCRYPTION",
            "cvv": "517",
            "encryption_integrity_check": "80df99ee3467e264",
            "expiry": {"month": 5, "year": 2024},
        }
    },
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    account_holder={
        "billing_address": {
            "city": "Tampa",
            "line1": "123 some street",
            "line2": "Apartment 3b",
            "postal_code": "33626",
            "state": "FL",
        },
        "consumer_id_creation_date": "2021-09-01",
        "device_ip_address": "127.0.0.1",
        "driver_license_number": "T000-000-0000",
        "email_field": "john.dow@abc.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": {"country_code": 1, "phone_number": "6035551234"},
        "reference_id": "12122012",
    },
    fraud_score={
        "a_ni_telephone_number": "5131234567",
        "cardholder_browser_information": "cardholderBrowserInformation",
        "fencible_item_amount": 1230,
        "is_fraud_rule_return": True,
        "session_id": "d38e582e-27e1-4748-811b-79281f3bb714",
    },
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        }
    },
    ship_to={
        "shipping_address": {
            "city": "Tampa",
            "line1": "123 some street",
            "line2": "Apartment 3b",
            "postal_code": "33626",
            "state": "FL",
        },
        "shipping_description": "C",
    },
)
```

#### Asynchronous Client

```python
from jpm_online_payments import AsyncClient
from os import getenv

client = AsyncClient(
    auth={
        "client_id": getenv("OAUTH_CLIENT_ID"),
        "client_secret": getenv("OAUTH_CLIENT_SECRET"),
    }
)
res = await client.fraudcheck.create(
    amount=10000,
    currency="USD",
    merchant_id="991234567890",
    payment_method_type={
        "card": {
            "account_number": "401200cpGlDovRz0026",
            "account_number_type": "SAFETECH_PAGE_ENCRYPTION",
            "cvv": "517",
            "encryption_integrity_check": "80df99ee3467e264",
            "expiry": {"month": 5, "year": 2024},
        }
    },
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    account_holder={
        "billing_address": {
            "city": "Tampa",
            "line1": "123 some street",
            "line2": "Apartment 3b",
            "postal_code": "33626",
            "state": "FL",
        },
        "consumer_id_creation_date": "2021-09-01",
        "device_ip_address": "127.0.0.1",
        "driver_license_number": "T000-000-0000",
        "email_field": "john.dow@abc.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": {"country_code": 1, "phone_number": "6035551234"},
        "reference_id": "12122012",
    },
    fraud_score={
        "a_ni_telephone_number": "5131234567",
        "cardholder_browser_information": "cardholderBrowserInformation",
        "fencible_item_amount": 1230,
        "is_fraud_rule_return": True,
        "session_id": "d38e582e-27e1-4748-811b-79281f3bb714",
    },
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        }
    },
    ship_to={
        "shipping_address": {
            "city": "Tampa",
            "line1": "123 some street",
            "line2": "Apartment 3b",
            "postal_code": "33626",
            "state": "FL",
        },
        "shipping_description": "C",
    },
)
```
