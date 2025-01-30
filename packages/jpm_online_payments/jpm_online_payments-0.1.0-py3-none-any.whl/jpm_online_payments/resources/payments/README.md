
### get <a name="get"></a>
Get a specific payment transaction by request Id

Request Original Authorization Transaction details

**API Endpoint**: `GET /payments`

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
res = client.payments.get(
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
res = await client.payments.get(
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    request_identifier="12cc0270-7bed-11e9-a188-1763956dd7f6",
)
```

### get_by_id <a name="get_by_id"></a>
Get a specific payment transaction by transaction Id

Get a specific payment transaction by transaction Id

**API Endpoint**: `GET /payments/{id}`

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
res = client.payments.get_by_id(
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
res = await client.payments.get_by_id(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6", merchant_id="991234567890"
)
```

### patch <a name="patch"></a>
Update payment transaction by transaction Id

Update an existing payment 1.Capture a payment for settlement. 2. Void a payment and authorization. The transaction will not settle. 3. Update a payment.

**API Endpoint**: `PATCH /payments/{id}`

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
res = client.payments.patch(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6",
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    capture_method="NOW",
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
res = await client.payments.patch(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6",
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    capture_method="NOW",
)
```

### create <a name="create"></a>
Create a payment

Create a payment request with a specified payment instrument. Authorization and Sale (Authorization and capture).

**API Endpoint**: `POST /payments`

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
res = client.payments.create(
    amount=10000,
    currency="USD",
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        },
        "soft_merchant": {
            "merchant_purchase_description": "Merchant Purchase Description"
        },
    },
    merchant_id="991234567890",
    payment_method_type={
        "ach": {
            "account_number": "1111111111111111",
            "account_type": "CHECKING",
            "financial_institution_routing_number": "123456789",
        }
    },
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    account_holder={"first_name": "JANE", "last_name": "SMITH"},
    capture_method="NOW",
    statement_descriptor="Statement Descriptor",
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
res = await client.payments.create(
    amount=10000,
    currency="USD",
    merchant={
        "merchant_software": {
            "company_name": "Payment Company",
            "product_name": "Application Name",
            "version": "1.235",
        },
        "soft_merchant": {
            "merchant_purchase_description": "Merchant Purchase Description"
        },
    },
    merchant_id="991234567890",
    payment_method_type={
        "ach": {
            "account_number": "1111111111111111",
            "account_type": "CHECKING",
            "financial_institution_routing_number": "123456789",
        }
    },
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    account_holder={"first_name": "JANE", "last_name": "SMITH"},
    capture_method="NOW",
    statement_descriptor="Statement Descriptor",
)
```
