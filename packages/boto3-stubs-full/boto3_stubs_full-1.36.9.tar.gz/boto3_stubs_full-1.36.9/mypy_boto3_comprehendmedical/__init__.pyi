"""
Main interface for comprehendmedical service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_comprehendmedical import (
        Client,
        ComprehendMedicalClient,
    )

    session = Session()
    client: ComprehendMedicalClient = session.client("comprehendmedical")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ComprehendMedicalClient

Client = ComprehendMedicalClient

__all__ = ("Client", "ComprehendMedicalClient")
