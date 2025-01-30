"""
Main interface for workspaces-thin-client service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_workspaces_thin_client import (
        Client,
        ListDevicesPaginator,
        ListEnvironmentsPaginator,
        ListSoftwareSetsPaginator,
        WorkSpacesThinClientClient,
    )

    session = Session()
    client: WorkSpacesThinClientClient = session.client("workspaces-thin-client")

    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_software_sets_paginator: ListSoftwareSetsPaginator = client.get_paginator("list_software_sets")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import WorkSpacesThinClientClient
from .paginator import ListDevicesPaginator, ListEnvironmentsPaginator, ListSoftwareSetsPaginator

Client = WorkSpacesThinClientClient

__all__ = (
    "Client",
    "ListDevicesPaginator",
    "ListEnvironmentsPaginator",
    "ListSoftwareSetsPaginator",
    "WorkSpacesThinClientClient",
)
