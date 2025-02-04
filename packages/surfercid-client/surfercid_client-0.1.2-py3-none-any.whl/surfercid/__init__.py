"""
SurferCID API Client
~~~~~~~~~~~~~~~~~~~

A Python client for interacting with the SurferCID API.

Basic usage:

    >>> from surfercid import SurferCIDClient
    >>> client = SurferCIDClient(api_key="your_api_key")
    >>> order = client.purchase(product_name="ltoken", quantity=1)
    >>> for account in order.accounts:
    ...     print(account.to_format())

:copyright: (c) 2024 by SurferCID
:license: MIT, see LICENSE for more details.
"""

from .client import SurferCIDClient
from .models import (
    Account,
    CIDAccount,
    MailAccount,
    UbiConnectAccount,
    LTokenAccount,
    OrderResponse,
)

__version__ = "0.1.0"
__all__ = [
    "SurferCIDClient",
    "Account",
    "CIDAccount",
    "MailAccount",
    "UbiConnectAccount",
    "LTokenAccount",
    "OrderResponse",
] 