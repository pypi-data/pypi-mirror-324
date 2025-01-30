"""
Main interface for personalize-events service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_personalize_events import (
        Client,
        PersonalizeEventsClient,
    )

    session = Session()
    client: PersonalizeEventsClient = session.client("personalize-events")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import PersonalizeEventsClient

Client = PersonalizeEventsClient

__all__ = ("Client", "PersonalizeEventsClient")
