"""
AZTP (Astha Zero Trust Platform) Client Library for Python
"""

from aztp_client.client import AztpClient
from aztp_client.common.types import SecuredAgent, Identity

__version__ = "0.1.0"
__all__ = ["AztpClient", "SecuredAgent", "Identity"] 