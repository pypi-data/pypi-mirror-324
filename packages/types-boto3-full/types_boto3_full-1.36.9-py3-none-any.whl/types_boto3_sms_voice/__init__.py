"""
Main interface for sms-voice service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sms_voice import (
        Client,
        PinpointSMSVoiceClient,
    )

    session = Session()
    client: PinpointSMSVoiceClient = session.client("sms-voice")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import PinpointSMSVoiceClient

Client = PinpointSMSVoiceClient


__all__ = ("Client", "PinpointSMSVoiceClient")
