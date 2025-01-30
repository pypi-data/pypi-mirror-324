"""
Main interface for healthlake service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_healthlake import (
        Client,
        HealthLakeClient,
    )

    session = Session()
    client: HealthLakeClient = session.client("healthlake")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import HealthLakeClient

Client = HealthLakeClient

__all__ = ("Client", "HealthLakeClient")
