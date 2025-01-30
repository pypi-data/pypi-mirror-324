
### get <a name="get"></a>
Retrieve Payment Details

Request capture details for a specific capture request

**API Endpoint**: `GET /captures`

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
res = client.captures.get(
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    request_identifier="10cc0270-7bed-11e9-a188-1763956dd7f6",
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
res = await client.captures.get(
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
    request_identifier="10cc0270-7bed-11e9-a188-1763956dd7f6",
)
```

### get_by_id <a name="get_by_id"></a>
Retrieve Payment Details by transaction Id

Request capture details for a specific capture request by captureId

**API Endpoint**: `GET /captures/{id}`

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
res = client.captures.get_by_id(
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
res = await client.captures.get_by_id(
    id="12cc0270-7bed-11e9-a188-1763956dd7f6",
    merchant_id="991234567890",
    request_id="10cc0270-7bed-11e9-a188-1763956dd7f6",
)
```
