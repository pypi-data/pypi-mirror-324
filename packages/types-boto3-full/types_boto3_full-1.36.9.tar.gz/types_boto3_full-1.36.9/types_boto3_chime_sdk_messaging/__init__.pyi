"""
Main interface for chime-sdk-messaging service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_chime_sdk_messaging import (
        ChimeSDKMessagingClient,
        Client,
    )

    session = Session()
    client: ChimeSDKMessagingClient = session.client("chime-sdk-messaging")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ChimeSDKMessagingClient

Client = ChimeSDKMessagingClient

__all__ = ("ChimeSDKMessagingClient", "Client")
