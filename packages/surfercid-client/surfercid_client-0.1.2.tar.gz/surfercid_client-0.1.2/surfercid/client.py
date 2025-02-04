"""
SurferCID API client implementation.
"""

from typing import Optional, Dict, Any, List, Union
from datetime import datetime
import requests

from .models import (
    Account,
    CIDAccount,
    MailAccount,
    UbiConnectAccount,
    LTokenAccount,
    OrderResponse,
)


class SurferCIDClient:
    """
    Client for interacting with the SurferCID API.
    
    This client provides methods to interact with all SurferCID API endpoints,
    including purchasing accounts, managing orders, and refreshing tokens.
    
    Example:
        >>> from surfercid import SurferCIDClient
        >>> client = SurferCIDClient(api_key="your_api_key")
        >>> order = client.purchase(product_name="ltoken", quantity=1)
        >>> for account in order.accounts:
        ...     print(account.to_format())
    """

    BASE_URL = "https://cid.surferwallet.net/publicApi"

    def __init__(self, api_key: str):
        """
        Initialize the SurferCID API client.
        
        Args:
            api_key (str): Your API key for authentication
        """
        self.api_key = api_key
        
    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method (str): HTTP method to use
            endpoint (str): API endpoint to call
            data (Dict[str, Any], optional): Request data. Defaults to None.
            
        Returns:
            Dict[str, Any]: API response data
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        
        if data is None:
            data = {}
            
        if method.upper() == "GET":
            # For GET requests, add apikey as query parameter
            params = {"apikey": self.api_key}
            if data:
                params.update(data)
            response = requests.get(url, params=params)
        else:
            headers = {"Content-Type": "application/json"}
            # For other methods (POST, etc), add apikey to the JSON body
            data["apikey"] = self.api_key
            response = requests.request(method, url, json=data, headers=headers)
            
        response.raise_for_status()
        return response.json()
    
    def refresh_token(self, token_data: Union[str, LTokenAccount]) -> LTokenAccount:
        """
        Refresh a token using the refreshToken endpoint.
        
        Args:
            token_data (Union[str, LTokenAccount]): Either a formatted token string (RID|MAC|PLATFORM|TOKEN)
                                                  or an LTokenAccount instance
            
        Returns:
            LTokenAccount: A new LTokenAccount instance with the refreshed token
            
        Raises:
            ValueError: If the token format is invalid or response is unsuccessful
            requests.exceptions.RequestException: If the API request fails
            
        Example:
            >>> account = client.purchase(product_name="ltoken", quantity=1).accounts[0]
            >>> refreshed = client.refresh_token(account)
            >>> print(f"New token: {refreshed.token}")
        """
        # Get original token parts for later use
        if isinstance(token_data, LTokenAccount):
            original_account = token_data
            token = token_data.token  # Just use the token value
        elif isinstance(token_data, str):
            # Parse the token string to get original values
            parts = token_data.split('|')
            if len(parts) != 4:
                raise ValueError("Invalid token format. Expected: RID|MAC|PLATFORM|TOKEN")
            original_account = LTokenAccount(
                created_at=datetime.now().isoformat(),
                rid=parts[0],
                mac=parts[1],
                platform=parts[2],
                name="",  # We don't have this from the formatted string
                token=parts[3]
            )
            token = parts[3]  # Just use the token part
        else:
            raise ValueError("token_data must be either a string or LTokenAccount instance")

        data = {
            "token": token  # Only send the token value
        }
        
        response = self._make_request("POST", "refreshToken", data)
        
        # Check if the request was successful
        if not response.get("success", False):
            raise ValueError(f"Token refresh failed: {response.get('message', 'Unknown error')}")
            
        # Get the new token from the response
        new_token = response.get("token")
        if not new_token:
            raise ValueError("No token in response")
            
        # Create a new LTokenAccount with the refreshed token
        return LTokenAccount(
            created_at=datetime.now().isoformat(),  # Update creation time to now
            mac=original_account.mac,
            name=original_account.name,
            platform=original_account.platform,
            rid=original_account.rid,
            token=new_token
        )
    
    def _parse_account(self, acc_data: Dict[str, Any], product_type: Optional[str] = None) -> Account:
        """
        Parse account data into appropriate Account type.
        
        Args:
            acc_data (Dict[str, Any]): Raw account data
            product_type (Optional[str]): Product type if known
            
        Returns:
            Account: Parsed account object
            
        Raises:
            ValueError: If the account type cannot be determined
        """
        if product_type == "cid" or "growid" in acc_data:
            return CIDAccount(**acc_data)
        elif product_type == "mail" or ("mail" in acc_data and "password" in acc_data and len(acc_data) == 2):
            return MailAccount(**acc_data)
        elif product_type == "ubiconnect" or "email" in acc_data:
            return UbiConnectAccount(**acc_data)
        elif product_type == "ltoken" or all(key in acc_data for key in ["created_at", "mac", "name", "platform", "rid", "token"]):
            return LTokenAccount(**acc_data)
        raise ValueError(f"Unknown account type: {acc_data}")
    
    def get_stock(self, product_name: str) -> Dict[str, Any]:
        """
        Get stock information for a specific product.
        
        Args:
            product_name (str): Name of the product (e.g., "ltoken", "old_account")
            
        Returns:
            Dict[str, Any]: Stock information containing:
                - available (int): Number of items in stock
                - price (float): Price per item
                - enabled (bool): Whether the product is enabled
            
        Example:
            >>> stock = client.get_stock("ltoken")
            >>> print(f"Available: {stock['available']}, Price: ${stock['price']}")
        """
        response = self._make_request("GET", "stock")
        
        # Convert product name to lowercase for case-insensitive comparison
        product_name = product_name.lower()
        
        # Search through products list
        for product in response.get("products", []):
            if product["name"].lower() == product_name:
                return {
                    "available": product["instock"],
                    "price": product["price"],
                    "enabled": product["enabled"]
                }
                
        # If product not found, return empty stock
        return {
            "available": 0,
            "price": 0,
            "enabled": False,
            "error": f"Product '{product_name}' not found"
        }
    
    def get_balance(self) -> float:
        """
        Get current balance of the account.
        
        Returns:
            float: Current balance
            
        Example:
            >>> balance = client.get_balance()
            >>> print(f"Current balance: ${balance}")
        """
        response = self._make_request("GET", "getBalance")
        return float(response.get("balance", 0))
    
    def purchase(self, product_name: str, quantity: int) -> OrderResponse:
        """
        Purchase products from the service.
        
        Args:
            product_name (str): Name of the product to purchase
            quantity (int): Number of items to purchase
            
        Returns:
            OrderResponse: Purchase response with order details
            
        Example:
            >>> order = client.purchase(product_name="ltoken", quantity=2)
            >>> for account in order.accounts:
            ...     print(account.to_format())
        """
        data = {
            "name": product_name,
            "quantity": quantity
        }
        
        response = self._make_request("POST", "purchase", data)
        accounts = [
            self._parse_account(acc_data, product_name)
            for acc_data in response.get("accounts", [])
        ]
            
        return OrderResponse(
            accounts=accounts,
            message=response.get("message", ""),
            success=response.get("success", False),
            cost=response.get("cost", 0),
            order_id=response.get("orderID", 0),
            order_date=datetime.fromisoformat(response.get("orderDate").replace('Z', '+00:00'))
        )
    
    def get_order(self, order_id: int) -> OrderResponse:
        """
        Get details of a specific order.
        
        Args:
            order_id (int): ID of the order to retrieve
            
        Returns:
            OrderResponse: Order details
            
        Example:
            >>> order = client.get_order(123)
            >>> print(f"Order cost: ${order.cost}")
        """
        data = {"orderID": order_id}
        response = self._make_request("GET", "getOrder", data)
        
        accounts = [
            self._parse_account(acc_data)
            for acc_data in response.get("accounts", [])
        ]
            
        return OrderResponse(
            accounts=accounts,
            message=response.get("message", ""),
            success=response.get("success", False),
            cost=response.get("cost", 0),
            order_id=response.get("orderID", 0),
            order_date=datetime.fromisoformat(response.get("orderDate").replace('Z', '+00:00'))
        )
    
    def get_orders(self, limit: Optional[int] = None) -> List[OrderResponse]:
        """
        Get list of orders.
        
        Args:
            limit (Optional[int]): Maximum number of orders to retrieve
            
        Returns:
            List[OrderResponse]: List of orders
            
        Example:
            >>> orders = client.get_orders(limit=5)
            >>> for order in orders:
            ...     print(f"Order {order.order_id}: ${order.cost}")
        """
        data = {}
        if limit is not None:
            data["limit"] = limit
            
        response = self._make_request("GET", "getOrders", data)
        orders = []
        
        for order_data in response.get("orders", []):
            accounts = [
                self._parse_account(acc_data)
                for acc_data in order_data.get("accounts", [])
            ]
                
            orders.append(OrderResponse(
                accounts=accounts,
                message=order_data.get("message", ""),
                success=order_data.get("success", False),
                cost=order_data.get("cost", 0),
                order_id=order_data.get("orderID", 0),
                order_date=datetime.fromisoformat(order_data.get("orderDate").replace('Z', '+00:00'))
            ))
            
        return orders 