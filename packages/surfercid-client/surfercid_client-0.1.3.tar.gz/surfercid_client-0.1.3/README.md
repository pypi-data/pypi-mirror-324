# SurferCID API Client

A Python client for interacting with the SurferCID API. This client provides easy access to SurferCID's services including purchasing accounts, checking orders, and managing balance.

## Project Structure

```
surfercid_client/
├── models.py           # Data models and response types
├── surfercid_client.py # Main API client implementation
└── requirements.txt    # Project dependencies
```

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from surfercid import SurferCIDClient
from surfercid.models import LTokenAccount

# Initialize the client
client = SurferCIDClient(api_key="your_api_key_here")

# Get stock information for a product
stock_info = client.get_stock("Ltoken")
print("Stock Info: ",stock_info)

# Check account balance
balance = client.get_balance()
print("Balance: ",balance)

# Example of working with LToken accounts
ltoken_order = client.purchase(product_name="Ltoken", quantity=1)

for account in ltoken_order.accounts:
    if isinstance(account, LTokenAccount):
        # Refresh token and get new LTokenAccount
        refreshed = client.refresh_token(account)
        print(f"Original token: {account.token}")
        print(f"Refreshed token: {refreshed.token}")
        # RID|MAC|PLATFORM|TOKEN
        print(f"New formatted token: {refreshed.to_format()}") 
```

## Available Methods

- `get_stock(product_name: str) -> Dict[str, Any]`: Get stock information for a specific product
- `get_balance() -> float`: Get current account balance
- `purchase(product_name: str, quantity: int) -> OrderResponse`: Purchase products
- `get_order(order_id: int) -> OrderResponse`: Get details of a specific order
- `get_orders(limit: Optional[int] = None) -> List[OrderResponse]`: Get list of orders
- `refresh_token(token_data: Union[str, LTokenAccount]) -> LTokenAccount`: Refresh an LToken. Returns a new LTokenAccount instance with the refreshed token. Accepts either a formatted token string or an LTokenAccount instance.

## Data Models

### Account Types
All account types inherit from the base `Account` class:

#### CIDAccount
```python
@dataclass
class CIDAccount(Account):
    growid: str
    password: str
    mail: str
    mail_pass: str
```

#### MailAccount
```python
@dataclass
class MailAccount(Account):
    mail: str
    password: str
```

#### UbiConnectAccount
```python
@dataclass
class UbiConnectAccount(Account):
    email: str
    password: str
    number: str
    secret_code: str
    recovery_codes: List[str]
```

#### LTokenAccount
```python
@dataclass
class LTokenAccount(Account):
    created_at: str
    mac: str
    name: str
    platform: str
    rid: str
    token: str

    def to_format(self) -> str:
        """Convert to RID|MAC|PLATFORM|TOKEN format"""
        return f"{self.rid}|{self.mac}|{self.platform}|{self.token}"
```

### OrderResponse
```python
@dataclass
class OrderResponse:
    accounts: List[Account]
    message: str
    success: bool
    cost: float
    order_id: int
    order_date: datetime
```

## Error Handling

The client will raise appropriate HTTP exceptions if the API requests fail. Make sure to handle these exceptions in your code:

```python
from requests.exceptions import RequestException

try:
    # Refresh a token
    refreshed = client.refresh_token(account)
except RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Invalid token or unsuccessful response: {e}")