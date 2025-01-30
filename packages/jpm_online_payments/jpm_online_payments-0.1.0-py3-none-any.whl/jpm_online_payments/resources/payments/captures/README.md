
### create <a name="create"></a>
Capture a payment

Capture a payment request for existing authorized transaction

**API Endpoint**: `POST /payments/{id}/captures`

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
res = client.payments.captures.create(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6",
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    amount=100,
    currency="USD",
    multi_capture={
        "is_final_capture": True,
        "multi_capture_record_count": 2,
        "multi_capture_sequence_number": "2",
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
res = await client.payments.captures.create(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6",
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    amount=100,
    currency="USD",
    multi_capture={
        "is_final_capture": True,
        "multi_capture_record_count": 2,
        "multi_capture_sequence_number": "2",
    },
)
```
