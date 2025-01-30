"""
Main interface for iot-data service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iot_data import (
        Client,
        IoTDataPlaneClient,
        ListRetainedMessagesPaginator,
    )

    session = Session()
    client: IoTDataPlaneClient = session.client("iot-data")

    list_retained_messages_paginator: ListRetainedMessagesPaginator = client.get_paginator("list_retained_messages")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import IoTDataPlaneClient
from .paginator import ListRetainedMessagesPaginator

Client = IoTDataPlaneClient

__all__ = ("Client", "IoTDataPlaneClient", "ListRetainedMessagesPaginator")
