"""
Main interface for savingsplans service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_savingsplans import (
        Client,
        SavingsPlansClient,
    )

    session = Session()
    client: SavingsPlansClient = session.client("savingsplans")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import SavingsPlansClient

Client = SavingsPlansClient


__all__ = ("Client", "SavingsPlansClient")
