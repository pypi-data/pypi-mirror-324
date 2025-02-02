# EnydayPy

An unofficial Python client for the Enyday API. This library provides a convenient way to interact with Enyday's services for energy consumption monitoring and management.

## Installation

```bash
pip install EnydayPy
```
## Quick Start

First, set up your environment variables with your Enyday account credentials in a `.env` file:	

```bash	
ENYDAY_USERNAME=your_email@example.com
ENYDAY_PASSWORD=your_password
```

Then, you can start using the library:

```python
import os
import enyday
from enyday.configuration import Configuration
from enyday.api_client import ApiClient
from enyday.api.authorization_api import AuthorizationApi
from dotenv import load_dotenv

# Load credentials from environment
load_dotenv()
username = os.getenv("ENYDAY_USERNAME")
password = os.getenv("ENYDAY_PASSWORD")

# Configure the client
configuration = Configuration(
    host="https://app.enyday.com/connected/api"
)

# Initialize and authenticate
with ApiClient(configuration) as client:
    auth_api = AuthorizationApi(client)
    auth_response = auth_api.get_auth_token(
        enyday.AuthRequest(email=username, password=password)
    )
    print(f"Successfully authenticated: {auth_response.auth_token}")
```

## Advanced Usage

### Fetching Power Consumption Data

```python
from datetime import datetime, timedelta
import pytz

# Set up date range
end_date = datetime.now(pytz.UTC)
start_date = end_date - timedelta(days=7)

# Get consumption data
consumption_api = ConsumptionDataApi(client)
power_data = consumption_api.get_hourly_power_data(
    begin=start_date,
    end=end_date,
    user_id=user_id,
    address_id=address_id
)
print(power_data)
```
### Address

```python
address_api = AddressApi(client)
addresses = address_api.get_addresses_by_user_id(user_id=user_id)
print(addresses)
```

## Features
- Authentication and authorization
- User management
- Address management
- Power consumption data retrieval
- Nordpool cost data access
- Timezone-aware datetime handling
- Optional DataFrame output format

## Requirements
- Python 3.7+
- python-dotenv
- Valid Enyday account credentials

## License
MIT License - see LICENSE file for details.

## Author
- @bruadam