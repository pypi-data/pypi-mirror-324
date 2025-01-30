"""
Main interface for kendra service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_kendra import (
        Client,
        KendraClient,
    )

    session = Session()
    client: KendraClient = session.client("kendra")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import KendraClient

Client = KendraClient


__all__ = ("Client", "KendraClient")
