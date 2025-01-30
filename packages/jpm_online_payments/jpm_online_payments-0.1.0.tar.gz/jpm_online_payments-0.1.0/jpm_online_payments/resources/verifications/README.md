
### get <a name="get"></a>
Get a specific verification transaction by request Id

Get a specific verification transaction by request Id.

**API Endpoint**: `GET /verifications`

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
res = client.verifications.get(
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    request_identifier="12cc0270-7bed-11e9-a188-1763956dd7f6",
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
res = await client.verifications.get(
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    request_identifier="12cc0270-7bed-11e9-a188-1763956dd7f6",
)
```

### get_by_id <a name="get_by_id"></a>
Get a specific verification transaction by transaction Id

Get a specific verification transaction by transaction Id.

**API Endpoint**: `GET /verifications/{id}`

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
res = client.verifications.get_by_id(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6",
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
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
res = await client.verifications.get_by_id(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6",
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
)
```

### create <a name="create"></a>
Verify a payment instrument

Validate a payment instrument with cardholder information without placing a funds hold on the consumer account (Not supported by all payment methods)

**API Endpoint**: `POST /verifications`

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
res = client.verifications.create(
    currency="USD",
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        }
    },
    merchant_id="991234567890",
    payment_method_type={
        "card": {
            "account_number": "4012000033330026",
            "expiry": {"month": 5, "year": 2027},
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
        }
    },
    account_on_file="NOT_STORED",
    initiator_type="CARDHOLDER",
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
res = await client.verifications.create(
    currency="USD",
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        }
    },
    merchant_id="991234567890",
    payment_method_type={
        "card": {
            "account_number": "4012000033330026",
            "expiry": {"month": 5, "year": 2027},
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
        }
    },
    account_on_file="NOT_STORED",
    initiator_type="CARDHOLDER",
)
```
