"""
Main interface for dlm service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_dlm import (
        Client,
        DLMClient,
    )

    session = Session()
    client: DLMClient = session.client("dlm")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import DLMClient

Client = DLMClient


__all__ = ("Client", "DLMClient")
