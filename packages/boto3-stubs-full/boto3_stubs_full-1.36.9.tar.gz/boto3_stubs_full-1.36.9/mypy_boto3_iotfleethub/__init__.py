"""
Main interface for iotfleethub service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotfleethub import (
        Client,
        IoTFleetHubClient,
        ListApplicationsPaginator,
    )

    session = Session()
    client: IoTFleetHubClient = session.client("iotfleethub")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import IoTFleetHubClient
from .paginator import ListApplicationsPaginator

Client = IoTFleetHubClient


__all__ = ("Client", "IoTFleetHubClient", "ListApplicationsPaginator")
