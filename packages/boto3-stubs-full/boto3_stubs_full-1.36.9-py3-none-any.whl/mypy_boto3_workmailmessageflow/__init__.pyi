"""
Main interface for workmailmessageflow service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_workmailmessageflow import (
        Client,
        WorkMailMessageFlowClient,
    )

    session = Session()
    client: WorkMailMessageFlowClient = session.client("workmailmessageflow")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import WorkMailMessageFlowClient

Client = WorkMailMessageFlowClient

__all__ = ("Client", "WorkMailMessageFlowClient")
