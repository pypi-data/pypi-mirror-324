
### get <a name="get"></a>
Get a specific refund transaction by request Id

Get a specific refund transaction by request Id.

**API Endpoint**: `GET /refunds`

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
res = client.refunds.get(
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
res = await client.refunds.get(
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    request_identifier="12cc0270-7bed-11e9-a188-1763956dd7f6",
)
```

### get_by_id <a name="get_by_id"></a>
Get a specific refund transaction by transaction Id

Get a specific refund transaction by transaction Id

**API Endpoint**: `GET /refunds/{id}`

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
res = client.refunds.get_by_id(
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
res = await client.refunds.get_by_id(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
)
```

### create <a name="create"></a>
Create a refund

Creates a refund request and returns funds to the consumer. 1. For refund associated with a previous payment, send transactionReferenceId. 2. For standalone refunds, send order and payment objects.

**API Endpoint**: `POST /refunds`

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
res = client.refunds.create(
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        }
    },
    merchant_id="000017904371",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    account_on_file="STORED",
    amount=1234,
    currency="USD",
    initiator_type="CARDHOLDER",
    payment_method_type={
        "transaction_reference": {
            "transaction_reference_id": "669b0915-af58-42b9-8815-ad375a658adb"
        }
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
res = await client.refunds.create(
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        }
    },
    merchant_id="000017904371",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    account_on_file="STORED",
    amount=1234,
    currency="USD",
    initiator_type="CARDHOLDER",
    payment_method_type={
        "transaction_reference": {
            "transaction_reference_id": "669b0915-af58-42b9-8815-ad375a658adb"
        }
    },
)
```
