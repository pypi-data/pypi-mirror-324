"""
Main interface for codeguruprofiler service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codeguruprofiler import (
        Client,
        CodeGuruProfilerClient,
        ListProfileTimesPaginator,
    )

    session = Session()
    client: CodeGuruProfilerClient = session.client("codeguruprofiler")

    list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import CodeGuruProfilerClient
from .paginator import ListProfileTimesPaginator

Client = CodeGuruProfilerClient


__all__ = ("Client", "CodeGuruProfilerClient", "ListProfileTimesPaginator")
