"""
Data models for the SurferCID API client.
"""

from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Account:
    """Base class for account data types."""
    pass


@dataclass
class LTokenAccount(Account):
    """
    Account model for LToken product type.
    
    Attributes:
        created_at (str): ISO format timestamp of when the token was created
        mac (str): MAC address associated with the token
        name (str): Account name
        platform (str): Platform identifier
        rid (str): Resource identifier
        token (str): Authentication token
    """
    created_at: str
    mac: str
    name: str
    platform: str
    rid: str
    token: str

    def to_format(self) -> str:
        """
        Convert the account data to RID|MAC|PLATFORM|TOKEN format.
        
        Returns:
            str: Formatted string in the format RID|MAC|PLATFORM|TOKEN
            
        Example:
            >>> account = LTokenAccount(...)
            >>> print(account.to_format())
            'RID123|00:11:22:33:44:55|1|TOKEN123'
        """
        return f"{self.rid}|{self.mac}|{self.platform}|{self.token}"

    @classmethod
    def from_format(cls, formatted_str: str, name: str = "") -> "LTokenAccount":
        """
        Create an LTokenAccount instance from a formatted string.
        
        Args:
            formatted_str (str): String in RID|MAC|PLATFORM|TOKEN format
            name (str, optional): Account name. Defaults to empty string.
            
        Returns:
            LTokenAccount: New instance with the parsed data
            
        Raises:
            ValueError: If the string format is invalid
            
        Example:
            >>> token_str = "RID123|00:11:22:33:44:55|1|TOKEN123"
            >>> account = LTokenAccount.from_format(token_str)
        """
        try:
            rid, mac, platform, token = formatted_str.split("|")
            return cls(
                created_at=datetime.now().isoformat(),
                mac=mac,
                name=name,
                platform=platform,
                rid=rid,
                token=token
            )
        except ValueError:
            raise ValueError("Invalid format. Expected RID|MAC|PLATFORM|TOKEN")


@dataclass
class CIDAccount(Account):
    """
    Account model for CID product type.
    
    Attributes:
        growid (str): Grow ID for the account
        password (str): Account password
        mail (str): Email address
        mail_pass (str): Email password
    """
    growid: str
    password: str
    mail: str
    mail_pass: str


@dataclass
class MailAccount(Account):
    """
    Account model for Mail product type.
    
    Attributes:
        mail (str): Email address
        password (str): Email password
    """
    mail: str
    password: str


@dataclass
class UbiConnectAccount(Account):
    """
    Account model for UbiConnect product type.
    
    Attributes:
        email (str): Email address
        password (str): Account password
        number (str): Phone number
        secret_code (str): Secret code for authentication
        recovery_codes (List[str]): List of recovery codes
    """
    email: str
    password: str
    number: str
    secret_code: str
    recovery_codes: List[str]


@dataclass
class OrderResponse:
    """
    Response model for order-related operations.
    
    Attributes:
        accounts (List[Account]): List of purchased accounts
        message (str): Response message
        success (bool): Whether the operation was successful
        cost (float): Order cost
        order_id (int): Unique order identifier
        order_date (datetime): Date and time of the order
    """
    accounts: List[Account]
    message: str
    success: bool
    cost: float
    order_id: int
    order_date: datetime 