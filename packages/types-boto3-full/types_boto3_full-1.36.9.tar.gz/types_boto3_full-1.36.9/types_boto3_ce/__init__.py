"""
Main interface for ce service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ce import (
        Client,
        CostExplorerClient,
    )

    session = Session()
    client: CostExplorerClient = session.client("ce")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import CostExplorerClient

Client = CostExplorerClient


__all__ = ("Client", "CostExplorerClient")
