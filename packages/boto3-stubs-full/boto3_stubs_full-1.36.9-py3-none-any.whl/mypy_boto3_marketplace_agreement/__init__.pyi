"""
Main interface for marketplace-agreement service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplace_agreement import (
        AgreementServiceClient,
        Client,
    )

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import AgreementServiceClient

Client = AgreementServiceClient

__all__ = ("AgreementServiceClient", "Client")
