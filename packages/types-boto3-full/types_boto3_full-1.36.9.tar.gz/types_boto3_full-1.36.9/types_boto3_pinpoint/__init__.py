"""
Main interface for pinpoint service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_pinpoint import (
        Client,
        PinpointClient,
    )

    session = Session()
    client: PinpointClient = session.client("pinpoint")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import PinpointClient

Client = PinpointClient


__all__ = ("Client", "PinpointClient")
