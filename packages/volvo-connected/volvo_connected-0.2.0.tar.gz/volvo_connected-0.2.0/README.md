# Volvo Connected Vehicle API

This is an unofficial Python client for the [Volvo Connected Vehicle API](https://developer.volvocars.com/apis/connected-vehicle/v2/overview/). It is based on the [official API documentation](https://developer.volvocars.com/apis/connected-vehicle/v2/specification/).

Source: [svrooij/py_volvo_connected](https://github.com/svrooij/py_volvo_connected)

## Installation

```bash
pip install volvo-connected
```

## Usage

```python
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from volvo_connected import (
  StaticAccessTokenProvider,
  # DynamicAccessTokenProvider,
  VolvoAuthenticationProvider,
  VolvoConnectedClient
)

# Create an access token provider using a static access token
access_token_provider = StaticAccessTokenProvider("YOUR_ACCESS_TOKEN")

# Or explore the DynamicAccessTokenProvider that allows you to auto refresh the token

# def access_token_function(url: str) -> str:
#   # Implement your logic to get the access token using the URL
#   return "your_dynamic_access_token"
# access_token_provider = DynamicAccessTokenProvider(access_token_function)

# Create an authentication provider using your VCC API key and the access token provider
auth_provider = VolvoAuthenticationProvider("YOUR_VCC_API_KEY", access_token_provider)

# Create a client with a request adapter that has the authentication provider
client = VolvoConnectedClient(HttpxRequestAdapter(auth_provider))
```

### Get all vehicles

```python
vehicles = await client.vehicles.get()
```

### Get vehicle by VIN

```python
vehicle = await client.vehicles.by_vin("YV4952NA4F120DEMO").get()
```

### Get Fuel or Battery level

```python
fuel_resp = await client.vehicles.by_vin("YV4952NA4F120DEMO").fuel.get()

fuel_resp.data.fuel_amount.value
# or
fuel_resp.data.battery_charge_level.value
```

### All other endpoints

This client is genereted based on the (adjusted) OpenAPI specification. And everything is strong typed, so go ahead and explore the API.